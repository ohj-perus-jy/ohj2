# Näkymän vaihtaminen samassa ikkunassa

Näkymän vaihtaminen samassa ikkunassa on tärkeä osa monen JavaFX-sovelluksen
toimintaa. Tämä mahdollistaa käyttäjälle sujuvan kokemuksen, kun hän voi siirtyä
eri näkymien välillä ilman, että uusi ikkuna avautuu.

Alla yksinkertainen esimerkki, jossa on kaksi näkymää: `MainView` ja
`SecondaryView`. Painikkeella pääsee toiselle näkymälle, ja toisella
painikkeella takaisin.

Juju on tämä: Asetamme nykyisen Scene-olion juurisolmuksi uuden näkymän. Näin
ikkunan koko ja muut ominaisuudet säilyvät, mutta sisältö vaihtuu. 

```
// FILE: main.fxml
<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.Button?>
<?import javafx.scene.layout.VBox?>

<VBox xmlns:fx="http://javafx.com/fxml" fx:controller="fi.jyu.ohj2.esimerkit.MainController">
    <Button text="Toiseen näkymään" onAction="#siirryToiseenNakymaan"/>
</VBox>
// FILE_END
// FILE: secondary.fxml
<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.Button?>
<?import javafx.scene.layout.VBox?>
<VBox xmlns:fx="http://javafx.com/fxml" fx:controller="fi.jyu.ohj2.esimerkit.SecondaryController">
    <Button text="Takaisin päänäkymään" onAction="#siirryPaanakymaan"/>
</VBox>
// FILE_END
// FILE: MainController.java
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class MainController {

    @FXML
    private void siirryToiseenNakymaan(ActionEvent event) throws Exception {
        Parent secondaryView = FXMLLoader.load(getClass().getResource("secondary.fxml"));
        Scene currentScene = ((Node) event.getSource()).getScene();
        currentScene.setRoot(secondaryView);
    }
}
// FILE_END
// FILE: SecondaryController.java
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class SecondaryController {

    @FXML
    private void siirryPaanakymaan(ActionEvent event) throws Exception {
        Parent mainView = FXMLLoader.load(App.class.getResource("main.fxml"));
        Scene currentScene = ((Node) event.getSource()).getScene();
        currentScene.setRoot(mainView);
    }
}
// FILE_END
```

<br />

<img src="./images/nakymat.gif" alt="Näkymän vaihtaminen ikkunassa" width="300"/>

Jos näkymien välillä on tarvetta välittää tietoa, se voidaan toteuttaa näkymän
lataamisen yhteydessä seuraavasti. Tässä `MainController` lähettää viestin
`SecondaryController`-oliolle, joka tulostaa sen konsoliin
`initialize()`-metodissaan. Täysin vastaavasti voitaisiin välittää tieto myös
takaisin päin.

```java,ignore
// FILE: MainController.java
public class MainController  {
    @FXML
    private void siirryToiseenNakymaan(ActionEvent event) throws Exception {
        FXMLLoader loader = new FXMLLoader(App.class.getResource("secondary.fxml"));
        loader.setControllerFactory(_ -> new SecondaryController("Moikka"));
        Parent secondaryRoot = loader.load();
        Scene currentScene = ((Node) event.getSource()).getScene();
        currentScene.setRoot(secondaryRoot);
    }
}
// FILE_END
// FILE: SecondaryController.java
public class SecondaryController implements Initializable {

    String valitettyViesti;
    public SecondaryController(String viesti) {
        valitettyViesti = viesti;
    }

    @FXML
    private void siirryPaanakymaan(ActionEvent event) throws Exception {
        Parent mainView = FXMLLoader.load(App.class.getResource("main.fxml"));
        Scene currentScene = ((Node) event.getSource()).getScene();
        currentScene.setRoot(mainView);
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        IO.println("Päänäkymästä huudellaan: " + valitettyViesti);
    }
}
// FILE_END
```