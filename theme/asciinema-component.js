(() => {
    const elements = document.querySelectorAll('asciinema[src]');

    for (const el of elements) {
        const src = el.getAttribute('src');
        const rows = +el.getAttribute('rows') || 24;
        const poster = el.getAttribute('poster') || undefined;
        const controls = el.getAttribute('controls') !== null;

        AsciinemaPlayer.create(src, el, {
            rows: rows,
            controls: controls,
            poster: poster,
            terminalFontSize: "12px",
            fit: false,
        });
    }
})();