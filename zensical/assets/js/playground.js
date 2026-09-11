/* Java-ohjelmien ajonapit: koodilohkon nappi lähettää koodin JYU:n
 * suorituspalvelimelle ja näyttää tulosteen koodin alle, kuten mdBookin
 * theme/playground_ext.js. Pyyntö on kenttä kentältä sama kuin mdBookissa.
 *
 * Nappi on teeman oma koodilohkon nappi (nav.md-code__nav > button.md-code__button),
 * joten ulkoasu tulee teemalta; omaa on vain kuvake (assets/css/playground.css).
 * Tuloste on tavallinen koodilohko (div.highlight). Editoitavia lohkoja ei ole:
 * ajetaan se koodi, joka sivulla lukee. */

(() => {
  "use strict";

  /* mdBookin PLAYGROUND_LANGS. */
  const LANGUAGES = ["java", "javascript"];

  /* mdBookin määreet, jotka jättävät napin pois; luokkina lohkon divissä
   * (convert.py: fence_info). */
  const SKIPPED = ["ignore", "noplayground"];

  /* Sama palvelin ja sama aikaraja kuin mdBookissa. */
  const EXECUTOR = "https://lakane.it.jyu.fi/executor/execute";
  const TIMEOUT = 6000;

  const language = (block) =>
    LANGUAGES.find((lang) => block.classList.contains(`language-${lang}`));

  const runnable = (block) =>
    language(block) && !SKIPPED.some((cls) => block.classList.contains(cls));

  /* textContent on pelkkää koodia: rivinumeroankkurit ovat tyhjiä <a>-elementtejä,
   * ja piilorivit lähtevät mukaan, koska CSS-piilotus ei vaikuta siihen. */
  const source = (block) => block.querySelector("code").textContent;

  /* Monitiedostolohkon tiedostot nimi -> sisältö: välilehtien otsikot ja
   * niiden koodilohkot samassa järjestyksessä, kuten mdBook lähettää. */
  const files = (set) => {
    const names = [...set.querySelectorAll(":scope > .tabbed-labels > label")];
    const blocks = [
      ...set.querySelectorAll(":scope > .tabbed-content > .tabbed-block"),
    ];
    return Object.fromEntries(
      names.map((name, index) => [name.textContent.trim(), source(blocks[index])]));
  };

  /* Ajettavat yksiköt: tavallinen lohko on yksi ohjelma, monitiedostolohkon
   * välilehdet yhdessä yksi. Avain on elementti, jonka perään tuloste tulee. */
  const units = new Map();
  for (const block of document.querySelectorAll("div.highlight")) {
    if (!runnable(block)) continue;
    const set = block.classList.contains("multifile")
      ? block.closest(".tabbed-set") : null;
    const unit = units.get(set || block) || [];
    unit.push(block);
    units.set(set || block, unit);
  }

  /* Nappirivi tehdään itse, koska teema tekee sen vain kopiointi- tai
   * valintanapin kanssa (content.code.copy/select), joita ei ole käytössä.
   * Jos teeman rivi on olemassa, käytetään sitä. */
  const addButton = (block) => {
    const code = block.querySelector("code");
    const pre = code.parentElement;
    let nav = pre.querySelector(":scope > nav.md-code__nav");
    if (!nav) {
      nav = document.createElement("nav");
      nav.className = "md-code__nav";
      pre.insertBefore(nav, code);
    }
    const button = document.createElement("button");
    button.className = "md-code__button";
    button.dataset.mdType = "run";
    button.title = "Suorita ohjelma";
    button.setAttribute("aria-label", button.title);
    nav.append(button);
    return button;
  };

  /* Tuloste koodin alle tavallisena koodilohkona; toinen ajo korvaa edellisen. */
  const outputFor = (anchor) => {
    let result = anchor.nextElementSibling;
    if (!result || !result.classList.contains("jyu-result")) {
      result = document.createElement("div");
      result.className = "language-text highlight jyu-result";
      result.innerHTML = "<pre><code></code></pre>";
      anchor.after(result);
    }
    return result.querySelector("code");
  };

  const say = (output, text, empty = false) => {
    output.textContent = text;
    output.classList.toggle("jyu-result-no-output", empty);
  };

  const run = async (anchor, blocks, buttons) => {
    const output = outputFor(anchor);
    const set = anchor.classList.contains("tabbed-set") ? anchor : null;
    buttons.forEach((button) => (button.disabled = true));
    say(output, "Suoritetaan…");

    /* Aikaraja katkaisee myös pyynnön; nappi palaa käyttöön ja tuloste kertoo syyn. */
    const abort = new AbortController();
    const timer = setTimeout(() => abort.abort(), TIMEOUT);
    try {
      const response = await fetch(EXECUTOR, {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          language: language(blocks[0]),
          code: set ? JSON.stringify(files(set)) : source(blocks[0]),
          multifile: Boolean(set),
        }),
        signal: abort.signal,
      });
      const body = await response.json();
      /* Kuten mdBookissa: virheet ensin, muuten tuloste. Kääntäjän virheet
       * tulevat output-kentässä. Lopun rivinvaihto pois, koska se näkyisi
       * laatikossa tyhjänä rivinä. */
      const text = (body.errors || body.output || "").replace(/\n+$/, "");
      say(output, text || "Ei tulostetta", !text);
    } catch (error) {
      say(output, error.name === "AbortError"
        ? `Ohjelma ei vastannut ${TIMEOUT / 1000} sekunnissa.`
        : `Suorituspalvelimeen ei saatu yhteyttä: ${error.message}`);
    } finally {
      clearTimeout(timer);
      buttons.forEach((button) => (button.disabled = false));
    }
  };

  for (const [anchor, blocks] of units) {
    const buttons = blocks.map(addButton);
    for (const button of buttons) {
      button.addEventListener("click", () => run(anchor, blocks, buttons));
    }
  }
})();
