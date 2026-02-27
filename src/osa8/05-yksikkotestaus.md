# Yksikkötestaus

Nyt kun olemme siirtyneet MVC-arkkitehtuuriin ja luoneet
`Tehtavakokoelma`-luokan, olemme saavuttaneet jotain erittäin tärkeää: olemme
erottaneet käyttöliittymän kokonaan irti sovelluksen logiikasta ja datasta.

Tällä on ratkaiseva ohjelmistotuotannollinen hyöty. Jos yrittäisimme testata
koodia käyttöliittymän kautta (esim. simuloimalla napin painalluksia), testaus
olisi hidasta, altista satunnaisille virheille ja vaatisi raskaiden
JavaFX-kirjastojen käynnistämisen. Koska kokoelmalla on nyt selkeä
ohjelmointirajapinta (metodit `lisaaTehtava`, `poistaTehtava` jne.), voimme
rakentaa **yksikkötestejä**, jotka kutsuvat suoraan kokoelmaa ja tarkistavat
asioiden toimiutuvuuden millisekunneissa ilman ruudulle aukeavia ikkunoita.

Tässä luvussa opimme myös, miksi erillinen `TehtavaRepository`-rajapinta
I/O-operaatioiden takana on testattavuudelle kultaa.

## Tiedostojen ja I/O:n abstrahointi testeissä

Mietitäänpä tilannetta, jossa lähtisimme testaamaan `Tehtavakokoelma`-luokkaa.
Mitä tapahtuu, jos kutsumme vahingossa kokoelmaa siten, että se tallentaa dataa
kovalevylle samalla kun ohjelman varsinainen käyttäjä muokkaa omia tehtäviään?
Tai mitä jos testisovellus jättää jälkeensä roskatiedostoja aina kun testit
ajetaan? Tiedosto-operaatiot (I/O) testeissä ovat yleensä pahasta: ne tekevät
testeistä hitaita ja vaikeasti hallittavia.

Siksi loimme arkkitehtuuriluvussa `TehtavaRepository`-rajapinnan.

Testejä varten voimme luoda luokan (ns. _Mock_- tai _Fake_-luokan), joka
**teeskentelee** tallentavansa tietoja tiedostoon, mutta todellisuudessa
tallentaakin ne vain normaaliin Java-listaan keskusmuistissa (In-Memory). Koska
`Tehtavakokoelma` puhuttelee vain rajapintaa, se ei edes tiedä juttelevansa
testiluokalle!

Luodaan ensin tämä _vale-säilö_ samaan pakettiin, mihin yksikkötestit myöhemmin
kirjoitetaan (normaalisti src/test/java...-kansion alle):

```java
public class MockTehtavaRepository implements TehtavaRepository {

    // Keskusmuistissa oleva data "tiedoston" sijaan
    private List<TehtavaDto> tallennetutData = new ArrayList<>();

    @Override
    public List<TehtavaDto> lataa() {
        return tallennetutData; // Palautetaan vain lista muistista
    }

    @Override
    public void tallenna(List<TehtavaDto> tehtavat) {
        // Kun kokoelma yrittää "tallentaa" levylle, kopioidaankin data vain tähän listaan!
        this.tallennetutData = new ArrayList<>(tehtavat);
    }
    
    // Testejä varten apumetodi asioiden todentamiseen
    public List<TehtavaDto> haeTallennetut() {
        return this.tallennetutData;
    }
}
```

## Tehtavakokoelman testaaminen JUnit 5:llä

Nyt voimme turvallisin mielin testata mallia. JUnit 5 -testiluokan runko voisi
näyttää tältä:

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TehtavakokoelmaTest {

    @Test
    void lisaaTehtava_lisaaTehtavanJaTallentaaSen() {
        // 1. Arrange: Valmistellaan testidata ja testattava luokka.
        // SYÖTETÄÄN VALE-SÄILÖ!
        MockTehtavaRepository mockRepo = new MockTehtavaRepository();
        Tehtavakokoelma malli = new Tehtavakokoelma(mockRepo);
        
        // 2. Act: Kutsutaan sitä metodia, jota testataan
        malli.lisaaTehtava("Käy kaupassa");
        
        // 3. Assert: Tarkistetaan, että lopputulos on toivottu
        assertEquals(1, malli.getTehtavat().size(), "Listassa pitäisi olla 1 tehtävä.");
        assertEquals("Käy kaupassa", malli.getTehtavat().get(0).getOtsikko(), "Otsikon pitäisi täsmätä");
        
        // Varmistetaan mock-luokan avulla, että kokoelma muisti myös PYYTÄÄ TALLENNUSTA repositorylta!
        assertEquals(1, mockRepo.haeTallennetut().size(), "Data olisi pitänyt tallentaa rajapinnan läpi!");
    }

    @Test
    void lisaaTehtava_eiLisaaTyhjaaOtsikkoa() {
        MockTehtavaRepository mockRepo = new MockTehtavaRepository();
        Tehtavakokoelma malli = new Tehtavakokoelma(mockRepo);
        
        malli.lisaaTehtava("   "); // Tyhjä syöte
        
        assertEquals(0, malli.getTehtavat().size(), "Tyhjiä tehtäviä ei saa lisätä listaan.");
    }
}
```

Huomaa kuinka vähän yllä oleva testi tekee töitä saavuttaakseen lähes laajan
peiton! Ensimmäinen testi paitsi validoi itse lisäämisen onnistumisen
ominaisuuksineen, myös todentaa epäsuorasti, että malliluokkamme todella osaa
tallentaa datan (koska se valui alaspäin `mockRepo`-luokan listaan). Tämä on
uskomattoman voimakasta!

Kuvitteleppa vaihtoehtoehtoisesti: ilman puhdasta MVC-arkkitehturaamme olisimme
yrittäneet kutsua suoraan controllerin logiikkaa `Main.java` luokasta ja
taistelisimme saadaksemme "VBox" elementtiboksien Checkboxien lukumäärän
tarkistettua, samalla varoitellen sitä sekoittamasta
`tehtavat.json`-originaalitietokantaamme.

## Yhteenveto I/O-abstraktioista

Oikean arkkitehtuurijärjestelyn suurin hyöty näkyy yleensä ensimmäisenä
testauksen sujuvuudessa. Kuvion voi ajatella menevän näin: `UI (Controller)` ->
`Business Logic (Tehtavakokoelma)` -> `Data Provider (TehtavaRepository)`

UI:n testaus automatisoidusti on vaikeaa. Data providerin (oikean tallentamisen)
automaattinen testaus on tyypillisesti melko hidasta. Mutta eristetty _business
logic_ eli sovelluksen hermokeskus voidaan suorittaa puhtaana logiikkakoodina
sekunnin murto-osiin käyttämällä rajapintojen (interfaces) mahdollistamia
vale-luokkia ympärillä olevien vaikeiden järjestelmien korvaamisessa
testiajonaikaisesti.

## Tehtävät

<task>
  <task-title>Tehtävä 8.5: TODO-ohjelma, vaihe 11. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-5-todo-11/handout.md}}

</handout>
</task>
