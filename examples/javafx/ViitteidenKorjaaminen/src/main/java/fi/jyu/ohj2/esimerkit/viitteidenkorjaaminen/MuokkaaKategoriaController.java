package fi.jyu.ohj2.esimerkit.viitteidenkorjaaminen;

import java.net.URL;
import java.util.Optional;
import java.util.ResourceBundle;

import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;

public class MuokkaaKategoriaController implements Initializable {

    @FXML
    private TextField kategoriaNimiTextField;

    @FXML
    private Button tallennaButton;

    private Kategoria kategoria;

    private Optional<Kategoria> palautettavaKategoria = Optional.empty();

    public MuokkaaKategoriaController(Kategoria kategoria, ObservableList<Kategoria> kategoriat) {
        this.kategoria = kategoria;
    }
    
    @Override
    public void initialize(URL arg0, ResourceBundle arg1) {
        kategoriaNimiTextField.setText(kategoria.getNimi());
    }

    @FXML
    void kasitteleTallenna(ActionEvent event) {
        String uusiNimi = kategoriaNimiTextField.getText();
        if (uusiNimi != null && !uusiNimi.isBlank()) {
            kategoria.setNimi(uusiNimi);
            palautettavaKategoria = Optional.of(kategoria);
        }
        tallennaButton.getScene().getWindow().hide();
    }

    public Optional<Kategoria> getKategoria() {
        return palautettavaKategoria;
    }
}
