#!/usr/bin/env python3
"""Fix blog references in archive HTML and vault entries.

Phase 1: Copy referenced images from www-2008-20 to public/assets/migrated/
Phase 2: Fix URLs in 78 blog archive HTML files
Phase 3: Clean up placeholder.jpg references in vault entries
"""

import os
import re
import shutil
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # homepage/
ASTRO_ROOT = PROJECT_ROOT / "michaltrs-hp-astro"
SOURCE_IMAGES = PROJECT_ROOT / "www-2008-20" / "blog" / "uploaded_images"
SOURCE_FILES = PROJECT_ROOT / "www-2008-20" / "blog" / "files"
MIGRATED_DIR = ASTRO_ROOT / "public" / "assets" / "migrated"
ARCHIVE_BLOG = ASTRO_ROOT / "public" / "archive" / "blog"
VAULT_DIR = ASTRO_ROOT / "src" / "content" / "vault"

# Stats
stats = {
    "images_copied": 0,
    "files_copied": 0,
    "html_fixed": 0,
    "vault_fixed": 0,
    "uploaded_images_replaced": 0,
    "blog_crossrefs_replaced": 0,
    "cnk_refs_replaced": 0,
    "blog_files_replaced": 0,
    "picasaweb_fixed": 0,
    "ggpht_removed": 0,
    "embeds_removed": 0,
    "onblur_removed": 0,
    "placeholder_removed": 0,
}


def phase1_copy_images():
    """Copy referenced images from www-2008-20 to public/assets/migrated/."""
    print("\n=== Phase 1: Copy referenced images ===")

    # Collect all referenced filenames from archive HTML
    referenced_images = set()
    referenced_files = set()

    for html_file in ARCHIVE_BLOG.glob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        for m in re.finditer(
            r'michaltrs\.net/blog/uploaded_images/([^"\'>\s]+)', content
        ):
            referenced_images.add(m.group(1))
        for m in re.finditer(
            r'michaltrs\.net/blog/files/([^"\'>\s]+)', content
        ):
            referenced_files.add(m.group(1))

    print(f"  Found {len(referenced_images)} unique image filenames referenced")
    print(f"  Found {len(referenced_files)} unique file filenames referenced")

    MIGRATED_DIR.mkdir(parents=True, exist_ok=True)

    # Copy referenced images
    for filename in sorted(referenced_images):
        src = SOURCE_IMAGES / filename
        dst = MIGRATED_DIR / filename
        if src.exists():
            if not dst.exists():
                shutil.copy2(src, dst)
                stats["images_copied"] += 1
                print(f"  Copied: {filename}")
            else:
                print(f"  Already exists: {filename}")
        else:
            print(f"  WARNING: Source not found: {filename}")

    # Copy referenced files (KMZ etc.)
    for filename in sorted(referenced_files):
        src = SOURCE_FILES / filename
        dst = MIGRATED_DIR / filename
        if src.exists():
            if not dst.exists():
                shutil.copy2(src, dst)
                stats["files_copied"] += 1
                print(f"  Copied: {filename}")
            else:
                print(f"  Already exists: {filename}")
        else:
            print(f"  WARNING: Source not found: {filename}")

    print(f"  → {stats['images_copied']} images copied, {stats['files_copied']} files copied")


def build_blog_crossref_map():
    """Build mapping from Blogger slugs to archive filenames."""
    archive_stems = [f.stem for f in ARCHIVE_BLOG.glob("*.html")]

    # Manual overrides for Blogger slugs that were truncated differently
    MANUAL_MAP = {
        "narodni-parky-usa-parky-v-utahu-zpet-do": "narodni-parky-usa-parky-v-utahu-a-zpet-do-las-vegas-2-tyden",
        "stelvio-pass-jeden-z-vrchol-letonch-kol": "stelvio-pass-jeden-z-vrcholu-letosnich-kol",
        "preview-letonch-alp-orcires-1850": "preview-letosnich-alp-orcieres-1850-francie",
        "nove-levne-shimano-deore-xt-praskly-ram": "nove-levne-shimano-deore-xt-a-praskly-ram-na-me-kone",
    }

    def find_archive_file(blogger_slug):
        """Find archive file matching a Blogger slug (prefix match)."""
        if blogger_slug in MANUAL_MAP:
            return MANUAL_MAP[blogger_slug] + ".html"
        # Direct match
        if blogger_slug in archive_stems:
            return blogger_slug + ".html"
        # Prefix match
        matches = [s for s in archive_stems if s.startswith(blogger_slug)]
        if len(matches) == 1:
            return matches[0] + ".html"
        if len(matches) > 1:
            # Pick shortest match (closest to slug)
            matches.sort(key=len)
            return matches[0] + ".html"
        return None

    return find_archive_file


# CNK mapping: old dot convention → new dash convention
CNK_MAP = {
    "2006.pyreneje": "2006-pyreneje",
    "2007.turecko": "2007-turecko",
    "2008.dolomiti": "2008-dolomiti",
    "2009.maroko": "2009-maroko",
}


def phase2_fix_html():
    """Fix URLs in blog archive HTML files."""
    print("\n=== Phase 2: Fix archive HTML files ===")

    find_archive = build_blog_crossref_map()

    for html_file in sorted(ARCHIVE_BLOG.glob("*.html")):
        content = html_file.read_text(encoding="utf-8")
        original = content

        # 1. Replace uploaded_images URLs → local paths
        def replace_uploaded_image(m):
            filename = m.group(1)
            if (SOURCE_IMAGES / filename).exists():
                stats["uploaded_images_replaced"] += 1
                return f"/assets/migrated/{filename}"
            print(f"  WARNING: Image not found locally: {filename}")
            return m.group(0)

        content = re.sub(
            r"https?://(?:www\.)?michaltrs\.net/blog/uploaded_images/([^\"'>\s]+)",
            replace_uploaded_image,
            content,
        )

        # 2. Replace blog cross-references → local archive paths
        def replace_blog_crossref(m):
            slug = m.group(1).replace(".html", "")
            archive_file = find_archive(slug)
            if archive_file:
                stats["blog_crossrefs_replaced"] += 1
                return f"/archive/blog/{archive_file}"
            print(
                f"  WARNING: No archive match for slug '{slug}' in {html_file.name}"
            )
            return m.group(0)

        content = re.sub(
            r"https?://blog\.michaltrs\.net/\d{4}/\d{2}/([^\"'>\s]+)",
            replace_blog_crossref,
            content,
        )

        # 2b. Same pattern but via www.michaltrs.net/blog/ instead of blog.michaltrs.net/
        content = re.sub(
            r"https?://(?:www\.)?michaltrs\.net/blog/\d{4}/\d{2}/([^\"'>\s]+)",
            replace_blog_crossref,
            content,
        )

        # 2c. Dead photo gallery links → replace href with #
        def fix_fotky_href(m):
            stats["blog_crossrefs_replaced"] += 1
            return 'href="#"'

        content = re.sub(
            r'href="https?://(?:www\.)?michaltrs\.net/fotky/[^"]*"',
            fix_fotky_href,
            content,
            flags=re.IGNORECASE,
        )

        # 3. Replace CNK references → local archive paths
        def replace_cnk(m):
            path = m.group(1).rstrip("/")
            for old, new in CNK_MAP.items():
                if old in path:
                    stats["cnk_refs_replaced"] += 1
                    return f"/archive/cnk/{new}/"
            if "vrcholy" in path:
                stats["cnk_refs_replaced"] += 1
                return "/archive/cnk/vrcholy/"
            print(f"  WARNING: Unknown CNK path: {path} in {html_file.name}")
            return m.group(0)

        content = re.sub(
            r"https?://(?:www\.)?michaltrs\.net/cnk/([^\"'>\s]+)",
            replace_cnk,
            content,
        )

        # 4. Replace blog/files references → local paths
        def replace_blog_file(m):
            stats["blog_files_replaced"] += 1
            return f"/assets/migrated/{m.group(1)}"

        content = re.sub(
            r"https?://(?:www\.)?michaltrs\.net/blog/files/([^\"'>\s]+)",
            replace_blog_file,
            content,
        )

        # 5. Remove dead Flash <embed> tags referencing picasaweb
        def remove_embed(m):
            stats["embeds_removed"] += 1
            return ""

        content = re.sub(
            r"<embed\s[^>]*picasaweb\.google\.[^>]*>\s*</embed>",
            remove_embed,
            content,
            flags=re.IGNORECASE,
        )

        # 6. Handle <a href="picasaweb..."><img src="ggpht..."/></a> → remove entirely
        def remove_picasaweb_ggpht(m):
            stats["picasaweb_fixed"] += 1
            stats["ggpht_removed"] += 1
            return ""

        content = re.sub(
            r'<a\s[^>]*href="https?://(?:www\.)?picasaweb\.google\.[^"]*"[^>]*>\s*<img\s[^>]*src="https?://lh\d+\.ggpht\.com[^"]*"[^>]*/?\s*>\s*</a>',
            remove_picasaweb_ggpht,
            content,
            flags=re.IGNORECASE,
        )

        # 7. Replace remaining picasaweb hrefs with # (keeps text/images, kills dead link)
        def fix_picasaweb_href(m):
            stats["picasaweb_fixed"] += 1
            return 'href="#"'

        content = re.sub(
            r'href="https?://(?:www\.)?picasaweb\.google\.[^"]*"',
            fix_picasaweb_href,
            content,
            flags=re.IGNORECASE,
        )

        # 8. Handle remaining standalone ggpht.com <img> tags → remove
        def remove_ggpht_img(m):
            stats["ggpht_removed"] += 1
            return ""

        content = re.sub(
            r'<img\s[^>]*src="https?://lh\d+\.ggpht\.com[^"]*"[^>]*/?\s*>',
            remove_ggpht_img,
            content,
            flags=re.IGNORECASE,
        )

        # 9. Remove Blogger onblur handlers
        onblur_pattern = ' onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"'
        onblur_count = content.count(onblur_pattern)
        if onblur_count:
            content = content.replace(onblur_pattern, "")
            stats["onblur_removed"] += onblur_count

        # Write if changed
        if content != original:
            html_file.write_text(content, encoding="utf-8")
            stats["html_fixed"] += 1
            print(f"  Fixed: {html_file.name}")

    print(f"  → {stats['html_fixed']} HTML files modified")


def phase3_fix_vault():
    """Clean up placeholder.jpg references in vault entries."""
    print("\n=== Phase 3: Fix vault entries ===")

    for md_file in sorted(VAULT_DIR.glob("*-blog.md")):
        content = md_file.read_text(encoding="utf-8")
        original = content

        # Remove <a> wrapping placeholder img
        content = re.sub(
            r'<a\s[^>]*>\s*<img\s[^>]*src="/assets/migrated/placeholder\.jpg"[^>]*/?\s*>\s*</a>',
            "",
            content,
        )

        # Remove standalone placeholder img tags
        content = re.sub(
            r'<img\s[^>]*src="/assets/migrated/placeholder\.jpg"[^>]*/?\s*>',
            "",
            content,
        )

        if content != original:
            md_file.write_text(content, encoding="utf-8")
            stats["vault_fixed"] += 1
            stats["placeholder_removed"] += original.count("placeholder.jpg")
            print(f"  Fixed: {md_file.name}")

    print(f"  → {stats['vault_fixed']} vault entries fixed")


def main():
    print("Blog Reference Migration Script")
    print("=" * 50)

    phase1_copy_images()
    phase2_fix_html()
    phase3_fix_vault()

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
