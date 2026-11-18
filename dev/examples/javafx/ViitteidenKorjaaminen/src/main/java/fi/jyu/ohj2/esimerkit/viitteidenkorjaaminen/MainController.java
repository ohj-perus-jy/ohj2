package fi.jyu.ohj2.esimerkit.viitteidenkorjaaminen;

import javafx.beans.Observable;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.ListCell;
import javafx.scene.control.ListView;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableRow;
import javafx.scene.control.TableView;
import javafx.scene.control.TextInputDialog;
import javafx.scene.paint.Color;
import javafx.scene.text.Text;
import javafx.stage.Modality;
import javafx.stage.Stage;
import tools.jackson.core.JacksonException;
import tools.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.net.URL;
import java.nio.file.Path;
import java.util.Optional;
import java.util.ResourceBundle;

public class MainController implements Initializable {

    private static final Kategoria TYHJA_KATEGORIA = new Kategoria("");

    private final ObservableList<Kategoria> kategoriat = FXCollections.observableArrayList(k -> new Observable[] {
            k.nimiProperty()
    });

    private final ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList();

    private Optional<Tehtava> valittuTehtava;
    private Optional<Kategoria> valittuKategoria;

    @FXML
    private ListView<Kategoria> kategoriatListView;

    @FXML
    private TableView<Tehtava> tehtavatTableView;

    @FXML
    private Button muokkaaKategoriaButton;

    @FXML
    private Button muokkaaTehtavaButton;

    @FXML
    private Button lisaaKategoriaButton;

    @FXML
    private Button poistaKategoriaButton;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        Path tehtavatPolku = Path.of("tehtavat.json");
        Path kategoriatPolku = Path.of("kategoriat.json");

        ObjectMapper mapper = new ObjectMapper();
        try {
            Kategoria[] k = mapper.readValue(kategoriatPolku.toFile(), Kategoria[].class);
            Tehtava[] t = mapper.readValue(tehtavatPolku.toFile(), Tehtava[].class);

            kategoriat.setAll(k);
            for (Tehtava tehtava : t) {
                Kategoria jsonistaLuettuKategoria = tehtava.getKategoria();
                tehtava.setKategoria(asetaKategoriaViite(jsonistaLuettuKategoria.getNimi()));
            }
            tehtavat.setAll(t);

        } catch (JacksonException e) {
            e.printStackTrace();
        }

        TableColumn<Tehtava, String> otsikkoColumn = new TableColumn<>("Otsikko");
        otsikkoColumn.setCellValueFactory(cellData -> cellData.getValue().otsikkoProperty());
        TableColumn<Tehtava, String> kategoriaColumn = new TableColumn<>("Kategoria");
        // flatMap seuraa dynaamista ketjua
        // Tehtava.kategoriaProperty() -> Kategoria.nimiProperty().
        // Jos tehtävän kategoria vaihtuu, sidonta siirtyy automaattisesti seuraamaan
        // uuden kategorian nimiPropertya. Jos taas saman kategorian nimi muuttuu,
        // taulukon solu päivittyy myös silloin. null-kategoria tuottaa null-arvon
        // ilman poikkeusta.
        kategoriaColumn.setCellValueFactory(
                 cellData -> cellData.getValue().kategoriaProperty().flatMap(kategoria -> kategoria.nimiProperty()));
        // kategoriaColumn.setCellValueFactory(cellData -> cellData.getValue().kategoriaProperty().asString());

        tehtavatTableView.getColumns().addAll(otsikkoColumn, kategoriaColumn);
        tehtavatTableView.getSelectionModel().selectedItemProperty().addListener((obs, vanha, uusi) -> {
            valittuTehtava = Optional.ofNullable(uusi);
        });
        tehtavatTableView.setItems(tehtavat);
        
        kategoriatListView.getSelectionModel().selectedItemProperty().addListener((obs, vanha, uusi) -> {
            valittuKategoria = Optional.ofNullable(uusi);
        });
        kategoriatListView.setItems(kategoriat);
        
        // UX-hifistelyä: 
        poistaValintaTyhjanRivinKlikkauksessa(tehtavatTableView);
        poistaValintaTyhjanRivinKlikkauksessa(kategoriatListView);
        muokkaaKategoriaButton.setDisable(true);
        muokkaaTehtavaButton.setDisable(true);
        poistaKategoriaButton.setDisable(true);
    }

    private void poistaValintaTyhjanRivinKlikkauksessa(ListView<Kategoria> listView) {
        listView.setCellFactory(_ -> {
            ListCell<Kategoria> cell = new ListCell<>() {
                @Override
                protected void updateItem(Kategoria item, boolean empty) {
                    super.updateItem(item, empty);
                    if (empty || item == null) {
                        setText(null);
                        setGraphic(null);
                        setStyle("");
                    } else {
                        setText(item.getNimi());
                        setGraphic(null);
                        setStyle("");
                    }
                }
            };
            cell.setOnMouseClicked(event -> {
                if (!cell.isEmpty()) {
                    valittuKategoria = Optional.of(cell.getItem());
                    muokkaaKategoriaButton.setDisable(false);
                    poistaKategoriaButton.setDisable(false);
                } else {
                    valittuKategoria = Optional.empty();
                    muokkaaKategoriaButton.setDisable(true);
                    poistaKategoriaButton.setDisable(true);
                    kategoriatListView.getSelectionModel().clearSelection();
                }
            });
            return cell;
        });
    }

    private void poistaValintaTyhjanRivinKlikkauksessa(TableView<Tehtava> tableView) {
        tableView.setRowFactory(tv -> {
            TableRow<Tehtava> row = new TableRow<>();
            row.setOnMouseClicked(event -> {
                if (!row.isEmpty()) {
                    valittuTehtava = Optional.of(row.getItem());
                    muokkaaTehtavaButton.setDisable(false);
                } else {
                    valittuTehtava = Optional.empty();
                    muokkaaTehtavaButton.setDisable(true);
                    tehtavatTableView.getSelectionModel().clearSelection();
                }
            });
            return row;
        });
    }

    @FXML
    void kasittelePoistaKategoria() {        
        if (valittuKategoria.isEmpty()) {
            return;
        }

        kategoriat.remove(valittuKategoria.get());

        for (Tehtava tehtava : tehtavat) {
            if (tehtava.getKategoria() == valittuKategoria.get()) {
                tehtava.setKategoria(TYHJA_KATEGORIA);
            }
        }
    }

    @FXML
    void kasitteleLisaaKategoria(ActionEvent event) {
        TextInputDialog dialog = new TextInputDialog();
        dialog.setTitle("Uusi kategoria");
        dialog.setHeaderText("Luo uusi kategoria");
        dialog.setContentText("Anna kategorian nimi:");

        // Jos tätä _ei_ tehdä, dialog sulkeutuu ennen kuin ehtii näyttää
        // virheilmoituksen
        Button okButton = (Button) dialog.getDialogPane().lookupButton(ButtonType.OK);
        okButton.addEventFilter(ActionEvent.ACTION, e -> {
            String nimi = dialog.getEditor().getText();
            if (nimi.isBlank()) {
                // Näytä tekstikentässä vihje, että nimi ei saa olla tyhjä
                dialog.getEditor().setText("");
                dialog.getEditor().setPromptText("Nimi ei saa olla tyhjä");
                e.consume(); // Estä dialogin sulkeutuminen
            } else if (kategoriat.stream().anyMatch(k -> k.getNimi().equals(nimi))) {
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setTitle("Virhe");
                alert.setHeaderText("Kategoria nimeltä '" + nimi + "' on jo olemassa");
                alert.showAndWait();
                e.consume(); // Estä dialogin sulkeutuminen
            }
        });

        // Tässä kohden tarvitsee enää käsitellä vain onnistuneet tapaukset,
        // koska epäonnistuneet on estetty tapahtumasta
        Optional<String> result = dialog.showAndWait();
        result.ifPresent(nimi -> {
            Kategoria uusiKategoria = new Kategoria(nimi);
            kategoriat.add(uusiKategoria);
        });
    }

    @FXML
    void kasitteleMuokkaaKategoria(ActionEvent event) {
        try {
            FXMLLoader loader = new FXMLLoader(App.class.getResource("muokkaaKategoria.fxml"));
            loader.setControllerFactory(_ -> new MuokkaaKategoriaController(valittuKategoria.get(), kategoriat));

            Parent root = loader.load();
            Stage muokkaaKategoriaDialogi = new Stage();
            muokkaaKategoriaDialogi.setScene(new Scene(root));
            muokkaaKategoriaDialogi.setTitle("Muokkaa kategoriaa");
            muokkaaKategoriaDialogi.initModality(Modality.APPLICATION_MODAL);
            muokkaaKategoriaDialogi.showAndWait();
            MuokkaaKategoriaController controller = loader.getController();
            if (controller.getKategoria().isPresent()) {
                Kategoria muokattuKategoria = controller.getKategoria().get();
                valittuKategoria.get().setNimi(muokattuKategoria.getNimi());
            }

        } catch (IOException ioe) {
            IO.println("Kategorian muokkaaminen epäonnistui: " + ioe.getMessage());
        }
    }

    @FXML
    void kasitteleMuokkaaTehtava(ActionEvent event) {
        try {
            FXMLLoader loader = new FXMLLoader(App.class.getResource("muokkaaTehtava.fxml"));
            loader.setControllerFactory(_ -> new MuokkaaTehtavaController(valittuTehtava.get(), kategoriat));

            Parent root = loader.load();
            Stage muokkaaTehtavaDialogi = new Stage();
            muokkaaTehtavaDialogi.setScene(new Scene(root));
            muokkaaTehtavaDialogi.setTitle("Muokkaa tehtävää");
            muokkaaTehtavaDialogi.initModality(Modality.APPLICATION_MODAL);
            muokkaaTehtavaDialogi.showAndWait();

            MuokkaaTehtavaController controller = loader.getController();
            if (controller.getTehtava().isPresent()) {
                valittuTehtava.get().setOtsikko(controller.getTehtava().get().getOtsikko());
                valittuTehtava.get().setKategoria(controller.getTehtava().get().getKategoria());
            }

        } catch (IOException ioe) {
            IO.println("Tehtävän muokkaaminen epäonnistui: " + ioe.getMessage());
        }
    }

    /**
     * Hakee ja palauttaa kategoriat-listalta Kategoria-olion, jolla on sama
     * nimi kuin JSONista luetulla Kategoria-oliolla, ja palauttaa sen. Jos
     * kategoriat-listalla ei ole Kategoria-oliota, jolla on sama nimi, tai jos
     * se on merkitty poistetuksi, palautetaan TYHJA_KATEGORIA.
     * 
     * @param nimi JSONista luetun Kategoria-olion nimi
     * @return kategoriat-listalta löytyvät Kategoria-olio. Jos ei löydy, tai se
     *         on merkitty poistetuksi, palautetaan TYHJA_KATEGORIA.
     */
    private Kategoria asetaKategoriaViite(String nimi) {

        for (Kategoria ehdokas : kategoriat) {
            if (ehdokas.getNimi().equals(nimi)) {
                return ehdokas;
            }
        }
        return TYHJA_KATEGORIA;
        /*
         * return kategoriat.stream()
         * .filter(ehdokas -> ehdokas.getNimi().equals(kategoria.getNimi()))
         * .findFirst()
         * .filter(ehdokas -> !ehdokas.isPoistettu())
         * .orElse(TYHJA_KATEGORIA);
         */
    }
}
