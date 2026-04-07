import json
import sys
import re

from util import preprocessor_start, process_chapters, get_book_items

"""
Replaces mdbook-alerts (Rust crate) with a Python preprocessor.
Transforms GitHub-style admonitions (> [!TYPE]) into styled HTML divs.

Generates the same HTML structure as mdbook-alerts 0.8.0:

<div class="mdbook-alerts mdbook-alerts-TYPE">
  <p class="mdbook-alerts-title">
    <span class="mdbook-alerts-icon"></span>
    TYPE
  </p>
  ...content...
</div>
"""

ALERT_PATTERN = re.compile(
    r'^(?P<prefix>\s*)> \[!(?P<type>[^\]]+)\]\s*\n'
    r'(?P<body>(?:\s*>.*\n?)*)',
    re.MULTILINE
)


def transform_alert(match):
    alert_type = match.group('type').strip()
    body = match.group('body')

    # Remove the leading '> ' from each line of the body
    lines = []
    for line in body.split('\n'):
        stripped = line.strip()
        if stripped.startswith('> '):
            lines.append(stripped[2:])
        elif stripped == '>':
            lines.append('')
        elif stripped:
            lines.append(stripped)
    
    content = '\n'.join(lines).strip()

    type_lower = alert_type.lower()
    title_display = type_lower.replace('ä', 'a').replace('ö', 'o') if type_lower == type_lower else type_lower
    title_display = type_lower

    return (
        f'\n<div class="mdbook-alerts mdbook-alerts-{type_lower}">\n'
        f'<p class="mdbook-alerts-title">\n'
        f'  <span class="mdbook-alerts-icon"></span>\n'
        f'  {type_lower}\n'
        f'</p>\n\n'
        f'{content}\n'
        f'</div>\n\n'
    )


def process_chapter(chapter):
    chapter['content'] = ALERT_PATTERN.sub(transform_alert, chapter['content'])


if __name__ == '__main__':
    preprocessor_start()

    context, book = json.load(sys.stdin)

    process_chapters(get_book_items(book), process_chapter)

    json.dump(book, sys.stdout)
