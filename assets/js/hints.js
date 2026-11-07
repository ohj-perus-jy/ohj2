/* Opastusnuolet koodilohkon nappeihin. Aidan määre (luokkana lohkon divissä,
 * convert.py: fence_info) nimeää napin: copyhint, runhint, eyehint. Napin
 * alle tulee keinuva nuoli (hints.css), joka poistuu napin ensimmäisellä
 * painalluksella. Painallus jää localStorageen ("jyu-hints"), eikä sen
 * tyypin nuolta näytetä enää millään sivulla. Vain nuolellisen napin
 * painallus muistetaan. Ilman localStoragea nuoli palaa seuraavalla sivulla.
 *
 * Nuoli on napin oma lapsi, joten se seuraa nappia, olipa rivissä mitä
 * nappeja tahansa; jos määreen nappia ei ole, nuolta ei tule. Nuoli on SVG
 * eikä maski, koska maski leikkaisi heittovarjon pois.
 *
 * Napit tekevät teema, playground.js ja hidelines.js DOMContentLoadedissa,
 * joten tämä on skripteistä viimeisenä (mkdocs-pohja.yml). */

(() => {
  "use strict";

  /* Määre -> napin data-md-type (teema, playground.js, hidelines.js). */
  const HINTS = { copyhint: "copy", runhint: "run", eyehint: "hidelines" };

  const KEY = "jyu-hints";

  /* localStorage voi puuttua (yksityinen tila); silloin nuoli poistuu vain
   * tältä sivulta. */
  const pressed = () => {
    try {
      const types = JSON.parse(localStorage.getItem(KEY));
      return new Set(Array.isArray(types) ? types : []);
    } catch {
      return new Set();
    }
  };
  const remember = (type) => {
    try {
      localStorage.setItem(KEY, JSON.stringify([...pressed().add(type)]));
    } catch {
      /* ei tallennusta */
    }
  };

  const ARROW = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 28">'
    + '<path d="M12 25V5M4.5 12.5 12 5l7.5 7.5" fill="none" stroke="currentColor"'
    + ' stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  const addHint = (button) => {
    const hint = document.createElement("span");
    hint.className = "jyu-hint";
    hint.setAttribute("aria-hidden", "true");
    hint.innerHTML = ARROW;
    button.append(hint);
  };

  /* Saman tyypin kaikki nuolet pois kerralla: sivulla voi olla useampi
   * opastettu lohko. */
  const removeHints = (type) => {
    for (const hint of document.querySelectorAll(
      `[data-md-type=${type}] > .jyu-hint`)) {
      hint.remove();
    }
  };

  const start = () => {
    const done = pressed();
    for (const [attribute, type] of Object.entries(HINTS)) {
      if (done.has(type)) continue;
      for (const block of document.querySelectorAll(`div.highlight.${attribute}`)) {
        const button = block.querySelector(
          `:scope > pre > nav.md-code__nav > [data-md-type=${type}]`);
        if (button) addHint(button);
      }
    }
    /* Kuuntelija dokumentissa, ei napeissa: nuolet voivat olla useassa
     * lohkossa. Vain nappi, jossa nuoli on, muistetaan ja poistaa saman
     * tyypin nuolet. */
    document.addEventListener("click", (event) => {
      const button = event.target.closest?.("nav.md-code__nav > [data-md-type]");
      if (!button?.querySelector(":scope > .jyu-hint")) return;
      const type = button.dataset.mdType;
      remember(type);
      removeHints(type);
    });
  };

  if (document.readyState === "loading") {
    addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
