/* Korostetut rivit (README.md kohta 9).
 *
 * mdBookissa koodilohkon sisällä oleva merkintäpari
 * ("// HIGHLIGHT_GREEN_BEGIN" ... "// HIGHLIGHT_GREEN_END") antaa väliin
 * jääville riveille värillisen taustan, ja merkintärivit itse jäävät pois
 * (theme/code-highlights.js). Merkinnät riisuu ja rivien numerot aidan
 * attribuuteiksi (data-hl-green="2 3") kirjoittaa convert.py
 * (mark_highlights); tähän jää numeroiden muuttaminen luokiksi.
 *
 * Rivit ovat Pygmentsin rivispaneja (Zensicalin oletus line_spans: "__span"),
 * eli koodilohkon <code>:n suorat span-lapset — sama tie kuin piiloriveillä
 * (assets/js/hidelines.js), ja samasta syystä: Markdownissa ei ole tapaa
 * merkitä yksittäistä koodiriviä.
 *
 * Ero mdBookiin on siinä, mitä selaimen on tehtävä. Siellä rivejä ei ole
 * elementteinä, joten skripti joutuu ajamaan korostuksen uudestaan, pilkkomaan
 * hljs:n tuottaman HTML:n riveiksi ja sulkemaan ja avaamaan kesken rivin
 * jäävät spanit itse (~100 riviä). Täällä rivit ovat valmiina omina
 * elementteinään, joten työ on luokan lisääminen.
 */

(() => {
  "use strict";

  /* Attribuutin nimi kertoo värin: data-hl-green -> dataset.hlGreen -> hl-green.
   * Väriä ei tunneta tässä nimeltä, vaan CSS päättää mitä kukin väri on
   * (assets/css/highlights.css). */
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

  /* Tulostussivun luvut haetaan vasta sivun latauduttua (print.js), joten ne
   * eivät olleet olemassa yllä; ilman tätä korostukset jäisivät kirjasta pois.
   * Sama kytkentä kuin piiloriveillä. */
  addEventListener("jyu-print-assembled", () => paint(document));
})();
