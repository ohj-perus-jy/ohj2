/* Sisällysluettelon sulkeminen kapealla näytöllä. Alle 960 px:n leveydellä
 * Zensical piirtää sisällysluettelon alakulman napista avautuvaksi laatikoksi,
 * ja avaus on pelkkää CSS:ää: nappi on <label>, joka rastittaa piilotetun
 * #__toc-valintaruudun, ja laatikko näkyy ruudun ollessa rastittuna. Kohdan
 * napautus vie otsikkoon, mutta mikään ei poista rastia, joten laatikko jää
 * peittämään juuri avattua tekstiä; myöskään laatikon ulkopuolen napautus ei
 * sulje sitä. Tässä rasti poistetaan molemmissa. Työpöydällä ruutua ei ole
 * rastittu, joten tämä ei tee mitään. */

(() => {
  const toggle = document.getElementById("__toc")
  const sidebar = document.querySelector(".md-sidebar--secondary")
  if (!toggle || !sidebar)
    return

  /* Yksi kuuntelija koko sivulle. Sivupalkin sisällä (nappi, laatikko)
   * suljetaan vain linkin napautuksesta, jotta vierityspalkin tai listan
   * reunan kosketus ei sulje; napin ja laatikon otsikon <label>it vaihtavat
   * rastin itse. Kaikki muu sivulla on ulkopuolta. */
  document.addEventListener("click", event => {
    if (!toggle.checked)
      return
    const inside = sidebar.contains(event.target)
    if (!inside || event.target.closest("a.md-nav__link"))
      toggle.checked = false
  })
})()

/* Sisällysluettelon häivytys sivupalkissa (layout.css): data-jyu-above, kun
 * listaa on vieritetty, ja data-jyu-below, kun listaa on alempana. Yläreunan
 * häivytys tulee sticky-otsikon alle, joten sen korkeus annetaan muuttujana.
 * Tila päivittyy vierittäessä, myös kun luettelo seuraa lukukohtaa
 * (toc.follow), ja kun teema muuttaa vieritysalueen korkeutta ikkunan mukaan
 * tai lista muuttaa korkeuttaan (kirjasimen lataus). Puolipiste alussa,
 * koska muuten lohko jäsentyisi kutsuksi edellisen lohkon tulokselle. */
;(() => {
  const wrap = document.querySelector(".md-sidebar--secondary .md-sidebar__scrollwrap")
  if (!wrap)
    return
  const title = wrap.querySelector(".md-nav__title")

  const update = () => {
    wrap.style.setProperty("--jyu-toc-title", `${title ? title.offsetHeight : 0}px`)
    wrap.toggleAttribute("data-jyu-above", wrap.scrollTop > 1)
    wrap.toggleAttribute("data-jyu-below",
      wrap.scrollTop + wrap.clientHeight < wrap.scrollHeight - 1)
  }

  wrap.addEventListener("scroll", update, { passive: true })
  const observer = new ResizeObserver(update)
  observer.observe(wrap)
  if (wrap.firstElementChild)
    observer.observe(wrap.firstElementChild)
  update()
})()
