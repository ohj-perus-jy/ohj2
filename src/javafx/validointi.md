# Tietojen validointi

Tietojen validoinnilla tarkoitetaan käyttäjän antamien tietojen oikeellisuuden
tarkistusta.
Validoinnilla varmistetaan, että käyttäjän muutokset eivät tuota
kohdealueen kannalta epäkelpoa tietomallia.

## Esimerkki

Olkoon meillä seuraavanlainen yksinkertainen sovellus:

```java,ignore
// FILE: MainController.java
public class MainController implements Initializable {
    @FXML
    private ListView<Lemmikki> lemmikitList;

    @FXML
    private TextField nimiField;

    @FXML
    private TextField lajiField;

    @FXML
    private Button lisaaButton;

    ObservableList<Lemmikki> lemmikit = FXCollections.observableArrayList();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        lemmikitList.setItems(lemmikit);
        
        lisaaButton.setOnAction(_ -> lisaaLemmikki());
    }

    private void lisaaLemmikki() {
        Lemmikki lemmikki = new Lemmikki();
        lemmikki.setNimi(nimiField.getText());
        lemmikki.setLaji(lajiField.getText());
        lemmikit.add(lemmikki);

        nimiField.clear();
        lajiField.clear();
    }
}
// FILE_END
// FILE: Lemmikki.java
public class Lemmikki {
    StringProperty nimi = new SimpleStringProperty();
    StringProperty laji = new SimpleStringProperty();

    public StringProperty lajiProperty() { return laji; }

    public String getLaji() { return laji.get(); }

    public void setLaji(String laji) { this.laji.set(laji); }

    public StringProperty nimiProperty() { return nimi; }

    public String getNimi() { return nimi.get(); }

    public void setNimi(String nimi) { this.nimi.set(nimi); }

    @Override
    public String toString() { return getNimi() + " (" + getLaji() + ")"; }
}
// FILE_END
// FILE: main.fxml
<?xml version="1.0" encoding="UTF-8"?>

<?import javafx.geometry.Insets?>
<?import javafx.scene.control.Button?>
<?import javafx.scene.control.ListView?>
<?import javafx.scene.control.TextField?>
<?import javafx.scene.layout.VBox?>

<VBox alignment="CENTER" spacing="20.0" xmlns="http://javafx.com/javafx/25" xmlns:fx="http://javafx.com/fxml/1" fx:controller="fi.jyu.ohj2.esimerkki.muistikortti.MainController">
    <padding>
        <Insets bottom="20.0" left="20.0" right="20.0" top="20.0" />
    </padding>
   <children>
      <ListView fx:id="lemmikitList" prefHeight="200.0" prefWidth="200.0" />
      <TextField fx:id="nimiField" promptText="Nimi" />
      <TextField fx:id="lajiField" promptText="Laji" />
      <Button fx:id="lisaaButton" mnemonicParsing="false" text="Lisää" />
   </children>
</VBox>
// FILE_END
```

Sovelluksessa on lista, johon voi lisätä lemmikkejä, joita mallinnetaan `Lemmikki`-luokalla:

<img src="images/validation-1.png" width="300">

Nyt listaan voi lisätä lemmikkejä ilman nimeä tai lajia, mikä ei ole hyvä idea.
On syytä estää käyttäjää lisäämästä nimettömiä tai lajittomia lemmikkejä.

## Yksinkertainen validointi

Yksinkertaisin validointi voidaan tehdä tarkistamalla kohdealueen vaatimukset
ennen tietomallin kohteen luomista. Voisimme siis tarkistaa
`lisaaLemmikki()`-metodissa, onko nimi- ja laji-kentissä tekstiä:

```java,ignore
private void lisaaLemmikki() {
    
    // TODO: Suorita tässä kohdassa tarkistus, jonka perusteella 
    // lisätään lemmikki vain, jos tieto on oikein, ts. validia.

    Lemmikki lemmikki = new Lemmikki();
    lemmikki.setNimi(nimi);
    lemmikki.setLaji(laji);
    lemmikit.add(lemmikki);

    nimiField.clear();
    lajiField.clear();
}
```

## Validointimetodi

Validointi on usein helppo tehdä kontrollerissa erillisessä metodissa:

```java,ignore
/**
 * Tarkista, onko lemmikki-kenttien sisältö validi. 
 * Jos ei, korosta virheelliset kentät.
 * 
 * @return true, jos validointi onnistuu, muuten false
 */
private boolean validoiLemmikki() {
    // Tyhjennetään kenttien tyylit
    nimiField.setStyle("");
    lajiField.setStyle("");

    // Haetaan kenttien sisällöt
    String nimi = nimiField.getText();
    String laji = lajiField.getText();

    // Validointi: Nimi ei saa olla tyhjä
    if (nimi.isBlank()) {
        // Jos validointi epäonnistuu, korostetaan virheellinen kenttä
        nimiField.setStyle("-fx-border-color: red; -fx-background-color: #ffcccc;");
        return false;
    }

    // Validointi: Laji ei saa olla tyhjä
    if (laji.isBlank()) {
        lajiField.setStyle("-fx-border-color: red; -fx-background-color: #ffcccc;");
        return false;
    }

    // True = Validointi onnistuu
    return true;
}

private void lisaaLemmikki() {
    // Suorita ensin validointi ennen lisäämistä
    if (!validoiLemmikki()) {
        return;
    }

    Lemmikki lemmikki = new Lemmikki();
    lemmikki.setNimi(nimiField.getText());
    lemmikki.setLaji(lajiField.getText());
    lemmikit.add(lemmikki);

    nimiField.clear();
    lajiField.clear();
}
```

## Validoinnin siirto tietomalliin

Testaamisen ja vastuunjaon kannalta voi olla selkeämpää, että validointi on osa
tietomallia. Tällöin validointi voidaan toteuttaa esimerkiksi suoraan osana
tietomalliluokkaa. Tässä esimerkissä `tarkistaVirheet` on osa
`Lemmikki`-luokkaa. Toteutetaan samalla myös luetelmatyyppi `Tarkistusvirhe`,
joka kuvaa mahdollisia virhetilanteita.

```java,ignore
public enum Tarkistusvirhe  {
    NIMI_TYHJA, LAJI_TYHJA
}

public class Lemmikki {    
    // ...

    // Varsinainen tarkistinmetodi
    public Tarkistusvirhe tarkistaVirheet() {
        if (getNimi().isBlank()) {
            return Tarkistusvirhe.NIMI_TYHJA;
        }
        if (getLaji().isBlank()) {
            return Tarkistusvirhe.LAJI_TYHJA;
        }
        return null;
    }
}
```

Lemmikin lisääminen tapahtuu edelleen `lisaaLemmikki()`-metodissa, mutta nyt
tarkistetaan tietomallin kohteen validointi suoraan tietomalliluokasta:

```java,ignore
private void lisaaLemmikki() {
    nimiField.setStyle("");
    lajiField.setStyle("");

    // Luodaan tietomallin kohde ja asetetaan arvot
    Lemmikki lemmikki = new Lemmikki();
    lemmikki.setNimi(nimiField.getText());
    lemmikki.setLaji(lajiField.getText());

    // Tarkistetaan, onko tietomallin kohde kohdealueen kannalta oikeellinen
    Tarkistusvirhe virheTulos = lemmikki.tarkistaVirheet();
    // Jos virhe löytyy, näytetään käyttäjälle virheilmoitus virheen perusteella
    if (virheTulos != null) {
        if (virheTulos == Tarkistusvirhe.NIMI_TYHJA) {
            nimiField.setStyle("-fx-border-color: red; -fx-background-color: #ffcccc;");
        }
        if (virheTulos == Tarkistusvirhe.LAJI_TYHJA) {
            lajiField.setStyle("-fx-border-color: red; -fx-background-color: #ffcccc;");   
        }
        return;
    }

    // Lisätään lemmikki vain, jos lemmikki on kohdealueen kannalta oikeellinen
    lemmikit.add(lemmikki);

    nimiField.clear();
    lajiField.clear();
}
```

Null-tarkistusten sijaan on usein huomattavasti mielekkäämpää käyttää
Optional-tyyppiä, joka kuvaa paremmin tilannetta, jossa virhe voi joko olla
olemassa tai ei. 

```java,ignore
public Optional<Tarkistusvirhe> tarkistaVirheet() {
    if (getNimi().isBlank()) {
        return Optional.of(Tarkistusvirhe.NIMI_TYHJA);
    }
    if (getLaji().isBlank()) {
        return Optional.of(Tarkistusvirhe.LAJI_TYHJA);
    }
    return Optional.empty();
}
```

Siinä missä null on näkymätön sopimus ja vaatii erillisen dokumentoinnin (joka
käytännössä jää valitettavasti usein tekemättä), Optional-tyyppi kertoo
täsmälleen mistä on kysymys. Näin virheen tarkastaminen muuttuu siistimmäksi. 

```java,ignore
private void lisaaLemmikki() {
    // ...

    Optional<Tarkistusvirhe> virheTulos = lemmikki.tarkistaVirheet();
    // Jos virhe löytyy, näytetään käyttäjälle virheilmoitus virheen perusteella
    if (virheTulos.isPresent()) {
        Tarkistusvirhe virhe = virheTulos.get();
        if (virhe == Tarkistusvirhe.NIMI_TYHJA) {
            nimiField.setStyle("-fx-border-color: red; -fx-background-color: #ffcccc;");
        }
        if (virhe == Tarkistusvirhe.LAJI_TYHJA) {
            lajiField.setStyle("-fx-border-color: red; -fx-background-color: #ffcccc;");   
        }
        return;
    }

    // ...
}
```