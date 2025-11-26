(function javaCodeHighlights() {
    /**
     * Java code highlighter for mdBook.
     *
     * Searches every rendered `pre > code.language-java` block for custom markers
     * (`// HIGHLIGHT_<COLOR>_BEGIN` ... `// HIGHLIGHT_<COLOR>_END`) and replaces the
     * enclosed lines with full-width highlight spans. Marker lines themselves are
     * removed so the final code looks clean, and overlapping/multiple highlights are
     * supported. Highlight colors are controlled via CSS variables in
     * `theme/code-highlights.css`.
     *
     * The code was almost entirely written by ChatGPT/GPT-5.1-Codex.
     */
    const MARKER_REGEX = /[ \t]*\/\/\s*HIGHLIGHT_([A-Z0-9]+)_(BEGIN|END)\s*(?:\r?\n)?/g;
    const COLOR_MAP = {
        GREEN: 'var(--code-highlight-green)',
        YELLOW: 'var(--code-highlight-yellow)',
        RED: 'var(--code-highlight-red)',
        BLUE: 'var(--code-highlight-blue)',
    };

    /**
     * Wraps a DOM range in a span configured with the highlight styles.
     * @param {Range} range
     * @param {string} color
     */
    function wrapRange(range, color) {
        if (range.collapsed) {
            range.detach?.();
            return;
        }

        const span = document.createElement('span');
        span.className = 'code-highlight-inline';
        span.style.backgroundColor = COLOR_MAP[color] || COLOR_MAP.GREEN;
        span.dataset.highlightColor = color;

        try {
            range.surroundContents(span);
        } catch (err) {
            // If surroundContents fails due to partially selected nodes,
            // fall back to extracting the contents manually.
            const contents = range.extractContents();
            span.appendChild(contents);
            range.insertNode(span);
        }
        range.detach?.();
    }

    /**
     * Advance the caret forward until a non-whitespace character is found.
     */
    function moveForwardPastBreaks(textNodes, indexMap, node, offset) {
        let idx = indexMap.get(node);
        let currentNode = node;
        let currentOffset = offset;

        while (currentNode) {
            const text = currentNode.nodeValue || '';
            while (currentOffset < text.length) {
                const ch = text[currentOffset];
                if (ch === '\n' || ch === '\r' || ch === ' ' || ch === '\t') {
                    currentOffset += 1;
                } else {
                    return { node: currentNode, offset: currentOffset };
                }
            }
            idx += 1;
            currentNode = textNodes[idx];
            currentOffset = 0;
        }

        return { node: currentNode || node, offset: currentOffset };
    }

    /**
     * Move the caret backward until the previous visible character.
     */
    function moveBackwardPastBreaks(textNodes, indexMap, node, offset) {
        let idx = indexMap.get(node);
        let currentNode = node;
        let currentOffset = offset;

        while (currentNode) {
            const text = currentNode.nodeValue || '';
            while (currentOffset > 0) {
                const ch = text[currentOffset - 1];
                if (ch === '\n' || ch === '\r' || ch === ' ' || ch === '\t') {
                    currentOffset -= 1;
                } else {
                    return { node: currentNode, offset: currentOffset };
                }
            }
            idx -= 1;
            currentNode = textNodes[idx];
            if (!currentNode) {
                break;
            }
            currentOffset = currentNode.nodeValue ? currentNode.nodeValue.length : 0;
        }

        return {
            node: currentNode || node,
            offset: currentNode ? currentOffset : 0,
        };
    }

    /**
     * Locate the start-of-line boundary for a node/offset pair.
     */
    function findLineStart(textNodes, indexMap, node, offset) {
        let idx = indexMap.get(node);
        let currentNode = node;
        let currentOffset = offset;
        const fallbackNode = textNodes[0] || node;

        while (currentNode) {
            const text = currentNode.nodeValue || '';
            let i = Math.min(currentOffset, text.length);
            while (i > 0) {
                const ch = text[i - 1];
                if (ch === '\n' || ch === '\r') {
                    return { node: currentNode, offset: i };
                }
                i -= 1;
            }
            idx -= 1;
            currentNode = textNodes[idx];
            if (!currentNode) {
                break;
            }
            currentOffset = currentNode.nodeValue ? currentNode.nodeValue.length : 0;
        }

        return { node: fallbackNode, offset: 0 };
    }

    /**
     * Locate the end-of-line boundary for a node/offset pair.
     */
    function findLineEnd(textNodes, indexMap, node, offset) {
        let idx = indexMap.get(node);
        let currentNode = node;
        let currentOffset = offset;
        const fallbackNode = textNodes[textNodes.length - 1] || node;

        while (currentNode) {
            const text = currentNode.nodeValue || '';
            let i = currentOffset;
            while (i < text.length) {
                const ch = text[i];
                if (ch === '\n' || ch === '\r') {
                    return { node: currentNode, offset: i };
                }
                i += 1;
            }
            idx += 1;
            currentNode = textNodes[idx];
            currentOffset = 0;
        }

        const fallbackOffset = fallbackNode && fallbackNode.nodeValue ? fallbackNode.nodeValue.length : 0;
        return { node: fallbackNode, offset: fallbackOffset };
    }

    /**
     * Removes indentation directly preceding a marker in-place so the entire line
     * vanishes once the marker comment is deleted.
     */
    function removeLeadingWhitespace(textNodes, indexMap, node, offset) {
        let idx = indexMap.get(node);
        let currentNode = node;
        let currentOffset = offset;

        while (currentNode) {
            const text = currentNode.nodeValue || '';
            while (currentOffset > 0) {
                const ch = text[currentOffset - 1];
                if (ch === ' ' || ch === '\t') {
                    currentNode.deleteData(currentOffset - 1, 1);
                    currentOffset -= 1;
                } else if (ch === '\n' || ch === '\r') {
                    return;
                } else {
                    return;
                }
            }
            idx -= 1;
            currentNode = textNodes[idx];
            if (!currentNode) {
                break;
            }
            currentOffset = currentNode.nodeValue ? currentNode.nodeValue.length : 0;
        }
    }

    /**
     * Remove trailing newline characters after a marker to avoid leaving blank rows.
     */
    function removeFollowingLineBreaks(textNodes, indexMap, node, offset) {
        let idx = indexMap.get(node);
        let currentNode = node;
        let currentOffset = offset;

        while (currentNode) {
            const text = currentNode.nodeValue || '';
            if (currentOffset >= text.length) {
                idx += 1;
                currentNode = textNodes[idx];
                currentOffset = 0;
                continue;
            }

            const ch = text[currentOffset];
            if (ch === '\r' || ch === '\n') {
                currentNode.deleteData(currentOffset, 1);
                continue;
            }
            break;
        }
    }

    /**
     * Process a single code element, applying highlights and removing marker lines.
     * @param {HTMLElement} code
     */
    function processCodeBlock(code) {
        const walker = document.createTreeWalker(code, NodeFilter.SHOW_TEXT, null);
        const textNodes = [];
        let node;
        while ((node = walker.nextNode())) {
            textNodes.push(node);
        }

        const indexMap = new Map(textNodes.map((textNode, idx) => [textNode, idx]));

        let activeRange = null;
        let activeColor = null;

        textNodes.forEach(textNode => {
            let text = textNode.nodeValue;
            if (!text || !text.includes('HIGHLIGHT_')) {
                return;
            }

            MARKER_REGEX.lastIndex = 0;

            let match;
            while ((match = MARKER_REGEX.exec(text)) !== null) {
                const matchStart = match.index;
                const matchLength = match[0].length;
                const color = match[1].toUpperCase();
                const type = match[2];

                removeLeadingWhitespace(textNodes, indexMap, textNode, matchStart);
                textNode.deleteData(matchStart, matchLength);
                text = textNode.nodeValue || '';
                removeFollowingLineBreaks(
                    textNodes,
                    indexMap,
                    textNode,
                    Math.min(matchStart, textNode.nodeValue ? textNode.nodeValue.length : 0)
                );

                if (type === 'BEGIN') {
                    const range = document.createRange();
                    const { node: startNode, offset: startOffset } = moveForwardPastBreaks(
                        textNodes,
                        indexMap,
                        textNode,
                        Math.min(matchStart, textNode.nodeValue.length)
                    );
                    range.setStart(startNode || textNode, startOffset);
                    activeRange = range;
                    activeColor = color;
                } else if (activeRange) {
                    const { node: endNode, offset: endOffset } = moveBackwardPastBreaks(
                        textNodes,
                        indexMap,
                        textNode,
                        Math.min(matchStart, textNode.nodeValue.length)
                    );
                    activeRange.setEnd(endNode || textNode, endOffset);
                    const startBoundary = findLineStart(
                        textNodes,
                        indexMap,
                        activeRange.startContainer,
                        activeRange.startOffset
                    );
                    const endBoundary = findLineEnd(
                        textNodes,
                        indexMap,
                        activeRange.endContainer,
                        activeRange.endOffset
                    );
                    activeRange.setStart(startBoundary.node || activeRange.startContainer, startBoundary.offset);
                    activeRange.setEnd(endBoundary.node || activeRange.endContainer, endBoundary.offset);
                    wrapRange(activeRange, activeColor);
                    activeRange = null;
                    activeColor = null;
                }

                MARKER_REGEX.lastIndex = matchStart;
            }
        });
    }

     document
        .querySelectorAll('pre > code.language-java')
        .forEach(processCodeBlock);
})();
