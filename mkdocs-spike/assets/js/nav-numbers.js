/* Lihavoi lukunumerot sivupalkissa, kuten mdBook tekee.
 *
 * Numero syntyy convert.py:ssä osaksi nav-otsikkoa ("6.1. Nimi"), joten sitä ei
 * voi valita CSS:llä. Material käärii otsikon <span class="md-ellipsis">:iin,
 * jonka sisällä teksti on välilyöntien ympäröimänä tekstisolmuna. */
(function () {
    "use strict";

    var NUMBER = /^(\d+(?:\.\d+)*\.)\s+/;

    function text_node_of(label) {
        for (var i = 0; i < label.childNodes.length; i += 1) {
            var node = label.childNodes[i];
            if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
                return node;
            }
        }
        return null;
    }

    function decorate(label) {
        if (label.dataset.navNumbered === "1") {
            return;
        }
        var node = text_node_of(label);
        if (!node) {
            return;
        }
        var match = NUMBER.exec(node.textContent.trim());
        if (!match) {
            return;
        }
        label.dataset.navNumbered = "1";

        var span = document.createElement("span");
        span.className = "nav-number";
        span.textContent = match[1];
        node.textContent = node.textContent.trim().slice(match[0].length);
        label.insertBefore(document.createTextNode(" "), node);
        label.insertBefore(span, label.firstChild);
    }

    function run() {
        document.querySelectorAll(".md-nav__link .md-ellipsis").forEach(decorate);
    }

    if (typeof document$ !== "undefined") {
        document$.subscribe(run);
    } else {
        document.addEventListener("DOMContentLoaded", run);
    }
})();
