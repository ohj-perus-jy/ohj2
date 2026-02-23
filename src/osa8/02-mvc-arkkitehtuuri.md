# MVC-arkkitehtuuri

Nyt kun tehtävädata on eriytetty malliksi, seuraava askel on selkeä rakenne
koko sovellukselle.

Tässä luvussa käytämme MVC-ajattelua, joka sopii tähän TODO-projektiin hyvin:
käyttöliittymä, data ja ohjauslogiikka erotetaan toisistaan.

## Kerrosten vastuut

`Model`

- Kuvaa sovelluksen datan (`Tehtava`, `Prioriteetti`).
- Sisältää datan käsittelyyn liittyvää logiikkaa.
- Ei tunne JavaFX-näkymää.

`View`

- FXML kuvaa näkymän rakenteen (`TableView`, painikkeet, kentät).
- Ei sisällä sovelluslogiikkaa.

`Controller`

- Reagoi käyttäjän toimintoihin (napit, tuplaklikkaus, valinnat).
- Päivittää mallia ja näkymää.
- Kutsuu tallennusta/latausta oikeissa kohdissa.

`Repository` (mallikerroksen apuluokka)

- Vastaa tiedoston luku- ja kirjoituslogiikasta (`JSON`).
- Ei tunne käyttöliittymäkomponentteja.

## Esimerkkirakenne

Yksi selkeä pakettijako:

```text
fi/jyu/ohj2/nimi/todo/
  model/
    Tehtava.java
    Prioriteetti.java
  persistence/
    TehtavaRepository.java
    JsonTehtavaRepository.java
  ui/
    MainController.java
```

## Repository-rajapinta

```java
public interface TehtavaRepository {
    List<TehtavaDto> lataa() throws IOException;
    void tallenna(List<TehtavaDto> tehtavat) throws IOException;
}
```

`JsonTehtavaRepository` toteuttaa tämän rajapinnan Jacksonilla.

## Controller pitää yhteyden malliin

Controllerissa pidetään sovelluksen tehtävät yhdessä `ObservableList`issä:

```java
public class MainController {
    private final ObservableList<Tehtava> tehtavat =
            FXCollections.observableArrayList();
    private final TehtavaRepository repository =
            new JsonTehtavaRepository(Path.of("tehtavat.json"));

    @FXML private TextField uusiTehtavaNimi;
    @FXML private TableView<Tehtava> tehtavaTaulu;

    public void initialize() {
        lataa();
        tehtavaTaulu.setItems(tehtavat);
    }
}
```

## Esimerkki: tehtävän lisäys MVC-tyylillä

```java
@FXML
private void lisaaTehtava() {
    String otsikko = uusiTehtavaNimi.getText();
    if (otsikko == null || otsikko.isBlank()) {
        uusiTehtavaNimi.requestFocus();
        return;
    }

    tehtavat.add(new Tehtava(otsikko.trim(), false));
    uusiTehtavaNimi.clear();
    uusiTehtavaNimi.requestFocus();
    tallenna();
}
```

Tässä:

- näkymä antaa syötteen (`TextField`)
- kontrolleri validoi
- malli päivittyy (`Tehtava` lisätään listaan)
- data tallennetaan repositoryn kautta

## Lataus ja tallennus

```java
private void tallenna() {
    try {
        List<TehtavaDto> dto = tehtavat.stream()
                .map(t -> new TehtavaDto(
                        t.getOtsikko(),
                        t.getKuvaus(),
                        t.isTehty(),
                        t.getPrioriteetti().name()))
                .toList();
        repository.tallenna(dto);
    } catch (IOException e) {
        naytaVirhe("Tallennus epäonnistui: " + e.getMessage());
    }
}

private void lataa() {
    try {
        List<TehtavaDto> dto = repository.lataa();
        tehtavat.setAll(dto.stream()
                .map(d -> {
                    Tehtava t = new Tehtava(d.otsikko(), d.tehty());
                    t.setKuvaus(d.kuvaus());
                    t.setPrioriteetti(Prioriteetti.valueOf(d.prioriteetti()));
                    return t;
                })
                .toList());
    } catch (IOException e) {
        naytaVirhe("Lataus epäonnistui: " + e.getMessage());
    }
}
```

## Miksi MVC auttaa tässä projektissa?

- Jokaisella osalla on selkeä vastuu.
- Sovelluksen kasvattaminen (esim. muokkausdialogi) on suoraviivaisempaa.
- Testaaminen helpottuu, kun tiedostologiikka on erotettu omaksi luokakseen.

<task>
  <task-title>Tehtävä 8.2: TODO-ohjelma, vaihe 8. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-2-todo-8/handout.md}}

  </handout>
</task>
