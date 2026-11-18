/* Teeman vaihto häivyttäen. Zensicalin yläpalkin nappi (partials/palette.html:
 * label -> radio __palette_N) vaihtaa bodyn data-md-color-*-attribuutit
 * change-tapahtumassa, ja värit hyppäävät kerralla. Vaihto ajetaan selaimen
 * näkymäsiirtymänä (document.startViewTransition): selain ottaa vanhasta
 * näkymästä kuvan ja häivyttää sen uuden päältä, jolloin tausta, teksti,
 * koodi, kuvat ja avoin hakuikkuna vaihtuvat samaan tahtiin. Kesto on
 * layout.css:ssä (::view-transition-old/new(root)).
 *
 * Kaappaus radion click-tapahtumassa kaappausvaiheessa, jotta se osuu sekä
 * napin painallukseen (label välittää clickin radiolle) että Zensicalin
 * Enter-näppäimeen (bundle.js kutsuu radion click()). Oma uusintaklikkaus
 * siirtymän sisällä merkitään lipulla, ettei se kaappaudu uudestaan.
 *
 * Käyttöjärjestelmän teeman vaihtuminen ja tulostus (print.js) vaihtavat
 * attribuutin suoraan eivätkä kulje tästä: ei häivytystä. Vähemmän liikettä
 * pyytävälle ja ilman rajapintaa vaihto on välitön kuten Zensicalilla. */

(() => {
  "use strict";

  const form = document.querySelector("form[data-md-component=palette]");
  if (!form || !document.startViewTransition) return;

  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  let replaying = false;

  form.addEventListener("click", (event) => {
    const input = event.target;
    if (replaying || reduced.matches ||
        !(input instanceof HTMLInputElement) || input.type !== "radio") return;
    event.preventDefault();
    document.startViewTransition(() => {
      replaying = true;
      try {
        input.click();
      } finally {
        replaying = false;
      }
    });
  }, true);
})();
