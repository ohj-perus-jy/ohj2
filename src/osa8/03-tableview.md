# TableView ja databinding

Osassa 7 tehtävät näytettiin `VBox`-säiliöissä `CheckBox`-komponentteina. Tämä
on oikein hyvä tapa opetella käyttöliittymän perusidea: luodaan komponentteja ja
lisätään ne näkymään. Menetelmä alkaa kuitenkin muuttua hankalaksi, kun dataa on
enemmän tai kun käyttöliittymältä halutaan enemmän toiminnallisuutta
(esimerkiksi lajittelu, rivin valinta, muokkaus tai useiden kenttien näyttäminen
siististi vierekkäin).

Tässä kohtaa käyttöön tulee `TableView`, eli taulukkokomponentti. `TableView` on
JavaFX:n valmis komponentti sellaisten tietojen näyttämiseen, jotka ovat
luonteeltaan rivi–sarake-muotoisia. Ajattele esimerkiksi taulukkoa, jossa
jokainen rivi on yksi tehtävä ja sarakkeet ovat tehtävän ominaisuuksia, kuten
otsikko, prioriteetti ja tehty/tekemättä-tila.

Tässä luvussa hyödynnämme myös JavaFX:n *propertyjä* ja databinding-ajattelua.
Property (esimerkiksi StringProperty tai BooleanProperty) on JavaFX:n tapa
mallintaa arvoja niin, että niiden muutoksia voidaan kuunnella. Käytännössä tämä
tarkoittaa sitä, että taulukon solut kytketään suoraan `Tehtava`-olion
attribuuttien arvoihin. Tällöin käyttöliittymässä oleva näkymä pysyy
automaattisesti synkronissa datan kanssa: kun arvo muuttuu datassa, näkymä
päivittyy, ja kun käyttäjä muuttaa arvoa taulukossa, muutos päivittyy samaan
propertyyn. 

Tämä on tärkeä ero verrattuna “kopioi arvo käyttöliittymään” -ajatteluun.
Taulukon soluun ei yleensä aseteta irrallista arvoa käsin, vaan solu lukee arvon
rivin olion propertystä. Siksi sama data voi olla käytössä yhtä aikaa sekä
ohjelman logiikassa että käyttöliittymässä ilman, että meidän tarvitsee jatkuvasti
synkronoida arvoja käsin.

Seuraavaksi rakennamme taulukon FXML:ään ja kytkemme sen kontrollerissa dataan.
Etenemme luvussa ohjelman toiminnan kannalta luontevassa järjestyksessä: ensin
määrittelemme näkymän rakenteen FXML:ssä, sitten kytkemme sarakkeet
`Tehtava`-olion propertyihin kontrollerissa, ja lopuksi teemme
boolean-sarakkeesta klikattavan checkbox-sarakkeen, jonka muutokset voidaan
tallentaa automaattisesti.

## FXML-rakenne

Aloitetaan näkymästä. FXML-tiedostossa määritellään, että käyttöliittymässä on
taulukko (`TableView`) ja sen sisällä kolme saraketta (`TableColumn`). Tässä
vaiheessa emme vielä kerro, mistä data tulee tai mitä sarakkeet näyttävät
käyttäjälle. Määrittelemme vain rakenteen: taulukko on olemassa, ja siinä on
sarakkeet otsikolle, prioriteetille ja tehty-tilalle.

```xml
<TableView fx:id="tehtavaTaulu">
    <columns>
        <TableColumn fx:id="otsikkoCol" text="Tehtävä" />
        <TableColumn fx:id="prioriteettiCol" text="Prioriteetti" />
        <TableColumn fx:id="tehtyCol" text="Tehty" />
    </columns>
</TableView>
```

Tässä on hyvä pysähtyä muutaman asian äärelle.

`TableView` on itse taulukko. Se näyttää rivejä, mutta ei vielä tiedä, millaisia
olioita rivit ovat. Se tieto annetaan kontrollerin puolella Java-koodissa.
FXML:ssä tärkeintä on antaa taulukolle fx:id, jotta kontrolleri voi viitata
siihen.

`<columns>`-lohko sisältää taulukon sarakkeet. Jokainen `TableColumn` kuvaa yhtä
näkyvää saraketta taulukossa. Sarakkeella on tässä kaksi olennaista asiaa:

 * `fx:id`, jonka avulla kontrolleri pääsee käsiksi juuri tähän sarakkeeseen
 * `text`, joka näkyy sarakkeen otsikkona käyttöliittymässä

On tärkeä huomata, että tässä vaiheessa sarakkeet ovat vasta "tyhjiä kuoria". Ne
näkyvät taulukossa otsikoineen, mutta niissä ei vielä näy mitään dataa.
Seuraavassa vaiheessa kerromme, mitä arvoa kukin sarake näyttää kustakin
`Tehtava`-oliosta.

## Sarakkeiden kytkeminen propertyihin

Kun FXML-rakenne on määritelty, kontrollerin tehtävä on yhdistää näkymä ja data.
Tämä tapahtuu kahdessa osassa. Ensin kontrolleriin määritellään viittaukset
FXML:ssä luotuihin komponentteihin. Sen jälkeen `initialize()`-metodissa asetetaan
taulukolle data ja kerrotaan jokaiselle sarakkeelle, mitä propertyä sen tulee
näyttää.

Controlleriin lisätään ensin `@FXML`-kentät:

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

`TableColumn<Tehtava, String>` tarkoittaa kahta asiaa:

 * ensimmäinen tyyppi (`Tehtava`) = minkä tyyppisiä olioita taulukon riveillä on
 * toinen tyyppi (`String`) = minkä tyyppinen arvo tässä sarakkeessa näytetään

Siksi `otsikkoCol` näyttää `String`-arvon (tehtävän otsikko), `prioriteettiCol`
näyttää `Prioriteetti`-arvon (tehtävän prioriteetti) ja `tehtyCol` näyttää
`Boolean`-arvon (tehtävän tehty/tekemättä-tila).

On erittäin tärkeää huomata, että sarake ei sisällä kokonaista `Tehtava`-oliota,
vaan se näyttää yhden ominaisuuden kyseisestä oliosta.

Seuraavaksi `initialize()`-metodissa kytketään taulukko dataan ja sarakkeet
propertyihin.

```java,ignore
@FXML
public void initialize() {
    tehtavaTaulu.setItems(tehtavat);

    otsikkoCol.setCellValueFactory(cd -> cd.getValue().otsikkoProperty());
    prioriteettiCol.setCellValueFactory(cd -> cd.getValue().prioriteettiProperty());
    tehtyCol.setCellValueFactory(cd -> cd.getValue().tehtyProperty());
    
    // ...
}
```

Käydään tämä rauhassa rivi riviltä läpi.

 * **`setItems(...)` — mitä taulukko näyttää riveinä?** Tämä rivi kertoo
taulukolle, mistä sen rivit tulevat. Meidän tapauksessamme `tehtavat` on
`ObservableList<Tehtava>`, joka sisältää kaikki tehtävät. Sana
*Observable* tarkoittaa, että lista osaa ilmoittaa muutoksista, eli esimerkiksi
jos rivejä lisätään tai poistetaan, `TableView` päivittää näkymän
automaattisesti. Ilman tätä riviä taulukko olisi olemassa, mutta se olisi tyhjä.
 * **`setCellValueFactory(...)` — mitä kukin sarake näyttää?** Esimerkiksi
   ```java,ignore
   otsikkoCol.setCellValueFactory(cd -> cd.getValue().otsikkoProperty());
   ```
   tarkoittaa käytännössä: *Kun taulukko tarvitsee arvon `otsikkoCol`-sarakkeeseen
   jollekin riville, hae kyseisen rivin `Tehtava`-oliosta `otsikkoProperty()`.*
   
Tässä 

 * `cd` tulee sanasta cell data (solun dataa kuvaava olio), 
 * `cd.getValue()` palauttaa kyseisen rivin `Tehtava`-olion
 * `otsikkoProperty()` palauttaa propertyn, josta sarake lukee näytettävän arvon. 
   
Sama idea toistuu muille sarakkeille. Tämä on juuri *databinding*-ajattelun ydin
tässä yhteydessä: sarake ei saa "kopiota" arvosta, vaan se kytketään propertyyn,
joka kuuluu rivin olioon.

Miksi tämä on parempi kuin arvojen asettaminen käsin? Jos tekisimme tämän ilman
propertyjä ja `TableView`:ta, joutuisimme usein itse luomaan jokaiselle riville
komponentit, täyttämään ne arvoilla sekä päivittämään näkymän erikseen, kun data
muuttuu. `TableView` yhdessä propertyjen kanssa vähentää tätä käsityötä
merkittävästi. Koodi kertoo enemmän siitä, mitä halutaan näyttää, eikä niinkään
siitä, miten jokainen pikseli päivitetään.

Huomautuksena: sarakkeet voidaan määritellä FXML:ään (kuten tässä teemme), mutta
ne voidaan myös luoda kokonaan Java-koodissa. SceneBuilder helpottaa usein FXML:n
rakenteen tekemistä, mutta sarakkeiden varsinainen datakytkentä tehdään silti
yleensä controllerissa.

## CheckBox-sarake ja tehtävien muutosten tallentaminen

`tehtyCol` on erityistapaus, koska se näyttää boolean-arvon (true / false).
Pelkkä true tai false tekstinä ei ole käyttöliittymässä kovin hyvä ratkaisu.
Käyttäjälle luonnollisempi tapa on klikata suoraan valintaruutua. Tätä varten
boolean-sarakkeelle voidaan asettaa `CheckBoxTableCell`.

```java
tehtyCol.setCellFactory(CheckBoxTableCell.forTableColumn(tehtyCol));
tehtyCol.setEditable(true);
tehtavaTaulu.setEditable(true);
```

Tässä tapahtuu kolme asiaa:

 * `setCellFactory(...)` määrittää, millaisena soluna sarake piirretään.
Nyt jokainen `tehtyCol`-sarakkeen solu näkyy checkboxina.
 * `tehtyCol.setEditable(true)` sallii tämän sarakkeen muokkauksen.
 * `tehtavaTaulu.setEditable(true)` sallii muokkauksen taulukkotasolla. (Pelkkä
   sarakkeen muokattavuus ei yleensä riitä, myös taulukon pitää olla muokattava.)

Tässä vaiheessa käyttäjä voi klikata checkboxia taulukossa, ja `tehtyProperty`
muuttuu myös taustalla. Mutta vielä yksi tärkeä asia puuttuu: miten muutos
tallennetaan tiedostoon?

Pelkkä klikattava checkbox ei automaagisesti kutsu `tallenna()`-metodia.
Checkbox muuttaa datan arvoa, mutta tallennuslogiikka täytyy kytkeä erikseen.
Tämä tehdään lisäämällä kuuntelija `tehtyProperty`:n.

## Tallennus propertyn muutoksesta

Yksi ratkaisu olisi sellainen, että kytkisimme `Tehtava`-olion `tehtyProperty`:n
muutokseen kuuntelijan, joka kutsuu tallennusta. Tämä tarkoittaa, että aina kun
`tehtyProperty` muuttuu (esimerkiksi checkboxia klikataan), tallennus tapahtuu
automaattisesti. Tämä olisi sinänsä kätevää, mutta pieneksi ongelmaksi
muodostuu, että Jackson-kirjaston kautta ladatut `Tehtava`-oliot eivät tätä
kuuntelijaa saa. Jackson-nimittäin luo `Tehtava`-olion suoraan konstruktorilla,
eikä se käytä setter-metodeja, joissa kuuntelija voisi olla. Voisimme kyllä
lisätä kuuntelijan erikseen jokaiselle `Tehtava`-oliolle.

Tähän on kuitenkin toinenkin, aavistuksen elegantimpi ratkaisu. Muistamme, että
`ObservableList` osaa ilmoittaa, kun sen sisältö muuttuu. Sille voidaan
kuitenkin antaa niin sanottu *ekstraktori* (extractor), joka kertoo listalle, mitä kunkin
olion propertyjä seurataan. 

Muuta `ObservableList`-kokoelman luonti seuraavasti:

```java,ignore
private final ObservableList<Tehtava> tehtavat 
   = FXCollections.observableArrayList(tehtava -> new Observable[] {tehtava.tehtyProperty()});
```

Tässä `tehtava -> new Observable[] { ... }` on ekstraktori. Se palauttaa
taulukon niistä `Observable`-olioista (käytännössä propertyistä), joita listan
halutaan seuraavan jokaisessa `Tehtava`-oliossa. Ekstraktori ei siis korvaa
propertyjen kuuntelijoita tallennusta varten; Tallennuskuuntelija kertoo mitä
tehdään, kun arvo muuttuu (esim. `tallenna()`), kun taas extractor kertoo
listalle mitä propertyjä kannattaa ylipäätään seurata.

## Miksi tallennus sidotaan propertyyn eikä checkboxin klikkaukseen?

Tämä on hyvä suunnitteluratkaisu. Jos tallennus sidotaan checkboxin
klikkaukseen, tallennus toimii vain silloin, kun muutos tapahtuu juuri sitä
kautta. Mutta jos sama `tehtyProperty` muuttuu myöhemmin jostakin muusta syystä
(esimerkiksi toisesta metodista), tallennus ei ehkä tapahdu.

Kun tallennus sidotaan propertyn muutokseen, logiikka on yleisempi ja
turvallisempi:

*Aina kun tehtävän tila muuttuu, tallenna.*

Tämä on databinding- ja property-ajattelun suuri etu: muutokset havaitaan
datatasolla, ei vain yksittäisen käyttöliittymätoiminnon kautta.

## Tehdyt tehtävät taulukon loppuun

`TableView` tukee lajittelua, mutta tehtyjen tehtävien siirtäminen taulukon
loppuun kannattaa toteuttaa tietoisesti määritellyllä lajittelulla. Yksi hyvä
tapa on käyttää `SortedList`-kokoelmaa, joka käärii alkuperäisen
`ObservableList<Tehtava>`-listan.

Ajatus on tämä

 * varsinainen data on edelleen ObservableList<Tehtava>-listassa
 * taulukolle annetaan näkyväksi dataksi SortedList<Tehtava>
 * lajittelukomparaattori määrittää, että tekemättömät tulevat ennen tehtyjä

```java,ignore
SortedList<Tehtava> lajitellut = new SortedList<>(tehtavat,
        Comparator.comparing(Tehtava::isTehty)); // false ennen true

tehtavaTaulu.setItems(lajitellut);
```

Koska `false` (tekemätön) tulee ennen `true` (tehty), tekemättömät tehtävät
näkyvät taulukossa ensin ja tehdyt lopussa.


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
