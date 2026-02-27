# MVC-arkkitehtuuri

Nyt kun meillä on luotuna `Tehtava`-malli propertyineen ja pystymme näyttämään
listan tehtäviä `TableView`-komponentissa, on aika pohtia koko sovelluksen
rakennetta.

Tällä hetkellä kaikki sovelluksen ohjauslogiikka, data ja tiedostokäsittely ovat
kietoutuneet `MainController`-luokkaan. Tämä tekee kontrollerista nopeasti liian
raskaan ylläpitää ja vaikean testata. Ratkaisu tähän on **MVC-arkkitehtuuri**
(Model-View-Controller).

Tässä luvussa jaamme sovelluksemme vastuualueisiin: käyttöliittymä, data ja
ohjauslogiikka erotetaan toisistaan. Erityisesti siirrämme datan hallinnan ja
tallennuksen kontrollerista omaan malliluokkaansa.

## Kerrosten vastuut

MVC-mallissa sovellus jaetaan kolmeen osaan:

### `View` (Näkymä)

- **Vastuu:** Miltä sovellus näyttää.
- **Toteutus:** FXML-tiedostot kuvaavat käyttöliittymän rakenteen (`TableView`,
  painikkeet, kentät).
- **Rajoitukset:** Ei sisällä lainkaan sovelluslogiikkaa (ei esim. tiedä miten
  tehtävät tallennetaan kovalevylle).

### `Model` (Malli)

- **Vastuu:** Mitä dataa sovelluksessa on ja miten sitä käsitellään
  (liiketoimintalogiikka).
- **Toteutus:** Olemme jo tehneet `Tehtava`-luokan mallintamaan yksittäistä
  tehtävää. Nyt luomme `Tehtavakokoelma`-luokan, joka pitää sisällään koko
  sovelluksen tilan (tehtävälistan) ja tarjoaa metodit tehtävien lisäämiseen,
  poistamiseen ja tallentamiseen.
- **Rajoitukset:** Ei tiedä mitään JavaFX-näkymästä (`TableView`, `TextField`),
  vaan luottaa _observable_-rakenteisiin kertoakseen muutoksista kiinnostuneille
  osapuolille.

### `Controller` (Ohjain)

- **Vastuu:** Toimia tulkkina näkymän ja mallin välillä.
- **Toteutus:** `MainController` reagoi käyttäjän tekemiin toimintoihin (esim.
  napin painallus), kutsuu mallin (`Tehtavakokoelma`) metodeja, ja sitoo näkymän
  (`TableView`) kiinni mallin tarjoamaan observable-dataan.

## Esimerkkirakenne

Arkkitehtuuria selkeyttää kooditiedostojen jakaminen paketteihin vastuun mukaan:

```text
fi.jyu.ohj2.nimi.todo
├── model
│   ├── Prioriteetti.java
│   ├── Tehtava.java
│   └── Tehtavakokoelma.java
├── persistence
│   ├── JsonTehtavaRepository.java
│   └── TehtavaRepository.java
└── ui
    ├── Main.java
    └── MainController.java
```

## Datatallennuksen eriyttäminen (Repository)

Ennen kuin siirrämme listan kontrollerista malliluokkaan, mietitään miten tiedon
lataus ja tallennus kannattaa hoitaa.

Vaikka voisimme kirjoittaa JSON-tallennuskoodin suoraan malliluokkaan
(`Tehtavakokoelma`), hyvä suunnitteluperiaate ohjaa erottamaan tallennuksen
omaksi kokonaisuudekseen. Yksi hyvin yleinen tapa tässä on käyttää
_Repository_-rajapintaa (säilö).

Rajapinnan tehokkuus piilee siinä, että `Tehtavakokoelma`-luokan ei tarvitse
tietää, _miten_ tai _minne_ data tallennetaan (onko se JSON-tiedosto, tietokanta
vai vain muisti). Se käyttää ainoastaan tallennus- ja latausmetodeja. Tämä on
elintärkeää erityisesti sovelluksen testaamisessa myöhemmin!

Luodaan pakettiin `persistence` rajapinta:

```java
package fi.jyu.ohj2.nimi.todo.persistence;

import java.io.IOException;
import java.util.List;

public interface TehtavaRepository {
    List<TehtavaDto> lataa() throws IOException;
    void tallenna(List<TehtavaDto> tehtavat) throws IOException;
}
```

(Huomaa: käytämme tässä Dto-luokkaa [Data Transfer Object], joka on
yksinkertainen record/luokka pelkkää tiedostosiirtoa varten ilman
JavaFX-property -kääreitä.)

Toteutamme tämän rajapinnan jo tutulla Jacksonilla
`JsonTehtavaRepository`-luokassa:

```java
package fi.jyu.ohj2.nimi.todo.persistence;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class JsonTehtavaRepository implements TehtavaRepository {
    private final Path tallennustiedosto;
    private final ObjectMapper mapper = new ObjectMapper();

    public JsonTehtavaRepository(Path tallennustiedosto) {
        this.tallennustiedosto = tallennustiedosto;
    }

    @Override
    public List<TehtavaDto> lataa() throws IOException {
        if (Files.notExists(tallennustiedosto)) {
            return List.of();
        }
        return mapper.readValue(tallennustiedosto.toFile(), new TypeReference<>() {});
    }

    @Override
    public void tallenna(List<TehtavaDto> tehtavat) throws IOException {
        mapper.writeValue(tallennustiedosto.toFile(), tehtavat);
    }
}
```

## Keskeinen tietomalli: Tehtavakokoelma

Nyt siirrämme sovelluksen sydämen, eli tehtävälistan hallinnan, pois
kontrollerista omaan logiikkaluokkaansa. Luodaan pakettiin `model` luokka
`Tehtavakokoelma`:

```java
package fi.jyu.ohj2.nimi.todo.model;

import fi.jyu.ohj2.nimi.todo.persistence.TehtavaDto;
import fi.jyu.ohj2.nimi.todo.persistence.TehtavaRepository;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;

import java.io.IOException;
import java.util.List;

public class Tehtavakokoelma {
    // 1. Ekstraktori takaa, että jos tehtävän 'tehtyProperty' muuttuu, lista huomaa sen
    private final ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList(
            t -> new javafx.beans.Observable[]{t.tehtyProperty()}
    );
    
    // 2. Riippuvuus tallennusmekanismista rajapinnan kautta
    private final TehtavaRepository repository;

    public Tehtavakokoelma(TehtavaRepository repository) {
        this.repository = repository;
        
        // Asetetaan tallennuskuuntelija listalle mallin sisällä
        this.tehtavat.addListener((javafx.collections.ListChangeListener<Tehtava>) change -> {
            tallenna();
        });
    }

    // --- Ohjelman logiikkametodit ---

    public void lataa() throws IOException {
        List<TehtavaDto> dtot = repository.lataa();
        List<Tehtava> muunnetut = dtot.stream()
                .map(d -> {
                    Tehtava t = new Tehtava(d.otsikko(), d.tehty());
                    t.setKuvaus(d.kuvaus());
                    t.setPrioriteetti(Prioriteetti.valueOf(d.prioriteetti()));
                    return t;
                })
                .toList();
        tehtavat.setAll(muunnetut);
    }

    private void tallenna() {
        try {
            List<TehtavaDto> dtot = tehtavat.stream()
                    .map(t -> new TehtavaDto(
                            t.getOtsikko(), 
                            t.getKuvaus(), 
                            t.isTehty(), 
                            t.getPrioriteetti().name()))
                    .toList();
            repository.tallenna(dtot);
        } catch (IOException e) {
            // Reaalimaailmassa heitettäisiin poikkeus eteenpäin tai kirjattaisiin lokiin
            System.err.println("Tallennus epäonnistui: " + e.getMessage());
        }
    }

    // --- Julkiset metodit kontrollerin käyttöön ---

    public ObservableList<Tehtava> getTehtavat() {
        return tehtavat;
    }

    public void lisaaTehtava(String otsikko) {
        if (otsikko == null || otsikko.isBlank()) return;
        tehtavat.add(new Tehtava(otsikko.trim(), false));
    }

    public void poistaTehtava(Tehtava tehtava) {
        if (tehtava != null) {
            tehtavat.remove(tehtava);
        }
    }
}
```

Huomaa, miten kaikki säännöt ("otsikko ei saa olla tyhjä", "päivitä tiedosto kun
lisätään tai ominaisuus muuttuu") asuvat nyt täällä malliluokassa! Täällä ei ole
tippaakaan koodia, joka tietäisi Tekstikentistä, ja `tallenna()`-logiikka ei
välitä puhuuko se tiedostolle vai tietokannalle. Se puhuu
`repository`-rajapinnalle.

## Kontrollerin uusi rooli

Päivitetään lopuksi `MainController`. Kontrollerin rooli on nyt hyvin selkeä
"virkailija" mallin ja näkymän välissä. Se ottaa `Tehtavakokoelma` -mallin
käyttöönsä ja delegoi itse tekemisen eteenpäin:

```java
package fi.jyu.ohj2.nimi.todo.ui;

import fi.jyu.ohj2.nimi.todo.model.Prioriteetti;
import fi.jyu.ohj2.nimi.todo.model.Tehtava;
import fi.jyu.ohj2.nimi.todo.model.Tehtavakokoelma;
import fi.jyu.ohj2.nimi.todo.persistence.JsonTehtavaRepository;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.CheckBoxTableCell;

import java.io.IOException;
import java.nio.file.Path;

public class MainController {
    @FXML private TextField uusiTehtavaNimi;
    @FXML private TableView<Tehtava> tehtavaTaulu;
    @FXML private TableColumn<Tehtava, String> otsikkoCol;
    @FXML private TableColumn<Tehtava, Prioriteetti> prioriteettiCol;
    @FXML private TableColumn<Tehtava, Boolean> tehtyCol;

    // 1. Luodaan uusi ylätason malli ja sille säilö
    private final Tehtavakokoelma malli = new Tehtavakokoelma(
            new JsonTehtavaRepository(Path.of("tehtavat.json"))
    );

    @FXML
    public void initialize() {
        // Alustetaan taulukon databinding propertyihin
        otsikkoCol.setCellValueFactory(cd -> cd.getValue().otsikkoProperty());
        prioriteettiCol.setCellValueFactory(cd -> cd.getValue().prioriteettiProperty());
        tehtyCol.setCellValueFactory(cd -> cd.getValue().tehtyProperty());
        
        tehtyCol.setCellFactory(CheckBoxTableCell.forTableColumn(tehtyCol));
        tehtyCol.setEditable(true);
        tehtavaTaulu.setEditable(true);

        try {
            malli.lataa();
        } catch (IOException e) {
            System.err.println("Lataus epäonnistui: " + e.getMessage());
        }

        // 2. Kytketään mallin tarjoama obserable lista kiinni taulukkoon
        tehtavaTaulu.setItems(malli.getTehtavat());
    }

    @FXML
    private void lisaaTehtava() {
        // Annetaan työn tekeminen mallin vastuulle
        malli.lisaaTehtava(uusiTehtavaNimi.getText());
        uusiTehtavaNimi.clear();
        uusiTehtavaNimi.requestFocus();
    }

    @FXML
    private void poistaValittu() {
        Tehtava valittu = tehtavaTaulu.getSelectionModel().getSelectedItem();
        // Delegoituminen mallille
        malli.poistaTehtava(valittu);
    }
}
```

Käyttöliittymäkontrollerin rivimäärä on pienentynyt huomattavasti ja logiikka on
helppolukuista!

## Miksi MVC auttaa tässä projektissa?

- Jokaisella osalla on selkeä vastuu (Yhtenäisyys- eli Single Responsibility
  -periaate).
- Logiikka (listan hallinta, syötteen kelpoisuuden tarkistus, tallennus) voidaan
  testata Java-ohjelmana `Tehtavakokoelma`-luokan avulla täysin ilman
  käyttöliittymän pyörittämistä tai klikkailua.
- Saman mallin (`Tehtavakokoelma` tilaoineen) voi tarvittaessa luovuttaa useiden
  eri näkymien (esim. useat tiettyjen prioriteettien taulukot) käyttöön
  vaivattomasti.

## Tehtävät

<task>
  <task-title>Tehtävä 8.2: TODO-ohjelma, vaihe 8. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-2-todo-8/handout.md}}

</handout>
</task>
