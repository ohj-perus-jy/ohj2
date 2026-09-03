# SceneBuilder

> [!Osaamistavoitteet]
> - Osaat käyttää SceneBuilder-työkalua JavaFX-käyttöliittymien luomiseen
> - Osaat yhdistää FXML-tiedoston ja kontrolleriluokan

> [!TÄRKEÄÄ]
>
> Tästä luvusta alkaen tarvitset SceneBuilder-työkalun.
> 
> Asenna työkalu seuraamalla [kurssin työkaluohjeita](../tyokalut.md#scenebuilder).

SceneBuilder on visuaalinen työkalu, joka helpottaa JavaFX-käyttöliittymien
luomista. Se tarjoaa drag-and-drop-käyttöliittymän, jonka avulla voit luoda ja
muokata FXML-tiedostossa määriteltyä käyttöliittymää ilman FXML:n kirjoittamista
käsin. SceneBuilderin avulla voit helposti lisätä komponentteja, määrittää
niiden ominaisuuksia ja järjestää ne haluamallasi tavalla. Se on erityisen
hyödyllinen, jos et ole vielä tottunut kirjoittamaan FXML:ää suoraan tai haluat
nopeuttaa käyttöliittymän suunnitteluprosessia.

SceneBuilderin päänäkymässä on kolme pääaluetta.

## Ensimmäinen komponentti

Avataan nyt alkuun projektimme `main.fxml`-näkymätiedosto SceneBuilderissä.

Avaa SceneBuilder ja valitse vasemmasta alalaidasta **Open Project**.
Hae ja avaa `src/resources/pakkaus`-kansiosta `main.fxml` (tässä `pakkaus`
viittaa edellisessä vaiheessa luotun projektin pääpakkauksen alikansioita).
Nyt sama käyttöliittymä, jonka näimme IDEAssa, pitäisi näkyä SceneBuilderissä:

<img src="images/scenebuilder-main-annotated.png">

Tutustutaan samalla SceneBuilderin käyttöliittymään:

1. **Suunnittelunäkymä.** Tässä näet FXML-tiedoston
   määrittelemän käyttöliittymän visuaalisena esityksenä. Voit tässä raahata
   komponentteja ja järjestää niitä haluamallasi tavalla.

2. **Inspector-näkymä.** Löydät tästä muun muassa *Properties*-, *Layout*-
   ja *Code*-paneeleja. Näissä paneeleissa voi muuttaa
   valitun komponentin ominaisuuksia, kuten tekstiä, fonttia, väriä sekä
   asettelua ja määrittää komponentin ja kontrollerin liittämiseen
   liittyvät asetukset.

3. **Library-näkymä.** Löydät tästä kaikki käytettävissä olevat komponentit, kuten painikkeet,
   tekstikentät, layout-komponentit ja niin edelleen.
   Saat lisättyä komponentit käyttöliittymään raahaamalla ne suunnittelunäkymään.

4. **Document-näkymä.** Näet tässä sovelluksesi kaikki komponentit puurakenteessa.
   Voit käyttää tämän näkymän komponenttien tarkkaan valintaan, siirtämiseen ja poistamiseen.

 * Vasemmalla on kaksi paneelia: **Library** ja **Document**. Library-paneelista
   löydät kaikki käytettävissä olevat komponentit, kuten painikkeet,
   tekstikentät, layout-komponentit ja niin edelleen. Document-paneelissa näet
   hierarkkisen esityksen oman sovelluksesi käyttöliittymän rakenteesta.
 
Suunnittelunäkymässä on valmiina painike, eli `Button`-komponentti sekä nimiö eli
`Label`-komponentti. Jos napsautat `Button`-komponenttia, näet oikealla
Properties-paneelissa kyseisen komponentin ominaisuuksia. Voit muuttaa
esimerkiksi tekstiä, fonttia, väriä ja monia muita ominaisuuksia.

Kokeile alkuun muokata painikkeen tekstiä. Klikkaa suunnittelunäkymässä olevasta
painikkeesta, jolloin painikkeen perusominaisuudet ilmestyvät Inspector-näkymän
Properties-paneeliin:

<img src="images/scenebuilder-button-props.png">

Muuta painikkeen *Text*-ominaisuus arvoon `Lisää tehtävä` ja paina <kbd>Enter</kbd>.
Huomaa, että painikkeen teksti päivittyy samalla suunnittelunäkymässä.

Tallenna muutokset (**File** <i class="bi bi-chevron-right"></i> **Save**).
Kokeile nyt ajaa sovellus taas IDEA:n kautta. Huomaat, että painikkeen teksti muuttui.

## Käyttöliittymän hierarkkinen rakenne

Vasemmalla olevassa Document-paneelissa näet käyttöliittymän rakenteen, joka
muistuttaa hierarkiaa: `Button` ja `Label`-komponentit ovat `VBox`-komponentin
lapsia. `VBox` (Vertical Box, eli "pystysuuntainen laatikko") on
layout-komponentti, joka järjestää lapsikomponentit automaattisesti
pystysuoraan. 

JavaFX:ssä on paljon vastaavia valmiita `Pane`-luokasta periytyviä luokkia,
jotka auttavat järjestelemään käyttöliittymää kokonaisuuksiin sen sijaan, että
kaikki komponentit olisivat yhdessä läjässä suoraan ikkunan alaisuudessa. 

 * `HBox`-komponentti järjestää lapsensa vaakasuoraan,
 * `GridPane`-komponentti järjestää lapsensa ruudukkomaisesti,
 * `BorderPane`-komponentti järjestää lapsensa reunoille ja keskelle, ja niin
edelleen. 

Näiden komponenttien avulla voidaan luoda monimutkaisiakin
käyttöliittymiä, jotka skaalautuvat hyvin eri kokoisiksi ikkunoiksi.

## Syöttökenttä

Lisätään nyt käyttöliittymään syöttökenttä, johon käyttäjä voi kirjoittaa.
Valitse vasemmalta **Library-näkymän** paneeleista **Controls** <i class="bi bi-chevron-right"></i> **`TextField`** ja raahaa se `VBox`-komponentin sisään,
aiemman tekstikentän ja painikkeen väliin:

<video src="images/scenebuilder-textfield-drag.mp4" controls></video>

(Mikäli pudotit tekstikentän väärään paikkaan, voit peruuttaa muutokset
painamalla <kbd>Ctrl</kbd>+<kbd>Z</kbd> tai <kbd>⌘</kbd>+<kbd>Z</kbd>)

Tallenna muutokset (**File** <i class="bi bi-chevron-right"></i> **Save**)
ja kokeile vielä käynnistää sovellus IDEA:ssa. Huomaat, että sovellukseen
ilmestyi syöttökenttä, johon voi kirjoittaa tekstiä.

<details><summary><i class="bi bi-stars jyu-gold"></i>Bonus: Missä käyttöliittymä on määritelty?</summary>

Avaa IDEA:ssa `resources`-kansiossa oleva `main.fxml`.
Tiedoston pitäisi näyttää nyt suunnilleen seuraavalta:

```xml
<?xml version="1.0" encoding="UTF-8"?>

<?import javafx.geometry.Insets?>
<?import javafx.scene.control.Button?>
<?import javafx.scene.control.Label?>
<?import javafx.scene.control.TextField?>
<?import javafx.scene.layout.VBox?>

<VBox alignment="CENTER" spacing="20.0" xmlns="http://javafx.com/javafx/25" xmlns:fx="http://javafx.com/fxml/1" fx:controller="fi.jyu.ohj2.dezhidki.todo.MainController">
    <padding>
        <Insets bottom="20.0" left="20.0" right="20.0" top="20.0" />
    </padding>

    <Label text="Hello, JavaFX!" />
   <TextField />
    <Button text="Lisää tehtävä" />
</VBox>
```

FXML-tiedosto sisältää käyttöliittymän näkymän määrittelyn käyttäen
tekstuaalista esittelymuotoa.
Vertaa tekstitiedostoa SceneBuilderissa olevaan hierarkiarakenteeseen:

<img src="images/scenebuilder-hierarchy.png">

SceneBuilder on siten yksinkertaisuudessaan sovellus, joka osaa lukea ja tuottaa
FXML-käyttöliittymätiedostoja.

</details>

## FXML:n ja kontrolleriluokan yhdistäminen

Painikkeesta ei vielä tapahdu mitään. Jotta voimme käsitellä käyttöliittymän
tapahtumia, kuten painikkeen klikkaus, meidän on luotava yhteys FXML-tiedoston
ja kontrolleriluokan välille. Tämä tapahtuu kahdessa vaiheessa: antamalla
komponenteille tunnisteet SceneBuilderissä ja määrittelemällä vastaavat
muuttujat Java-koodissa.

### Tunnisteiden määrittäminen komponenteille

FXML:ssä jokaisella komponentilla, jota haluamme hallita ohjelmallisesti, täytyy 
olla yksilöllinen tunniste. Lisätään alkuun tunnisteet painikkeelle ja
syöttökentälle ja kokeillaan tulostaa kenttään kirjoitettu teksti konsoliin.

Valitse SceneBuilderissa syöttökenttä ja valitse Inspector-näkymän alapuolella
oleva Code-paneeli:

<video src="images/scenebuilder-code-panel.mp4" controls></video>

Aseta tunnisteen eli *fx:id*-kentän arvoksi jokin uniikki komponenttia kuvaava
nimi käyttäen `camelCase`-kirjoitustyyliä, esimerkiksi `uusiTehtavaNimi`.
Vahvista muutos painamalla <kbd>Enter</kbd>.
Toista sama painikkeelle ja anna sen tunnisteeksi `lisaaUusiTehtavaPainike`.

Tallenna lopuksi FXML-tiedosto.

### Komponenttien määrittäminen kontrollerissa

Saatoit huomata, että heti tunnisteen määrittämisen jälkeen SceneBuilder
näyttää varoituksen "No injectable field found":

<img src="images/scenebuilder-inject-warning.png">

Korjataan varoitus lisäämällä tunnistetta vastaavat attribuutit
kontrolleriluokkaan. Voit toistaiseksi tyhjentää varoituksen painamalla
**Clear**-painiketta, sillä SceneBuilder ei tyhjennä varoituksia automaattisesti.

Palaa IDEAan ja avaa `MainController.java`. Lisää luokkaan kaksi attribuuttia
luokan alkuun:

```java,ignore
@FXML
private Button lisaaUusiTehtavaPainike;

@FXML
private TextField uusiTehtavaNimi;
```

Korjaa mahdolliset import-määreiden puute lisäämällä `import`-määreet 
`javafx.scene.control`-pakkauksessa oleviin `Button` ja `TextField`-luokkiin:

<video src="images/intellij-component-imports.mp4" controls></video>

> [!TÄRKEÄÄ]
> Muuttujan nimen on oltava täsmälleen sama kuin SceneBuilderissä määritellyn
> *fx:id*-arvon. JavaFX yhdistää komponentit ja attribuutit toisiinsa käyttäen
> tunnistetta. Jos tunnisteet eivät täsmää, JavaFX ei osaa yhdistää niitä.

Kokeile kääntää ja ajaa ohjelma uudestaan. Ohjelman pitäisi toimia kuten
ennenkin.

Mitä tämä käytännössä teki? Kun ohjelma käynnistyy, `App`-luokassa määritelty
`FXMLLoader`-olio lukee `main.fxml`-tiedoston ja huomaa siellä määritellyt
komponentit sekä niiden *fx:id*-tunnisteet. Tämän jälkeen se
luo ilmentymän `MainController`-luokasta ja etsii `@FXML`-*annotaatiolla*
merkityt attribuutit. Lopuksi lataaja asettaa annotoitujen attribuuttien arvoksi
komponenttien oliot attribuutin nimen ja *fx:id*-tunnisteen perusteella.
Siispä `FXMLLoader` tekee puolestamme jotakuinkin seuraavaa:

```java,ignore
// Älä kopioi.
// FXMLLoader tekee tämän meidän puolestamme käyttäen attribuutin nimeä ja
// fx:id-asetuksen arvoa.
this.uusiTehtavaNimi = (TextField)findComponentById("uusiTehtavaNimi");
// Tämän jälkeen uusiTehtavaNimi sisältää näkymässä olevan TextField-komponentin olion.
```

## Kontrollerin elinkaari ja `initialize`-metodi

Jos kontrolleri toteuttaa `Initializable`-rajapinnan, JavaFX kutsuu metodin
automaattisesti, kun FXML-tiedosto on täysin ladattu ja kontrolleriluokassa
olevat attribuutit on alustettu.
Tämä on oikea paikka määritellä komponenttien käyttäytymiseen liittyviä toimintoja.

Lisätään alkuun `initialize()`-metodiin seuraava rivi testataksemme, että
syöttökentän olio on todellakin käytettävissä koodista.

```java,ignore
uusiTehtavaNimi.requestFocus();
```

Aja ohjelma uudestaan. Nyt heti ohjelman käynnistyessä syöttökenttä aktivoituu,
eli se saa ns. *fokuksen*, ikään kuin kenttää olisi klikattu:

<img src="images/todo-app-focus.png">

## Tapahtumien käsittely

Pelkän fokuksen lisääminen on vielä hieman tylsää. Lisätään sovellukselle
toiminnallisuus, että painiketta klikattaessa konsoliin tulostetaan
tekstikentässä oleva teksti.

JavaFX-sovelluksissa kaikenlaiset vuorovaikutukset komponenttien kanssa 
muodostavat *tapahtumia*. Esimerkiksi painikkeen painaminen, näppäimen
painaminen syöttökentässä, tekstin kopioiminen tai liittäminen, kaikki
muodostavat erilaisia tapahtumia.
Käyttöliittymän ohjelmointi onkin yleisesti sitä, että ensin määritellään
käyttöliittymässä näkyvät osat ja sitten reagoidaan osien tapahtumiin.

Reagointi tapahtumiin JavaFX:ssä tapahtuu lisäämällä komponenteille
*tapahtumakäsittelijät* käyttäen muun muassa 
komponenttien `setOn`-alkavia metodeja. `setOn`-metodit ottavat parametrina
funktioviitteen tai lambdalausekkeen, joka kutsutaan, kun tapahtuma laukeaa.

Lisätään painikkeelle nyt yleinen toimintatapahtuma `setOnAction`-metodia.
Tämä `action`-tapahtuma laukeaa, kun käyttäjä vuorovaikuttaa komponentin kanssa
komponentille ominaisella tavalla. Painikkeiden tapauksessa `action`-tapahtuma
laukeaa painiketta klikkaamalla tai painamalla <kbd>Enter</kbd>-painiketta, kun
fokus on painikkeessa.
Huomaa, että muissa komponenteissa `action`-tapahtuma voi merkitä jotain toista
komponentille ominaista vuorovaikutusta.

Lisää `initialize()`-metodiin tapahtumakäsittelijä
`lisaaUusiTehtavaPainike`-painikkeelle käyttäen `setOnAction`-metodia.
Tässä vaiheessa painikkeen painaminen käsitellään hakemalla tekstikentän sisältö
ja tulostamalla se näytölle:

```java,ignore
lisaaUusiTehtavaPainike.setOnAction(event -> {
    String teksti = uusiTehtavaNimi.getText(); // Haetaan tekstikentän sisältö
    IO.println("Tekstikentän sisältö: " + teksti); // Tulostetaan se konsoliin
});
```

<details><summary>Lisätietoa: Miksi emme lisää tapahtumankäsittelijää suoraan konstruktorissa?</summary>

Syy liittyy JavaFX:n alustuksen järjestykseen ja siihen, milloin
FXML-komponentit ovat saatavilla. 

Kun käynnistät JavaFX-sovelluksen, tapahtuu seuraavaa:

1. JavaFX luo kontrollerin kutsumalla konstruktoria `new MainController()`.
2. `@FXML`-kentät ovat tässä vaiheessa vielä `null`.
3. `FXMLLoader` lukee FXML-tiedoston ja injektoi kenttiin oikeat komponentit
   `fx:id`-arvojen perusteella.
4. Lopuksi kutsutaan `initialize()`-metodi.

Jos siis kirjoitat konstruktoriin koodia, joka käyttää FXML-komponentteja, saat
`NullPointerException`in. Voit kokeilla tätä itse kirjoittamalla
tapahtumankäsittelijän konstruktorin sisään:

```java,ignore
public MainController() {
    uusiTehtavaNimi.requestFocus();
    lisaaUusiTehtavaPainike.setOnAction(event -> {
        String teksti = uusiTehtavaNimi.getText();
        IO.println(teksti);
    });
}
```

Yllä olevassa esimerkissä sekä `lisaaUusiTehtavaPainike` että `uusiTehtavaNimi`
ovat konstruktorin aikana vielä `null`.

Siksi tapahtumankäsittelijät ja muut FXML-komponentteihin nojaavat alustukset
tehdään `initialize()`-metodissa.

</details>

Tallenna ja käynnistä sovellus. 
Nyt kun painiketta klikataan, konsoliin tulostuu tekstikentän sisältö:

<video src="images/todo-app-field-works.mp4" controls></video>

Meillä on nyt alustava graafinen "Hei maailma!" -sovellus! 🥳

## Tekstikentän sisällön näyttäminen ikkunassa

Tekstin tulostuminen konsoliin on kylläkin mukavaa, mutta todellisessa
sovelluksessa on harvoin konsoli samaan aikaan auki. 
Muutetaankin sovellusta vielä niin, että syöttökenttään kirjoitettu teksti
lisätään yläpuolella olevaan nimiökomponenttiin.

Mene SceneBuilderiin ja valitse `Label`-nimiökomponentti, jossa lukee nyt
"Hello, JavaFX!". Ensin, valitse Inspector-näkymästä Properties-paneeli
ja poista Text-asetuksesta kaikki teksti. Nimiö jää silloin tyhjäksi:

<img src="images/scenebuilder-label-cleanup.png">

Lisää sen jälkeen nimiölle *fx:id*-asetukseen tunniste Code-paneelista.
Anna tunnisteeksi esimerkiksi `tekemattomat`.
Tallenna FXML-tiedosto.

Lisää kontrolleriluokkaan nimiötä vastaava attribuutti:

```java,ignore
@FXML
private Label tekemattomat;
```

Lisää tarpeelliset `import`-määreet. Mikäli IntelliJ tarjoaa useita vaihtoehtoja
`Label`-luokalle, valitse `javafx.scene.control`-pakkauksessa oleva vaihtoehto.

Muokkaa aiemmin tekemääsi tapahtumankäsittelijää niin, että
teksti lisätäänkin nimiöön:

```java,ignore
lisaaUusiTehtavaPainike.setOnAction(event -> {
    String teksti = uusiTehtavaNimi.getText();
    // HIGHLIGHT_RED_BEGIN
    IO.println("Tekstikentän sisältö: " + teksti);
    // HIGHLIGHT_RED_END
    //HIGHLIGHT_GREEN_BEGIN
    tekemattomat.setText(tekemattomat.getText() + teksti + "\n");
    //HIGHLIGHT_GREEN_END
});
```

Tallenna ja aja. Nyt painikkeen painaminen lisää tekstin syötekentän yläpuolelle
olevaan nimiöön aina omalle rivilleen:

<video src="images/todo-app-label-print.mp4" controls></video>

Saatoit huomata, että toisen rivin lisääminen ei näy ellei ikkunan kokoa
suurenna. Korjaamme ikkunankokoon liittyvät ongelmat tämän tutoriaalin osan lopussa.

<task>
  <task-title num="7.2">Todo-sovellus, vaihe 2<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/7-2-todo-2/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa7/tehtava1">Tee tehtävä TIMissä</a></task-link>
</task>