/* Leipätekstin kirjasimen ja koon valikko yläpalkissa. Avaa ja sulkee
 * paneelin, kirjoittaa kirjasimen bodyn data-jyu-font-attribuuttiin ja koon
 * bodyn --jyu-text-scale-muuttujaan sekä molemmat localStorageen ("jyu-font",
 * "jyu-text-size"). Tallennetut arvot lukee sivun alussa header.html:n
 * inline-skripti, jotta teksti ei välähdä oletuskirjasimella eikä hyppää.
 *
 * Oletukset (data-font="", koko 100) eivät tallennu vaan poistavat
 * tallennuksen. Paneeli pysyy auki valittaessa, jotta kirjasinta ja kokoa voi
 * kokeilla yhdessä; se sulkeutuu painikkeesta, Esc:llä ja kun kohdistus tai
 * napautus menee muualle. Koon napit ovat listan yllä, ja + ja − toimivat
 * näppäiminä koko paneelissa. Kirjasinlista on role="listbox" kuten <select>:
 * nuolet liikkuvat ja Enter valitsee. Myös hiiri siirtää kohdistusta, joten
 * korostettuna on aina yksi kohta. Painikkeessa on vain kuvake, joten
 * valinnat kerrotaan sen aria-labelissa ja teeman vihjeessä
 * (content.tooltips) (kohdan data-short ja koko), ks. hint. */

(() => {
  "use strict";

  const FONT_KEY = "jyu-font";
  const SIZE_KEY = "jyu-text-size";

  const root = document.querySelector("[data-md-component=jyu-font]");
  if (!root) return;

  const button = root.querySelector(".jyu-font__button");
  const panel = root.querySelector(".jyu-font__panel");
  const list = root.querySelector(".jyu-font__list");
  const items = [...root.querySelectorAll(".jyu-font__item")];
  const steppers = [...root.querySelectorAll(".jyu-font__step")];
  const reset = root.querySelector(".jyu-font__reset");
  const steps = (root.dataset.steps || "100").split(" ").map(Number);
  if (!button || !panel || !list || !items.length || !reset) return;

  /* localStorage voi puuttua (yksityinen tila); silloin valinta koskee vain tätä sivua. */
  const stored = (key) => {
    try {
      return localStorage.getItem(key) || "";
    } catch {
      return "";
    }
  };
  const store = (key, value) => {
    try {
      if (value) localStorage.setItem(key, value);
      else localStorage.removeItem(key);
    } catch {
      /* ei tallennusta */
    }
  };

  /* Teeman vihje on auki, kun painikkeella on osoitin tai kohdistus. Sen
   * teksti annetaan titlenä: tooltips.js siirtää titlen vihjeeseen ja pitää
   * sen poissa attribuutista, ettei selain näytä omaa vihjettään rinnalle,
   * myös kun valinta vaihtuu vihjeen ollessa auki. Paneelin ollessa auki
   * vihje piilotetaan (cover), koska se tulisi painikkeen alle paneelin
   * päälle; piilossa sitä ei voi mitata, joten se mitataan esiin tullessa
   * (measure). Vihjeen id on aria-describedbyssä vain vihjeen ollessa auki,
   * joten se otetaan talteen.
   *
   * Esc palauttaa kohdistuksen painikkeeseen, jolloin vihje aukeaisi ja jäisi
   * näkyviin, vaikka osoitin on muualla ja valinta näkyi juuri paneelissa.
   * Siksi Escin jälkeen (quiet) kohdistus ei pidä vihjettä auki: se näkyy
   * vain osoittimen ollessa painikkeella, kunnes kohdistus lähtee painikkeesta. */
  let tip = "";
  let quiet = false;
  let hovered = false;
  const hint = (text) => {
    button.title = text;
  };
  const measure = () => {
    const inner = document.getElementById(tip)?.firstElementChild;
    if (inner) inner.parentElement.style.setProperty("--md-tooltip-width", `${inner.offsetWidth}px`);
  };
  const cover = () => {
    const element = document.getElementById(tip);
    if (element) element.hidden = !panel.hidden || (quiet && !hovered);
  };
  const hover = (on) => {
    hovered = on;
    cover();
    if (on) measure();
  };
  button.addEventListener("pointerenter", () => hover(true));
  button.addEventListener("pointerleave", () => hover(false));
  button.addEventListener("blur", () => { quiet = false; });
  button.addEventListener("focus", cover);
  new MutationObserver(() => {
    tip = button.getAttribute("aria-describedby") || tip;
    cover();
  }).observe(button, { attributeFilter: ["aria-describedby"] });

  let font = items[0];
  let size = 100;

  const describe = () => {
    const short = font.dataset.short || font.querySelector(".jyu-font__name").textContent;
    const text = `Leipäteksti: ${short}, ${size} %`;
    hint(text);
    button.setAttribute("aria-label", text);
  };

  /* Valittu kohta on listan ainoa sarkaimella saavutettava, jotta Tab vie
   * koon napeista listaan ja listasta pois. */
  const applyFont = (id) => {
    font = items.find((candidate) => candidate.dataset.font === id) || items[0];
    const chosen = font.dataset.font;
    if (chosen) document.body.setAttribute("data-jyu-font", chosen);
    else document.body.removeAttribute("data-jyu-font");
    for (const candidate of items) {
      candidate.setAttribute("aria-selected", String(candidate === font));
      candidate.tabIndex = candidate === font ? 0 : -1;
    }
    describe();
  };

  const applySize = (value) => {
    size = steps.includes(value) ? value : 100;
    if (size === 100) document.body.style.removeProperty("--jyu-text-scale");
    else document.body.style.setProperty("--jyu-text-scale", String(size / 100));
    reset.firstElementChild.textContent = `${size} %`;
    reset.setAttribute("aria-disabled", String(size === 100));
    for (const stepper of steppers) {
      const next = steps.indexOf(size) + Number(stepper.dataset.step);
      stepper.setAttribute("aria-disabled", String(next < 0 || next >= steps.length));
    }
    describe();
  };

  /* Lukukohta pysyy paikallaan: ennen koon vaihtoa haetaan syvin tekstilohko,
   * joka näkyy yläpalkin alareunassa, ja vaihdon jälkeen sivua vieritetään
   * niin, että lohkon sama kohta on taas siinä. Kokonaan näkyvästä lohkosta
   * pidetään paikallaan yläreuna. Ilman tätä yläpuolinen teksti kasvaisi tai
   * kutistuisi ja luettava kohta karkaisi ruudulta. Piilossa olevat lohkot
   * (suljettu details, toinen välilehti) ohitetaan, koska niillä ei ole
   * korkeutta. */
  const BLOCKS = "p, li, dt, dd, h1, h2, h3, h4, h5, h6, pre, tr, figure, summary, .admonition-title";
  const keepReading = () => {
    const content = document.querySelector(".md-content__inner");
    if (!content) return () => {};
    const top = document.querySelector(".md-header")?.getBoundingClientRect().bottom ?? 0;
    let block = null;
    for (const candidate of content.querySelectorAll(BLOCKS)) {
      if (block && !block.contains(candidate)) break;
      const box = candidate.getBoundingClientRect();
      if (box.height && box.bottom > top) block = candidate;
    }
    if (!block) return () => {};
    const before = block.getBoundingClientRect();
    const part = Math.max(0, (top - before.top) / before.height);
    return () => {
      const after = block.getBoundingClientRect();
      window.scrollBy(0, after.top + part * after.height - (before.top + part * before.height));
    };
  };

  const resize = (value) => {
    if (!steps.includes(value) || value === size) return;
    const restore = keepReading();
    store(SIZE_KEY, value === 100 ? "" : String(value));
    applySize(value);
    restore();
  };

  const step = (direction) => resize(steps[steps.indexOf(size) + direction]);

  /* Kohtien nimet näkyvät omilla kirjasimillaan, ja selain lataa kirjasimen
   * vasta kun sitä käytetään: ilman tätä nimet piirtyisivät avattaessa ensin
   * varakirjasimella ja vaihtuisivat hetken päästä, jolloin listan leveyskin
   * muuttuu. Lataus alkaa, kun osoitin tai kohdistus tulee valikkoon, eli
   * ennen kuin lista ehtii aueta. Perheet luetaan tyyleistä (fontmenu.css). */
  const preload = () => {
    for (const item of items) {
      const label = item.querySelector(".jyu-font__name");
      document.fonts?.load("1em " + getComputedStyle(label).fontFamily, label.textContent);
    }
  };
  root.addEventListener("pointerenter", preload, { once: true });
  root.addEventListener("focusin", preload, { once: true });

  const open = () => {
    panel.hidden = false;
    cover();
    button.setAttribute("aria-expanded", "true");
    font.focus();
  };

  /* Vihje tulee taas näkyviin, joten se mitataan nyt (ks. hint). */
  const close = (refocus) => {
    if (panel.hidden) return;
    panel.hidden = true;
    quiet = refocus;
    cover();
    measure();
    button.setAttribute("aria-expanded", "false");
    if (refocus) button.focus();
  };

  const choose = (item) => {
    store(FONT_KEY, item.dataset.font);
    applyFont(item.dataset.font);
  };

  /* Hiirellä kohdistus ei jää painikkeeseen, koska teeman vihje pysyisi
   * silloin auki osoittimen lähdettyä. Näppäimistöllä (click-tapahtuman
   * detail 0) kohdistus jää painikkeeseen. */
  button.addEventListener("click", (event) => {
    if (panel.hidden) {
      open();
    } else {
      close(false);
      if (event.detail) button.blur();
    }
  });

  button.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      open();
    }
  });

  for (const stepper of steppers) {
    stepper.addEventListener("click", () => step(Number(stepper.dataset.step)));
  }
  reset.addEventListener("click", () => resize(100));

  list.addEventListener("click", (event) => {
    const item = event.target.closest(".jyu-font__item");
    if (item) choose(item);
  });

  /* Hiiren alla oleva kohta saa kohdistuksen (ulkoasu: :focus). Erillinen
   * :hover-korostus jäisi näkyviin nuolilla liikuttaessa toisen rinnalle. */
  list.addEventListener("pointermove", (event) => {
    const item = event.target.closest(".jyu-font__item");
    if (item && item !== document.activeElement) item.focus();
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
    }
  });

  /* + ja − missä tahansa paneelissa; Ctrl/Cmd jää selaimen zoomaukselle. */
  panel.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      event.preventDefault();
      close(true);
    } else if ((event.key === "+" || event.key === "-") && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      step(event.key === "+" ? 1 : -1);
    }
  });

  /* Sulje, kun kohdistus siirtyy valikon ulkopuolelle (Tab) tai painetaan
   * muualle. Ilman relatedTargetia kohdistus ei siirtynyt minnekään, vaan
   * esimerkiksi paneelin tyhjää kohtaa napautettiin. */
  root.addEventListener("focusout", (event) => {
    if (event.relatedTarget && !root.contains(event.relatedTarget)) close(false);
  });

  document.addEventListener("pointerdown", (event) => {
    if (!root.contains(event.target)) close(false);
  });

  /* Alkutila: bodyn attribuutti ja muuttuja ovat jo asetettu, tässä vihje,
   * valintamerkki ja kokorivi. */
  applyFont(stored(FONT_KEY));
  applySize(Number(stored(SIZE_KEY)) || 100);
})();
