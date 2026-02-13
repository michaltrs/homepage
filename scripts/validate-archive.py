#!/usr/bin/env python3
"""
Validate archive content: check all links, images, and embeds.
Generates link-history.md and console report of broken items.
"""

import os
import re
import sys
import ssl
import json
import time
import socket
import urllib.request
import urllib.error
from html.parser import HTMLParser
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

ARCHIVE_DIR = Path(__file__).resolve().parent.parent / "public" / "archive"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "link-history.md"

TIMEOUT = 10
MAX_WORKERS = 10

# Skip checking these URL patterns (known dead / intentionally broken)
SKIP_PATTERNS = []

# Local paths that are routing-only (handled by Astro, not static files)
SKIP_LOCAL_PATHS = {"/vault", "/archive/style.css", "/archive/lightbox.js"}

# User-Agent to avoid being blocked by servers
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class LinkExtractor(HTMLParser):
    """Extract URLs from <a href>, <img src>, <iframe src>, <source src>."""

    def __init__(self):
        super().__init__()
        self.links = []       # (tag, attr, url, anchor_text_or_alt)
        self._current_a = None
        self._a_text = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and "href" in attrs_dict:
            href = attrs_dict["href"]
            self._current_a = href
            self._a_text = ""
        elif tag == "img" and "src" in attrs_dict:
            alt = attrs_dict.get("alt", "")
            self.links.append(("img", "src", attrs_dict["src"], alt))
        elif tag == "iframe" and "src" in attrs_dict:
            self.links.append(("iframe", "src", attrs_dict["src"], ""))
        elif tag == "source" and "src" in attrs_dict:
            self.links.append(("source", "src", attrs_dict["src"], ""))

    def handle_data(self, data):
        if self._current_a is not None:
            self._a_text += data

    def handle_endtag(self, tag):
        if tag == "a" and self._current_a is not None:
            self.links.append(("a", "href", self._current_a, self._a_text.strip()))
            self._current_a = None
            self._a_text = ""


def extract_links(html_path):
    """Parse an HTML file and extract all links."""
    try:
        with open(html_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading {html_path}: {e}")
        return []

    parser = LinkExtractor()
    try:
        parser.feed(content)
    except Exception as e:
        print(f"  ERROR parsing {html_path}: {e}")
        return []

    return parser.links


def classify_url(url):
    """Classify URL as local, external, anchor, mailto, javascript, or data."""
    if not url or url.startswith("#"):
        return "anchor"
    if url.startswith("mailto:"):
        return "mailto"
    if url.startswith("javascript:"):
        return "javascript"
    if url.startswith("data:"):
        return "data"
    if url.startswith("http://") or url.startswith("https://") or url.startswith("//"):
        return "external"
    return "local"


def check_local_file(url, html_path):
    """Check if a local file reference exists on disk."""
    if url.startswith("/"):
        # Absolute path from public root
        public_dir = ARCHIVE_DIR.parent
        local_path = public_dir / url.lstrip("/")
    else:
        # Relative path from current HTML file
        local_path = html_path.parent / url

    # Strip query/fragment
    path_str = str(local_path).split("?")[0].split("#")[0]
    return os.path.exists(path_str), path_str


def check_external_url(url):
    """Check external URL via HTTP HEAD (fallback to GET). Returns (status, message)."""
    if url.startswith("//"):
        url = "https:" + url

    for skip in SKIP_PATTERNS:
        if skip in url:
            return "skipped", "skipped by pattern"

    # Create SSL context that doesn't verify (some old sites have bad certs)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for method in ["HEAD", "GET"]:
        try:
            req = urllib.request.Request(url, method=method, headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,*/*",
            })
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
                code = resp.getcode()
                final_url = resp.geturl()
                if 200 <= code < 300:
                    if final_url != url:
                        return "redirect", f"{code} → {final_url}"
                    return "alive", str(code)
                elif 300 <= code < 400:
                    return "redirect", f"{code}"
                else:
                    return "dead", f"{code}"
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 406, 501):
                continue  # Retry with GET
            return "dead", f"HTTP {e.code}"
        except urllib.error.URLError as e:
            return "dead", f"URLError: {e.reason}"
        except socket.timeout:
            return "dead", "timeout"
        except Exception as e:
            if method == "HEAD":
                continue
            return "dead", f"Error: {type(e).__name__}: {e}"

    return "dead", "all methods failed"


def main():
    print("=" * 60)
    print("Archive Validator — michaltrs.cz")
    print("=" * 60)
    print(f"Archive dir: {ARCHIVE_DIR}")
    print()

    # Find all HTML files
    html_files = sorted(ARCHIVE_DIR.rglob("*.html"))
    print(f"Found {len(html_files)} HTML files")
    print()

    # Data structures
    all_external_links = {}  # url -> (status, message)
    page_data = {}           # rel_path -> [(tag, attr, url, text, url_type)]

    broken_local = []        # (html_rel, tag, url)
    broken_external = []     # (html_rel, tag, url, anchor, status_msg)
    broken_images = []       # (html_rel, url)
    broken_embeds = []       # (html_rel, url)

    external_urls_to_check = {}  # url -> set of (html_rel, tag, anchor)

    # Phase 1: Extract all links
    print("Phase 1: Extracting links from HTML files...")
    for html_path in html_files:
        rel_path = html_path.relative_to(ARCHIVE_DIR)
        links = extract_links(html_path)
        page_entries = []

        for tag, attr, url, text in links:
            url_type = classify_url(url)

            if url_type == "local":
                # Skip routing-only paths (handled by Astro)
                base_url = url.split("?")[0].split("#")[0]
                if base_url in SKIP_LOCAL_PATHS:
                    pass
                else:
                    exists, resolved = check_local_file(url, html_path)
                    if not exists:
                        broken_local.append((str(rel_path), tag, url))
                        if tag == "img":
                            broken_images.append((str(rel_path), url))
                        elif tag == "iframe":
                            broken_embeds.append((str(rel_path), url))

            elif url_type == "external":
                full_url = ("https:" + url) if url.startswith("//") else url
                if full_url not in external_urls_to_check:
                    external_urls_to_check[full_url] = set()
                external_urls_to_check[full_url].add((str(rel_path), tag, text))

            page_entries.append((tag, attr, url, text, url_type))

        page_data[str(rel_path)] = page_entries

    print(f"  Local references checked")
    print(f"  Unique external URLs to check: {len(external_urls_to_check)}")
    print()

    # Phase 2: Check external URLs (parallel)
    print(f"Phase 2: Checking {len(external_urls_to_check)} external URLs...")
    checked = 0
    total = len(external_urls_to_check)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {
            executor.submit(check_external_url, url): url
            for url in external_urls_to_check
        }
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            checked += 1
            try:
                status, message = future.result()
            except Exception as e:
                status, message = "dead", f"Exception: {e}"

            all_external_links[url] = (status, message)

            if status == "dead":
                for html_rel, tag, anchor in external_urls_to_check[url]:
                    broken_external.append((html_rel, tag, url, anchor, message))
                    if tag == "img":
                        broken_images.append((html_rel, url))
                    elif tag == "iframe":
                        broken_embeds.append((html_rel, url))

            if checked % 20 == 0 or checked == total:
                print(f"  [{checked}/{total}] Last: {status} — {url[:80]}")

    print()

    # Phase 3: Console report
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)

    # Stats
    alive_count = sum(1 for s, _ in all_external_links.values() if s == "alive")
    redirect_count = sum(1 for s, _ in all_external_links.values() if s == "redirect")
    dead_count = sum(1 for s, _ in all_external_links.values() if s == "dead")
    skipped_count = sum(1 for s, _ in all_external_links.values() if s == "skipped")

    print(f"\nExternal URLs: {len(all_external_links)} unique")
    print(f"  Alive:     {alive_count}")
    print(f"  Redirect:  {redirect_count}")
    print(f"  Dead:      {dead_count}")
    print(f"  Skipped:   {skipped_count}")

    print(f"\nBroken local refs: {len(broken_local)}")
    print(f"Broken images:     {len(broken_images)}")
    print(f"Broken embeds:     {len(broken_embeds)}")

    if broken_local:
        print(f"\n--- Broken Local References ({len(broken_local)}) ---")
        for html_rel, tag, url in sorted(broken_local):
            print(f"  [{tag}] {html_rel} → {url}")

    if broken_images:
        print(f"\n--- Broken Images ({len(broken_images)}) ---")
        for html_rel, url in sorted(broken_images):
            print(f"  {html_rel} → {url}")

    if broken_embeds:
        print(f"\n--- Broken Embeds ({len(broken_embeds)}) ---")
        for html_rel, url in sorted(broken_embeds):
            print(f"  {html_rel} → {url}")

    if broken_external:
        print(f"\n--- Dead External Links ({len(broken_external)}) ---")
        for html_rel, tag, url, anchor, msg in sorted(broken_external):
            anchor_str = f' "{anchor}"' if anchor else ""
            print(f"  [{tag}] {html_rel} → {url}{anchor_str} — {msg}")

    if redirect_count:
        print(f"\n--- Redirected URLs ({redirect_count}) ---")
        for url, (status, msg) in sorted(all_external_links.items()):
            if status == "redirect":
                print(f"  {url} — {msg}")

    # Phase 4: Generate link-history.md
    print(f"\nPhase 4: Generating {OUTPUT_FILE.name}...")

    lines = []
    lines.append("# Link History — Archiv michaltrs.cz\n")
    lines.append("")
    lines.append("Kompletní seznam externích odkazů z archivu (2001–2013).")
    lines.append("Stav ověřen: únor 2026.\n")
    lines.append("")

    # Group by page
    for rel_path in sorted(page_data.keys()):
        entries = page_data[rel_path]
        external_entries = []
        for tag, attr, url, text, url_type in entries:
            if url_type == "external":
                full_url = ("https:" + url) if url.startswith("//") else url
                status, message = all_external_links.get(full_url, ("unknown", "not checked"))

                if status == "alive":
                    badge = "živý"
                elif status == "redirect":
                    badge = "přesměrován"
                elif status == "dead":
                    badge = "mrtvý"
                elif status == "skipped":
                    badge = "přeskočen"
                else:
                    badge = "neznámý"

                anchor_text = text.strip() if text and text.strip() else ""
                external_entries.append((badge, full_url, anchor_text, tag))

        if external_entries:
            lines.append(f"## {rel_path}")
            for badge, url, anchor, tag in external_entries:
                tag_suffix = f" ({tag})" if tag != "a" else ""
                anchor_suffix = f" — {anchor}" if anchor else ""
                lines.append(f"- [{badge}] {url}{anchor_suffix}{tag_suffix}")
            lines.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  Written to {OUTPUT_FILE}")
    print()

    # Phase 5: JSON dump for further processing
    report_file = Path(__file__).resolve().parent / "validation-report.json"
    report = {
        "broken_local": broken_local,
        "broken_images": broken_images,
        "broken_embeds": broken_embeds,
        "broken_external": [(h, t, u, a, m) for h, t, u, a, m in broken_external],
        "external_links": {url: {"status": s, "message": m} for url, (s, m) in all_external_links.items()},
    }
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"JSON report: {report_file}")

    print("\nDone!")
    return 1 if (broken_local or broken_images or broken_embeds) else 0


if __name__ == "__main__":
    sys.exit(main())
