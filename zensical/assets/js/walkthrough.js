/* Vaiheittainen ohje: lähteen <walkthrough scenes="..."> ja <step scene="...">
 * (convert.py: convert_walkthroughs). Ilman tätä skriptiä ohje on tavallista
 * tekstiä: luvut ##-otsikkoina ja vaiheet ###-otsikkoina peräkkäin. Sellaisena
 * se myös tulostuu, koska /tulosta/ liittää luvut DOMParserilla eikä sisällön
 * <script> silloin aja. Skripti tekee ohjeesta esityksen, jossa näkyy yksi
 * vaihe kerrallaan: piirretty kohtaus ja sen alla vaiheen oma teksti.
 *
 * Kohtaukset ovat sivun omassa tiedostossa, joka on sivulla <script>-tagina
 * ennen tätä skriptiä ja lisää listaan window.jyuWalkScenes funktion
 * (ui) => ({ nimi: () => "<html>" }). ui on alla oleva piirtoapujen kokoelma.
 * Jos yhtään kohtausta ei tule (tiedosto puuttuu), ohje jää tekstiksi.
 *
 * Kohtauksen HTML:ssä animaatiota ohjaavat attribuutit:
 *   data-type       elementin teksti kirjoittuu näkyviin merkki kerrallaan
 *                   (elementissä pelkkää tekstiä)
 *   data-show       elementti tulee näkyviin
 *   data-click      kursori siirtyy elementin päälle ja klikkaa;
 *                   data-on="luokka" lisää klikatessa luokan
 *   data-hide="n"   elementti poistuu kohdassa n (esim. suljettu ikkuna)
 *   data-scroll="px" sisältö vierittyy px verran ylös data-orderin kohdalla
 *                   (esim. pitkä lomake); sisäkkäiset vieritykset summautuvat
 *   data-ring       korostuskehys, kun animaatio on lopussa
 *   data-order="n"  numeroidut ensin pienimmästä alkaen, sitten muut
 *                   dokumenttijärjestyksessä; saman elementin tapahtumat
 *                   järjestyksessä show, click, type
 * Esitys avautuu odottamaan (sivun avautuessa, myös jaetusta osoitteesta, ja
 * tekstistä palatessa): vaihe on alussaan ja näyttämöllä on iso toistonappi,
 * josta animaatio lähtee. Seuraava-nappi, →-näppäin, pyyhkäisy vasemmalle,
 * luvun pilleri, aikajanan merkki ja linkki vaiheeseen (sisällysluettelo)
 * animoivat heti. Edellinen näyttää vaiheen heti valmiina, ja vähemmän
 * liikettä pyytäneelle (prefers-reduced-motion) vaihe on aina valmiina.
 *
 * Kohtaus on piirretty tietokoneen näytölle. Kapeassa palstassa (puhelin)
 * ohje avautuu siksi tekstinä, ja esityksen saa napista. Jos esityksen avaa
 * kapeassa palstassa, siinä on lähikuva: kohtaus lukukokoisena, ja kuva
 * seuraa tapahtumaa eli keskittää kirjoitettavan, klikattavan tai korostetun
 * kohdan. Näyttämön kulman napista saa koko kuvan.
 *
 * Näyttämön oikeassa alakulmassa ovat kuvakkeet kuten videosoittimissa.
 * Koko ruutu -kuvakkeesta esitys täyttää näytön: kohtaus vasemmalla ja
 * vaiheen teksti oikealla, jottei tekstiä tarvitse vierittää kuvan alta.
 * Sama kuvake tai Esc sulkee.
 *
 * Ääneen lukeminen: jos vaiheilla on äänitiedosto (<section data-audio>,
 * convert.py: walkthrough_audio; äänet tekee zensical/puhe.py), kulmassa on
 * myös kaiutin, josta lukemisen saa päälle ja pois.
 *
 * Yksittäinen animaatio: tavallisen sivun <animation scenes="..." scene="...">
 * (convert.py: convert_animations) on yksi kohtaus ilman vaiheita, esim.
 * kuvakaappauksen tilalla. Tagin sisältö on varalla: se näkyy ilman skriptiä
 * ja tulosteessa, ks. enhanceAnimation. */

(() => {
  "use strict";

  /* Kohtaukset piirretään tähän kokoon ja skaalataan näyttämön kokoiseksi. */
  const WIDTH = 800;
  const HEIGHT = 500;

  /* Tätä kapeammassa palstassa ohje avautuu tekstinä ja esitys lähikuvana:
   * koko kohtaus olisi alle 0,65-kertainen, 13 px teksti alle 8,5 px. */
  const SMALL_WIDTH = 520;

  /* Lähikuvan skaala: 13 px teksti ~9 px:ksi. */
  const CLOSE_UP = 0.72;

  /* Yksittäinen animaatio alkaa, kun näyttämöstä näkyy tämä osuus. */
  const IN_VIEW = 0.5;

  /* Ääneen lukemisen kaiutin näyttämön kulmassa: aallot päällä, risti pois
   * päältä (walkthrough.css näyttää niistä toisen). Valinta muistetaan
   * selaimessa. */
  const SPEAKER = '<svg viewBox="0 0 24 24" aria-hidden="true">'
    + '<path d="M3 9h4l5-4v14l-5-4H3z" fill="currentColor"/>'
    + '<path class="jw-speak-on" d="M15.5 8.5a5 5 0 0 1 0 7M18 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
    + '<path class="jw-speak-off" d="M16 9.5l5 5m0-5l-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
    + "</svg>";
  const SPEAK_KEY = "jyu-walk-speak";

  /* Koko ruudun kuvake näyttämön kulmassa: nuolet ulos, kun koko ruutu ei ole
   * päällä, ja sisään, kun on (walkthrough.css näyttää niistä toisen). */
  const FULL = '<svg viewBox="0 0 24 24" aria-hidden="true">'
    + '<path class="jw-full-on" d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    + '<path class="jw-full-off" d="M9 4v5H4M15 4v5h5M20 15h-5v5M4 15h5v5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    + "</svg>";

  /* Iso toistonappi näyttämöllä, kun esitys odottaa alkamista (go). */
  const PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true">'
    + '<path d="M8 5v14l11-7z" fill="currentColor"/></svg>';

  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");

  const esc = (value) => String(value)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");

  /* --- Piirtoavut kohtaustiedostoille ----------------------------------- */

  const imageName = /\.(png|jpe?g|gif|svg)$/i;

  const ui = {
    esc,

    /* Sovellusikkuna. look: light, dark (IDE) tai terminal. body on HTML:ää. */
    window({ title = "", look = "light", body = "" }) {
      return `<div class="jw-win jw-win--${look}">`
        + `<div class="jw-titlebar"><span class="jw-dots"><i></i><i></i><i></i></span>`
        + `<span class="jw-title">${esc(title)}</span></div>${body}</div>`;
    },

    /* Selainikkuna. typeUrl: osoite kirjoitetaan ensimmäisenä (data-order 0). */
    browser({ title, url, body = "", typeUrl = false }) {
      const typed = typeUrl ? ' data-type data-order="0"' : "";
      return ui.window({
        title,
        body: `<div class="jw-address"><span class="jw-url"${typed}>${esc(url)}</span></div>`
          + `<div class="jw-page">${body}</div>`,
      });
    },

    /* GitLabin sivu vasemman reunan valikkoineen. side: valikon rivit
     * (HTML:ää, jotta rivin voi merkitä, esim. <span class="jw-sel">). */
    gitlab({ title, url, crumb = "", body = "", typeUrl = false, heading = "ohj1ht",
      side = ["Manage", "Plan", "Code", "Build", "Deploy", "Operate", "Monitor", "Analyze", "Settings"] }) {
      const items = side.map((item) => (item.startsWith("<") ? item : `<span>${esc(item)}</span>`)).join("");
      return ui.browser({
        title, url, typeUrl,
        body: `<div class="jw-gl"><div class="jw-gl-side"><b>${esc(heading)}</b>${items}</div>`
          + `<div class="jw-gl-main">${crumb ? `<div class="jw-gl-crumb">${esc(crumb)}</div>` : ""}`
          + `${body}</div></div>`,
      });
    },

    /* GitLabin tiedostolista. Rivi: [nimi, viimeisin commit, aika, attribuutit].
     * Kansion nimi päättyy /-merkkiin. */
    files(rows) {
      const icon = (name) => (name.endsWith("/") ? "dir" : imageName.test(name) ? "img" : "doc");
      const body = rows.map(([name, commit, updated, extra = ""]) =>
        `<div${extra ? ` ${extra}` : ""}><span><i class="jw-icon jw-icon--${icon(name)}"></i>`
        + `${esc(name)}</span><span>${esc(commit)}</span><span>${esc(updated)}</span></div>`).join("");
      return `<div class="jw-gl-files"><div><span>Name</span><span>Last commit</span>`
        + `<span>Last update</span></div>${body}</div>`;
    },

    /* Git Bash -istunto. session: [{ cwd, branch, cmd, out }], out: rivit
     * merkkijonoina tai [väri, rivi] (green, red, cyan, yellow, magenta).
     * Komennot from..to-1 kirjoitetaan tässä vaiheessa, aiemmat ovat historiaa.
     * order: jos annettu, j:s kirjoitettava komento saa data-order order + j
     * ja sen tuloste order + j + 0.9, jolloin väliin mahtuu muita tapahtumia
     * (esim. kirjautumisikkuna ennen tulostetta). */
    gitBash({ session, from, to = from, order, user = "olli@kannettava", home = "/c/Users/olli" }) {
      const prompt = ({ cwd, branch }) =>
        `<div><span class="jw-t-green">${esc(user)}</span> <span class="jw-t-magenta">MINGW64</span>`
        + ` <span class="jw-t-yellow">${esc(cwd)}</span>`
        + `${branch ? ` <span class="jw-t-cyan">(${esc(branch)})</span>` : ""}</div>`;
      const output = (lines = []) => lines.map((line) => {
        const [color, text] = Array.isArray(line) ? line : ["", line];
        return `<div${color ? ` class="jw-t-${color}"` : ""}>${esc(text) || " "}</div>`;
      }).join("");
      const at = (value) => (order === undefined ? "" : ` data-order="${value}"`);
      const caret = '<div>$ <span class="jw-caret"></span></div>';

      let html = "";
      for (let i = 0; i < from; i++) {
        html += prompt(session[i]) + `<div>$ ${esc(session[i].cmd)}</div>` + output(session[i].out);
      }
      html += prompt(session[Math.min(from, session.length - 1)]);
      /* Seuraavan komennon rivi on edellisen tulosteen sisällä, jotta se tulee
       * näkyviin vasta tulosteen mukana eikä odota tyhjänä kirjoitettavan
       * rivin alla. */
      const command = (i) =>
        `<div>$ <span data-type${at(order + i - from)}>${esc(session[i].cmd)}</span></div>`;
      if (from < to) html += command(from);
      for (let i = from; i < to; i++) {
        const next = session[i + 1] ?? session[i];
        html += `<div data-show${at(order + i - from + 0.9)}>${output(session[i].out)}${prompt(next)}`
          + `${i === to - 1 ? caret : command(i + 1)}</div>`;
      }
      if (from === to) html += caret;

      const last = session[Math.min(to, session.length - 1)];
      return ui.window({
        title: `MINGW64:${last.cwd.replace(/^~/, home)}`,
        look: "terminal",
        body: `<div class="jw-terminal">${html}</div>`,
      });
    },

    /* Tekstieditori. lines: HTML-rivejä, jotka numeroidaan first:stä alkaen,
     * tai [numeron paikalle tuleva teksti, HTML] (esim. selitysrivi ilman
     * numeroa), joka ei kasvata numerointia. */
    editor({ title, tab, lines, first = 1 }) {
      let number = first;
      const rows = lines.map((line) => {
        const [label, html] = Array.isArray(line) ? line : [number++, line];
        return `<div><span class="jw-ln">${label}</span><span>${html}</span></div>`;
      }).join("");
      return ui.window({
        title, look: "dark",
        body: `<div class="jw-tabs"><span>${esc(tab)}</span></div><div class="jw-code">${rows}</div>`,
      });
    },

    /* Muistio (Windows 11): välilehti, valikkorivi, teksti ilman
     * rivinumeroita ja tilarivi. lines: HTML-rivejä. */
    notepad({ title, tab, lines, status = ["Rivi 1, sarake 1", "100 %", "Windows (CRLF)", "UTF-8"] }) {
      const rows = lines.map((html) => `<div>${html || " "}</div>`).join("");
      return ui.window({
        title,
        body: `<div class="jw-np-tabs"><span>${esc(tab)}</span></div>`
          + `<div class="jw-np-menu"><span>Tiedosto</span><span>Muokkaa</span><span>Näytä</span></div>`
          + `<div class="jw-np-text">${rows}</div>`
          + `<div class="jw-np-status">${status.map((item) => `<span>${esc(item)}</span>`).join("")}</div>`,
      });
    },

    /* Tiedostonhallinta. rows: [nimi, tyyppi, koko, attribuutit]. */
    explorer({ title, path, rows, places = ["Koti", "Työpöytä", "Lataukset", "Kuvat", "Tämä tietokone"] }) {
      const icon = (name, type) => (type === "Kansio" ? "dir" : imageName.test(name) ? "img" : "doc");
      const list = rows.map(([name, type, size, extra = ""]) =>
        `<div${extra ? ` ${extra}` : ""}><span><i class="jw-icon jw-icon--${icon(name, type)}"></i>`
        + `${esc(name)}</span><span>${esc(type)}</span><span>${esc(size)}</span></div>`).join("");
      return ui.window({
        title,
        body: `<div class="jw-ex-bar"><span>←</span><span>→</span><span>↑</span>`
          + `<span class="jw-ex-path">${esc(path)}</span></div>`
          + `<div class="jw-ex"><div class="jw-ex-side">${places.map((p) => `<span>${esc(p)}</span>`).join("")}</div>`
          + `<div class="jw-ex-list"><div><span>Nimi</span><span>Tyyppi</span><span>Koko</span></div>${list}</div></div>`,
      });
    },
  };

  /* --- Kohtauksen soitin ------------------------------------------------- */

  const CURSOR = '<svg class="jw-cursor" viewBox="0 0 22 22" aria-hidden="true">'
    + '<path d="M3 2 L3 18 L7.5 14 L10.5 20.5 L13 19.3 L10 13 L16 13 Z"/></svg>';

  /* Keskeytetty animaatio (uusi vaihe alkoi) heittää tämän. */
  const STOP = Symbol("stop");

  /* Saman elementin tapahtumien järjestys; hide tulee omalla numerollaan. */
  const KINDS = ["show", "click", "type"];

  /* Elementin paikka kohtauksen omissa koordinaateissa. Skaala mitataan
   * piirrosalustasta eikä muuttujasta, jotta mittaus osuu myös kesken
   * lähikuvan siirtymän. */
  const box = (canvas, element) => {
    const outer = canvas.getBoundingClientRect();
    const inner = element.getBoundingClientRect();
    const scale = outer.width / WIDTH;
    return {
      x: (inner.left - outer.left) / scale, y: (inner.top - outer.top) / scale,
      w: inner.width / scale, h: inner.height / scale,
    };
  };

  const centre = (canvas, element) => {
    const { x, y, w, h } = box(canvas, element);
    return [x + w / 2, y + h / 2];
  };

  const visible = (element) => !element.closest(".jw-gone");

  function render(scenes, name) {
    const scene = scenes[name];
    if (scene) {
      try {
        return scene();
      } catch (error) {
        console.error(`vaiheittainen ohje: kohtaus ${name}`, error);
      }
    }
    return `<div class="jw-missing">Kohtausta ei löytynyt: ${esc(name ?? "")}</div>`;
  }

  /* Kohtauksen piirto ja animaatio piirrosalustalle. Vaiheittainen ohje ja
   * yksittäinen animaatio käyttävät samaa. focus(elementit, animoi): ohjeen
   * lähikuva, joka keskittää elementit. -> siirtyikö kuva. */
  function player(canvas, focus = () => false) {
    let run = 0;
    let ringsShown = false;
    let cursor = { x: 640, y: 420 };

    const wait = (ms, token) => new Promise((resolve) => setTimeout(resolve, ms))
      .then(() => { if (token !== run) throw STOP; });

    const moveCursor = (x, y, animate) => {
      const pointer = canvas.querySelector(".jw-cursor");
      if (!pointer) return;
      if (!animate) pointer.style.transition = "none";
      pointer.style.transform = `translate(${x - 3}px, ${y - 2}px)`;
      if (!animate) {
        pointer.getBoundingClientRect();
        pointer.style.transition = "";
      }
      cursor = { x, y };
    };

    const drawRings = () => {
      for (const ring of canvas.querySelectorAll(".jw-ring")) ring.remove();
      if (!ringsShown) return;
      for (const element of canvas.querySelectorAll("[data-ring]")) {
        if (element.closest(".jw-gone, .jw-hidden")) continue;
        const { x, y, w, h } = box(canvas, element);
        const ring = document.createElement("div");
        ring.className = "jw-ring";
        Object.assign(ring.style, {
          left: `${x - 5}px`, top: `${y - 5}px`, width: `${w + 10}px`, height: `${h + 10}px`,
        });
        canvas.append(ring);
      }
    };

    /* Kohtauksen tapahtumat järjestyksessä, ks. tiedoston alku. */
    const timeline = () => {
      const events = [];
      const elements = canvas.querySelectorAll(
        "[data-type], [data-show], [data-click], [data-hide], [data-scroll]");
      [...elements].forEach((element, index) => {
        KINDS.forEach((kind, rank) => {
          if (element.hasAttribute(`data-${kind}`)) {
            events.push({ element, kind, index, rank, order: element.dataset.order });
          }
        });
        /* Vieritys data-orderin kohdalla, piilotus omalla numerollaan. */
        if (element.hasAttribute("data-scroll")) {
          events.push({ element, kind: "scroll", index, rank: KINDS.length, order: element.dataset.order });
        }
        if (element.hasAttribute("data-hide")) {
          events.push({ element, kind: "hide", index, rank: KINDS.length + 1, order: element.dataset.hide });
        }
      });
      const key = ({ order }) => (order === undefined || order === "" ? Infinity : Number(order));
      /* Infinity - Infinity on NaN, joka on epätosi: tasatilanne ratkeaa
       * dokumenttijärjestyksestä. */
      return events.sort((a, b) => key(a) - key(b) || a.index - b.index || a.rank - b.rank);
    };

    /* Valmiin kohtauksen lähikuva: korostetut kohdat, muuten viimeisin
     * klikkaus tai muu tapahtuma. */
    const focusFinished = (animate) => {
      const events = timeline().filter(({ element, kind }) => kind !== "hide" && visible(element));
      const rings = [...canvas.querySelectorAll("[data-ring]")].filter(visible);
      const clicks = events.filter(({ kind }) => kind === "click");
      const target = rings.length ? rings : [(clicks.at(-1) ?? events.at(-1))?.element].filter(Boolean);
      if (target.length) focus(target, animate);
    };

    function finish(direct) {
      const events = timeline();
      for (const { element, kind } of events) {
        if (kind === "click" && element.dataset.on) element.classList.add(element.dataset.on);
        if (kind === "hide") element.classList.add("jw-gone");
        if (kind === "scroll") {
          element.style.transition = "none";
          element.style.transform = `translateY(-${element.dataset.scroll}px)`;
        }
      }
      /* Kursori jää viimeisen klikkauksen kohdalle. Jos se kohde sulkeutui
       * (valikko, ikkuna), kursori pois, ettei se osoita tyhjää. */
      const last = events.filter(({ kind }) => kind === "click").at(-1)?.element;
      const pointed = Boolean(last) && visible(last);
      if (direct && pointed) moveCursor(...centre(canvas, last), false);
      canvas.querySelector(".jw-cursor")?.classList.toggle("jw-cursor--none", !pointed);
      ringsShown = true;
      drawRings();
      focusFinished(!direct);
    }

    /* ready: animaatio valmistellaan heti (kirjoitettavat tyhjiksi,
     * näkyviin tulevat piiloon), mutta se alkaa vasta tämän lupauksen
     * täytyttyä. */
    async function play(token, ready) {
      const events = timeline();
      const texts = new Map();
      for (const { element, kind } of events) {
        if (kind === "type" && !texts.has(element)) {
          texts.set(element, element.textContent);
          element.textContent = "";
        }
        if (kind === "show") element.classList.add("jw-hidden");
      }
      await ready;
      if (token !== run) throw STOP;
      /* Lähikuva klikkauksen tai kirjoituksen kohdalle ennen tapahtumaa,
       * näkyviin tulevan kohdalle vasta sen tultua: terminaalissa tulematon
       * tuloste ei vie tilaa, joten sillä ei ole vielä paikkaa. */
      const first = events.find(({ kind }) => kind === "click" || kind === "type");
      if (first) focus([first.element], false);
      await wait(350, token);
      for (const { element, kind } of events) {
        /* Vieritys liukuu CSS-siirtymällä (walkthrough.css: [data-scroll]). */
        if (kind === "scroll") {
          element.style.transform = `translateY(-${element.dataset.scroll}px)`;
          await wait(600, token);
          continue;
        }
        if ((kind === "click" || kind === "type") && focus([element], true)) await wait(500, token);
        if (kind === "show") {
          element.classList.remove("jw-hidden");
          element.classList.add("jw-reveal");
          if (focus([element], true)) await wait(500, token);
          await wait(420, token);
        } else if (kind === "click") {
          const [x, y] = centre(canvas, element);
          moveCursor(x, y, true);
          await wait(750, token);
          const pulse = document.createElement("div");
          pulse.className = "jw-pulse";
          Object.assign(pulse.style, { left: `${x}px`, top: `${y}px` });
          canvas.append(pulse);
          if (element.dataset.on) element.classList.add(element.dataset.on);
          await wait(450, token);
        } else if (kind === "type") {
          const text = texts.get(element);
          const delay = Math.max(14, Math.min(45, 1500 / text.length));
          for (let i = 1; i <= text.length; i++) {
            element.textContent = text.slice(0, i);
            await wait(delay, token);
          }
          await wait(200, token);
        } else {
          element.classList.add("jw-gone");
          await wait(300, token);
        }
      }
      await wait(150, token);
      finish(false);
    }

    /* Uusi kohtaus; keskeyttää edellisen animaation. animate: animoi, paitsi
     * jos lukija on pyytänyt vähemmän liikettä. ready: lupaus, jota
     * animaatio tai valmiin kohtauksen mittaus odottaa (näkyviin tulo). */
    function show(html, { animate = false, ready } = {}) {
      const token = ++run;
      ringsShown = false;
      canvas.innerHTML = html + CURSOR;
      canvas.querySelector(".jw-cursor").classList.toggle("jw-cursor--none",
        !canvas.querySelector("[data-click]"));
      moveCursor(cursor.x, cursor.y, false);
      if (animate && !reducedMotion.matches) {
        play(token, ready).catch((error) => { if (error !== STOP) throw error; });
      } else if (ready) {
        ready.then(() => { if (token === run) finish(true); });
      } else {
        finish(true);
      }
    }

    return { show, drawRings, focusFinished, finished: () => ringsShown };
  }

  /* --- Esitys ------------------------------------------------------------ */

  /* Otsikon teksti ilman teeman ¶-linkkiä. */
  const headingText = (heading) => [...heading.childNodes]
    .filter((node) => !node.classList?.contains("headerlink"))
    .map((node) => node.textContent).join("").trim();

  function enhance(root, scenes) {
    const chapters = [];
    const steps = [];
    for (const child of root.children) {
      if (child.matches("h2")) {
        chapters.push({ title: headingText(child), heading: child, first: steps.length });
      } else if (child.matches(".jyu-step")) {
        if (!chapters.length) chapters.push({ title: "", heading: null, first: 0 });
        const heading = child.querySelector("h2, h3, h4, h5, h6");
        steps.push({
          el: child, heading, scene: child.dataset.scene, index: steps.length,
          chapter: chapters.length - 1, title: heading ? headingText(heading) : "",
        });
      }
    }
    if (!steps.length) return;

    /* Aikajana on kohtauksen alla luvuittain: luvun pilleri ja sen alla luvun
     * vaiheet, osan leveys vaiheiden määrän mukaan (walkthrough.css:
     * .jw-timeline; sarakkeet ja kapean palstan flex-grow tästä). Vaiheet
     * ennen ensimmäistä lukua ovat osa ilman pilleriä; luku ilman vaiheita
     * ei näy. */
    const parts = chapters.map((chapter, index) => ({
      ...chapter, index, steps: steps.filter((step) => step.chapter === index),
    })).filter((part) => part.steps.length);

    const spoken = steps.some((step) => step.el.dataset.audio);

    const shell = document.createElement("div");
    shell.className = "jw-ui";
    shell.innerHTML =
      `<div class="jw-top">`
      + `<p class="jw-notice" hidden>Kuvallinen esitys on tehty tietokoneen näytölle, `
      + `joten ohje näytetään tässä tekstinä.</p>`
      + `<div class="jw-actions">`
      + `<button type="button" class="jw-mode">Näytä tekstinä</button></div></div>`
      + `<div class="jw-screen"><div class="jw-stage"><div class="jw-canvas" aria-hidden="true"></div>`
      + `<button type="button" class="jw-play" aria-label="Aloita esitys" hidden>${PLAY}</button>`
      + `<button type="button" class="jw-zoom" hidden>Koko kuva</button>`
      + `<div class="jw-controls">`
      + (spoken ? `<button type="button" class="jw-speak" aria-pressed="false"`
        + ` aria-label="Lue ääneen" title="Lue ääneen">${SPEAKER}</button>` : "")
      + `<button type="button" class="jw-full" aria-pressed="false"`
      + ` aria-label="Koko ruutu" title="Koko ruutu">${FULL}</button></div></div></div>`
      + `<div class="jw-live"><div class="jw-timeline" role="group" aria-label="Luvut ja vaiheet"`
      + ` style="grid-template-columns: ${parts.map((part) => `${part.steps.length}fr`).join(" ")}">${parts.map((part) =>
        `<div class="jw-part" style="flex-grow: ${part.steps.length}">`
        + (part.title ? `<button type="button" class="jw-pill" data-chapter="${part.index}">${esc(part.title)}</button>` : "")
        + `<div class="jw-ticks">${part.steps.map((step) =>
          `<button type="button" class="jw-tick" aria-label="Vaihe ${step.index + 1}: ${esc(step.title)}"`
          + ` title="${step.index + 1}. ${esc(step.title)}"></button>`).join("")}</div></div>`).join("")}</div>`
      + `<div class="jw-bar"><span class="jw-count" aria-live="polite"></span>`
      + `<button type="button" class="jw-replay">Toista</button>`
      + `<button type="button" class="jw-prev">← Edellinen</button>`
      + `<button type="button" class="jw-next">Seuraava →</button></div></div>`;
    root.prepend(shell);
    root.classList.add("jyu-walk--live");
    root.tabIndex = -1;

    const $ = (selector) => shell.querySelector(selector);
    const stage = $(".jw-stage");
    const canvas = $(".jw-canvas");
    const zoomButton = $(".jw-zoom");
    const playButton = $(".jw-play");
    const modeButton = $(".jw-mode");
    const fullButton = $(".jw-full");
    const speakButton = $(".jw-speak");
    const voice = new Audio();
    const notice = $(".jw-notice");
    const ticks = [...shell.querySelectorAll(".jw-tick")];
    const chapterButtons = [...shell.querySelectorAll("[data-chapter]")];

    let current = 0;
    let closeUp = false;
    let wantCloseUp = true;
    let full = false;
    let native = false;
    let speaking = false;
    let started = false;
    /* Odottavan animaation käynnistys (go "wait"), kun toistonappi näkyy. */
    let startPlay = null;
    let camera = { x: WIDTH / 2, y: HEIGHT / 2 };

    /* Piirrosalustan skaala ja siirto. Lähikuvassa camera on kohtauksen piste,
     * joka tulee näyttämön keskelle, kuitenkin niin, ettei kuvan reuna irtoa. */
    const applyCamera = (animate) => {
      const width = stage.clientWidth;
      const height = stage.clientHeight;
      const scale = closeUp ? CLOSE_UP : width / WIDTH;
      let x = 0;
      let y = 0;
      if (closeUp) {
        x = Math.min(0, Math.max(width - WIDTH * scale, width / 2 - camera.x * scale));
        y = Math.min(0, Math.max(height - HEIGHT * scale, height / 2 - camera.y * scale));
      }
      canvas.classList.toggle("jw-canvas--moving", animate && !reducedMotion.matches);
      canvas.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
    };

    /* Lähikuva elementtien kohdalle. Näyttämöä leveämpi alue tasataan
     * vasempaan reunaan ja korkeampi alareunaan: terminaalin uusin rivi on
     * alimpana. -> siirtyikö kuva. */
    const focus = (elements, animate) => {
      if (!closeUp) return false;
      const boxes = elements.filter(visible).map((element) => box(canvas, element));
      if (!boxes.length) return false;
      const left = Math.min(...boxes.map((b) => b.x));
      const top = Math.min(...boxes.map((b) => b.y));
      const right = Math.max(...boxes.map((b) => b.x + b.w));
      const bottom = Math.max(...boxes.map((b) => b.y + b.h));
      const seenWidth = stage.clientWidth / CLOSE_UP;
      const seenHeight = stage.clientHeight / CLOSE_UP;
      const next = {
        x: right - left > seenWidth ? left - 12 + seenWidth / 2 : (left + right) / 2,
        y: bottom - top > seenHeight ? bottom + 12 - seenHeight / 2 : (top + bottom) / 2,
      };
      const moved = Math.hypot(next.x - camera.x, next.y - camera.y) > 24;
      camera = next;
      applyCamera(animate);
      return moved;
    };

    const scene = player(canvas, focus);

    /* Näyttämön koko: lähikuva päälle tai pois. Piilossa oleva näyttämö
     * (tekstinä) on 0 px leveä, eikä sen mitasta päätetä mitään. */
    const fit = () => {
      if (!stage.clientWidth) return;
      const small = stage.clientWidth < SMALL_WIDTH;
      closeUp = small && wantCloseUp;
      zoomButton.hidden = !small;
      zoomButton.textContent = closeUp ? "Koko kuva" : "Lähikuva";
      applyCamera(false);
    };

    /* animate: false näyttää vaiheen valmiina, true animoi, "wait" jättää
     * vaiheen alkuunsa ja näyttämölle ison toistonapin, josta animaatio ja
     * ääni lähtevät (open). Muu siirtyminen ottaa napin pois. */
    function go(index, animate, remember = true) {
      current = Math.max(0, Math.min(steps.length - 1, index));
      const step = steps[current];

      steps.forEach((each, i) => each.el.classList.toggle("jyu-step--current", i === current));
      $(".jw-count").textContent = `Vaihe ${current + 1} / ${steps.length}`;
      $(".jw-prev").disabled = current === 0;
      $(".jw-next").disabled = current === steps.length - 1;
      for (const button of chapterButtons) {
        button.setAttribute("aria-current", String(Number(button.dataset.chapter) === step.chapter));
      }
      ticks.forEach((tick, i) => {
        tick.classList.toggle("jw-tick--done", i < current);
        tick.classList.toggle("jw-tick--current", i === current);
      });
      /* Osoite seuraa vaihetta, jotta uudelleenlataus ja jaettu linkki
       * avaavat saman vaiheen. replaceState ei vieritä eikä laukaise
       * hashchangea. */
      if (remember && step.heading?.id) history.replaceState(null, "", `#${step.heading.id}`);

      /* Edellinen odottava animaatio päästetään lupauksestaan vasta nyt,
       * jolloin seuraava kohtaus on jo alkanut ja soitin keskeyttää sen. */
      startPlay?.();
      startPlay = null;
      const wait = animate === "wait";
      const ready = wait ? new Promise((resolve) => { startPlay = resolve; }) : undefined;
      playButton.hidden = !wait;
      scene.show(render(scenes, step.scene), { animate: Boolean(animate), ready });
      if (!wait) speak();
    }

    const textMode = () => root.classList.contains("jyu-walk--text");

    /* Osoitteen vaihe: linkki vaiheen tai luvun otsikkoon (sisällysluettelo,
     * jaettu osoite). -> vaiheen numero tai -1. */
    function hashIndex() {
      const id = decodeURIComponent(location.hash.slice(1));
      const target = id && document.getElementById(id);
      if (!target || !root.contains(target) || shell.contains(target)) return -1;
      let index = steps.findIndex((step) => step.el.contains(target));
      if (index < 0) index = chapters.find((chapter) => chapter.heading === target)?.first ?? -1;
      return index < steps.length ? index : -1;
    }

    /* Sisällysluettelon linkki: vaihe alkaa alusta. -> osuiko osoite vaiheeseen. */
    function followHash() {
      if (textMode()) return false;
      const index = hashIndex();
      if (index < 0) return false;
      go(index, true, false);
      root.scrollIntoView({ block: "start" });
      return true;
    }

    /* Esityksen avaus sivun avautuessa ja tekstistä palatessa: osoitteen
     * vaihe tai nykyinen, alussaan odottamassa toistonappia (go "wait").
     * Vähemmän liikettä pyytäneelle vaihe on heti valmiina, koska animaatiota
     * ei olisi. */
    function open() {
      const index = hashIndex();
      go(index < 0 ? current : index, reducedMotion.matches ? false : "wait", false);
      if (index >= 0) root.scrollIntoView({ block: "start" });
    }

    /* Tekstinä tai esityksenä. Esitykseen palatessa näyttämö tulee näkyviin,
     * joten sen koko mitataan ennen vaiheen piirtämistä. */
    function setMode(text) {
      if (text) {
        setFull(false);
        voice.pause();
      }
      root.classList.toggle("jyu-walk--text", text);
      modeButton.textContent = text ? "Näytä esityksenä" : "Näytä tekstinä";
      notice.hidden = !(text && root.clientWidth < SMALL_WIDTH);
      if (text) return;
      fit();
      open();
    }

    /* Ääneen lukeminen: kun kaiutin on päällä, vaiheen oma äänitiedosto soi
     * alusta aina vaiheeseen siirryttäessä. Vaiheelta, jonka ääni puuttuu tai
     * on tehty vanhasta tekstistä, ei kuulu mitään (convert.py:
     * walkthrough_audio). Sivun avautuessa ääni alkaa vasta toistonapista
     * (open), ja vähemmän liikettä pyytäneelle, jolle vaihe on heti valmiina,
     * ei itsestään ollenkaan (started): selain estäisi sen ennen lukijan
     * ensimmäistä painallusta. */
    function speak() {
      voice.pause();
      const src = steps[current].el.dataset.audio;
      if (!speaking || !started || textMode() || !src) return;
      /* Sama tiedosto (Toista) alusta itse: saman osoitteen uudelleen
       * asettaminen ei kaikissa selaimissa lataa tiedostoa uudestaan. */
      const url = new URL(src, document.baseURI).href;
      if (voice.src === url) voice.currentTime = 0;
      else voice.src = url;
      voice.play().catch(() => {});
    }

    /* Päälle: vaihe alkaa alusta kuten Toista-napista, jotta ääni ja animaatio
     * kulkevat yhdessä (go soittaa äänen). Pois: vain ääni pysähtyy. */
    function setSpeaking(on) {
      speaking = on;
      speakButton.setAttribute("aria-pressed", String(on));
      try {
        localStorage.setItem(SPEAK_KEY, on ? "1" : "0");
      } catch {
        /* Yksityinen ikkuna tai estetty tallennus: valinta vain tälle käynnille. */
      }
      if (on) go(current, true);
      else speak();
    }

    /* Koko ruutu (näyttämön kulman kuvake): kohtaus vasemmalla ja vaiheen
     * teksti oikealla (walkthrough.css: .jyu-walk--full). Selaimen koko
     * näytön tila, kun se
     * onnistuu; muuten, esimerkiksi iPhonella, ikkunan täyttävä kerros.
     * native: koko näytön tila on päällä, joten sen päättyminen (Esc
     * selaimelle) sulkee myös kerroksen. */
    function setFull(on) {
      if (on === full) return;
      full = on;
      root.classList.toggle("jyu-walk--full", on);
      document.documentElement.classList.toggle("jw-full-open", on);
      const label = on ? "Sulje koko ruutu (Esc)" : "Koko ruutu";
      fullButton.setAttribute("aria-label", label);
      fullButton.title = label;
      fullButton.setAttribute("aria-pressed", String(on));
      if (on) {
        root.requestFullscreen?.().then(() => { native = full; }, () => {});
        root.focus({ preventScroll: true });
      } else {
        native = false;
        if (document.fullscreenElement === root) document.exitFullscreen().catch(() => {});
        root.scrollIntoView({ block: "start" });
      }
    }

    const next = () => { if (current < steps.length - 1) go(current + 1, true); };
    const previous = () => { if (current > 0) go(current - 1, false); };

    $(".jw-next").addEventListener("click", next);
    $(".jw-prev").addEventListener("click", previous);
    $(".jw-replay").addEventListener("click", () => go(current, true));
    /* Toistonappi: odottava animaatio ja ääni alkavat. Painallus on lukijan
     * ele, joten selain sallii äänen. Klikkaus jatkaa näyttämölle, joka
     * kohdistaa ohjeen nuolinäppäimiä varten. */
    playButton.addEventListener("click", () => {
      playButton.hidden = true;
      startPlay?.();
      startPlay = null;
      speak();
    });
    ticks.forEach((tick, i) => tick.addEventListener("click", () => go(i, true)));
    for (const button of chapterButtons) {
      button.addEventListener("click", () => go(chapters[Number(button.dataset.chapter)].first, true));
    }
    modeButton.addEventListener("click", () => setMode(!textMode()));
    fullButton.addEventListener("click", () => setFull(!full));
    if (speakButton) {
      try {
        speaking = localStorage.getItem(SPEAK_KEY) === "1";
      } catch {
        speaking = false;
      }
      speakButton.setAttribute("aria-pressed", String(speaking));
      speakButton.addEventListener("click", () => setSpeaking(!speaking));
    }
    document.addEventListener("fullscreenchange", () => {
      if (native && document.fullscreenElement !== root) setFull(false);
    });
    zoomButton.addEventListener("click", () => {
      wantCloseUp = !wantCloseUp;
      fit();
      if (closeUp && scene.finished()) scene.focusFinished(false);
    });
    stage.addEventListener("click", () => root.focus({ preventScroll: true }));
    root.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && full) {
        setFull(false);
        event.preventDefault();
        return;
      }
      if (textMode() || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      if (event.target.closest("input, textarea, select, [contenteditable]")) return;
      if (event.key === "ArrowRight") next();
      else if (event.key === "ArrowLeft") previous();
      else return;
      event.preventDefault();
    });

    /* Pyyhkäisy kosketusnäytöllä: vasemmalle seuraava, oikealle edellinen.
     * Näyttämön touch-action: pan-y jättää pystysuuntaisen vierityksen
     * selaimelle (walkthrough.css). */
    let swipe = null;
    stage.addEventListener("pointerdown", (event) => {
      swipe = event.pointerType === "mouse" ? null : { x: event.clientX, y: event.clientY };
    });
    stage.addEventListener("pointerup", (event) => {
      if (!swipe) return;
      const dx = event.clientX - swipe.x;
      const dy = event.clientY - swipe.y;
      swipe = null;
      if (Math.abs(dx) < 50 || Math.abs(dy) > Math.abs(dx)) return;
      if (dx < 0) next();
      else previous();
    });
    stage.addEventListener("pointercancel", () => { swipe = null; });

    addEventListener("hashchange", followHash);
    /* Linkki nykyiseen vaiheeseen ei muuta osoitetta eikä laukaise
     * hashchangea, joten klikkaus toistaa vaiheen tässä. */
    document.addEventListener("click", (event) => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      const link = event.target.closest("a[href^='#']");
      if (link && link.hash === location.hash) followHash();
    });

    new ResizeObserver(() => {
      fit();
      scene.drawRings();
      if (closeUp && scene.finished()) scene.focusFinished(false);
    }).observe(stage);

    if (root.clientWidth < SMALL_WIDTH) {
      setMode(true);
    } else {
      fit();
      open();
    }
    started = true;
    /* Kehykset mitataan tekstistä, joka voi vaihtaa kirjasinta latauksen jälkeen. */
    document.fonts?.ready.then(scene.drawRings);
  }

  /* --- Yksittäinen animaatio --------------------------------------------- */

  /* Tavallisen sivun animaatio (.jyu-anim, convert.py: convert_animations).
   * Kohtaus piirretään tagin sisällön eteen, ja sisältö piiloutuu näytöltä
   * mutta jää ruudunlukijalle ja tulosteeseen (walkthrough.css). Kohtaus soi
   * kerran, kun näyttämöstä näkyy puolet: sivua vieritettäessä tai kun sen
   * välilehti avataan. Siihen asti näkyy animaation alku. Vähemmän liikettä
   * pyytäneelle kohtaus piirretään valmiina, kun se tulee näkyviin, koska
   * piilossa olevalta välilehdeltä ei voi mitata kursorin ja kehysten
   * paikkaa. Lähikuvaa ei ole: kapeassa palstassa kohtaus pienenee kuten
   * kuva. Jos kohtausta ei ole, sisältö jää näkyviin. */
  function enhanceAnimation(root, scenes) {
    const name = root.dataset.scene;
    if (!scenes[name]) {
      console.error(`animaatio: kohtausta ei löytynyt: ${name}`);
      return;
    }

    const shell = document.createElement("div");
    shell.className = "jw-anim";
    shell.innerHTML = `<div class="jw-stage"><div class="jw-canvas" aria-hidden="true"></div></div>`
      + `<div class="jw-anim-bar"><button type="button" class="jw-replay">Toista</button></div>`;
    root.prepend(shell);
    root.classList.add("jyu-anim--live");

    const stage = shell.querySelector(".jw-stage");
    const canvas = shell.querySelector(".jw-canvas");
    const scene = player(canvas);

    new ResizeObserver(() => {
      if (!stage.clientWidth) return;
      canvas.style.transform = `scale(${stage.clientWidth / WIDTH})`;
      scene.drawRings();
    }).observe(stage);

    /* Ensimmäinen ilmoitus tulee heti, ja isIntersecting on tosi pienestäkin
     * osasta, joten kynnys tarkistetaan itse (pyöristyksen varalla väljästi). */
    const threshold = reducedMotion.matches ? 0 : IN_VIEW;
    const ready = new Promise((resolve) => {
      const observer = new IntersectionObserver((entries) => {
        if (!entries.some((entry) => entry.isIntersecting
          && entry.intersectionRatio >= threshold - 0.01)) return;
        observer.disconnect();
        resolve();
      }, { threshold });
      observer.observe(stage);
    });

    scene.show(render(scenes, name), { animate: true, ready });
    shell.querySelector(".jw-replay").addEventListener("click",
      () => scene.show(render(scenes, name), { animate: true }));
    document.fonts?.ready.then(scene.drawRings);
  }

  const scenes = {};
  for (const factory of window.jyuWalkScenes ?? []) {
    try {
      Object.assign(scenes, factory(ui));
    } catch (error) {
      console.error("vaiheittainen ohje: kohtaustiedosto", error);
    }
  }
  if (Object.keys(scenes).length) {
    for (const root of document.querySelectorAll(".jyu-walk")) enhance(root, scenes);
    for (const root of document.querySelectorAll(".jyu-anim")) enhanceAnimation(root, scenes);
  }
})();
