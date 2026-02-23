# TableView ja databinding

Osassa 7 tehtävät näytettiin `VBox`-säiliöissä `CheckBox`-komponentteina.
Se toimii pienelle datalle, mutta skaalautuu huonosti, kun tehtäviä on paljon.

`TableView` on tähän tilanteeseen parempi ratkaisu:

- data on rivimuotoista
- sarakkeet voidaan lajitella
- valinta, suodatus ja muokkaus toimivat yhtenäisesti

## FXML-rakenne

Lisää näkymään taulukko:

```xml
<TableView fx:id="tehtavaTaulu">
    <columns>
        <TableColumn fx:id="otsikkoCol" text="Tehtävä" />
        <TableColumn fx:id="prioriteettiCol" text="Prioriteetti" />
        <TableColumn fx:id="tehtyCol" text="Tehty" />
    </columns>
</TableView>
```

## Sarakkeiden kytkeminen propertyihin

```java
@FXML
private TableView<Tehtava> tehtavaTaulu;
@FXML
private TableColumn<Tehtava, String> otsikkoCol;
@FXML
private TableColumn<Tehtava, Prioriteetti> prioriteettiCol;
@FXML
private TableColumn<Tehtava, Boolean> tehtyCol;
```

`initialize`-metodissa:

```java
otsikkoCol.setCellValueFactory(cd -> cd.getValue().otsikkoProperty());
prioriteettiCol.setCellValueFactory(cd -> cd.getValue().prioriteettiProperty());
tehtyCol.setCellValueFactory(cd -> cd.getValue().tehtyProperty());

tehtavaTaulu.setItems(viewModel.getTehtavat());
```

## CheckBox-sarake

Boolean-sarakkeelle kannattaa asettaa `CheckBoxTableCell`, jolloin käyttäjä voi
klikata tehtävätilan suoraan taulukossa:

```java
tehtyCol.setCellFactory(CheckBoxTableCell.forTableColumn(tehtyCol));
tehtyCol.setEditable(true);
tehtavaTaulu.setEditable(true);
```

## Suodatus FilteredListillä

Kun data on `ObservableList`issä, suodatus onnistuu ilman erillistä kopiota:

```java
FilteredList<Tehtava> suodatettu = new FilteredList<>(viewModel.getTehtavat(), t -> true);
SortedList<Tehtava> lajiteltu = new SortedList<>(suodatettu);

lajiteltu.comparatorProperty().bind(tehtavaTaulu.comparatorProperty());
tehtavaTaulu.setItems(lajiteltu);
```

Esimerkiksi näyttämään vain tekemättömät:

```java
suodatettu.setPredicate(t -> !t.isTehty());
```

## Poisto valitusta rivistä

`TableView` pitää valitun rivin helposti saatavilla:

```java
poistaPainike.setOnAction(e -> {
    Tehtava valittu = tehtavaTaulu.getSelectionModel().getSelectedItem();
    if (valittu != null) {
        viewModel.poistaTehtava(valittu);
    }
});
```

Tällä muutoksella näkymä muuttuu selvästi hallittavammaksi ja valmiiksi
seuraavaan vaiheeseen: tehtävän yksityiskohtien muokkaukseen.

<task>
  <task-title>Tehtävä 8.3: TODO-ohjelma, vaihe 9. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-3-todo-9/handout.md}}

  </handout>
</task>
