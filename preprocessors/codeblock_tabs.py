import json
import sys
import re
import io
import secrets

from util import preprocessor_start, process_chapters


CODE_BLOCK_PATTERN = re.compile(r"""^(?P<indentation> *)([`~]{3,})[ \t]*(?P<language>.*?)[ \t]*$\n(?P<code_block_contents>.*?)\n^\1\2[ \t]*$""", flags=re.MULTILINE | re.DOTALL)


def process_chapter(chapter):
    cur_contents = chapter['content']

    while True:
        match = CODE_BLOCK_PATTERN.search(cur_contents)
        if not match:
            break

        code_block_contents = match.group('code_block_contents')
        indentation = match.group('indentation')
        language = match.group('language')

        print(f"Found code block with lang='{language}' and indent_level={len(indentation)}:\n{code_block_contents}\n", file=sys.stderr)

        cur_contents = cur_contents[match.end():]

if __name__ == '__main__':
    preprocessor_start()

    context, book = json.load(sys.stdin)

    process_chapters(book['sections'], process_chapter)

    print(json.dumps(book))