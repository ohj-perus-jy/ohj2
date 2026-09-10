/* Terminaalinauhoitukset (README.md kohta 16).
 *
 * Kirjan 13 nauhoitusta ovat lähteessä raakana HTML:nä:
 * <asciinema src="images/rec_java.cast" rows="3" poster="npt:5"></asciinema>.
 * Tagi menee Markdownin läpi sellaisenaan ja Zensical kirjoittaa suhteellisen
 * polun sivun uuteen sijaintiin, joten convert.py:ssä ei ole tälle kohdalle
 * mitään: puuttui soitin, ei merkkaus. Ilman soitinta tagi on selaimelle
 * tuntematon elementti, joka ei näy sivulla mitenkään.
 *
 * Soitin on sama kuin kirjassa (assets/js/asciinema-player.min.js ja
 * assets/css/asciinema-player.css, kopiot theme/:stä), ja create() antaa sille
 * samat asetukset kuin theme/asciinema-component.js mdBookissa.
 *
 * Ero kirjaan on latauksessa. mdBook lataa soittimen joka sivulle
 * (book.toml: additional-js ja additional-css), mutta se on 162 kt skriptiä ja
 * 45 kt tyyliä: skripti enemmän kuin Zensicalin oma bundle.js (167 kt), tyyli
 * kolmannes teeman omasta. Nauhoituksia on kolmella sivulla 190:stä, joten
 * soitin haetaan vasta kun sivulla on jotain soitettavaa. Siksi mkdocs.yml:ssä
 * on vain tämä tiedosto: soitin on docs/assets/:ssa mutta ei millään sivulla
 * ennen kuin tämä lisää sen.
 *
 * Osoitteet luetaan tämän tiedoston omasta osoitteesta eikä sivuston juuresta,
 * koska teema kirjoittaa assettien polut suhteellisina (../../assets/js/) ja
 * sivusto voi olla palvelimella alihakemistossa.
 */

(() => {
  "use strict";

  const HERE = document.currentScript.src;
  const PLAYER_JS = new URL("asciinema-player.min.js", HERE);
  const PLAYER_CSS = new URL("../css/asciinema-player.css", HERE);

  /* Haku kerran per sivu, vaikka kutsuja olisi kaksi (tulostussivu). */
  let loading = null;

  const load = () => (loading ??= new Promise((resolve, reject) => {
    const style = document.createElement("link");
    style.rel = "stylesheet";
    style.href = PLAYER_CSS;
    document.head.append(style);

    const script = document.createElement("script");
    script.src = PLAYER_JS;
    script.addEventListener("load", resolve);
    script.addEventListener("error", () =>
      reject(new Error(`asciinema-soitinta ei saatu haettua: ${PLAYER_JS}`)));
    document.head.append(script);
  }));

  const create = (element) => {
    /* Attribuutit ovat kirjan omat: rows on nauhoituksen korkeus riveinä,
     * poster ruutu, joka näkyy ennen toistoa ("npt:5" = kohta 5 s), ja
     * controls kertoo, näkyykö toistopalkki. Kaksi viimeistä eivät tule
     * tagista vaan ovat samat kaikille, ja kummatkin ovat kirjan omat
     * (theme/asciinema-component.js): kirjasin on 12 px, ja fit: false jättää
     * terminaalin skaalaamatta elementin leveyteen. */
    return AsciinemaPlayer.create(element.getAttribute("src"), element, {
      rows: +element.getAttribute("rows") || 24,
      poster: element.getAttribute("poster") || undefined,
      controls: element.hasAttribute("controls"),
      terminalFontSize: "12px",
      fit: false,
    });
  };

  /* Ensimmäinen ruutu sivulle piirrettynä.
   *
   * Soitin piirtää terminaalin omassa requestAnimationFrame-kutsussaan, joten
   * ruutu ei ole valmis silloinkaan, kun nauhoitus on haettu: mitattuna
   * getDuration():n ratketessa terminaalirivejä on 0. Yksi oma
   * ruudunpäivityksen odotus ei auta, koska soitin ajastaa omansa vasta
   * hakunsa jälkeen — kumpi on ensin, on kiinni ajoituksesta (mitattuna 13
   * nauhoituksesta piirtyi 0). Siksi odotetaan piirtynyttä riviä eikä
   * ruudunpäivitystä. */
  const drawn = (element) => new Promise((resolve) => {
    if (element.querySelector(".ap-line")) return resolve();

    const observer = new MutationObserver(() => {
      if (!element.querySelector(".ap-line")) return;
      observer.disconnect();
      resolve();
    });
    observer.observe(element, { childList: true, subtree: true });
  });

  /* Merkintä data-ready kertoo, mitkä on jo soitettu: tulostussivu kutsuu
   * tätä toiseen kertaan, ja soitin lisäisi silloin toisen soittimen samaan
   * elementtiin.
   *
   * Palautettu lupaus ratkeaa vasta, kun jokainen soitin on hakenut
   * nauhoituksensa ja piirtänyt siitä ensimmäisen ruudun; sitä odottaa
   * tulostussivu, ks. alla. Hakemista odotetaan soittimen omalla
   * rajapinnalla (getDuration() on kääre sen sisäisen init()-lupauksen
   * ympärillä), koska se myös hylkää lupauksen, jos nauhoitusta ei ole:
   * puuttuva tiedosto huomataan siitä heti eikä vasta tulostuksen
   * aikarajasta. */
  const play = async (root) => {
    const elements = [...root.querySelectorAll("asciinema[src]:not([data-ready])")];
    if (!elements.length) return;

    await load();
    await Promise.all(elements.map(async (element) => {
      element.dataset.ready = "";
      const player = create(element);
      await player.getDuration();
      await drawn(element);
    }));
  };

  play(document);

  /* Tulostussivun luvut haetaan vasta sivun latauduttua (print.js), joten ne
   * eivät olleet olemassa yllä. Sama kytkentä kuin piiloriveillä ja
   * korostuksilla; mdBookissa print.html on tavallinen sivu, jolla soitin
   * ajetaan muiden tapaan.
   *
   * Yksi ero niihin: soitin on haettava verkosta, joten työ ei ole valmis
   * kuuntelijan palatessa. Siksi lupaus jätetään tapahtuman listaan, jota
   * print.js odottaa ennen tulostusikkunaa — ilman sitä mitattuna 13
   * nauhoituksesta oli tulostushetkellä piirrettynä 0. */
  addEventListener("jyu-print-assembled", (event) => {
    const done = play(document);
    event.detail?.pending?.push(done);
  });
})();
