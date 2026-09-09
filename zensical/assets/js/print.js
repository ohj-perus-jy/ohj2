/* Koko kirja yhdelle sivulle: /tulosta/.
 *
 * mdBookissa tulostussivu (print.html) syntyy käännösaikana: mdBook renderöi
 * jokaisen luvun erikseen ja liittää valmiit HTML-palat peräkkäin. Sama ei
 * onnistu Markdown-tasolla eli convert.py:ssä, koska luvut eivät ole
 * itsenäisiä: kokeiltuna 73 luvun otsikosta 32 katosi, kun luvut liitettiin
 * yhdeksi Markdown-tiedostoksi. Syy on lukujen raaka HTML (<details>,
 * tehtäväkorttien divit) ja koodiaidat: sivun loppuessa jäsennin palautuu alkutilaan, mutta
 * yhdistetyssä tiedostossa kesken jäänyt lohko jatkuu seuraavaan lukuun ja
 * nielaisee sen alun.
 *
 * Siksi liittäminen tehdään samasta paikasta kuin mdBookissa: valmiista
 * HTML:stä. Selain hakee jokaisen luvun oman sivun ja poimii siitä
 * artikkelin, jolloin jokainen luku on jäsennetty erikseen — täsmälleen
 * kuten sitä yksin luettaessa.
 *
 * Sivun rungon (linkkilistan) kirjoittaa convert.py. Ilman JavaScriptiä
 * lista jää näkyviin sellaisenaan, eli sivu on silloin kirjan sisällysluettelo.
 */

(() => {
  "use strict";

  /* Teema vaaleaksi tulostuksen ajaksi.
   *
   * Selaimet jättävät taustavärit oletuksena tulostamatta, joten tummassa
   * teemassa paperille jäisi vaalea teksti valkoiselle pohjalle. Teeman oma
   * vaihdin tekee saman kuin tämä: vaihtaa <body>:n data-md-color-scheme:n,
   * jolloin kaikki värimuuttujat tulevat teemalta eikä niitä tarvitse
   * toistaa tulostustyylitiedostossa.
   *
   * Kuuntelijat ovat kaikilla sivuilla, koska yksittäisen luvun voi tulostaa
   * ilman tätä sivuakin. */
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

  /* Yhden luvun sisältö omalta sivultaan.
   *
   * Osoitteille käy kaksi eri asiaa:
   *
   *  - Suhteelliset kuvat ja linkit ratkaistaan luvun oman sivun suhteen ja
   *    kirjoitetaan absoluuttisina. Tulostussivu on eri hakemistossa kuin
   *    luku, joten muuten ne osoittaisivat väärään paikkaan. Sama pätee
   *    mdBookin print.html:ssä: luvusta toiseen menevä linkki vie luvun
   *    omalle sivulle.
   *  - Sivun sisäiset ankkurit (#otsikko) jäävät sivun sisäisiksi, jotta
   *    kirjaa voi selata tällä sivulla ja jotta PDF:n sisäiset linkit
   *    hyppäävät PDF:n sisällä. Sitä varten jokaisen luvun tunnisteet
   *    saavat eteensä luvun oman etuliitteen: sama otsikko esiintyy
   *    kirjassa monta kertaa (esim. "Tehtävät" joka osassa), ja Materialin
   *    koodirivien ankkurit (__codelineno-0-1) alkavat joka sivulla
   *    alusta. Ilman etuliitettä sivulla olisi 1767 kahteen kertaan
   *    esiintyvää tunnistetta ja linkki veisi ensimmäiseen osumaan.
   */
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

    /* Välilehtien radiopainikkeet tarvitsevat saman etuliitteen, vaikka
     * kumpikaan kahdesta attribuutista ei ole tunniste: label viittaa
     * inputiin for-attribuutilla, ja ryhmä muodostuu name-attribuutista.
     * Ilman tätä labelin for osoittaisi etuliitteen jälkeen olemattomaan
     * id:hen eikä välilehtiä voisi vaihtaa, ja jokaisen luvun __tabbed_1
     * kuuluisi samaan ryhmään, jolloin koko sivulla olisi yksi valinta.
     * Paperille tämä ei näy — Materialin print-säännöt näyttävät kaikki
     * välilehdet joka tapauksessa — mutta ruudulla sivu on myös luettava. */
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

    /* Sivukohtaiset toiminnot pois: muokkauslinkki (overrides/main.html),
     * Materialin omat sisältöpainikkeet ja palauteruutu. Ne ovat artikkelin
     * sisällä, joten ne tulisivat muuten mukaan jokaisen luvun perään. */
    for (const extra of article.querySelectorAll(
      ".md-content__button, .md-source-file, .md-feedback",
    )) {
      extra.remove();
    }

    return article;
  }

  /* Kuvat valmiiksi ennen tulostusikkunaa: selain tulostaa sen mitä ruudulla
   * on sillä hetkellä, ja lataamaton kuva jäisi tyhjäksi laatikoksi.
   * decode() torjuu myös sen, että kuva on ladattu mutta ei vielä purettu.
   * Aikaraja siltä varalta, että jokin kuva ei lataudu lainkaan — silloin
   * tulostetaan ilman sitä eikä jäädä odottamaan loputtomiin. */
  function imagesReady(root, timeout = 20000) {
    const images = [...root.querySelectorAll("img")].map((image) =>
      image.decode().catch(() => {}),
    );
    return Promise.race([
      Promise.all(images),
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

    /* Luvut suoraan artikkelin lapsiksi, ei omiin kääreisiinsä.
     *
     * Materialin oma tyyli osuu sisältöön suorina lapsivalitsimina
     * (.md-typeset > .highlight, > table, ...), joten kääre-elementti jää
     * niiden väliin ja rikkoo ne. Mitattuna 390 px:llä: suorana lapsena
     * koodilohko saa Materialin negatiiviset marginaalit (-16 px) ja
     * levittyy reunasta reunaan 375 px:iin, kääreen sisällä marginaalit
     * katoavat ja lohko kutistuu 343 px:iin 16 px sisennettynä. mdBook
     * tekee saman:
     * print.html:ssä luvut ovat peräkkäin samassa säiliössä ja niiden
     * välissä on pelkkä tyhjä <div>, joka pakottaa sivunvaihdon. */
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

    /* Luvut ovat vasta nyt sivulla, joten niitä käsittelevät skriptit eivät
     * ole nähneet niitä. Piilorivit (assets/js/hidelines.js) kuuntelevat tätä;
     * ilman sitä ne tulostuisivat kirjan mukana. */
    dispatchEvent(new Event("jyu-print-assembled"));

    say(
      failed.length
        ? `Koottu ${links.length - failed.length}/${links.length} lukua. Jäi hakematta: ${failed.join(", ")}`
        : `Koottu ${links.length} lukua.`,
    );

    await imagesReady(document);
    print();
  }

  assemble();
})();
