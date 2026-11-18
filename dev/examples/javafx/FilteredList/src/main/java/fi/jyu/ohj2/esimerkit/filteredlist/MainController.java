package fi.jyu.ohj2.esimerkit.filteredlist;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.CheckBox;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import tools.jackson.databind.ObjectMapper;

import java.net.URL;
import java.nio.file.Path;
import java.util.ResourceBundle;

public class MainController implements Initializable {

    ObservableList<Kategoria> kategoriat = FXCollections.observableArrayList();
    ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList();
    FilteredList<Tehtava> suodatetutTehtavat;

    @FXML
    private CheckBox checkBox;

    @FXML
    private ComboBox<Kategoria> comboBox;

    @FXML
    private TableView<Tehtava> tableView;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        Path tehtavatPolku = Path.of("tehtavat.json");
        Path kategoriatPolku = Path.of("kategoriat.json");

        ObjectMapper mapper = new ObjectMapper();
        try {
            Kategoria[] k = mapper.readValue(kategoriatPolku.toFile(), Kategoria[].class);
            Tehtava[] t = mapper.readValue(tehtavatPolku.toFile(), Tehtava[].class);

            this.kategoriat.setAll(k);
            this.tehtavat.setAll(t);

        } catch (Exception e) {
            e.printStackTrace();
        }

        comboBox.setItems(kategoriat);

        suodatetutTehtavat = new FilteredList<>(tehtavat, t -> true);

        // kategoriaComboBox.getSelectionModel().selectedItemProperty().addListener((obs,
        // vanha, uusi) -> {
        comboBox.setOnAction(e -> {
            paivitaSuodatus();
        });

        // Tällä varmistetaan, että suodatus on pois päältä, kun checkbox ei ole valittuna        
        comboBox.disableProperty().bind(checkBox.selectedProperty().not());
        
        TableColumn<Tehtava, String> otsikkoColumn = new TableColumn<>("Otsikko");
        otsikkoColumn.setCellValueFactory(cellData -> cellData.getValue().otsikkoProperty());
        TableColumn<Tehtava, String> kategoriaColumn = new TableColumn<>("Kategoria");
        kategoriaColumn.setCellValueFactory(cellData -> cellData.getValue().kategoriaProperty().asString());
        tableView.getColumns().addAll(otsikkoColumn, kategoriaColumn);

        tableView.setItems(suodatetutTehtavat);
    }

    @FXML
    private void paivitaSuodatus() {
        Kategoria valittuKategoria = comboBox.getSelectionModel().getSelectedItem();
        if (checkBox.isSelected() && valittuKategoria != null) {
            suodatetutTehtavat.setPredicate(t -> t.getKategoria().getNimi().equals(valittuKategoria.getNimi()));
        } else {
            suodatetutTehtavat.setPredicate(t -> true); // Näytä kaikki
        }
    }
}
