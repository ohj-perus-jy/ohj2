(function javaCodeHighlights() {
    /**
     * Java code highlighter for mdBook.
     *
     * For each `pre > code.language-java` block:
     *   1. Reads textContent, parses HIGHLIGHT markers, builds a per-line color map.
     *   2. Strips marker lines from the text and re-runs hljs for syntax coloring.
     *   3. Splits the resulting innerHTML at newlines, wraps highlighted lines in
     *      a <span class="hl-line hl-green"> etc., and writes innerHTML back.
     *
     * Because each line is made self-contained (unclosed hljs spans are closed
     * and re-opened), the wrapping never conflicts with hljs DOM structure.
     */
    var MARKER_RE = /^\s*\/\/\s*HIGHLIGHT_([A-Z0-9]+)_(BEGIN|END)\s*$/;

    document.querySelectorAll('pre > code.language-java').forEach(function (code) {
        var rawLines = code.textContent.split('\n');

        /* ---- 1. Parse markers ---- */
        var lineColors = [];   // one entry per non-marker line: null | "GREEN" | …
        var hasMarkers = false;
        var active = null;

        for (var i = 0; i < rawLines.length; i++) {
            var m = rawLines[i].match(MARKER_RE);
            if (m) {
                hasMarkers = true;
                active = m[2] === 'BEGIN' ? m[1].toUpperCase() : null;
            } else {
                lineColors.push(active);
            }
        }

        if (!hasMarkers) return;

        /* ---- 2. Strip markers and re-run hljs ---- */
        var clean = [];
        for (var i = 0; i < rawLines.length; i++) {
            if (!rawLines[i].match(MARKER_RE)) clean.push(rawLines[i]);
        }
        code.textContent = clean.join('\n');

        if (typeof hljs !== 'undefined') {
            code.removeAttribute('data-highlighted');
            if (hljs.highlightElement) hljs.highlightElement(code);
            else if (hljs.highlightBlock) hljs.highlightBlock(code);
        }

        /* ---- 3. Wrap highlighted lines ---- */
        var htmlLines = code.innerHTML.split('\n');
        var result = [];
        var openTags = [];  // stack of opening <span …> strings

        for (var j = 0; j < htmlLines.length; j++) {
            var line = htmlLines[j];
            var color = j < lineColors.length ? lineColors[j] : null;

            // Re-open spans left open from previous line
            var prefix = openTags.join('');
            var suffix = '';
            for (var k = 0; k < openTags.length; k++) suffix += '</span>';

            // Track which spans open/close within this line
            var re = /<(\/?)span([^>]*)>/g;
            var tm;
            while ((tm = re.exec(line)) !== null) {
                if (tm[1] === '/') openTags.pop();
                else openTags.push('<span' + tm[2] + '>');
            }

            // Self-contained line fragment
            var full = prefix + line + suffix;

            if (color) {
                result.push('<span class="hl-line hl-' + color.toLowerCase() + '">' + full + '&#8203;</span>');
            } else {
                result.push(full);
            }
        }

        code.innerHTML = result.join('\n');
    });
})();
