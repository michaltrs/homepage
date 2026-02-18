#!/usr/bin/env python3
"""
Fix archive links after migration from HTML to Astro.

1. Vault entries (src/content/vault/*.md):
   - .html → trailing slash (e.g. /archive/blog/foo.html → /archive/blog/foo/)
   - .html#anchor → trailing slash + anchor (e.g. /archive/blog/foo.html#more → /archive/blog/foo/#more)

2. Cross-references in archive .astro files (src/pages/archive/**/*.astro):
   - Same .html → clean URL conversion
   - Self-referencing links → replace <a> with <span>

3. CNK index.html → directory slug mapping:
   - /archive/cnk/2009-maroko/index.html → /archive/cnk/2009-maroko/
   - /archive/cnk/2009-maroko/ stays as /archive/cnk/2009-maroko/ (already correct)
"""

import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
VAULT_DIR = PROJECT_ROOT / "src" / "content" / "vault"
ARCHIVE_DIR = PROJECT_ROOT / "src" / "pages" / "archive"


def html_to_clean_url(url: str) -> str:
    """Convert /archive/...html to clean URL with trailing slash."""
    # Handle anchors
    anchor = ""
    if "#" in url:
        url, anchor = url.split("#", 1)
        anchor = "#" + anchor

    # /archive/cnk/2009-maroko/index.html → /archive/cnk/2009-maroko/
    if url.endswith("/index.html"):
        return url[:-len("index.html")] + anchor

    # /archive/blog/foo.html → /archive/blog/foo/
    if url.endswith(".html"):
        return url[:-len(".html")] + "/" + anchor

    return url + anchor


def get_self_url(file_path: Path) -> str:
    """Get the URL that this file resolves to."""
    rel = file_path.relative_to(ARCHIVE_DIR)
    stem = rel.stem
    parent = str(rel.parent)

    if parent == ".":
        return f"/archive/{stem}/"
    else:
        if stem == "index":
            return f"/archive/{parent}/"
        else:
            return f"/archive/{parent}/{stem}/"


def fix_vault_entries():
    """Fix links in vault .md files."""
    changes = []

    for md_file in sorted(VAULT_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        original = content

        # Replace /archive/...html references
        def replace_archive_link(m):
            old = m.group(0)
            new = html_to_clean_url(old)
            if old != new:
                changes.append((md_file.name, old, new))
            return new

        content = re.sub(
            r'/archive/[^\s"\')\]]+\.html(?:#[^\s"\')\]]*)?',
            replace_archive_link,
            content
        )

        if content != original:
            md_file.write_text(content, encoding="utf-8")

    return changes


def fix_archive_cross_refs():
    """Fix cross-references in archive .astro files."""
    changes = []

    for astro_file in sorted(ARCHIVE_DIR.rglob("*.astro")):
        content = astro_file.read_text(encoding="utf-8")
        original = content
        self_url = get_self_url(astro_file)

        # Replace /archive/...html references in href attributes
        def replace_archive_link(m):
            old_url = m.group(1)
            new_url = html_to_clean_url(old_url)
            if old_url != new_url:
                changes.append((str(astro_file.relative_to(PROJECT_ROOT)), old_url, new_url))
            return f'href="{new_url}"'

        content = re.sub(
            r'href="(/archive/[^"]*\.html(?:#[^"]*)?)"',
            replace_archive_link,
            content
        )

        if content != original:
            astro_file.write_text(content, encoding="utf-8")

    return changes


def fix_self_references():
    """Find and flag self-referencing links in archive pages."""
    changes = []

    for astro_file in sorted(ARCHIVE_DIR.rglob("*.astro")):
        content = astro_file.read_text(encoding="utf-8")
        original = content
        self_url = get_self_url(astro_file)

        # Find <a> tags where href points to self
        # Pattern: <a href="/archive/blog/foo/">text</a> on the page /archive/blog/foo/
        def replace_self_ref(m):
            full_match = m.group(0)
            href = m.group(1)
            link_text = m.group(2)

            # Normalize for comparison (strip anchors)
            href_base = href.split("#")[0]
            if href_base.rstrip("/") == self_url.rstrip("/"):
                changes.append((str(astro_file.relative_to(PROJECT_ROOT)), f"self-ref: {href}", f"<span>{link_text}</span>"))
                return f"<span>{link_text}</span>"
            return full_match

        content = re.sub(
            r'<a\s+href="(/archive/[^"]*)"[^>]*>(.*?)</a>',
            replace_self_ref,
            content,
            flags=re.DOTALL
        )

        if content != original:
            astro_file.write_text(content, encoding="utf-8")

    return changes


def main():
    print("=" * 60)
    print("Fixing archive links")
    print("=" * 60)

    print("\n--- Vault entries ---")
    vault_changes = fix_vault_entries()
    for fname, old, new in vault_changes:
        print(f"  {fname}: {old} → {new}")
    print(f"  Total: {len(vault_changes)} replacements")

    print("\n--- Archive cross-references ---")
    xref_changes = fix_archive_cross_refs()
    for fname, old, new in xref_changes:
        print(f"  {fname}: {old} → {new}")
    print(f"  Total: {len(xref_changes)} replacements")

    print("\n--- Self-referencing links ---")
    self_changes = fix_self_references()
    for fname, old, new in self_changes:
        print(f"  {fname}: {old}")
    print(f"  Total: {len(self_changes)} replacements")

    total = len(vault_changes) + len(xref_changes) + len(self_changes)
    print(f"\n{'=' * 60}")
    print(f"Grand total: {total} replacements")


if __name__ == "__main__":
    main()
