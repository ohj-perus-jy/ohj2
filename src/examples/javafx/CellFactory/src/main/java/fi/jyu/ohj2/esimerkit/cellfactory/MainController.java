package fi.jyu.ohj2.esimerkit.cellfactory;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.CheckBox;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TableCell;
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
    private CheckBox suodataCheckBox;

    @FXML
    private ComboBox<Kategoria> valitseKategoriaComboBox;

    @FXML
    private TableView<Tehtava> tehtavatTableView;

    @FXML
    private CheckBox naytaMyosPoistetutCheckBox;

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
            // Asetetaan vielä tehtävien kategoria-viitteet oikeiksi kategoriat-olioiksi,
            // jotta suodatus ja muotoilu toimii
            for (Tehtava tehtava : this.tehtavat) {
                Kategoria oikeaKategoria = this.kategoriat.stream()
                        .filter(kategoria -> kategoria.getNimi().equals(tehtava.getKategoria().getNimi()))
                        .findFirst()
                        .orElse(tehtava.getKategoria());
                tehtava.setKategoria(oikeaKategoria);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        valitseKategoriaComboBox.setItems(kategoriat.filtered(k -> !k.isPoistettu()));
        suodatetutTehtavat = new FilteredList<>(tehtavat, t -> !t.getKategoria().isPoistettu());
        valitseKategoriaComboBox.getSelectionModel().selectedItemProperty().addListener((obs, vanha, uusi) -> {
            paivitaSuodatus();
        });

        // Tällä varmistetaan, että suodatus on pois päältä, kun checkbox ei ole
        // valittuna
        valitseKategoriaComboBox.disableProperty().bind(suodataCheckBox.selectedProperty().not());
        suodataCheckBox.selectedProperty()
                .addListener((obs, vanha, uusi) -> naytaMyosPoistetutCheckBox.setSelected(false));

        naytaMyosPoistetutCheckBox.selectedProperty().addListener((obs, vanha, uusi) -> {
            if (uusi) {
                suodatetutTehtavat.setPredicate(t -> true);
            } else {
                paivitaSuodatus();
            }
        });

        naytaMyosPoistetutCheckBox.disableProperty().bind(suodataCheckBox.selectedProperty());

        TableColumn<Tehtava, String> otsikkoColumn = new TableColumn<>("Otsikko");
        otsikkoColumn.setCellValueFactory(cellData -> cellData.getValue().otsikkoProperty());
        TableColumn<Tehtava, String> kategoriaColumn = new TableColumn<>("Kategoria");
        kategoriaColumn.setCellValueFactory(cellData -> cellData.getValue().kategoriaProperty().asString());
        kategoriaColumn.setCellFactory(cell -> new TableCell<Tehtava, String>() {
            @Override
            protected void updateItem(String item, boolean empty) {
                super.updateItem(item, empty);
                if (empty || item == null) {
                    setText(null);
                    setStyle("");
                } else {
                    setText(item);
                    Tehtava tehtava = getTableRow().getItem();
                    if (tehtava != null && tehtava.getKategoria().isPoistettu()) {
                        setStyle("-fx-text-fill: red;");
                    } else {
                        setStyle("");
                    }
                }
            }
        });
        tehtavatTableView.getColumns().addAll(otsikkoColumn, kategoriaColumn);
        tehtavatTableView.setItems(suodatetutTehtavat);
    }

    @FXML
    private void paivitaSuodatus() {
        Kategoria valittuKategoria = valitseKategoriaComboBox.getSelectionModel().getSelectedItem();
        if (suodataCheckBox.isSelected() && valittuKategoria != null) {
            suodatetutTehtavat.setPredicate(t -> t.getKategoria().getNimi().equals(valittuKategoria.getNimi()));
        } else {
            // Näytä kaikki tehtävät, jotka eivät kuulu poistettuihin kategorioihin
            suodatetutTehtavat.setPredicate(t -> !t.getKategoria().isPoistettu());
        }
    }
}
