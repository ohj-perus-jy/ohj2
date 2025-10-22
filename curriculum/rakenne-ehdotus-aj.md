# Opintojakson rakenne ja tavoitteet

## OPS-tason osaamistavoitteet ja sisältö

Nykyinen muotoilu OPSissa kuuluu näin.

> Osaamistavoitteet: Oppia ymmärtämään oliopohjaisen ohjelmoinnin perusteet. Kyky tuottaa pieniä/keskikokoisia oliopohjaisia ohjelmia. Samoin tavoitteena on "testaus ensin" (TDD) ajatuksen sisäistäminen. Kyky suunnitella ja toteuttaa graafinen käyttöliittymä.
> Sisältö: Java-kieli, ohjelmansuunnittelun ja olio-ohjelmoinnin periaatteita, ohjelman testaaminen. Rekursio.

## Suoritustapa

Ehdotus, joka ei pitäisi olla ristiriidassa OPSin kanssa:  

 * Joka viikko 8 viikkotehtävää ja (ainakin) 2 extra-tehtävää
 * "Esiharkka" (tutoriaalia seuraten; tästä saa viikkotehtäväpisteitä) viikoilla 8-9
 * Varsinainen harkka viikoilla 9-12
    - ❓Ongelma: Miten harkka tarkastetaan? Aiemmin 7 tarkastuspistettä, nyt vähemmän? Voidaanko käyttää itsearviointia tai vertaisarviointia?

Lisäideoita arvosanan antamiseen, en ole varma voiko näitä käyttää:

 * Tentti, johon voi osallistua, jos on palauttanut vähintään 40% viikkotehtävistä
 * Jos tekee 12 * 4 = 48 viikkotehtävää ja harkan, saa automaattisesti arvosanan 1
 * Jos tekee 12 * 8 = 96 viikkotehtävää ja harkan, saa automaattisesti arvosanan 5

## Muutosloki

<details closed><summary>15.10.2025</summary>

Tärkeimmät muutokset viikon takaiseen versioon nähden:

 - Viikko 2: Pieni olioverkko, ei vielä perintää.
 - Viikko 3: Perintä ja rajapinnat, polymorfismi
 - Viikko 4: Abstraktit luokat, enumit, pakkaus. Tähän myös testausta mukaan. 
 - Tietorakenteet viikolta 4 viikolle 5
 - Viikolle 5 jonkin yksinkertaisen (tieto-)rakenteen tekeminen, joka toteuttaa jonkin rajapinnan. ArrayList??
 - Rekursio viikolta 7 viikolle 6
 - GUI-tutoriaali viikolta 8 viikolle 7
 - Viikolle 9 iteraattorit ja HTTP IO
 - SOLID ja design patterns viikolta 9 viikolle 10 (onko liian myöhään...)
 - Viikolle 10 koodauskäytänteitä
 - Viikolle 11 monisäikeisyyttä ja ohjelmointiparadigmoja (tässä ei mulla ollut aiemmin mitään)

</details>

## Viikko 1: Java-kielen perusteet, rakenteisen ohjelmoinnin kertaus, luokka ja olio

Java-kielen perusteet. Kerrataan lyhyesti rakenteisen ohjelmoinnin perusteet (Ohj1-kurssin pikakertaus). Käsitellään dataa funktioiden avulla (Ohj1-kurssin tapaan); askel kohti olio-ohjelmointia

Luokka ja olio, olioinstanssi. 

## Viikko 2: Olio-ohjelmoinnin perusteet

Toteutetaan olioiden yhteistyö pienessä olioverkossa. Oliot välittävät riippuvuudet toisilleen konstruktorissa. Pidetään kytkentä löyhänä, eli olioiden välinen riippuvuus on vain rajapinnan (metodien) varassa, ei sisäisen toteutuksen varassa.

(Ei vielä perintää tai rajapintoja.)

<details><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

 * Eteneminen "data+funktio"-ajatuksesta (Ohj1) kohti "tila+metodi"-ajatusta (Ohj2)  
 * Luokka ja olio
 * Konstruktori, metodi, attribuutti
 * this, get, set, kapselointi
 * public, private
 * Representaation piilottaminen: Kutsuja ei tiedä (eikä voi riippua siitä) miten olion tila on toteutettu. Toteutustaa voi muuttaa ilman että kutsujan tarvitsee muuttaa koodiaan.
 * Invariantit (tilin saldo ei voi olla negatiivinen, ikä ei voi olla negatiivinen, jne.)

</details>

<details><summary>Esimerkkejä</summary>

Olioiden yhteistyö

```java
class TilausRivi { int summa() { return määrä * yksikköhinta; } }
class Tilaus { int välisumma() { int summa=0; for (var li:items) summa+=li.summa(); return summa; } }
```

"Tell, don't ask" -periaate

```java
int välisumma = tilaus.välisumma(); // oikein

// väärin, jos tilauksen toteutus muuttuu, tämä koodi menee rikki
int välisumma = 0; for (var rivi:tilaus.getItems()) välisumma += rivi.summa(); 
```

 * Näkyvyys, protected, package

</details>

## Viikko 3: Perintä, rajapinnat, polymorfismi

Perintä, rajapinta. Polymorfismi. Staattinen attribuutti ja metodi. Ylikirjoitus, final. 

Viitevälitys, arvovälitys. Immutable-olio. 

<details closed><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

 * Käytetään perintää ja rajapintoja olioiden yhteistyössä
 * Testaaminen rajapintaa vasten, ei toteutusta vasten.
 * "Moniperintä" rajapintojen avulla

</details>

## Viikko 4: Abstraktit luokat

Abstrakti luokka ja abstrakti metodi. Koostaminen, polymorfismi (jatkuu), dynaaminen sidonta, Liskovin korvausperiaate. 

<details closed><summary>Asiasisältö ja tavoitteet</summary>

 * Abstrakti luokka: Luokka, josta ei tehdä instansseja, mutta joka voi sisältää toteutettua koodia. Abstrakti luokka määrittelee rajapinnan (abstraktit metodit) ja tarjoaa osan toteutuksesta. Aliluokat täydentävät toteutuksen.
 * Ero abstraktin luokan ja rajapinnan välillä
 * Ymmärtää rajapinnan (interface) rooli ja käyttää sitä vaihtokohdissa (strategiat, palvelut).
 * instanceof, tyyppimuunnos (*cast*)
 * Tunnistaa milloin perintää kannattaa käyttää, ja milloin koostaminen on parempi vaihtoehto.
 * Tunnistaa polymorfismin merkitys olioiden yhteistyössä. Olio, joka käyttää ylätason tyyppiä (rajapinta, abstrakti luokka) voi toimia erilaisten aliluokkien kanssa.
 * Ylikirjoitus, `@Override`, final
 * Liskovin korvausperiaate, LSP
 * Dynaaminen sidonta: Kutsuttava metodi päätetään ajon aikana olion todellisen tyypin perusteella, ei muuttujan tyypin perusteella.

</details>

<details closed><summary>Esimerkkejä</summary>

```java
// Esimerkki testaamisesta rajapintaa vasten
interface Maksutapa { void maksa(double summa); }
class Pankkikortti implements Maksutapa { void maksa(double summa) { ... } }
class Lasku implements Maksutapa { void maksa(double summa) { ... } }
void suoritaMaksu(Maksutapa m, double summa) { m.maksa(summa); }

Maksutapa m = new Pankkikortti(); suoritaMaksu(m, 100.0);
m = new Lasku(); suoritaMaksu(m, 200.0);

// Testi
class MockMaksutapa implements Maksutapa {
  double maksettuSumma = 0.0;
  void maksa(double summa) { maksettuSumma += summa; }
}
void testSuoritaMaksu() {
  MockMaksutapa m = new MockMaksutapa();
  suoritaMaksu(m, 100.0);
  assert m.maksettuSumma == 100.0;
  suoritaMaksu(m, 50.0);
  assert m.maksettuSumma == 150.0;
}

// ------

abstract class Elain { abstract void aantele(); }
class Koira extends Elain { void aantele() { System.out.println("Hau!"); } }
Elain e = new Koira(); e.aantele();
Elain e2 = new Elain(); // ! ei voi tehdä
Elain e3 = new Kissa(); e3.aantele();

interface Ajettava { void aja(); }
class Auto implements Ajettava { void aja() { System.out.println("Vroom!"); } }
Ajettava a = new Auto(); a.aja();
Ajettava a2 = new Ajettava(); // ! ei voi tehdä
Ajettava a3 = new Vene(); a3.aja();

class Tesla extends Auto implements Sähköauto, Ajettava { ... }
interface Sähköauto { void lataa(); }
interface Ajettava { void aja(); }
class Auto implements Ajettava { void aja() { System.out.println("Vroom!"); } }
Tesla t = new Tesla(); t.aja(); t.lataa();
Ajettava a = new Tesla(); a.aja(); a.lataa(); // ! ei voi tehdä
Sähköauto s = new Tesla(); s.lataa(); s.aja(); // ! ei voi tehdä
```
</details>

## Viikko 5: Tietorakenteet

Javan kokoelmat, niiden käyttö ja rajapintojen ymmärtäminen kokoelmien yhteydessä. List, ArrayList, Set, HashSet, Map, HashMap, ... (Ei välttämättä kaikkia, osa voidaan jättää maininnan tasolle.)

Geneerisyys, tyyppiparametri(t), equals, hashCode

Tehdään itse yksinkertainen kokoelma, joka toteuttaa jonkin tai joitakin rajapintoja. 

<details><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

 * Kokoelmat: List, Set, Map. Oikean kokoelman valinta käyttötarkoituksen mukaan.
   - List: järjestys, duplikaatit sallittu
   - Set: järjestys ei ole tärkeä, duplikaatit eivät ole sallittuja
   - Map: avain-arvo-parit
   - ArrayList, HashSet, HashMap
   - for-each-silmukka
   - Collections-luokka (sort, reverse, ...)
 * Geneerisyyden perusteet, tyyppiparametrit, timanttioperaattori
 * Rajapintaa vasten ohjelmointi: List, Set, Map
   - `List<String> nimet = new ArrayList<String>();`
   - `Map<String, Integer> sanakirja = new HashMap<String, Integer>();`
   - `List<Tilaus> tilaukset = new ArrayList<Tilaus>();`
 * Perustellaan yhtäsuuruus (equals-metodi) Set- ja Map-kokoelmien yhteydessä
 * Lyhyesti käydään läpi vaikutukset suorituskykyyn: ArrayList, HashMap, List, Set
 * Viite- ja arvoparametrit, immutability

</details>

## Viikko 6: Streamit, lambda-lausekkeet, rekursio, Optional, tiedosto-I/O, JSON

Stream-rajapinta, map, filter, reduce. Funktioparametrit (?), Optional (?).

Poikkeukset (checked, unchecked), try-catch, finally, heittäminen (throw, throws). Tiedosto-I/O (teksti, CSV). Yksinkertainen JSON-käsittely. Mahdollisesti GUI-asiaa jo tässä kohdassa. 

Rekursio, perus- ja induktiotapaukset, rekursiivinen tietorakenne (?). Hajota ja hallitse -periaate. Pinon käyttö rekursiossa. Mahdollisesti jotakin dynaamisesta ohjelmoinnista.

**Tämä viikko on aika täysi. Voisiko osan asioista siirtää aiemmaksi, ja osan myöhemmäksi?** 

<details closed><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

 * File, Scanner
 * PrintWriter
 * Jokin JSON-kirjasto: Gson, Jackson, org.json???
 * Stream-rajapinta ja lambda-lausekkeiden käyttö
 * Optional-luokka: isPresent, ifPresent, orElse, map, flatMap

</details>

## Viikko 7: GUI 1, harjoitustyö-tutoriaali

GUI, osa 1. JavaFX, SceneBuilder.
 
 * FXML ja SceneBuilder
 * Scene–Stage–Node
 * Layoutit: VBox, HBox, GridPane, BorderPane
 * Peruskomponentit: Label, Button, TextField, RadioButton, (TextArea, ListView, ComboBox, CheckBox, Menu, MenuItem, Alert?)
 * Properties & Bindings: Yksisuuntainen ja kaksisuuntainen sidonta
 * Layoutit: VBox, HBox, BorderPane
 * Näkymä ja sen määrittely erilliseen tiedostoon
 * ListView, ComboBox ja niiden käyttö ObservableListin kanssa
 * Layoutit (VBox, HBox, GridPane, BorderPane)
 * Tapahtumankäsittely ja lambda-lausekkeet
 
Arkkitehtuurin alkeet (MVC / MVVM) sen osalta mitä tarvitaan pienen JavaFX-sovelluksen tekemiseen. 

Projektin rakenne, Gradle tai Maven. Tarvittavat kansiot ja niiden kytkennät arkkitehtuuriin.

GUI-tutoriaalin ensimmäinen osa. 

Tutoriaali tehdään GITiin (valikoitujen) hyvien käytäntöjen mukaisesti. 

### Esimerkkejä

Laskuri ja lomake, jossa "Tallenna" aktivoituu vain validina.

Login-mock: TextField + PasswordField; "Kirjaudu" aktivoituu, kun ehdot täyttyvät.

Haku + label: hakukenttä, jonka pituus näkyy labelissa bindingilla.

## Viikko 8: GUI 2, TDD, oman harjoitustyön aloitus

GUI, osa 2. 

 * Listat, taulukot ja muunnokset: Osaa näyttää ja editoida listamuotoista dataa, käyttää ObservableList, FilteredList, SortedList, cellFactory, StringConverter.
 * Dialogit: Osaa avata modaalisia dialogeja ja käsitellä niiden paluuarvoja.

MVVM

 * Vastuiden erottelu: Model, View, ViewModel. Ei Nodeja ViewModelissa.
 * Data binding ViewModelin ja Viewn välillä. Esimerkki: TextFieldin ja ViewModelin propertyn välinen sidonta.

Yksikkötestaus JUnit5:llä. Mocking (Mockito tms.). 

Harjoitustyön suunnitelma: aihe, luokkakaavio, olioiden yhteistyö. 

### Esimerkkejä

Henkilölista-näkymä: TableView<Person> + hakukenttä (FilteredList) + rivin kaksoisklikkaus avaa muokkausdialogin ja päivittää listan, jos käyttäjä painaa Tallenna.

Lisää listaan "Lisää/Poista/Muokkaa" toiminnot: muokkaus dialogilla, lisääminen tyhjällä dialogilla, poisto vahvistus-alertilla. Tallenna lista ohjelman eliniän ajaksi (in-memory).

## Viikko 9: Iteraattorit, HTTP I/O

GUI, osa 3.

* FileChooser / DirectoryChooser: avaa/tallenna, suodattimet.
* Pieni Navigator (StackPane) tai TabPane-navigaatio.
* Virheiden käsittely UI:ssa (alertit, disable-tilat),
 
Javan iteraattorit (= Iterable, Iterator: hasNext, next, remove)

HTTP I/O: Lähinnä siitä näkökulmasta, että osataan *hakea* JSON-dataa verkosta.

Oman harjoitustyön ensimmäinen vaihe (TODO: Speksaa mitä pitää olla valmiina). 

## Viikko 10: Koodin laatu, hyvät koodauskäytänteet, johdattelua suunnittelumalleihin

Koodihaju, refaktorointi, SOLID. Johdantoa olioiden suunnittelumalleihin (design patterns) esimerkiksi *Observer*. Mahdollisesti UML:n perusteita. git branch, git merge. README, kommentit, git commit.

Harkka toinen vaihe (TODO: Speksaa mitä pitää olla valmiina). 

## Viikko 11: Monisäikeisyys, ohjelmointiparadigmat

Monisäikeisyyden perusteet, säikeiden luominen ja hallinta, ExecutorService, Future, CompletableFuture. (TODO: Jääkö pintapuoliseksi?)

Ohjelmointiparadigmojen vertailua (Samin ehdotus, mutta myöhemmin): funktionaalinen, oliopohjainen

Harkka kolmas vaihe (TODO: Speksaa mitä pitää olla valmiina). 

## Viikko 12: Oman projektin viimeistely

Harkka neljäs vaihe (TODO: Speksaa mitä pitää olla valmiina). 

## Viikko 13: Tentti

Tentti

## Ajatuksia oppimateriaalin, viikkotehtävien ja harjoitustyön suhteesta

Oppimateriaalissa näytettävät esimerkit voisivat ainakin osittain kytkeytyä toisiinsa, ts. muodostaisivat "jatkuvan tarinan". Viikkotehtävissä voitaisiin sitten soveltaa oppimateriaalissa opittuja asioita. Tällaisesta ideasta hyvänä esimerkkinä toimii Full Stack Open (blogisovellus vs. todo-sovellus); toki tuossa erona on se että päästään aika nopeastikin CRUDiin, kun meillä pitäisi lähteä ensin hiljalleen ensin C:stä, sitten R jne. Mutta silti tämä olisi motivoivampaa kuin pelkät irralliset tehtävät (joita toki tarvitaan myös).

## Mihin tarvittaisiin tuntiopettajien apuja?

 * Uuden "monisteen" kirjoittamiseen ja tarkastamiseen (heti)
 * Viikkotehtävien laatimiseen ja tarkastamiseen (heti)
 * Harjoitustyön määrittelyssä avustaminen (heti) 
 * Harjoitustyön hyväksyntäkriteerien laatiminen (viimeistään joulu-tammikuu)
 * Työkalujen käyttöönoton testaaminen ja ohjeistaminen (viimeistään marras-joulukuussa; vasta sitten kun harkka on määritelty)
 * Muiden tekemien viikkotehtävien katselmointiin ja kommentointiin (viimeistään kurssin alettua)

