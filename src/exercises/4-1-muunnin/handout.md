1. Luo rajapinta nimeltään `Muunnin`.
Määrittele rajapintaan yksi metodi: `String muunna(String syote)`.
Muista, että rajapinnassa metodilla ei ole runkoa (ei aaltosulkeita `{}`).

2. Tee luokat `PienetKirjaimet`, `IsotKirjaimet` ja `IsoAlkukirjain`, jotka toteuttavat `Muunnin`-rajapinnan.
  * `PienetKirjaimet`-luokan `muunna`-metodi muuntaa annetun merkkijonon pieniksi kirjaimiksi. `muunna("Hei Maa")` --> `"hei maa"`.
  * `IsotKirjaimet`-luokan `muunna`-metodi muuntaa annetun merkkijonon suuraakkosiksi. `muunna("Hei Maa")` --> `"HEI MAA"`.
  * `IsoAlkukirjain`-luokan `muunna`-metodi muuntaa annetun merkkijonon siten,
    että vain ensimmäinen kirjain on suuraakkonen ja muut pieniä. `muunna("HEI MAA")` -->
    `"Hei maa"`.

3. Testaa ohjelmaasi valmiiksi annetulla pääohjelmalla.
