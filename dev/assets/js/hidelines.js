/* Piilorivit ja silmänappi, kuten mdBookin hide-boring. convert.py riisuu
 * "//-"-etuliitteen ja kirjoittaa piilorivien numerot lohkon diviin
 * (data-hidden="1 5"); tässä rivit saavat luokan boring ja lohko napin.
 *
 * Rivit ovat Pygmentsin rivispaneja (line_spans), <code>:n suorat span-lapset
 * lähteen järjestyksessä. Tunnisteisiin ei nojata, koska tulostussivu
 * kirjoittaa ne uusiksi (print.js). Nappi menee samaan teeman nappiriviin kuin
 * kopiointinappi ja ajonappi (playground.js).
 *
 * Piilotilassa näkyvä koodi on vasemmassa reunassa: näkyvien rivien yhteinen
 * sisennys (esim. Main-metodin rungon kahdeksan välilyöntiä) siirretään omaan
 * spaniin, joka piilotetaan piilorivien mukana ja tulee esiin niiden kanssa.
 * Lähteessä ohjelma on siis kirjoitettu kokonaan oikein sisennettynä. Silmän
 * painallus liu'uttaa rivit ja sisennyksen auki (hidelines.css). Aidan
 * määre eyehint opastaa silmän luo (hints.js). */

(() => {
  "use strict";

  /* aria-pressed kertoo asennon ja valitsee kuvakkeen (assets/css/hidelines.css). */
  const label = (button, shown) => {
    button.setAttribute("aria-pressed", String(shown));
    button.title = shown ? "Piilota rivit" : "Näytä piilotetut rivit";
    button.setAttribute("aria-label", button.title);
  };

  /* Teema tekee kopiointinapin rivin vasta DOMContentLoaded-tapahtumassa eikä
   * katso, onko rivi jo olemassa; sama lykkäys kuin playground.js:ssä. Rivit
   * piilotetaan silti heti, ettei piilorivi vilahda ennen tapahtumaa. */
  const afterTheme = (callback) => {
    if (document.readyState === "loading") {
      addEventListener("DOMContentLoaded", callback);
    } else {
      callback();
    }
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
      code.classList.add("jyu-toggled");
      label(button, !code.classList.toggle("hide-boring"));
    });
    nav.append(button);
  };

  /* Rivin alun välilyönnit ja sarkaimet. */
  const leading = (line) => /^[ \t]*/.exec(line.textContent)[0];

  /* Näkyvien rivien (ei piilorivi, ei tyhjä) pisin yhteinen sisennys. Verrataan
   * merkkijonoja, ei pituuksia, jotta sarkaimet ja välilyönnit eivät sekoitu. */
  const commonIndent = (lines) => {
    let common = null;
    for (const line of lines) {
      if (line.classList.contains("boring") || !line.textContent.trim()) continue;
      const indent = leading(line);
      if (common === null) {
        common = indent;
        continue;
      }
      let length = 0;
      while (length < common.length && common[length] === indent[length]) length++;
      common = common.slice(0, length);
      if (!common) break;
    }
    return common ?? "";
  };

  /* Sisennyksen alusta `indent` omaan spaniin. Välilyönnit ovat Pygmentsin
   * tekstisolmuissa (yleensä yksi span.w), mutta ne voivat jakautua useampaan,
   * joten solmuja käydään läpi, kunnes merkit on otettu. Span tulee rivin
   * suoraksi lapseksi ensimmäisen tekstiä sisältävän lapsen eteen, jotta se
   * ei jää tyhjentyneen tokenin sisään. */
  const dedent = (line, indent) => {
    if (!indent || !line.textContent.trim() || !leading(line).startsWith(indent)) return;
    const walker = document.createTreeWalker(line, NodeFilter.SHOW_TEXT);
    let remaining = indent.length;
    let first = null;
    for (let node = walker.nextNode(); node && remaining > 0; node = walker.nextNode()) {
      if (!node.data) continue;
      first ??= node;
      const taken = Math.min(remaining, node.data.length);
      node.data = node.data.slice(taken);
      remaining -= taken;
    }
    let child = first;
    while (child.parentNode !== line) child = child.parentNode;
    const span = document.createElement("span");
    span.className = "jyu-indent";
    span.textContent = indent;
    /* Leveys tyylille (hidelines.css) ch-yksikköinä: sarkain on tab-sizen
     * verran välilyöntejä. */
    const tabSize = Number(getComputedStyle(line).tabSize) || 8;
    span.style.setProperty(
      "--jyu-indent", String(indent.replace(/\t/g, " ".repeat(tabSize)).length));
    line.insertBefore(span, child);
  };

  const hide = (root) => {
    for (const block of root.querySelectorAll("div.highlight[data-hidden]")) {
      const code = block.querySelector("code");
      if (!code || code.querySelector(":scope > span.boring")) continue;
      const lines = code.querySelectorAll(":scope > span");
      for (const number of block.dataset.hidden.split(" ")) {
        lines[Number(number) - 1]?.classList.add("boring");
      }
      const indent = commonIndent(lines);
      for (const line of lines) {
        if (!line.classList.contains("boring")) dedent(line, indent);
      }
      code.classList.add("hide-boring");
      afterTheme(() => addButton(code));
    }
  };

  hide(document);

  /* Tulostussivun luvut tulevat sivulle vasta myöhemmin (print.js); ilman
   * tätä piilorivit tulostuisivat kirjan mukana. */
  addEventListener("jyu-print-assembled", () => hide(document));
})();
