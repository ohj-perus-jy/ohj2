# Malli ja Observable-rajapinta

Osassa 7 TODO-tehtävät mallinnettiin käyttöliittymäkomponentteina (`CheckBox`).
Ratkaisu oli sinänsä hyvä aloitus, mutta pidemmällä aikavälillä se tekee
sovelluksesta jäykän: data ja käyttöliittymä ovat liian vahvasti sidottuja
toisiinsa.

Tässä luvussa erotamme datan omaksi malliksi ja kytkemme sen JavaFX:n
`Observable`-rajapintoihin.

## Miksi erillinen malli?

Tässä yhteydessä sanalla *malli* tarkoitetaan sovelluksen datan rakennetta ja
siihen liittyvää tilaa ilman käyttöliittymäriippuvuuksia. Malli vastaa siis
kysymykseen siitä, mitä tietoa sovelluksessa on, ei siihen, miltä tieto näyttää
ruudulla. 

TODO-sovelluksessamme on jatkon kannalta hyödyllistä, että tehtävä kuvataan
erillisenä oliona eikä esimerkiksi `CheckBox`-komponenttina.

Kun tehtävä on oma malliolionsa, samaa tietoa voidaan käsitellä riippumatta
siitä, näytetäänkö tieto taulukkona, listana tai jossain erillisessä
muokkausikkunassa. Tämä tekee sovelluksesta joustavamman, koska uusia kenttiä,
kuten kuvaus, prioriteetti tai määräpäivä, voidaan lisätä suoraan malliin ilman
että käyttöliittymälogiikkaa täytyy kirjoittaa alusta uudelleen. Samalla
tiedoston tallennus ja lataus selkeytyvät, koska tallennamme varsinaista
sovellusdataa emmekä käyttöliittymäkomponenttien sisäistä tilaa.

Pelkkä malli ei kuitenkaan vielä yksin ratkaise käyttöliittymän päivittymistä.
Jos tehtävädata muuttuu ohjelman ajon aikana, näkymän pitäisi reagoida tähän
automaattisesti ilman, että jokaisen muutoksen jälkeen kirjoitetaan erikseen
päivityskoodia kaikkiin käyttöliittymäkomponentteihin. Tässä kohtaa tulevat
mukaan JavaFX:n *observable*-rakenteet, joiden avulla data ja käyttöliittymä
voidaan kytkeä toisiinsa hallitusti.

## Mitä Observable tarkoittaa JavaFX:ssä?

JavaFX:ssä sana **observable** (*havaittava*) tarkoittaa sitä, että olio osaa
ilmoittaa muutoksistaan muille sovelluksen osille automaattisesti. Tämä on
perustana sille, miten käyttöliittymä saadaan päivittymään heti, kun data muuttuu.

Käytännössä käytämme kolmea pääasiallista tyyppiä:

* `ObservableList<T>` ilmoittaa, kun listaan lisätään tai siitä poistetaan alkioita.
* `ObservableValue<T>` ilmoittaa, kun sen sisältämä yksittäinen arvo muuttuu.
* **Property**-tyypit, kuten `StringProperty` ja `BooleanProperty`, ovat näiden
  havaittavien arvojen käytännöllisiä toteutuksia. Niitä voi myös **sitoa**
  (*binding*) toisiinsa, jolloin yhden arvon muutos heijastuu automaattisesti toiseen.

## Hyvin pieni esimerkki ensin

Ennen `Tehtava`-mallia katsotaan tarkemmin, miten JavaFX:n automaattinen tiedonvälitys
toimii. Alla olevassa esimerkissä luomme listan, joka osaa kertoa itsestään muille:

```java
// 1. Luodaan erikoistyyppinen lista tavallisen ArrayListin sijaan
ObservableList<String> nimet = FXCollections.observableArrayList();

// 2. Rekisteröidään "kuuntelija", joka reagoi heti kun listan sisältö muuttuu
nimet.addListener((ListChangeListener<String>) change -> {
    while (change.next()) { // Käydään läpi kaikki tapahtuneet muutokset
        if (change.wasAdded()) {
            System.out.println("Lisättiin: " + change.getAddedSubList());
        }
    }
});

// 3. Muutetaan dataa
nimet.add("Ada");
nimet.add("Linus");
```

Voit halutessasi tehdä kurssin JavaFX-arkkityypin
(`io.github.ohj-perus-jy:javafx-fxml-template`), tyhjentää `main`-metodin, ja
laittaa tämän koodin testiksi siihen. Näet, että kun `nimet.add("Ada")` ja
`nimet.add("Linus")` suoritetaan, konsoliin tulostuu tieto siitä, että nimi on
lisätty.

**Mitä tässä tapahtuu?** Tavallinen `ArrayList` on passiivinen: jos lisäät sinne
alkion, mikään toinen olio ei tiedä siitä, ellei se toinen erikseen käy
tarkistamassa listan kokoa. `ObservableList` taas on aktiivinen. Kun kutsumme
`nimet.add("Ada")`, lista lähettää välittömästi ilmoituksen kaikille muutoksista
kiinnostuneille, jotka ovat rekisteröityneet kuuntelijoiksi. Näitä kuuntelijoita
kutsutaan *tilaajiksi* (subscribers).

Yllä olevan esimerkin `while (change.next())` saattaa näyttää monimutkaiselta,
mutta se on JavaFX:n vakiotapa käsitellä listamuutoksia. Yhdellä kertaa listaan
saattaa tulla useita muutoksia (esim. `addAll`), ja silmukka varmistaa, että
jokainen niistä käsitellään.

### Kytkentä käyttöliittymään (FXML)

Vaikka esimerkissä tulostimme tiedon vain konsoliin, oikeassa sovelluksessa listan
tilaaja on yleensä jokin käyttöliittymäkomponentti.

Kuvitellaan, että meillä on FXML-tiedostossa `ListView`-komponentti:

```xml
<!-- fxml-tiedosto -->
<ListView fx:id="nimitulosteet" />
```

Controller-luokassa kytkemme datan ja näkymän toisiinsa yhdellä komennolla:

```java
@FXML private ListView<String> nimitulosteet;

public void initialize() {
    // Kytketään lista ja komponentti toisiinsa
    nimitulosteet.setItems(nimet);
}
```

Tämän kytkennän jälkeen **meidän ei tarvitse koskaan kutsua mitään "päivitä näkymä"
-metodia**. Kun koodissa tehdään `nimet.add("Uusi nimi")`, nimi ilmestyy ruudulle
automaattisesti. `ListView` on sisäisesti lisännyt itsensä listan kuuntelijaksi
samalla tavalla kuin teimme esimerkin `addListener`-kohdassa.

Tavoitteenamme on siis **yksisuuntainen riippuvuus**: logiikkamme muokkaa vain
puhdasta dataa (listaa), ja JavaFX huolehtii siitä, että näkymä heijastaa aina
datan nykyistä tilaa.

## Pieni Tehtävä-malli (ilman propertyjä)

Ennen laajaa mallia tehdään ensin tarkoituksella pieni malli:

```java
public class Tehtava {
    private String otsikko;
    private boolean tehty;

    public Tehtava(String otsikko, boolean tehty) {
        this.otsikko = otsikko;
        this.tehty = tehty;
    }

    public String getOtsikko() {
        return otsikko;
    }

    public void setOtsikko(String otsikko) {
        this.otsikko = otsikko;
    }

    public boolean isTehty() {
        return tehty;
    }

    public void setTehty(boolean tehty) {
        this.tehty = tehty;
    }
}
```

Sitten lista:

```java
private final ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList();
```

Tässä vaiheessa tehtävä on jo selkeä *dataolio* eikä käyttöliittymäkomponentti.
Lisäksi tehtävät ovat yhdessä listassa, ja koska lista on observable, näkymä voi
kuunnella sitä suoraan.

## Miksi tämä ei vielä riitä?

`ObservableList` kertoo, kun listaan lisätään tai poistetaan tehtäviä.
Mutta jos yhden tehtävän sisäinen kenttä muuttuu (`otsikko`/`tehty`), lista ei
yksin aina riitä automaattiseen UI-päivitykseen.

Siksi JavaFX-sovelluksissa kannattaa käyttää mallin kentissä propertyjä.

## Laajennetaan Tehtava-malli property-pohjaiseksi

```java
public class Tehtava {
    private final StringProperty otsikko = new SimpleStringProperty("");
    private final StringProperty kuvaus = new SimpleStringProperty("");
    private final BooleanProperty tehty = new SimpleBooleanProperty(false);
    private final ObjectProperty<Prioriteetti> prioriteetti =
            new SimpleObjectProperty<>(Prioriteetti.KESKI);

    public Tehtava() {}

    public Tehtava(String otsikko, boolean tehty) {
        setOtsikko(otsikko);
        setTehty(tehty);
    }

    public String getOtsikko() { return otsikko.get(); }
    public void setOtsikko(String value) { otsikko.set(value); }
    public StringProperty otsikkoProperty() { return otsikko; }

    public String getKuvaus() { return kuvaus.get(); }
    public void setKuvaus(String value) { kuvaus.set(value); }
    public StringProperty kuvausProperty() { return kuvaus; }

    public boolean isTehty() { return tehty.get(); }
    public void setTehty(boolean value) { tehty.set(value); }
    public BooleanProperty tehtyProperty() { return tehty; }

    public Prioriteetti getPrioriteetti() { return prioriteetti.get(); }
    public void setPrioriteetti(Prioriteetti value) { prioriteetti.set(value); }
    public ObjectProperty<Prioriteetti> prioriteettiProperty() { return prioriteetti; }
}
```

Prioriteetti voidaan mallintaa enumilla:

```java
public enum Prioriteetti {
    MATALA, KESKI, KORKEA
}
```

## Listan perusoperaatiot

Kun malli on kunnossa, ViewModeliin (tai vastaavaan logiikkaluokkaan) voi tehdä
perusmetodit:

```java
public ObservableList<Tehtava> getTehtavat() {
    return tehtavat;
}

public void lisaaTehtava(String otsikko) {
    if (otsikko == null || otsikko.isBlank()) {
        return;
    }
    tehtavat.add(new Tehtava(otsikko.trim(), false));
}

public void poistaTehtava(Tehtava tehtava) {
    tehtavat.remove(tehtava);
}
```

## Reagointi muutoksiin yhdessä paikassa

Tallennuksen voi kytkeä listan muutoksiin:

```java
tehtavat.addListener((ListChangeListener<Tehtava>) change -> {
    while (change.next()) {
        if (change.wasAdded() || change.wasRemoved()) {
            tallenna();
        }
    }
});
```

Näin tallennus voidaan tehdä yhdessä paikassa ilman, että jokaiseen nappiin
kirjoitetaan erillinen `tallenna()`-kutsu.

## JSON ja propertyt

Jackson ei suoraan tykkää JavaFX-property-objekteista. Käytännössä on selkeintä
tehdä erillinen tiedonvälitysluokka (data transfer object, DTO) tiedostomuotoa varten:

```java
public record TehtavaDto(
        String otsikko,
        String kuvaus,
        boolean tehty,
        String prioriteetti
) {}
```

Silloin muunnos tehdään eksplisiittisesti niin, että tallennuksessa
`Tehtava` muunnetaan `TehtavaDto`:ksi ja latauksessa `TehtavaDto`
muunnetaan takaisin `Tehtava`:ksi. Tämä pitää käyttöliittymämallin ja
tiedostomuodon erillään.

<task>
  <task-title>Tehtävä 8.1: TODO-ohjelma, vaihe 7. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-1-todo-7/handout.md}}

  </handout>
</task>
