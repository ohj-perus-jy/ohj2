# Malli ja Observable-rajapinta

[Osassa 7.5](../osa7/05-tehtavien-lukeminen-tallennus.md) teimme
`Tehtava`-luokan, jonka tarkoituksena oli mallintaa JSON-tiedostoon
tallennettavan tehtävän tiedon. Käyttöliittymässä tehtävät käsiteltiin
`CheckBox`-olioina. Tehtävien tallentamisen ja lataamisen yhteydessä muunsimme
tehtäväoliot muodosta toiseen (`CheckBox` <-> `Tehtava`). Kuten [tämän osan
johdannossa mainittiin](./index.md), tämä muuntaminen ei pidemmällä aikavälillä ole hyvä
ratkaisu.

Ensimmäinen päävaihe datan ja käyttöliittymän vastuiden erottamisessa olisikin
vähentää datan toistoa. Eräs selkeä tapa on tehdä `Tehtava`-luokasta ainoa tapa
mallintaa yksittäisen tehtävän toiminnot ja tila. Käyttöliittymäkielessä
`Tehtava`-luokasta tulee niin kutsuttu *malliluokka* (engl. model class).
Malli-termillä tarkoitetaan sovelluksen datan rakennetta ja siihen liittyvää
tilaa ilman käyttöliittymäriippuvuuksia. Malli vastaa siis kysymykseen siitä,
mitä tietoa sovelluksessa on, ei siihen, miltä tieto näyttää ruudulla.

<!-- Kun tehtävä on oma malliolionsa, samaa tietoa voidaan käsitellä riippumatta
siitä, näytetäänkö tieto taulukkona, listana tai erillisessä
muokkausikkunassa. Tämä tekee sovelluksesta joustavamman, koska uusia kenttiä,
kuten kuvaus, prioriteetti tai määräpäivä, voidaan lisätä suoraan malliin ilman
että käyttöliittymälogiikkaa täytyy kirjoittaa alusta uudelleen. Samalla
tiedoston tallennus ja lataus selkeytyvät, koska tallennamme varsinaista
sovellusdataa emmekä käyttöliittymäkomponenttien tilaa. -->

Heti ensimmäiseksi ongelmaksi nousee, miten `Tehtava`-olion tiedot saadaan
käyttöliittymälle. Lisäksi jos tehtävädata muuttuu ohjelman ajon aikana, näkymän
pitäisi reagoida tähän automaattisesti ilman, että jokaisen muutoksen jälkeen
kirjoitetaan erikseen päivityskoodia kaikkiin käyttöliittymäkomponentteihin. 

Tässä kohtaan meitä auttavat JavaFX:n `Observable`-rakenteet, joiden avulla data
ja käyttöliittymä voidaan kytkeä toisiinsa hallitusti.

## `Observable`-rakenteet

Sana **observable** (havaittava) tarkoittaa, että olio osaa ilmoittaa
muutoksistaan muille sovelluksen olioille. Oliot, jotka kuuntelevat havaittavan
olion muutoksia kutsutaan puolestaan **havaitsijoiksi** (observer),
**tilaajiksi** (subscriber) tai **kuuntelijoiksi** (listener). Näillä termeillä
tarkoitetaan käytännössä samaa asiaa, vaikka eri konteksteissa saatetaan käyttää
painotuksista riippuen eri termejä. 

Haivaitsijat ja havaittavat oliot liittyvät syvemmin ohjelmistosuunnittelun
*observer*-suunnittelumalliin, jota käsitellään tarkemmin myöhemmissä osissa.
Tässä vaiheessa oleellista on ymmärtää, että JavaFX:ssä observable-rakenteet
toimivat perustana sille, miten käyttöliittymä saadaan päivittymään heti, kun
data muuttuu.

JavaFX:ssä käytämme pääosin seuraavia `Observable`-rakenteita:

- `ObservableList<T>`,  joka ilmoittaa, kun listaan lisätään tai siitä poistetaan
  alkioita,
- `ObservableValue<T>`, joka ilmoittaa, kun sen sisältämä yksittäinen arvo
  muuttuu,
- `Property`-tyyppejä, jotka ilmoittavat aina, kun sen sisältämä arvo muuttuu.
  `Property`-tyypit ovat havaittavia versioita niitä vastaavista
  primitiivityypeistä. Esimerkiksi `StringProperty` on havaittava versio
  `String`-tyypistä, `BooleanProperty` vastaavasti `Boolean`-tyypistä ja niin
  edelleen. 

<!-- Havaittavia tyyppejä voidaan sitoa toisiinsa, jolloin yhden arvon
  muutos aiheuttaa automaattisesti toisen arvon päivittymisen. Esimerkiksi jos
  tehtävän otsikko on `StringProperty`-tyyppinen olio, se voidaan sitoa
  `Label`-komponenttiin, jolloin `Label`-teksti päivittyy automaattisesti, kun
  tehtävän otsikko muuttuu. -->

### Johdatteleva esimerkki

Unohdetaan ihan hetkeksi Todo-sovellus ja yritetään saada kiinni
`Observable`-tyyppien toiminnasta johdattelevan esimerkin avulla.

Tehdään uusi JavaFX projekti seuraamalla [osan
7.1](../osa7/01-javafx-perusteet.md#ensimmäinen-javafx-sovellus) ohjeita.
Anna sovellukselle jokin toinen nimi ja groupId-arvo, vaikkapa
`ObservableEsimerkki` ja `fi.jyu.ohj2.esimerkit.observable`.

Kommentoi pois `Main`-luokan `main()`-pääohjelmasta
`Application.launch()`-kutsu:

```java,ignore
public static void main(String[] args) {
    // HIGHLIGHT_GREEN_BEGIN
    // Application.launch(App.class, args);
    // HIGHLIGHT_GREEN_END
}
```

Sovelluksemme käyttäytyy nyt kuin tavallinen komentoriviohjelma. Kokeile alkuun
lisätä ja ajaa alla oleva esimerkki. Lisää tarvittaessa import-määre: `import
javafx.collections.*;`.

```java
//-// ==========================================
//-// ÄLÄ KOPIOI TÄTÄ PIILOSSA OLEVAA KOODIA.
//-// Tämä koodi on olemassa, jotta mdbookissa voidaan matkia ObservableList-luokan 
//-// toimintaa. JavaFX-sovelluksessa ObservableList on toteutettuna valmiiksi.
//-// ==========================================
//-static interface ListChangeListener<E> {
//-    void onChanged(Change<E> c);
//-    class Change<E> {
//-        boolean next = true, added;
//-        List<E> items;
//-        Change(boolean a, E item) { 
//-            added = a; 
//-            items = a ? Collections.singletonList(item) : Collections.emptyList(); 
//-        }
//-        boolean next() { boolean r = next; next = false; return r; }
//-        boolean wasAdded() { return added; }
//-        List<E> getAddedSubList() { return items; }
//-    }
//-}
//-
//-static class ObservableList<E> extends ArrayList<E> {
//-    List<ListChangeListener<E>> listeners = new ArrayList<>();
//-    void addListener(ListChangeListener<E> l) { listeners.add(l); }
//-    public boolean add(E e) {
//-        super.add(e);
//-        listeners.forEach(l -> l.onChanged(new ListChangeListener.Change<>(true, e)));
//-        return true;
//-    }
//-    public boolean remove(Object o) {
//-        if (super.remove(o)) {
//-            listeners.forEach(l -> l.onChanged(new ListChangeListener.Change<>(false, null)));
//-        }
//-        return true;
//-    }
//-}
//-
//-static class FXCollections {
//-    public static <E> ObservableList<E> observableArrayList() { return new ObservableList<>(); }
//-}
//-
public static void main(String[] args) {
    // 1. Luodaan havaittavia lista tavallisen ArrayListin sijaan
    ObservableList<String> nimet = FXCollections.observableArrayList();

    // 2. Rekisteröidään "kuuntelija", joka reagoi heti kun listan sisältö muuttuu
    nimet.addListener((ListChangeListener<String>) change -> {
        int koko = nimet.size();
        IO.println("Listalla on nyt " + koko + " nimeä.");
    });

    // 3. Muutetaan dataa
    nimet.add("Denis");
    nimet.add("Antti-Jussi");

    // Application.launch(App.class, args);
}
```

Kun ajat koodin, näet, että aina kun `nimet.add()` suoritetaan, konsoliin
tulostuu tieto siitä, että nimi on lisätty. Teksti tulostuu aina kun
`nimet`-listaan tehdään muutos mistä päin ohjelmaa tahansa. 

`ObservableList`-olion oleellinen ero tavalliseen listaan on, että sillä on
`addListener`-metodi, jonka avulla voidaan rekisteröidä muuta koodia
havaitsemaan, kun listaan tehdään muutoksia. Jos lisäät alkioita tavalliseen
`ArrayList`-listaan, mikään toinen olio ei automaattisesti tiedä siitä, ellei se
erikseen käy tarkistamassa listan kokoa. `ObservableList` taas on aktiivinen.
Kun kutsumme `nimet.add()`, lista lähettää ilmoituksen kaikille muutoksista
kiinnostuneille, jotka ovat rekisteröityneet havaitsijoiksi
`addListener()`-metodin avulla. 

Yllä olevassa esimerkissä havaitsija on lambdalauseke, joka tulostaa konsoliin
listan koon muutoksen jälkeen. 

Lambdan `change`-parametri sisältää kuvauksen juuri tapahtuneesta
muutoksesta tai muutoksista, jos niitä tapahtui useita: mitä indeksejä muutos
koski, lisättiinkö vai poistettiinko alkioita, ja mitä alkioita lisättiin tai
poistettiin. Kyseisellä oliolla on käytettävissään metodeja, joiden avulla
voidaan selvittää muutokseen liittyviä yksityiskohtia, kuten `wasAdded()`,
`wasRemoved()`, `getAddedSubList()` ja `getRemoved()` ([ks.
JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.base/javafx/collections/ListChangeListener.Change.html)). 

Kokeillaan `change`-parametrin käyttöä. Lisätään kuuntelijaan ehto, jonka
perusteella listaan lisättäessä tulostetaan jotakin, mutta poistettaessa ei.

```java
//-// ==========================================
//-// ÄLÄ KOPIOI TÄTÄ PIILOSSA OLEVAA KOODIA.
//-// Tämä koodi on olemassa, jotta mdbookissa voidaan matkia ObservableList-luokan 
//-// toimintaa. JavaFX-sovelluksessa ObservableList on toteutettuna valmiiksi.
//-// ==========================================
//-static interface ListChangeListener<E> {
//-    void onChanged(Change<E> c);
//-    class Change<E> {
//-        boolean next = true, added;
//-        List<E> items;
//-        Change(boolean a, E item) { 
//-            added = a; 
//-            items = a ? Collections.singletonList(item) : Collections.emptyList(); 
//-        }
//-        boolean next() { boolean r = next; next = false; return r; }
//-        boolean wasAdded() { return added; }
//-        List<E> getAddedSubList() { return items; }
//-    }
//-}
//-
//-static class ObservableList<E> extends ArrayList<E> {
//-    List<ListChangeListener<E>> listeners = new ArrayList<>();
//-    void addListener(ListChangeListener<E> l) { listeners.add(l); }
//-    public boolean add(E e) {
//-        super.add(e);
//-        listeners.forEach(l -> l.onChanged(new ListChangeListener.Change<>(true, e)));
//-        return true;
//-    }
//-    public boolean remove(Object o) {
//-        if (super.remove(o)) {
//-            listeners.forEach(l -> l.onChanged(new ListChangeListener.Change<>(false, null)));
//-        }
//-        return true;
//-    }
//-}
//-
//-static class FXCollections {
//-    public static <E> ObservableList<E> observableArrayList() { return new ObservableList<>(); }
//-}
//-
public static void main(String[] args) {
    ObservableList<String> nimet = FXCollections.observableArrayList();

    nimet.addListener((ListChangeListener<String>) change -> {
        // HIGHLIGHT_GREEN_BEGIN
        while (change.next()) { // Käydään läpi kaikki tapahtuneet muutokset
            if (change.wasAdded()) { // Tarkistetaan, oliko muutos lisäys
                IO.println("Listalle lisättiin: " + change.getAddedSubList());
            }
        }
        // HIGHLIGHT_GREEN_END
        // Tämä osa koodista suoritetaan edelleen aina kuuntelijaa kutsuttaessa, 
        // riippumatta siitä, oliko muutos lisäys vai poisto
        int koko = nimet.size();
        IO.println("Listalla on nyt " + koko + " nimeä.");
    });

    nimet.add("Denis");
    nimet.add("Antti-Jussi");
    // HIGHLIGHT_GREEN_BEGIN
    nimet.add("Sami");
    nimet.remove("Denis");
    // HIGHLIGHT_GREEN_END
    
    // Application.launch(App.class, args);
}
```

Yllä olevan esimerkin `while (change.next())` on JavaFX:n tapa käsitellä
listalla tapahtuneita muutoksia. Yhdellä kertaa listaan saattaa tulla useita
muutoksia (esim. alkioiden lisäys, alkoiden poisto, alkioiden siirtäminen).
Silmukka varmistaa, että jokainen niistä käsitellään.

Kuuntelijoita voi olla useita. Jokainen `addListener(...)` rekisteröi uuden
kuuntelijan. Kun listassa tapahtuu muutos, JavaFX ilmoittaa siitä kaikille
kuuntelijoille yksi kerrallaan. Yksi havaitsija voi esimerkiksi päivittää
käyttöliittymää, toinen voi kirjoittaa lokia ja kolmas voi tehdä validointia.

<details><summary> Valinnaista lisätietoa: Miksi lambdalausekkeessa tarvitaan tyyppimuunnos? </summary>

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

### Kytkentä käyttöliittymään

JavaFX:ssä havaittavia olioita käytetään siten, että muutosten havaitsija on
jokin käyttöliittymässä oleva komponentti. Katsotaan vielä, miten tämä toimii
käytännössä.

Palauta `Main`-luokka alkuperäiseen tilaan, jossa `main()`-metodissa on
vain `Application.launch()`-kutsu. Ota sen jälkeen pohjaksi alla oleva valmis kontrolleriluokka
ja FXML-näkymä:

```java,ignore
// FILE: MainController.java
package fi.jyu.ohj2.esimerkit.observable;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;

import java.net.URL;
import java.util.ResourceBundle;

public class MainController implements Initializable {
    @FXML
    private TextField nimikentta;

    @FXML
    private Button nimipainike;

    @FXML
    private ListView<String> nimitulosteet;

    private ObservableList<String> nimet = FXCollections.observableArrayList();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

    }
}
// FILE_END
// FILE: main.fxml
<?xml version="1.0" encoding="UTF-8"?>

<?import javafx.scene.layout.VBox?>
<?import javafx.scene.control.TextField?>
<?import javafx.scene.control.Button?>
<?import javafx.scene.control.ListView?>
<?import javafx.geometry.Insets?>

<VBox prefWidth="400" prefHeight="400" alignment="CENTER" spacing="20.0" xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1" fx:controller="fi.jyu.ohj2.esimerkit.observable.MainController">
    <padding>
        <Insets bottom="20.0" left="20.0" right="20.0" top="20.0"/>
    </padding>

    <ListView fx:id="nimitulosteet" />
    <TextField fx:id="nimikentta" />
    <Button text="Lisää nimi" fx:id="nimipainike" />
</VBox>
// FILE_END
```

Kokeile ajaa sovellus, jonka pitäisi näyttää suunnilleen täältä:

<img src="images/list-app.png" width="300">

Kontrollerissa olevat attribuutit `nimikentta` ja `nimipainike` vastaavat
käyttöliittymässä olevaa kenttää ja painiketta. Puolestaan `nimet` on lista
nimistä käyttäen `ObservableList`-listaa; siis sama lista kuin ylempänä olevissa
esimerkeissä. Lopuksi `nimitulosteet` on `ListView`-komponentti
([JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.controls/javafx/scene/control/ListView.html)),
joka osaa näyttää `ObservableList`-listan sisällön käyttöliittymässä.
View-sanalla varustettuja komponentteja, kuten `ListView`, kutsutaan usein
*näkymäkomponenteiksi* (view component).

Alkuun `ListView` ei tiedä, minkä listan sisältöä näytetään. 
Kytketään nyt nimilista ja näkymäkomponentti toisiinsa kontrolleriluokassa:

```java,ignore
public void initialize(URL url, ResourceBundle resourceBundle) {
    // HIGHLIGHT_GREEN_BEGIN
    nimitulosteet.setItems(nimet);

    nimet.add("Denis");
    nimet.add("Antti-Jussi");
    nimet.add("Sami");
    // HIGHLIGHT_GREEN_END
}
```

Näin asetamme `nimitulosteet`-komponentin `nimet`-listan havaitsijaksi.
Varsinainen `addListener()`-kutsu tapahtuu `setItems()`-metodissa aivan samalla
tavalla kuin teimme itse aiemmin. Tämän kytkennän jälkeen meidän ei tarvitse
koskaan kutsua mitään "päivitä lista" -metodia. Kun koodissa tehdään
`nimet.add("Uusi nimi")`, nimi ilmestyy ruudulle automaattisesti. 

Tätä on tietysti vielä pikkuisen hankala nähdä, koska `initialize()`-metodissa
nimien lisäys kovakoodattuna. Lisätään vielä painikkeelle tapahtumankäsittelijä,
joka lisää listaan uuden nimen.

```java,ignore
public void initialize(URL url, ResourceBundle resourceBundle) {
    nimitulosteet.setItems(nimet);

    // HIGHLIGHT_RED_BEGIN
    nimet.add("Denis");
    nimet.add("Antti-Jussi");
    nimet.add("Sami");
    // HIGHLIGHT_RED_END

    // HIGHLIGHT_GREEN_BEGIN
    nimipainike.setOnAction(event -> {
        String teksti = nimikentta.getText();
        nimet.add(teksti);
        nimikentta.clear();
        nimikentta.requestFocus();
    });
    // HIGHLIGHT_GREEN_END
}
```

Kokeile nyt ajaa sovellus ja lisätä nimiä käyttöliittymän kautta.

<video src="images/list-app-works.mp4" controls></video>

TODO: Tämä kappale pois -- toistoa?
Huomaa: JavaFX havaitsee listan lisäyksiä ja huolehtii siitä, että näkymä vastaa
dataa. Näin malli ja näkymä ovat erillään toisistaan ja hoitavat omia
vastuitaan: malli vastaa datan tilasta ja käyttöliittymä vain datan
esittämisestä.

## Tehtävä malliluokaksi

Palataan nyt takaisin Todo-sovellukseemme. Tavoitteenamme olisi nyt mallintaa
kaikki tehtävän tila `Tehtava`-luokalla, jolloin tehtävästä tulisi todellinen
malliluokka. Puolestaan `VBox`- ja `CheckBox`-komponentit hoitaisivat vain datan
esittämisen. 

Aloitetaan lisäämällä `MainController`-luokkaan `ObservableList`-attribuutti, joka
toimii kaikkien tehtävien säiliönä.

```java,ignore
private ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList();
```

Muuta sitten `lisaaTehtava()`-metodi niin, että se ei enää lisää
`CheckBox`-komponenttia, vaan lisää uuden `Tehtava`-olion
listaamme. 

```java,ignore
private void lisaaTehtava() {
    String teksti = uusiTehtavaNimi.getText();
    if (teksti == null || teksti.isBlank()) {
        uusiTehtavaNimi.requestFocus();
        return;
    }
    teksti = teksti.trim();
    // HIGHLIGHT_RED_BEGIN
    tekemattomat.getChildren().add(luoCheckBox(teksti, false));
    // HIGHLIGHT_RED_END
    // HIGHLIGHT_GREEN_BEGIN
    tehtavat.add(new Tehtava(teksti, false));
    // HIGHLIGHT_GREEN_END
    uusiTehtavaNimi.clear();
    uusiTehtavaNimi.requestFocus();
    tallenna();
}
```

Vastaavasti voimme nyt muuttaa `tallenna()`-metodin toimintaa niin, että 
tallennamme suoraan `tehtavat`-listan, koska se on jatkossa ns. "totuuden
lähde".

```java,ignore
private void tallenna() {
    // HIGHLIGHT_RED_BEGIN
    List<Tehtava> kaikkiTehtavat = new ArrayList<>();
    kaikkiTehtavat.addAll(haeTehtavat(tekemattomat));
    kaikkiTehtavat.addAll(haeTehtavat(tehdyt));
    // HIGHLIGHT_RED_END
    ObjectMapper mapper = new ObjectMapper();
    // HIGHLIGHT_YELLOW_BEGIN
    mapper.writeValue(Path.of("tehtavat.json"), tehtavat);
    // HIGHLIGHT_YELLOW_END
}
```

Lisäksi `lataa()`-metodi yksinkertaistuu, kun voimme käyttää `addAll()`-metodia,
joka lisää kaikki alkiot kerralla:

```java,ignore
private void lataa() {
    Path path = Path.of("tehtavat.json");
    if (Files.notExists(path)) {
        return;
    }
    try {
        ObjectMapper mapper = new ObjectMapper();
        List<Tehtava> kaikkiTehtavat = mapper.readValue(path.toFile(), new TypeReference<>() {});
        // HIGHLIGHT_RED_BEGIN
        kaikkiTehtavat.forEach(tehtava -> {
            CheckBox checkbox = luoCheckBox(tehtava.getTeksti(), tehtava.getTehty());
            if (tehtava.getTehty()) {
                tehdyt.getChildren().add(checkbox);
            } else {
                tekemattomat.getChildren().add(checkbox);
            }
        });
        // HIGHLIGHT_RED_END
        // HIGHLIGHT_GREEN_BEGIN
        tehtavat.addAll(kaikkiTehtavat);
        // HIGHLIGHT_GREEN_END
    } catch (JacksonException je) {
        IO.println("JSONin lukeminen epäonnistui: " + je.getMessage());
    }
}
```

Nyt tehtävien luominen, tallentaminen ja lataaminen on toiminnallisesti erotettu
käyttöliittymän komponenteista. Toisin sanoen, `Tehtava`-luokka ja
`tehtavat`-lista muodostavat yhdessä sovelluksen mallin.

Luonnollisesti muutoksen seurauksena nyt sovelluksen avaaminen ja tehtävien
lisääminen ei näy käyttöliittymässä, koska mallin ja käyttöliittymän välillä ei
ole mitään kytkentää. Toteutetaan nyt käyttöliittymän päivittäminen tehtävien
perusteella.

Tässä kohtaa on myös luontevaa muuttaa myös `luoCheckBox`-metodin esittelyrivi.
Aiemmin annoimme sille parametrina tekstin ja valintatiedon erikseen
(`String, boolean`), mutta nyt kun meillä on koko `Tehtava`-olio käytettävissä,
annetaan se suoraan parametrina. Näin metodi saa kaiken tarvitsemansa tiedon
yhdellä kertaa.

```java,ignore
// HIGHLIGHT_YELLOW_BEGIN
private CheckBox luoCheckBox(Tehtava t) {
    CheckBox tehtava = new CheckBox(t.getTeksti());
    tehtava.setSelected(t.getTehty());
// HIGHLIGHT_YELLOW_END
    // metodin loppuosa piilotettu...
//-    tehtava.setOnAction(event -> {
//-        if (tehtava.isSelected()) {
//-            tekemattomat.getChildren().remove(tehtava);
//-            tehdyt.getChildren().add(tehtava);
//-        } else {
//-            tehdyt.getChildren().remove(tehtava);
//-            tekemattomat.getChildren().add(tehtava);
//-        }
//-        tallenna();
//-    });
//-    return tehtava;
}
```

Tehdään nyt käyttöliittymän päivittämiseen apumetodi `paivitaNakyma`.

```java,ignore
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

Nyt voimme kytkeä kaiken yhteen. Kuitenkin nyt sen sijaan, että
`paivitaNakyma()` kutsuttaisiin tehtävien lisäämisen tai lataamisen yhteydessä,
kytkemme malli ja näkymä löyhästi `ObservableList`-listan avulla. Lisätään
listalle havaitsija, joka pävittää näkymän ja tallentaa tehtävät aina, kun
tehtävälista muuttuu:


```java
public void initialize(URL url, ResourceBundle resourceBundle) {
    // HIGHLIGHT_GREEN_BEGIN
    tehtavat.addListener((ListChangeListener<Tehtava>) change -> {
        paivitaNakyma();
        tallenna();
    });
    // HIGHLIGHT_GREEN_END

    // metodin loppuosa piilotettu...
//-    lataa();
//-    uusiTehtavaNimi.setOnAction(event -> lisaaTehtava());
//-    lisaaUusiTehtavaPainike.setOnAction(event -> lisaaTehtava());
}
```

Koska nyt tallennuskin tapahtuu aina, kun lista muuttuu, voimme myös poistaa erillisen
`tallenna()`-metodikutsun `lisaaTehtava()`-metodista:

```java,ignore
private void lisaaTehtava() {
    // metodin alkuosa piilotettu...
//-    String teksti = uusiTehtavaNimi.getText();
//-    if (teksti == null || teksti.isBlank()) {
//-        uusiTehtavaNimi.requestFocus();
//-        return;
//-    }
//-    teksti = teksti.trim();
//-    tehtavat.add(new Tehtava(teksti, false));
//-    uusiTehtavaNimi.clear();
//-    uusiTehtavaNimi.requestFocus();
    // ...
    // HIGHLIGHT_RED_BEGIN
    tallenna();
    // HIGHLIGHT_RED_END
}
```

Jos kokeilet sovellusta nyt, tiedostosta ladatut tiedostot näkyvät
käyttöliittymässä, ja uusien tehtävien lisääminen toimii.

## CheckBox-tapahtuma muuttaa mallia

Tällä hetkellä `luoCheckBox`-metodi sisältää edelleen logiikkaa, joka siirtelee
checkboxia käsin VBox-säiliöiden välillä. Tässä on nyt hieman turhaa toistoa
näkymän päivittämiseen verrattuna, joten otetaan jo tässä vaiheessa vanha koodi
pois:

```java,ignore
private CheckBox luoCheckBox(Tehtava t) {
    CheckBox tehtava = new CheckBox(t.getTeksti());
    tehtava.setSelected(t.getTehty());
    tehtava.setOnAction(event -> {
        // HIGHLIGHT_RED_BEGIN
        if (tehtava.isSelected()) {
            tekemattomat.getChildren().remove(tehtava);
            tehdyt.getChildren().add(tehtava);
        } else {
            tehdyt.getChildren().remove(tehtava);
            tekemattomat.getChildren().add(tehtava);
        }
        tallenna();
        // HIGHLIGHT_RED_END
    });
    return tehtava;
}
```

Nyt meidän on muutettava ajattelutapaa. Valintaruudun klikkaamisen ei tulisi
siirtää itse itseään, vaan ainoastaan muuttaa mallia. Puolestaan kun malli
muuttuu, `tehtavat`-listan havaitsija päivittää näkymää
`paivitaNakyma()`-metodia käyttäen.

Tässä vaiheessa `Tehtava`-olio ei *vielä* osaa ilmoittaa sisäisen tilansa
muuttumisesta. Jos kutsuisimme vain `tehtava.setTehty(true)`, `ObservableList`
ei huomaisi tällä hetkellä mitään, koska itse listaan ei tullut uutta oliota. 

Juuri nyt kierrämme ongelmaa mallintamalla tilan muuttumista poistamalla vanha
tehtävä ja lisäämällä uusi tehtävä, jonka tehty tila on päinvastainen.
Samalla uudelleennimetään vielä `CheckBox`-olion muuttuja kuvaavammin, koska se
ei enää mallinna tehtävää, vaan on pelkästään valintaruutu:

```java
private CheckBox luoCheckBox(Tehtava t) {
    CheckBox cb = new CheckBox(t.getTeksti());
    cb.setSelected(t.getTehty());
    cb.setOnAction(event -> {
        // MUUTOS: Emme enää siirrä komponenttia käsin VBoxista toiseen.
        // Sen sijaan päivitämme mallilistaa, mikä laukaisee näkymän päivityksen.
        // HIGHLIGHT_GREEN_BEGIN
        tehtavat.remove(t);
        tehtavat.add(new Tehtava(t.getTeksti(), !t.getTehty()));
        // HIGHLIGHT_GREEN_END
    });
    return cb;
}
```

Nyt valintaruudun toiminta on suoraviivaisempi:

1. Käyttäjä klikkaa valintaruutua.
2. `luoCheckBox`-metodin `setOnAction`-tapahtumakäsittelijä muuttaa mallilistaa (`remove` ja `add`).
   Tässä vaiheessa VBox-komponentteihin ei vielä kosketa.
3. `tehtavat`-listan kuuntelija (`addListener`) huomaa, että listan sisältö
   muuttui.
4. Kuuntelija kutsuu `paivitaNakyma()`- ja `tallenna()`-metodeja.
5. Vasta nyt `paivitaNakyma()` tyhjentää VBoxit ja rakentaa ne uudestaan mallin
   uuden tilan mukaiseksi.

Erityiesti valintaruudun vastuu on nyt yksikäsitteinen: mallin muuttaminen.

Mainittakoon, että tämä ratkaisu on hieman tehoton. Nyt koko käyttöliittymä
rakennetaan uudestaan yhden klikkauksen takia. Toisaalta checkbox-olion tilan
muuttaminen aiheuttaa kaksi erillistiä muutosta `tehtavat`-listaan: vanhan
`Tehtava`-olion poiston ja uuden `Tehtava`-olion lisäyksen. Toisin sanoen,
`paivitaNakyma()` tulee kutsutuksi kahdesti aina, kun valintaruutua klikataan.
Tämä on tietysti vähän turhaa, mutta toimii, koska `ObservableList` huomaa
molemmat muutokset ja päivittää näkymän automaattisesti.

Saavutimme kuitenkin päätavoitteemme: sovelluksen tilan ja sen muutoksen
mallintaminen on siirtynyt `tehtavat`-listan ja `Tehtava`-olioiden vastuulle.

<task>
  <task-title>Tehtävä 8.1: Todo-sovellus, vaihe 7. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-1-todo-7/handout.md}}

</handout>
</task>
