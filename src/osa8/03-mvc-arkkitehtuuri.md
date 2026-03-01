# MVC-arkkitehtuuri

Nyt kun meillä on luotuna `Tehtava`-malli propertyineen ja pystymme näyttämään
listan tehtäviä `TableView`-komponentissa, on aika pohtia koko sovelluksen
arkkitehtuuria.

<!-- Tällä hetkellä kaikki sovelluksen ohjauslogiikka, data ja tiedostokäsittely ovat
kietoutuneet `MainController`-luokkaan. Tämä tekee kontrollerista nopeasti liian
raskaan ylläpitää ja vaikean testata.  -->

Sovelluksen arkkitehtuuri tarkoittaa sitä, miten ohjelman eri osat ja
vastuualueet järjestetään järkeväksi kokonaisuudeksi. Hyvä arkkitehtuuri tekee
koodista helpommin ymmärrettävää, laajennettavaa ja testattavaa. Tässä
projektissa sille on tarvetta erityisesti siksi, että tehtävien käsittely,
tallennus ja käyttöliittymä eivät kasautuisi yhteen samaan luokkaan.

Arkkitehtuuria ei usein tarvitse miettiä nollasta, vaan on olemassa valmiita
yleisesti hyväksi todettua artkkitehtuuriratkaisuja.
Eräs ratkaisu sovelluksen arkkitehtuurin suunnitteluun on **MVC**
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
tiedoille, useita näkymiä eri ruuduille tai käyttötilanteille sekä
useita kontrollereita, jotka vastaavat omista käyttöliittymän osistaan. MVC
kuvaa siis ennen kaikkea vastuiden jakamisen periaatetta, ei sitä, että koko
sovellus pitäisi rakentaa vain yhdestä Model-, View- ja Controller-luokasta.

Tässä osassa tunnistamme sovelluksemme osien vastuualueet ja erotamme
loput datan hallinnan ja tallennuksen toimintoja kontrollerista omaan malliluokkaansa.

## MVC-arkkitehtuurin kerrokset ja vastuut

Katsotaan tarkemmin, mitkä ovat kunkin kerroksen eli osan vastuut MVC-arkkitehtuurissa ja
miten kukin kerros toteutetaan tässä projektissa.

### Näkymä (view)

- **Vastuu:** Miltä sovellus näyttää.
- **Toteutus Todo-sovelluksessa:** FXML-tiedostot, jotka kuvaavat käyttöliittymän rakenteen.
- **Rajoitukset:** Ei sisällä lainkaan sovelluslogiikkaa (ei esim. tiedä miten
  tehtävät tallennetaan kovalevylle).

### Malli (model)

- **Vastuu:** Mitä dataa sovelluksessa on ja miten sitä käsitellään
  (liiketoimintalogiikka).
- **Toteutus Todo-sovelluksessa:** Olemme jo tehneet `Tehtava`-luokan mallintamaan yksittäistä
  tehtävää. Tässä osassa luomme lisäksi `Tehtavakokoelma`-luokan, joka pitää sisällään
  koko sovelluksen tilan (tehtävälistan) ja tarjoaa metodit tehtävien
  lisäämiseen, poistamiseen ja tallentamiseen. 
  <!-- Koska `Tehtava` on itsessään Jacksonin ymmärtämää muotoa (siinä on tyhjä 
  konstruktori sekä setterit ja getterit), se voidaan myös sellaisenaan tallentaa tiedostoon. -->
- **Rajoitukset:** Ei tiedä mitään JavaFX-näkymästä (`TableView`, `TextField`),
  vaan luottaa observable-rakenteisiin kertoakseen muutoksista kiinnostuneille
  osapuolille.


### Ohjain (controller)

- **Vastuu:** Toimia tulkkina näkymän ja mallin välillä.
- **Toteutus Todo-sovelluksessa:** `MainController` reagoi käyttäjän tekemiin toimintoihin, kuten
  painikkeen painallukseen, kutsuu mallin (`Tehtavakokoelma`) metodeja, ja sitoo
  näkymän (`TableView`) kiinni malliin `Observable`-tietorakenteiden avulla.

## MVC kannustaa noudattamaan yhden vastuun periaatetta

*Yksi vastuu* (engl. Single Responsibility) on yksi ohjelmistosuunnittelun
periaate, jonka mukaan jokaisella
luokalla tai ohjelman osalla pitäisi olla yksi selkeä vastuualue; yksi
pääasiallinen syy muuttua. Ajatus on, että samaan luokkaan ei tule kasata
asioita, jotka muuttuvat eri syistä. Yhden vastuun periaate on yksi [viidestä
SOLID-periaatteesta](https://en.wikipedia.org/wiki/SOLID), johon palataan
tarkemmin myöhemmässä osassa.
"Syy muuttua" tarkoittaa tässä yhteydessä tarvetta tai vaatimusta, jonka vuoksi
luokan toteutusta joudutaan muuttamaan. 

Todo-sovelluksessamme esimerkiksi tehtävien tallentaminen tiedostoon voisi
muuttua siksi, että haluamme vaihtaa JSON-tiedoston tietokantaan. Käyttöliittymä
puolestaan voi muuttua siksi, että haluamme näyttää tehtävät eri tavalla,
tai vaikkapa tarjota sama sovellus komentorivi- tai verkkoversiona.
Jos sama luokka huolehtisi
sekä tallennuksesta että käyttöliittymästä, nämä kaksi erilaista muutostarvetta
sotkeutuisivat toisiinsa.

MVC-arkkitehtuuri tukee yhden vastuun periaatteen noudattamista, koska eri
syistä muuttuvat asiat erotetaan lähtökohtaisesti eri kerroksiin.
Tässä projektissa periaate näkyy esimerkiksi näin:

- `Tehtava` ja `Tehtavakokoelma` kuuluvat malliin, koska niiden tehtävä on
  kuvata sovelluksen dataa ja siihen liittyviä sääntöjä.
- `MainController` ei tallenna tiedostoja itse, vaan delegoi sen mallille.
- FXML-näkymä ei sisällä sovelluslogiikkaa, vaan vain käyttöliittymän rakenteen.

Jos `MainController` vastaisi samaan aikaan painikkeiden käsittelystä, syötteiden
tarkistuksesta, tehtävien tallennuksesta ja tiedoston lukemisesta, luokalla
olisi monta eri syytä muuttua. Tällöin sitä olisi vaikeampi testata, ylläpitää
ja laajentaa turvallisesti.

<!-- DZ: Ehkä palataan tähän osassa 9? -->
<!-- Voit halutessasi tutustua yhden vastuun periaatteeseen ja MVC:hen lisää näistä
linkeistä: (1) Robert C. Martin: [The Single Responsibility
Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html).
(2) Apple:
[Model-View-Controller](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/Model-View-Controller/Model-View-Controller.html) -->

## Sovelluksen pakkausten refaktorointi

JavaFX-sovelluksessa MVC-arkkitehtuurin mukainen jako on helpointa nähdä
projektin pakkauksista ja kansiorakenteesta.
Tällä hetkellä sovelluksemme luokat jakautuvat seuraaviin pakkauksiin:

```bob
fi.jyu.ohj2.nimi.todo
├── data
│   └── Tehtava
├── App
├── Main
└── MainController
```

Refaktoroidaan nykyisten pakkausten nimet ja jaetaan luokat uusiin pakkauksiin niin, että
MVC-arkkitehtuurin mukainen vastuunjako näkyy selkeämmin:

```text
fi.jyu.ohj2.nimi.todo
├── model
│   └── Tehtava
├── controller
│   └── MainController
├── App
└── Main
```

Aloitetaan muuttamalla nykyinen `data`-alipakkaus `model`-alipakkaukseen.
Avaa IntelliJ IDEA:n projektiselain ja klikkaa hiiren toissijaisella
painikkeella `data`-alipakkauksesta. Valitse sitten **Rename** avautuneesta
valikosta. Tämän jälkeen vaihda avautuneesta valikosta pakkauksen
`data`-loppuosa `model`-loppuosaan ja paina **Refactor**:

<video src="images/intellij-refactor-rename.mp4" controls></video>

Tee tämän jälkeen uusi alipakkaus nimeltään `controller` (ks. [osa
](../osa6/04-ulkoiset-kirjastot-ja-java-projektien-hallintatyokalut.md#pakkaukset-javassa))
ja raahaa `MainController`-luokka uuteen pakkaukseen:

<video src="images/intellij-refactor-new-package.mp4" controls></video>

Huomaa, että IDEA osaa automaattisesti refaktoroida luokkien sisällä olevia
`package`-määreitä sekä FXML-tiedostossa olevan luokkaviitteen.

## Tehtavakokoelma

Siirrämme nyt sovelluksen sydämen, eli tehtävälistan hallinnan ja tietojen luku-
ja tallennusoperaatiot, pois kontrollerista omaan luokkaansa.
Kyseinen toiminnallisuus liittyy selvästi sovelluksen dataan ja sen käsittelyyn,
joten tehtävälista ja sen hallinta kuuluu MVC-arkkitehtuurissa mallikerrokseen.

Luodaan `model`-pakkaukseen luokka `Tehtavakokoelma` ja siirretään siihen
tehtävien hallintaan kuuluvat toiminnot: `tehtava`-lista, listaan liittyvä
alustus, `lataa()`-metodi ja `tallenna()`-metodi.
Seuraamme myös kapselointiperiaatetta: teemme `tehtavat`-listasta `private`
ja temme apumetodit `getTehtavat()`. `lisaaTehtava()` sekä `poistaTehtava()`, joilla hoidetaan
tehtävien lisääminen ja poistaminen sekä kytkentä käyttöliittymään.
Samalla teemme pari pientä refaktorointia: siirrämme tallennustiedoston
sijainnin sekä `ObjectMapper`-olion kokoelman attribuutteihin, sillä kumpaakin
käytetään latauksen ja tallennuksen yhteydessä.


```java,ignore
package fi.jyu.ohj2.dezhidki.todo.model;

//-import javafx.beans.Observable;
//-import javafx.collections.FXCollections;
//-import javafx.collections.ListChangeListener;
//-import javafx.collections.ObservableList;
//-import tools.jackson.core.JacksonException;
//-import tools.jackson.core.type.TypeReference;
//-import tools.jackson.databind.ObjectMapper;
//-
//-import java.nio.file.Files;
//-import java.nio.file.Path;
//-import java.util.List;
// import-määreet piilotettu tilan säästämiseksi

public class Tehtavakokoelma {
    private final ObservableList<Tehtava> tehtavat = FXCollections.observableArrayList(
            tehtava -> new Observable[]{tehtava.tehtyProperty()}
    );

    private final Path tiedostoPolku = Path.of("tehtavat.json");
    private final ObjectMapper mapper = new ObjectMapper();

    public Tehtavakokoelma() {
        tehtavat.addListener((ListChangeListener<Tehtava>) change -> {
            tallenna();
        });
    }

    public ObservableList<Tehtava> getTehtavat() {
            return tehtavat;
    }

    public void tallenna() {
        mapper.writeValue(tiedostoPolku, tehtavat);
    }

    public void lataa() {
        if (Files.notExists(tiedostoPolku)) {
            return;
        }
        try {
            List<Tehtava> kaikkiTehtavat = mapper.readValue(tiedostoPolku, new TypeReference<>() {});
            tehtavat.addAll(kaikkiTehtavat);
        } catch (JacksonException je) {
            IO.println("JSONin lukeminen epäonnistui: " + je.getMessage());
        }
    }

    public void lisaaTehtava(String teksti) {
        if (teksti == null || teksti.isBlank()) {
            return;
        }
        teksti = teksti.trim();
        tehtavat.add(new Tehtava(teksti, false));
    }

    public void poistaTehtava(Tehtava tehtava) {
        if (tehtava == null) {
            return;
        }
        tehtavat.remove(tehtava);
    }
}
```

Huomaa, miten kaikki säännöt ("otsikko ei saa olla tyhjä", "päivitä tiedosto kun
lisätään tai ominaisuus muuttuu") asuvat nyt täällä malliluokassa!

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
package fi.jyu.ohj2.nimi.todo.controller;

//-import fi.jyu.ohj2.nimi.todo.model.Tehtava;
//-import fi.jyu.ohj2.nimi.todo.model.Tehtavakokoelma;
//-import javafx.collections.transformation.SortedList;
//-import javafx.fxml.FXML;
//-import javafx.fxml.Initializable;
//-import javafx.scene.control.Button;
//-import javafx.scene.control.TableColumn;
//-import javafx.scene.control.TableView;
//-import javafx.scene.control.TextField;
//-import javafx.scene.control.cell.CheckBoxTableCell;
//-
//-import java.net.URL;
//-import java.util.Comparator;
//-import java.util.ResourceBundle;
// import-määreet piilotettu tilan säästämiseksi

public class MainController implements Initializable {
    @FXML
    private Button lisaaUusiTehtavaPainike;

    @FXML
    private TextField uusiTehtavaNimi;

    @FXML
    private TableView<Tehtava> tehtavaTaulu;

    @FXML
    private Button poistaValittuPainike;

    // HIGHLIGHT_YELLOW_BEGIN
    private Tehtavakokoelma tehtavakokoelma = new Tehtavakokoelma();
    // HIGHLIGHT_YELLOW_END

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        // HIGHLIGHT_YELLOW_BEGIN
        SortedList<Tehtava> tehtavatLajiteltu = tehtavakokoelma.getTehtavat().sorted(Comparator.comparing(Tehtava::getTehty));
        // HIGHLIGHT_YELLOW_END
        tehtavaTaulu.setItems(tehtavatLajiteltu);
        tehtavaTaulu.setEditable(true);

        TableColumn<Tehtava, Boolean> tehtySarake = new TableColumn<>("Tehty");
        tehtySarake.setCellValueFactory(cd -> cd.getValue().tehtyProperty());
        tehtySarake.setCellFactory(CheckBoxTableCell.forTableColumn(tehtySarake));
        tehtavaTaulu.getColumns().add(tehtySarake);

        TableColumn<Tehtava, String> tekstiSarake = new TableColumn<>("Tehtävä");
        tekstiSarake.setCellValueFactory(cd -> cd.getValue().tekstiProperty());
        tehtavaTaulu.getColumns().add(tekstiSarake);

        // HIGHLIGHT_YELLOW_BEGIN
        tehtavakokoelma.lataa();
        // HIGHLIGHT_YELLOW_END
        uusiTehtavaNimi.setOnAction(event -> lisaaTehtava());
        lisaaUusiTehtavaPainike.setOnAction(event -> lisaaTehtava());
        poistaValittuPainike.setOnAction(event -> poistaValittu());
    }

    private void lisaaTehtava() {
        // HIGHLIGHT_YELLOW_BEGIN
        tehtavakokoelma.lisaaTehtava(uusiTehtavaNimi.getText());
        // HIGHLIGHT_YELLOW_END
        uusiTehtavaNimi.clear();
        uusiTehtavaNimi.requestFocus();
    }

    private void poistaValittu() {
        Tehtava valittuTehtava = tehtavaTaulu.getSelectionModel().getSelectedItem();
        // HIGHLIGHT_YELLOW_BEGIN
        tehtavakokoelma.poistaTehtava(valittuTehtava);
        // HIGHLIGHT_YELLOW_END
    }

    // HIGHLIGHT_RED_BEGIN
    private void tallenna() {
//-        ObjectMapper mapper = new ObjectMapper();
//-        mapper.writeValue(Path.of("tehtavat.json"), tehtavat);
    }

    private void lataa() {
//-        Path path = Path.of("tehtavat.json");
//-        if (Files.notExists(path)) {
//-            return;
//-        }
//-        try {
//-            ObjectMapper mapper = new ObjectMapper();
//-            List<Tehtava> kaikkiTehtavat = mapper.readValue(path.toFile(), new TypeReference<>() {});
//-            tehtavat.addAll(kaikkiTehtavat);
//-        } catch (JacksonException je) {
//-            IO.println("JSONin lukeminen epäonnistui: " + je.getMessage());
//-        }
    }
    // HIGHLIGHT_RED_END
}
```

## Tehtävät

<task>
  <task-title>Tehtävä 8.2: Todo-sovellus, vaihe 8. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-2-todo-8/handout.md}}

</handout>
</task>
