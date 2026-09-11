/* Leipätekstin kirjasimen alasvetovalikko yläpalkissa. Avaa ja sulkee listan,
 * kirjoittaa valinnan bodyn data-jyu-font-attribuuttiin ja localStorageen
 * ("jyu-font"). Tallennetun arvon lukee sivun alussa header.html:n
 * inline-skripti, jotta teksti ei välähdä oletuskirjasimella.
 *
 * Oletus (data-font="") ei tallennu vaan poistaa tallennuksen. Lista on
 * role="listbox" kuten <select>: nuolet liikkuvat, Enter valitsee, Esc sulkee.
 * Painikkeessa on vain kuvake, joten valinta kerrotaan sen title- ja
 * aria-label-attribuuteissa (kohdan data-short). */

(() => {
  "use strict";

  const KEY = "jyu-font";

  const root = document.querySelector("[data-md-component=jyu-font]");
  if (!root) return;

  const button = root.querySelector(".jyu-font__button");
  const list = root.querySelector(".jyu-font__list");
  const items = [...root.querySelectorAll(".jyu-font__item")];
  if (!button || !list || !items.length) return;

  /* localStorage voi puuttua (yksityinen tila); silloin valinta koskee vain tätä sivua. */
  const stored = () => {
    try {
      return localStorage.getItem(KEY) || "";
    } catch {
      return "";
    }
  };
  const store = (id) => {
    try {
      if (id) localStorage.setItem(KEY, id);
      else localStorage.removeItem(KEY);
    } catch {
      /* ei tallennusta */
    }
  };

  const apply = (id) => {
    const item = items.find((candidate) => candidate.dataset.font === id) || items[0];
    const chosen = item.dataset.font;
    if (chosen) document.body.setAttribute("data-jyu-font", chosen);
    else document.body.removeAttribute("data-jyu-font");
    for (const candidate of items) {
      candidate.setAttribute("aria-selected", String(candidate === item));
    }
    const name = "Leipätekstin kirjasin: " + (item.dataset.short || item.querySelector(".jyu-font__name").textContent);
    button.title = name;
    button.setAttribute("aria-label", name);
  };

  const selected = () => items.find((item) => item.getAttribute("aria-selected") === "true") || items[0];

  const open = () => {
    list.hidden = false;
    button.setAttribute("aria-expanded", "true");
    selected().focus();
  };

  const close = (refocus) => {
    if (list.hidden) return;
    list.hidden = true;
    button.setAttribute("aria-expanded", "false");
    if (refocus) button.focus();
  };

  const choose = (item) => {
    store(item.dataset.font);
    apply(item.dataset.font);
    close(true);
  };

  button.addEventListener("click", () => (list.hidden ? open() : close(false)));

  button.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      open();
    }
  });

  list.addEventListener("click", (event) => {
    const item = event.target.closest(".jyu-font__item");
    if (item) choose(item);
  });

  list.addEventListener("keydown", (event) => {
    const index = items.indexOf(document.activeElement);
    const move = (to) => {
      event.preventDefault();
      items[(to + items.length) % items.length].focus();
    };
    switch (event.key) {
      case "ArrowDown": move(index + 1); break;
      case "ArrowUp": move(index - 1); break;
      case "Home": move(0); break;
      case "End": move(items.length - 1); break;
      case "Enter":
      case " ":
        event.preventDefault();
        if (index >= 0) choose(items[index]);
        break;
      case "Escape":
        event.preventDefault();
        close(true);
        break;
      case "Tab":
        close(false);
        break;
    }
  });

  /* Sulje, kun painetaan muualle. */
  document.addEventListener("pointerdown", (event) => {
    if (!root.contains(event.target)) close(false);
  });

  /* Alkutila: bodyn attribuutti on jo asetettu, tässä vihje ja valintamerkki. */
  apply(stored());
})();
