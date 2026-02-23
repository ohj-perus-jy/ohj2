# MVVM-arkkitehtuuri

Nyt kun tehtävädata on eriytetty malliksi, seuraava askel on selkeä rakenne
kokonaiselle sovellukselle.

Tässä materiaalissa käytämme MVVM-jäsennystä, joka on JavaFX-projekteissa
käytännöllinen tapa erottaa käyttöliittymän logiikka, data ja näkymä.
Samat ideat pätevät myös MVC-ajatteluun.

## Kerrosten vastuut

`Model`

- Kuvaa sovelluksen dataa (`Tehtava`, `Prioriteetti`).
- Ei tunne näkymäkomponentteja.

`ViewModel`

- Sisältää näkymän tarvitseman datan `Observable`-muodossa.
- Tarjoaa metodit näkymän toimintoihin (lisää, poista, suodata, tallenna).
- Ei suoraan tunne FXML:ää.

`View + Controller`

- FXML kuvaa näkymärakenteen.
- Controller yhdistää komponentit ViewModeliin.
- Controllerin pitää olla ohut: ei raskasta domain-logiikkaa.

`Repository`

- Vastaa tiedon lukemisesta ja kirjoittamisesta (`JSON`).
- Ei tunne JavaFX-näkymää.

## Esimerkkirakenne

Yksi mahdollinen pakettijako:

```text
fi/jyu/ohj2/nimi/todo/
  model/
    Tehtava.java
    Prioriteetti.java
  persistence/
    TehtavaRepository.java
    JsonTehtavaRepository.java
  viewmodel/
    TodoViewModel.java
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

`JsonTehtavaRepository` toteuttaa tämän rajapinnan käyttäen Jacksonia.

## ViewModel-luokka

```java
public class TodoViewModel {
    private final ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList();
    private final TehtavaRepository repository;

    public TodoViewModel(TehtavaRepository repository) {
        this.repository = repository;
    }

    public ObservableList<Tehtava> getTehtavat() {
        return tehtavat;
    }

    public void lisaaTehtava(String otsikko) {
        if (otsikko == null || otsikko.isBlank()) {
            return;
        }
        tehtavat.add(new Tehtava(otsikko.trim(), false));
    }

    public void poistaTehtava(Tehtava tehtava) {
        tehtavat.remove(tehtava);
    }
}
```

## Controllerin rooli

Controller ei luo tehtäväolioita käsin eikä serialisoi JSONia.
Se tekee lähinnä kolme asiaa:

- lukee syötteet komponenteista
- kutsuu ViewModel-metodeja
- sitoo komponentit ViewModelin dataan

Tällöin esimerkiksi nappikäsittelijä pysyy lyhyenä:

```java
lisaaUusiTehtavaPainike.setOnAction(e -> {
    viewModel.lisaaTehtava(uusiTehtavaNimi.getText());
    uusiTehtavaNimi.clear();
    uusiTehtavaNimi.requestFocus();
});
```

## Mitä hyötyä tästä on?

- Sovelluslogiikka on testattavissa ilman JavaFX-käynnistystä.
- JSON-tallennuksen voi vaihtaa myöhemmin tietokantaan ilman UI-muutoksia.
- Uusien näkymien lisääminen (esim. muokkausdialogi) on helpompaa.

<task>
  <task-title>Tehtävä 8.2: TODO-ohjelma, vaihe 8. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-2-todo-8/handout.md}}

  </handout>
</task>
