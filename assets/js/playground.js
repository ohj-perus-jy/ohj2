/* C#-ohjelmien ajonapit: koodilohkon nappi lähettää koodin JYU:n
 * suorituspalvelimelle ja näyttää tulosteen koodin alle, kuten mdBookin
 * theme/playground_ext.js. Pyyntö on kenttä kentältä sama kuin mdBookissa.
 *
 * Nappi on teeman oma koodilohkon nappi (nav.md-code__nav > button.md-code__button),
 * joten ulkoasu tulee teemalta; omaa on vain kuvake (assets/css/playground.css).
 * Tuloste on tavallinen koodilohko (div.highlight). Ajetaan se koodi, joka
 * sivulla lukee; editable-lohkossa lukija saa muuttaa sitä (makeEditable). */

(() => {
  "use strict";

  /* mdBookin PLAYGROUND_LANG (ohj1: csharp); java ja javascript ohj2:n koekirjan
   * (tests/book) ja testien takia. */
  const LANGUAGES = ["csharp", "java", "javascript"];

  /* mdBookin "feature-jypeli"-määre: kieleksi lähetetään "csharp-jypeli", kuten
   * theme/playground_ext.js tekee. */
  const FEATURE_PREFIX = "feature-";

  /* Suorituspalvelin palauttaa Jypeli-ohjelman ruudun tulosteen sisällä kuvana
   * (data-URI merkkien välissä), kuten mdBookissa. */
  const DATA_URI_RE = /@@@DATA_URI_BEGIN@@@(.+?)@@@DATA_URI_END@@@/g;

  /* mdBookin määreet, jotka jättävät napin pois; luokkina lohkon divissä
   * (convert.py: fence_info). */
  const SKIPPED = ["ignore", "noplayground"];

  /* Sama palvelin ja sama aikaraja kuin mdBookissa. */
  const EXECUTOR = "https://lakane.it.jyu.fi/executor/execute";
  const TIMEOUT = 6000;

  const language = (block) =>
    LANGUAGES.find((lang) => block.classList.contains(`language-${lang}`));

  /* Palvelimelle lähetettävä kieli: kieli ja feature-määreet väliviivoin. */
  const executorLanguage = (block) => {
    const features = [...block.classList]
      .filter((cls) => cls.startsWith(FEATURE_PREFIX))
      .map((cls) => cls.slice(FEATURE_PREFIX.length));
    return [language(block), ...features].join("-");
  };

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

  /* Teema tekee kopiointinapin ja sen nappirivin (content.code.copy) vasta
   * DOMContentLoaded-tapahtumassa eikä katso, onko rivi jo olemassa. Omat
   * napit lisätään siksi vasta sen jälkeen samaan riviin: teeman kuuntelija
   * ehtii ensin, koska sen skripti on ladattu ennen tätä. Tulostussivulla
   * (print.js) tapahtuma on jo ohi ja lohkoilla ei ole teeman riviä. */
  const afterTheme = (callback) => {
    if (document.readyState === "loading") {
      addEventListener("DOMContentLoaded", callback);
    } else {
      callback();
    }
  };

  /* Nappi teeman riviin; ilman kopiointinappia (ignore, noplayground eivät
   * vaikuta siihen, mutta no-copy-luokka jättää sen pois) rivi tehdään itse. */
  const addButton = (block, type = "run", title = "Suorita ohjelma") => {
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
    button.dataset.mdType = type;
    button.title = title;
    button.setAttribute("aria-label", button.title);
    nav.append(button);
    return button;
  };

  /* Kohdistimen kohdalle tekstiä niin, että selaimen oma kumoaminen (Ctrl+Z)
   * toimii; Range-rajapinnalla lisätty teksti ei menisi kumoamispinoon. */
  const insert = (text) => document.execCommand("insertText", false, text);

  /* Kohdistimen rivin sisennys. Range.toString() lukee tekstisolmut kuten
   * textContent, joten piilorivit eivät sotke laskua. */
  const indentAtCaret = (code) => {
    const range = getSelection().getRangeAt(0).cloneRange();
    range.setStart(code, 0);
    return /[ \t]*/.exec(range.toString().split("\n").pop())[0];
  };

  /* Näkyvän koodin lopussa (viimeinen rivi tai piilorivien edellä) Chromium
   * käyttää rivin oman rivinvaihdon uuden rivin vaihdoksi, jolloin seuraava
   * (piilo)rivi jatkuisi kirjoitetun perään samalle riville. Rivit ovat
   * <code>:n suoria span-lapsia; kohdistimen rivi saa vaihtonsa takaisin. */
  const keepLineBreak = (code) => {
    let line = getSelection().anchorNode;
    while (line && line.parentNode !== code) line = line.parentNode;
    if (line?.nodeType === Node.ELEMENT_NODE && line.nextSibling
        && !line.textContent.endsWith("\n")) {
      line.append("\n");
    }
  };

  /* mdBookin "editable"-määre: koodia voi muuttaa sivulla. Editoria (ACE) ei
   * ole, vaan <code> on contenteditable. Ajonappi lukee koodin vasta ajaessaan
   * (source), joten muutettu koodi lähtee palvelimelle ilman muuta. Pygmentsin
   * väritys ei päivity kirjoittaessa: uusi teksti saa sen tokenin värin, jonka
   * sisään se kirjoitetaan. Selain ilman plaintext-only-tukea (Firefox < 136)
   * jättää lohkon tavalliseksi ajettavaksi lohkoksi. */
  const makeEditable = (block, runButton) => {
    const code = block.querySelector("code");
    try {
      code.contentEditable = "plaintext-only";
    } catch {
      return;
    }
    code.spellcheck = false;
    code.translate = false;
    code.setAttribute("autocapitalize", "off");
    code.setAttribute("autocorrect", "off");
    code.setAttribute("aria-label", "Muokattava koodi");

    /* Alkuperäinen talteen vasta kohdistuksessa: silloin hidelines.js ja
     * highlights.js ovat jo merkinneet rivinsä, ja peruutus palauttaa nekin. */
    let original = null;
    const reset = addButton(block, "reset", "Peruuta muutokset");
    reset.disabled = true;
    code.addEventListener("focus", () => (original ??= code.innerHTML));
    code.addEventListener("input", () => {
      reset.disabled = code.innerHTML === original;
    });
    reset.addEventListener("click", () => {
      code.innerHTML = original;
      reset.disabled = true;
    });

    code.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
        event.preventDefault();
        runButton.click();
      } else if (event.key === "Enter") {
        event.preventDefault();
        insert(`\n${indentAtCaret(code)}`);
        keepLineBreak(code);
      } else if (event.key === "Tab" && !event.shiftKey
                 && !event.ctrlKey && !event.altKey && !event.metaKey) {
        event.preventDefault();
        insert("    ");
      } else if (event.key === "Escape") {
        /* Sarkain sisentää, joten näppäimistöllä lohkosta pääsee pois näin. */
        code.blur();
      }
    });
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

  /* Tulosteen kuvat (Jypeli): data-URI:t pois tekstistä ja <img>-elementeiksi
   * tulostelaatikon perään; edellisen ajon kuvat pois ensin.
   * -> [loppu teksti, kuvien määrä] */
  const showImages = (box, text) => {
    box.querySelectorAll("img.jyu-result-image").forEach((img) => img.remove());
    let images = 0;
    const rest = text.replace(DATA_URI_RE, (_, uri) => {
      const img = document.createElement("img");
      img.src = uri;
      img.className = "jyu-result-image";
      box.append(img);
      images += 1;
      return "";
    });
    return [rest, images];
  };

  const run = async (anchor, blocks, buttons) => {
    const output = outputFor(anchor);
    const box = output.closest(".jyu-result");
    const set = anchor.classList.contains("tabbed-set") ? anchor : null;
    buttons.forEach((button) => (button.disabled = true));
    box.classList.remove("jyu-result-image-only");
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
          language: executorLanguage(blocks[0]),
          code: set ? JSON.stringify(files(set)) : source(blocks[0]),
          /* multifile vain monitiedostolohkolle: ohj1:n mdBook-skripti ei
           * lähetä kenttää lainkaan, ja palvelimen C#-polku aikakatkaisee
           * pyynnön, jossa on multifile: false (Java sietää sen). */
          ...(set ? { multifile: true } : {}),
        }),
        signal: abort.signal,
      });
      const body = await response.json();
      /* Kuten mdBookissa: virheet ensin, muuten tuloste. Kääntäjän virheet
       * tulevat output-kentässä. Lopun rivinvaihto pois, koska se näkyisi
       * laatikossa tyhjänä rivinä. */
      const [rest, images] = showImages(box, body.errors || body.output || "");
      const text = rest.replace(/\n+$/, "");
      /* Pelkkä kuva (Jypelin ikkuna) on tuloste sekin: tekstilaatikko jää
       * pois, ettei kuvan yllä lue "Ei tulostetta" kuten mdBookissa. */
      const imageOnly = !text && images > 0;
      box.classList.toggle("jyu-result-image-only", imageOnly);
      say(output, text || (imageOnly ? "" : "Ei tulostetta"), !text && !imageOnly);
    } catch (error) {
      say(output, error.name === "AbortError"
        ? `Ohjelma ei vastannut ${TIMEOUT / 1000} sekunnissa.`
        : `Suorituspalvelimeen ei saatu yhteyttä: ${error.message}`);
    } finally {
      clearTimeout(timer);
      buttons.forEach((button) => (button.disabled = false));
    }
  };

  afterTheme(() => {
    for (const [anchor, blocks] of units) {
      const buttons = blocks.map((block) => addButton(block));
      buttons.forEach((button, index) => {
        button.addEventListener("click", () => run(anchor, blocks, buttons));
        if (blocks[index].classList.contains("editable")) {
          makeEditable(blocks[index], button);
        }
      });
    }
  });
})();
