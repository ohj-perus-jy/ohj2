# JavaFX osa 2, MVC

> [!VAROITUS]
> Tämä osa julkaistaan 2. maaliskuuta 2026. {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Osaat erottaa datan, sovelluslogiikan ja käyttöliittymän toisistaan
>   JavaFX-projektissa.
> - Osaat käyttää JavaFX:n `Observable`-rajapintaan perustuvia tyyppejä niin,
>   että käyttöliittymä päivittyy automaattisesti datan mukana.
> - Osaat esittää tehtävädatan `TableView`-komponentissa ja hyödyntää
>   databindingia.
> - Osaat tehdä tehtävien muokkausnäkymän, jossa on validointi ja
>   priorisointitieto.
> - Osaat kirjoittaa yksikkötestejä Todo-sovelluksen mallille ja
>   sovelluslogiikalle.
> - Harjoitustyön vaihe 2 palautus TIMiin (ei tarvitse erikseen näyttää
>   tuntiopettajalle).

Osassa 7 teimme toimivan Todo-sovelluksen, jossa tehtävät mallinnettiin pitkälti
käyttöliittymäkomponenteilla (`CheckBox`) ja tallennettiin JSON-tiedostoon.

Ratkaisu oli sinänsä hyvä aloitus, mutta pidemmällä aikavälillä se tekee
sovelluksesta jäykän. Esimerkiksi jos haluamme lisätä tehtäville uusia
ominaisuuksia, kuten pidemmän kuvauksen tai vaikkapa prioriteetin, meidän
pitäisi lisätä uusia komponentteja, kuten `TehtavaCheckBox`-komponentti.
Edelleen jos haluaisimme muokata tehtävän dataa lomakkeena, joutuisimme tekemään
oman `TehtavaForm`-komponentin. Silloin taas on epäselvää, kumpi datan
esitysmuodoista on "oikea": pitääkö `TehtavaCheckBox`-tehtävän tiedot siirtää
aina `TehtavaForm`-tehtäviin vai toisinpäin? 

Oliopohjaista suunnittelua mukaillen *kohdealueen ydintoiminta ja sen
esittäminen käyttäjälle ovat kaksi erillistä vastuuta*. Todo-sovelluksen
tehtävien tiedot ja niiden hallinta olisi parasta mallintaa omana
kokonaisuutena. Puolestaan käyttöliittymän ainoa vastuu tulisi olla esittää
kohdealueen data. Valintaruudut eivät itsessään ole tehtävä, vaan vain tapa
esittää niitä.

Tässä osassa jatkamme osan 7 Todo-sovelluksen työstämistä.
Keskitymme nyt sovelluksen käyttöliittymän ja ydintoiminnan
erottamiseen. Lopuksi katsomme, miten tämä erottaminen mahdollistaa
ydintoiminnan oikeellisuuden varmistamista automaattisilla testeilla.

JavaFX tarjoaa aputyökaluja, jolla käyttöliittymä ja ydinlogiikka voidaan pitää
ns. "löyhästi sidottuna". Tässä osassa:

- Siirrämme kaikki tehtävien tiedot `Tehtava`-luokkaan ja mallinnamme tehtävät `ObservableList`-kokoelmalla.
- Käytämme `TableView`-näkymää tehtävien datan esittämiseen.
- Jäsennämme sovelluksen luokat MVC-arkkitehtuurin mukaisesti kolmeen vastuualueeseen.
- Lisäämme tehtävän muokkausikkunan, jossa voi muokata kuvausta, prioriteettia
  ja määräpäivää.
- Varmistamme ratkaisun toimivuutta yksikkötesteillä.
- Julkaisemme valmiin projektimme GitLab- tai GitHub-etävarastopalvelussa.
