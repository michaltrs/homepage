#!/usr/bin/env python3
"""
Fix dead links in archive HTML files based on validation-report.json.
Replaces <a href="dead-url">text</a> with <span class="dead-link">text <small>(stránka již neexistuje)</small></span>
"""

import json
import re
import os
from pathlib import Path

ARCHIVE_DIR = Path(__file__).resolve().parent.parent / "public" / "archive"
REPORT_FILE = Path(__file__).resolve().parent / "validation-report.json"

# Statuses to treat as dead (replace the link)
DEAD_STATUSES = {
    "HTTP 404", "HTTP 410", "HTTP 400", "HTTP 500",
}

# Patterns in error messages that indicate truly dead
DEAD_PATTERNS = [
    "nodename nor servname",
    "Connection refused",
    "Name or service not known",
    "all methods failed",
]

# URLs to NOT replace (403 sites that likely just block bots)
SKIP_URLS = {
    # These return 403 but are probably alive (blocking bots)
    "http://www.canon.cz/produkty/zrcadlovky/eos400d/index.htm",
    "http://www.canon.cz/produkty/objektivy/17-85mm/index.htm",
    "http://www.sejmi-cyklistu.cz/",  # not in dead list but just in case
}

# URLs where we know a redirect/replacement
REDIRECT_REPLACEMENTS = {}


def is_dead(url, message):
    """Determine if a URL should be marked as dead."""
    if url in SKIP_URLS:
        return False
    for status in DEAD_STATUSES:
        if message.startswith(status):
            return True
    for pattern in DEAD_PATTERNS:
        if pattern in message:
            return True
    return False


def replace_dead_link_in_html(html, url, is_img=False):
    """Replace <a href="url">text</a> with dead-link span in HTML content."""
    changes = 0

    # Escape URL for regex (handle special chars)
    escaped_url = re.escape(url)

    if is_img:
        # For dead images: replace <img src="url"...> with a placeholder text
        pattern = re.compile(
            r'<img\s[^>]*src\s*=\s*["\']' + escaped_url + r'["\'][^>]*/?>',
            re.IGNORECASE
        )
        replacement = '<span class="dead-link"><small>(obrázek již není dostupný)</small></span>'
        new_html, n = pattern.subn(replacement, html)
        if n:
            html = new_html
            changes += n

    # For <a> tags: replace link with dead-link span, keeping anchor text
    # Match <a href="url" ...>text</a>
    pattern = re.compile(
        r'<a\s[^>]*href\s*=\s*["\']' + escaped_url + r'["\'][^>]*>(.*?)</a>',
        re.IGNORECASE | re.DOTALL
    )

    def replace_match(m):
        anchor_text = m.group(1).strip()
        if not anchor_text or anchor_text == url:
            return '<span class="dead-link"><small>(odkaz již neexistuje)</small></span>'
        return f'<span class="dead-link">{anchor_text} <small>(stránka již neexistuje)</small></span>'

    new_html, n = pattern.subn(replace_match, html)
    if n:
        html = new_html
        changes += n

    return html, changes


def main():
    with open(REPORT_FILE) as f:
        report = json.load(f)

    # Build map: html_file -> set of (url, is_img) to fix
    fixes = {}
    for html_rel, tag, url, anchor, message in report["broken_external"]:
        if not is_dead(url, message):
            continue
        if html_rel not in fixes:
            fixes[html_rel] = set()
        is_img = tag == "img"
        fixes[html_rel].add((url, is_img))

    # Also fix broken external images
    for html_rel, url in report.get("broken_images", []):
        if url.startswith("http"):
            if html_rel not in fixes:
                fixes[html_rel] = set()
            fixes[html_rel].add((url, True))

    print(f"Files to fix: {len(fixes)}")
    total_changes = 0

    for html_rel, url_set in sorted(fixes.items()):
        html_path = ARCHIVE_DIR / html_rel
        if not html_path.exists():
            print(f"  SKIP (not found): {html_rel}")
            continue

        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        file_changes = 0
        for url, is_img in url_set:
            html, n = replace_dead_link_in_html(html, url, is_img)
            file_changes += n

        if file_changes:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  {html_rel}: {file_changes} replacements")
            total_changes += file_changes
        else:
            print(f"  {html_rel}: no matches found (already fixed?)")

    print(f"\nTotal: {total_changes} replacements in {len(fixes)} files")


if __name__ == "__main__":
    main()
