import json
import sys
import re
import io
import secrets

from util import preprocessor_start, process_chapters, get_book_items

"""
Format:

### [Tab Name](#tab/group_id)

Tab contents here.

***
"""
TAB_PATTERN = re.compile(r"""
(?P<header_level>\#{1,5})\s+\[(?P<name>.*)\]\(\#tab\/(?P<group_id>.*?)\)    # ### [Tab Name](#tab/group_id)
\s*                                                                         # Whitespace
(?P<contents>(?:.|\n)*?)                                                    # Tab contents                       
\*{3,}                                                                      # *** separator               
\s*                                                                         # Optional trailing whitespace               
""", flags=re.VERBOSE)


def write_accordion(buffer, contents):
    accordion_id = f"accordion-{secrets.token_hex(4)}"
    default_visible_group = next((group_id for group_id, _, _, _ in contents if 'default' in group_id), None) or contents[0][0]

    buffer.write('<div class="accordion">')
    buffer.write('<ul class="accordion-tabs" role="tablist">\n')
    for group_id, name, _, _ in contents:
        if "default" in group_id:
            continue

        buffer.write(f"""
<li role="presentation">
<a href="#{accordion_id}-{group_id}" role="tab" aria-controls="{accordion_id}-{group_id}" data-accordion-target="{group_id}" {'aria-selected="true" tabindex="0"' if group_id == default_visible_group else 'aria-selected="false" tabindex="-1"'}>
{name}
</a>
</li>\n""")

    buffer.write('</ul>\n')

    buffer.write('\n<div class="accordion-contents">\n')

    for group_id, name, content, header_level in contents:
        buffer.write(f"""
<section id="{accordion_id}-{group_id}" role="tabpanel" data-accordion-group="{group_id}" {'aria-hidden="true" hidden' if group_id != default_visible_group else 'aria-hidden="false"'}>
<h{header_level} class="accordion-title-print" aria-hidden="true">

{name}

</h{header_level}>

{content}

</section>""")

    buffer.write("</div></div>\n\n")

def process_chapter(chapter):
    result = io.StringIO()
    cur_contents = chapter['content']

    section_contents = []

    while True:
        match = TAB_PATTERN.search(cur_contents)
        if not match:
            break

        group_id = match.group('group_id')
        name = match.group('name')
        contents = match.group('contents')
        header_level = len(match.group('header_level').strip())

        before = cur_contents[:match.start()]
        after = cur_contents[match.end():]

        if before.strip():
            if section_contents:
                write_accordion(result, section_contents)
            section_contents = []

        section_contents.append((group_id, name, contents, header_level))

        result.write(before)
        cur_contents = after

    if section_contents:
        write_accordion(result, section_contents)

    result.write(cur_contents)

    chapter['content'] = result.getvalue()


if __name__ == '__main__':
    preprocessor_start()

    context, book = json.load(sys.stdin)

    process_chapters(get_book_items(book), process_chapter)

    json.dump(book, sys.stdout)