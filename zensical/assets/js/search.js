/* Liittää assets/css/search.css:n hakuikkunan shadow-juureen, johon sivun
 * tyylit eivät ulotu. Tiedosto on jo ladattu sivulle (extra_css), joten
 * selain ei hae sitä uudestaan. bundle.js luo juuren ennen tätä skriptiä;
 * MutationObserver on varalla.
 *
 * Lisäksi hiiren korostus pois nuolinäppäimillä liikuttaessa (data-jyu-keys,
 * sääntö search.css:ssä). Zensical korostaa samalla tavalla sekä valitun että
 * hiiren alla olevan tuloksen ja vierittää valitun keskelle: paikallaan olevan
 * hiiren alla korostus hyppisi vierityksen mukana riviltä toiselle. */

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

  const attach = () => {
    const host = [...document.body.children].find((el) => el.shadowRoot);
    if (!host) return false;
    if (!host.shadowRoot.querySelector('link[href*="assets/css/search.css"]'))
      host.shadowRoot.append(link.cloneNode());
    followKeys(host);
    return true;
  };

  if (attach()) return;
  const observer = new MutationObserver(() => {
    if (attach()) observer.disconnect();
  });
  observer.observe(document.body, { childList: true });
})();
