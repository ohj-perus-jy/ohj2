/* Koko sivun ääneenluku. convert.py (mark_speech) merkitsee kirja.toml:n
 * [puhe] sivut -listan sivuilla jokaisen luettavan lohkon, jolla on leike:
 * kappaleen, luettelon kohdan, laatikon otsikon ja taulukon alussa on tyhjä
 * <span class="jyu-puhe" data-puhe="tunniste">, otsikolla, koodilohkolla ja
 * kirjan omilla elementeillä (<summary>, tehtäväkortin pää, kaavio...)
 * attribuutti data-puhe itsellään. Leike on assets/puhe/<tunniste>.mp3
 * (äänet tekee zensical/puhe.py). Välilehtijoukkojen ilmoitukset ovat sivun
 * lopun JSON-lohkossa <script id="jyu-puhe">.
 *
 * Yläpalkin kaiutin (overrides/partials/header.html) on piilossa, kunnes
 * sivulta löytyy merkki. Painallus avaa alareunaan soitinpalkin ja aloittaa
 * lukemisen ensimmäisestä ruudulla näkyvästä lohkosta; uusi painallus tai
 * palkin rasti lopettaa. Palkissa on edellinen, toista/tauko, seuraava ja
 * nopeus, joka vaihtuu painalluksella seuraavaan (SPEEDS) ja jää muistiin.
 * Kun palkki on auki, lohkon klikkaus lukee siitä. Luettava lohko korostetaan
 * ja pidetään näkyvissä, ellei lukija ole juuri itse vierittänyt.
 *
 * Luetaan vain se, mikä on toistohetkellä näkyvissä: valitsematon välilehti,
 * suljetun <details>-kohdan sisältö ja animaation korvaama varasisältö
 * ohitetaan. Välilehtijoukkoon tultaessa luetaan ensin joukon ilmoitus ja
 * valitun välilehden ilmoitus, jotta kuulija tietää, mitä jäi lukematta.
 * Leike, joka ei lataudu (puuttuu), ohitetaan. Ulkoasu: assets/css/puhe.css. */

(() => {
  "use strict";

  const button = document.querySelector(".jyu-puhe-button");
  const article = document.querySelector("article.md-content__inner");
  const markers = article ? [...article.querySelectorAll("[data-puhe]")] : [];
  if (!button || !markers.length) return;

  /* Lohkot, joiden alussa oleva merkki korostaa koko lohkon. */
  const BLOCK = "p, li, dt, dd, summary, .admonition-title";

  /* Irrallisen tekstin raja: Python-Markdown jättää aidan jälkeisen tekstin
   * samaan kappaleeseen, ja selain sulkee kappaleen aidan kohdalla, joten
   * teksti jää ilman omaa lohkoaan (ks. loose). */
  const BREAKS = new Set(["P", "DIV", "UL", "OL", "DL", "TABLE", "PRE", "BLOCKQUOTE",
    "DETAILS", "SECTION", "FIGURE", "HR", "H1", "H2", "H3", "H4", "H5", "H6"]);

  /* Lukijan oma vieritys keskeyttää seuraamisen näin pitkäksi aikaa. */
  const USER_SCROLL_MS = 4000;

  /* Nopeusnapin kierto; valinta talteen localStorageen. */
  const SPEEDS = [1, 1.1, 1.25, 1.5, 1.75, 2];
  const SPEED_KEY = "jyu-puhe-nopeus";

  const ICONS = {
    prev: '<path d="M19 20 9 12l10-8zM5 19V5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    next: '<path d="m5 4 10 8-10 8zM19 5v14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    play: '<path d="M7 4v16l13-8z" fill="currentColor"/>',
    pause: '<path d="M7 4h4v16H7zM13 4h4v16h-4z" fill="currentColor"/>',
    close: '<path d="M18 6 6 18M6 6l12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  };
  const icon = (name) => `<svg viewBox="0 0 24 24" aria-hidden="true">${ICONS[name]}</svg>`;

  const read = (id) => {
    try {
      return JSON.parse(document.getElementById(id)?.textContent || "{}");
    } catch {
      return {};
    }
  };
  /* Leikkeet sivuston juuresta; teeman __config kertoo juuren suhteessa sivuun. */
  const root = new URL(`${read("__config").base || "."}/assets/puhe/`, location.href);
  const clipUrl = (clip) => new URL(`${clip}.mp3`, root).href;
  const tabSets = read("jyu-puhe").valilehdet || {};

  /* Irrallinen teksti omaan kääreeseensä merkistä seuraavaan lohkoon tai
   * merkkiin, jotta sen voi korostaa. */
  function loose(marker) {
    const wrapper = document.createElement("span");
    wrapper.className = "jyu-puhe-irto";
    marker.before(wrapper);
    let node = marker;
    while (node && !(node.nodeType === 1 && (BREAKS.has(node.nodeName)
      || (node !== marker && node.matches("[data-puhe]"))))) {
      const next = node.nextSibling;
      wrapper.append(node);
      node = next;
    }
    return wrapper;
  }

  /* Merkin korostettava ja näkyvyydeltään tarkistettava lohko. */
  function target(marker) {
    if (marker.nodeName !== "SPAN") {
      return marker.classList.contains("multifile")
        ? marker.closest(".tabbed-set") || marker : marker;
    }
    const cell = marker.closest("th, td");
    if (cell) return cell.closest("table");
    return marker.parentElement.matches(BLOCK) ? marker.parentElement : loose(marker);
  }

  const units = markers.map((marker) => ({ clip: marker.dataset.puhe, target: target(marker) }));
  const byTarget = new Map();
  units.forEach((unit, index) => {
    if (!byTarget.has(unit.target)) byTarget.set(unit.target, index);
  });

  const visible = (element) => (element.checkVisibility
    ? element.checkVisibility() : element.getClientRects().length > 0);

  /* Välilehtijoukko: otsikot avaimena (convert.py: mark_speech) ja valittu. */
  function tabAnnouncement(set) {
    const labels = [...set.querySelectorAll(":scope > .tabbed-labels > label")];
    const entry = tabSets[labels.map((label) => label.textContent.trim()).join("\n")];
    if (!entry) return [];
    const checked = set.querySelector(":scope > input:checked");
    const label = labels.find((item) => checked && item.htmlFor === checked.id);
    return [entry.joukko, label && entry.valinta[label.textContent.trim()]].filter(Boolean);
  }

  /* Joukot, joihin lohko kuuluu mutta edellinen ei, uloimmasta alkaen. */
  function announcements(element, previous) {
    const sets = [];
    for (let set = element.closest(".tabbed-set"); set; set = set.parentElement.closest(".tabbed-set")) {
      if (!previous || !set.contains(previous)) sets.unshift(set);
    }
    return sets.flatMap(tabAnnouncement);
  }

  const bar = document.createElement("div");
  bar.className = "jyu-puhe-bar";
  bar.setAttribute("role", "region");
  bar.setAttribute("aria-label", "Ääneenluku");
  bar.hidden = true;
  bar.innerHTML = ''
    + `<button type="button" class="jyu-puhe-prev" title="Edellinen kappale" aria-label="Edellinen kappale">${icon("prev")}</button>`
    + `<button type="button" class="jyu-puhe-play" title="Tauko" aria-label="Tauko">${icon("pause")}</button>`
    + `<button type="button" class="jyu-puhe-next" title="Seuraava kappale" aria-label="Seuraava kappale">${icon("next")}</button>`
    + '<button type="button" class="jyu-puhe-speed" title="Lukunopeus"></button>'
    + '<span class="jyu-puhe-count"></span>'
    + '<span class="jyu-puhe-status" role="status"></span>'
    + `<button type="button" class="jyu-puhe-close" title="Lopeta lukeminen" aria-label="Lopeta lukeminen">${icon("close")}</button>`;
  document.body.append(bar);
  const $ = (selector) => bar.querySelector(selector);
  const playButton = $(".jyu-puhe-play");
  const speedButton = $(".jyu-puhe-speed");
  const count = $(".jyu-puhe-count");
  const status = $(".jyu-puhe-status");

  const audio = new Audio();
  const warm = new Audio();
  warm.preload = "auto";
  let current = -1;
  let queue = [];
  let previous = null;
  let highlighted = null;
  let open = false;
  let userScrolledAt = 0;
  let speed = 1;

  /* Uusi src palauttaa playbackRaten defaultPlaybackRateen, joten asetetaan
   * molemmat. */
  function setSpeed(value) {
    speed = SPEEDS.includes(value) ? value : 1;
    audio.defaultPlaybackRate = audio.playbackRate = speed;
    const shown = `${String(speed).replace(".", ",")}×`;
    speedButton.textContent = shown;
    speedButton.setAttribute("aria-label", `Lukunopeus ${shown}`);
  }

  function setPlaying(playing) {
    const label = playing ? "Tauko" : "Toista";
    playButton.innerHTML = icon(playing ? "pause" : "play");
    playButton.title = label;
    playButton.setAttribute("aria-label", label);
    if (navigator.mediaSession) navigator.mediaSession.playbackState = playing ? "playing" : "paused";
  }

  function highlight(element) {
    highlighted?.classList.remove("jyu-puhe-nyt");
    highlighted = element;
    element?.classList.add("jyu-puhe-nyt");
    if (!element || Date.now() - userScrolledAt < USER_SCROLL_MS) return;
    const rect = element.getBoundingClientRect();
    const top = document.querySelector(".md-header")?.offsetHeight || 0;
    if (rect.top < top || rect.bottom > innerHeight - bar.offsetHeight) {
      const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
      element.scrollIntoView({ block: "center", behavior: reduced ? "auto" : "smooth" });
    }
  }

  function showCount() {
    const shown = units.filter((unit) => visible(unit.target));
    const position = units.slice(0, current + 1).filter((unit) => visible(unit.target)).length;
    count.textContent = `${Math.min(position, shown.length)} / ${shown.length}`;
  }

  /* Seuraava näkyvä lohko indeksistä alkaen, tai lopetus. */
  function startUnit(index) {
    while (index < units.length && !visible(units[index].target)) index += 1;
    current = index;
    if (index >= units.length) {
      finish();
      return;
    }
    const unit = units[index];
    queue = [...announcements(unit.target, previous), unit.clip];
    previous = unit.target;
    status.textContent = "";
    highlight(unit.target);
    showCount();
    const following = units.slice(index + 1).find((item) => visible(item.target));
    if (following) warm.src = clipUrl(following.clip);
    playNext();
  }

  function playNext() {
    const clip = queue.shift();
    if (!clip) {
      startUnit(current + 1);
      return;
    }
    audio.src = clipUrl(clip);
    document.dispatchEvent(new CustomEvent("jyu-aani", { detail: "puhe" }));
    audio.play().then(() => setPlaying(true), () => setPlaying(false));
  }

  function finish() {
    audio.removeAttribute("src");
    highlight(null);
    setPlaying(false);
    count.textContent = "";
    status.textContent = "Sivu luettu";
  }

  function firstInView() {
    const top = document.querySelector(".md-header")?.offsetHeight || 0;
    const index = units.findIndex((unit) => visible(unit.target)
      && unit.target.getBoundingClientRect().bottom > top);
    return Math.max(index, 0);
  }

  /* Kaiuttimen nimi ("Kuuntele sivu") pysyy, ja tila on aria-pressedissä:
   * valitsimen nimi ei saa vaihtua tilan mukana, ja teeman vihje palauttaisi
   * sulkeutuessaan nimen, joka napilla oli vihjeen auetessa. */
  function setOpen(on) {
    open = on;
    bar.hidden = !on;
    document.body.classList.toggle("jyu-puhe-auki", on);
    button.setAttribute("aria-pressed", String(on));
    if (on) {
      previous = null;
      startUnit(firstInView());
    } else {
      audio.pause();
      audio.removeAttribute("src");
      queue = [];
      highlight(null);
    }
  }

  function toggle() {
    if (current >= units.length) {
      previous = null;
      startUnit(0);
    } else if (audio.paused) {
      document.dispatchEvent(new CustomEvent("jyu-aani", { detail: "puhe" }));
      audio.play().then(() => setPlaying(true), () => setPlaying(false));
    } else {
      audio.pause();
      setPlaying(false);
    }
  }

  function step(direction) {
    let index = Math.min(current, units.length) + direction;
    while (index >= 0 && index < units.length && !visible(units[index].target)) index += direction;
    if (index >= 0) startUnit(index);
  }

  audio.addEventListener("ended", playNext);
  /* Puuttuva tai rikkinäinen leike ohitetaan. */
  audio.addEventListener("error", () => {
    if (open && audio.getAttribute("src")) playNext();
  });

  /* Teeman vihje on auki myös kohdistuksen ajan, joten osoittimen painallus
   * vapauttaa kohdistuksen, jotta vihje sulkeutuu osoittimen lähtiessä (kuten
   * teeman koodinapeissa). Näppäimistöllä kohdistus jää. */
  button.addEventListener("click", (event) => {
    setOpen(!open);
    if (event.detail) button.blur();
  });
  playButton.addEventListener("click", toggle);
  $(".jyu-puhe-prev").addEventListener("click", () => step(-1));
  $(".jyu-puhe-next").addEventListener("click", () => step(1));
  /* localStorage voi puuttua (yksityinen tila); silloin nopeus koskee vain tätä sivua. */
  speedButton.addEventListener("click", () => {
    setSpeed(SPEEDS[(SPEEDS.indexOf(speed) + 1) % SPEEDS.length]);
    try {
      localStorage.setItem(SPEED_KEY, String(speed));
    } catch {
      /* ei tallennusta */
    }
  });
  $(".jyu-puhe-close").addEventListener("click", () => setOpen(false));

  /* Lohkon klikkaus lukee siitä; linkit, napit, koodi ja valinta eivät. */
  article.addEventListener("click", (event) => {
    if (!open || String(getSelection()).trim()) return;
    if (event.target.closest("a, button, input, select, textarea, label, summary, pre, code, .highlight")) return;
    for (let element = event.target; element && element !== article; element = element.parentElement) {
      if (byTarget.has(element)) {
        previous = null;
        startUnit(byTarget.get(element));
        return;
      }
    }
  });

  const userScroll = () => { userScrolledAt = Date.now(); };
  addEventListener("wheel", userScroll, { passive: true });
  addEventListener("touchmove", userScroll, { passive: true });
  addEventListener("keydown", (event) => {
    if (["ArrowUp", "ArrowDown", "PageUp", "PageDown", "Home", "End", " "].includes(event.key)) userScroll();
  });

  /* Vaiheittaisen ohjeen ääni (walkthrough.js) ja tämä eivät soi yhtä aikaa. */
  document.addEventListener("jyu-aani", (event) => {
    if (event.detail !== "puhe" && !audio.paused) {
      audio.pause();
      setPlaying(false);
    }
  });

  if (navigator.mediaSession) {
    navigator.mediaSession.setActionHandler("play", () => { if (open && audio.paused) toggle(); });
    navigator.mediaSession.setActionHandler("pause", () => { if (open && !audio.paused) toggle(); });
    navigator.mediaSession.setActionHandler("previoustrack", () => { if (open) step(-1); });
    navigator.mediaSession.setActionHandler("nexttrack", () => { if (open) step(1); });
  }

  try {
    setSpeed(Number(localStorage.getItem(SPEED_KEY)));
  } catch {
    setSpeed(1);
  }
  button.hidden = false;
})();
