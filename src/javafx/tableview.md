# TableView

## Tyhjän rivin klikkaaminen

Oletuksena TableView-komponentti *ei* poista valintaa, jos käyttäjä klikkaa tyhjää riviä. Tämä on usein epäintuitiivista.

Tyhjän rivin klikkaaminen saadaan koodissa kiinni esimerkiksi asettamalla
riveille `setOnMouseClicked`-kuuntelija, joka tarkistaa, onko klikattu rivi `null` ja poistaa valinnan, jos näin on.

```java,ignore
tableView.setRowFactory(tv -> {
    TableRow<MyData> rivi = new TableRow<>();
    rivi.setOnMouseClicked(tapahtuma -> {
        if (rivi.isEmpty()) {
            tableView.getSelectionModel().clearSelection();
        }
    });
    return rivi;
});
```

## Rivien suodattaminen {#filteredlist}

Esimerkki on pitkähkö; löydät sen kokonaisuudessaan [GitHubista](https://github.com/ohj-perus-jy/ohj2/tree/main/src/examples/javafx/FilteredList).

`TableView`-komponentti ei tarjoa suoraan tukea rivien
suodattamiseen.JavaFX-kirjastossa on `FilteredList`-luokka, joka mahdollistaa
suodattamisen.

Oletetaan, että meillä on tehtäviä ja kategorioita. Kukin tehtävä kuuluu
johonkin yhteen kategoriaan. Haluamme valita kategorian pudotusvalikosta ja
nähdä vain kyseiseen kategoriaan kuuluvat tehtävät.

`Tehtävä` ja `Kategoria` voisivat näyttää seuraavilta:

```java,ignore
// FILE: Tehtava.java
package fi.jyu.ohj2.esimerkit.filteredlist;

//- import javafx.beans.property.ObjectProperty;
//- import javafx.beans.property.SimpleObjectProperty;
//- import javafx.beans.property.SimpleStringProperty;
//- import javafx.beans.property.StringProperty;
//- 
public class Tehtava {

    private final StringProperty otsikko = new SimpleStringProperty();
    private final ObjectProperty<Kategoria> kategoria = new SimpleObjectProperty<>();

    public Tehtava() {
        // Tarvitaan Jacksonille
    }

    public Tehtava(String otsikko, Kategoria kategoria) {
        this.otsikko.set(otsikko);
        this.kategoria.set(kategoria);
    }

    // Otsikko
    public void setOtsikko(String otsikko) {
        this.otsikko.set(otsikko);
    }

    public String getOtsikko() {
        return otsikko.get();
    }

    public StringProperty otsikkoProperty() {
        return otsikko;
    }

    // Kategoria
    public void setKategoria(Kategoria kategoria) {
        this.kategoria.set(kategoria);
    }

    public Kategoria getKategoria() {
        return kategoria.get();
    }

    public ObjectProperty<Kategoria> kategoriaProperty() {
        return kategoria;
    }
}
// FILE_END
// FILE: Kategoria.java
package fi.jyu.ohj2.esimerkit.filteredlist;

//- import javafx.beans.property.SimpleStringProperty;
//- import javafx.beans.property.StringProperty;
//- 
public class Kategoria {

    private final StringProperty nimi = new SimpleStringProperty();

    public Kategoria() {
        // Tarvitaan Jacksonille
    }

    public Kategoria(String nimi) {
        this.nimi.set(nimi);
    }

    // Nimi
    public void setNimi(String nimi) {
        this.nimi.set(nimi);
    }

    public String getNimi() {
        return nimi.get();
    }

    public StringProperty nimiProperty() {
        return nimi;
    }

    public String toString() {
        return getNimi();
    }
}
// FILE_END
```

Käyttöliittymä voisi näyttää vaikkapa seuraavalta: Meillä on `TableView`
tehtävien näyttämistä varten, `CheckBox`-komponentti, jolla aktivoidaan
suoritus, ja `ComboBox`-komponentti, josta valitaan kategoria.

<img src="images/filtered1.png" alt="Käyttöliittymä suodatukselle" width="300"/>

Tee kullekin elementille fx:id ja vastaavat kentät kontrolleriin. 

Lisää attribuutti `FilteredList<Tehtava> suodatetutTehtavat` kontrolleriin. 

Kun olet ladannut tehtävät ja kategoriat esimerkiksi JSON-tiedostosta, luo `FilteredList`-olio ja aseta se `TableView`-komponentin datalähteeksi:

```java,ignore
// Oletetaan, että tehtavat on ladattu ObservableListiin nimeltä 'tehtavat'
suodatetutTehtavat = new FilteredList<>(tehtavat, t -> true);
tableView.setItems(suodatetutTehtavat);
```

Tässä `t -> true` on lambdalauseke joka määrittää mitkä tehtävät näytetään.
Aluksi kaikki näytetään, koska ehto on aina tosi.

Lisätään `ComboBox`-komponentille kuuntelija, joka päivittää suodatuskriteeriä:

```java,ignore
comboBox.setOnAction(event -> { 
    paivitaSuodatus();
});

private void paivitaSuodatus() {
    Kategoria valittuKategoria = comboBox.getSelectionModel().getSelectedItem();
    suodatetutTehtavat.setPredicate(t -> 
        t.getKategoria().getNimi().equals(valittuKategoria.getNimi())
    ); 
}
```

Tässä `setPredicate`-metodi määrittää suodatuskriteerin. Jos kategoria on
valitsematta, näytetään kaikki tehtävät. Muuten näytetään vain ne tehtävät,
joiden kategoria vastaa valittua kategoriaa.

Tässä on kuitenkin se ongelma, että kerran valittua filtteröintiä ei voida
poistaa. Siksi lisäsimme `CheckBox`-komponentin, jolla filtteröinti voidaan
aktivoida ja deaktivoida. Muutetaan `paivitaSuodatus`-metodia seuraavasti:

```java,ignore
private void paivitaSuodatus() {
    Kategoria valittuKategoria = comboBox.getSelectionModel().getSelectedItem();
    if (checkBox.isSelected() && valittuKategoria != null) {
        suodatetutTehtavat.setPredicate(t -> 
        t.getKategoria().getNimi().equals(valittuKategoria.getNimi()) 
    ); 
    } else {
        suodatetutTehtavat.setPredicate(t -> true); // Näytä kaikki
    }
}
```

Suodatus kannattaa disabloida kokonaan, kun `CheckBox`-komponentti ei ole
valittuna. Tämä onnistuu esimerkiksi näin.

```java,ignore
comboBox.disableProperty().bind(checkBox.selectedProperty().not());
```

Tämä rivi vaatinee hieman selitystä. Tässä `comboBox`-komponentti sidotaan
`checkBox`-komponentin `selected`-ominaisuuden käänteiseen arvoon. Tämä
tarkoittaa, että `comboBox` on käytössä vain silloin, kun `checkBox` on
valittuna. Tämä `selectedProperty` on olemassa `CheckBox`-komponentissa
valmiina, joten sitä ei tarvitse erikseen määritellä.

Lopputulos näyttää vaikkapa tältä:

<img src="images/filtered2.gif" alt="Suodatettu näkymä" width="300"/>