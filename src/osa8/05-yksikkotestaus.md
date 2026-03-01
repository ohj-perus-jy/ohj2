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

Tässä osassa opimme myös, miten pääsemme eroon ärsyttävästä ongelmasta:
tiedosto-operaatioista testeissä.

## Ongelma: Tiedostojen ja I/O:n testaus on vaarallista

Mietitäänpä tilannetta, jossa lähtisimme testaamaan uutta hienoa
`Tehtavakokoelma`-luokkaamme. Mitä tapahtuu, jos testi tekee kokoelmaan kymmenen
uutta tehtävää ja testaa, että lukumäärä täsmää? Koska laitoimme observerin
varoittamaan muutoksista ja kutsumaan kokoelman `tallenna()`-metodia, ohjelma
tallentaa nämä testitehtävät **oikealle kovalevylle** (esim.
`tehtavat.json`-tiedostoon).

Oikealle kovalevylle kirjoittaminen on testeissä yleensä pahasta, sillä se tekee
testeistä erittäin hitaita pyöriä, jos satoja testejä ajettaisiin sekunneissa
peräjälkeen.

## Ratkaisu: Datatallennuksen eriyttäminen abstraktioiden taakse (Repository-suunnittelumalli)

Jotta pääsemme näistä ongelmista eroon tehdessämme yksikkötestejä, turvaudumme
ohjelmistosuunnittelun klassiseen temppuun: erotamme tallennuspaikan
(`tehtavat.json` via `ObjectMapper`) suorasta käytöstä. Hyvä suunnitteluperiaate
ohjaa erottamaan tallennuksen omaksi kokonaisuudekseen, ja tähän käytetään usein
_Repository_-rajapintaa (säilö).

Rajapinnan tehokkuus piilee siinä, että `Tehtavakokoelma`-luokan ei sen jälkeen
enää tarvitse tietää, _miten_ tai _minne_ data tallennetaan (onko se
JSON-tiedosto, tietokanta vai vain keskusmuistilista testausta varten).

### 1. Luodaan rajapinta `TehtavaRepository`

Luodaan pakettiin `persistence` uusi rajapinta:

```java
package fi.jyu.ohj2.nimi.todo.persistence;

import fi.jyu.ohj2.nimi.todo.model.Tehtava;
import java.io.IOException;
import java.util.List;

public interface TehtavaRepository {
    List<Tehtava> lataa() throws IOException;
    void tallenna(List<Tehtava> tehtavat) throws IOException;
}
```

### 2. Irroitetaan JSON-tallennuskoodi mallista omaan toteutukseensa `JsonTehtavaRepository`

Kopioidaan tallennuskoodit `Tehtavakokoelmasta` uuteen omistettuun luokkaan,
joka on rajapinnan mukainen suorittaja (implementaatio):

```java
package fi.jyu.ohj2.nimi.todo.persistence;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import fi.jyu.ohj2.nimi.todo.model.Tehtava;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class JsonTehtavaRepository implements TehtavaRepository {
    private final Path tallennustiedosto;
    private final ObjectMapper mapper = new ObjectMapper();

    public JsonTehtavaRepository(Path tallennustiedosto) {
        this.tallennustiedosto = tallennustiedosto;
    }

    @Override
    public List<Tehtava> lataa() throws IOException {
        if (Files.notExists(tallennustiedosto)) {
            return List.of();
        }
        return mapper.readValue(tallennustiedosto.toFile(), new TypeReference<>() {});
    }

    @Override
    public void tallenna(List<Tehtava> tehtavat) throws IOException {
        mapper.writeValue(tallennustiedosto.toFile(), tehtavat);
    }
}
```

### 3. Päivitetään Tehtavakokoelma huolimaan kuka tahansa tallentaja

Muokkaamme `Tehtavakokoelman` konstruktoria niin, että sille _annetaan_ jokin
rajapinnan toteuttaja tiedostojumpan sijaan:

```java
public class Tehtavakokoelma {
    private final ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList(
            t -> new javafx.beans.Observable[]{
                t.tehtyProperty(),
                t.otsikkoProperty(),
                t.prioriteettiProperty()
            }
    );
    
    // Riippuvuus tallennusmekanismista on nyt rajapinnan takana!
    private final TehtavaRepository repository;

    // Konstruktoriin tungetaan haluttu tallennusväline sisältäpäin luomisen sijaan (Dependency Injection)
    public Tehtavakokoelma(TehtavaRepository repository) {
        this.repository = repository;
        
        this.tehtavat.addListener((javafx.collections.ListChangeListener<Tehtava>) change -> {
            tallenna();
        });
    }

    public void lataa() throws IOException {
        // Nyt olemme vain delegointia aiemman monimutkaisen logiikan sijaan!
        List<Tehtava> ladatut = repository.lataa();
        tehtavat.setAll(ladatut);
    }

    private void tallenna() {
        try {
            // Nyt olemme vain delegointia aiemman monimutkaisen logiikan sijaan!
            repository.tallenna(tehtavat);
        } catch (IOException e) {
            System.err.println("Tallennus epäonnistui: " + e.getMessage());
        }
    }
    
    // ... kaikki muut lisaaTehtava yms. samat kuin aiemmin!
}
```

(Muista vihdoin vaihtaa `MainController`issa uusi rivi muotoon
`new Tehtavakokoelma(new JsonTehtavaRepository(Path.of("tehtavat.json")));`)

## Testaaminen vale-säilöllä JUnit 5:ssä

Testiympäristössä (eli `src/test/java...`-kansiossa) voimme nyt luoda luokan
(ns. _Mock_- tai _Fake_-luokan), joka **teeskentelee** tallentavansa tietoja
tiedostoon, mutta todellisuudessa tallentaakin ne vain normaaliin Java-listaan
laitteen välimuistiin.

```java
public class MockTehtavaRepository implements TehtavaRepository {

    // Keskusmuistissa oleva data "tiedoston" sijaan testejä varten
    private List<Tehtava> tallennetutData = new ArrayList<>();

    @Override
    public List<Tehtava> lataa() {
        return tallennetutData; 
    }

    @Override
    public void tallenna(List<Tehtava> tehtavat) {
        // Kun kokoelma yrittää "tallentaa" levylle, kopioidaankin data vain tähän temp-listaan!
        this.tallennetutData = new ArrayList<>(tehtavat);
    }
    
    public List<Tehtava> haeTallennetut() {
        return this.tallennetutData;
    }
}
```

Nyt voimme turvallisin mielin testata mallia JUnit-testeillä:

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TehtavakokoelmaTest {

    @Test
    void lisaaTehtava_lisaaTehtavanJaTallentaaSen() {
        // 1. Arrange: Valmistellaan testidata. SYÖTETÄÄN VALE-SÄILÖ!
        MockTehtavaRepository mockRepo = new MockTehtavaRepository();
        Tehtavakokoelma malli = new Tehtavakokoelma(mockRepo);
        
        // 2. Act: Kutsutaan metodia
        malli.lisaaTehtava("Käy kaupassa");
        
        // 3. Assert: Tarkistetaan tulos oikeassa data-domainissa
        assertEquals(1, malli.getTehtavat().size(), "Listassa pitäisi olla 1 tehtävä.");
        assertEquals("Käy kaupassa", malli.getTehtavat().get(0).getOtsikko(), "Otsikon pitäisi täsmätä");
        
        // 4. Assert 2: Varmistetaan mock-luokan avulla, että kokoelma laukaisi tallennuksen tapahtuman yhteydessä
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

Kuvitteleppa vaihtoehtoehtoisesti: ilman puhdasta MVC-arkkitehturaamme olisimme
yrittäneet kutsua suoraan controllerin logiikkaa `Main.java` luokasta ja
taistelisimme saadaksemme "VBox" elementtiboksien Checkboxien lukumäärän
tarkistettua, samalla varoitellen sitä sekoittamasta aitoa
`tehtavat.json`-originaalitietokantaamme!

## Yhteenveto I/O-abstraktioista

Oikean arkkitehtuurijärjestelyn suurin hyöty näkyy yleensä ensimmäisenä
testauksen sujuvuudessa. Kuvion voi ajatella menevän näin: `UI (Controller)` ->
`Business Logic (Tehtavakokoelma)` -> `Data Provider (TehtavaRepository)`

UI:n testaus automatisoidusti on vaikeaa. Data providerin (oikean tallentamisen
levylle) automaattinen testaus on tyypillisesti melko hidasta ja haurasta. Mutta
eristetty _business logic_ eli sovelluksen hermokeskus voidaan suorittaa
puhtaana logiikkakoodina sekunnin murto-osiin käyttämällä rajapintojen
(interfaces) mahdollistamia vale-luokkia ympärillä olevien vaikeiden
järjestelmien korvaamisessa testiajonaikaisesti.

## Tehtävät

<task>
  <task-title>Tehtävä 8.5: TODO-ohjelma, vaihe 11. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-5-todo-11/handout.md}}

</handout>
</task>
