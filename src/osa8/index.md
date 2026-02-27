# JavaFX osa 2, MVC

> [!VAROITUS]
> Tämä osio julkaistaan 2. maaliskuuta 2026. {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Osaat erottaa datan, sovelluslogiikan ja käyttöliittymän toisistaan
>   JavaFX-projektissa.
> - Osaat käyttää JavaFX:n `Observable`-rajapintoja ja kokoelmia niin, että
>   käyttöliittymä päivittyy automaattisesti datan mukana.
> - Osaat esittää tehtävädatan `TableView`-komponentissa ja hyödyntää
>   databindingia.
> - Osaat tehdä tehtävien muokkausnäkymän, jossa on validointi ja
>   priorisointitieto.
> - Osaat kirjoittaa yksikkötestejä TODO-sovelluksen mallille ja
>   sovelluslogiikalle.
> - Harjoitustyön vaihe 2 palautus TIMiin (ei tarvitse erikseen näyttää
>   tuntiopettajalle).

Osassa 7 teimme toimivan TODO-sovelluksen, jossa tehtävät mallinnettiin pitkälti
käyttöliittymäkomponenteilla (`CheckBox`) ja tallennettiin JSON-tiedostoon.
Ratkaisu toimii, mutta nyt sovelluksen ydinlogiikka ja käyttöliittymmä
ovat erittäin tiukasti sidottuna toisiinsa.
Esimerkiksi tehtävän tila mallinetaan suoraan
`CheckBox`-käyttöliittymäkomponentilla, joka ei ole sovelluksen kohdealueen 
kannalta ydinkäsite. Sovelluksen tarkoituksena onkin hallita tehtäviä eikä
valintaruutuja; käyttöliittymän on oltava vain tapa *esittää* data.

Sovelluksen ydintoiminnan ja käyttöliittymän tiukka sidonta kostautuu myös, kun
sovellusta halutaan laajentaa. Jos haluaisimme jatkossa tallentaa lisäksi
vaikkapa tehtävien tarkempia kuvauksia, prioriteettitasoa tai vaikkapa mallintaa
tehtävien alitehtäviä, käyttöliittymäkomponenttien käyttämien sekä tilan
esittämiseen että käsittelyyn monimutkaistaa koodia. Kun esityslogiikan ja
sovelluksen ydinlogiikan eroa on vaikeaa nähdä, muutosten tekeminen
jompaankumpaan muuttuu hankalaksi.




- Uusien ominaisuuksien lisääminen kasvattaa kontrolleria nopeasti liian
  suureksi.

Tässä osassa refaktoroimme sovelluksen rakennetta ja jatkamme sitä eteenpäin:

- Siirrämme tehtävädatan omaan malliin ja käytämme `ObservableList`-kokoelmaa.
- Jäsennämme sovelluksen MVC-arkkitehtuurin mukaisesti selkeisiin kerroksiin.
- Vaihdamme näkymän `TableView`-pohjaiseksi.
- Lisäämme tehtävän muokkausikkunan, jossa voi muokata kuvausta, prioriteettia
  ja määräpäivää.
- Varmistamme ratkaisun toimivuutta yksikkötesteillä.

Nämä muutokset valmistavat suoraan harjoitustyön toiseen vaiheeseen.

- [Malli ja Observable-rajapinta](./01-malli-ja-observable-rajapinta.md)
- [TableView ja databinding](./02-tableview.md)
- [MVC-arkkitehtuuri](./03-mvc-arkkitehtuuri.md)
- [Useita näkymiä ja tehtävän muokkaus](./04-useita-nakymia.md)
- [Yksikkötestaus](./05-yksikkotestaus.md)
- [Versionhallinnan etäkäyttö (Git)](./06-versionhallinnan-etakaytto.md)
- [Tehtävät](./07-tehtavat.md)
