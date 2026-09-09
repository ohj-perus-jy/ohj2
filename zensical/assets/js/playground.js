/* Java-ohjelmien ajonapit (README.md kohta 3).
 *
 * mdBookissa jokainen ```java-lohko, jossa ei ole määrettä ignore eikä
 * noplayground, saa oikeaan yläkulmaan nuolinapin: se lähettää lohkon koodin
 * JYU:n suorituspalvelimelle ja näyttää tulosteen koodin alle
 * (theme/playground_ext.js). Sama tehdään tässä, ja pyyntö on kenttä kentältä
 * sama kuin mdBookissa — sama palvelin, samat kentät — joten kirjan koodit
 * ajetaan täsmälleen kuten ennenkin.
 *
 * Kolme asiaa tulee teemalta eikä tästä tiedostosta:
 *
 *  - Nappi on teeman oma koodilohkon nappi (nav.md-code__nav >
 *    button.md-code__button, samat luokat kuin kopiointi- ja
 *    valintanapissa), joten paikka, koko, värit ja hover-käytös tulevat
 *    teeman CSS:stä. Omaa tyyliä on vain kuvake, ks. assets/css/playground.css.
 *  - Tuloste on tavallinen koodilohko (div.highlight), eli teema piirtää sen
 *    samalla tavalla kuin koodin. Myös mdBookissa tuloste on koodilohkon
 *    näköinen laatikko koodin alla (theme/css/chrome.css: pre > .result).
 *  - Monitiedostolohkon välilehdet ovat teeman välilehtiä (kohta 5).
 *
 * Piilorivit (kohta 2) lähtevät ajoon siinä missä muutkin rivit: ne ovat
 * lohkon HTML:ssä tallessa, vaikka CSS piilottaa ne, eikä textContent välitä
 * näkyvyydestä. Etuliite "//-" on riisuttu jo käännösaikana (convert.py:
 * hide_lines), kuten mdBookissakin.
 *
 * ACE-editori (kohta 20) puuttuu, joten kahdessa editable-lohkossa ajetaan se
 * koodi, joka sivulla lukee — muokata sitä ei voi.
 */

(() => {
  "use strict";

  /* mdBookin theme/playground_ext.js: PLAYGROUND_LANGS. */
  const LANGUAGES = ["java", "javascript"];

  /* mdBookin määreet, jotka jättävät napin pois. Ne ovat luokkina
   * lohkon divissä, ks. convert.py: fence_info (kohta 4). */
  const SKIPPED = ["ignore", "noplayground"];

  /* Sama palvelin ja sama 6 sekunnin raja kuin mdBookissa. Mitattuna yhden
   * ohjelman kääntäminen ja ajaminen kestää 2,5-3,4 s ja saman koodin toisto
   * 0,07 s (palvelin muistaa tuloksen), eli raja on väljä muttei ylenpalttinen. */
  const EXECUTOR = "https://lakane.it.jyu.fi/executor/execute";
  const TIMEOUT = 6000;

  const language = (block) =>
    LANGUAGES.find((lang) => block.classList.contains(`language-${lang}`));

  const runnable = (block) =>
    language(block) && !SKIPPED.some((cls) => block.classList.contains(cls));

  /* Lohkon koodi ajettavassa muodossa. Rivinumeroankkurit ovat tyhjiä
   * <a>-elementtejä ja piilorivit tavallista koodia, joten textContent on
   * pelkkää koodia — juuri se, jonka mdBookkin lähettää. */
  const source = (block) => block.querySelector("code").textContent;

  /* Monitiedostolohkon tiedostot nimi -> sisältö. Nimet ovat välilehtien
   * otsikoita ja sisällöt niiden koodilohkoja, samassa järjestyksessä; sama
   * hakemisto kuin mdBook lähettää (playground_ext.js: run_code). */
  const files = (set) => {
    const names = [...set.querySelectorAll(":scope > .tabbed-labels > label")];
    const blocks = [
      ...set.querySelectorAll(":scope > .tabbed-content > .tabbed-block"),
    ];
    return Object.fromEntries(
      names.map((name, index) => [name.textContent.trim(), source(blocks[index])]));
  };

  /* Ajettavat lohkot yksiköiksi: tavallinen lohko on yksi ohjelma, ja
   * monitiedostolohkon välilehdet ovat yhdessä yksi ohjelma. Avain on se
   * elementti, jonka perään tuloste tulee. */
  const units = new Map();
  for (const block of document.querySelectorAll("div.highlight")) {
    if (!runnable(block)) continue;
    const set = block.classList.contains("multifile")
      ? block.closest(".tabbed-set") : null;
    const unit = units.get(set || block) || [];
    unit.push(block);
    units.set(set || block, unit);
  }

  /* Nappi lohkon omaan nappiriviin. Teema tekee rivin itse vain, jos
   * kopiointi- tai valintanappi on käytössä (mkdocs.yml: content.code.copy,
   * content.code.select) — kumpaakaan ei ole, joten rivi tehdään tässä
   * samannimisenä ja samaan paikkaan kuin teema sen tekisi (pre:n sisään
   * ennen koodia). Jos napit joskus otetaan käyttöön, tämä käyttää teeman
   * riviä eikä tee omaansa. */
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

  /* Tuloste koodin alle. Se on tavallinen koodilohko, joten teema piirtää sen
   * samalla tavalla kuin koodin: sama tausta, sama kirjasin, samat reunat ja
   * sama vieritys pitkillä riveillä. Sama elementti myös uusitaan, eli toinen
   * ajo korvaa edellisen tulosteen. */
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

    /* Vastaus voi jäädä tulematta, ja silloin napin pitää palata käyttöön ja
     * tulosteessa lukea miksi. mdBook kilpailuttaa fetchin ajastinta vastaan
     * ja jättää pyynnön käyntiin; AbortController tekee saman ja katkaisee
     * myös pyynnön. */
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
      /* Sama järjestys kuin mdBookissa: virheet ensin, muuten tuloste.
       * Kääntäjän virheilmoitukset tulevat tältä palvelimelta output-kentässä,
       * eli myös ne näkyvät tässä. Lopun rivinvaihto pois, koska se näkyisi
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
