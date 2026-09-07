/* mdBookin //- piilorivien vastine.
 *
 * convert.py on riisunut //- etuliitteen ja tallentanut rivinumerot
 * data-boring-attribuuttiin. pymdownx.highlight (line_spans) on kääriny
 * jokaisen rivin omaan spaniin, joten rivit voi piilottaa yksitellen. */
(function () {
    "use strict";

    var EYE = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">'
        + '<path fill="currentColor" d="M12 9a3 3 0 1 1 0 6 3 3 0 0 1 0-6m0-4.5c5 0 9.27 3.11 11 '
        + '7.5-1.73 4.39-6 7.5-11 7.5S2.73 16.39 1 12c1.73-4.39 6-7.5 11-7.5M3.18 12a9.82 9.82 0 0 0 '
        + '17.64 0 9.82 9.82 0 0 0-17.64 0"/></svg>';

    function decorate(block) {
        if (block.dataset.boringReady === "1") {
            return;
        }
        block.dataset.boringReady = "1";

        var code = block.querySelector("code");
        if (!code) {
            return;
        }
        var lines = code.querySelectorAll(':scope > span[id^="__codeline"]');
        var numbers = block.dataset.boring.trim().split(/\s+/);
        var hidden = 0;
        numbers.forEach(function (raw) {
            var line = lines[parseInt(raw, 10) - 1];
            if (line) {
                line.classList.add("boring");
                hidden += 1;
            }
        });
        if (hidden === 0) {
            return;
        }

        block.classList.add("hide-boring");

        var button = document.createElement("button");
        button.className = "boring-toggle";
        button.innerHTML = EYE;
        button.title = "Näytä piilotetut rivit";
        button.setAttribute("aria-label", button.title);
        button.addEventListener("click", function () {
            var hiddenNow = block.classList.toggle("hide-boring");
            button.title = hiddenNow ? "Näytä piilotetut rivit" : "Piilota rivit";
            button.setAttribute("aria-label", button.title);
            button.classList.toggle("boring-toggle--open", !hiddenNow);
        });
        block.appendChild(button);
    }

    function run() {
        document.querySelectorAll(".highlight[data-boring]").forEach(decorate);
    }

    if (typeof document$ !== "undefined") {
        document$.subscribe(run);
    } else {
        document.addEventListener("DOMContentLoaded", run);
    }
})();
