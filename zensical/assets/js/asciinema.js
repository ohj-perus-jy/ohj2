/* Terminaalinauhoitusten soitin. Lähteen <asciinema src=... rows=... poster=...>
 * menee Markdownin läpi sellaisenaan; ilman soitinta tagi ei näy mitenkään.
 * Soitin on kirjan oma (assets/js/asciinema-player.min.js ja
 * assets/css/asciinema-player.css) ja asetukset samat kuin mdBookin
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
     * kirjasinkoko ja fit: false ovat samat kuin theme/asciinema-component.js:ssä. */
    return AsciinemaPlayer.create(element.getAttribute("src"), element, {
      rows: +element.getAttribute("rows") || 24,
      poster: element.getAttribute("poster") || undefined,
      controls: element.hasAttribute("controls"),
      terminalFontSize: "12px",
      fit: false,
    });
  };

  /* Soitin piirtää terminaalin omassa requestAnimationFrame-kutsussaan vasta
   * hakunsa jälkeen, joten ruutu ei ole valmis getDuration():n ratketessa.
   * Siksi odotetaan piirtynyttä riviä, ei ruudunpäivitystä. */
  const drawn = (element) => new Promise((resolve) => {
    if (element.querySelector(".ap-line")) return resolve();

    const observer = new MutationObserver(() => {
      if (!element.querySelector(".ap-line")) return;
      observer.disconnect();
      resolve();
    });
    observer.observe(element, { childList: true, subtree: true });
  });

  /* data-ready estää toisen soittimen samaan elementtiin, kun tulostussivu
   * kutsuu uudestaan. Lupaus ratkeaa, kun jokainen soitin on hakenut
   * nauhoituksensa (getDuration() hylkää, jos tiedosto puuttuu) ja piirtänyt
   * ensimmäisen ruudun. */
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

  /* Tulostussivun luvut tulevat sivulle vasta myöhemmin (print.js). Soitin
   * haetaan verkosta, joten lupaus jätetään tapahtuman listaan, jota print.js
   * odottaa ennen tulostusikkunaa. */
  addEventListener("jyu-print-assembled", (event) => {
    const done = play(document);
    event.detail?.pending?.push(done);
  });
})();
