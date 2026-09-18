/* Testaa tietosi -visa: convert.py:n (convert_quizzes) vaihtoehtolistoista
 * napit. Valinta paljastaa oikean vastauksen ja perustelun ja jää
 * localStorageen ("jyu-visa": kysymyksen data-id -> valittu arvo).
 *
 * Tulostussivun luvut (print.js) jäävät tarkoituksella ilman nappeja:
 * paperilla kysymys on lista ja perustelu <details>. */

(() => {
  "use strict";

  const KEY = "jyu-visa";
  const RESULT = { oikein: "Oikein!", vaarin: "Väärin" };

  /* localStorage voi puuttua (yksityinen tila); silloin vastaus elää vain sivulla. */
  const stored = () => {
    try {
      const answers = JSON.parse(localStorage.getItem(KEY));
      return answers && typeof answers === "object" && !Array.isArray(answers) ? answers : {};
    } catch {
      return {};
    }
  };
  const store = (answers) => {
    try {
      localStorage.setItem(KEY, JSON.stringify(answers));
    } catch {
      /* ei tallennusta */
    }
  };

  const options = (question) => [...question.querySelectorAll(".jyu-visa-vaihtoehdot > li")];

  const reveal = (question, value) => {
    const correct = question.dataset.vastaus;
    question.dataset.vastattu = value;
    for (const option of options(question)) {
      const chosen = option.dataset.arvo === value;
      option.classList.toggle("jyu-visa-valittu", chosen);
      option.classList.toggle("jyu-visa-oikea", option.dataset.arvo === correct);
      const button = option.querySelector(".jyu-visa-nappi");
      button.setAttribute("aria-disabled", "true");
      button.setAttribute("aria-pressed", String(chosen));
    }
    const details = question.querySelector(":scope > details");
    if (!details) return;
    details.dataset.tulos = value === correct ? "oikein" : "vaarin";
    details.querySelector("summary").textContent = RESULT[details.dataset.tulos];
    details.open = true;
  };

  const reset = (question, summary) => {
    delete question.dataset.vastattu;
    for (const option of options(question)) {
      option.classList.remove("jyu-visa-valittu", "jyu-visa-oikea");
      const button = option.querySelector(".jyu-visa-nappi");
      button.removeAttribute("aria-disabled");
      button.removeAttribute("aria-pressed");
    }
    const details = question.querySelector(":scope > details");
    if (!details) return;
    delete details.dataset.tulos;
    details.querySelector("summary").textContent = summary;
    details.open = false;
  };

  const enhance = (visa) => {
    const questions = [...visa.querySelectorAll(".jyu-visa-q")];
    const summaries = new Map(questions.map((question) => [
      question, question.querySelector(":scope > details > summary")?.textContent ?? ""]));

    const clear = document.createElement("p");
    clear.className = "jyu-visa-nollaus";
    const clearButton = document.createElement("button");
    clearButton.type = "button";
    clearButton.textContent = "Tyhjennä vastaukset";
    clear.append(clearButton);
    const showClear = () => {
      clear.hidden = !questions.some((question) => question.dataset.vastattu);
    };
    clearButton.addEventListener("click", () => {
      const answers = stored();
      for (const question of questions) {
        delete answers[question.dataset.id];
        reset(question, summaries.get(question));
      }
      store(answers);
      showClear();
    });

    const answers = stored();
    for (const question of questions) {
      for (const option of options(question)) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "jyu-visa-nappi";
        /* Teksti yhteen spaniin: muuten jokainen koodinpätkä olisi oma flex-kohteensa. */
        const text = document.createElement("span");
        text.append(...option.childNodes);
        button.append(text);
        option.append(button);
        button.addEventListener("click", () => {
          if (question.dataset.vastattu) return;
          reveal(question, option.dataset.arvo);
          store({ ...stored(), [question.dataset.id]: option.dataset.arvo });
          showClear();
        });
      }
      const saved = answers[question.dataset.id];
      if (options(question).some((option) => option.dataset.arvo === saved)) {
        reveal(question, saved);
      }
    }
    visa.append(clear);
    visa.classList.add("jyu-visa-js");
    showClear();
  };

  for (const visa of document.querySelectorAll(".jyu-visa")) enhance(visa);
})();
