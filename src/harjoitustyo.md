# Harjoitustyö

[Opintojaksoon kuuluu harjoitustyö](./suorittaminen.md), jossa toteutetaan graafinen Java-sovellus.
Alla on kuvattu harjoitustyön vaatimukset. Harjoitustyö toteutetaan vaiheittain
osissa 9-12. Kussakin osassa on annettu ohjeita, joiden tarkoituksena on auttaa
sinua etenemään harjoitustyössä, mutta voit toteuttaa vaatimukset myös muulla
tavalla, kunhan ne täyttyvät.

Kannatta tehdä osissa 7-8 toteutettu mallisovellus ensin valmiiksi. Saat siitä
apua harjoitustyön toteutukseen. 

Viimeistään osan 12 palautuksessa harjoitustyösi tulee täyttää kaikki alla
olevat vaatimukset. 

**Näytä harjoitustyösi ohjaajalle ennen osan 12 palautusta etä- tai
lähiohjauksessa.** Kun ohjaaja on tarkastanut työsi, hän merkitsee
harjoitustyösi hyväksytyksi TIMissä. 

## Vaatimus 1: Tietomalli

1.1 Sovelluksessa on vähintään kaksi kohdealueen mallinnettavaa asiaa. Se voi
    olla esimerkiksi tehtävä (kuten mallisovelluksessa), tapahtuma, kirja,
    asiakas, treeni, peli, resepti tms. Jokaisella mallinnettavalla oliolla on
    omia kohdealueen kannalta merkittäviä attribuutteja/ominaisuuksia. Osien
    7-8 sovelluksessa oli yksi kohdealueen mallinnettava asia, `Tehtava`.
    Muistikorttisovelluksessa ne ovat `Kortti` ja `Korttipakka`. Kulujen
    hallintasovelluksessa ne ovat `Tapahtuma` ja `Kategoria`.
    Kirjastosovelluksessa ne ovat `Kirja` ja `Lainaaja`. Taloyhtiön
    hallintasovelluksessa ne ovat `Asunto` ja `Asukas`. 

1.2 Attribuutti, jonka ainoa tarkoitus on viitata toiseen attribuuttiin, ei ole
    hyväksyttävä mallinnettava asia. Esimerkiksi `Tehtavakokoelma` ei ole
    mallinnettava asia, koska se sisältää vain listan `Tehtava`-olioita, ja
    lisäksi joitain apumetodeja, jotka liittyvät vain `Tehtava`-olioiden
    hallintaan.

1.3 Sovelluksen dataa ei mallinneta käyttöliittymäkomponenteilla, vaan omilla
    malliluokilla.

1.4 Sovelluksessa käytetään JavaFX:n havaittavia rakenteita silloin, kun ne
    liittyvät käyttöliittymän ja datan kytkemiseen. Käytännössä tämä tarkoittaa
    vähintään sitä, että keskeinen tietokokoelma on `ObservableList` tai vastaava
    havaittava rakenne.

1.5 Datan esittämiseen käytetään tarkoituksenmukaista komponenttia. Jos työssä on
  useita samantyyppisiä olioita, `TableView` on yleensä luonteva ratkaisu.

## Vaatimus 2: Perustoiminnallisuus

2.1 Kullekin mallinnetulle oliolle on toteutettava ns. CRUD-toiminnallisuus, eli
    käyttäjä voi luoda, lukea, päivittää ja poistaa olioita käyttöliittymästä.
    Todo-sovelluksessa tämä oli tehty/ei-tehty -tila. 

2.2 Käyttäjän ei saa antaa lisätä ilmeisen virheellistä tietoa, kuten tyhjää
    nimeä tai muuta pakollisen kentän puuttumista. Ts. jonkinlainen validointi
    on toteutettava joko mallissa tai käyttöliittymässä.

2.3 Tietoa päivitettäessä ja poistettaessa sovellukseen ei saa jäädä
    vääriä tietoja, kuten vanhentuneita olioita tai viittauksia.

## Vaatimus 3: Tallennus

3.1 Sovelluksen tiedot tallennetaan tiedostoon, jotta ne säilyvät ohjelman
    sulkemisen jälkeen.

3.2 Tallennetut tiedot ladataan takaisin ohjelman käynnistyessä.

## Vaatimus 4: Käyttöliittymä

4.1 Sovelluksessa on graafinen käyttöliittymä, jossa on vähintään kaksi näkymää.
    Näkymät voivat olla esimerkiksi päänäkymä, jossa käyttäjä näkee kaikki
    oliot, ja muokkausnäkymä (esimerkiksi dialogi), jossa käyttäjä voi muuttaa
    tai lisää olion tietoja.

4.2 Käyttöliittymä on jäsennelty ja käyttökelpoinen: syöttökentät, painikkeet,
    nimiöt ja listaus eivät saa olla sattumanvaraisesti aseteltuja.

4.3 Käyttäjän kannalta keskeiset toiminnot löytyvät päänäkymästä ilman, että
    ohjelmaa pitää käyttää komentorivin kautta.

## Vaatimus 5: Arkkitehtuuri ja vastuunjako

5.1 Sovelluksen rakenteen tulee noudattaa vähintään karkeasti samaa ajatusta
    kuin Todo-sovelluksessa: data, käyttöliittymä ja niitä yhteen kytkevä logiikka
    on erotettu toisistaan.

5.2 Sovelluksen data ja tallennuslogiikka on erotettu käyttöliittymälogiikasta.
    Käyttöliittymä tai sen ohjaaja ei saa sisältää kaikkea sovelluksen dataa ja
    tallennuslogiikkaa itsessään.

5.3 Tiedon lataus ja tallennus on erotettu omaksi vastuukseen pois
    käyttöliittymälogiikasta.

## Vaatimus 6: Testaus

6.1 Sovelluksen keskeiselle mallille tai sovelluslogiikalle on kirjoitettu
    ainakin joitakin yksikkötestejä.

## Vaatimus 7: Versiohallinta

7.1 Työlle on tehty julkinen Git-etävarasto GitLabiin tai GitHubiin.

7.2 Projektissa on vähintään `.gitignore` ja lyhyt `README.md`, jossa kerrotaan,
    mikä sovellus on kyseessä ja miten se käynnistetään.

7.3 Git-commitit on nimetty kuvaavasti, ja niissä on selkeä kuvaus siitä, mitä muutoksia on tehty.
