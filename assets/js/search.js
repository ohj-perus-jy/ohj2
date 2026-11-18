/* Liittää assets/css/search.css:n hakuikkunan shadow-juureen, johon sivun
 * tyylit eivät ulotu. Tiedosto on jo ladattu sivulle (extra_css), joten
 * selain ei hae sitä uudestaan. bundle.js luo juuren ennen tätä skriptiä;
 * MutationObserver on varalla.
 *
 * Lisäksi hiiren korostus pois nuolinäppäimillä liikuttaessa (data-jyu-keys,
 * sääntö search.css:ssä). Zensical korostaa samalla tavalla sekä valitun että
 * hiiren alla olevan tuloksen ja vierittää valitun keskelle: paikallaan olevan
 * hiiren alla korostus hyppisi vierityksen mukana riviltä toiselle.
 *
 * Myös hakukentän paikkamerkki suomeksi: bundle.js:ssä se on kiinteästi
 * "Search" eikä tule teeman käännöksistä (language: fi).
 *
 * Ja sulkunappi (×) kenttärivin oikeaan päähän: puhelimella ikkuna täyttää
 * ruudun kapeaa reunusta vaille (search.css), eikä Escape-näppäintä tai
 * kunnollista napautettavaa taustaa ole. Zensicalin
 * oma sulkija on rivin ensimmäinen nappi ("Close search"), mutta sen kuvake
 * on suurennuslasi, josta sulkemista ei arvaa. Luokkanimet ovat Zensicalin
 * minifioimia, ks. search.css. */

(() => {
  "use strict";

  const link = document.querySelector(
    'link[rel="stylesheet"][href*="assets/css/search.css"]');
  if (!link || !document.querySelector(".md-search")) return;

  /* Attribuutti isännässä eikä ikkunan elementeissä, jotka Zensical piirtää
   * uudelleen. Vieritys hiiren alla tuottaa selaimessa keinotekoisia
   * hiiritapahtumia, joten hiiri on liikkunut vasta kun sen paikka muuttuu;
   * paikkaa seurataan koko sivulla, jotta se tiedetään jo ikkunan auetessa. */
  const followKeys = (host) => {
    let x, y;
    host.shadowRoot.addEventListener("keydown", (event) => {
      if (event.key === "ArrowDown" || event.key === "ArrowUp")
        host.setAttribute("data-jyu-keys", "");
    });
    document.addEventListener("pointermove", (event) => {
      if (event.screenX !== x || event.screenY !== y)
        host.removeAttribute("data-jyu-keys");
      x = event.screenX;
      y = event.screenY;
    }, true);
  };

  /* Lucide-kuvake "x", kuten Zensicalin omat kuvakkeet (bundle.js: cp). */
  const CLOSE_ICON =
    '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"' +
    ' viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"' +
    ' stroke-linecap="round" stroke-linejoin="round">' +
    '<path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';

  /* Nappi Zensicalin nappien luokkaa (.a, search.css), jotta se näyttää
   * samalta. Sulkeminen klikkaa yläpalkin hakunappia, jonka klikkausta
   * Zensical kuuntelee ja joka avaa ja sulkee ikkunan vuorotellen: ikkunan
   * omaan koodiin ei tarvitse koskea. Kohdistus pois napista, koska suljettu
   * ikkuna on vain läpinäkyvä (opacity) ja nappi jäisi muuten kohdistetuksi
   * näkymättömiin. Lisäys kenttäriville ei häiritse Zensicalia: se piirtää
   * vain omat elementtinsä uudelleen eikä poista vieraita. */
  const addCloseButton = (controls) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "a jyu-close";
    button.setAttribute("aria-label", "Sulje haku");
    button.innerHTML = CLOSE_ICON;
    button.addEventListener("click", () => {
      button.blur();
      document.querySelector(".md-search__button").click();
    });
    controls.append(button);
  };

  /* Kenttä ja kenttärivi ovat olemassa ennen ikkunan avaamista ja säilyvät
   * sulkemisen yli, eikä Zensical kirjoita muuttumatonta paikkamerkkiä
   * uudelleen, joten kerta riittää; MutationObserver on varalla, jos ikkunaa
   * ei vielä ole piirretty (se piirretään vasta hakemiston latauduttua). */
  const prepare = (root) => {
    const ready = () => {
      const input = root.querySelector('input[placeholder="Search"]');
      if (!input) return false;
      input.placeholder = "Hae";
      addCloseButton(input.closest(".w"));
      return true;
    };
    if (ready()) return;
    const observer = new MutationObserver(() => {
      if (ready()) observer.disconnect();
    });
    observer.observe(root, { childList: true, subtree: true });
  };

  const attach = () => {
    const host = [...document.body.children].find((el) => el.shadowRoot);
    if (!host) return false;
    if (!host.shadowRoot.querySelector('link[href*="assets/css/search.css"]'))
      host.shadowRoot.append(link.cloneNode());
    followKeys(host);
    prepare(host.shadowRoot);
    return true;
  };

  if (attach()) return;
  const observer = new MutationObserver(() => {
    if (attach()) observer.disconnect();
  });
  observer.observe(document.body, { childList: true });
})();
