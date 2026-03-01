# Sovelluslogiikan ja käyttöliittymän yhdistäminen

Sovelluksemme voisi jo nyt toimia eräänlaisena Todo-listana.
Palautetaan kuitenkin vielä mieleen, mitä ominaisuuksia suunnittelimme tämän
osan alussa:

* Käyttäjä voi lisätä uuden tehtävän
* Käyttäjä näkee listan kaikista tehtävistä
* Käyttäjä voi merkitä tehtävän tehdyksi
* Käyttäjä voi poistaa tehtävän
* Käyttäjä voi palauttaa tehdyn tehtävän takaisin tekemättömäksi
* Tehtävät tallennetaan tiedostoon, jotta ne säilyvät sovelluksen sulkemisen jälkeen
* Tehtävät haetaan tiedostosta sovelluksen käynnistyessä

Näitä huomioon ottaen sovelluksemme ei ole vielä kovin käytettävä: tehtäviä
voidaan lisätä, ja pystymme näkemään kaikki tehtävät, mutta tehtäviä ei voi
poistaa eikä merkitä tehdyksi.

Muutetaan käyttöliittymä siten, että tehtävät näytetään valintaruutuina,
jolloin ne voi merkitä tehdyksi tai tekemättömäksi. Lisäksi listataan tehdyt ja
tekemättömät tehtävät omaan listaan. Piirretään alustava
wireframe-suunnitelmakuva:

<img src="images/todo-app-wireframe.png">

Yllä oleva kuva on piirretty käyttäen
[wireframe.cc](https://wireframe.cc/Mq98ie) -palvelua, mutta vastaavia
suunnitelmakuvia voidaan piirtää millä tahansa piirtotyökalulla. 
Yleisesti ottaen käyttöliittymiä on hyvä suunnitella hieman etukäteen, jotta 
sen toteuttaminen olisi suoraviivaisempaa.

## Komponenttien luominen dynaamisesti 

Aloitetaan ensin muuttamalla painikkeen toimintaa niin, että uusi tehtävä
lisätään käyttöliittymään valintaruutuna, eli ns. `CheckBox`-komponenttina.
Koska käyttäjä voi lisätä uusia tehtäviä rajattomasti, emme voi
lisätä valintaruutuja SceneBuilderin kautta. Sen sijaan lisäämme komponentteja
suoraan kontrollerin koodissa.

Valmistellaan ensiksi käyttöliittymä. Mene SceneBuilderiin ja poista siellä
oleva `Label`-nimiökomponentti. Koska nimiössä ei ole oletuksena tekstiä, 
sitä ei pysty klikkaamaan suunnittelunäkymässä.
Sen sijaan valitse nimiö käyttäen vasemmalla puolella olevan Document-näkymän
Hierarchy-paneelia:

<video src="images/scenebuilder-hierarchy-panel-select.mp4"></video>

Poista nimiö painamalla <kbd>Delete</kbd> (macOS: <kbd>⌫ delete</kbd>).
Saat varoituksen "This component has an fx:id. Do you really want to delete
it?" sen merkiksi, että nimiökomponenttia käytetään kontrollerin koodissa.
Valitse varoitusdialogissa **Delete**.

Tämän jälkeen etsi `VBox`-komponentti Library-näkymästä (**Library** 
<i class="bi bi-chevron-right"></i> **Containers** 
<i class="bi bi-chevron-right"></i> **VBox**
) ja raahaa se tekstikentän yläpuolelle:

<img src="images/scenebuilder-vbox-add.png" >

`VBox` (**V**ertical **Box**) on ns. *sisältökomponentti*, joka on tarkoitettu
muiden komponenttien ryhmittelyyn ja asetteluun. Sisältökomponentteihin voi
lisätä muita elementteja, joita sisältökomponentti asettelee sille ominaisella
tavalla. Esimerkiksi `VBox` asettelee kaikki sen sisällä olevat komponentit
pystysuorasti ylhäältä alas.

Anna uudelle `VBox`-komponentille fx:id-tunnisteeksi `tekemattomat`, eli sama
kuin poistetun nimiökomponentin. Tallenna FXML-tiedosto ja muokkaa sitten `MainController`-luokka niin,
että `tekemattomat`-attribuutin tyyppi on jatkossa `VBox`:


```java,ignore
// HIGHLIGHT_RED_BEGIN
@FXML
private Label tekemattomat;
// HIGHLIGHT_RED_END
// HIGHLIGHT_GREEN_BEGIN
@FXML
private VBox tekemattomat;
// HIGHLIGHT_GREEN_END
```

Nyt tapahtumankäsittelijä ei enää toimi, koska
`VBox`-komponentti ei sisällä `getText`/`setText`-metodia. 
Sen sijaan `VBox`-komponentin oleellinen metodi on `getChildren()`, joka
palauttaa listan kaikista sen sisältämistä komponenteista.
Muokataankin painikkeen tapahtumakäsittelijä niin, että painikkeen painalluksesta
alustetaan uusi `CheckBox`-olio ja lisätään se `VBox`-komponenttiin.
Tällöin tapahtumakäsittelijästä tulee seuraavanlainen:

```java,ignore
lisaaUusiTehtavaPainike.setOnAction(event -> {
    String teksti = uusiTehtavaNimi.getText();
    CheckBox tehtava = new CheckBox(teksti);
    tekemattomat.getChildren().add(tehtava);
});
```

Kokeile ajaa sovellus tässä vaiheessa. Huomaat, että "Lisää tehtävä" -painike
luo uuden valintaruutukomponentin ja lisää sen syöttökentän yläpuolelle.
Valintaruudut ovat klikattavissa ikään kuin merkiksi siitä, onko tehtävä
tehty:

<video src="images/todo-app-checbox-add.mp4" controls></video>

Parannetaan sovelluksen käytettävyyttä hieman tässä vaiheessa. Ensiksi, jos
"Lisää tehtävä" -painiketta painaa ilman, että syöttökenttään kirjoittaa mitään,
sovellukseen ilmestyy tyhjä valintaruutu. Lisäämme järkevyystarkistuksen: jos
tekstikentästä haettu teksti on `null`-viite, ei sisällä mitään tekstiä tai
sisältää vain välilyöntejä, lopetetaan tapahtumankäsittely kesken.
Tämä onnistuu `String`-tyypin `isBlank()`-metodilla.
Lisäksi, poistetaan tehtävän alusta ja lopusta turhia välilyöntejä, jos käyttäjä
saattaa kirjoittaa ne vahingossa käyttäen `trim()`-metodia:

```java,ignore
lisaaUusiTehtavaPainike.setOnAction(event -> {
    String teksti = uusiTehtavaNimi.getText();
    // HIGHLIGHT_GREEN_BEGIN
    if (teksti == null || teksti.isBlank()) {        
        return; 
    }
    teksti = teksti.trim();
    // HIGHLIGHT_GREEN_END
    CheckBox tehtava = new CheckBox(teksti);
    tekemattomat.getChildren().add(tehtava);
});
```

Toiseksi, tehtävän lisääminen jättää tehtävätekstin syöttökenttään, jolloin
uuden tehtävän lisäämistä varten joudumme kumittamaan pois vanhan tekstin.
Käytetään sitä varten `TextField`-komponentin `clear()`-metodia, jolla
me tyhjennämme tekstikentän sisällön aina tehtävän lisäämisen lopuksi:

```java,ignore
lisaaUusiTehtavaPainike.setOnAction(event -> {
    String teksti = uusiTehtavaNimi.getText();
    if (teksti == null || teksti.isBlank()) {        
        return; 
    }
    teksti = teksti.trim();
    CheckBox tehtava = new CheckBox(teksti);
    tekemattomat.getChildren().add(tehtava);
    // HIGHLIGHT_GREEN_BEGIN
    uusiTehtavaNimi.clear();
    // HIGHLIGHT_GREEN_END
});
```

Kolmanneksi, tehtävän lisäämisen jälkeen joudumme klikkaamaan syöttökentästä
ennen kuin seuraavan tehtävän kirjoittamista. Tehdään tämä klikkaus
ohjelmallisesti käyttäen `requestFocus()`-metodia, joka siirtää fokuksen eli
ikään kuin simuloi komponentin valintaa. 
Huomaa, että metodi on lisättävä kaikkiin kohtiin, jossa tapahtumankäsittely
päättyy:

```java,ignore
lisaaUusiTehtavaPainike.setOnAction(event -> {
    String teksti = uusiTehtavaNimi.getText();
    if (teksti == null || teksti.isBlank()) {        
        // HIGHLIGHT_GREEN_BEGIN
        uusiTehtavaNimi.requestFocus(); 
        // HIGHLIGHT_GREEN_END
        return; 
    }
    teksti = teksti.trim();
    CheckBox tehtava = new CheckBox(teksti);
    tekemattomat.getChildren().add(tehtava);
    uusiTehtavaNimi.clear();
    // HIGHLIGHT_GREEN_BEGIN
    uusiTehtavaNimi.requestFocus(); 
    // HIGHLIGHT_GREEN_END
});
```

<details><summary><i class="bi bi-stars jyu-gold"></i>Bonus: Fokuksen automaattinen asettaminen tapahtuman lopuksi </summary>

Nyt hieman ärsyttävästi joudumme asettamaan fokuksen kahteen kohtaan.

Eräs JavaFX-tyylinen tapa ratkaista ongelma on käyttää
`Platform.runLater()`-metodia ([JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.graphics/javafx/application/Platform.html#runLater(java.lang.Runnable))), joka ajaa
sille annettavan koodin myöhemmin sovelluksen aikana (mutta aikaisintaan
sen tapahtuman jälkeen, jona metodia kutsuttiin).
Metodi ottaa parametrina `Runnable`-rajapintaa toteuttavan olion. Koska
`Runnable` on funktionaalinen (ks. [Luku 6.1](../osa6/01-funktiorajapinnat-ja-lambda-lausekkeet.md#valmiita-funktiorajapintoja)), voimme
antaa parametrina lambdalausekkeen tai funktioviitteen metodiin, joka ei ota
mitään parametreja eikä palauta mitään.
Koska `requestFocus()`-metodi täsmää parametrien ja palautusarvon kannalta
`Runnable`-rajapinnan kanssa, voimme käyttää funktioviitettä suoraan.
Tällöin tapahtumankäsittely yksinkertaistuu muotoon:

```java,ignore
lisaaUusiTehtavaPainike.setOnAction(event -> {
    Platform.runLater(uusiTehtavaNimi::requestFocus);
    String teksti = uusiTehtavaNimi.getText();
    if (teksti == null || teksti.isBlank()) {        
        return; 
    }
    teksti = teksti.trim();
    CheckBox tehtava = new CheckBox(teksti);
    tekemattomat.getChildren().add(tehtava);
    uusiTehtavaNimi.clear();
});
```

Toinen tapa on soveltaa geneerisia metodeja (ks. [luku
4.4](../osa4/04-tyyppiparametrit-ja-geneerisyys.md#geneerinen-metodi)) sekä 
funktionaalisia rajapintoja (ks. [luku
6.1](../osa6/01-funktiorajapinnat-ja-lambda-lausekkeet.md)).
Koska lambdalausekkeita voidaan ottaa parametrina ja toisaalta palauttaa arvona,
voimme tehdä apumetodin `ajaJaFokusoi`, joka ottaa parametrina
tapahtumakäsittelijän ja palauttaa uuden tapahtumakäsittelijän, joka kutsuu
`requestFocus` aina lopuksi:

```java,ignore


static <T extends Event> EventHandler<T> ajaJaFokusoi(EventHandler<T> kasittelija, Node komponentti) {
    return e -> {
        kasittelija.handle(e);
        komponentti.requestFocus();
    };
}
```

Tällaista metodia, joka palauttaa parametrina annetun funktion pienellä
muutoksella, kutsutaan yleensä ns. *käärijämetodiksi* tai *wrapper-metodiksi*.
Nimensä mukaan metodi siis "käärii" alkuperäisen funktion toisen sisään.

Apumetodin avulla voimme yksinkertaistaa tapahtumankäsittelijän muotoon:

```java,ignore
lisaaUusiTehtavaPainike.setOnAction(ajaJaFokusoi(event -> {
    String teksti = uusiTehtavaNimi.getText();
    if (teksti == null || teksti.isBlank()) {
        return;
    }
    teksti = teksti.trim();
    CheckBox tehtava = new CheckBox(teksti);
    tekemattomat.getChildren().add(tehtava);
    uusiTehtavaNimi.clear();
}, uusiTehtavaNimi));
```

Huomaa, että kaikki JavaFX-komponentin perivät `Node`-luokasta.
</details>

Lopuksi, tehtävän lisääminen vaatii aina "Lisää tehtävä" -painikkeen painamista.
Tehokäyttäjälle voisi olla kätevämpi lisätä tehtäviä myös
<kbd>Enter</kbd>-painiketta käyttäen, jolloin uusia tehtäviä voi lisätä 
paljon nopeammin.
Huomaamme, että `TextField`-komponentin `onAction`-tapahtuma laukeaa, kun
käyttäjä painaa <kbd>Enter</kbd>-painiketta kentässä (ks.
[JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.controls/javafx/scene/control/TextField.html#setOnAction(javafx.event.EventHandler))).
Lisätään siis myös `uusiTehtavaNimi`-syöttökentälle tapahtumankäsittelijä
käyttäen `setOnAction`-metodia. Koska haluamme käsitellä näppäimen painallusta
ja tekstikentän <kbd>Enter</kbd>-painiketta samalla tavalla, refaktoroidaan
samalla tapahtumankäsittely omaksi metodiksi:

```java,ignore
public void initialize(URL url, ResourceBundle resourceBundle) {
    lisaaUusiTehtavaPainike.setOnAction(event -> lisaaTehtava());
    uusiTehtavaNimi.setOnAction(event -> lisaaTehtava());
}

private void lisaaTehtava() {
    String teksti = uusiTehtavaNimi.getText();
    if (teksti == null || teksti.isBlank()) {
        uusiTehtavaNimi.requestFocus();
        return;
    }
    teksti = teksti.trim();
    CheckBox tehtava = new CheckBox(teksti);
    tekemattomat.getChildren().add(tehtava);
    uusiTehtavaNimi.clear();
    uusiTehtavaNimi.requestFocus();
}
```

Kokeillaan nyt vielä ajaa sovellus ja testataan, että kaikki toimii.
Muutosten myötä sovellus on nyt hieman käytettävämpi:

- Tehtävien lisääminen ei onnistu jos tekstikenttä on tyhjä
- Tehtävän lisääminen tyhjentää tekstikentän ja palauttaa fokuksen siihen
  nopeampaa kirjoittamista varten
- Tehtäviä voidaan lisätä myös painamalla <kbd>Enter</kbd>-painiketta

<video src="images/todo-app-usability.mp4" controls></video>

## Käsitellyt tehtävät

Jatketaan sovelluksen toimintojen edistämistä. Muutetaan sovellusta niin, että
käsitellyt tehtävät ovat aina erillään tekemättömistä, jolloin tehtävien
tekemistä on helpompaa seurata.

Palaa SceneBuilderiin ja lisää uusi `VBox`-komponentti tekemättömien tehtävien
`VBox`-komponentin alle. Anna samalla uudelle `VBox`-komponentin
*fx:id*-tunnisteeksi `tehdyt`:

<img src="images/scenebuilder-tehdyt-vbox.png" width="600">

Tallenna FXML-tiedosto, ja määrittele kontrolleriluokkaan vastaava `VBox
tehdyt` -attribuutti:

```java,ignore
@FXML
private VBox tehdyt;
```

Tehdään niin, että aina, kun valintaruutua klikataan, tehtävä siirtyy
tekemättömästä tehdyksi ja samalla siirtyy ylemmästä alempaan
`VBox`-komponenttiin.
Huomaamme, että `CheckBox`-komponentti perii `ButtonBase`-luokan,
jolloin `onAction`-tapahtuma laukeaa aina, kun valintaruutupainiketta klikataan
(ks.
[JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.controls/javafx/scene/control/CheckBox.html)).
Muutetaan `lisaaTehtava()`-metodia niin, että valintaruudun
`onAction`-tapahtumalle asetetaan käsittelijä. Tapahtumankäsittelijässä ensiksi
poistamme valintaruudun `tekemattomat`-säiliökomponentista ja lisätään se
`tehdyt`-säiliökomponenttiin:


```java,ignore
private void lisaaTehtava() {
    // metodin alku piilotettu...
//-    String teksti = uusiTehtavaNimi.getText();
//-    if (teksti == null || teksti.isBlank()) {
//-        uusiTehtavaNimi.requestFocus();
//-        return;
//-    }
//-    teksti = teksti.trim();
    CheckBox tehtava = new CheckBox(teksti);
    // HIGHLIGHT_GREEN_BEGIN
    tehtava.setOnAction(event -> {
        tekemattomat.getChildren().remove(tehtava);
        tehdyt.getChildren().add(tehtava);
    });
    // HIGHLIGHT_GREEN_END
    tekemattomat.getChildren().add(tehtava);
    // metodin loppu piilotettu...
//-    uusiTehtavaNimi.clear();
//-    uusiTehtavaNimi.requestFocus();
}
```

<!-- 
DZ: En saanut tätä toistettua. Ilmeisesti add automaattisesti poistaa checkboxin tekemattomat-vboxista (?)


 Huomaa, että tapahtumakäsittelijässä *ensiksi poistamme* valintaruudun
 tekemättömien tehtävien säiliöstä ja *sitten lisätään* tehtyjen tehtävien säiliöön.
 **JavaFX:ssä sama komponenttiolio saa olla vain yhden toisen komponentin sisällä.**
 Jos sen sijaan yrittäisimme ensin lisätä valintaruutu tehtyihin tehtäviin ja
 sitten poistaa tekemättömistä, aiheutuisi siitä virhe:

 ```java,ignore
 tehdyt.getChildren().add(tehtava); // VIRHE: tehtava on jo tekemattomat-säiliössä
 tekemattomat.getChildren().remove(tehtava);
 ``` 
 
-->

Kokeile ajaa sovellusta. Nyt tehtävän klikkaaminen siirtää sen alempaan
`VBox`-säiliöön.
Klikkaamalla jo tehtyä
tehtävää se ei kuitenkaan siirry takaisin tekemättömiin. 
Lisäksi, jos katsot IDEAssa konsoliin, näet poikkeuksen:

```
java.lang.IllegalArgumentException: Children: duplicate children added: parent = VBox[id=tehdyt]
```

Poikkeus kertoo, että yritämme lisätä
samaa `CheckBox`-komponenttia uudestaan `tehdyt`-säiliöön, vaikka se on jo
siellä. Muokataan logiikkaa niin, että jos tehtävä merkittiin tehdyksi,
siirretään se tehtyihin ja jos tehtävä merkittiin tekemättömäksi, siirretään se
takaisin tekemättömiin. 
Voimme käyttää tässä `CheckBox`-komponentin `isSelected()`-metodia,
joka kertoo, onko valintaruutu valittu tai ei (ks.
[JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.controls/javafx/scene/control/CheckBox.html#isSelected())).
Tällöin tapahtumakäsittely muuttuu seuraavaan muotoon:


```java,ignore
tehtava.setOnAction(event -> {
    if (tehtava.isSelected()) { // Tehtävä valittu --> Siirretään tehtyjen joukkoon
        tekemattomat.getChildren().remove(tehtava);
        tehdyt.getChildren().add(tehtava);
    } else { // Tehtävä ei-valittu--> Siirretään takaisin tekemättömien joukkoon
        tehdyt.getChildren().remove(tehtava);
        tekemattomat.getChildren().add(tehtava);
    }
});
```

Kokeile nyt ajaa sovellus. Tehtävien merkkaaminen tehdyksi pitäisi nyt siirtää
ne alempaan säiliöön. Vastaavasti tehtävien merkkaaminen tekemättömäksi siirtää
ne takaisin ylös:

<video src="images/todo-app-checkbox-move.mp4" controls></video>

Huomaa, että `isSelected()`-metodilla on jo tiedossaan "uusi" arvo, onko
komponentti valittuna vai ei. 
Tilan päivitys tapahtuu ennen `setOnAction`-tapahtuman laukeamista. 
Kun käyttäjä klikkaa valintaruutua, tapahtumaketju on karkeasti seuraava:

 * Hiiren painallus rekisteröityy käyttöjärjestelmään.
 * JavaFX päivittää sisäisen `selected`-ominaisuuden (esim. `false` -> `true`).
 * `ActionEvent` luodaan ja `setOnAction`-käsittelijä suoritetaan.
 * Käsittelijän suoritus: Kun kutsut tässä vaiheessa `isSelected()`, saat jo uuden, päivitetyn tilan.


## Nimiöt säiliöille

Tehdään vielä pieni muutos parantaakseen käyttäjäystävällisyyttä.
Lisää yksi nimiökomponentti (`Label`) tekemättömien tehtävien säiliön
yläpuolelle ja aseta sen Text-attribuutiksi `TODO`.
Sen jälkeen lisää vielä yksi nimiökomponentti tehtyjen tehtävien säiliön
yläpuolelle ja aseta sen Text-attribuutiksi `TEHTY`:

<img src="images/scenebuilder-vbox-label.png">

Tallenna FXML-tiedosto ja kokeile vielä ajaa sovellus IDEA:sta varmistaksesi,
että kaikki vieläkin toimii.

<task>
  <task-title>Tehtävä 7.4: Todo-sovellus, vaihe 4. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/7-4-todo-4/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa7/tehtava4">Tee tehtävä TIMissä</a></task-link>
</task>

