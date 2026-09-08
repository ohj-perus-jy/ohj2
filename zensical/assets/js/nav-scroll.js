/* Valikon vieritys, kun luku avataan.
 *
 * Alalukujen avaaminen on Zensicalissa pelkkää CSS:ää: nuoli on <label>,
 * joka rastittaa piilotetun valintaruudun, ja rastitettu ruutu näyttää
 * sisarenaan olevan alaluettelon. Mikään ei siis vieritä kiskoa. Listan
 * alapäässä se tarkoittaa, että alaluvut avautuvat kokonaan näkyvän alueen
 * alapuolelle: nuoli kääntyy, mutta ruudulla ei tapahdu mitään. Mitattu
 * 1440 x 900: kun viimeinen luku ("13 JavaFX-ohjeita") avataan lista pohjaan
 * asti vieritettynä, kaikki kuusi alalukua jäävät kiskon alareunan (900 px)
 * alapuolelle, alimmillaan 1114 px:ään.
 *
 * Zensical vierittää kyllä itse aktiivisen kohdan näkyviin — mutta vain
 * sivun latautuessa (sidebar-komponentti keskittää .md-nav__link--active
 * vieritysalueeseen). Avaamiseen se ei reagoi mitenkään: nuolen <label>-
 * käsittelijä päivittää vain aria-expandedin.
 *
 * Tämä on branchin ensimmäinen oma JavaScript. CSS:llä tätä ei voi tehdä:
 * vieritys on tapahtuma, ei tyyli.
 */

(() => {
  const rail = document.querySelector(
    ".md-sidebar--primary .md-sidebar__scrollwrap")
  if (!rail)
    return

  /* Vieritetään sen verran, että avatun luvun alalaita tulee näkyviin, ja
   * alalaidan alle jätetään sama ilma kuin listan alareunaan (layout.css),
   * jottei viimeinen alaluku jää kiinni ruudun reunaan.
   *
   * Enintään kuitenkin sen verran, että luvun oma rivi jää kiskon
   * yläreunaan. Alalukuja voi olla enemmän kuin kiskoon mahtuu, ja silloin
   * on tärkeämpää nähdä mikä luku avattiin kuin nähdä kaikki sen alaluvut. */
  const reveal = (item, behavior) => {
    const railBox = rail.getBoundingClientRect()
    const itemBox = item.getBoundingClientRect()
    const gap = parseFloat(getComputedStyle(
      rail.querySelector(".md-nav--primary > .md-nav__list")).paddingBottom)

    const hidden = itemBox.bottom + gap - railBox.bottom
    if (hidden > 0)
      rail.scrollBy({
        top: Math.min(hidden, itemBox.top - railBox.top),
        behavior
      })
  }

  /* Yksi kuuntelija kiskolle, ei jokaiselle valintaruudulle erikseen. */
  rail.addEventListener("change", event => {
    const toggle = event.target
    if (!toggle.classList.contains("md-nav__toggle") || !toggle.checked)
      return

    const item = toggle.parentElement
    const nested = item.querySelector(
      ":scope > .md-nav:not(.md-nav--secondary)")
    if (!nested)
      return

    /* Vieritys vasta kun luku on auennut. Selain rajaa vierityksen siihen
     * vieritysvaraan, joka on olemassa käskyn hetkellä, ja aukeaminen on
     * animoitu (grid-template-rows: 0fr -> 1fr, 0,25 s) — vara siis syntyy
     * vasta jälkikäteen. Mitattu: heti muutostapahtumassa annettu scrollBy
     * jättää vierityksen alkuunsa (27 px), koska vara kasvaa 27 -> 267 px
     * vasta seuraavan 0,25 s aikana.
     *
     * Ehto luetaan teemasta eikä käyttäjän asetuksesta: Material katkaisee
     * kaikki siirtymät, kun käyttäjä on pyytänyt vähemmän liikettä
     * (* { transition: none }). Silloin luku on jo auki eikä
     * transitionend-tapahtumaa tule lainkaan, joten myös vieritys tehdään
     * kerralla. */
    if (parseFloat(getComputedStyle(nested).transitionDuration) === 0) {
      reveal(item, "auto")
      return
    }

    /* Nimenomaan grid-template-rows: samalla elementillä on myös 0 s
     * visibility-siirtymä, joka päättyy heti, ja lapsilla omansa. */
    nested.addEventListener("transitionend", function opened(end) {
      if (end.target !== nested || end.propertyName !== "grid-template-rows")
        return
      nested.removeEventListener("transitionend", opened)
      if (toggle.checked)
        reveal(item, "smooth")
    })
  })
})()
