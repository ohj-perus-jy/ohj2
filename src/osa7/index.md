# JavaFX osa 1, SceneBuilder

> [!VAROITUS]
> Tämä osa julkaistaan 23. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
> - Osaat tehdä JavaFX-projektin
> - Ymmärrät käyttöliittymän luomisen periaatteet SceneBuilderia käyttäen
> - Osaat tehdä lomakkeen, jossa kysytään käyttäjältä tietoa, tallennetaan tieto
>   (in-memory), ja esitetään syötetty tieto käyttäjälle käyttöliittymässä.
> - Osaat luoda projektillesi paikallisen Git-varaston sopivilla asetuksilla, ja
>   tehdä varastoon committeja


Olemme tähän mennessä toteuttaneet ohjelmia, jotka toimivat tekstipohjaisessa
komentoriviympäristössä. Tässä osassa otamme askeleen kohti visuaalisempia
sovelluksia ja tutustumme **JavaFX**-kirjastoon, jonka avulla rakennamme
graafisia käyttöliittymiä.

Käytämme **SceneBuilder**-työkalua käyttöliittymän visuaaliseen suunnitteluun.
Samalla otamme käyttöön **versionhallinnan (Git)**, joka auttaa meitä hallitsemaan
projektin koodia ja valmistautumaan harjoitustyön ensimmäiseen vaiheeseen.

Osien 7 ja 8 aikana rakennamme yksinkertaisen TODO-sovelluksen. Tähän osioon
kuuluu tehtäviä, joissa opit tekemään saman sovelluksen omatoimisesti. Nämä osat
antavat sinulle tarvittavan ymmärryksen JavaFX:stä, jotta voit luoda oman
harjoitustyön osien 9-11 aikana. 

Osassa 7 teemme sovellukseen seuraavat ominaisuudet:

 * Käyttäjä voi lisätä uuden tehtävän
 * Käyttäjä näkee listan kaikista tehtävistä
 * Käyttäjä voi merkitä tehtävän tehdyksi
 * Käyttäjä voi poistaa tehtävän
 * Käyttäjä voi palauttaa tehdyn tehtävän takaisin tekemättömäksi
 * Tehtävät tallennetaan tiedostoon, jotta ne säilyvät sovelluksen sulkemisen jälkeen
 * Tehtävät haetaan tiedostosta sovelluksen käynnistyessä

Tämän osan lopuksi sovelluksemme toimii seuraavasti:

<video src="images/todo-app-final-product.mp4" controls></video>

Kuten aiemminkin, tämänkin osan tehtävistä täytyy tehdä vähintään 50%.
Erityisesti osissa 7 ja 8 kuitenkin suosittelemme tekemään kaikki tehtävät
jotta harjoitustyön tekeminen olisi helpompaa. Bonustehtävät jäävät kuitenkin
edelleen vapaavalintaisiksi. 