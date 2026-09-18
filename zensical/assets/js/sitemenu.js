/* Sivustovalikko yläpalkissa: nuolipainike avaa ja sulkee linkkilistan.
 * Merkkaus: overrides/partials/header.html, ulkoasu: assets/css/sitemenu.css.
 *
 * Kohdat ovat tavallisia linkkejä, joten valintaa ei käsitellä täällä.
 * Näppäimistö kuten kirjasinvalikossa: nuolet liikkuvat, Esc sulkee. */

(() => {
  "use strict";

  const root = document.querySelector("[data-md-component=jyu-sites]");
  if (!root) return;

  const button = root.querySelector(".jyu-sites__button");
  const list = root.querySelector(".jyu-sites__list");
  if (!button || !list) return;

  const links = [...list.querySelectorAll("a")];

  const open = () => {
    list.hidden = false;
    button.setAttribute("aria-expanded", "true");
  };

  const close = (refocus) => {
    if (list.hidden) return;
    list.hidden = true;
    button.setAttribute("aria-expanded", "false");
    if (refocus) button.focus();
  };

  button.addEventListener("click", () => (list.hidden ? open() : close(false)));

  root.addEventListener("keydown", (event) => {
    /* Nimilinkin nuolet vierittävät sivua kuten ennenkin. */
    if (event.target !== button && !list.contains(event.target)) return;
    const index = links.indexOf(document.activeElement);
    const move = (to) => {
      event.preventDefault();
      open();
      links[(to + links.length) % links.length].focus();
    };
    switch (event.key) {
      case "ArrowDown": move(index + 1); break;
      case "ArrowUp": move(index < 0 ? -1 : index - 1); break;
      case "Home": if (index >= 0) move(0); break;
      case "End": if (index >= 0) move(-1); break;
      case "Escape":
        if (!list.hidden) {
          event.preventDefault();
          close(true);
        }
        break;
    }
  });

  /* Sulje, kun kohdistus tai painallus siirtyy muualle. */
  root.addEventListener("focusout", (event) => {
    if (event.relatedTarget && !root.contains(event.relatedTarget)) close(false);
  });

  document.addEventListener("pointerdown", (event) => {
    if (!button.contains(event.target) && !list.contains(event.target)) close(false);
  });
})();
