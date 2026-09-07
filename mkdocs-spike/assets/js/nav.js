/* Sivupalkin näyttö/piilo -nappi, kuten mdBookissa.
 *
 * Material näyttää sivupalkin työpöydällä aina; hampurilaisnappi on vain
 * mobiilissa. Lisätään headeriin oma nappi, joka piilottaa palkin ja muistaa
 * valinnan. */
(function () {
    "use strict";

    var KEY = "jyu-nav-hidden";
    var ICON = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">'
        + '<path fill="currentColor" d="M3 5h18v2H3V5m0 6h18v2H3v-2m0 6h18v2H3v-2Z"/></svg>';

    function stored() {
        try {
            return localStorage.getItem(KEY) === "1";
        } catch (error) {
            return false;
        }
    }

    function store(hidden) {
        try {
            localStorage.setItem(KEY, hidden ? "1" : "0");
        } catch (error) {
            /* privaatti selausikkuna — valinta ei säily, ei haittaa */
        }
    }

    function apply(hidden, button) {
        document.body.classList.toggle("jyu-nav-hidden", hidden);
        button.setAttribute("aria-pressed", hidden ? "true" : "false");
        button.title = hidden ? "Näytä sisällysluettelo" : "Piilota sisällysluettelo";
        button.setAttribute("aria-label", button.title);
    }

    function install() {
        if (document.querySelector(".jyu-nav-toggle")) {
            return;
        }
        var header = document.querySelector(".md-header__inner");
        var title = header && header.querySelector(".md-header__title");
        if (!header || !title) {
            return;
        }

        var button = document.createElement("button");
        button.className = "md-header__button md-icon jyu-nav-toggle";
        button.type = "button";
        button.innerHTML = ICON;
        header.insertBefore(button, title);

        apply(stored(), button);
        button.addEventListener("click", function () {
            var hidden = !document.body.classList.contains("jyu-nav-hidden");
            apply(hidden, button);
            store(hidden);
        });
    }

    if (typeof document$ !== "undefined") {
        document$.subscribe(install);
    } else {
        document.addEventListener("DOMContentLoaded", install);
    }
})();
