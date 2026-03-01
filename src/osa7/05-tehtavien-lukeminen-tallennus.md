# Tehtävien lukeminen ja kirjoittaminen tiedostoon

Sovelluksemme alkaa olla lähellä valmis toiminnallisesti.
Toteutetaan vielä kaksi viimeistä toiminnallisuutta:

* Tehtävät tallennetaan tiedostoon, jotta ne säilyvät sovelluksen sulkemisen jälkeen
* Tehtävät haetaan tiedostosta sovelluksen käynnistyessä

[Osassa 6.5](../osa6/05-tiedostojen-kasittely.md) opimme, miten olioita voi
tallentaa tiedostoihin käyttäen JSON-tiedostomuotoa.
Suunnitellaan hieman tiedostomuotoa. Tällä hetkellä yksittäinen tehtävä
voitaisiin mallintaa kahdella attribuutilla: tehtävän *teksti* merkkijonona sekä
tieto, onko *tehtävä tehty* boolean-arvona.
Toisin sanoen, yksittäistä tehtävää voidaan mallintaa JSON-oliona:

```json
{
    "teksti": "Opiskele ohjelmointia",
    "tehty": true
}
```

Koska tehtäviä on monta, tallennetaan kaikki tehtävät yhteen listaan,
jolloin JSON-tiedoston muoto olisi seuraavanlainen:

```json
[
    {
        "teksti": "Opiskele ohjelmointia",
        "tehty": true
    },
    {
        "teksti": "Mene kouluun",
        "tehty": false
    }
]
```

## Tallentamisen valmistelu

Lisää alkuun riippuvuus Jackson-kirjastoon [osan
6.5](../osa6/05-tiedostojen-kasittely.md#jackson) ohjeen mukaisesti. 

Teemme seuraavaksi luokan `Tehtava`, joka mallintaa yllä olevaa yksittäistä
tehtävää. Lisäämme luokkaan attribuutit `teksti` ja `tehty` sekä tarvittavat
saantimetodit. Teemme lisäksi rakentajan, joka asettaa attribuuttien arvot:

```java,ignore
public class Tehtava {
    @SuppressWarnings("FieldMayBeFinal")
    private String teksti;
    @SuppressWarnings("FieldMayBeFinal")
    private boolean tehty;

    @SuppressWarnings("unused")
    public Tehtava() { /* Jätä tyhjäksi tai tee oletustoteutus */ }

    public Tehtava(String teksti, boolean tehty) { /* Lisää toteutus */ }

    public boolean getTehty() { /* Lisää toteutus */ }

    public String getTeksti() { /* Lisää toteutus */ }
}
```

Lisää järkevä toteutus itse. Jätämme `set`-asetusmetodit toistaiseksi
lisäämättä, koska käytämme luokkaa toistaiseksi vain tehtävien lataamiseen ja
tallentamiseen. Emme kuitenkaan merkitse attribuutteja `final`-määreellä, jotta
Jackson-kirjasto osaa asettaa arvoja attribuutteihin. Lisäämme vielä
oletusmuodostajan, jota Jackson käyttää olioiden alustamiseen.

<details><summary><i class="bi bi-stars jyu-gold"></i>Bonus: Tehtävä on tietue </summary>

Jos luokan attribuutteja ei ole tarkoitettu muokattavaksi (eli
kaikki attribuutit ovat `final`), luokka voidaan kirjoittaa tiiviimmässä muodossa
käyttäen Javan tietuesyntaksia:

```java
record Tehtava(String teksti, boolean tehty) {}
```

Tietuesyntaksia käydään tarkemmin läpi [luvussa
6.5](../osa6/05-tiedostojen-kasittely.md#record-luokka-jsonin-mallintamiseen).

Materiaalin seuraavassa osassa tehtäväolioita käytetään suoraan
käyttöliittymässä, jolloin lisäämme tarvittavat `set`-asetusmetodit. 
Tästä syystä toteutamme tehtävät tavallisena luokkana.

</details>

## Tehtävien tallentaminen

Aloitetaan tehtävien tallentamisella. Aivan aluksi meidän pitäisi saada
tuotettua lista tehtävistä `Tehtava`-olioina. Tällä hetkellä mallinnamme
tehtävät suoraan `CheckBox`-komponentilla. Niinpä meidän täytyy muuntaa
`VBox`-säiliössä olevat valintaruudut listaksi tehtävistä. Listojen muuntaminen
onnistuu helposti muun muassa striimeillä (ks. [luku
6.2](../osa6/02-kokoelmien-kasittely-stream-api.md)). Lisätään
`lisaaTehtava`-metodin loppuun koodi, joka hakee alkuun kaikki tekemättömät
tehtävät:

```java,ignore
void lisaaTehtava() {
    //...metodin alku piilotettu
//-    String teksti = uusiTehtavaNimi.getText();
//-    if (teksti == null || teksti.isBlank()) {
//-        uusiTehtavaNimi.requestFocus();
//-        return;
//-    }
//-    teksti = teksti.trim();
//-    CheckBox tehtava = new CheckBox(teksti);
//-    tehtava.setOnAction(event -> {
//-        if (tehtava.isSelected()) {
//-            tekemattomat.getChildren().remove(tehtava);
//-            tehdyt.getChildren().add(tehtava);
//-        } else {
//-            tehdyt.getChildren().remove(tehtava);
//-            tekemattomat.getChildren().add(tehtava);
//-        }
//-    });
//-    tekemattomat.getChildren().add(tehtava);
//-    uusiTehtavaNimi.clear();
//-    uusiTehtavaNimi.requestFocus();

    List<Tehtava> tekemattomatList = tekemattomat.getChildren().stream()
            .map(n -> (CheckBox) n)
            .map(cb -> new Tehtava(cb.getText(), cb.isSelected()))
            .toList();
}
```

Käytämme tässä striimiä, joka koostuu kahdesta
`map`-muunnoksesta ja `toList()`-kerääjästä.
Huomaa, että `VBox`-säiliön lapsikomponentit ovat tyyppiä `Node` &ndash; JavaFX:ssä kaikki
visuaaliset komponentit, myös `CheckBox`, periytyvät `Node`-luokasta.
Tässä tapauksessa tiedämme varmasti, että tehtyjen ja tekemättömien tehtävien
lista sisältää ainoastaan `CheckBox`-komponentteja.
Tästä syystä ensimmäinen `map`-muunnos muuntaa kaikki säiliössä olevat oliot
`CheckBox`-tyypiksi; muunnos ei tässä tapauksessa tuota virheitä.

Toinen `map`-muunnos muuntaa `CheckBox`-oliot `Tehtava`-olioiksi.
`CheckBox`-luokan `getText()`-metodi palauttaa valintaruudussa näkyvän tekstin
(ks. [JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.controls/javafx/scene/control/Labeled.html#getText()))
eli tehtävän tekstin ja `isSelected()` palauttaa valintaruudun tilan (ks. [JavaDoc](https://download.java.net/java/GA/javafx25/docs/api/javafx.controls/javafx/scene/control/CheckBox.html#setSelected(boolean))), eli onko
tehtävä tehty tai ei.
Lopuksi `toList()` kerää kaikki tehtävät listaan.

<details><summary>Tekemättömien lista perinteisellä silmukalla</summary>

Tekemättömien listan voisi toki muodostaa myös perinteisellä
silmukkarakenteella. Alla vertailun vuoksi sama koodi for-each-silmukkana.

```java,ignore
List<Tehtava> tekemattomatList = new ArrayList<>();
for (Node node : tekemattomat.getChildren()) {
    CheckBox c = (CheckBox) node;
    String tekstiC = c.getText();
    boolean tehtyC = c.isSelected();
    Tehtava tehtava = new Tehtava(tekstiC, tehtyC);
    tekemattomatList.add(tehtava);
}
```

</details>

<details><summary><i class="bi bi-stars jyu-gold"></i>Bonus: Mitä jos säiliössä on muitakin kuin CheckBox-komponentteja?</summary>

Tässä tapauksessa jätimme tyyppitarkistuksen pois, koska tiesimme, että
`VBox`-säiliöt sisältävät vain valintaruutuja. Jos sen sijaan `VBox` sisältäisi
erilaisia komponentteja, ja haluaisimme löytää vain tietyntyyppiset komponentit,
voisimme tehdä tyyppitarkistuksen. Tämä tehdään `instanceof`-operaattorilla,
jonka perään voidaan kirjoittaa muuttujan nimi (tässä `c`), johon tarkistettu
objekti sijoitetaan uuden tyypin kera:

```java,ignore
List<Tehtava> tekemattomatList = new ArrayList<>();

for (Node node : tekemattomat.getChildren()) {
    // Periaatteessa kaikki lapsikomponentit pitäisi 
    // olla CheckBox-komponentteja, mutta varmuuden vuoksi tarkistetaan 
    // tämä kuitenkin. 
    if (!(node instanceof CheckBox c)) {
        continue;
    }
    // Jos pääsemme tänne, niin node on CheckBox, 
    // ja voimme turvallisesti käyttää c-muuttujaa
    // CheckBox-tyyppisenä.

    String tekstiC = c.getText();
    boolean tehtyC = c.isSelected();
    Tehtava tehtava = new Tehtava(tekstiC, tehtyC);
    tekemattomatList.add(tehtava);
}
```

Mainittakoon, että vastaavat tyyppitarkistukset on myös mahdollista toteuttaa
striimeillä käyttäen `mapMulti`-metodia ([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html#mapMulti(java.util.function.BiConsumer))), jonka avulla voi valikoivasti poistaa
tai lisätä alkioita striimiin:

```java,ignore
tekemattomat.getChildren().stream()
            .<CheckBox>mapMulti((n, consumer) -> {
                // Tarkistetaan, onko komponentti tyyppiä CheckBox
                if (n instanceof CheckBox c) {
                    // Jos on, c-muuttuja sisältää tyyppimuunnetun komponentin
                    // consumer.accept lisää komponentin striimiin
                    consumer.accept(c);
                }
            })
            .map(cb -> new Tehtava(cb.getText(), cb.isSelected()))
            .toList();
```

</details>

<!-- Lisäksi muistamme, että meillä on kaksi eri säiliötä: yksi tekemättömille ja
yksi tehdyille tehtäville.

Palastellaan ongelma kahteen alaongelmaan: tehtävien hakeminen yhdestä säiliöstä ja
tehtävien yhdistäminen yhdeksi listaksi.
Tehdään ensiksi `MainController`-kontrolleriin apumetodi `haeTehtavat()`,
joka ottaa parametrina `VBox`-säiliön ja palauttaa siinä olevat tehtävät
`List<Tehtava>`-oliona: -->
<!-- 

```java,ignore
private List<Tehtava> haeTehtavat(VBox sailio) {
    return sailio.getChildren().stream()
            .map(n -> (CheckBox) n)
            .map(cb -> new Tehtava(cb.getText(), cb.isSelected()))
            .toList();
}
``` 

-->

Kokeillaan nyt tallentaa ainakin tekemättömiä tehtäviä tiedostoon käyttäen
Jackson-kirjastoa. Lisäämme `lisaaTehtava()`-metodin loppuun Jackson-kirjaston
`ObjectMapper`-olion ja käytämme sen `writeValue()`-metodia:

```java,ignore
private void lisaaTehtava() {
    //...metodin alku piilotettu
//-    String teksti = uusiTehtavaNimi.getText();
//-    if (teksti == null || teksti.isBlank()) {
//-        uusiTehtavaNimi.requestFocus();
//-        return;
//-    }
//-    teksti = teksti.trim();
//-    CheckBox tehtava = new CheckBox(teksti);
//-    tehtava.setOnAction(event -> {
//-        if (tehtava.isSelected()) {
//-            tekemattomat.getChildren().remove(tehtava);
//-            tehdyt.getChildren().add(tehtava);
//-        } else {
//-            tehdyt.getChildren().remove(tehtava);
//-            tekemattomat.getChildren().add(tehtava);
//-        }
//-    });
//-    tekemattomat.getChildren().add(tehtava);
//-    uusiTehtavaNimi.clear();
//-    uusiTehtavaNimi.requestFocus();

    List<Tehtava> tekemattomatList = tekemattomat.getChildren().stream()
            .map(n -> (CheckBox) n)
            .map(cb -> new Tehtava(cb.getText(), cb.isSelected()))
            .toList();
    // HIGHLIGHT_GREEN_BEGIN
    ObjectMapper mapper = new ObjectMapper();
    mapper.writeValue(Path.of("tehtavat.json"), tekemattomatList);
    // HIGHLIGHT_GREEN_END
}
```

Kokeile nyt ajaa sovellus ja lisätä pari uutta tehtävää. Joka kerta, kun lisäät
uuden tehtävän, tehtävät tallentuvat `tehtavat.json`-tiedostoon. Näet tiedoston
IDEAssa sen jälkeen, kun suljet sovelluksen.

> [!HUOMAUTUS]
> 
> Tässä välissä on hyvä lisätä `.gitignore`-tiedostoon rivi `tehtavat.json`,
> koska tuota tiedostoa ei haluta versionhallintaan. Tallennuksen jälkeen
> lisää `.gitignore`-komento Gitiin ja tee uusi commit:
>
> ```
> git add .gitignore
> ```
> ```
> git commit -m "Lisätty tehtavat.json .gitignoreen"
> ```
> 
> Jos lisäsit jo `tehtavat.json`-tiedoston versionhallintaan, poista se ensin
> komennolla `git rm --cached tehtavat.json`, tee commit, ja muuta vasta sen
> jälkeen `.gitignore`-tiedostoa.

Luonnollisesti myös tehdyt tehtävät tulee tallentaa. Jotta koodia ei tarvitse
toistaa, tehdään yllä olevasta koodista uusi metodi, `haeTehtavat(VBox vbox)`, joka palauttaa VBox-parametrin lapsikomponenttien perusteella listan
`Tehtava`-olioita. Sen jälkeen kerätään sekä tehdyt että tekemättömät tehtävät
samaan listaan:

```java,ignore
private List<Tehtava> haeTehtavat(VBox sailio) {
    return sailio.getChildren().stream()
            .map(n -> (CheckBox) n)
            .map(cb -> new Tehtava(cb.getText(), cb.isSelected()))
            .toList();
}

private void lisaaTehtava() {
    //...metodin alku piilotettu
//-    String teksti = uusiTehtavaNimi.getText();
//-    if (teksti == null || teksti.isBlank()) {
//-        uusiTehtavaNimi.requestFocus();
//-        return;
//-    }
//-    teksti = teksti.trim();
//-    CheckBox tehtava = new CheckBox(teksti);
//-    tehtava.setOnAction(event -> {
//-        if (tehtava.isSelected()) {
//-            tekemattomat.getChildren().remove(tehtava);
//-            tehdyt.getChildren().add(tehtava);
//-        } else {
//-            tehdyt.getChildren().remove(tehtava);
//-            tekemattomat.getChildren().add(tehtava);
//-        }
//-    });
//-    tekemattomat.getChildren().add(tehtava);
//-    uusiTehtavaNimi.clear();
//-    uusiTehtavaNimi.requestFocus();

    // HIGHLIGHT_RED_BEGIN
    List<Tehtava> tekemattomatList = tekemattomat.getChildren().stream()
            .map(n -> (CheckBox) n)
            .map(cb -> new Tehtava(cb.getText(), cb.isSelected()))
            .toList();
    // HIGHLIGHT_RED_END
    // HIGHLIGHT_GREEN_BEGIN
    List<Tehtava> tehtavat = new ArrayList<>();
    tehtavat.addAll(haeTehtavat(tekemattomat));
    tehtavat.addAll(haeTehtavat(tehdyt));
    // HIGHLIGHT_GREEN_END
    ObjectMapper mapper = new ObjectMapper();
    mapper.writeValue(Path.of("tehtavat.json"), tehtavat);
}
```

Kokeile ajaa sovellus ja tutki, miten `tehtavat.json`-tiedosto muuttuu.
Nyt sekä tekemättömät että tehdyt tehtävät tallentuvat aina, kun lisäät uuden tehtävän.

Huomaamme kuitenkin, että tehtävien tila ei päivity tiedostoon, kun tehtävä
merkitään tehdyksi tai tekemättömäksi. 
Tämä kyllä onnistuu, jos kirjoitetaan sama tallennuskoodi
uudestaan `CheckBox`-komponentin `setOnAction`-tapahtumankäsittelijään,
mutta koodin toistaminen ei ole hyvä ratkaisu. 

Mietitäänpä siis hetki. Tallentaminen on selkeästi oma kokonaisuutensa, joka ei
liity suoraan siihen, miten tehtävät luodaan, näytetään tai siirretään.
Refaktoroidaan tallennus siis omaksi metodiksi:

```java,ignore
private void tallenna() {
    List<Tehtava> kaikkiTehtavat = new ArrayList<>();
    kaikkiTehtavat.addAll(haeTehtavat(tekemattomat));
    kaikkiTehtavat.addAll(haeTehtavat(tehdyt));
    ObjectMapper mapper = new ObjectMapper();
    mapper.writeValue(Path.of("tehtavat.json"), kaikkiTehtavat);
}
```

Nyt voimme korvata `lisaaTehtava()`-metodin lopussa olevan koodin pelkällä
`tallenna()`-metodin kutsulla. Lisäksi voimme kutsua `tallenna()`-metodia
valintaruudun omassa `onAction`-tapahtumakäsittelijässä, jolloin tallennus
tehdään myös aina, kun jonkin valintaruudun tila muuttuu:

```java,ignore
private void lisaaTehtava() {
    // metodin alku piilotettu...
//-    String teksti = uusiTehtavaNimi.getText();
//-    if (teksti == null || teksti.isBlank()) {
//-        uusiTehtavaNimi.requestFocus();
//-        return;
//-    }
//-    teksti = teksti.trim();
    CheckBox tehtava = new CheckBox(teksti);
    tehtava.setOnAction(event -> {
        // tapahtumankäsittelijän alku piilotettu...
//-        if (tehtava.isSelected()) {
//-            tekemattomat.getChildren().remove(tehtava);
//-            tehdyt.getChildren().add(tehtava);
//-        } else {
//-            tehdyt.getChildren().remove(tehtava);
//-            tekemattomat.getChildren().add(tehtava);
//-        }
        // HIGHLIGHT_GREEN_BEGIN
        tallenna();
        // HIGHLIGHT_GREEN_END
    });
//-    tekemattomat.getChildren().add(tehtava);
//-    uusiTehtavaNimi.clear();
//-    uusiTehtavaNimi.requestFocus();
    // HIGHLIGHT_RED_BEGIN
    List<Tehtava> tehtavat = new ArrayList<>();
    tehtavat.addAll(haeTehtavat(tekemattomat));
    tehtavat.addAll(haeTehtavat(tehdyt));
    ObjectMapper mapper = new ObjectMapper();
    mapper.writeValue(Path.of("tehtavat.json"), tehtavat);
    // HIGHLIGHT_RED_END
    // HIGHLIGHT_GREEN_BEGIN
    tallenna();
    // HIGHLIGHT_GREEN_END
}
```

Kokeile sovellusta uudestaan. Nyt tehtävien lisääminen sekä tehtävän tilan
muuttaminen tallentaa tehtävät `tehtavat.json`-tiedostoon.

Huomaamme tässä vaiheessa, että `lisaaTehtava()`-metodi on myös paisunut hieman
liian isoksi.
Uuden `CheckBox`-valintaruudun luominen on selkeästi
oma kokonaisuutensa, joten se on järkevää erottaa omaksi metodiksi.
Tehdään uusi `luoCheckBox()`-metodi, joka ottaa parametrina valintaruutuun
lisättävä teksti ja joka palauttaa luodun valintaruutuolion. Siirretään metodiin
nykyinen `CheckBox`-oliota luova koodi sinne:

```java,ignore
private CheckBox luoCheckBox(String teksti) {
    CheckBox tehtava = new CheckBox(teksti);
    // metodin runko piilotettu...
//-    tehtava.setOnAction(event -> {
//-        if (tehtava.isSelected()) {
//-            tekemattomat.getChildren().remove(tehtava);
//-            tehdyt.getChildren().add(tehtava);
//-        } else {
//-            tehdyt.getChildren().remove(tehtava);
//-            tekemattomat.getChildren().add(tehtava);
//-        }
//-        tallenna();
//-    });
    return tehtava;
}

private void lisaaTehtava() {
    // metodin alku piilotettu...
//-    String teksti = uusiTehtavaNimi.getText();
//-    if (teksti == null || teksti.isBlank()) {
//-        uusiTehtavaNimi.requestFocus();
//-        return;
//-    }
//-    teksti = teksti.trim();
    // HIGHLIGHT_RED_BEGIN
    CheckBox tehtava = new CheckBox(teksti);
    tehtava.setOnAction(event -> {
        if (tehtava.isSelected()) {
            tekemattomat.getChildren().remove(tehtava);
            tehdyt.getChildren().add(tehtava);
        } else {
            tehdyt.getChildren().remove(tehtava);
            tekemattomat.getChildren().add(tehtava);
        }
        tallenna();
    });
    // HIGHLIGHT_RED_END
    // HIGHLIGHT_YELLOW_BEGIN
    tekemattomat.getChildren().add(luoCheckBox(teksti));
    // HIGHLIGHT_YELLOW_END
    // metodin loppu piilotettu...
//-    uusiTehtavaNimi.clear();
//-    uusiTehtavaNimi.requestFocus();
//-    tallenna();
}
```

## Tehtävien lataaminen
  
Nyt olemme saaneet tehtävät tallennettua, mutta ne pitäisi myös lukea ohjelman
käynnistyessä. Tehdään sitä varten saman tien metodi `lataa()`. Käytetään tiedoston
lukemiseen tapaa, jonka opimme [luvussa 6.5](../osa6/05-tiedostojen-kasittely.md#jackson), eli käytetään
`ObjectMapper`-luokan `readValue()`-metodia. Kääritään koko komeus `try-catch`-lohkon sisään, jotta mahdolliset poikkeukset saadaan kiinni:

```java,ignore
private void lataa() {
    Path path = Path.of("tehtavat.json");
    if (Files.notExists(path)) {
        return;
    }
    try {
        ObjectMapper mapper = new ObjectMapper();
        List<Tehtava> kaikkiTehtavat = mapper.readValue(path.toFile(), new TypeReference<>() {});
        kaikkiTehtavat.forEach(tehtava -> {
            CheckBox checkbox = luoCheckBox(tehtava.getTeksti());
            if (tehtava.getTehty()) {
                tehdyt.getChildren().add(checkbox);
            } else {
                tekemattomat.getChildren().add(checkbox);
            }
        });
    } catch (JacksonException je) {
        IO.println("JSONin lukeminen epäonnistui: " + je.getMessage());
    }
}
```

Toistaiseksi virheen sattuessa tulostamme vain virheen konsoliin.
Käsittelemme myöhemmässä osassa, miten virhetilanne voitaisiin ilmoittaa
käyttäjälle tarkemmin. 
Lisätään metodin kutsu `initialize()`-metodin alkuun:

```java,ignore
public void initialize(URL url, ResourceBundle resourceBundle) {
    lataa();
    // metodin loppu piilotettu...
//-    uusiTehtavaNimi.setOnAction(event -> lisaaTehtava());
//-    lisaaUusiTehtavaPainike.setOnAction(event -> lisaaTehtava());
}
```

Kokeile ajaa sovellus. Nyt tehtävät pysyvät tallessa, vaikka ohjelma
suljettaisiin ja käynnistettäisiin uudelleen:

<video src="images/todo-app-save-load-buggy.mp4" controls></video>

Huomaamme, että lukemisessa, tai oikeastaan valintaruutujen luomisessa, on pieni
ongelma. Kun ohjelma käynnistetään uudelleen, tehtyjen tehtävien listassa
valintaruudut eivät ole enää valittuna.
Tämä johtuu siitä, että `luoCheckBox()`-metodi ei ota huomioon sitä, onko tehtävä tehty vai ei.
Korjataan tämä lisäämällä metodille parametri, joka kertoo, onko valintaruutu
luomisen yhteydessä valittu tai ei:

```java,ignore
private CheckBox luoCheckBox(String teksti, boolean valittu) {
    CheckBox tehtava = new CheckBox(teksti);
    // HIGHLIGHT_GREEN_BEGIN
    tehtava.setSelected(valittu);
    // HIGHLIGHT_GREEN_END
    // metodin loppuosa piilotettu...
//-    tehtava.setOnAction(event -> {
//-        if (tehtava.isSelected()) {
//-            tekemattomat.getChildren().remove(tehtava);
//-            tehdyt.getChildren().add(tehtava);
//-        } else {
//-            tehdyt.getChildren().remove(tehtava);
//-            tekemattomat.getChildren().add(tehtava);
//-        }
//-        tallenna();
//-    });
//-    return tehtava;
}
```

Nyt voimme asettaa valintaruudun oikean "tehty/ei-tehty" -tilan latauksen yhteydessä:

```java,ignore
private void lataa() {
    // metodin alkuosa piilotettu...
//-    Path path = Path.of("tehtavat.json");
//-    if (Files.notExists(path)) {
//-        return;
//-    }
//-    try {
//-        ObjectMapper mapper = new ObjectMapper();
//-        List<Tehtava> kaikkiTehtavat = mapper.readValue(path.toFile(), new TypeReference<>() {});
        kaikkiTehtavat.forEach(tehtava -> {
            // HIGHLIGHT_YELLOW_BEGIN
            CheckBox checkbox = luoCheckBox(tehtava.getTeksti(), tehtava.getTehty());
            // HIGHLIGHT_YELLOW_END
    // metodin loppuosa piilotettu...
//-            if (tehtava.getTehty()) {
//-                tehdyt.getChildren().add(checkbox);
//-            } else {
//-                tekemattomat.getChildren().add(checkbox);
//-            }
//-        });
//-    } catch (JacksonException je) {
//-        IO.println("JSONin lukeminen epäonnistui: " + je.getMessage());
//-    }
}
```

Samalla korjaamme `lisaaTehtava()`-metodissa oleva `luoCheckBox()`-kutsu.
Koska uusi tehtävä lisätään aina tekemättömäksi, annetaan parametrin arvoksi
`false`:

```java,ignore
private void lisaaTehtava() {
    // metodin alkuosa piilotettu...
//-    String teksti = uusiTehtavaNimi.getText();
//-    if (teksti == null || teksti.isBlank()) {
//-        uusiTehtavaNimi.requestFocus();
//-        return;
//-    }
//-    teksti = teksti.trim();
    // HIGHLIGHT_YELLOW_BEGIN
    tekemattomat.getChildren().add(luoCheckBox(teksti, false));
    // HIGHLIGHT_YELLOW_END
    // metodin loppuosa piilotettu...
//-    uusiTehtavaNimi.clear();
//-    uusiTehtavaNimi.requestFocus();
//-    tallenna();
}
```

Kokeile tallentaa ja ajaa sovellus uudelleen. Nyt sovelluksen käynnistyessä
tehtyjen tehtävien valintaruudut merkataan "tehty"-tilaan oikein:

<img src="images/todo-app-save-load-works.png">

<task>
  <task-title>Tehtävä 7.5: Todo-sovellus, vaihe 5. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/7-5-todo-5/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa7/tehtava5">Tee tehtävä TIMissä</a></task-link>
</task>
