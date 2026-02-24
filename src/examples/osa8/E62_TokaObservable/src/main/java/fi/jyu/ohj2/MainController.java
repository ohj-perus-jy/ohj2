package fi.jyu.ohj2;

import javafx.collections.FXCollections;
import javafx.collections.ListChangeListener;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;

import java.net.URL;
import java.util.ResourceBundle;

public class MainController implements Initializable {

    ObservableList<String> nimet = FXCollections.observableArrayList();

    @FXML
    private ListView<String> nimitulosteet;

    @FXML
    private TextField nimikentta;

    @FXML
    private void lisaaNimi() {
        String uusiNimi = nimikentta.getText();
        nimet.add(uusiNimi);
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        nimitulosteet.setItems(nimet);

        nimet.addListener((ListChangeListener.Change<? extends String> change) -> {
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
