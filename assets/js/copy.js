/* Kopiointinapin ilmoitus napin viereen. Teeman nappi (content.code.copy)
 * kuittaa kopioinnin sivun oikean alakulman ilmoituksella (.md-dialog), joka
 * on niin kaukana napista, ettei lukija huomaa sitä. Tässä nappi otetaan
 * teemalta: sen data-clipboard-target poistetaan, jolloin teeman ClipboardJS
 * ei tartu painallukseen, ja kopiointi ja kuittaus tehdään itse. Kuittaus
 * on nappirivin elementti, mutta tyyli sijoittaa sen rivin vasemmalle
 * puolelle, joten se ei siirrä nappeja. Ulkoasu: assets/css/copy.css. */

(() => {
  "use strict";

  /* Ilmoituksen kesto, kuten teeman omalla. */
  const SHOWN_MS = 2000;

  /* Komentorivilohkon kehotteet: "$ ", "root@kontti:/app# " ja Alpinen
   * komentotulkin "/ # " tai "/app # ". Pelkkä "# " on rootin kehote vain
   * lohkossa, jossa ei ole muita kehotteita; muuten se on tulosteen
   * kommenttirivi (cat Dockerfile). "#5 [1/5] FROM …" on BuildKitin
   * tulostetta. */
  const PROMPT =
    /^(?:[\w.-]+@[\w.-]+:[^\s$#]*[$#]|[~/][^\s$#]* [$#]|\$)(?: |$)/;
  const ROOT_PROMPT = /^#(?: |$)/;

  /* Heredocin lopetussana; <<< on here-string eikä aloita heredocia. */
  const HEREDOC = /(?<!<)<<(?!<)-?\s*(['"]?)(\w+)\1/;

  /* Komentorivilohkon (```console) rivit: kunkin rivin teksti, sen alussa
   * olevan kehotteen pituus (0, jos kehotetta ei ole) ja komento (null, jos
   * rivi on tulostetta tai pelkkä kehote). Komento jatkuu \-rivinvaihdon yli
   * ja heredocin loppuun asti, joten niiden rivit (myös #-kommentit) ovat
   * komentoa sellaisinaan eikä niissä ole kehotetta. Kehote tunnistetaan
   * tekstistä eikä Pygmentsin luokista (.gp, .go): Pygments pitää BuildKitin
   * tulosterivejä kehotteina ja venyttää kehotteen rivin seuraavaan $- tai
   * %-merkkiin (echo $?, kill %1). null, jos lohkossa ei ole yhtään
   * kehotetta. */
  const parse = (text) => {
    const lines = text.split("\n");
    const prompt = lines.some((line) => PROMPT.test(line)) ? PROMPT
      : lines.some((line) => ROOT_PROMPT.test(line)) ? ROOT_PROMPT : null;
    if (!prompt) return null;
    const parsed = [];
    let heredoc = null;
    let continued = false;
    for (const line of lines) {
      if (heredoc) {
        parsed.push({ line, prompt: 0, command: line });
        if (line.trim() === heredoc) heredoc = null;
        continue;
      }
      let command = line;
      let length = 0;
      if (!continued) {
        length = line.match(prompt)?.[0].length ?? 0;
        command = length ? line.slice(length) : "";
        if (!command.trim()) {
          parsed.push({ line, prompt: length, command: null });
          continue;
        }
      }
      parsed.push({ line, prompt: length, command });
      continued = command.endsWith("\\");
      heredoc = command.match(HEREDOC)?.[2] ?? null;
    }
    return parsed;
  };

  /* Kopiointinapin teksti komentorivilohkosta: vain komennot, kehote ja
   * tulosterivit pois, koska terminaaliin liitettyinä ne ajettaisiin
   * komentoina. Lohko ilman yhtään kehotetta kopioidaan sellaisenaan. */
  const commands = (text) => {
    const lines = parse(text);
    if (!lines) return text;
    return lines.filter((line) => line.command !== null)
      .map((line) => line.command).join("\n");
  };

  /* Hiirellä maalattuun tekstiin ei tule kehotetta: kehotteen merkit
   * kääritään elementtiin, jota ei voi valita (copy.css). Kääre tehdään
   * tekstisolmuihin eikä Pygmentsin elementteihin, joten kehote säilyttää
   * värinsä, vaikka se jakautuisi usealle elementille. Kehote jää sivun
   * tekstiksi, joten kopiointinappi (innerText), haku ja ruudunlukija
   * näkevät sen kuten ennenkin. */
  const markPrompts = (code) => {
    const lines = parse(code.textContent);
    if (!lines) return;
    const prompts = [];
    let offset = 0;
    for (const { line, prompt } of lines) {
      if (prompt) prompts.push([offset, offset + prompt]);
      offset += line.length + 1;
    }
    const nodes = [];
    const walker = document.createTreeWalker(code, NodeFilter.SHOW_TEXT);
    for (let node, start = 0; (node = walker.nextNode());
      start += node.length) {
      nodes.push([node, start]);
    }
    /* Lopusta alkuun: jaettu solmu pitää alkunsa, joten aiempien kehotteiden
     * kohdat solmuissa pysyvät oikeina. */
    for (const [from, to] of prompts.reverse()) {
      for (const [node, start] of nodes) {
        const head = Math.max(from - start, 0);
        const tail = Math.min(to - start, node.length);
        if (head >= tail) continue;
        if (tail < node.length) node.splitText(tail);
        const part = head ? node.splitText(head) : node;
        const wrapper = document.createElement("span");
        wrapper.className = "jyu-prompt";
        part.before(wrapper);
        wrapper.append(part);
      }
    }
  };

  /* Sama teksti kuin teeman: näkyvä koodi (innerText). Attribuutti kertoo
   * tyyleille kopioinnin olevan käynnissä (highlights.css, hidelines.css,
   * teeman rivinumerot ja huomautukset). */
  const text = (code) => {
    code.setAttribute("data-md-copying", "");
    const result = code.innerText;
    code.removeAttribute("data-md-copying");
    return code.closest(".language-console")
      ? commands(result.trimEnd()) : result.trimEnd();
  };

  const notify = (nav, message) => {
    let note = nav.querySelector(":scope > .jyu-copied");
    if (!note) {
      note = document.createElement("span");
      note.className = "jyu-copied";
      note.setAttribute("role", "status");
      nav.prepend(note);
    }
    /* Näkyviin ennen tekstiä: role="status" lukee muutoksen ääneen vain
     * näkyvästä elementistä. */
    note.classList.add("jyu-copied--shown");
    note.textContent = message;
    clearTimeout(note.timer);
    note.timer = setTimeout(
      () => note.classList.remove("jyu-copied--shown"), SHOWN_MS);
  };

  const takeOver = (button) => {
    const pre = button.closest("pre");
    const code = pre?.querySelector(":scope > code");
    if (!code) return;
    button.removeAttribute("data-clipboard-target");
    button.addEventListener("click", async () => {
      const nav = button.parentElement;
      try {
        await navigator.clipboard.writeText(text(code));
        notify(nav, "Kopioitu leikepöydälle");
      } catch {
        notify(nav, "Kopiointi ei onnistunut");
      }
    });
  };

  /* Teema tekee napit vasta DOMContentLoaded-tapahtumassa (ks. playground.js:
   * afterTheme). Ilman leikepöytärajapintaa (http muualla kuin localhostissa)
   * napit jäävät teemalle, joka osaa vanhan execCommand-tavan. Kehotteet
   * merkitään silloinkin, koska maalaaminen ei tarvitse rajapintaa. */
  const start = () => {
    document.querySelectorAll(".language-console pre > code")
      .forEach(markPrompts);
    if (!navigator.clipboard?.writeText) return;
    document.querySelectorAll(".md-code__button[data-md-type=copy]")
      .forEach(takeOver);
  };
  if (document.readyState === "loading") {
    addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
