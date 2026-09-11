/* Koko kirja yhdelle sivulle (/tulosta/), kuten mdBookin print.html.
 *
 * Luvut liitetään valmiista HTML:stä, ei Markdownista: luvuissa on raakaa
 * HTML:ää ja koodiaitoja, ja yhteen Markdown-tiedostoon liitettynä kesken
 * jäänyt lohko nielaisisi seuraavan luvun alun. Selain hakee siis jokaisen
 * luvun oman sivun ja poimii siitä artikkelin.
 *
 * Sivun rungon (linkkilistan) kirjoittaa convert.py; ilman JavaScriptiä
 * sivu on kirjan sisällysluettelo. */

(() => {
  "use strict";

  /* Teema vaaleaksi tulostuksen ajaksi: selaimet eivät tulosta taustavärejä,
   * joten tumma teema antaisi vaalean tekstin valkoiselle. Vaihdetaan bodyn
   * data-md-color-scheme kuten teeman oma vaihdin, jolloin värit tulevat
   * teemalta. Kaikilla sivuilla, koska yksittäisenkin luvun voi tulostaa. */
  let schemeBeforePrint = null;

  addEventListener("beforeprint", () => {
    const scheme = document.body.getAttribute("data-md-color-scheme");
    if (scheme && scheme !== "default") {
      schemeBeforePrint = scheme;
      document.body.setAttribute("data-md-color-scheme", "default");
    }
  });

  addEventListener("afterprint", () => {
    if (schemeBeforePrint) {
      document.body.setAttribute("data-md-color-scheme", schemeBeforePrint);
      schemeBeforePrint = null;
    }
  });

  const book = document.getElementById("jyu-print");
  if (!book) return;

  const status = document.getElementById("jyu-print-status");
  const links = [...book.querySelectorAll("a[href]")];

  const say = (text) => {
    if (status) status.textContent = text;
  };

  /* Yhden luvun artikkeli omalta sivultaan. Suhteelliset osoitteet
   * kirjoitetaan absoluuttisina, koska tulostussivu on eri hakemistossa kuin
   * luku. Sivun sisäiset ankkurit jäävät sivun sisäisiksi, ja luvun tunnisteet
   * saavat luvun etuliitteen, koska sama tunniste ("Tehtävät", Materialin
   * __codelineno-0-1) toistuu monessa luvussa. */
  async function fetchChapter(url) {
    const response = await fetch(url, { credentials: "same-origin" });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);

    const parsed = new DOMParser().parseFromString(await response.text(), "text/html");
    const article = parsed.querySelector(".md-content__inner");
    if (!article) throw new Error("sivulta ei löytynyt artikkelia");

    const prefix = new URL(url).pathname.replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, "");
    for (const element of article.querySelectorAll("[id]")) {
      element.id = `${prefix}--${element.id}`;
    }

    /* Välilehtien label[for] ja input[name] tarvitsevat saman etuliitteen,
     * vaikka eivät ole tunnisteita: muuten for osoittaisi olemattomaan id:hen
     * ja kaikkien lukujen __tabbed_1 kuuluisi samaan radioryhmään. */
    for (const label of article.querySelectorAll("label[for]")) {
      label.htmlFor = `${prefix}--${label.htmlFor}`;
    }

    for (const input of article.querySelectorAll("input[name]")) {
      input.name = `${prefix}--${input.name}`;
    }

    for (const element of article.querySelectorAll("[href], [src]")) {
      for (const name of ["href", "src"]) {
        const value = element.getAttribute(name);
        if (value === null || /^[a-z][a-z0-9+.-]*:/i.test(value) || value.startsWith("//")) {
          continue;
        }
        element.setAttribute(
          name,
          value.startsWith("#")
            ? `#${prefix}--${value.slice(1)}`
            : new URL(value, url).href,
        );
      }
    }

    /* Sivukohtaiset toiminnot (muokkauslinkki, Materialin sisältöpainikkeet,
     * palauteruutu) pois: ne ovat artikkelin sisällä ja toistuisivat joka
     * luvun perässä. */
    for (const extra of article.querySelectorAll(
      ".md-content__button, .md-source-file, .md-feedback",
    )) {
      extra.remove();
    }

    return article;
  }

  /* Odotetaan ennen tulostusikkunaa, että kuvat on purettu ja kuuntelijoiden
   * jälkityö (pending, esim. asciinema.js:n soitin) on valmis. Aikaraja ja
   * nielaistut virheet: yksi puuttuva tiedosto ei saa estää tulostusta. */
  function contentReady(root, pending, timeout = 20000) {
    const images = [...root.querySelectorAll("img")].map((image) =>
      image.decode().catch(() => {}),
    );
    return Promise.race([
      Promise.all([...images, ...pending.map((task) => task.catch(() => {}))]),
      new Promise((resolve) => setTimeout(resolve, timeout)),
    ]);
  }

  async function assemble() {
    say(`Kootaan kirjaa: 0/${links.length} lukua`);

    let done = 0;
    const failed = [];
    const chapters = await Promise.all(
      links.map(async (link) => {
        try {
          return await fetchChapter(link.href);
        } catch (error) {
          failed.push(`${link.textContent} (${error.message})`);
          return null;
        } finally {
          say(`Kootaan kirjaa: ${++done}/${links.length} lukua`);
        }
      }),
    );

    /* Luvut suoraan artikkelin lapsiksi, ei kääreisiin: Materialin tyylit
     * osuvat suorina lapsivalitsimina (.md-typeset > .highlight), ja kääre
     * rikkoisi ne. Välissä pelkkä sivunvaihto-div kuten mdBookissa. */
    const assembled = document.createDocumentFragment();
    for (const chapter of chapters.filter(Boolean)) {
      if (assembled.childElementCount) {
        const separator = document.createElement("div");
        separator.className = "jyu-print-break";
        assembled.append(separator);
      }
      assembled.append(...chapter.childNodes);
    }
    book.replaceWith(assembled);

    /* Luvut ovat vasta nyt sivulla; niitä käsittelevät skriptit (hidelines.js,
     * highlights.js, asciinema.js) kuuntelevat tätä. Kuuntelija, jonka työ
     * jatkuu vielä, työntää lupauksensa pending-listaan (ks. contentReady). */
    const pending = [];
    dispatchEvent(new CustomEvent("jyu-print-assembled", { detail: { pending } }));

    say(
      failed.length
        ? `Koottu ${links.length - failed.length}/${links.length} lukua. Jäi hakematta: ${failed.join(", ")}`
        : `Koottu ${links.length} lukua.`,
    );

    await contentReady(document, pending);
    print();
  }

  assemble();
})();
