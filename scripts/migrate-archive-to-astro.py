#!/usr/bin/env python3
"""
Migrate archive HTML files to Astro pages.

Parses 136 "archive template" HTML files from public/archive/,
extracts title, subtitle, category, and content, generates .astro files
in src/pages/archive/, and deletes the source HTML files (preserving assets).

Only files using /archive/style.css (the archive template) are migrated.
Doxygen docs, university project pages, etc. remain as static HTML.
"""

import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

PROJECT_ROOT = Path(__file__).parent.parent
PUBLIC_ARCHIVE = PROJECT_ROOT / "public" / "archive"
PAGES_ARCHIVE = PROJECT_ROOT / "src" / "pages" / "archive"


def is_archive_template(html: str) -> bool:
    """Check if the HTML file uses the standard archive template."""
    return '/archive/style.css' in html


def extract_title(html: str) -> str:
    """Extract the page title from <h1>."""
    m = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    return m.group(1).strip() if m else ""


def extract_subtitle(html: str) -> str:
    """Extract subtitle from <p><i>...</i></p> in the header div."""
    m = re.search(r'<div class="header">\s*<h1>.*?</h1>\s*<p><i>(.*?)</i></p>', html, re.DOTALL)
    return m.group(1).strip() if m else ""


def detect_category(rel_path: str) -> str:
    """Detect category from the relative file path."""
    parts = rel_path.split(os.sep)
    if len(parts) > 1 and parts[0] in ('blog', 'cnk', 'cvut-fel', 'spse-v-uzlabine'):
        return parts[0]
    return 'root'


def extract_content(html: str) -> str:
    """Extract the body content between header and footer, excluding nav/header/footer/script."""
    # Find end of header div
    header_match = re.search(
        r'<div class="header">\s*<h1>.*?</h1>\s*<p><i>.*?</i></p>\s*</div>',
        html, re.DOTALL
    )
    if not header_match:
        return ""

    after_header = html[header_match.end():]

    # Find the footer div
    footer_match = re.search(r'\s*<div class="footer">', after_header)
    if footer_match:
        content = after_header[:footer_match.start()]
    else:
        # Fallback: find </body>
        body_end = after_header.find('</body>')
        if body_end != -1:
            content = after_header[:body_end]
        else:
            content = after_header

    # Remove trailing lightbox script tags
    content = re.sub(r'\s*<script\s+src="/archive/lightbox\.js"\s*>\s*</script>\s*$', '', content)

    # Strip leading/trailing whitespace but preserve internal formatting
    content = content.strip()

    # Strip outer <div class="content">...</div> wrapper if present
    # (ArchiveLayout already wraps content in this div)
    m = re.match(r'^<div class="content">\s*(.*?)\s*</div>\s*$', content, re.DOTALL)
    if m:
        content = m.group(1).strip()

    return content


def compute_astro_path(rel_path: str) -> Path:
    """
    Compute the .astro output path from relative HTML path.

    Rules:
    - blog/foo.html -> blog/foo.astro
    - cnk/2009-maroko/index.html -> cnk/2009-maroko.astro
    - cnk/index.html -> cnk/index.astro
    - cvut-fel/36apc.html -> cvut-fel/36apc.astro
    - era-socialnich-siti.html -> era-socialnich-siti.astro
    """
    parts = Path(rel_path).parts
    name = parts[-1]

    if name == 'index.html':
        if len(parts) >= 3:
            # e.g. cnk/2009-maroko/index.html -> cnk/2009-maroko.astro
            category = parts[0]
            subdir = parts[1]
            return Path(category) / f"{subdir}.astro"
        elif len(parts) == 2:
            # e.g. cnk/index.html -> cnk/index.astro
            category = parts[0]
            return Path(category) / "index.astro"
        else:
            # Shouldn't happen but handle gracefully
            return Path("index.astro")
    else:
        # e.g. blog/foo.html -> blog/foo.astro
        # e.g. era-socialnich-siti.html -> era-socialnich-siti.astro
        stem = Path(name).stem
        if len(parts) >= 2:
            category = parts[0]
            return Path(category) / f"{stem}.astro"
        else:
            return Path(f"{stem}.astro")


def escape_astro_content(content: str) -> str:
    """Escape content that could interfere with Astro template parsing."""
    # Replace curly braces that aren't part of HTML entities
    # We need to be careful not to break HTML entities like &#8364;
    # Astro treats { and } as expression delimiters in the template
    content = content.replace('{', '&#123;')
    content = content.replace('}', '&#125;')
    return content


def generate_astro_file(title: str, subtitle: str, category: str, content: str) -> str:
    """Generate the .astro file content."""
    # Escape special characters in props
    escaped_title = title.replace('"', '&quot;').replace('`', '\\`')
    escaped_subtitle = subtitle.replace('"', '&quot;').replace('`', '\\`')

    # Escape content for Astro template
    escaped_content = escape_astro_content(content)

    return f"""---
import ArchiveLayout from '../{"../" * 0}layouts/ArchiveLayout.astro';
---
<ArchiveLayout title="{escaped_title}" subtitle="{escaped_subtitle}" category="{category}">
{escaped_content}
</ArchiveLayout>
"""


def fix_import_depth(astro_content: str, rel_path: Path) -> str:
    """Fix the import path depth based on the .astro file location."""
    # Count directory depth from src/pages/archive/
    parts = rel_path.parts
    # Files at root (e.g. era-socialnich-siti.astro) need ../../layouts/
    # Files in category (e.g. blog/foo.astro) need ../../../layouts/
    depth = len(parts) - 1  # -1 for the filename itself
    # From src/pages/archive/{depth}/file.astro -> src/layouts/
    # Always need to go up: archive -> pages -> src, then into layouts
    ups = "../" * (depth + 3)  # +3 for archive/pages/src
    # Actually let's just compute properly:
    # file is at src/pages/archive/blog/foo.astro
    # layout is at src/layouts/ArchiveLayout.astro
    # relative: ../../../../src/layouts/... NO
    # from src/pages/archive/blog/foo.astro:
    #   ../../../layouts/ArchiveLayout.astro (up to archive, pages, src... wait no)
    #   ../../.. gets to src/, then /layouts/
    # Let me think again:
    # src/pages/archive/foo.astro -> ../../layouts/ (up archive, up pages)
    # src/pages/archive/blog/foo.astro -> ../../../layouts/ (up blog, up archive, up pages)

    ups = "../" * (depth + 2)  # +2 for going up through archive/ and pages/

    return astro_content.replace(
        "import ArchiveLayout from '../layouts/ArchiveLayout.astro';",
        f"import ArchiveLayout from '{ups}layouts/ArchiveLayout.astro';"
    )


def main():
    if not PUBLIC_ARCHIVE.exists():
        print(f"Error: {PUBLIC_ARCHIVE} does not exist")
        sys.exit(1)

    # Collect all HTML files
    html_files = []
    for root, dirs, files in os.walk(PUBLIC_ARCHIVE):
        for f in files:
            if f.endswith('.html'):
                full_path = Path(root) / f
                rel_path = full_path.relative_to(PUBLIC_ARCHIVE)
                html_files.append((full_path, str(rel_path)))

    print(f"Found {len(html_files)} HTML files in {PUBLIC_ARCHIVE}")

    migrated = 0
    skipped = 0
    errors = []

    for full_path, rel_path in sorted(html_files, key=lambda x: x[1]):
        try:
            html = full_path.read_text(encoding='utf-8')
        except Exception as e:
            errors.append(f"  ERROR reading {rel_path}: {e}")
            continue

        if not is_archive_template(html):
            skipped += 1
            print(f"  SKIP (not template): {rel_path}")
            continue

        title = extract_title(html)
        subtitle = extract_subtitle(html)
        category = detect_category(rel_path)
        content = extract_content(html)

        if not title:
            errors.append(f"  ERROR: no title found in {rel_path}")
            continue

        astro_rel = compute_astro_path(rel_path)
        astro_content = generate_astro_file(title, subtitle, category, content)
        astro_content = fix_import_depth(astro_content, astro_rel)

        # Write .astro file
        astro_full = PAGES_ARCHIVE / astro_rel
        astro_full.parent.mkdir(parents=True, exist_ok=True)
        astro_full.write_text(astro_content, encoding='utf-8')

        # Delete source HTML
        full_path.unlink()

        migrated += 1
        print(f"  OK: {rel_path} -> src/pages/archive/{astro_rel}")

    print(f"\n{'='*60}")
    print(f"Migrated: {migrated}")
    print(f"Skipped:  {skipped} (not archive template)")
    print(f"Errors:   {len(errors)}")
    if errors:
        for e in errors:
            print(e)


if __name__ == "__main__":
    main()
