# Johdetut Observable-arvot

Käyttöliittymässä monesti halutaan näyttää varsinaisen tiedon lisäksi tiedoista
laskettuja arvoja, kuten arvojen summaa, keskiarvoa, yhdistelmää tai vastaavaa.
Johdettua arvoja voidaan laskea suoraan, kuten:

```java,ignore
String henkilonNimiSukunimi = ihminen.getNimi() + ihminen.getSukunimi();
```

Kuitenkin johdettu arvo ei havaitse alkuperäisten arvojen muutoksia: jos ihmisen
nimi tai sukunimi muuttuu, ihmisen yhdistetty nimi-sukunimi ei päivity
automaattisesti.

## Esimerkki

Olkoon meillä seuraava sovellus henkilön tietojen syöttämiseksi:

```java,ignore
// FILE: MainController.java
public class MainController implements Initializable {
    @FXML
    private TableColumn<Pelaaja, String> nimiColumn;

    @FXML
    private TableColumn<Pelaaja, Number> syntymavuosiColumn;

    @FXML
    private TableColumn<Pelaaja, Number> ikaColumn;

    @FXML
    private TableView<Pelaaja> pelaajatTable;

    @FXML
    private Label pelaajiaLkmLabel;

    @FXML
    private Button lisaaPelaajaButton;

    private ObservableList<Pelaaja> pelaajat = FXCollections.observableArrayList();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        nimiColumn.setCellFactory(TextFieldTableCell.forTableColumn());
        nimiColumn.setCellValueFactory(cellData -> cellData.getValue().nimiProperty());

        syntymavuosiColumn.setCellFactory(TextFieldTableCell.forTableColumn(new NumberStringConverter("####")));
        syntymavuosiColumn.setCellValueFactory(cellData -> cellData.getValue().syntymavuosiProperty());

        // Tämä ei toimi!
        // setCellValueFactory vaatii ObservableValue-arvon, mutta ikä on int-kokonaisluku
        // ikaColumn.setCellValueFactory(cellData -> LocalDate.now().getYear() - cellData.getValue().getSyntymavuosi());

        lisaaPelaajaButton.setOnAction(event -> {
            Pelaaja uusiPelaaja = new Pelaaja();
            uusiPelaaja.setNimi("Uusi Pelaaja");
            uusiPelaaja.setSyntymavuosi(2000);
            pelaajat.add(uusiPelaaja);
        });

        pelaajatTable.setItems(pelaajat);
    }
}
// FILE_END
// FILE: Pelaaja.java
public class Pelaaja {
    StringProperty nimi = new SimpleStringProperty();
    IntegerProperty syntymavuosi = new SimpleIntegerProperty();

    public StringProperty nimiProperty() { return nimi; }

    public String getNimi() { return nimi.get(); }

    public void setNimi(String nimi) { this.nimi.set(nimi); }

    public IntegerProperty syntymavuosiProperty() { return syntymavuosi; }

    public int getSyntymavuosi() { return syntymavuosi.get(); }

    public void setSyntymavuosi(int syntymavuosi) { this.syntymavuosi.set(syntymavuosi); }
}
// FILE_END
// FILE: main.fxml
<?xml version="1.0" encoding="UTF-8"?>

<?import javafx.geometry.Insets?>
<?import javafx.scene.control.Button?>
<?import javafx.scene.control.Label?>
<?import javafx.scene.control.TableColumn?>
<?import javafx.scene.control.TableView?>
<?import javafx.scene.layout.HBox?>
<?import javafx.scene.layout.VBox?>

<VBox alignment="CENTER" spacing="20.0" xmlns="http://javafx.com/javafx/25" xmlns:fx="http://javafx.com/fxml/1" fx:controller="fi.ohj2.esimerkit.bindingstest.MainController">
    <padding>
        <Insets bottom="20.0" left="20.0" right="20.0" top="20.0" />
    </padding>
   <children>
      <TableView fx:id="pelaajatTable" editable="true" prefHeight="200.0" prefWidth="200.0">
        <columns>
          <TableColumn fx:id="nimiColumn" prefWidth="200.0" text="Nimi" />
          <TableColumn fx:id="syntymavuosiColumn" prefWidth="50.0" text="Syntymävuosi" />
            <TableColumn fx:id="ikaColumn" editable="false" prefWidth="50.0" text="Ikä" />
        </columns>
         <columnResizePolicy>
            <TableView fx:constant="CONSTRAINED_RESIZE_POLICY" />
         </columnResizePolicy>
      </TableView>
      <HBox VBox.vgrow="NEVER">
         <children>
            <Label text="Pelaajia: " />
            <Label fx:id="pelaajiaLkmLabel" text="0" />
         </children>
      </HBox>
      <Button fx:id="lisaaPelaajaButton" mnemonicParsing="false" text="Lisää pelaaja" />
   </children>
</VBox>
// FILE_END
```

Tässä esimerkissä on pari ongelmaa:

- Uuden pelaajan lisääminen ei päivitä pelaajien lukumäärää
- Pelaajan syntymävuoden muokkaaminen ei päivitä pelaajan ikää

<video src="images/bindings-1.mp4" controls></video>

## `Observable`-arvon muuttaminen toiseksi arvoksi

Kaikki `ObservableValue`-arvot, kuten `StringProperty`, `IntegerProperty`,
`FloatProperty`, jne. sisältävät `map()`-apumetodin (ks.
[JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.base/javafx/beans/value/ObservableValue.html#map(java.util.function.Function))),
jonka avulla arvolle voi suorittaa laskutoimituksia.
Esimerkiksi pelaajan iän saa laskettua syntymävuodesta seuraavasti:

```java,ignore
ObservableValue<Number> ika = pelaaja.syntymavuosiProperty().map(vuosi -> LocalDate.now().getYear() - vuosi.intValue());
```

Tällöin `ika`-muuttujan sisältämä arvo lasketaan syntymävuodesta kaavalla
`LocalDate.now().getYear() - vuosi.intValue()` aina, kun pelaajan syntymävuosi
muuttuu.
Koska `ObservableValue` on havaittava arvo, voi sen voi käyttää
`setCellValueFactory`-metodissa:

```java,ignore
public void initialize(URL url, ResourceBundle resourceBundle) {
    nimiColumn.setCellFactory(TextFieldTableCell.forTableColumn());
    nimiColumn.setCellValueFactory(cellData -> cellData.getValue().nimiProperty());

    syntymavuosiColumn.setCellFactory(TextFieldTableCell.forTableColumn(new NumberStringConverter("####")));
    syntymavuosiColumn.setCellValueFactory(cellData -> cellData.getValue().syntymavuosiProperty());

    // HIGHLIGHT_GREEN_BEGIN
    ikaColumn.setCellValueFactory(cellData -> 
        cellData.getValue().syntymavuosiProperty().map(
            syntymavuosi -> LocalDate.now().getYear() - syntymavuosi.intValue()));
    // HIGHLIGHT_GREEN_END

    lisaaPelaajaButton.setOnAction(event -> {
        Pelaaja uusiPelaaja = new Pelaaja();
        uusiPelaaja.setNimi("Uusi Pelaaja");
        uusiPelaaja.setSyntymavuosi(2000);
        pelaajat.add(uusiPelaaja);
    });

    pelaajatTable.setItems(pelaajat);
}
```

## Funktion muuttaminen `Observable`-arvoksi

Pelaajan lukumäärää saadaan selville aina kutsumalla `pelaajat.size()`.
`size()`-metodi ei kuitenkaan ole havaittava. Lisäksi `pelaajat`-lista ei
sisällä yllä mainittua `map()`-metodia.
Voimme kuitenkin muuntaa minkä tahansa funktion havaittavaksi käyttämällä
`Bindings`-luokan (ks.
[JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.base/javafx/beans/binding/Bindings.html#))
`createXBinding`-apumetodeja. Tässä `X` tarkoittaa havaittavan arvon tyyppiä,
eli esimerkiksi `Integer`, `Long`, `String` tai `Object`.
Koska `size()` on kokonaisluku, käytämme
`Bindings.createIntegerBinding()`-metodia (ks.
[JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.base/javafx/beans/binding/Bindings.html#createIntegerBinding(java.util.concurrent.Callable,javafx.beans.Observable...))).

```java,ignore
IntegerBinding pelaajienLkm = Bindings.createIntegerBinding(() -> pelaajat.size(), pelaajat);
```

`Bindings.createIntegerBinding()` ottaa vähintään kaksi parametria:
lambdalausekkeen, josta havaittava arvo lasketaan ja yhden tai useamman
`Observalbe`-arvon, jonka muuttuessa havaittava arvo lasketaan uudestaan.
Tässä tapauksessa ensimmäinen paremetri kertoo, että `pelaajienLkm`-arvo lasketaan aina
lausekkeella `pelaajat.size()`. Toinen parametri `pelaajat` kertoo, että arvo on
päivitettävä aina, kun `pelaajat`-listan sisältö muuttuu.

`Bindings.createXBinding`-metodi palauttaa `Binding`-tyyppisen havaittavan
arvon, jonka voi käyttää samalla tavalla kuin muut `Observable`-arvot.
Tässä tapauksessa voimme sitoa `pelaajiaLkmLabel`-kentän tekstin
`textProperty()`-arvoon:

```java,ignore
public void initialize(URL url, ResourceBundle resourceBundle) {
    nimiColumn.setCellFactory(TextFieldTableCell.forTableColumn());
    nimiColumn.setCellValueFactory(cellData -> cellData.getValue().nimiProperty());

    syntymavuosiColumn.setCellFactory(TextFieldTableCell.forTableColumn(new NumberStringConverter("####")));
    syntymavuosiColumn.setCellValueFactory(cellData -> cellData.getValue().syntymavuosiProperty());

    ikaColumn.setCellValueFactory(cellData -> cellData.getValue().syntymavuosiProperty().map(syntymavuosi -> LocalDate.now().getYear() - syntymavuosi.intValue()));

    lisaaPelaajaButton.setOnAction(event -> {
        Pelaaja uusiPelaaja = new Pelaaja();
        uusiPelaaja.setNimi("Uusi Pelaaja");
        uusiPelaaja.setSyntymavuosi(2000);
        pelaajat.add(uusiPelaaja);
    });

    // HIGHLIGHT_GREEN_BEGIN
    IntegerBinding pelaajienLkm = Bindings.createIntegerBinding(() -> pelaajat.size(), pelaajat);
    pelaajiaLkmLabel.textProperty().bind(pelaajienLkm.asString());
    // HIGHLIGHT_GREEN_END

    pelaajatTable.setItems(pelaajat);
}
```

`Property`-tyypin `bind()`-metodi sitoo arvon johonkin toiseen havaittavaan
arvoon. Tässä tapauksessa pelaajien lukumäärän nimiön teksti sidotaan
pelaajien lukumäärään. Tällöin, jos `pelaajat`-lista muuttuu, niin

- `pelaajienLkm`-arvo havaitsee muutoksen ja laskee arvonsa uudestaan lausekkeella `pelaajat.size()`
- `pelaajienLkm.asString()` havaitsee muutoksen `pelaajienLkm`-arvossa ja
  päivittää arvonsa kutsumalla `pelaajienLkm.toString()`
- `pelaajiaLkmLabel.textProperty()` havaitsee muutoksen `pelaajienLkm.asString()`-arvossa
  ja päivittää oman sisältönsä vastaamaan uutta arvoa

