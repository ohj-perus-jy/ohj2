# Yksikkötestaus

Yksikkötestauksen perusidea on yksinkertainen: testataan ohjelman pieniä osia,
kuten yksittäisiä luokkia tai metodeja, erillään muusta järjestelmästä. Tavoite
on varmistaa, että kukin osa toimii oikein omalla vastuullaan. Kun testin
ajatus pidetään pienenä ja tarkkarajaisena, virheiden paikantaminen on paljon
helpompaa kuin tilanteessa, jossa koko ohjelmaa yritetään testata kerralla.

Yksikkötestit ovat hyödyllisiä, koska ne paljastavat virheitä nopeasti jo
kehitysvaiheessa. Toiseksi ne toimivat eräänlaisena turvaverkkona: jos muutamme
koodia myöhemmin, ajamalla yksikkötestit näemme nopeasti rikkoutuiko jokin
aiemmin toiminut ominaisuus. Kolmanneksi ne pakottavat ohjelmoijan miettimään,
millainen luokan rajapinta on ja mitä sen oikeastaan pitäisi tehdä.

Ajatellaan esimerkiksi `Tehtavakokoelma`-luokkaa. Voimme kirjoittaa testin,
joka lisää kokoelmaan yhden tehtävän ja tarkistaa, että listassa on nyt yksi
alkio. Voimme kirjoittaa toisen testin, joka yrittää lisätä tyhjän otsikon ja
tarkistaa, ettei tehtävää lisätä lainkaan. Kolmas testi voisi poistaa valitun
tehtävän ja varmistaa, että listan koko pienenee oikein. Jokaisessa näistä
testeistä tarkistetaan yksi selkeä käyttäytyminen.

## JUnit 5

Java-maailmassa yksikkötestejä tehdään usein **JUnit**-kirjastolla. JUnit antaa
valmiit työkalut testimetodien kirjoittamiseen sekä odotettujen tulosten
tarkistamiseen. 

Kirjoitushetkellä ajantasainen JUnit-version on 6.0.3, joka tunnetaan myös
nimellä JUnit Jupiter. JUnit otetaan käyttöön lisäämällä sen riippuvuus
projektin `pom.xml`-tiedostoon `junit-jupiter`-riippuvuus.

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.10.2</version>
    <scope>test</scope>
</dependency>
```

Testit kirjoitetaan tavallisesti hakemistoon `src/test/java`.

Kokeillaan tehdä pääluokkaamme ensin aliohjelma `Keskiarvo`, joka laskee
keskiarvon kuitenkin niin, jos listassa on `lopetusluku` tai sitä suurempi luku,
kaikki sen jälkeen olevat luvut jätetään huomioimatta. 

```java,ignore
public static double keskiarvo(List<Integer> luvut, int lopetusluku) {
    if (luvut.isEmpty()) {
        throw new IllegalArgumentException("Lista ei saa olla tyhjä");
    }
    int summa = 0;
    int lukujenMaara = 0;
    for (int luku : luvut) {
        if (luku >= lopetusluku) {
            break;
        }
        summa += luku;
        lukujenMaara++;
    }
    return (double) summa / lukujenMaara;
}
```

Tehdään sitten tälle metodille yksikkötesti. Tee `test/java`-kansioon uusi
luokka `KeskiarvoTest` ja kirjoita siihen seuraavat kaksi testimetodia. Muuta
ensimmäinen `import`-lause vastaamaan oman pääluokkasi nimeä.

```java,ignore
import fi.jyu.ohj2.Main;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class KeskiarvoTest {

    @Test
    void keskiarvoLaskeeOikein() {
        List<Integer> luvut = List.of(1, 2, 3, 4, 5);
        double tulos = Main.keskiarvo(luvut, 10);
        assertEquals(3.0, tulos, "Keskiarvon pitäisi olla 3.0");
    }

    @Test
    void keskiarvoLopettaaOikein() {
        List<Integer> luvut = List.of(1, 2, 3, 10, 4, 5);
        double tulos = Main.keskiarvo(luvut, 10);
        assertEquals(2.0, tulos, "Keskiarvon pitäisi olla 2.0, koska 10 ja sen jälkeen olevat luvut jätetään huomioimatta");
    }   
}
```

Testit voi ajaa esimerkiksi `public class KeskiarvoTest`-luokan vasemmalla
puolella olevasta vihreästä nuolesta. JUnit ajaa testit ja näyttää tulokset
IDE:n testinäkymässä. Jos kaikki testit menevät läpi, näet vihreän merkin. Jos
jokin testi epäonnistuu, näet punaisen merkin ja virheilmoituksen, joka kertoo
mikä meni pieleen.

Meiltä puuttuu yksi tärkeä testi: mitä tapahtuu, jos yhtään validia lukua ei
ole? Sovitaan tässä, että aliohjelmamme tulisi heittää
`IllegalArgumentException`- poikkeus. Kirjoitetaan vielä testi, joka varmistaa,
että tämä tapahtuu:

```java,ignore
@Test
void keskiarvoHeittaaPoikkeuksenTyhjallaListalla() {
    @Test
    void eiYhtaanLukuaMukaanKeskiarvoon() {
        List<Integer> luvut = List.of(10, 20, 30, 40, 50, 60);
        IllegalArgumentException exception =
                assertThrows(IllegalArgumentException.class, () -> {
                    Main.keskiarvo(luvut, 10);
                });
        assertEquals("Yhtään lukua ei tullut mukaan keskiarvoon", exception.getMessage());
    }
}
```

Nyt testitulos näyttää punaista:

```
org.opentest4j.AssertionFailedError: Expected java.lang.IllegalArgumentException to be thrown, but nothing was thrown.
```

Nollalla jakaminen ei `double`-luvuilla laskettaessa heitä poikkeusta, vaan
palauttaa `NaN`-arvon. Korjataan tämä aliohjelmassamme.

```java,ignore
public static double keskiarvo(List<Integer> luvut, int lopetusluku) {
    // ... aiempi koodi ennallaan ...
    // HIGHLIGHT_GREEN_BEGIN
    if (lukujenMaara == 0) {
        throw new IllegalArgumentException("Yhtään lukua ei tullut mukaan keskiarvoon");
    }
    // HIGHLIGHT_GREEN_END
    return (double) summa / lukujenMaara;
}
```

Nyt kaikki testit menevät läpi!

## Yksikkötestaus ja MVC-arkkitehtuuri

Nyt kun olemme siirtyneet MVC-arkkitehtuuriin ja luoneet
`Tehtavakokoelma`-luokan, olemme erottaneet käyttöliittymän kokonaan irti
sovelluksen logiikasta ja datasta. Tällä on ratkaiseva ohjelmistotuotannollinen
hyöty. Jos yrittäisimme testata koodia käyttöliittymän kautta esimerkiksi
simuloimalla napin painalluksia, testaus olisi hidasta, altista satunnaisille
virheille ja vaatisi raskaiden JavaFX-kirjastojen käynnistämisen. Koska
kokoelmalla on nyt selkeä ohjelmointirajapinta (metodit `lisaaTehtava`,
`poistaTehtava` jne.), voimme rakentaa **yksikkötestejä**, jotka kutsuvat
suoraan kokoelmaa ja tarkistavat asioiden toimiutuvuuden millisekunneissa ilman
ruudulle aukeavia ikkunoita.

Seuraavaksi opimme myös, miten pääsemme eroon ärsyttävästä ongelmasta:
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


## Mock- ja Fake-luokat

Testauksessa käytetään usein niin sanottuja *mock*- tai *fake*-olioita, kun
testattava luokka tekee yhteistyötä jonkin toisen olion kanssa. Ajatus on, että
oikean yhteistyöolion tilalle annetaan testissä kevyt korvike, jonka toimintaa
on helpompi hallita. Näin testi voidaan kohdistaa juuri siihen luokkaan, jota
halutaan testata, ilman että mukana on turhaan tiedostoja, tietokantoja,
verkkoa tai muuta raskasta ympäristöä.

Ajatellaan yksinkertaista esimerkkiä, jossa luokka `Pakkasvahti` kysyy
lämpötilan toiselta oliolta, esimerkiksi `Lampoanturi`-rajapinnan kautta. Jos
haluamme testata, toimiiko `Pakkasvahti` oikein, emme välttämättä halua käyttää
oikeaa anturia, koska sellaista ei ehkä testissä ole olemassa tai sen palauttama
arvo vaihtelee koko ajan. Sen sijaan voimme tehdä valeanturin, joka palauttaa
aina esimerkiksi arvon `21.5`. Tällöin testi on ennustettava: tiedämme tarkalleen,
mitä arvoa `Pakkasvahti` saa ja mitä sen pitäisi tehdä sillä.

Esimerkiksi:

```java
public interface Lampoanturi {
    double mittaaLampotila();
}

public class Pakkasvahti {
    private final Lampoanturi anturi;

    public Pakkasvahti(Lampoanturi anturi) {
        this.anturi = anturi;
    }

    public boolean onkoPakkasta() {
        return anturi.mittaaLampotila() < 0;
    }
}
```

Oikeassa ohjelmassa `Lampoanturi` voisi lukea arvon fyysiseltä laitteelta, mutta
testissä voimme käyttää yksinkertaista valeoliota:

```java
public class ValeLampoanturi implements Lampoanturi {
    @Override
    public double mittaaLampotila() {
        return 21.5;
    }
}
```

Tällöin `Pakkasvahti`-luokkaa testatessa tiedämme varmasti, että anturi
palauttaa aina saman arvon.

Tällaiset korvikeoliot ovat hyödyllisiä erityisesti silloin, kun oikea riippuvuus
on hidas, vaikeasti hallittava tai aiheuttaa sivuvaikutuksia. Seuraavaksi
hyödynnämme samaa ajatusta todo-sovelluksessa tekemällä vale-säilön, joka
teeskentelee tallentavansa dataa, mutta pitääkin sen vain muistissa testin ajan.

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
  <task-title>Tehtävä 8.5: Todo-sovellus, vaihe 11. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-5-todo-11/handout.md}}

</handout>
</task>
