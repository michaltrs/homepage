#!/usr/bin/env python3
"""
Migrate ČVUT FEL subjects from old PHP site to Astro archive.

Parses desc.php files, generates archive HTML pages and vault markdown entries.
"""

import os
import re
import html

# Paths
SRC_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'www-2008-20', 'cvut_fel')
ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'archive', 'cvut-fel')
VAULT_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'content', 'vault')

# Approximate semester dates for each subject (for pubDate in vault entries)
SUBJECT_DATES = {
    '36vb':   '2003-06-15',
    '36ups':  '2003-06-15',
    '12ue':   '2003-06-15',
    '02f':    '2004-02-01',
    '36soj':  '2004-02-01',
    '36ls':   '2004-06-15',
    '12mt':   '2004-06-15',
    '17tp1':  '2004-06-15',
    '36pt':   '2004-06-15',
    '36aps':  '2005-02-01',
    '36nlp':  '2005-02-01',
    '04nj':   '2005-02-01',
    '36osy':  '2005-06-15',
    '36pjc':  '2005-06-15',
    '36dbs':  '2005-06-15',
    '36paa':  '2005-06-15',
    '36sim':  '2005-06-15',
    '36dsy':  '2006-01-15',
    '36nan':  '2006-01-15',
    '36pj':   '2006-01-15',
    '36pjw':  '2006-01-15',
    '01m6f':  '2006-06-15',
    '34prs':  '2006-06-15',
    '36pob':  '2006-06-15',
    '36pz':   '2006-06-15',
    '36si':   '2006-06-15',
    '36los':  '2006-06-15',
    '36par':  '2007-02-01',
    '36apc':  '2007-02-01',
    '36prm':  '2007-02-01',
    '36spa':  '2007-06-15',
    '36unx':  '2007-06-15',
    '36dsp':  '2007-06-15',
    '36ami':  '2007-06-15',
    '36mps':  '2008-01-15',
    '36dp':   '2008-02-13',
    'ostatni': '2006-03-01',
}


def parse_desc_php(filepath, subject_dir):
    """Parse a desc.php file and return (title, html_content, description)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    base_url = f'/archive/cvut-fel/{subject_dir}'

    # Extract title from <h2> tag
    h2_match = re.search(r'<h2>(.*?)</h2>', content, re.DOTALL)
    title = h2_match.group(1).strip() if h2_match else subject_dir

    # Extract description from introductory text
    desc = extract_description(content)

    # Convert PHP calls to HTML
    html_content = convert_php_to_html(content, base_url, subject_dir)

    return title, html_content, desc


def extract_description(content):
    """Extract a plain-text description from the introductory text in desc.php."""
    # Get content between first <div> and first <h3> or first <?php (whichever comes first)
    div_match = re.search(r'<div[^>]*>(.*?)(?:<h3>|$)', content, re.DOTALL)
    if not div_match:
        return ''

    text = div_match.group(1)

    # Remove PHP blocks
    text = re.sub(r'<\?php.*?\?>', '', text, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Unescape HTML entities
    text = html.unescape(text)

    # Truncate to reasonable length for description
    if len(text) > 200:
        text = text[:197].rsplit(' ', 1)[0] + '...'

    return text


def convert_php_to_html(content, base_url, subject_dir):
    """Convert PHP function calls in desc.php to pure HTML."""
    # Remove HTML comments at the top
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Remove the <h2> tag (will be in the page header instead)
    content = re.sub(r'<h2>.*?</h2>\s*', '', content, flags=re.DOTALL)

    # Replace $base references with archive URL
    content = content.replace("$base.'", f"'{base_url}")
    content = content.replace('$base."', f'"{base_url}')

    # Process download_item calls → <li> elements
    # Use quoted-string matching to handle parens inside comments
    def replace_download_item(m):
        url = m.group(1).strip("'\"")
        text = m.group(2).strip("'\"")
        icon = m.group(3).strip("'\"")
        comment = m.group(4).strip("'\"")

        if not url.startswith('/') and not url.startswith('http'):
            url = f'{base_url}/{url}'

        comment_html = f' — {comment}' if comment else ''
        return f'<li><a href="{url}">{text}</a>{comment_html}</li>'

    content = re.sub(
        r"download_item\(\s*('[^']*')\s*,\s*('[^']*')\s*,\s*('[^']*')\s*,\s*('[^']*')\s*\)",
        replace_download_item,
        content
    )

    # Process img calls → <img> or <a><img></a>
    def replace_img(m):
        src = m.group(1).strip("'\"")
        url_or_empty = m.group(2).strip("'\"")
        alt = m.group(3).strip("'\"")
        align = m.group(4).strip("'\"")

        if src and not src.startswith('/') and not src.startswith('http'):
            src = f'{base_url}/{src}'
        if url_or_empty and not url_or_empty.startswith('/') and not url_or_empty.startswith('http'):
            url_or_empty = f'{base_url}/{url_or_empty}'

        style = ''
        if align == 'r':
            style = ' style="float:right; margin-left:15px; max-width:250px"'
        elif align == 'c':
            style = ' style="display:block; margin:10px auto; max-width:300px"'

        if url_or_empty:
            return f'<a href="{url_or_empty}"><img src="{src}" alt="{alt}"{style}></a>'
        else:
            return f'<img src="{src}" alt="{alt}"{style}>'

    content = re.sub(
        r"img\(\s*('[^']*')\s*,\s*('[^']*')\s*,\s*('[^']*')\s*,\s*('[^']*')\s*\)",
        replace_img,
        content
    )

    # Process urllink calls → <a> elements
    def replace_urllink(m):
        url = m.group(1).strip("'\"")
        text = m.group(2).strip("'\"")

        if not url.startswith('/') and not url.startswith('http'):
            url = f'{base_url}/{url}'

        return f'<a href="{url}">{text}</a>'

    content = re.sub(
        r"urllink\(\s*('[^']*')\s*,\s*('[^']*')\s*,\s*('[^']*')\s*\)",
        replace_urllink,
        content
    )

    # Remove entire <?php ... ?> blocks (now empty after replacements)
    content = re.sub(r'<\?php\s*\?>', '', content)
    content = re.sub(r'<\?php\s*', '', content)
    content = re.sub(r'\s*\?>', '', content)

    # Remove PHP semicolons and leftover whitespace on lines that only have ";"
    content = re.sub(r'(?<=</li>)\s*;', '', content)
    content = re.sub(r'(?<=</a>)\s*;', '', content)
    content = re.sub(r'(?<=>)\s*;', '', content)
    content = re.sub(r'^\s*;\s*$', '', content, flags=re.MULTILINE)

    # Fix relative image/link paths in "ostatni" (raw HTML, not PHP functions)
    if subject_dir == 'ostatni':
        # Fix href="ostatni/..." → href="/archive/cvut-fel/ostatni/..."
        content = re.sub(
            r'(href|src)="ostatni/',
            rf'\1="/archive/cvut-fel/ostatni/',
            content
        )

    # Remove wrapping <div> tags (we have our own structure)
    content = re.sub(r'^\s*<div[^>]*>\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*</div>\s*$', '', content, flags=re.MULTILINE)

    # Wrap orphan <li> elements in <ul> tags
    content = wrap_li_in_ul(content)

    # Clean up excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()


def wrap_li_in_ul(content):
    """Wrap consecutive <li>...</li> elements in <ul> tags if not already in a list."""
    lines = content.split('\n')
    result = []
    in_auto_ul = False
    ul_depth = 0  # track existing <ul> nesting

    for line in lines:
        stripped = line.strip()

        # Track existing <ul> nesting
        if re.search(r'<ul[\s>]', stripped) or stripped == '<ul>':
            ul_depth += 1
        if '</ul>' in stripped:
            ul_depth = max(0, ul_depth - 1)

        # Only auto-wrap when not inside an existing <ul>
        if ul_depth == 0:
            has_li = '<li>' in stripped

            if has_li and not in_auto_ul:
                # Start a new auto-wrapped ul
                result.append('    <ul>')
                in_auto_ul = True
            elif in_auto_ul and not has_li and stripped:
                # Non-li, non-empty line → close auto ul
                # But skip if it's just whitespace or empty
                if stripped not in ('', '<br/>', '<br>'):
                    result.append('    </ul>')
                    in_auto_ul = False

        result.append(line)

    if in_auto_ul:
        result.append('    </ul>')

    return '\n'.join(result)


def generate_archive_html(title, body_content, subject_dir):
    """Generate a complete archive HTML page."""
    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} | ČVUT FEL | Archiv Michal Trs</title>
    <link rel="stylesheet" href="/archive/style.css">
</head>
<body>
    <div class="nav"><a href="/vault">&larr; Zpět do The Vault</a></div>
    <div class="header">
        <h1>{html.escape(title)}</h1>
        <p><i>ČVUT FEL — studijní materiály a semestrální práce</i></p>
    </div>
    {body_content}
    <div class="footer">&copy; Michal Trs | Archivováno z michaltrs.net/cvut_fel/ | <a href="/vault">The Vault</a></div>
</body>
</html>"""


def generate_vault_entry(title, subject_dir, description, pub_date):
    """Generate a vault markdown entry."""
    link = f'/archive/cvut-fel/{subject_dir}.html'
    safe_title = title.replace('"', '\\"')
    safe_desc = description.replace('"', '\\"') if description else ''

    is_milestone = subject_dir == '36dp'

    return f"""---
title: "ČVUT FEL — {safe_title}"
pubDate: {pub_date}T00:00:00.000Z
description: "{safe_desc}"
link: "{link}"
category: "cvut-fel"
isMilestone: {str(is_milestone).lower()}
---

{description}
"""


def main():
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    os.makedirs(VAULT_DIR, exist_ok=True)

    subjects = sorted([
        d for d in os.listdir(SRC_DIR)
        if os.path.isdir(os.path.join(SRC_DIR, d))
        and os.path.exists(os.path.join(SRC_DIR, d, 'desc.php'))
    ])

    print(f"Found {len(subjects)} subjects to migrate")

    html_count = 0
    vault_count = 0

    for subject in subjects:
        desc_path = os.path.join(SRC_DIR, subject, 'desc.php')
        print(f"\nProcessing: {subject}")

        title, body_content, description = parse_desc_php(desc_path, subject)
        print(f"  Title: {title}")
        print(f"  Desc: {description[:80]}..." if len(description) > 80 else f"  Desc: {description}")

        # Generate archive HTML
        archive_html = generate_archive_html(title, body_content, subject)
        html_path = os.path.join(ARCHIVE_DIR, f'{subject}.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(archive_html)
        html_count += 1

        # Generate vault entry
        pub_date = SUBJECT_DATES.get(subject, '2005-06-01')
        vault_content = generate_vault_entry(title, subject, description, pub_date)
        vault_filename = f'{pub_date}-cvut-fel-{subject}.md'
        vault_path = os.path.join(VAULT_DIR, vault_filename)
        with open(vault_path, 'w', encoding='utf-8') as f:
            f.write(vault_content)
        vault_count += 1

    print(f"\n{'='*60}")
    print(f"Migration complete!")
    print(f"  HTML pages: {html_count}")
    print(f"  Vault entries: {vault_count}")


if __name__ == '__main__':
    main()
