/* Piilorivit ja silmänappi, kuten mdBookin hide-boring. convert.py riisuu
 * "//-"-etuliitteen ja kirjoittaa piilorivien numerot lohkon diviin
 * (data-hidden="1 5"); tässä rivit saavat luokan boring ja lohko napin.
 *
 * Rivit ovat Pygmentsin rivispaneja (line_spans), <code>:n suorat span-lapset
 * lähteen järjestyksessä. Tunnisteisiin ei nojata, koska tulostussivu
 * kirjoittaa ne uusiksi (print.js). Nappi menee samaan teeman nappiriviin kuin
 * ajonappi (playground.js); kumpi tahansa tiedosto voi olla ensin. */

(() => {
  "use strict";

  /* aria-pressed kertoo asennon ja valitsee kuvakkeen (assets/css/hidelines.css). */
  const label = (button, shown) => {
    button.setAttribute("aria-pressed", String(shown));
    button.title = shown ? "Piilota rivit" : "Näytä piilotetut rivit";
    button.setAttribute("aria-label", button.title);
  };

  const addButton = (code) => {
    const pre = code.parentElement;
    let nav = pre.querySelector(":scope > nav.md-code__nav");
    if (!nav) {
      nav = document.createElement("nav");
      nav.className = "md-code__nav";
      pre.insertBefore(nav, code);
    }
    const button = document.createElement("button");
    button.className = "md-code__button";
    button.dataset.mdType = "hidelines";
    label(button, false);
    button.addEventListener("click", () => {
      label(button, !code.classList.toggle("hide-boring"));
    });
    nav.append(button);
  };

  const hide = (root) => {
    for (const block of root.querySelectorAll("div.highlight[data-hidden]")) {
      const code = block.querySelector("code");
      if (!code || code.querySelector(":scope > span.boring")) continue;
      const lines = code.querySelectorAll(":scope > span");
      for (const number of block.dataset.hidden.split(" ")) {
        lines[Number(number) - 1]?.classList.add("boring");
      }
      code.classList.add("hide-boring");
      addButton(code);
    }
  };

  hide(document);

  /* Tulostussivun luvut tulevat sivulle vasta myöhemmin (print.js); ilman
   * tätä piilorivit tulostuisivat kirjan mukana. */
  addEventListener("jyu-print-assembled", () => hide(document));
})();
