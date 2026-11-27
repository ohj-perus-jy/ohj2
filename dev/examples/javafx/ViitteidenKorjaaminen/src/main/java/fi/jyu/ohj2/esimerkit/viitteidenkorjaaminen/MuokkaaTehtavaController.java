package fi.jyu.ohj2.esimerkit.viitteidenkorjaaminen;

import java.net.URL;
import java.util.List;
import java.util.Optional;
import java.util.ResourceBundle;

import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;

public class MuokkaaTehtavaController implements Initializable {

    @FXML
    private ComboBox<Kategoria> kategoriaComboBox;

    @FXML
    private Button tallennaButton;

    @FXML
    private Label tehtavaLabel;

    private List<Kategoria> kategoriat;
    private Tehtava tehtava;
    private Optional<Tehtava> palautettavaTehtava = Optional.empty();

    public MuokkaaTehtavaController(Tehtava tehtava, ObservableList<Kategoria> kategoriat) {
        this.tehtava = tehtava;
        this.kategoriat = kategoriat;
    }

    public Optional<Tehtava> getTehtava() {
        return palautettavaTehtava;
    }

    public void setKategoriat(List<Kategoria> kategoriat) {
        this.kategoriat = kategoriat;
    }
    
    @Override
    public void initialize(URL arg0, ResourceBundle rb) {        
        kategoriaComboBox.getItems().addAll(kategoriat);
        tehtavaLabel.setText(tehtava.getOtsikko());
        kategoriaComboBox.getSelectionModel().select(tehtava.getKategoria());
    }
    
    @FXML
    void kasitteleTallenna(ActionEvent event) {
        Kategoria valittuKategoria = kategoriaComboBox.getSelectionModel().getSelectedItem();
        if (valittuKategoria != null) {
            tehtava.setKategoria(valittuKategoria);
            palautettavaTehtava = Optional.of(tehtava);
        }
        tallennaButton.getScene().getWindow().hide();
    }
}
