# Validointi, priorisointi ja tehtävien muokkaus

Tässä luvussa lisätään TODO-sovellukseen tehtävän yksityiskohtien muokkaus.
Käyttäjä voi avata tehtävän tuplaklikkaamalla taulukkoriviä, tehdä muutokset ja
tallentaa ne.

## Muokattavat tiedot

Laajennetaan `Tehtava`-mallia kentillä:

- `kuvaus` (`StringProperty`)
- `prioriteetti` (`ObjectProperty<Prioriteetti>`)
- `deadline` (`ObjectProperty<LocalDate>`)

## Tuplaklikkaus avaa muokkausdialogin

Lisää taulukolle hiirikäsittelijä:

```java
tehtavaTaulu.setRowFactory(tv -> {
    TableRow<Tehtava> row = new TableRow<>();
    row.setOnMouseClicked(event -> {
        if (event.getClickCount() == 2 && !row.isEmpty()) {
            avaaMuokkausDialogi(row.getItem());
        }
    });
    return row;
});
```

## Dialogin rakenne

Yksinkertaisimmillaan dialogi sisältää:

- `TextField` otsikolle
- `TextArea` kuvaukselle
- `ComboBox<Prioriteetti>` prioriteetille
- `DatePicker` deadlinelle
- painikkeet `Tallenna` ja `Peruuta`

Voit tehdä dialogin erillisenä FXML-näkymänä tai ohjelmallisesti.

## Validointi

Tallennusta ei pidä sallia, jos otsikko on tyhjä:

```java
String otsikko = otsikkoField.getText();
if (otsikko == null || otsikko.isBlank()) {
    naytaVirhe("Tehtävän nimi ei saa olla tyhjä.");
    return;
}
```

Hyvä käytäntö on myös estää menneisyyteen jäävä deadline:

```java
LocalDate deadline = deadlinePicker.getValue();
if (deadline != null && deadline.isBefore(LocalDate.now())) {
    naytaVirhe("Määräpäivä ei voi olla menneisyydessä.");
    return;
}
```

## Muutosten tallennus malliin

Kun validointi menee läpi, kirjoita arvot takaisin valittuun tehtävään:

```java
tehtava.setOtsikko(otsikkoField.getText().trim());
tehtava.setKuvaus(kuvausArea.getText().trim());
tehtava.setPrioriteetti(prioriteettiCombo.getValue());
tehtava.setDeadline(deadlinePicker.getValue());
```

Koska taulukon sarakkeet ovat sidottu propertyihin, näkymä päivittyy automaattisesti.

## Tallennus tiedostoon muokkauksen jälkeen

Muokkauksen jälkeen kutsu ViewModelin tallennusmetodia:

```java
viewModel.tallenna();
```

Näin myös kuvaus, prioriteetti ja deadline säilyvät sovelluksen uudelleenkäynnistyksen yli.

<task>
  <task-title>Tehtävä 8.4: TODO-ohjelma, vaihe 10. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-4-todo-10/handout.md}}

  </handout>
</task>
