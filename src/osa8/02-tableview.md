# TableView ja databinding

Osassa 7 tehtävät näytettiin `VBox`-säiliöissä `CheckBox`-komponentteina. Tämä
on oikein hyvä tapa opetella käyttöliittymän perusidea: luodaan komponentteja ja
lisätään ne näkymään. 
Huomasimme edellisessä osassa, että mallin ja käyttöliittymän erottaminen
toisistaan vaatii `paivitaNakyma()`-metodia, joka kutsutaan aina, kun malli
muuttuu. Näkymän päivittäminen mallin muuttuessa voi kuitenkin osoittautua
pullonkaulaksi sovelluksen koon kasvaessa, ja näkymän päivittämisen optimointi
on itsessään hankala ongelma, johon ei tämän kurssin puitteissa pureuduta.

Tässä kohtaa onkin parempi nojautua JavaFX:n valmiin näkymäkomponentteihin, jotka
osaavat tehokkaasti esittää olioita ja reagoida niiden muutoksiin.
Otamme tässä luvussa käyttöön `TableView`- eli taulukkokomponentin
`TableView` on
JavaFX:n valmis komponentti, jolla olioita voidaan esittää riveinä ja olioiden
ominaisuuksia sarakkeina.
Ajattele esimerkiksi taulukkoa, jossa
jokainen rivi on yksi tehtävä ja sarakkeet ovat tehtävän ominaisuuksia, kuten
otsikko, prioriteetti ja tehty/tekemättä-tila.

## Esivalmistelu: Tehtävä-luokka havaittavaksi

JavaFX:n `TableView` osaa reagoida olioiden määrän muutosten lisäksi
olioiden attribuuttien muutoksiin. Esimerkiksi, jos jos jonkun tehtävän teksti
muutetaan käyttöliittymässä, `TableView` osaa havaita muutoksen automaattisesti.
Tätä varten kuitenkaan pelkästään `ObservableList`-listan käyttö ei riitä, koska
se osaa havaita vain tehtävien lisäämistä ja poistamista.
Sen sijaan meidän tulee tehdä itse *tehtävät ja niiden ominasuudet
havaittaviksi*.

Olion yksittäisi ominaisuuksia voidaan muuttaa havaittaviksi käyttäen
`Property`-tyyppejä. Property-tyypit "käärivät" tavalliset
arvot, kuten `boolean` tai `String`, ja tarjoavat mekanismin ilmoittaa, kun
niiden arvo muuttuu. Esimerkiksi `StringProperty` on havaittava versio
`String`-tyypistä, `BooleanProperty` vastaavasti `Boolean`-tyypistä ja niin
edelleen. Havaittavat tyypit mahdollistavat sen, että olion yksittäisiä
attribuuttien arvojen muutosta voidaan havaita samalla tavalla kuin
`ObservableList`-listassa voidaan havaita olioiden lisäämistä ja poistoa.

Päivitetään `Tehtava`-mallimme käyttämään `Property`-kääreitä, jotta tehtävän
kaikki tiedot ovat havaittavia.
Yksinkertaisesti sanottuna,
kun aiemmin tehtävällä oli tavallinen `boolean tehty` -muuttuja, joka oli
piilotettu ohjelman uumeniin, muutamme sen nyt _observable_-tyyppiseksi,
`BooleanProperty tehty`-muuttujaksi.





 Tällöin
käyttöliittymässä oleva näkymä pysyy synkronissa datan kanssa: kun arvo muuttuu
datassa, näkymä päivittyy, ja kun käyttäjä muuttaa arvoa taulukossa, muutos
päivittyy samaan propertyyn.

Seuraavaksi rakennamme taulukon FXML:ään ja kytkemme sen kontrollerissa dataan.
Etenemme luvussa ohjelman toiminnan kannalta luontevassa järjestyksessä: ensin
määrittelemme näkymän rakenteen FXML:ssä, sitten kytkemme sarakkeet
`Tehtava`-olion propertyihin kontrollerissa, ja lopuksi teemme
boolean-sarakkeesta klikattavan checkbox-sarakkeen.

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

- `fx:id`, jonka avulla kontrolleri pääsee käsiksi juuri tähän sarakkeeseen
- `text`, joka näkyy sarakkeen otsikkona käyttöliittymässä

On tärkeä huomata, että tässä vaiheessa sarakkeet ovat vasta "tyhjiä kuoria". Ne
näkyvät taulukossa otsikoineen, mutta niissä ei vielä näy mitään dataa.
Seuraavassa vaiheessa kerromme, mitä arvoa kukin sarake näyttää kustakin
`Tehtava`-oliosta.

## Sarakkeiden kytkeminen propertyihin

Kun FXML-rakenne on määritelty, kontrollerin tehtävä on yhdistää näkymä ja data.
Tämä tapahtuu kahdessa osassa. Ensin kontrolleriin määritellään viittaukset
FXML:ssä luotuihin komponentteihin. Sen jälkeen `initialize()`-metodissa
asetetaan taulukolle data ja kerrotaan jokaiselle sarakkeelle, mitä propertyä
sen tulee näyttää.

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

- ensimmäinen tyyppi (`Tehtava`) = minkä tyyppisiä olioita taulukon riveillä on
- toinen tyyppi (`String`) = minkä tyyppinen arvo tässä sarakkeessa näytetään /
  käsitellään

Siksi `otsikkoCol` näyttää `String`-arvon (tehtävän otsikko), `prioriteettiCol`
näyttää `Prioriteetti`-arvon ja `tehtyCol` näyttää `Boolean`-arvon (tehtävän
tehty/tekemättä-tila).

On tärkeä huomata, että sarake ei sisällä kokonaista `Tehtava`-oliota, vaan se
näyttää yhden ominaisuuden kyseisestä oliosta.

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

- **`setItems(...)` — mitä taulukko näyttää riveinä?** Tämä rivi kertoo
  taulukolle, mistä sen rivit tulevat. Meidän tapauksessamme `tehtavat` on
  `ObservableList<Tehtava>`, joka sisältää kaikki tehtävät. Sana _Observable_
  tarkoittaa, että lista osaa ilmoittaa muutoksista, eli esimerkiksi jos rivejä
  lisätään tai poistetaan, `TableView` päivittää näkymän automaattisesti. Ilman
  tätä riviä taulukko olisi olemassa, mutta se olisi tyhjä.
- **`setCellValueFactory(...)` — mitä kukin sarake näyttää?** Esimerkiksi
  ```java,ignore
  otsikkoCol.setCellValueFactory(cd -> cd.getValue().otsikkoProperty());
  ```
  tarkoittaa käytännössä: _Kun taulukko tarvitsee arvon
  `otsikkoCol`-sarakkeeseen jollekin riville, hae kyseisen rivin
  `Tehtava`-oliosta `otsikkoProperty()`._

Tässä

- `cd` tulee sanasta cell data (solun dataa kuvaava olio),
- `cd.getValue()` palauttaa kyseisen rivin `Tehtava`-olion
- `otsikkoProperty()` palauttaa propertyn, josta sarake lukee näytettävän arvon.

Sama idea toistuu muille sarakkeille. Tämä on juuri _databinding_-ajattelun ydin
tässä yhteydessä: sarake ei saa "kopiota" arvosta, vaan se kytketään propertyyn,
joka kuuluu rivin olioon.

Miksi tämä on parempi kuin arvojen asettaminen käsin? Jos tekisimme tämän ilman
propertyjä ja `TableView`:ta, joutuisimme usein itse luomaan jokaiselle riville
komponentit, täyttämään ne arvoilla sekä päivittämään näkymän erikseen, kun data
muuttuu. `TableView` yhdessä propertyjen kanssa vähentää tätä käsityötä
merkittävästi. Koodi kertoo enemmän siitä, mitä halutaan näyttää, eikä niinkään
siitä, miten jokainen pikseli päivitetään.

Huomautuksena: sarakkeet voidaan määritellä FXML:ään (kuten tässä teemme), mutta
ne voidaan myös luoda kokonaan Java-koodissa. SceneBuilder helpottaa usein
FXML:n rakenteen tekemistä, mutta sarakkeiden varsinainen datakytkentä tehdään
silti yleensä controllerissa.

Voimme poistaa `tehtavat.addListener(...)`-kutsusta `paivitaNakyma()`-kutsun
kokonaan, koska `TableView` hoitaa näkymän päivittämisen automaattisesti --
joskin [TODO] ei vielä toimi.

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

- `setCellFactory(...)` määrittää, millaisena soluna sarake piirretään. Nyt
  jokainen `tehtyCol`-sarakkeen solu näkyy checkboxina.
- `tehtyCol.setEditable(true)` sallii tämän sarakkeen muokkauksen.
- `tehtavaTaulu.setEditable(true)` sallii muokkauksen taulukkotasolla. (Pelkkä
  sarakkeen muokattavuus ei yleensä riitä, myös taulukon pitää olla muokattava.)

Tässä vaiheessa käyttäjä voi klikata checkboxia taulukossa, ja `tehtyProperty`
muuttuu myös taustalla. Yksi tärkeä asia kuitenkin puuttuu: miten muutos
tallennetaan tiedostoon?

Pelkkä klikattava checkbox ei automaagisesti kutsu `tallenna()`-metodia.
Checkbox muuttaa datan arvoa, mutta tallennuslogiikka täytyy kytkeä erikseen.
Tämä tehdään lisäämällä kuuntelija `tehtyProperty`:n.

## Tallennus propertyn muutoksesta

Yksi ratkaisu olisi sellainen, että kytkisimme `Tehtava`-olion `tehtyProperty`:n
muutokseen kuuntelijan, joka kutsuu tallennusta.

```java,ignore
tehtyProperty().addListener((obs, vanhaArvo, uusiArvo) -> tallenna());
```

Tämä tarkoittaa, että aina kun `tehtyProperty` muuttuu (esimerkiksi checkboxia
klikataan), tallennus tapahtuu automaattisesti. Tämä olisi sinänsä kätevää,
mutta pieneksi ongelmaksi muodostuu, että Jackson-kirjaston kautta ladatut
`Tehtava`-oliot eivät tätä kuuntelijaa saa. Jackson-nimittäin luo
`Tehtava`-olion suoraan konstruktorilla, eikä se käytä setter-metodeja, joissa
kuuntelija voisi olla. Jos nyt muutamme UI:ssa `tehtavat.json`-tiedostosta
ladatun tehtävän tilaa, tallennus ei tapahdu, koska kuuntelija ei ole koskaan
lisätty.

Voisimme kyllä lisätä kuuntelijan erikseen jokaiselle `Tehtava`-oliolle
`initialize()`-metodissa silmukassa &nbsp; tämä olisi ihan toimiva ratkaisu.
Katsoimme saman tapaista esimerkkiä
[osan 8.1 alussa](./01-malli-ja-observable-rajapinta.md#ensimmainen-esimerkki).

```java,ignore
public void initialize(...) {
    // ...
    tehtavat.addListener((ListChangeListener<String>) change -> {
        while (change.next()) {
            if (change.wasAdded()) {
                for (Tehtava t : change.getAddedSubList()) {
                    t.tehtyProperty().addListener((obs, vanhaArvo, uusiArvo) -> tallenna());
                }
            }
        }
    });
}
```

Tähän on kuitenkin toinenkin, aavistuksen elegantimpi ratkaisu. Muistamme, että
`ObservableList` osaa ilmoittaa, kun sen sisältö muuttuu. Sille voidaan
kuitenkin antaa niin sanottu _ekstraktori_ (extractor), joka kertoo listalle,
mitä kunkin olion propertyjä seurataan.

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

_Aina kun tehtävän tila muuttuu, tallenna._

Tämä on databinding- ja property-ajattelun suuri etu: muutokset havaitaan
datatasolla, ei vain yksittäisen käyttöliittymätoiminnon kautta.

## Tehdyt tehtävät taulukon loppuun

`TableView` tukee lajittelua, mutta tehtyjen tehtävien siirtäminen taulukon
loppuun kannattaa toteuttaa tietoisesti määritellyllä lajittelulla. Yksi hyvä
tapa on käyttää `SortedList`-kokoelmaa, joka käärii alkuperäisen
`ObservableList<Tehtava>`-listan.

Ajatus on tämä

- varsinainen data on edelleen ObservableList<Tehtava>-listassa
- taulukolle annetaan näkyväksi dataksi SortedList<Tehtava>
- lajittelukomparaattori määrittää, että tekemättömät tulevat ennen tehtyjä

```java,ignore
SortedList<Tehtava> lajitellut = new SortedList<>(tehtavat,
        Comparator.comparing(Tehtava::isTehty)); // false ennen true

tehtavaTaulu.setItems(lajitellut);
```

Koska `false` (tekemätön) tulee ennen `true` (tehty), tekemättömät tehtävät
näkyvät taulukossa ensin ja tehdyt lopussa.

## Poisto valitusta rivistä

Nyt kun meillä on taulukko, voimme käyttää sitä poistamaan valittuja tehtäviä.
Ensin meidän on luotava käyttöliittymään painike poistamista varten, esimerkiksi
painike, jonka teksinä on "Poista valittu". Sido painike FXML-ohjaimeen (esim.
`onAction="#poistaValittu"`).

Jotta poisto toimii oikein, käyttöliittymän on ensin tiedettävä, mikä rivi
taulukosta on valittuna. `TableView` pitää kirjaa valitusta rivistä omassa
`SelectionModel`issaan. Voimme saada valitun `Tehtava`-olion sitä kautta.

Lisää ohjaimeen seuraava metodi:

```java
@FXML
private void poistaValittu() {
    // 1. Hae valittu tehtävä taulukon valintamallista
    Tehtava valittuTehtava = tehtavaTaulu.getSelectionModel().getSelectedItem();

    // 2. Jos mitään ei ole valittu, ei tehdä mitään
    if (valittuTehtava == null) {
        return;
    }

    // 3. Poistetaan tehtävä mallilistasta
    tehtavat.remove(valittuTehtava);
    
    // 4. Tallennetaan muutos
    tallenna();
}
```

Tämä metodi huolehtii hienosti siitä, että oikea tehtävä poistetaan taustalla
olevasta listasta, ja omdatabindingin ansiosta `TableView` päivittyy jälleen
kerran automaattisesti ilman että taulukkoa täytyy käsin virkistää!

## Tehtävät

<task>
  <task-title>Tehtävä 8.3: TODO-ohjelma, vaihe 9. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-3-todo-9/handout.md}}

</handout>
</task>
