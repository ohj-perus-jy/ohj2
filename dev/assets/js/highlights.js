/* Korostetut rivit. mdBookin merkintäparit (// HIGHLIGHT_GREEN_BEGIN ... END)
 * riisuu convert.py (mark_highlights) ja kirjoittaa rivinumerot aidan
 * attribuuteiksi (data-hl-green="2 3"); tässä numerot muutetaan luokiksi.
 * Rivit ovat Pygmentsin rivispaneja, <code>:n suorat span-lapset, kuten
 * piiloriveillä (hidelines.js). */

(() => {
  "use strict";

  /* Attribuutin nimi kertoo värin: data-hl-green -> hl-green. Värin itse
   * määrittelee CSS (assets/css/highlights.css). */
  const paint = (root) => {
    for (const block of root.querySelectorAll("div.highlight")) {
      const code = block.querySelector("code");
      if (!code) continue;
      const lines = code.querySelectorAll(":scope > span");
      for (const [name, numbers] of Object.entries(block.dataset)) {
        if (!/^hl[A-Z]/.test(name)) continue;
        const color = `hl-${name.slice(2).toLowerCase()}`;
        for (const number of numbers.split(" ")) {
          lines[Number(number) - 1]?.classList.add("hl-line", color);
        }
      }
    }
  };

  paint(document);

  /* Tulostussivun luvut tulevat sivulle vasta myöhemmin (print.js). */
  addEventListener("jyu-print-assembled", () => paint(document));
})();
