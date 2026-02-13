import sys


def preprocessor_start():
    if len(sys.argv) > 1:
        if sys.argv[1] == "supports":
            sys.exit(0)


def process_chapters(sections, processor):
    for section in sections:
        if 'Chapter' in section:
            chapter = section['Chapter']
            processor(chapter)

            if "sub_items" in chapter:
                process_chapters(chapter['sub_items'], processor)
