/* Terminaalinauhoitusten soitin. Lähteen <asciinema src=... rows=... poster=...>
 * menee Markdownin läpi sellaisenaan; ilman soitinta tagi ei näy mitenkään.
 * Soitin on kirjan oma (assets/js/asciinema-player.min.js ja
 * assets/css/asciinema-player.css: asciinema-player 3.17.0, Apache 2.0,
 * assets/LICENSE-asciinema-player.txt) ja asetukset samat kuin mdBookin
 * theme/asciinema-component.js:ssä.
 *
 * Toisin kuin mdBookissa, soitin ja sen tyyli haetaan vasta sivulla, jolla on
 * nauhoitus, koska ne ovat isompia kuin teeman oma skripti. Osoitteet luetaan
 * tämän tiedoston osoitteesta, koska teema kirjoittaa assettipolut suhteellisina. */

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
    /* rows, poster ja controls tulevat tagista (kirjan omat attribuutit);
     * fit: false on sama kuin theme/asciinema-component.js:ssä. Kirjasinkoko
     * on layout.css:ssä eikä terminalFontSize-asetuksena, koska asetus
     * kirjoittaisi kiinteän koon tyyliattribuuttiin CSS:n ohi. */
    return AsciinemaPlayer.create(element.getAttribute("src"), element, {
      rows: +element.getAttribute("rows") || 24,
      poster: element.getAttribute("poster") || undefined,
      controls: element.hasAttribute("controls"),
      fit: false,
    });
  };

  /* Soitin piirtää rivit tyhjinä heti ja posterin vasta nauhoituksen haun
   * jälkeen, eikä haun valmistumisesta tule tapahtumaa (getDuration() ei
   * odota). Siksi odotetaan riviä, jossa on tekstiä. Haun virhe tulee
   * error-tapahtumana. Ilman posteria soitin hakee nauhoituksen vasta
   * toistettaessa, joten odotettavaa ei ole. */
  const drawn = (element, player) => new Promise((resolve, reject) => {
    const posterDrawn = () => [...element.querySelectorAll(".ap-line")]
      .some((line) => line.textContent.trim());
    if (!element.hasAttribute("poster") || posterDrawn()) return resolve();

    const observer = new MutationObserver(() => {
      if (!posterDrawn()) return;
      observer.disconnect();
      resolve();
    });
    observer.observe(element, { childList: true, subtree: true, characterData: true });
    player.addEventListener("error", ({ message }) => {
      observer.disconnect();
      reject(new Error(`asciinema-nauhoitusta ei saatu: ${element.getAttribute("src")}: ${message}`));
    });
  });

  /* data-ready estää toisen soittimen samaan elementtiin, kun tulostussivu
   * kutsuu uudestaan. Lupaus ratkeaa, kun jokainen soitin on hakenut
   * nauhoituksensa ja piirtänyt posterin, ja hylätään, jos tiedosto puuttuu. */
  const play = async (root) => {
    const elements = [...root.querySelectorAll("asciinema[src]:not([data-ready])")];
    if (!elements.length) return;

    await load();
    await Promise.all(elements.map((element) => {
      element.dataset.ready = "";
      return drawn(element, create(element));
    }));
  };

  play(document);

  /* Tulostussivun luvut tulevat sivulle vasta myöhemmin (print.js). Soitin
   * haetaan verkosta, joten lupaus jätetään tapahtuman listaan, jota print.js
   * odottaa ennen tulostusikkunaa. */
  addEventListener("jyu-print-assembled", (event) => {
    const done = play(document);
    event.detail?.pending?.push(done);
  });
})();
