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

        /* mdbook wraps hidden ("//-") lines in <span class="boring">; step 2 below
           nukes those spans, so remember which raw lines they covered. */
        var boringRaw = [];
        var rawIdx = 0;
        code.childNodes.forEach(function (node) {
            var isBoring = node.nodeType === 1 && node.classList.contains('boring');
            var parts = node.textContent.split('\n');
            for (var i = 0; i < parts.length; i++) {
                if (i > 0) rawIdx++;
                if (isBoring && parts[i] !== '') boringRaw[rawIdx] = true;
            }
        });

        /* ---- 1. Parse markers ---- */
        var lineColors = [];   // one entry per non-marker line: null | "GREEN" | …
        var lineBoring = [];   // same indexing: was this line hidden?
        var hasMarkers = false;
        var active = null;

        for (var i = 0; i < rawLines.length; i++) {
            var m = rawLines[i].match(MARKER_RE);
            if (m) {
                hasMarkers = true;
                active = m[2] === 'BEGIN' ? m[1].toUpperCase() : null;
            } else {
                lineColors.push(active);
                lineBoring.push(!!boringRaw[i]);
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

        /* ---- 3. Handle horizontal overflow ---- */
        var pre = code.parentElement;
        if (pre.scrollWidth > pre.clientWidth) {
            /* Content overflows: make <code> inline-block so that its
               block-level .hl-line children inherit the full content
               width rather than just the visible width. */
            code.style.display  = 'inline-block';
            code.style.minWidth = '100%';
        }

        /* ---- 4. Wrap highlighted lines ---- */
        var htmlLines = code.innerHTML.split('\n');
        var out = '';
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
                full = '<span class="hl-line hl-' + color.toLowerCase() + '">' + full + '</span>';
            }

            var nl = j < htmlLines.length - 1 ? '\n' : '';
            out += lineBoring[j] ? '<span class="boring">' + full + nl + '</span>' : full + nl;
        }

        code.innerHTML = out;
    });
})();
