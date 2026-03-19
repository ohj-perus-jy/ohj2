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

Tämä rivi vaatinee hieman selitystä. Tässä `comboBox`-komponentin sitominen
*disabloidaan* `checkBox`-komponentin `selected`-ominaisuuden käänteisen arvon
mukaisesti. Toisin sanoen, kun `checkBox` on valittuna, `comboBox`-komponenttia
"ei disabloida". JavaFX:ssä ei ole `enableProperty()`-metodia, joten meidän on
käytettävä `disableProperty()`-metodia ja käännettävä sen arvo.

Tämä `selectedProperty` on olemassa `CheckBox`-komponentissa
valmiina, joten sitä ei tarvitse erikseen määritellä.

Lopputulos näyttää vaikkapa tältä:

<img src="images/filtered2.gif" alt="Suodatettu näkymä" width="300"/>

## Solujen uudelleenmuotoilu

Tämäkin esimerkki löytyy kokonaisuudessaan [GitHubista](https://github.com/ohj-perus-jy/ohj2/tree/main/src/examples/javafx/CellFactory).

Joskus voi olla tarvetta muuttaa solun ulkoasua tietyissä olosuhteissa.

Jatkaen edellistä esimerkkiä, oletetaan, että kategorioita voisi poistaa.
Poistettu kategoria halutaan näyttää punaisella tekstillä, jotta käyttäjä
huomaa, että kategoria on poistettu. Käyttöliittymä voisi näyttää vaikkapa
seuraavalta:

<img src="images/filtered3.gif" alt="Poistettu kategoria punaisella"
width="400"/>

Tieto siitä, onko kategoria poistettu, voisi olla `Kategoria`-luokan
ominaisuutena, ja luonnollisesti mukana myös JSON-tiedostossa. Katso esimerkit
näistä luokista GitHubista: [Kategoria.java](https://github.com/ohj-perus-jy/ohj2/blob/29df2988f92a002812842c0cb03dc054c86565ae/src/examples/javafx/CellFactory/src/main/java/fi/jyu/ohj2/esimerkit/cellfactory/Kategoria.java#L38), [kategoriat.json](https://github.com/ohj-perus-jy/ohj2/blob/main/src/examples/javafx/CellFactory/kategoriat.json).

Toki voisimme lisätä taulukkoon uuden sarakkeen, joka näyttää, onko kategoria
poistettu ja tehdä suodatusta sitä kautta. Tämä ei kuitenkaan ole aina kovin
elegantti ratkaisu. Parempi idea on näyttää tieto poistetuista kategorioista
suoraan kategorian nimessä, esimerkiksi punaisella tekstillä. 

Edellisessä esimerkissä lisäsimme kategoriasarakkeen seuraavasti. 

```java,ignore
kategoriaColumn.setCellValueFactory(cellData -> cellData.getValue().kategoriaProperty().asString());
```

Tällä määritellään, mistä tieto soluun haetaan. Sillä ei voi vaikuttaa solun
ulkoasuun. Se täytyy tehdä `setCellFactory`-metodin avulla, kuten opimme [osassa
8.2](../osa8/02-tableview.md#tehty-sarake-valintaruuduksi). Valitettavasti ei
ole mitään valmista `CellFactory`-luokkaa, joka osaisi muuttaa tekstin värin.
Niinpä meillä on kaksi vaihtoehtoa: (1) Voimme tehdä oman `CellFactory`-luokan
perimällä `TableCell`-luokan tai (2) käyttää lambdalauseketta. Ensimmäinen
vaihtoehto on työläämpi, mutta hyödyllinen, jos käytämme samaa logiikkaa
useammassa sarakkeessa tai jopa useammassa taulukossa. Tässä tapauksessa meille
kuitenkin riittää yhden sarakkeen muokkaus, joten käytämme lambdalauseketta. 

```java,ignore
kategoriaColumn.setCellFactory(column -> {
  return new TableCell<Tehtava, String>() {
    @Override
    protected void updateItem(String item, boolean empty) {
      super.updateItem(item, empty);
      if (item == null || empty) { // Tyhjä solu täytyy käsitellä erikseen
          setText(null);
          setStyle("");
      } else {
        setText(item); // Näytä soluun kuuluva teksti
        Tehtava tehtava = getTableRow().getItem(); // Hakee koko rivin datan
        if (tehtava != null && tehtava.getKategoria().isPoistettu()) { 
          setStyle("-fx-text-fill: red;"); // Asettaa poistetun tekstin punaiseksi
        } else {
          setStyle(""); // Palauttaa oletustyylin, jos kategoria ei ole poistettu
        }
      }
    }
  };
});
```

Perusideana on ylikirjoittaa TableCell-luokan `updateItem`-metodi. Tätä metodia
kutsutaan aina, kun TableView-oliossa olevan solun sisältöä tai ulkoasua
tarvitsee päivittää, esimerkiksi kun taulukko renderöidään tai kun solun arvo
muuttuu. Ylikirjoittamalla `updateItem`-metodin voimme määritellä tarkasti,
miten solun sisältö ja ulkoasu päivitetään. 

Lisätään vielä valintapainike, jolla käyttäjä voi näyttää poistetut kategoriat
tai piilottaa ne. Oletuksena tämän valintapainikkeen pitää olla pois päältä ja
silloin näytetään vain ne tehtävät, jotka eivät kuulu poistettuihin
kategorioihin.

```java,ignore
@FXML
private CheckBox naytaMyosPoistetutCheckBox;

// ...

public void initialize(URL url, ResourceBundle resourceBundle) {
    // ...

    naytaMyosPoistetutCheckBox.setOnAction(event -> {
        if (naytaMyosPoistetutCheckBox.isSelected()) {
            suodatetutTehtavat.setPredicate(t -> true); // Näytä kaikki
        } else {
            paivitaSuodatus(); 
        }
    });

    // ...
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
```

Poistettujen kategorioiden valintapainike kannattaa disabloida, kun muu suodatus
on käytössä. 

```
java,ignore
naytaMyosPoistetutCheckBox.disableProperty().bind(suodataCheckBox.selectedProperty());
```

Tämän seurauksena pitää myös resetoida käyttöliittymästä poistettujen
kategorioiden valintapainike suodatuksen yhteydessä.

```java,ignore
suodataCheckBox.selectedProperty()
               .addListener((obs, vanha, uusi) -> 
                naytaMyosPoistetutCheckBox.setSelected(false));
```
