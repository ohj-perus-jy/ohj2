/* Päävalikon piilotus työpöydällä: yläpalkin painike kytkee kiskon päälle ja
 * pois. Merkkaus: overrides/partials/header.html, ulkoasu: assets/css/layout.css.
 *
 * Tila on html-elementin attribuutti (data-jyu-rail="hidden"), josta
 * layout.css nollaa kiskon leveyden ja piilottaa kiskon. Valinta tallentuu
 * selaimeen (localStorage jyu-rail), ja header.html:n skripti asettaa
 * attribuutin ennen sisältöä, joten seuraava sivu aukeaa oikeassa tilassa
 * ilman välähdystä; tässä vain painikkeen teksti ja tila sovitetaan siihen.
 *
 * Kapealla näytöllä painike on piilossa ja valikko on teeman laatikko, mutta
 * attribuutti saa olla: layout.css lukee sen vain kiskon leveyksillä. */

(() => {
  "use strict";

  const button = document.getElementById("jyu-rail-button");
  const rail = document.querySelector(".md-sidebar--primary");
  if (!button || !rail) return;

  const KEY = "jyu-rail";
  const root = document.documentElement;
  /* Sama raja kuin kiskolla (layout.css). */
  const desktop = matchMedia("(min-width: 73.75em)");

  /* aria-controls osoittaa kiskoon; teema ei anna sille id:tä. */
  rail.id = button.getAttribute("aria-controls");

  const isHidden = () => root.getAttribute("data-jyu-rail") === "hidden";

  /* Vihjeen teksti kertoo, mitä painallus tekee. Title siirtyy teeman
   * vihjeeseen (tooltips.js), myös vihjeen ollessa auki. */
  const describe = () => {
    const text = isHidden() ? "Näytä valikko" : "Piilota valikko";
    button.title = text;
    button.setAttribute("aria-label", text);
    button.setAttribute("aria-expanded", String(!isHidden()));
  };

  /* Teema vierittää avoimen luvun näkyviin vain sivun latautuessa, eikä
   * piilotetulla (display: none) kiskolla ole mittoja, joten piilotettuna
   * avatun sivun kisko olisi palatessaan listan alussa. Luku keskelle, kuten
   * teema tekee latautuessa. Sivu ei vieri: kisko on kiinteä. */
  const reveal = () => {
    const wrap = rail.querySelector(".md-sidebar__scrollwrap");
    const active = wrap?.querySelector(".md-nav__link--active");
    if (!active) return;
    const area = wrap.getBoundingClientRect();
    const box = active.getBoundingClientRect();
    if (box.top >= area.top && box.bottom <= area.bottom) return;
    wrap.scrollTop += box.top - area.top - (area.height - box.height) / 2;
  };

  /* Luettu kohta pysyy paikallaan. Kiskon mukana tekstipalsta levenee tai
   * kapenee, jolloin kohdan yläpuolinen sisältö rivittyy eri korkuiseksi,
   * mutta vieritys (scrollY) ei muutu, ja kohta karkaisi ruudulta. Selaimen
   * oma ankkurointi ei auta: Chrome keskeyttää sen, kun isännän täyte
   * muuttuu, eikä Safari tee sitä lainkaan. Ankkuri on tekstipalstan
   * ensimmäinen ruudulla alkava lohko (kappale, otsikko, koodilohko): sen
   * yläreuna pidetään samassa kohdassa ruutua liu'un ajan (layout.css:
   * 0,25 s), jonka aikana palsta levenee joka kehyksellä. Lohko, joka
   * alkaa ruudun yläpuolelta, ei kelpaa, koska sen omat rivit rivittyvät;
   * jos muuta ei ole (yksi pitkä lohko), sen yläreuna on silti parempi
   * kuin ei mitään. Rivinsisäisestä osumasta (linkki, koodi) noustaan
   * lohkoon, jonka rivit rivittyvät. */
  const anchor = () => {
    const content = document.querySelector(".md-content__inner");
    if (!content || !scrollY) return null;
    const column = content.getBoundingClientRect();
    const x = column.left + column.width / 2;
    const header = document.querySelector(".md-header")?.getBoundingClientRect().bottom ?? 0;
    let fallback = null;
    for (let y = header + 1; y < innerHeight; y += 8) {
      let element = document.elementFromPoint(x, y);
      if (!element || element === content || !content.contains(element)) continue;
      while (element.parentElement !== content
             && getComputedStyle(element).display.startsWith("inline")) {
        element = element.parentElement;
      }
      const box = element.getBoundingClientRect();
      if (box.top >= header) return { element, top: box.top };
      fallback ??= { element, top: box.top };
      y = Math.max(y, box.bottom);
    }
    return fallback;
  };

  const hold = (anchored) => {
    if (!anchored) return;
    const until = performance.now() + 400;
    const step = () => {
      const top = anchored.element.getBoundingClientRect().top;
      if (Math.abs(top - anchored.top) >= 0.5) {
        scrollTo({ top: scrollY + top - anchored.top, behavior: "instant" });
      }
      if (performance.now() < until) requestAnimationFrame(step);
    };
    step();
  };

  const toggle = () => {
    const anchored = anchor();
    if (isHidden()) root.removeAttribute("data-jyu-rail");
    else root.setAttribute("data-jyu-rail", "hidden");
    hold(anchored);
    describe();
    if (!isHidden()) reveal();
    try {
      if (isHidden()) localStorage.setItem(KEY, "hidden");
      else localStorage.removeItem(KEY);
    } catch {
      /* ei tallennusta */
    }
  };

  describe();

  /* Hiirellä painettu painike menettää kohdistuksen, jottei vihje jää auki
   * osoittimen lähdettyä (tooltips.js tekee saman muille napeille, mutta
   * jättää aria-expanded-napit itselleen). Näppäimistöllä (detail 0)
   * kohdistus jää, jotta kytkentä edestakaisin onnistuu. */
  button.addEventListener("click", (event) => {
    toggle();
    if (event.detail) button.blur();
  });

  /* b kytkee kiskon kuten teeman s avaa haun: vain työpöydällä, ilman
   * muunnosnäppäimiä ja vain kun ei kirjoiteta. Hakukenttä on shadow
   * DOM:issa, jossa event.target on isäntä: composedPath kertoo kentän. */
  document.addEventListener("keydown", (event) => {
    if (event.key !== "b" || event.repeat || !desktop.matches) return;
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const target = event.composedPath()[0];
    if (target instanceof Element
        && target.closest("input, textarea, select, [contenteditable]")) return;
    event.preventDefault();
    toggle();
  });
})();
