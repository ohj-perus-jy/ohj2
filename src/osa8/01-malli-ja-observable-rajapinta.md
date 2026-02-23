# Malli ja Observable-rajapinta

Osassa 7 tehtävät mallinnettiin käyttöliittymäkomponentteina (`CheckBox`).
Ratkaisu oli hyvä aloitus, mutta pidemmällä aikavälillä se tekee sovelluksesta
jäykän: data ja käyttöliittymä ovat liian vahvasti sidottuja toisiinsa.

Tässä luvussa erotamme datan omaksi malliksi ja kytkemme sen JavaFX:n
`Observable`-rajapintoihin.

## Miksi erillinen malli?

Kun tehtävä on oma olionsa, voimme:

- tallentaa ja ladata sen helpommin tiedostosta
- testata sovelluslogiikkaa ilman käyttöliittymää
- käyttää samaa dataa useassa näkymässä
- lisätä ominaisuuksia (kuvaus, prioriteetti, deadline) ilman UI-hakkerointia

## Mitä Observable tarkoittaa JavaFX:ssä?

JavaFX:ssä sana *observable* tarkoittaa, että olio osaa ilmoittaa muutoksista.
Käytännössä osa luokista toteuttaa tämän suoraan, ja osa rakentuu sen päälle:

- `ObservableList<T>`: kuunnellaan listan lisäyksiä/poistoja.
- `ObservableValue<T>`: kuunnellaan yksittäisen arvon muutoksia.
- `Property`-tyypit (`StringProperty`, `BooleanProperty`, ...): erityisiä
  `ObservableValue`-tyyppejä, joita voi myös sitoa (`bind`).

## Hyvin pieni esimerkki ensin

Ennen TODO-mallia katsotaan miniesimerkki pelkällä merkkijonolistalla:

```java
ObservableList<String> nimet = FXCollections.observableArrayList();

nimet.addListener((ListChangeListener<String>) change -> {
    while (change.next()) {
        if (change.wasAdded()) {
            System.out.println("Lisättiin: " + change.getAddedSubList());
        }
    }
});

nimet.add("Ada");
nimet.add("Linus");
```

Mitä tästä kannattaa huomata:

- Muutoksia ei tarvitse erikseen “pollata”.
- Kun listaan lisätään arvo, kuuntelija saa tiedon heti.

Jos sama lista on kytketty esimerkiksi `ListView`-komponenttiin
`listView.setItems(nimet)`, käyttöliittymä päivittyy automaattisesti.

## Pieni Tehtava-malli (ilman propertyjä)

Ennen laajaa mallia tehdään ensin tarkoituksella pieni malli:

```java
public class Tehtava {
    private String otsikko;
    private boolean tehty;

    public Tehtava(String otsikko, boolean tehty) {
        this.otsikko = otsikko;
        this.tehty = tehty;
    }

    public String getOtsikko() {
        return otsikko;
    }

    public void setOtsikko(String otsikko) {
        this.otsikko = otsikko;
    }

    public boolean isTehty() {
        return tehty;
    }

    public void setTehty(boolean tehty) {
        this.tehty = tehty;
    }
}
```

Sitten lista:

```java
private final ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList();
```

Nyt meillä on jo kolme tärkeää asiaa:

- tehtävä on *dataolio*, ei UI-komponentti
- tehtävät ovat yhdessä listassa
- lista on observable, joten näkymä voi kuunnella sitä suoraan

## Miksi tämä ei vielä riitä?

`ObservableList` kertoo, kun listaan lisätään tai poistetaan tehtäviä.
Mutta jos yhden tehtävän sisäinen kenttä muuttuu (`otsikko`/`tehty`), lista ei
yksin aina riitä automaattiseen UI-päivitykseen.

Siksi JavaFX-sovelluksissa kannattaa käyttää mallin kentissä propertyjä.

## Laajennetaan Tehtava-malli property-pohjaiseksi

```java
public class Tehtava {
    private final StringProperty otsikko = new SimpleStringProperty("");
    private final StringProperty kuvaus = new SimpleStringProperty("");
    private final BooleanProperty tehty = new SimpleBooleanProperty(false);
    private final ObjectProperty<Prioriteetti> prioriteetti =
            new SimpleObjectProperty<>(Prioriteetti.KESKI);

    public Tehtava() {}

    public Tehtava(String otsikko, boolean tehty) {
        setOtsikko(otsikko);
        setTehty(tehty);
    }

    public String getOtsikko() { return otsikko.get(); }
    public void setOtsikko(String value) { otsikko.set(value); }
    public StringProperty otsikkoProperty() { return otsikko; }

    public String getKuvaus() { return kuvaus.get(); }
    public void setKuvaus(String value) { kuvaus.set(value); }
    public StringProperty kuvausProperty() { return kuvaus; }

    public boolean isTehty() { return tehty.get(); }
    public void setTehty(boolean value) { tehty.set(value); }
    public BooleanProperty tehtyProperty() { return tehty; }

    public Prioriteetti getPrioriteetti() { return prioriteetti.get(); }
    public void setPrioriteetti(Prioriteetti value) { prioriteetti.set(value); }
    public ObjectProperty<Prioriteetti> prioriteettiProperty() { return prioriteetti; }
}
```

Prioriteetti voidaan mallintaa enumilla:

```java
public enum Prioriteetti {
    MATALA, KESKI, KORKEA
}
```

## Listan perusoperaatiot

Kun malli on kunnossa, ViewModeliin (tai vastaavaan logiikkaluokkaan) voi tehdä
perusmetodit:

```java
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
```

## Reagointi muutoksiin yhdessä paikassa

Tallennuksen voi kytkeä listan muutoksiin:

```java
tehtavat.addListener((ListChangeListener<Tehtava>) change -> {
    while (change.next()) {
        if (change.wasAdded() || change.wasRemoved()) {
            tallenna();
        }
    }
});
```

Näin tallennus voidaan tehdä yhdessä paikassa ilman, että jokaiseen nappiin
kirjoitetaan erillinen `tallenna()`-kutsu.

## JSON ja propertyt

Jackson ei suoraan tykkää JavaFX-property-objekteista. Käytännössä on selkeintä
tehdä erillinen DTO-luokka tiedostomuotoa varten:

```java
public record TehtavaDto(
        String otsikko,
        String kuvaus,
        boolean tehty,
        String prioriteetti
) {}
```

Silloin muunnos tehdään eksplisiittisesti:

- `Tehtava -> TehtavaDto` tallennuksessa
- `TehtavaDto -> Tehtava` latauksessa

Tämä pitää käyttöliittymämallin ja tiedostomuodon erillään.

<task>
  <task-title>Tehtävä 8.1: TODO-ohjelma, vaihe 7. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-1-todo-7/handout.md}}

  </handout>
</task>
