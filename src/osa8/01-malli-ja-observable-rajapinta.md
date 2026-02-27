# Malli ja Observable-rajapinta

Tässä luvussa erotamme datan omaksi malliksi ja kytkemme sen JavaFX:n
`Observable`-rajapintoihin.

## Miksi erillinen malli?

Tässä yhteydessä sanalla _malli_ tarkoitetaan sovelluksen datan rakennetta ja
siihen liittyvää tilaa ilman käyttöliittymäriippuvuuksia. Malli vastaa siis
kysymykseen siitä, mitä tietoa sovelluksessa on, ei siihen, miltä tieto näyttää
ruudulla.

Osan 7 jälkeen Todo-sovelluksemme jäi tilaan, jossa tehtävät mallinnettiin
käyttöliittymässä olevien valintaruutukomponenttien avulla. Ratkaisu oli sinänsä
hyvä aloitus, mutta pidemmällä aikavälillä se tekee sovelluksesta jäykän.
Esimerkiksi jos haluamme lisätä tehtäville uusia ominaisuuksia, kuten pidempi
kuvaus tai vaikkapa prioriteetti, meidän pitäisi muuttaa koko
käyttöliittymälogiikkaa esimerkiksi perimällä `CheckBox`-komponentti uudeksi
`TehtavaCheckBox`-komponentiksi, joka osaa näyttää kaikki uudet kentät.
Ensinnäkin tämä sitoo datan sen näyttämiseen, mikä ei ole hyvä
suunnitteluperiaate. Toisekseen, jos haluamme näyttää samaa dataa jossain muussa
muodossa kuin valintapainikkeina, meidän pitäisi kirjoittaa erikseen logiikkaa
jokaiseen uuteen näkymään.

Kun tehtävä on oma malliolionsa, samaa tietoa voidaan käsitellä riippumatta
siitä, näytetäänkö tieto taulukkona, listana tai erillisessä
muokkausikkunassa. Tämä tekee sovelluksesta joustavamman, koska uusia kenttiä,
kuten kuvaus, prioriteetti tai määräpäivä, voidaan lisätä suoraan malliin ilman
että käyttöliittymälogiikkaa täytyy kirjoittaa alusta uudelleen. Samalla
tiedoston tallennus ja lataus selkeytyvät, koska tallennamme varsinaista
sovellusdataa emmekä käyttöliittymäkomponenttien tilaa.

Pelkkä malli ei kuitenkaan vielä yksin ratkaise käyttöliittymän päivittymistä.
Jos tehtävädata muuttuu ohjelman ajon aikana, näkymän pitäisi reagoida tähän
automaattisesti ilman, että jokaisen muutoksen jälkeen kirjoitetaan erikseen
päivityskoodia kaikkiin käyttöliittymäkomponentteihin. 

Tässä kohtaa tulevat mukaan JavaFX:n _observable_-rakenteet, joiden avulla data
ja käyttöliittymä voidaan kytkeä toisiinsa hallitusti.

## Mitä Observable tarkoittaa JavaFX:ssä?

JavaFX:ssä sana **observable** (_havaittava_) tarkoittaa sitä, että olio osaa
ilmoittaa muutoksistaan muille sovelluksen osille automaattisesti. Tämä on
perustana sille, miten käyttöliittymä saadaan päivittymään heti, kun data
muuttuu.

Käytämme pääasiassa seuraavia tyyppiä:

- `ObservableList<T>`,  joka ilmoittaa, kun listaan lisätään tai siitä poistetaan
  alkioita.
- `ObservableValue<T>`, joka ilmoittaa, kun sen sisältämä yksittäinen arvo
  muuttuu.
- **Property**-tyyppejä, jotka ovat havaittavia versioita niitä vastaavista
  primitiivityypeistä. Esimerkiksi `StringProperty` on havaittava versio
  `String`-tyypistä, `BooleanProperty` vastaavasti `Boolean`-tyypistä ja niin
  edelleen. Havaittavia tyyppejä voidaan sitoa toisiinsa, jolloin yhden arvon
  muutos aiheuttaa automaattisesti toisen arvon päivittymisen. Esimerkiksi jos
  tehtävän otsikko on `StringProperty`-tyyppinen olio, se voidaan sitoa
  `Label`-komponenttiin, jolloin `Label`-teksti päivittyy automaattisesti, kun
  tehtävän otsikko muuttuu.

## Hyvin pieni esimerkki ensin {#ensimmainen-esimerkki}

Ennen `Tehtava`-mallia katsotaan tarkemmin, miten JavaFX:n automaattinen
tiedonvälitys toimii. Alla olevassa esimerkissä luomme listan, joka osaa kertoa
itsestään muille:

```java,ignore
// 1. Luodaan havaittavia lista tavallisen ArrayListin sijaan
ObservableList<String> nimet = FXCollections.observableArrayList();

// 2. Rekisteröidään "kuuntelija", joka reagoi heti kun listan sisältö muuttuu
nimet.addListener((ListChangeListener<String>) change -> {
    int koko = nimet.size();
    IO.println("Listalla on nyt " + koko + " nimeä.");
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
kutsutaan _tilaajiksi_ (subscribers). Yllä olevassa esimerkissä tilaaja on
lambda-funktio, joka tulostaa konsoliin listan koon muutoksen jälkeen.

Lambda-funktion `change`-parametri sisältää kuvauksen juuri tapahtuneesta
muutoksesta tai muutoksista, jos niitä tapahtui useita: mitä indeksejä muutos
koski, lisättiinkö vai poistettiinko alkioita, ja mitä alkioita lisättiin tai
poistettiin. Kyseisellä oliolla on käytettävissään metodeja, kuten `wasAdded()`,
`wasRemoved()`, `getAddedSubList()` ja `getRemoved()`, joiden avulla voidaan
lukea tarkasti, mitä muutoksia tapahtui. TODO: JavaDoc. Yllä olevassa
esimerkissämmehän emme tuota parametria käyttäneet lainkaan.

Lisätään kuuntelijaan ehto, jonka perusteella listaan lisättäessä tulostetaan
jotakin, mutta poistettaessa ei. Tässä kohtaa tarvitsemme `change`-parametria.

```java,ignore
nimet.addListener((ListChangeListener<String>) change -> {
    while (change.next()) { // Käydään läpi kaikki tapahtuneet muutokset
        if (change.wasAdded()) {
            IO.println("Listalle lisättiin: " + change.getAddedSubList());
        }
    }
    int koko = nimet.size();
    IO.println("Listalla on nyt " + koko + " nimeä.");
});

nimet.add("Ada");
nimet.add("Linus");
nimet.add("Grace");
nimet.remove("Linus");
```

Yllä olevan esimerkin `while (change.next())` on JavaFX:n tapa käsitellä
listalla tapahtuneita muutoksia. Yhdellä kertaa listaan saattaa tulla useita
muutoksia (esim. `addAll`). Silmukka varmistaa, että jokainen niistä
käsitellään.

Kuuntelijoita voi olla useita. Jokainen `addListener(...)` rekisteröi uuden
tilaajan samaan listaan. Kun listassa tapahtuu muutos, JavaFX ilmoittaa siitä
kaikille rekisteröidyille kuuntelijoille yksi kerrallaan. Esimerkiksi yksi
kuuntelija voi päivittää käyttöliittymää, toinen voi kirjoittaa lokia ja kolmas
voi tehdä validointia.

<details><summary> Valinnaista lisätietoa: Miksi lambda-lausekkeessa tarvitaan tyyppimuunnos? </summary>

Vielä sananen `change`-parametrista, joka näyttää hieman monimutkaiselta.
`Change` on geneerinen olio, joka sisältää tietoa listassa kulloinkin
tapahtuneesta muutoksesta. `Change`-oliota käytetään
`ListChangeListener`-rajapinnan `onChanged`-metodissa; tuon metodin esittelyrivi
on `void onChanged(Change<?
extends E> c);`. Nyt meillä `E` on `String`, joten
täydellinen tyyppi on `ListChangeListener.Change<? extends String>`. Syy tälle
syntaksille on siinä, että listat ovat geneerisiä, ja tällä tavalla erilaisia
listamuutoksia (lisäys, poisto, korvaus, jne.) voidaan käsitellä samalla
`Change`-oliolla.

</details>

## Kytkentä käyttöliittymään (FXML)

Oikeassa sovelluksessa muutoksista ei yleensä tulostella konsoliin, vaan listan
muutosten tilaaja on yleensä jokin käyttöliittymäkomponentti.

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
            while (change.next()) { // Käydään läpi kaikki tapahtuneet muutokset
                if (change.wasAdded()) {
                    IO.println("Listalle lisättiin: " + change.getAddedSubList());
                }
            }
            int koko = nimet.size();
            IO.println("Listalla on nyt " + koko + " nimeä.");
        });

        nimet.add("Ada");
        nimet.add("Linus");
        nimet.add("Grace");
        nimet.remove("Linus");
    }
}
```

Tehdään nyt FXML-tiedostoon komponentti, joka osaa näyttää
`ObservableList`-listan sisällön; `ListView` osaa juurikin tämän. Lisää
FXML-tiedostoon valmiina olevan VBoxin sisään tämä rivi:

```xml
<ListView fx:id="nimitulosteet" />
```

Kontrolleriluokassa kytkemme datan ja näkymän toisiinsa yhdellä komennolla:

```java,ignore
@FXML private ListView<String> nimitulosteet;

public void initialize() {
    // Kytketään lista ja komponentti toisiinsa
    nimitulosteet.setItems(nimet);

    // ... loput initialize-koodista ...
}
```

Tämän kytkennän jälkeen **meidän ei tarvitse koskaan kutsua mitään "päivitä
näkymä" -metodia**. Kun koodissa tehdään `nimet.add("Uusi nimi")`, nimi ilmestyy
ruudulle automaattisesti. `ListView` on sisäisesti lisännyt itsensä listan
kuuntelijaksi samalla tavalla kuin teimme esimerkin `addListener`-kohdassa.

Tätä on tietysti vielä pikkuisen hankala nähdä, koska `initialize()`-metodissa
on suoraan kovakoodattuna `nimet.add("Ada")` ja `nimet.add("Linus")`. Kokeillaan
siis vielä, että saamme listaan uusia nimiä käyttöliittymästä käsin. Lisää
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

JavaFX huolehtii siitä, että näkymä päivittyy, kun data muuttuu. Toisaalta se,
mitä näkymässä tapahtuu, ei vaikuta datan rakenteeseen tai tilaan. Näin data ja
näkymä ovat erillään toisistaan, ja molempia voidaan muuttaa ilman, että toinen
niistä vaikuttaa toiseen.

## Pieni Tehtävä-malli (ensin tavallisilla kentillä)

Siirrytään nyt nimilistasta takaisin Todo-sovellukseemme. Tavoitteenamme on
siirtää sovelluksen "totuus" mallilistaan niin, että `VBox`-komponentit ovat
vain näkymää, joka päivittyy datan perusteella.

Aloitetaan lisäämällä `MainController`-luokkaan uusi attribuutti, joka toimii
sovelluksen datana:

```java
private final ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList();
```

Muutetaan nyt `lisaaTehtava()`-metodi niin, että se ei enää lisää
`CheckBox`-komponenttia suoraan `VBoxiin`, vaan lisää uuden `Tehtava`-olion
listaamme:

```java
private void lisaaTehtava() {
    String teksti = uusiTehtavaNimi.getText();
    if (teksti == null || teksti.isBlank()) {
        uusiTehtavaNimi.requestFocus();
        return;
    }
    // Lisätään mallilistaan, ei enää suoraan käyttöliittymään
    tehtavat.add(new Tehtava(teksti.trim(), false));
    uusiTehtavaNimi.clear();
    uusiTehtavaNimi.requestFocus();
}
```

Jotta näkymä päivittyisi, tarvitsemme metodin, joka osaa rakentaa
`VBox`-sisällöt aina mallilistan sisällön perusteella.

Tässä kohtaa on luontevaa muuttaa myös `luoCheckBox`-metodin esittelyrivi.
Aiemmin annoimme sille parametrina tekstin ja valintatiedon erikseen
(`String, boolean`), mutta nyt kun meillä on koko `Tehtava`-olio käytettävissä,
annetaan se suoraan parametrina. Näin metodi saa kaiken tarvitsemansa tiedon
yhdellä kertaa.

```java
private void paivitaNakyma() {
    // Tyhjennetään nykyiset listat
    tekemattomat.getChildren().clear();
    tehdyt.getChildren().clear();

    // Rakennetaan näkymä uudestaan mallin perusteella.
    // Metodi luoCheckBox(tehtava) saa nyt koko olion parametrina.
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

Myös tallennus muuttuu suoraviivaisemmaksi. Meidän ei tarvitse enää lukea
tietoja käyttöliittymäkomponenteista, vaan voimme kirjoittaa suoraan listan
sisällön JSON-tiedostoon:

```java
private void tallenna() {
    try {
        ObjectMapper mapper = new ObjectMapper();
        mapper.writeValue(Path.of("tehtavat.json"), tehtavat);
    } catch (IOException e) {
        IO.println("Tallennus epäonnistui: " + e.getMessage());
    }
}
```

Vastaavasti lataaminen on helpompaa, koska saamme suoraan listan
`Tehtava`-olioita ilman, että meidän tarvitsee rakentaa niistä
`CheckBox`-komponentteja. Palautetaan tästä metodista lista `Tehtava`-olioita,
jotka voidaan suoraan lisätä mallilistaan.

```java
private List<Tehtava> lataa() {
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

Nyt voimme kytkeä kaiken yhteen `initialize()`-metodissa. Voimme hyödyntää
`ObservableList`-listan kuuntelijaa, jotta `paivitaNakyma()` ja `tallenna()`
ajetaan automaattisesti aina, kun lista muuttuu.

```java
public void initialize(URL url, ResourceBundle resourceBundle) {

    // Asetetaan listalle kuuntelija
    tehtavat.addListener((ListChangeListener<Tehtava>) change -> {
        paivitaNakyma();
        tallenna();
    });

    // Ladataan tehtävät ja lisätään ne listaan (tämä aktivoi kuuntelijan)
    tehtavat.addAll(lataa());

    // Enter ja nappi vain lisäävät uuden tehtävän listaan
    uusiTehtavaNimi.setOnAction(event -> lisaaTehtava());
    lisaaUusiTehtavaPainike.setOnAction(event -> lisaaTehtava());
}
```

Checkboxin tilan muutos ei kuitenkaan vielä tallennu JSONiin. Korjataan tämä
seuraavaksi.

## CheckBox-tapahtuma muuttaa mallia

Nyt sovelluksemme osaa jo lisätä tehtäviä mallin kautta, mutta checkboxien
klikkaaminen on vielä ongelma. `luoCheckBox` sisältää edelleen logiikkaa, joka
siirtelee checkboxia käsin `VBox`-säiliöiden välillä:

```java,ignore
// VANHA VERSIO (poistuva logiikka korostettu)
private CheckBox luoCheckBox(Tehtava tehtava) {
    CheckBox cb = new CheckBox(tehtava.getTeksti());
    cb.setSelected(tehtava.getTehty());
    cb.setOnAction(event -> {
        // HIGHLIGHT_RED_BEGIN
        if (cb.isSelected()) {
            tekemattomat.getChildren().remove(cb);
            tehdyt.getChildren().add(cb);
        } else {
            tehdyt.getChildren().remove(cb);
            tekemattomat.getChildren().add(cb);
        }
        tallenna();
        // HIGHLIGHT_RED_END
    });
    return cb;
}
```

Nyt meidän on muutettava ajattelutapaa. Checkboxin ei tule siirtää itseään, vaan
muuttaa mallia. Kun malli muuttuu, `tehtavat`-listan kuuntelija herää ja kutsuu
`paivitaNakyma()`-metodia. Tuo metodi puolestaan tyhjentää molemmat VBoxit ja
sijoittaa tehtävät oikeisiin laatikoihin niiden tilan perusteella.

Valitettavasti tavallinen `Tehtava`-olio ei osaa ilmoittaa sisäisen tilansa
muuttumisesta. Jos kutsuisimme vain `tehtava.setTehty(true)`, `ObservableList`
ei huomaisi mitään, koska itse listaan ei tullut uutta oliota. Tässä vaiheessa
käytämme "remove/add"-kikkaa: poistamme vanhan olion ja lisäämme tilalle uuden,
jolla on päivitetty tila.

Tässä on `luoCheckBox`-metodin uusi versio. Huomaa, miten kaikki
`getChildren().remove()` -kutsut ovat poistuneet, koska `paivitaNakyma()` hoitaa
sijoittelun jatkossa:

```java
private CheckBox luoCheckBox(Tehtava tehtava) {
    CheckBox cb = new CheckBox(tehtava.getTeksti());
    cb.setSelected(tehtava.getTehty());

    cb.setOnAction(event -> {
        // MUUTOS: Emme enää siirrä komponenttia käsin VBoxista toiseen.
        // Sen sijaan päivitämme mallilistaa, mikä laukaisee näkymän päivityksen.
        tehtavat.remove(tehtava);
        tehtavat.add(new Tehtava(tehtava.getTeksti(), cb.isSelected()));
    });

    return cb;
}
```

Nyt prosessi on looginen ja reaktiivinen:

1. Käyttäjä klikkaa CheckBoxia.
2. `luoCheckBox`-metodin `setOnAction` muuttaa mallilistaa (`remove` & `add`).
   Tässä vaiheessa VBox-komponentteihin ei vielä kosketa.
3. `tehtavat`-listan kuuntelija (`addListener`) huomaa, että listan sisältö
   muuttui.
4. Kuuntelija kutsuu `paivitaNakyma()`- ja `tallenna()`-metodeja.
5. Vasta nyt `paivitaNakyma()` tyhjentää VBoxit ja rakentaa ne uudestaan mallin
   uuden tilan mukaiseksi.

Tämä ratkaisu on hieman tehoton, koska koko käyttöliittymä rakennetaan uudestaan
yhden klikkauksen takia. Toisaalta checkbox-olion tilan muuttaminen aiheuttaa
kaksi muutosta `tehtavat`-listaan: vanhan `Tehtava`-olion poiston ja uuden
`Tehtava`-olion lisäyksen. Tämä on tietysti vähän turhaa, mutta toimii, koska
`ObservableList` huomaa molemmat muutokset ja päivittää näkymän automaattisesti.

Opimme kuitenkin tärkeän asian: sovelluksen tila on nyt siirtynyt
`tehtavat`-listaan käyttöliittymäkomponenttien sisältä. Seuraavaksi katsomme,
miten JavaFX:n _property_-tyypit ratkaisevat mallin mallintamisen tyylikkäämmin
niin, ettei koko näkymää tarvitse jatkuvasti rakentaa uudelleen.

## Laajennetaan Tehtava-malli property-pohjaiseksi

Kuten aikaisemmin opimme, observable tarkoittaa arvoa, jonka muutoksia voidaan
kuunnella. Kokoelmien lisäksi JavaFX:ssä voidaan kuunnella myös yksittäisten
arvojen muutoksia käyttämällä _Property_-tyyppejä. Yksinkertaisesti sanottuna,
kun aiemmin tehtävällä oli tavallinen `boolean tehty` -muuttuja, joka oli
piilotettu ohjelman uumeniin, muutamme sen nyt _observable_-tyyppiseksi,
`BooleanProperty tehty`-muuttujaksi. Property-tyypit "käärivät" tavalliset
arvot, kuten `boolean` tai `String`, ja tarjoavat mekanismin ilmoittaa, kun
niiden arvo muuttuu. JavaFX:n `TableView`-komponentti, joka osaa näyttää arvoja
taulukkomuodossa (käytämme sitä hetken kuluttua), voi tilata ilmoituksen
(eli kuunnella) juuri tämän yhden tehtävän tilan muutoksista.

Päivitetään `Tehtava`-mallimme käyttämään `Property`-kääreitä. Lisätään samalla
vaivalla myös pari uutta kenttää: kuvaus ja prioriteetti. Kuvaus on
tekstikenttä, joka antaa lisätietoa tehtävästä. Prioriteetti kertoo tehtävän
tärkeyden. Käytämme näitä hieman myöhemmin. 

```java
import javafx.beans.property.BooleanProperty;
import javafx.beans.property.ObjectProperty;
import javafx.beans.property.SimpleBooleanProperty;
import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

public class Tehtava {
    // Alkuperäiset attribuutit on korvattu Property-kääreillä
    private final StringProperty otsikko = new SimpleStringProperty("");
    private final StringProperty kuvaus = new SimpleStringProperty("");
    private final BooleanProperty tehty = new SimpleBooleanProperty(false);
    private final ObjectProperty<Prioriteetti> prioriteetti = new SimpleObjectProperty<>(Prioriteetti.KESKI);

    // Jackson (tallennuskirjastomme) edellyttää usein tyhjän konstruktorin olemassaoloa
    public Tehtava() {}

    public Tehtava(String otsikko, boolean tehty) {
        setOtsikko(otsikko);
        setTehty(tehty);
    }

    // --- Property-setterit ja getterit ---
    // Huomaa, että JavaFX-tyylissä on tapana tarjota kolme metodia per property:
    // 1. Tavallinen get-metodi (palauttaa esim. boolean)
    // 2. Tavallinen set-metodi (ottaa esim. boolean)
    // 3. property-metodi (palauttaa itse Property-olion, esim. BooleanProperty)

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

Prioriteetti voidaan kätevästi mallintaa niin sanotulla *enumilla* eli
luettelotyypillä, joka määrittelee rajatun joukon vakioarvoja. Meidän
tapauksessamme prioriteetilla on kolme mahdollista arvoa: matala, keski ja
korkea. Enum on tapa mallintaa tällaisia vaihtoehtoja tyypin tasolla. 

```java,ignore
public enum Prioriteetti {
    MATALA, KESKI, KORKEA
}
```

Nyt tallennus voidaan tehdä yhdessä paikassa ilman, että jokaiseen nappiin
kirjoitetaan erillinen `tallenna()`-kutsu.

Olemme saavuttaneet tilanteen, jossa sekä kokonainen lista (`ObservableList`)
että listan yksittäiset alkiot (`Property`) osaavat kertoa tilansa muutoksista.
Olemme valmiita irrottautumaan pitkältä tuntuvalta `paivitaNakyma()` metodista
kokonaan, joka rakensi `CheckBox`-komponentteja `VBox`-laatikoiden sisään –
otetaan seuraavassa luvussa avuksi `TableView`!

<task>
  <task-title>Tehtävä 8.1: TODO-ohjelma, vaihe 7. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-1-todo-7/handout.md}}

</handout>
</task>
