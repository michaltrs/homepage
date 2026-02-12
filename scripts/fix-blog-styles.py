#!/usr/bin/env python3
"""Clean up inline styles on images across all archive HTML files.

- Blog: remove deprecated attrs, clean inline styles, add CSS classes, lightbox
- CNK: remove width/height HTML attrs from thumbnail images, add lightbox
- CVUT-FEL: normalize inline float/center styles to CSS classes
- SPSE: normalize inline styles to CSS classes
- All: add lightbox.js script tag, add lightbox class to image links
"""

import os
import re
import glob

ARCHIVE = os.path.join(os.path.dirname(__file__), '..', 'public', 'archive')
IMAGE_EXTS = re.compile(r'\.(jpe?g|png|gif|webp|svg|bmp)$', re.IGNORECASE)
LIGHTBOX_SCRIPT = '<script src="/archive/lightbox.js"></script>'

stats = {'files': 0, 'images_cleaned': 0, 'lightbox_links': 0, 'scripts_added': 0,
         'tables_removed': 0, 'videos_converted': 0}


def is_image_href(href):
    """Check if an href points to an image file."""
    return bool(IMAGE_EXTS.search(href.split('?')[0]))


def extract_float(style):
    """Extract float direction from inline style string."""
    if not style:
        return None
    if re.search(r'float\s*:\s*left', style):
        return 'left'
    if re.search(r'float\s*:\s*right', style):
        return 'right'
    if re.search(r'display\s*:\s*block', style) and re.search(r'margin\s*.*auto', style):
        return 'center'
    if re.search(r'display\s*:\s*inline', style):
        return 'inline'
    return None


def add_class(tag, cls):
    """Add a CSS class to an HTML tag string."""
    if 'class="' in tag:
        return re.sub(r'class="([^"]*)"', lambda m: f'class="{m.group(1)} {cls}"', tag)
    # Insert class before the first space after tag name or before >
    return re.sub(r'^(<\w+)', rf'\1 class="{cls}"', tag)


def clean_blog_img_tag(tag, parent_float=None):
    """Clean a single <img ...> tag. parent_float overrides if img has no float."""
    original = tag

    # Skip if already processed (has img- class)
    if re.search(r'class="[^"]*img-', tag):
        return tag

    # Remove deprecated attributes
    tag = re.sub(r'\s*border="0"', '', tag)
    tag = re.sub(r'\s*imageanchor="\d+"', '', tag)

    # Extract float info from img style before removing
    style_match = re.search(r'style="([^"]*)"', tag)
    style = style_match.group(1) if style_match else ''
    float_dir = extract_float(style) or parent_float

    # Remove width/height HTML attributes
    tag = re.sub(r'\s*width="\d+"', '', tag)
    tag = re.sub(r'\s*height="\d+"', '', tag)

    # Remove entire style attribute
    tag = re.sub(r'\s*style="[^"]*"', '', tag)

    # Add appropriate CSS class
    if float_dir == 'left':
        tag = add_class(tag, 'img-left')
    elif float_dir == 'right':
        tag = add_class(tag, 'img-right')
    elif float_dir == 'inline':
        tag = add_class(tag, 'img-inline')
    else:
        tag = add_class(tag, 'img-center')

    if tag != original:
        stats['images_cleaned'] += 1
    return tag


def clean_blog_anchor_img_pair(match):
    """Clean an <a>...<img>...</a> pair, transferring float from anchor to img."""
    full = match.group(0)
    a_tag_match = re.match(r'(<a\b[^>]*>)', full)
    if not a_tag_match:
        return full
    a_tag = a_tag_match.group(1)

    # Skip if already processed (by separator/table handler)
    if 'class="lightbox' in a_tag:
        return full

    # Extract float from anchor style before cleaning
    a_style_match = re.search(r'style="([^"]*)"', a_tag)
    a_style = a_style_match.group(1) if a_style_match else ''
    anchor_float = extract_float(a_style)

    # Clean anchor tag
    a_clean = a_tag
    a_clean = re.sub(r'\s*imageanchor="\d+"', '', a_clean)
    a_clean = re.sub(r'\s*style="[^"]*"', '', a_clean)

    # Add lightbox if href is an image
    href_match = re.search(r'href="([^"]*)"', a_clean)
    if href_match and is_image_href(href_match.group(1)):
        a_clean = add_class(a_clean, 'lightbox')
        if 'target=' not in a_clean:
            a_clean = re.sub(r'(<a\b)', r'\1 target="_blank"', a_clean)
        stats['lightbox_links'] += 1

    # Clean img tag, passing anchor's float as parent context
    def replace_img(m):
        return clean_blog_img_tag(m.group(0), parent_float=anchor_float)

    rest = full[len(a_tag):]
    rest = re.sub(r'<img\b[^>]*>', replace_img, rest)

    return a_clean + rest


def clean_blog_standalone_img(match):
    """Clean a standalone <img> tag (not inside an anchor)."""
    return clean_blog_img_tag(match.group(0))


def clean_blog_standalone_anchor(match):
    """Clean an <a> tag that doesn't wrap an image."""
    tag = match.group(0)
    tag = re.sub(r'\s*imageanchor="\d+"', '', tag)
    return tag


def clean_blog_table_wrapper(match):
    """Replace Blogger table caption containers with simpler markup."""
    full = match.group(0)

    # Extract the <a><img></a> or <img> inside
    inner_match = re.search(r'(<a\b[^>]*>.*?</a>|<img\b[^>]*>)', full, re.DOTALL)
    if not inner_match:
        return full

    inner = inner_match.group(0)

    # Clean inner img: remove border, width, height, style
    def clean_inner_img(m):
        t = m.group(0)
        t = re.sub(r'\s*border="0"', '', t)
        t = re.sub(r'\s*width="\d+"', '', t)
        t = re.sub(r'\s*height="\d+"', '', t)
        t = re.sub(r'\s*style="[^"]*"', '', t)
        stats['images_cleaned'] += 1
        return t

    inner = re.sub(r'<img\b[^>]*>', clean_inner_img, inner)

    # Clean inner anchor: remove imageanchor, style, add lightbox
    def clean_inner_anchor(m):
        t = m.group(0)
        t = re.sub(r'\s*imageanchor="\d+"', '', t)
        t = re.sub(r'\s*style="[^"]*"', '', t)
        href_match = re.search(r'href="([^"]*)"', t)
        if href_match and is_image_href(href_match.group(1)):
            t = add_class(t, 'lightbox')
            if 'target=' not in t:
                t = re.sub(r'(<a\b)', r'\1 target="_blank"', t)
            stats['lightbox_links'] += 1
        return t

    inner = re.sub(r'<a\b[^>]*>', clean_inner_anchor, inner)

    # Extract caption text
    caption_match = re.search(r'class="tr-caption"[^>]*>(.*?)</td>', full, re.DOTALL)
    caption = caption_match.group(1).strip() if caption_match else ''

    # Get float direction from the table style
    table_style = re.search(r'<table[^>]*style="([^"]*)"', full)
    table_style_str = table_style.group(1) if table_style else ''
    float_dir = extract_float(table_style_str)

    # Build replacement - figure with caption
    fig_class = 'img-right' if float_dir == 'right' else 'img-left' if float_dir == 'left' else 'img-center'
    if caption:
        replacement = f'<figure class="{fig_class}">{inner}<figcaption>{caption}</figcaption></figure>'
    else:
        replacement = f'<figure class="{fig_class}">{inner}</figure>'

    return replacement


def clean_blog_separator(match):
    """Clean separator divs with centered images."""
    full = match.group(0)

    # Extract inner content (the <a><img></a>)
    inner_match = re.search(r'(<a\b[^>]*>.*?</a>|<img\b[^>]*>)', full, re.DOTALL)
    if not inner_match:
        return full

    inner = inner_match.group(0)

    # Clean inner img: remove border, width, height, style
    def clean_inner_img(m):
        t = m.group(0)
        t = re.sub(r'\s*border="0"', '', t)
        t = re.sub(r'\s*width="\d+"', '', t)
        t = re.sub(r'\s*height="\d+"', '', t)
        t = re.sub(r'\s*style="[^"]*"', '', t)
        stats['images_cleaned'] += 1
        return t

    inner = re.sub(r'<img\b[^>]*>', clean_inner_img, inner)

    # Clean inner anchor: remove imageanchor, style, add lightbox
    def clean_inner_anchor(m):
        t = m.group(0)
        t = re.sub(r'\s*imageanchor="\d+"', '', t)
        t = re.sub(r'\s*style="[^"]*"', '', t)
        href_match = re.search(r'href="([^"]*)"', t)
        if href_match and is_image_href(href_match.group(1)):
            t = add_class(t, 'lightbox')
            if 'target=' not in t:
                t = re.sub(r'(<a\b)', r'\1 target="_blank"', t)
            stats['lightbox_links'] += 1
        return t

    inner = re.sub(r'<a\b[^>]*>', clean_inner_anchor, inner)

    return f'<div class="img-center">{inner}</div>'


def extract_youtube_id(url):
    """Extract YouTube video ID from various URL formats."""
    # /v/VIDEO_ID, /embed/VIDEO_ID, watch?v=VIDEO_ID
    m = re.search(r'youtube\.com/(?:v|embed)/([a-zA-Z0-9_-]+)', url)
    if m:
        return m.group(1)
    m = re.search(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', url)
    if m:
        return m.group(1)
    return None


def convert_youtube_object(match):
    """Convert YouTube <object>/<embed> Flash to responsive <iframe>."""
    block = match.group(0)
    # Try param movie value first, then embed src
    vid_id = None
    m = re.search(r'<param\s+name="movie"\s+value="([^"]+)"', block)
    if m:
        vid_id = extract_youtube_id(m.group(1))
    if not vid_id:
        m = re.search(r'<embed\s[^>]*src="([^"]+)"', block)
        if m:
            vid_id = extract_youtube_id(m.group(1))
    if not vid_id:
        return block  # Not a YouTube embed, leave alone
    stats['videos_converted'] += 1
    return f'<div class="video-responsive"><iframe src="https://www.youtube.com/embed/{vid_id}" allowfullscreen></iframe></div>'


def convert_youtube_iframe(match):
    """Wrap existing YouTube <iframe> in responsive container + https."""
    tag = match.group(0)
    m = re.search(r'src="([^"]+)"', tag)
    if not m:
        return tag
    src = m.group(1)
    vid_id = extract_youtube_id(src)
    if not vid_id:
        return tag
    stats['videos_converted'] += 1
    return f'<div class="video-responsive"><iframe src="https://www.youtube.com/embed/{vid_id}" allowfullscreen></iframe></div>'


def convert_maps_iframe(match):
    """Wrap Google Maps <iframe> in responsive container."""
    tag = match.group(0)
    # Upgrade http to https, remove fixed dimensions
    src_m = re.search(r'src="([^"]+)"', tag)
    if not src_m:
        return tag
    src = src_m.group(1).replace('http://', 'https://')
    stats['videos_converted'] += 1
    return f'<div class="video-responsive"><iframe src="{src}" allowfullscreen></iframe></div>'


def convert_dead_embed(match):
    """Replace dead Flash embeds with placeholder text."""
    stats['videos_converted'] += 1
    return '<p><em>(Flash obsah již není dostupný)</em></p>'


def process_video_embeds(html):
    """Convert all video/Flash embeds to modern responsive format."""
    # 1. YouTube <object>...</object> (old Flash)
    html = re.sub(
        r'<object\b[^>]*>(?:(?!</object>).)*?youtube\.com(?:(?!</object>).)*?</object>',
        convert_youtube_object,
        html, flags=re.DOTALL
    )

    # 2. YouTube <iframe> (already modern, just wrap + https)
    # Skip if already inside .video-responsive
    html = re.sub(
        r'(?<!video-responsive">)<iframe\b[^>]*youtube\.com[^>]*>(?:(?!</iframe>).)*?</iframe>',
        convert_youtube_iframe,
        html, flags=re.DOTALL
    )

    # 3. Google Maps <iframe>
    html = re.sub(
        r'(?<!video-responsive">)<iframe\b[^>]*maps\.google\.com[^>]*>(?:(?!</iframe>).)*?</iframe>',
        convert_maps_iframe,
        html, flags=re.DOTALL
    )

    # 4. Dead Flash: <object> with non-YouTube src (stream.cz, swatch, brutalbob, etc.)
    html = re.sub(
        r'<object\b[^>]*>(?:(?!</object>).)*?(?:stream\.cz|swatch\.com|brutalbob|brightcove)(?:(?!</object>).)*?</object>',
        convert_dead_embed,
        html, flags=re.DOTALL
    )

    # 5. Dead <object> wrapping Windows Media Player (must run before standalone embed rule)
    html = re.sub(
        r'<object\b[^>]*(?:x-ms-asf|mplayer)[^>]*>(?:(?!</object>).)*?</object>',
        convert_dead_embed,
        html, flags=re.DOTALL
    )

    # 6. Dead standalone <embed> (brightcove, Windows Media Player, etc.)
    html = re.sub(
        r'<embed\b[^>]*(?:brightcove|x-ms-asf|mms://)[^>]*>(?:</embed>)?',
        convert_dead_embed,
        html, flags=re.DOTALL
    )

    # 7. Clean up <center> wrapper around converted content
    html = re.sub(
        r'<center>\s*(<div class="video-responsive">.*?</div>)\s*</center>',
        r'\1',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<center>\s*(<p><em>\(Flash obsah.*?</em></p>)\s*</center>',
        r'\1',
        html, flags=re.DOTALL
    )

    return html


def process_blog(html, filepath):
    """Process a blog HTML file."""
    # 1. Replace Blogger table caption containers first (before individual tag cleanup)
    html = re.sub(
        r'<table\b[^>]*class="tr-caption-container"[^>]*>.*?</table>',
        clean_blog_table_wrapper,
        html,
        flags=re.DOTALL
    )

    # 2. Replace separator divs
    html = re.sub(
        r'<div\b[^>]*class="separator"[^>]*>.*?</div>',
        clean_blog_separator,
        html,
        flags=re.DOTALL
    )

    # 3. Clean <a>...<img>...</a> pairs (float transfers from anchor to img)
    html = re.sub(
        r'<a\b[^>]*href="[^"]*"[^>]*>(?:(?!</a>).)*?<img\b[^>]*>(?:(?!</a>).)*?</a>',
        clean_blog_anchor_img_pair,
        html,
        flags=re.DOTALL
    )

    # 4. Clean remaining standalone <a> tags (remove imageanchor etc.)
    html = re.sub(r'<a\b[^>]*imageanchor[^>]*>', clean_blog_standalone_anchor, html)

    # 5. Clean remaining standalone <img> tags
    html = re.sub(r'<img\b[^>]*>', clean_blog_standalone_img, html)

    # 6. Convert video/Flash embeds to responsive iframes
    html = process_video_embeds(html)

    # 7. Remove Picasa "Posted by Picasa" badge divs
    html = re.sub(
        r'<div[^>]*>\s*<a\b[^>]*picasa\.google\.com[^>]*>.*?</a>\s*</div>',
        '',
        html, flags=re.DOTALL
    )

    # 8. Convert remaining Blogger photo tables (width:auto) to figure+figcaption
    def convert_blogger_photo_table(match):
        block = match.group(0)
        # Extract float from table style
        float_dir = None
        style_m = re.search(r'style="([^"]*)"', block.split('</table>')[0].split('<td')[0])
        if style_m and 'float' in style_m.group(1):
            float_dir = extract_float(style_m.group(1))
        # Extract image (first cell)
        img_m = re.search(r'(<a\b[^>]*>.*?<img\b[^>]*>.*?</a>|<img\b[^>]*>)', block, re.DOTALL)
        if not img_m:
            return block
        img_html = img_m.group(0)
        # Extract caption (second cell, if present)
        caption = ''
        caption_m = re.search(r'<td[^>]*>(?:(?!</td>).)*?(?:Zdroj|Posted|Album)(?:(?!</td>).)*?</td>', block, re.DOTALL)
        if caption_m:
            caption_text = re.sub(r'<td[^>]*>\s*', '', caption_m.group(0))
            caption_text = re.sub(r'\s*</td>', '', caption_text)
            caption_text = re.sub(r'font-family:[^;]+;?\s*', '', caption_text)
            caption_text = re.sub(r'font-size:[^;]+;?\s*', '', caption_text)
            caption_text = re.sub(r'text-align:[^;]+;?\s*', '', caption_text)
            caption_text = re.sub(r'\s*style="\s*"', '', caption_text)
            if caption_text.strip():
                caption = f'\n<figcaption>{caption_text.strip()}</figcaption>'
        float_class = f' class="img-{float_dir}"' if float_dir else ''
        stats['images_cleaned'] += 1
        return f'<figure{float_class}>{img_html}{caption}\n</figure>'

    html = re.sub(
        r'<table\b[^>]*style="[^"]*width:\s*auto[^"]*"[^>]*>.*?</table>',
        convert_blogger_photo_table,
        html, flags=re.DOTALL
    )

    # 9. Unwrap <center> tags (keep inner content)
    html = re.sub(r'<center>\s*(?:<br\s*/?>)?\s*', '', html)
    html = re.sub(r'\s*</center>', '', html)

    return html


def process_cnk(html, filepath):
    """Process a CNK HTML file — clean images, remove layout tables."""
    def clean_cnk_img(match):
        tag = match.group(0)
        original = tag
        # Remove width/height HTML attributes
        tag = re.sub(r'\s*width="\d+"', '', tag)
        tag = re.sub(r'\s*height="\d+"', '', tag)
        if tag != original:
            stats['images_cleaned'] += 1
        return tag

    html = re.sub(r'<img\b[^>]*>', clean_cnk_img, html)

    # Add lightbox class to <a> tags pointing to images
    def add_cnk_lightbox(match):
        tag = match.group(0)
        href_match = re.search(r'href="([^"]*)"', tag)
        if href_match and is_image_href(href_match.group(1)):
            if 'lightbox' not in tag:
                tag = add_class(tag, 'lightbox')
                if 'target=' not in tag:
                    tag = re.sub(r'(<a\b)', r'\1 target="_blank"', tag)
                stats['lightbox_links'] += 1
        return tag

    html = re.sub(r'<a\b[^>]*href="[^"]*"[^>]*>', add_cnk_lightbox, html)

    # --- P2b: Remove layout tables ---

    def extract_images(fragment):
        """Extract all <a><img></a> and standalone <img> from HTML."""
        return re.findall(
            r'(<a\b[^>]*>(?:(?!</a>).)*?<img\b[^>]*>(?:(?!</a>).)*?</a>|<img\b[^>]*/?>)',
            fragment, re.DOTALL
        )

    def clean_img_align(html_str):
        """Remove align attributes from HTML string."""
        return re.sub(r'\s*align="[^"]*"', '', html_str)

    def is_image_only_cell(cell_content):
        """Check if cell content is just image links with minimal text."""
        s = cell_content
        # Only strip <a> tags that wrap images, not text-only links
        s = re.sub(r'<a\b[^>]*>(?:(?!</a>).)*?<img\b[^>]*>(?:(?!</a>).)*?</a>',
                    '', s, flags=re.DOTALL)
        s = re.sub(r'<img\b[^>]*/?\s*>', '', s)
        s = re.sub(r'<div\b[^>]*>.*?</div>', '', s, flags=re.DOTALL)
        s = re.sub(r'<br\s*/?>', '', s)
        s = re.sub(r'&nbsp;', '', s)
        s = s.strip()
        return len(s) < 20

    # 1. <table align="right"> photo grid → gallery (nested in 2003-viden)
    def convert_align_right_grid(m):
        imgs = extract_images(m.group(0))
        if not imgs:
            return m.group(0)
        cleaned = [clean_img_align(img) for img in imgs]
        stats['tables_removed'] += 1
        return '<div class="gallery">\n' + '\n'.join(cleaned) + '\n</div>'

    html = re.sub(
        r'<table\s+align="right"\s*>\s*<tr\b.*?</table>',
        convert_align_right_grid,
        html, flags=re.DOTALL
    )

    # 2. <table class="stred"> galleries → <div class="gallery">
    #    Skip if table has significant text (data table like bike specs)
    def convert_stred_gallery(m):
        table_html = m.group(0)
        # Check for significant text content (= data table, not gallery)
        text_check = re.sub(
            r'<a\b[^>]*>(?:(?!</a>).)*?<img\b[^>]*>(?:(?!</a>).)*?</a>',
            '', table_html, flags=re.DOTALL)
        text_check = re.sub(r'<img\b[^>]*/?\s*>', '', text_check)
        text_check = re.sub(r'<[^>]+>', '', text_check)
        text_check = text_check.strip()
        if len(text_check) > 50:
            return m.group(0)
        imgs = extract_images(table_html)
        if not imgs:
            return m.group(0)
        cleaned = [clean_img_align(img) for img in imgs]
        stats['tables_removed'] += 1
        return '<div class="gallery">\n' + '\n'.join(cleaned) + '\n</div>'

    html = re.sub(
        r'<table\s+class="stred"\s*>.*?</table>',
        convert_stred_gallery,
        html, flags=re.DOTALL
    )

    # 3. <table width="..." align="left/right"> thumbnails → float div
    def convert_float_table(m):
        align = m.group(1)
        imgs = extract_images(m.group(0))
        if not imgs:
            return m.group(0)
        cleaned = [clean_img_align(img) for img in imgs]
        cls = 'img-left' if align == 'left' else 'img-right'
        stats['tables_removed'] += 1
        return '<div class="' + cls + '">\n' + '\n'.join(cleaned) + '\n</div>'

    html = re.sub(
        r'<table\s+width="\d+"\s+align="(left|right)"[^>]*>.*?</table>',
        convert_float_table,
        html, flags=re.DOTALL
    )

    # 4. <table align="center"> → gallery
    def convert_center_gallery(m):
        imgs = extract_images(m.group(0))
        if not imgs:
            return m.group(0)
        cleaned = [clean_img_align(img) for img in imgs]
        stats['tables_removed'] += 1
        return '<div class="gallery">\n' + '\n'.join(cleaned) + '\n</div>'

    html = re.sub(
        r'<table\s+align="center"\s*>.*?</table>',
        convert_center_gallery,
        html, flags=re.DOTALL
    )

    # 5. Stats tables with "Ujetá vzdálenost:" → info divs
    def convert_stats_table(m):
        content = m.group(0)
        result = []
        dist_match = re.search(
            r'Ujetá vzdálenost:</td>\s*<td><b>(.*?)</b></td>', content)
        if dist_match:
            result.append(
                '<div class="info">Ujetá vzdálenost: <b>' +
                dist_match.group(1) + '</b></div>')
        profile_match = re.search(
            r'Profil cesty:</td>\s*<td>(.*?)\s*</td>', content, re.DOTALL)
        if profile_match:
            profile = profile_match.group(1).strip()
            result.append(
                '<div class="info">Profil cesty: ' + profile + '</div>')
        if result:
            stats['tables_removed'] += 1
            return '\n'.join(result)
        return m.group(0)

    html = re.sub(
        r'<table>\s*<tr>\s*<td>Ujetá vzdálenost:.*?</table>',
        convert_stats_table,
        html, flags=re.DOTALL
    )

    # 6. Remaining bare <table> (text+map) → unwrap
    def unwrap_bare_table(m):
        content = m.group(0)
        if 'class="tab"' in content or 'class="fv"' in content:
            return content

        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', content, re.DOTALL)
        if not rows:
            return content

        result_parts = []
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)

            text_cells = []
            img_cells = []
            gallery_cells = []

            for cell in cells:
                cell = cell.strip()
                if not cell:
                    continue
                if '<div class="gallery">' in cell:
                    gallery_cells.append(cell)
                elif is_image_only_cell(cell):
                    imgs = extract_images(cell)
                    if imgs:
                        cleaned = [clean_img_align(img) for img in imgs]
                        img_cells.append(
                            '<div class="img-right">' +
                            ' '.join(cleaned) + '</div>')
                else:
                    text_cells.append(cell)

            # Float images before text (for float layout), galleries after
            result_parts.extend(img_cells)
            result_parts.extend(text_cells)
            result_parts.extend(gallery_cells)

        if result_parts:
            stats['tables_removed'] += 1
            return '\n'.join(result_parts)
        return content

    html = re.sub(
        r'<table>(.*?)</table>',
        unwrap_bare_table,
        html, flags=re.DOTALL
    )

    # 7. Standalone <img ... align="left/right"> → CSS class
    def clean_standalone_img_align(m):
        tag = m.group(0)
        align_match = re.search(r'align="(left|right)"', tag)
        if not align_match:
            return tag
        align = align_match.group(1)
        tag = re.sub(r'\s*align="[^"]*"', '', tag)
        cls = 'img-left' if align == 'left' else 'img-right'
        tag = add_class(tag, cls)
        stats['images_cleaned'] += 1
        return tag

    html = re.sub(
        r'<img\b[^>]*\balign="[^"]*"[^>]*/?>',
        clean_standalone_img_align, html
    )

    # 8. <div align="right"> → inline style
    html = re.sub(
        r'<div\s+align="right">',
        '<div style="text-align: right">', html
    )

    # 9. Float first image/link inside .odstavec (map or diary scan)
    # Pattern: <div class="odstavec"> [whitespace] <a ...><img ...></a> or <img ...>
    def float_odstavec_first_img(m):
        prefix = m.group(1)  # <div class="odstavec"> + whitespace
        tag = m.group(2)     # <a ...> or <img ...>
        if 'img-right' in tag or 'img-left' in tag:
            return m.group(0)  # Already has float class
        tag = add_class(tag, 'img-right')
        stats['images_cleaned'] += 1
        return prefix + tag

    html = re.sub(
        r'(<div\s+class="odstavec">\s*)(<(?:a|img)\b[^>]*>)',
        float_odstavec_first_img,
        html
    )

    return html


def process_cvut_fel(html, filepath):
    """Process a CVUT FEL HTML file — normalize inline styles to classes."""
    # Skip Doxygen auto-generated files
    if '/dokumentace/' in filepath or '/imb-cvut/doc/' in filepath:
        return html

    def clean_fel_img(match):
        tag = match.group(0)
        original = tag

        style_match = re.search(r'style="([^"]*)"', tag)
        if not style_match:
            return tag

        style = style_match.group(1)
        float_dir = extract_float(style)

        # Remove deprecated attrs
        tag = re.sub(r'\s*border="0"', '', tag)
        tag = re.sub(r'\s*width="\d+"', '', tag)
        tag = re.sub(r'\s*height="\d+"', '', tag)

        # Remove style, add class
        tag = re.sub(r'\s*style="[^"]*"', '', tag)
        if float_dir == 'right':
            tag = add_class(tag, 'img-right')
        elif float_dir == 'left':
            tag = add_class(tag, 'img-left')
        elif float_dir == 'center':
            tag = add_class(tag, 'img-center')
        elif float_dir == 'inline':
            tag = add_class(tag, 'img-inline')
        else:
            tag = add_class(tag, 'img-center')

        if tag != original:
            stats['images_cleaned'] += 1
        return tag

    html = re.sub(r'<img\b[^>]*style="[^"]*"[^>]*>', clean_fel_img, html)

    # Add lightbox to image links
    def add_fel_lightbox(match):
        tag = match.group(0)
        href_match = re.search(r'href="([^"]*)"', tag)
        if href_match and is_image_href(href_match.group(1)):
            if 'lightbox' not in tag:
                tag = add_class(tag, 'lightbox')
                if 'target=' not in tag:
                    tag = re.sub(r'(<a\b)', r'\1 target="_blank"', tag)
                stats['lightbox_links'] += 1
        return tag

    html = re.sub(r'<a\b[^>]*href="[^"]*"[^>]*>', add_fel_lightbox, html)

    # Unwrap <center> tags (keep content)
    html = re.sub(r'<center>\s*', '', html)
    html = re.sub(r'\s*</center>', '', html)

    # Unwrap <font> tags (keep content)
    html = re.sub(r'<font\b[^>]*>', '', html)
    html = re.sub(r'</font>', '', html)

    # Clean deprecated <hr> attributes
    html = re.sub(r'<hr\s+[^>]*(?:size|width|noshade)[^>]*/?\s*>', '<hr>', html)

    # Remove cellspacing/cellpadding/border from tables (CSS handles this)
    html = re.sub(r'\s*cellspacing="\d+"', '', html)
    html = re.sub(r'\s*cellpadding="\d+"', '', html)
    html = re.sub(r'(<table\b[^>]*)\s*border="\d+"', r'\1', html)

    # Convert align= on p/div/td to inline style
    def convert_align_attr(m):
        tag = m.group(0)
        align_m = re.search(r'align="(\w+)"', tag)
        if not align_m:
            return tag
        align = align_m.group(1).lower()
        tag = re.sub(r'\s*align="\w+"', '', tag)
        if 'style="' in tag:
            tag = re.sub(r'style="', f'style="text-align: {align}; ', tag)
        else:
            tag = re.sub(r'(>)', f' style="text-align: {align}">', tag, count=1)
        return tag

    html = re.sub(r'<(?:p|div|td|th)\b[^>]*\balign="[^"]*"[^>]*>', convert_align_attr, html)

    return html


def process_spse(html, filepath):
    """Process an SPSE HTML file — normalize inline styles to classes."""
    def clean_spse_img(match):
        tag = match.group(0)
        original = tag

        style_match = re.search(r'style="([^"]*)"', tag)
        if not style_match:
            return tag

        style = style_match.group(1)
        float_dir = extract_float(style)

        tag = re.sub(r'\s*style="[^"]*"', '', tag)

        if float_dir == 'inline':
            tag = add_class(tag, 'img-inline')
        elif float_dir == 'right':
            tag = add_class(tag, 'img-right')
        elif float_dir == 'left':
            tag = add_class(tag, 'img-left')
        else:
            tag = add_class(tag, 'img-center')

        if tag != original:
            stats['images_cleaned'] += 1
        return tag

    html = re.sub(r'<img\b[^>]*style="[^"]*"[^>]*>', clean_spse_img, html)

    # Clean text-align:center on parent <p> tags wrapping images
    html = re.sub(
        r'<p\s+style="text-align:\s*center;\s*">(\s*<img\b)',
        r'<p>\1',
        html
    )

    return html


def add_lightbox_script(html):
    """Add lightbox.js script tag before </body> if not already present."""
    if LIGHTBOX_SCRIPT in html:
        return html
    if '</body>' in html:
        html = html.replace('</body>', f'{LIGHTBOX_SCRIPT}\n</body>')
        stats['scripts_added'] += 1
    return html


def detect_category(filepath):
    """Detect which category a file belongs to based on path."""
    rel = os.path.relpath(filepath, ARCHIVE)
    if rel.startswith('blog/'):
        return 'blog'
    if rel.startswith('cnk/'):
        return 'cnk'
    if rel.startswith('cvut-fel/'):
        return 'cvut-fel'
    if rel.startswith('spse-v-uzlabine/'):
        return 'spse'
    return None


def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    original = html
    category = detect_category(filepath)

    if category == 'blog':
        html = process_blog(html, filepath)
    elif category == 'cnk':
        html = process_cnk(html, filepath)
    elif category == 'cvut-fel':
        html = process_cvut_fel(html, filepath)
    elif category == 'spse':
        html = process_spse(html, filepath)

    html = add_lightbox_script(html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        stats['files'] += 1
        return True
    return False


def main():
    html_files = glob.glob(os.path.join(ARCHIVE, '**', '*.html'), recursive=True)
    html_files.sort()

    print(f'Found {len(html_files)} HTML files in archive')
    print()

    by_category = {'blog': [], 'cnk': [], 'cvut-fel': [], 'spse': [], 'other': []}
    for f in html_files:
        cat = detect_category(f) or 'other'
        by_category[cat].append(f)

    for cat, files in by_category.items():
        if not files:
            continue
        changed = 0
        for filepath in files:
            if process_file(filepath):
                changed += 1
                print(f'  [{cat}] {os.path.relpath(filepath, ARCHIVE)}')
        print(f'  {cat}: {changed}/{len(files)} files modified')
        print()

    print('Summary:')
    print(f'  Files modified: {stats["files"]}')
    print(f'  Images cleaned: {stats["images_cleaned"]}')
    print(f'  Lightbox links added: {stats["lightbox_links"]}')
    print(f'  Layout tables removed: {stats["tables_removed"]}')
    print(f'  Videos converted: {stats["videos_converted"]}')
    print(f'  Script tags added: {stats["scripts_added"]}')


if __name__ == '__main__':
    main()
