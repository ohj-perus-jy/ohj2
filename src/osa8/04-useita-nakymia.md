# Useita näkymiä ja tehtävän muokkaus

On hyvin tavallista, että sovelluksessa on useampiakin näkymiä kuin vain
pääikkuna. Halusimme esimerkiksi aiemmin avata erillisen muokkausikkunan
valitulle tehtävälle taulukkoa tuplaklikkaamalla. JavaFX:ssä voi olla rinnakkain
useita ikkunoita auki (_Stage_), joista kukin esittää omaa näkymäänsä (_Scene_).
Voidaan myös ladata kokonaan uusi _Scene_ ja vaihtaa se olemassa olevan _Stagen_
sisälle.

Tässä osassa opimme avaamaan uuden dialogin (`Stage`), joka pysäyttää muun
ohjelman suorituksen (eli on _modaalinen_), ja miten sille siirretään dataa
muokattavaksi. Muistetaan edellisistä luvuista `Tehtavakokoelma` ja observable
propertyt – kun avaamme muokkausikkunan ja muokkaamme sille annettua
`Tehtava`-oliota, meidän ei tarvitse kertoa asiasta erikseen `TableView`:lle!

## 1. Muokkausnäkymän FXML

Rakenna SceneBuilderissä tai käsin haluamasi näköinen muokkausdialogi. Siellä
voisi olla esimerkiksi tekstikentät otsikolle ja kuvaukselle sekä `ComboBox`
prioriteetille. Tallenna esimerkiksi nimellä `MuokkausNakyma.fxml` ui-pakettiin.

```xml
<?xml version="1.0" encoding="UTF-8"?>

<!-- Tässä tyypillisesti VBox tai GridPane pääelementtinä -->
<VBox xmlns="http://javafx.com/javafx" xmlns:fx="http://javafx.com/fxml" 
      fx:controller="fi.jyu.ohj2.nimi.todo.ui.MuokkausController">
      
   <TextField fx:id="otsikkoKentta" promptText="Tehtävän otsikko"/>
   <TextArea fx:id="kuvausKentta" promptText="Kuvaus" />
   <ComboBox fx:id="prioriteettiCombo" />
   
   <HBox>
       <Button text="Tallenna" onAction="#tallenna" />
       <Button text="Peruuta" onAction="#peruuta" />
   </HBox>
</VBox>
```

Asetimme FXML-koodien `fx:controller`-attribuutiksi `MuokkausController`-luokan
nimen. SceneBuilderin oikean reunan alapaneelista "Controller" voit syöttää
tämän myös graafisesti.

## 2. Ohjainluokka (MuokkausController)

Meidän täytyy voida syöttää `MuokkausControllerille` se `Tehtava`-olio, jota
käyttäjä klikkasi, ennen kuin ikkuna näytetään hänelle.

Tehdään `ui`-pakettiin seuraavanlainen luokka:

```java
package fi.jyu.ohj2.nimi.todo.ui;

import fi.jyu.ohj2.nimi.todo.model.Prioriteetti;
import fi.jyu.ohj2.nimi.todo.model.Tehtava;
import javafx.fxml.FXML;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

public class MuokkausController {
    @FXML private TextField otsikkoKentta;
    @FXML private TextArea kuvausKentta;
    @FXML private ComboBox<Prioriteetti> prioriteettiCombo;

    private Tehtava muokattava; // Controller säilöö viitteen operoitavaan dataan

    @FXML
    public void initialize() {
        // Alustetaan combo-boksin asetusarvot enumista
        prioriteettiCombo.getItems().setAll(Prioriteetti.values());
    }

    // Metodi, jota kutsumme ennen dialogin avaamista
    public void setTehtava(Tehtava t) {
        this.muokattava = t;
        // Päivitetään heti näkymän alkuarvot datan perusteella
        otsikkoKentta.setText(t.getOtsikko());
        kuvausKentta.setText(t.getKuvaus());
        prioriteettiCombo.setValue(t.getPrioriteetti());
    }

    @FXML
    private void tallenna() {
        // Otetaan kenttien tekstit talteen itse olioon
        muokattava.setOtsikko(otsikkoKentta.getText());
        muokattava.setKuvaus(kuvausKentta.getText());
        muokattava.setPrioriteetti(prioriteettiCombo.getValue());

        // Lopuksi suljetaan dialogi-akkuna (stage)
        sulje();
    }

    @FXML
    private void peruuta() {
        // Jos peruutetaan, taustalla olevaa Tehtava-oliota ei muokata lainkaan
        sulje();
    }

    private void sulje() {
        // Ovela tapa hakea Stage minkä tahansa komponentin kautta ja sulkea se
        Stage stage = (Stage) otsikkoKentta.getScene().getWindow();
        stage.close();
    }
}
```

Huomaa kuinka tämä controller toimii yhdellä ainoalla tehtävällä tietämättä
mitään isoista sovellusrakenteista kuten tallennuspaikasta. Kun set-metodeja
kutsutaan (`muokattava.setOtsikko(...)`), `ObservableList`:ssä roikkuva
alkuperäinen `Tehtava`-olio lähettää ilmoituksen (observablena), johon
`TableView` on valmiiksi tarttunut. Niinpä alkuperäinen taulukkonäkymä päivittyy
lennosta!

### Validointi

Tallennusta ei pidä sallia, jos otsikko on tyhjä. Käyttäjän syötteet on aina
syytä tarkistaa (validoida) ennen kuin niitä sijoitetaan malliolioon. Voimme
päivittää `tallenna()`-metodiamme siten, että se hylkää virheelliset syötteet:

```java
@FXML
private void tallenna() {
    String otsikko = otsikkoKentta.getText();
    
    // Nollataan mahdolliset aiemmat virhetyylit
    otsikkoKentta.setStyle("");
    otsikkoKentta.setTooltip(null);
    
    if (otsikko == null || otsikko.isBlank()) {
        // Vaihdetaan reunus punaiseksi virheen merkiksi
        otsikkoKentta.setStyle("-fx-border-color: red; -fx-border-width: 2px;");
        
        // Asetetaan Tooltip, joka näkyy kun käyttäjä vie hiiren kentän päälle
        Tooltip virhe = new Tooltip("Tehtävän otsikko ei saa olla tyhjä!");
        otsikkoKentta.setTooltip(virhe);
        
        return; 
    }

    // Jos kaikki on kunnossa, päivitetään malliolio
    muokattava.setOtsikko(otsikko.trim());
    muokattava.setKuvaus(kuvausKentta.getText().trim());
    muokattava.setPrioriteetti(prioriteettiCombo.getValue());

    sulje();
}
```

> [!NOTE]
> **Miksi emme käytä tässä suoraan databindingiä (bindBidirectional)?**
>
> Olisihan se kätevää sitoa tekstikenttä suoraan olion propertyyn, eikö vain?
> Mutta jos tekisimme niin
> (`otsikkoKentta.textProperty().bindBidirectional(muokattava.otsikkoProperty())`),
> jokainen näppäimen painallus muuttaisi dataa välittömästi taustalla. Jos
> käyttäjä kirjoittaisi jotain väärin tai iskisikin lopulta
> "Peruuta"-painiketta, alkuperäinen `Tehtava` olisi jo ehditty pilata ja
> tallentaa levylle taulukon havahtumisen myötä.
>
> Siksi otamme syötteet vastaan tavallisina tekstikenttinä, **validoimme ne
> ensin**, ja vasta painettaessa "Tallenna" siirrämme hyväksytyt syötteet
> varsinaiseen malliolioon.

## 3. Pääohjain lataa uuden näkymän (MainController)

Pääkontrollerissa (`MainController`) tehtävänämme on nyt lisätä ohjeet
taulukolle, että tuplaklikkaaminen edellyttää operaatioita (toinen mahdollisuus
olisi tietysti erillinen "Muokkaa"-painike).

Lisäämme `MainControllerin` `initialize`-logiikkaan tapahtumankuuntelijan
(`RowFactory` kielellä):

```java
public void initialize() {
    // ...
    // täällä oli valmiina sarakkeiden setCellValueFactory jne.

    // Asetetaan taulukolle ohje, miten luoda ja käsitellä rivejä (TableRows)
    tehtavaTaulu.setRowFactory(tv -> {
        TableRow<Tehtava> row = new TableRow<>();
        
        // Jokaista riviä voi ns. klikata. Asetamme tälle toiminnon.
        row.setOnMouseClicked(event -> {
            // Jos oli tuplaklikkaus ETKÄ tyhjän rivialueen klikkaus (jolla ei dataa)
            if (event.getClickCount() == 2 && (!row.isEmpty())) {
                Tehtava kohde = row.getItem();
                avaaMuokkausikkuna(kohde);
            }
        });
        return row;
    });
}
```

Itse lataus-metodi uusia FXML-tiedostoja (näkymiä) varten noudattaa tuttua
`FXMLLoader`-syntaksia:

```java
private void avaaMuokkausikkuna(Tehtava tehtava) {
    try {
        // Ladataan FXML luoden samalla Stage-olio sille
        FXMLLoader loader = new FXMLLoader(getClass().getResource("MuokkausNakyma.fxml"));
        // Huom: täytyy importata javafx.scene.Parent ja javafx.scene.Scene puitteissa
        Parent root = loader.load();

        // Koska määritimme controllerin näkymässä, FXML-loader tiesi luoda meille ohjaimen. Voimme napata sen!
        MuokkausController ohjain = loader.getController();
        // Nyt voimme tunkea halutun dataolion uuden ohjaimen muistiin!
        ohjain.setTehtava(tehtava);

        Stage tyovaihe = new Stage();
        tyovaihe.setTitle("Muokkaa tehtävää");
        // Modaalinen = et voi klikkailla alkuperäistä pääikkunaa samalla
        tyovaihe.initModality(Modality.APPLICATION_MODAL); 
        tyovaihe.setScene(new Scene(root));
        
        // Pysäyttää ohjelman suorituksen (ohjaimen näkökulmasta) edellisen näkymän osalta kunnes dialogi tapetaan
        tyovaihe.showAndWait(); 
        
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

## Yhteenveto

1. Muokkausnäkymällä tehtiin oma ohjain. FXML-tiedoston
   `fx:controller`-attribuutti kertoo mikä java-ohjain on kyseessä.
2. `MainController` lataa tiedoston (`FXMLLoader.load()`), joka synnyttää
   ohjainolion valmiiksi muistiin.
3. Hakemalla ohjaimen (`loader.getController()`) pystyimme kutsumaan omaa
   metodia (`setTehtava`) antaen datan (valitun taulukkorivin tiedon) uuden
   ikkunan muistiin.
4. Muutokset on heti käytössä koko ohjelman laajudella `ObservableList`-taikojen
   ansiosta kun dialogin savea painettiin!

## Tehtävät

<task>
  <task-title>Tehtävä 8.4: TODO-ohjelma, vaihe 10. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-4-todo-10/handout.md}}

</handout>
</task>
