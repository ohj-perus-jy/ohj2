"""Rekisteröi materiaalin omat elementit lohkotason elementeiksi.

Python-Markdown käärii tuntemattomat tagit <p>:n sisään, jolloin <task>-korttien
rakenne rikkoutuu. Tämä laajennus kertoo sille, että ne ovat lohkoelementtejä —
sen jälkeen md_in_html osaa renderöidä niiden sisällön markdownina ilman että
src/:n merkkaukseen kosketaan.
"""

from markdown.extensions import Extension

BLOCK_ELEMENTS = ["task", "task-title", "handout"]


class CustomBlocksExtension(Extension):
    def extendMarkdown(self, md):
        for name in BLOCK_ELEMENTS:
            if name not in md.block_level_elements:
                md.block_level_elements.append(name)


def makeExtension(**kwargs):
    return CustomBlocksExtension(**kwargs)
