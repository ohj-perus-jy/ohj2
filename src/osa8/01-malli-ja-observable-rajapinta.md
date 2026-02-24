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

## Hyvin pieni esimerkki ensin {#ensimmainen-esimerkki}

Ennen `Tehtava`-mallia katsotaan tarkemmin, miten JavaFX:n automaattinen tiedonvälitys
toimii. Alla olevassa esimerkissä luomme listan, joka osaa kertoa itsestään muille:

```java
// 1. Luodaan erikoistyyppinen lista tavallisen ArrayListin sijaan
ObservableList<String> nimet = FXCollections.observableArrayList();

// 2. Rekisteröidään "kuuntelija", joka reagoi heti kun listan sisältö muuttuu
nimet.addListener((ListChangeListener<String>) change -> {
    while (change.next()) { // Käydään läpi kaikki tapahtuneet muutokset
        if (change.wasAdded()) {
            IO.println("Listalle lisättiin: " + change.getAddedSubList());
        }
    }
});

// 3. Muutetaan dataa
nimet.add("Ada");
nimet.add("Linus");
```

Voit halutessasi tehdä kurssin JavaFX-arkkityypin
(`io.github.ohj-perus-jy:javafx-fxml-template`), laittaa `main`-metodissa olevan
`launch()`-kutsun kommenttiin, ja laittaa tämän koodin testiksi siihen. Näet,
että kun `nimet.add("Ada")` ja `nimet.add("Linus")` suoritetaan, konsoliin
tulostuu tieto siitä, että nimi on lisätty.

**Mitä tässä tapahtuu?** Tavallinen `ArrayList` on passiivinen: jos lisäät sinne
alkion, mikään toinen olio ei tiedä siitä, ellei se toinen erikseen käy
tarkistamassa listan kokoa. `ObservableList` taas on aktiivinen. Kun kutsumme
`nimet.add("Ada")`, lista lähettää välittömästi ilmoituksen kaikille muutoksista
kiinnostuneille, jotka ovat rekisteröityneet kuuntelijoiksi. Näitä kuuntelijoita
kutsutaan *tilaajiksi* (subscribers). Meidän tapauksessamme tilaaja on
lambda-funktio, joka tulostaa konsoliin, mitä on tapahtunut.

TODO: Sananen tyyppimuunnoksesta lambda-lausekkeessa. Mitä `change`-parametri
itse asiassa sisältää? 

<details><summary> Valinnaista lisätietoa: Miksi lambda-lausekkeessa tarvitaan tyyppimuunnos? </summary>

Vielä sananen `change`-parametrista, joka näyttää hieman monimutkaiselta.
`Change` on geneerinen olio, joka sisältää tietoa listassa kulloinkin tapahtuneesta
muutoksesta. `Change`-oliota käytetään `ListChangeListener`-rajapinnan
`onChanged`-metodissa; tuon metodin esittelyrivi on `void onChanged(Change<?
extends E> c);`. Nyt meillä `E` on `String`, joten täydellinen tyyppi on
`ListChangeListener.Change<? extends String>`. Syy tälle syntaksille on siinä,
että listat ovat geneerisiä, ja tällä tavalla erilaisia listamuutoksia (lisäys,
poisto, korvaus, jne.) voidaan käsitellä samalla `Change`-oliolla.

</details>

Yllä olevan esimerkin `while (change.next())` on JavaFX:n tapa käsitellä
listamuutoksia. Yhdellä kertaa listaan saattaa tulla useita muutoksia (esim.
`addAll`), ja silmukka varmistaa, että jokainen niistä käsitellään.

## Kytkentä käyttöliittymään (FXML)

Vaikka esimerkissä tulostimme tiedon vain konsoliin, oikeassa sovelluksessa
listan muutosten tilaaja on yleensä jokin käyttöliittymäkomponentti.

Tehdään pari muutosta, jotta pääsemme näkemään tämän käytännössä. Palauta
`main`-metodissa olevan `launch()`-kutsu takaisin. Siirrä
`ObservableList<String> nimet`-määrittely `MainController.java`-tiedostoon
attribuutiksi, ja laita `initialize()`-metodiin `nimet.addListener(...)`-kutsu
sekä `nimet.add(...)`-kutsut. 

Tiedostojen pitäisi nyt näyttää suunnilleen tältä. Import-lauseet on jätetty
pois tilan säästämiseksi. 

`Main.java`

```java,ignore
public class Main {
    public static void main(String[] args) {
        Application.launch(App.class, args);
    }
}
```

`MainController.java`

```java
public class MainController implements Initializable {
    ObservableList<String> nimet = FXCollections.observableArrayList();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        //- // nimet.addListener((ListChangeListener.Change<? extends String> change) -> {
        nimet.addListener((ListChangeListener<String>) change -> {
            while (change.next()) { 
                if (change.wasAdded()) {
                    IO.println("Listalle lisättiin: " + change.getAddedSubList());
                }
            }
        });

        nimet.add("Ada");
        nimet.add("Linus");
    }
}
```

Tehdään nyt FXML-tiedostoon komponentti, joka osaa näyttää
`ObservableList`-listan sisällön; `ListView` osaa juurikin tämän. Lisää
FXML-tiedostoon valmiina olevan VBoxin sisään tämä rivi: 

```xml
<ListView fx:id="nimitulosteet" />
```

Controller-luokassa kytkemme datan ja näkymän toisiinsa yhdellä komennolla:

```java,ignore
@FXML private ListView<String> nimitulosteet;

public void initialize() {
    // Kytketään lista ja komponentti toisiinsa
    nimitulosteet.setItems(nimet);

    // ... loput initialize-koodista ...
}
```

Tämän kytkennän jälkeen **meidän ei tarvitse koskaan kutsua mitään "päivitä näkymä"
-metodia**. Kun koodissa tehdään `nimet.add("Uusi nimi")`, nimi ilmestyy ruudulle
automaattisesti. `ListView` on sisäisesti lisännyt itsensä listan kuuntelijaksi
samalla tavalla kuin teimme esimerkin `addListener`-kohdassa.

Tätä on tietysti vielä pikkuisen hankala nähdä, koska `initialize()`-metodissa
on suoraan kovakoodattuna `nimet.add("Ada")` ja `nimet.add("Linus")`. Kokeillaan
siis vielä, että saamme listaan uusia nimiä suoraan käyttöliittymästä. Lisää
FXML:ään `TextField` ja `Button`, joiden avulla käyttäjä voi syöttää uuden nimen
listaan.

```xml
<TextField fx:id="nimikentta" />
<Button text="Lisää nimi" onAction="#lisaaNimi" />
```

Nyt `Button`-komponenttimme on määritetty kutsumaan `lisaaNimi`-metodia, kun
sitä klikataan. FXML-kielessä kutsuttavan metodin nimeä edeltää `#`-merkki.
Toteutetaan tämä metodi `MainController`-luokassa:

```java
@FXML private TextField nimikentta;

@FXML
private void lisaaNimi() {
    String uusiNimi = nimikentta.getText();
    nimet.add(uusiNimi);
}
```

Tavoitteenamme on siis **yksisuuntainen riippuvuus**: JavaFX huolehtii siitä,
että näkymä päivittyy, kun data muuttuu, mutta ei itse muuta dataa. Vastaavasti
logiikka, joka muuttaa dataa, ei pidä riippua siitä, miten data näytetään. 

## Pieni Tehtävä-malli (ensin tavallisilla kentillä)

Siirrytään nyt nimilistasta takaisin TODO-sovellukseemme. Lähtötilanne on nyt
tämä: 

 * tehtävien lukeminen tapahtuu `lataaTehtavat()`-metodissa, joka hakee datan
   JSON-tiedostosta, muuttaa sen ensin `Tehtava`-olioiksi, ja sitten luo
   `CheckBox`-komponentteja.
 * Tehtävien lisääminen tapahtuu `lisaaTehtava()`-metodissa, joka luo uuden
   `CheckBox`-komponentin ja lisää sen suoraan `VBox`-komponenttiin.
 * Tehtävien tilan muuttaminen tapahtuu `CheckBox`-tapahtumankäsittelijässä, joka
   siirtää `CheckBox`-komponentteja `VBox`-komponenttien välillä.
 * Tehtävien tallennus tapahtuu `tallenna()`-metodissa, joka hakee datan takaisin
   `VBox`-komponenteista ja kirjoittaa sen JSON-tiedostoon.

Seuraavaksi siirretään "totuus" mallilistaan. Ajatus on se, että
`tehtavat`-lista olisi jatkossa päädata ja `VBox`-komponentit ovat vain näkymää.
Tavoite olisi seuraava:

 * `lataaTehtavat()`-metodi hakee datan JSON-tiedostosta, muuttaa sen
   `Tehtava`-olioiksi, kuten ennenkin, mutta ei luo `CheckBox`-komponentteja.
   Sen sijaan se palauttaa listan `Tehtava`-olioita, joka asetetaan
   `tehtavat`-attribuuttiin.
 * `lisaaTehtava()`-metodi luo uuden `Tehtava`-olion ja lisää sen `tehtavat`-listaan.
 * Tehtävien tilan muuttaminen tapahtuu `CheckBox`-tapahtumankäsittelijässä, joka
   muuttaa mallin tilaa eikä siirtele komponentteja.
 * Näkymä päivittyy automaattisesti, kun mallin data muuttuu.
 * `tallenna()`-metodi hakee datan suoraan mallista eikä tarvitse tietää
   näkymästä mitään.

Aloitetaan lisäämällä `MainController`-luokkaan uusi attribuutti:

```java
private final ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList();
```

Nykyisessä koodissa `lisaaTehtava()` lisää suoraan `CheckBox`in `VBox`:iin.
Muuta se lisäämään `Tehtava` listaan:

```java
private void lisaaTehtava() {
    String teksti = uusiTehtavaNimi.getText();
    if (teksti == null || teksti.isBlank()) {
        uusiTehtavaNimi.requestFocus();
        return;
    }
    tehtavat.add(new Tehtava(teksti.trim(), false));
    uusiTehtavaNimi.clear();
    uusiTehtavaNimi.requestFocus();
}
```

Nyt lisää metodi, joka rakentaa `VBox`-sisällön aina `tehtavat`-listasta:

```java
private void paivitaNakyma() {
    tekemattomat.getChildren().clear();
    tehdyt.getChildren().clear();

    for (Tehtava tehtava : tehtavat) {
        CheckBox cb = luoCheckBox(tehtava);
        if (tehtava.getTehty()) {
            tehdyt.getChildren().add(cb);
        } else {
            tekemattomat.getChildren().add(cb);
        }
    }
}
```

### Vaihe 4: kuuntele listaa yhdessä paikassa

Kytke `initialize()`-metodissa listan muutokset näkymään ja tallennukseen:

```java
@Override
public void initialize(URL url, ResourceBundle resourceBundle) {
    tehtavat.addListener((ListChangeListener<Tehtava>) change -> {
        paivitaNakyma();
        tallenna();
    });

    tehtavat.addAll(lataaTehtavat());
    paivitaNakyma();

    uusiTehtavaNimi.setOnAction(event -> lisaaTehtava());
    lisaaUusiTehtavaPainike.setOnAction(event -> lisaaTehtava());
}
```

Huomaa, että `lataa()` kannattaa muuttaa palauttamaan lista:

```java
private List<Tehtava> lataaTehtavat() {
    Path path = Path.of("tehtavat.json");
    if (Files.notExists(path)) {
        return List.of();
    }
    try {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(path.toFile(), new TypeReference<>() {});
    } catch (JacksonException je) {
        IO.println("JSONin lukeminen epäonnistui: " + je.getMessage());
        return List.of();
    }
}
```

### Vaihe 5: CheckBox-tapahtuma muuttaa mallia

Aiemmassa ratkaisussa `CheckBox`-tapahtuma siirteli komponentteja `VBox`ien
välillä, ja data luettiin myöhemmin takaisin UI:sta. Koska koko siirtymän
tärkein ajatus on, että käyttöliittymä ei enää ole datan säilytyspaikka, meidän
pitää muuttaa tapahtumankäsittelijä niin, että se muuttaa mallia eikä
UI-komponentteja.

Kun checkboxia klikataan, tapahtumankäsittelijä päivittää `tehtavat`-listaa.
Valitettavasti meillä ei ole vielä tapaa päivittää `Tehtava`-olion sisäistä
tilaa esimerkiksi `tehtava.setTehty(true)`-kutsulla. Tarkemmin sanoen voisimme
toki tuollaisen metodin tehdä, mutta `ObservableList` ei huomaisi, että olion
sisäinen tila on muuttunut, koska `ObservableList` tarkkailee oletuksena vain
listan rakennetta (alkioiden määrä ja järjestys), ei listalla olevien olioiden
sisäisiä kenttiä. JavaFX:ssä on kyllä keino ratkaista tämä, mutta katsotaan
aluksi hieman yksinkertaisempaa tapaa. 

Tehdään uusi `Tehtava`-olio, joka on muuten sama kuin vanha, mutta
`tehty`-kenttä on päinvastainen. Tämä on hieman kömpelöä, mutta toimii:

```java
private CheckBox luoCheckBox(Tehtava tehtava) {
    CheckBox cb = new CheckBox(tehtava.getTeksti());
    cb.setSelected(tehtava.getTehty());
    cb.setOnAction(event -> {
        tehtavat.remove(tehtava);
        tehtavat.add(new Tehtava(tehtava.getTeksti(), cb.isSelected()));
    });
    return cb;
}
```


Cb-olion tilan muuttaminen aiheuttaa kaksi muutosta `tehtavat`-listaan: vanhan
`Tehtava`-olion poiston ja uuden `Tehtava`-olion lisäyksen. Tämä on tietysti
vähän turhaa, mutta toimii, koska `ObservableList` huomaa molemmat muutokset ja
päivittää näkymän automaattisesti.

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

Tallennuksen voi kytkeä listan muutoksiin:

```java
tehtavat.addListener((ListChangeListener<Tehtava>) change -> {
      tallenna();
  }
);
```

Näin tallennus voidaan tehdä yhdessä paikassa ilman, että jokaiseen nappiin
kirjoitetaan erillinen `tallenna()`-kutsu.


<task>
  <task-title>Tehtävä 8.1: TODO-ohjelma, vaihe 7. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-1-todo-7/handout.md}}

  </handout>
</task>
