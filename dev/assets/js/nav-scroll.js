/* Valikon vieritys, kun luku avataan. Alalukujen avaaminen on Zensicalissa
 * pelkkää CSS:ää (nuolen <label> rastittaa piilotetun valintaruudun), joten
 * listan alapäässä alaluvut avautuvat näkyvän alueen alapuolelle eikä mikään
 * vieritä kiskoa. Teema vierittää aktiivisen kohdan näkyviin vain sivun
 * latautuessa. */

(() => {
  const rail = document.querySelector(
    ".md-sidebar--primary .md-sidebar__scrollwrap")
  if (!rail)
    return

  /* Vieritetään niin, että avatun luvun alalaita tulee näkyviin ja alle jää
   * sama ilma kuin listan alareunaan (layout.css). Enintään kuitenkin niin,
   * että luvun oma rivi jää kiskon yläreunaan: tärkeämpää on nähdä, mikä luku
   * avattiin, kuin kaikki sen alaluvut. */
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

    /* Vieritys vasta kun luku on auennut: selain rajaa vierityksen käskyhetken
     * vieritysvaraan, ja aukeaminen on animoitu (grid-template-rows). Kesto
     * luetaan teemasta, koska Material poistaa siirtymät, kun käyttäjä on
     * pyytänyt vähemmän liikettä; silloin transitionend ei tule lainkaan. */
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
