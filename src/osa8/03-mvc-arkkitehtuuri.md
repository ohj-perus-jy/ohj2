# MVC-arkkitehtuuri

Nyt kun meillä on luotuna `Tehtava`-malli propertyineen ja pystymme näyttämään
listan tehtäviä `TableView`-komponentissa, on aika pohtia koko sovelluksen
rakennetta.

Tällä hetkellä kaikki sovelluksen ohjauslogiikka, data ja tiedostokäsittely ovat
kietoutuneet `MainController`-luokkaan. Tämä tekee kontrollerista nopeasti liian
raskaan ylläpitää ja vaikean testata. 

Sovelluksen arkkitehtuuri tarkoittaa sitä, miten ohjelman eri osat ja
vastuualueet järjestetään järkeväksi kokonaisuudeksi. Hyvä arkkitehtuuri tekee
koodista helpommin ymmärrettävää, laajennettavaa ja testattavaa. Tässä
projektissa sille on tarvetta erityisesti siksi, että tehtävien käsittely,
tallennus ja käyttöliittymä eivät kasautuisi yhteen samaan luokkaan.

Eräs arkkitehtuuriratkaisu tähän sovellukseen on **MVC**
(Model-View-Controller).

MVC-arkkitehtuurissa sovellus jaetaan kolmeen osaan: malliin (Model),
näkymään (View) ja ohjaimeen (Controller). Malli huolehtii datasta ja sen
käsittelystä, näkymä näyttää käyttöliittymän ja ohjain välittää käyttäjän
toiminnot mallille sekä päivittää näkymää. Tässä projektissa MVC auttaa
selkeyttämään rakennetta niin, että `MainController` ei vastaa enää yksin
kaikesta, vaan tehtävälistan logiikka ja tallennus voidaan siirtää omaan
malliluokkaansa.

Käytännön sovelluksessa ei yleensä ole vain yhtä mallia, yhtä näkymää ja yhtä
kontrolleria. Samassa ohjelmassa voi olla useita malleja eri
datakokonaisuuksille, useita näkymiä eri ruuduille tai käyttötilanteille sekä
useita kontrollereita, jotka vastaavat omista käyttöliittymän osistaan. MVC
kuvaa siis ennen kaikkea vastuiden jakamisen periaatetta, ei sitä, että koko
sovellus pitäisi rakentaa vain yhdestä Model-, View- ja Controller-kolmikosta.

Tässä osassa jaamme sovelluksemme vastuualueisiin: käyttöliittymä, data ja
ohjauslogiikka erotetaan toisistaan. Erityisesti siirrämme datan hallinnan ja
tallennuksen kontrollerista omaan malliluokkaansa.

## Kerrosten vastuut

Katsotaan tarkemmin, mitkä ovat kunkin kerroksen vastuut ja miten kukin kerros
toteutetaan tässä projektissa.

### Näkymä (view)

- **Vastuu:** Miltä sovellus näyttää.
- **Toteutus:** FXML-tiedostot kuvaavat käyttöliittymän rakenteen (`TableView`,
  painikkeet, kentät).
- **Rajoitukset:** Ei sisällä lainkaan sovelluslogiikkaa (ei esim. tiedä miten
  tehtävät tallennetaan kovalevylle).

### Malli (model)

- **Vastuu:** Mitä dataa sovelluksessa on ja miten sitä käsitellään
  (liiketoimintalogiikka).
- **Toteutus:** Olemme jo tehneet `Tehtava`-luokan mallintamaan yksittäistä
  tehtävää. Tässä osassa luomme `Tehtavakokoelma`-luokan, joka pitää sisällään
  koko sovelluksen tilan (tehtävälistan) ja tarjoaa metodit tehtävien
  lisäämiseen, poistamiseen ja tallentamiseen. 
  <!-- Koska `Tehtava` on itsessään Jacksonin ymmärtämää muotoa (siinä on tyhjä 
  konstruktori sekä setterit ja getterit), se voidaan myös sellaisenaan tallentaa tiedostoon. -->
- **Rajoitukset:** Ei tiedä mitään JavaFX-näkymästä (`TableView`, `TextField`),
  vaan luottaa observable-rakenteisiin kertoakseen muutoksista kiinnostuneille
  osapuolille.

### Ohjain (controller)

- **Vastuu:** Toimia tulkkina näkymän ja mallin välillä.
- **Toteutus:** `MainController` reagoi käyttäjän tekemiin toimintoihin, kuten
  painikkeen painallukseen, kutsuu mallin (`Tehtavakokoelma`) metodeja, ja sitoo
  näkymän (`TableView`) kiinni mallin tarjoamaan observable-dataan.

## Yhden vastuun periaate (engl. Single Responsibility Principle)

*Yksi vastuu* on yksi ohjelmistosuunnittelun periaate, jonka mukaan jokaisella
luokalla tai ohjelman osalla pitäisi olla yksi selkeä vastuualue; yksi
pääasiallinen syy muuttua. Ajatus on, että samaan luokkaan ei tule kasata
asioita, jotka muuttuvat eri syistä. Yhden vastuun periaate on yksi [viidestä
SOLID-periaatteesta](https://en.wikipedia.org/wiki/SOLID).

"Syy muuttua" tarkoittaa tässä yhteydessä tarvetta tai vaatimusta, jonka vuoksi
luokan toteutusta joudutaan muuttamaan. 

Todo-sovelluksessamme esimerkiksi tehtävien tallentaminen tiedostoon voisi
muuttua siksi, että haluamme vaihtaa JSON-tiedoston tietokantaan. Käyttöliittymä
puolestaan voi muuttua siksi, että haluamme näyttää tehtävät eri tavalla, lisätä
uuden näkymän tai muuttaa painikkeiden toimintaa. Jos sama luokka huolehtisi
sekä tallennuksesta että käyttöliittymästä, nämä kaksi erilaista muutostarvetta
sotkeutuisivat toisiinsa.

MVC liittyy tähän siten, että se auttaa jakamaan vastuut konkreettisesti
ohjelman eri osiin, kuten yllä kuvailimme. MVC ei automaattisesti takaa
täydellistä rakennetta, mutta se tukee yhden vastuun periaatetta, koska eri
syistä muuttuvat asiat erotetaan lähtökohtaisesti eri kerroksiin.

Tässä projektissa periaate näkyy esimerkiksi näin:

- `Tehtava` ja `Tehtavakokoelma` kuuluvat malliin, koska niiden tehtävä on
  kuvata sovelluksen dataa ja siihen liittyviä sääntöjä.
- `MainController` ei tallenna tiedostoja itse, vaan delegoi sen mallille.
- FXML-näkymä ei sisällä sovelluslogiikkaa, vaan vain käyttöliittymän rakenteen.

Jos `MainController` vastaisi samaan aikaan nappien käsittelystä, syötteiden
tarkistuksesta, tehtävien tallennuksesta ja tiedoston lukemisesta, luokalla
olisi monta eri syytä muuttua. Tällöin sitä olisi vaikeampi testata, ylläpitää
ja laajentaa turvallisesti.

Voit halutessasi tutustua yhden vastuun periaatteeseen ja MVC:hen lisää näistä
linkeistä: (1) Robert C. Martin: [The Single Responsibility
Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html).
(2) Apple:
[Model-View-Controller](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/Model-View-Controller/Model-View-Controller.html)

## Esimerkkirakenne

Arkkitehtuuria selkeyttää kooditiedostojen jakaminen pakkauksiin vastuun mukaan:

```text
fi.jyu.ohj2.nimi.todo
├── model
│   ├── Prioriteetti.java
│   ├── Tehtava.java
│   └── Tehtavakokoelma.java
└── ui
    ├── Main.java
    └── MainController.java
```

Kontrolleri sijoitetaan tässä samaan `ui`-pakkaukseen näkymän kanssa, koska se on
käytännössä käyttöliittymäkerroksen osa: se reagoi näkymän tapahtumiin ja
välittää kutsut mallille, mutta ei itse hallitse dataa. Erilliselle
`controller`-pakkaukselle olisi hyvä peruste etenkin silloin, jos sovelluksessa on
useita kontrollereita, mutta tässä esimerkissä `ui`-pakkaus pitää rakenteen
yksinkertaisena.

## Tehtavakokoelma

Siirrämme nyt sovelluksen sydämen, eli tehtävälistan hallinnan ja tietojen luku-
ja tallennusoperaatiot, pois kontrollerista omaan luokkaansa. Luodaan
`model`-pakkaukseen luokka `Tehtavakokoelma`. Import-lauseet on jätetty pois
tilan säästämiseksi.

```java,ignore
package fi.jyu.ohj2.nimi.todo.model;

public class Tehtavakokoelma {
    // 1. Ekstraktori takaa, että jos tehtävän propertyt muuttuvat, lista huomaa sen
    private final ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList(
            t -> new javafx.beans.Observable[]{ // TODO: Tarvitaanko "javafx.beans."?
                t.tehtyProperty(),
                t.otsikkoProperty(),
                t.prioriteettiProperty()
            }
    );
    
    // Tiedoston tallennuspolku ja datan käsittelijä
    private final Path tallennustiedosto = Path.of("tehtavat.json");
    private final ObjectMapper mapper = new ObjectMapper();

    public Tehtavakokoelma() {
        // Asetetaan tallennuskuuntelija listalle mallin sisällä
        this.tehtavat.addListener((javafx.collections.ListChangeListener<Tehtava>) change -> {
            tallenna();
        });
    }

    // --- Ohjelman logiikkametodit ---

    public void lataa() throws IOException {
        if (Files.exists(tallennustiedosto)) {
            // Lataaminen tiedostosta Jacksonin avulla
            List<Tehtava> ladatut = mapper.readValue(tallennustiedosto.toFile(), new TypeReference<>() {});
            tehtavat.setAll(ladatut);
        }
    }

    private void tallenna() {
        try {
            // Kirjoitetaan lista JSON-muodossa tiedostoon
            mapper.writeValue(tallennustiedosto.toFile(), tehtavat);
        } catch (IOException e) {
            // Tuotantosovelluksessa heitettäisiin poikkeus eteenpäin 
            // tai kirjattaisiin lokiin. Tässä esimerkissä vain tulostetaan virhe.
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
tippaakaan koodia, joka tietäisi tekstikentistä.

## Kontrollerin uusi rooli

Päivitetään lopuksi `MainController`. Kontrollerin rooli on nyt hyvin selkeä
"virkailija" mallin ja näkymän välissä. Se ottaa kokoelmiin liittyvän logiikan
pois harteiltaan ja vain viestii käyttöliittymän ja `Tehtavakokoelman` välillä.
`Tehtavakokoelma` toimii tässä kontrollerin käyttämänä ylätason mallina: se
omistaa tehtävälistan, huolehtii sen lataamisesta ja tallentamisesta sekä
tarjoaa metodit tehtävien lisäämiseen ja poistamiseen. Se tarvittiin, jotta
tehtäviin liittyvä data ja logiikka saatiin siirrettyä pois kontrollerista omaan
luokkaansa, jolloin kontrollerin vastuuksi jäi vain käyttöliittymän ja mallin
yhdistäminen.

Vaikka tässä vaiheessa tämä refaktorointi saattaa vaikuttaa vain koodin
siirtämisestä paikasta toiseen, kysymys on enemmänkin vastuiden erottamisesta
eri luokkiin MVC-mallin mukaisesti. Kun tehtävälistan hallinta, tallennus ja
syötteiden tarkistus ovat omassa malliluokassaan, niitä voidaan kehittää ja
testata itsenäisesti ilman käyttöliittymää, ja kontrolleri pysyy
yksinkertaisempana. 

```java,ignore
package fi.jyu.ohj2.nimi.todo.ui;

public class MainController {
    @FXML private TextField uusiTehtavaNimi;
    @FXML private TableView<Tehtava> tehtavaTaulu;
    @FXML private TableColumn<Tehtava, String> otsikkoCol;
    @FXML private TableColumn<Tehtava, Prioriteetti> prioriteettiCol;
    @FXML private TableColumn<Tehtava, Boolean> tehtyCol;

    // 1. Luodaan uusi ylätason malli 
    private final Tehtavakokoelma malli = new Tehtavakokoelma();

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
  eri näkymien (esim. useat tiettyjen prioriteettien taulukot tai
  muokkausikkuna) käyttöön vaivattomasti.

## Tehtävät

<task>
  <task-title>Tehtävä 8.2: Todo-sovellus, vaihe 8. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-2-todo-8/handout.md}}

</handout>
</task>
