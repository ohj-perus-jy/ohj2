/* Piilorivit näkyvistä ja silmänappi ne esiin (README.md kohta 2).
 *
 * mdBookissa "//-"-alkuinen rivi kuuluu ohjelmaan muttei näy sivulla:
 * esikäsittely riisuu etuliitteen ja kääri rivin <span class="boring">iin,
 * book.js piilottaa rivit (hide-boring) ja lisää lohkoon silmänapin, josta ne
 * saa esiin. Etuliitteen riisuu täällä convert.py (hide_lines) ja kirjoittaa
 * samalla piilorivien numerot lohkon diviin (data-hidden="1 5"), koska
 * Markdownissa ei ole tapaa merkitä yksittäistä koodiriviä. Loput on tässä.
 *
 * Rivit ovat Pygmentsin rivispaneja (Zensicalin oletus line_spans: "__span"),
 * eli koodilohkon <code>:n suorat span-lapset: yksi per rivi ja samassa
 * järjestyksessä kuin lähteessä. Niiden tunnisteisiin ei nojata, koska
 * tulostussivu kirjoittaa jokaisen tunnisteen uusiksi (print.js).
 *
 * Nappi menee samaan teeman nappiriviin kuin ajonappi (playground.js), kuten
 * mdBookissa (theme/css/chrome.css: pre > .buttons). Kumpi tahansa tiedosto
 * voi olla ensin: kumpikin tekee rivin vain, jos sitä ei vielä ole.
 */

(() => {
  "use strict";

  /* Napin teksti kertoo, mitä painaminen tekee, ja aria-pressed sen, kummassa
   * asennossa se on; sama attribuutti valitsee kuvakkeen
   * (assets/css/hidelines.css). */
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

  /* Tulostussivun luvut haetaan vasta sivun latauduttua (print.js), joten ne
   * eivät olleet olemassa yllä. Ilman tätä piilorivit tulostuisivat kirjan
   * mukana; mdBookissa print.html on tavallinen sivu, jolla book.js tekee
   * saman kuin muillakin sivuilla. */
  addEventListener("jyu-print-assembled", () => hide(document));
})();
