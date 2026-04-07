import json
import sys


def preprocessor_start():
    if len(sys.argv) > 1:
        if sys.argv[1] == "supports":
            sys.exit(0)


def get_book_items(book):
    """Get book items, supporting both mdBook 0.4 ('sections') and 0.5+ ('items')."""
    return book.get('items', book.get('sections', []))


def process_chapters(sections, processor):
    for section in sections:
        if 'Chapter' in section:
            chapter = section['Chapter']
            processor(chapter)

            if "sub_items" in chapter:
                process_chapters(chapter['sub_items'], processor)
