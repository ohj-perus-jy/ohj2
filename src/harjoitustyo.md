# Harjoitustyö

[Opintojaksoon kuuluu harjoitustyö](./suorittaminen.md), jossa toteutat
graafisen Java-käyttöliittymäsovelluksen käyttäen JavaFX-kirjastoa. 
Löydät alta harjoitustyön tarkat arvioitavat vaatimukset.

Voit tehdä harjoitustyön joko valmiin vaatimusmäärittelyn perusteella tai
keksiä oman aiheen. Löydät kaikki aiheiden kuvaukset ja vaatimukset
[osassa 9](osa9/01-harjoitustyo.md).

Harjoitustyö toteutetaan vaiheittain osissa 9–12. 
Jokainen osa sisältää ohjeita, joiden tarkoituksena on auttaa sinua etenemään, mutta voit
toteuttaa vaatimukset myös muulla varten, kunhan ne täyttyvät.

Suosittelemme, että ennen harjoitustyön tekemistä tutustut ja teet osien 7 ja 8
mallisovellukset. Saat siitä merkittävästi apua harjoitustyön toteutukseen.

**Näytä lopullinen, kaikkia vaatimuksia täyttävä harjoitustyösi kurssin
tuntiopettajalle
ennen osan 12 palautusta etä- tai lähiohjauksessa.** Kun tuntiopettaja on
hyväksynyt työsi, hän tekee siitä merkinnän TIMissä.

## Harjoitustyön tekniset vaatimukset ja arviointi

Alla olevia vaatimuksia käytetään harjoitustyön arvioinnissa.
Tuntiopettaja arvioi harjoitustyön asteikolla hylätty/hyväksytty. 
Hylätyn harjoitustyön voi täydentää tuntiopettajan antaman palautteen
perusteella.

Lähtökohtaisesti työn on täytettävä kaikki alla olevat vaatimukset.
Yksittäisten vaatimusten kohdalla voidaan joustaa, mikäli työ on muilta osin
tavanomaista laajempi tai ansiokkaampi, tai jos työn aihe sitä vaatii.
Tuntiopettaja tekee lopullisen arvion työn hyväksymisestä tapauskohtaisesti.

### Vaatimus 1: Tietomalli

**1.1 Sovelluksessa on vähintään kaksi kohdealueen mallinnettavaa asiaa.**  
Se voi olla esimerkiksi tehtävä, tapahtuma, kirja, asiakas, treeni, peli,
resepti tai vastaava. Jokaisella mallinnettavalla oliolla on omia kohdealueen
kannalta merkittäviä attribuutteja tai ominaisuuksia.
Osien 7–8 mallisovelluksessa oli yksi mallinnettava asia: `Tehtava`.
Puolestaan muistikorttisovelluksessa ne voisivat olla `Kortti` ja `Korttipakka`.
Kulujen hallintasovelluksessa taas sopivat mallinnettavat asiat olisivat
`Tapahtuma` ja `Kategoria`.

**1.2 Jokaisella kohdealuetta mallinnettavalla asialla on oltava vähintään yksi
kohdealueen kannalta oleellinen ja asialle ominainen attribuutti.**
Osien 7–8 mallisovelluksessa `Tehtava`-luokka sisälsi attribuutit `tehty`,
`otsikko`, `kuvaus` ja `prioriteetti`.

Huomaa, että *attribuutti, jonka ainoa tarkoitus on viitata toiseen
malliin tai jonka arvo on johdettavissa jonkun toisen attribuutin arvosta*
ei lasketa tähän vaatimukseen mukaan.
Esimerkiksi osan 7–8 mallisovelluksen
`Tehtavakokoelma`-luokka sisältää ainoana attribuuttina `tehtavat`-kokoelman,
joka on vain kokoelma viitteitä tehtäviin, ja siten sitä ei laskettaisi tähän
vaatimukseen mukaan.
Sen sijaan muistikorttisovelluksessa `Korttipakka` sisältää korttikokoelman
lisäksi korttipakan otsikon ja kuvauksen, jotka lasketaan sovelluksen kannalta
oleellisiksi ja korttipakalle ominaisiksi.

**1.3 Sovelluksen dataa ei mallinneta käyttöliittymäkomponenteilla, vaan omilla
malliluokilla.**

**1.4 Sovelluksessa käytetään JavaFX:n havaittavia (observable) rakenteita silloin, kun ne liittyvät käyttöliittymän ja datan kytkemiseen.**  
Vähintään keskeisen tietokokoelman tulee olla `ObservableList` tai vastaava.

**1.5 Datan esittämiseen käyttöliittymässä käytetään tarkoituksenmukaista komponenttia.**  
Jos työssä on useita samantyyppisiä olioita, `TableView` on yleensä luonteva rataisu.

### Vaatimus 2: Perustoiminnallisuus

**2.1 Kullekin mallinnetulle oliolle on toteutettava CRUD-toiminnallisuus käyttöliittymässä.**  
Käyttäjä voi luoda (*Create*), lukea (*Read*), päivittää (*Update*) ja poistaa
(*Delete*) olioita käyttöliittymän kautta. Esimerkiksi osan 7–8
mallisovelluksessa käyttäjä voi luoda tehtäviä
painikkeella, lukea ne `TableView`-komponentista, muokata tehtäviä erillisessä
näkymässä ja poistaa ne
poistopainikkeella.

**2.2 Käyttäjän ei saa antaa lisätä ilmeisen virheellistä tietoa.**  
Esimerkiksi tyhjää nimeä tai pakollisen kentän puuttumista ei tule sallia. Validointi on toteutettava joko mallissa tai käyttöliittymässä.

**2.3 Käyttöliittymän tila vastaa aina mallin tilaa ja päinvastoin.**  
Tietoa päivitettäessä tai poistettaessa malliin tai käyttöliittymään ei saa jäädä väärää tietoa. Olion poistaminen mallista poistaa sen välittömästi myös näkyvistä.

### Vaatimus 3: Tallennus

**3.1 Sovelluksen tiedot tallennetaan tiedostoon.**  
Tiedot säilyvät ohjelman sulkemisen jälkeen. Tallennus voi tapahtua automaattisesti tai erillisenä "Tallenna"-toimintona.

**3.2 Tallennetut tiedot ladataan takaisin ohjelman käynnistyessä.**

### Vaatimus 4: Käyttöliittymä

**4.1 Sovelluksessa on graafinen käyttöliittymä, jossa on vähintään kaksi näkymää.**  
Näkymät voivat olla esimerkiksi päänäkymä (listaus) ja muokkausnäkymä (dialogi).

**4.2 Käyttöliittymä on jäsennelty ja käyttökelpoinen.**  
Syöttökentät, painikkeet, nimiöt ja listaukset on aseteltu loogisesti, eivätkä ne ole sattumanvaraisia.

### Vaatimus 5: Arkkitehtuuri ja vastuunjako

**5.1 Sovelluksen rakenne noudattaa MVC-mallia (Model-View-Controller).**  
Tietomalli, käyttöliittymä ja niitä yhteen kytkevä ohjainlogiikka on erotettu toisistaan.

**5.2 Sovelluksen data ja tallennuslogiikka on erotettu ohjainluokasta.**  
Käyttöliittymän ohjain ei saa sisältää kaikkea sovelluksen dataa ja tallennuslogiikkaa.

**5.3 Tiedon lataus ja tallennus on erotettu omaksi vastuualueekseen.**

### Vaatimus 6: Testaus

**6.1 Sovelluksen keskeiselle mallille tai sovelluslogiikalle on kirjoitettu yksikkötestejä.**  
Testeissä on varmistettava, että keskeiset metodit (kuten lisääminen ja poistaminen) muokkaavat tietomallin tilaa odotetusti.

### Vaatimus 7: Versiohallinta ja projektinhallinta

**7.1 Työlle on luotu julkinen Git-etävarasto (esim. GitLab tai GitHub).**

**7.2 Projektissa on `.gitignore`-tiedosto ja `README.md`.**  
README-tiedostossa kerrotaan lyhyesti, mikä sovellus on kyseessä ja miten se toimii.

**7.3 Git-commitit on nimetty kuvaavasti.**  
Commiteista käy ilmi, mitä muutoksia kukin niistä sisältää.

**7.4 Työtä on edistetty iteratiivisesti tallentaen iteraatioiden tulokset omina
committeina.**  
Etävarastossa ei saa olla vain yhtä "valmis sovellus" -committia, vaan kehityshistorian tulee näkyä.
