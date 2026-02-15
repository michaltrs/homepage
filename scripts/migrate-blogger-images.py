#!/usr/bin/env python3
"""Download all blogger.googleusercontent.com images and update HTML references."""

import os
import re
import hashlib
import urllib.request
import urllib.error
import ssl
from pathlib import Path

ARCHIVE_DIR = Path("public/archive")
OUTPUT_DIR = Path("public/assets/migrated/blog")
# Relative path from archive HTML files to the migrated images
ASSET_PATH = "/assets/migrated/blog"

def find_blogger_urls():
    """Find all blogger.googleusercontent.com URLs in archive HTML files."""
    url_pattern = re.compile(r'https://blogger\.googleusercontent\.com/[^"\'>\s]+')
    results = []  # (file_path, url)

    for html_file in sorted(ARCHIVE_DIR.rglob("*.html")):
        content = html_file.read_text(encoding="utf-8")
        for match in url_pattern.finditer(content):
            results.append((html_file, match.group(0)))

    return results

def url_to_filename(url):
    """Extract a unique filename from a blogger URL.

    URL pattern: .../s{size}/{filename}
    We use: {filename} (with short hash prefix if collision)
    """
    # Get the original filename from URL
    parts = url.rstrip("/").split("/")
    filename = parts[-1]
    # URL-decode percent-encoded chars
    filename = urllib.request.url2pathname(filename).replace("/", "_")
    # Get the size part (s200, s1600, etc.)
    size_part = parts[-2] if len(parts) >= 2 else "unknown"
    # Create a short hash from the full URL (minus the size) to handle collisions
    base_url = "/".join(parts[:-2])
    url_hash = hashlib.md5(base_url.encode()).hexdigest()[:6]

    name, ext = os.path.splitext(filename)
    return f"{name}-{size_part}-{url_hash}{ext}"

def download_image(url, dest_path):
    """Download an image from URL to dest_path."""
    if dest_path.exists():
        print(f"  SKIP (exists): {dest_path.name}")
        return True

    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = resp.read()
            dest_path.write_bytes(data)
            size_kb = len(data) / 1024
            print(f"  OK ({size_kb:.0f}KB): {dest_path.name}")
            return True
    except Exception as e:
        print(f"  FAIL: {url} -> {e}")
        return False

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Find all URLs
    print("=== Scanning for Blogger URLs ===")
    all_refs = find_blogger_urls()
    unique_urls = sorted(set(url for _, url in all_refs))
    print(f"Found {len(all_refs)} references across {len(set(f for f, _ in all_refs))} files")
    print(f"Unique URLs: {len(unique_urls)}")

    # Step 2: Build URL -> local filename mapping
    url_to_local = {}
    for url in unique_urls:
        local_name = url_to_filename(url)
        url_to_local[url] = local_name

    # Step 3: Download all images
    print(f"\n=== Downloading {len(unique_urls)} images ===")
    ok = 0
    fail = 0
    for url in unique_urls:
        local_name = url_to_local[url]
        dest = OUTPUT_DIR / local_name
        if download_image(url, dest):
            ok += 1
        else:
            fail += 1

    print(f"\nDownloaded: {ok}, Failed: {fail}")

    # Step 4: Update HTML files
    print(f"\n=== Updating HTML references ===")
    files_updated = set()
    for html_file in sorted(set(f for f, _ in all_refs)):
        content = html_file.read_text(encoding="utf-8")
        original = content

        for url, local_name in url_to_local.items():
            local_path = f"{ASSET_PATH}/{local_name}"
            content = content.replace(url, local_path)

        if content != original:
            html_file.write_text(content, encoding="utf-8")
            files_updated.add(html_file)
            count = original.count("blogger.googleusercontent.com") - content.count("blogger.googleusercontent.com")
            print(f"  Updated: {html_file} ({count} replacements)")

    print(f"\nTotal files updated: {len(files_updated)}")

    # Step 5: Verify no remaining references
    print(f"\n=== Verification ===")
    remaining = find_blogger_urls()
    if remaining:
        print(f"WARNING: {len(remaining)} Blogger URLs still remain!")
        for f, url in remaining:
            print(f"  {f}: {url[:80]}...")
    else:
        print("All Blogger URLs successfully migrated!")

if __name__ == "__main__":
    main()
