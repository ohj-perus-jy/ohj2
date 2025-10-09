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
    - ❓Ongelma: Miten harkka tarkastetaan? Aiemmin 7 tarkastuspistettä, nyt vähemmän?

Lisäideoita arvosanan antamiseen, en ole varma voiko näitä käyttää:

 * Tentti, johon voi osallistua, jos on palauttanut vähintään 40% viikkotehtävistä
 * Jos tekee 12 * 4 = 48 viikkotehtävää ja harkan, saa automaattisesti arvosanan 1
 * Jos tekee 12 * 8 = 96 viikkotehtävää ja harkan, saa automaattisesti arvosanan 5

## Viikko 1

Kerrataan lyhyesti Ohjelmointi 1 -asioita. 

Tutkitaan miten *data ja funktiot* (Ohj1) muuttuvat *olioiksi*, joilla on *tila* ja *metodeja* (Ohj2).

<details><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

 * Perusohjelman rakenne, muuttujat, tietotyypit, operaattorit, if-lause, while-silmukka, for-silmukka, taulukot, aliohjelmat. Näistä 2-3 tehtävää..
 * Tallennetaan tietoa muuttujiin, tehdään aliohjelmia jotka muuttavat näitä (parametrien ja paluuarvojen kautta) esim. oma nimi ja pankkitilin saldo
 * Sitten koodataan pieni ohjelma, jossa on luokka, olio, attribuutit, jotka tekevät saman asian (pankkitili, jolla on nimi ja saldo, ja metodit talleta ja nosta)
 * Ero funktioiden ja metodien välillä.

</details>

<details><summary>Esimerkkejä</summary>


Data ja funktiot (Ohj1)

```java
String nimi = "Matti Meikäläinen";
double saldo = 100.0;
double talleta(double maara) { saldo = saldo + maara; return saldo; }
double nosta(double maara) { saldo = saldo - maara; return saldo; }
// ...
saldo = talleta(50.0);
saldo = nosta(20.0);
System.out.println("Hei " + nimi + ", tilillä on " + saldo + " euroa.");
```

Olio, jolla on tila (attribuutit) ja metodeja (Ohj2)

```java
class Pankkitili {
  String nimi; double saldo;
  Pankkitili(String nimi, double alkusaldo) {
    this.nimi = nimi; this.saldo = alkusaldo;
  }
  double talleta(double maara) { saldo = saldo + maara; return saldo; }
  double nosta(double maara) { saldo = saldo - maara; return saldo; }
  // ...
}

Pankkitili tili = new Pankkitili("Matti Meikäläinen", 100.0);
tili.talleta(50.0); tili.nosta(20.0);
System.out.println("Hei " + tili.nimi + ", tilillä on " + tili.saldo + " euroa.");
```

</details>

<details class="todo"><summary>Tehtäviä (TODO)</summary>

 * TODO

</details>

## Viikko 2

Kapselointi, representaation piilottaminen, konstruktorit, yhtäsuuruus

<details><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

 * Luokka ja olio
 * Konstruktori, metodi, attribuutti
 * this, get, set
 * public-, private
 * Kapselointi: Olion tila on yksityinen, sitä voi muuttaa vain metodien kautta. 
 * Representaation piilottaminen: Kutsuja ei tiedä (eikä voi riippua siitä) miten olion tila on toteutettu. Toteutustaa voi muuttaa ilman että kutsujan tarvitsee muuttaa koodiaan.
 * Vahvat invariantit (asia jonka pitää aina olla totta, esim. tilin saldo ei voi olla negatiivinen, ikä ei voi olla negatiivinen, jne.)
    - Koska viikolla 2 ei vielä ole poikkeuksia, niin invariantin tarkastaminen voi tapahtua esimerkiksi tulosteessa (esim. nostaTililtä-metodissa tarkistetaan että saldo ei mene negatiiviseksi, ja jos menee, niin palautetaan alkuperäinen saldo; jos iban-muodossa on virhe, niin asetetaan tilin saldo nollaksi ja tulostetaan varoitus). Poikkeuksista lisää myöhemmin.

</details>

<details><summary>Esimerkkejä</summary>

```java
class Pankkitili {
  // attribuutit ...

  // konstruktori(t) ...

  public double talleta(double maara) { 
    if (maara > 0) saldo = saldo + maara;  // ei vielä poikkeuksia
    return saldo; 
  }
  public double nosta(double maara) { 
    if (maara > 0 && saldo >= maara) saldo = saldo - maara;  // ei vielä poikkeuksia
    return saldo;
}
```

</details>

<details><summary>Tehtäviä</summary>

 * Yhtäsuuruus, equals...
 * Pankkitili
 * Playlist (ei vielä kokoelma-ominaisuuksia List<String> lisäksi): tee luokka Playlist, jolla on metodit lisäämiselle, poistamiselle, seuraavan kappaleen hakemiselle, kappaleiden määrän kysymiselle, ...
 * Auto, jolla on attribuutit merkki, malli, vuosimalli, ajettu matka, polttoainetankin koko, polttoaineen määrä tankissa. Metodit tankkaa, aja, kerro tiedot autosta.
 * ...

</details>

## Viikko 3

Staattinen attribuutti ja metodi. Ylikirjoitus, `@Override`, final.

<details ><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

Toteutetaan olioiden yhteistyö. Pienessä olioverkossa, oliot välittävät riippuvuudet toisilleen konstruktorissa. Pidetään kytkentä löyhänä, eli olioiden välinen riippuvuus on vain rajapinnan (metodien) varassa, ei sisäisen toteutuksen varassa.

Tämä on askel ennen perintää ja rajapintoja. 

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

<details><summary>Tehtäviä (TODO)</summary>

  * TODO

</details>

## Viikko 4

List, ArrayList, Set, HashSet, Map, HashMap, geneerisyys `<T>`, `<K, V>`, equals, hashCode

<details><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

 * Kokoelmat: List, Set, Map. Oikean kokoelman valinta käyttötarkoituksen mukaan.
   - List: järjestys, duplikaatit sallittu
   - Set: järjestys ei ole tärkeä, duplikaatit eivät ole sallittuja
   - Map: avain-arvo-parit
   - ArrayList, HashSet, HashMap
   - for-each-silmukka
   - Collections-luokka (sort, reverse, ...)
 * Geneerisyyden perusteet, tyyppiparametrit, timanttioperaattori
   - Käytetään geneerisiä kokoelmia tyyppiturvallisen koodin kirjoittamiseen
   - `List<String> nimet = new ArrayList<String>();`
   - `Map<String, Integer> sanakirja = new HashMap<String, Integer>();`
   - `List<Tilaus> tilaukset = new ArrayList<Tilaus>();`
 * Perustellaan yhtäsuuruus (equals-metodi) Set- ja Map-kokoelmien yhteydessä
 * Lyhyesti käydään läpi vaikutukset suorituskykyyn: ArrayList, HashMap
   - ArrayList on nopea, jos indeksi tiedetään
   - HashMap on nopea, jos avain tiedetään
   - List ja Set ovat hitaita, jos etsitään arvoa (koska joudutaan käymään läpi kokoelma alusta loppuun)
 * Stream-rajapinta (osa 1): map, filter, reduce; painotus kuitenkin silmukoissa edelleen
 * Viite- ja arvoparametrit, immutability

</details>

<details><summary>Esimerkkejä: TODO</summary>

 * TODO

</details>

<details><summary>Tehtäviä</summary>

 * Kirjoita funktio, joka palauttaa sanakohtaiset esiintymämäärät annetusta tekstistä Map<String,Integer>-rakenteena. Testaa vähintään: tyhjä syöte, yksi sana, useita samoja sanoja, sekalainen kirjainkoko. Sanojen vertailu on kirjainkoolla riippumatonta (esim. “Ada” == “ada”).
 * Kirjoita funktio, joka saa listan käyttäjätunnuksia (List<String>) ja palauttaa listan niistä tunnuksista, jotka esiintyvät uudelleen (duplikaatit) siinä järjestyksessä, jossa ne toisena kertana ilmestyvät. Käytä HashSet-rakennetta duplikaattien havaitsemiseen.
 * ...

</details>

## Viikko 5

Perintä, rajapinta. Polymorfismi, dynaaminen sidonta, ylikirjoitus, Liskovin korvausperiaate. Abstrakti luokka ja abstrakti metodi

<details closed><summary>Asiasisältö ja tavoitteet</summary>

  * Käytetään perintää ja rajapintoja olioiden yhteistyössä
  * instanceof, tyyppimuunnos (*cast*)
  * Ymmärtää rajapinnan (interface) rooli ja käyttää sitä vaihtokohdissa (strategiat, palvelut).
  * Abstrakti luokka: Luokka, josta ei tehdä instansseja, mutta joka voi sisältää toteutettua koodia. Abstrakti luokka määrittelee rajapinnan (abstraktit metodit) ja tarjoaa osan toteutuksesta. Aliluokat täydentävät toteutuksen.
  * Rajapinta: Määrittelee vain metodien nimet ja parametrit, ei toteutusta. Luokka voi toteuttaa useita rajapintoja, mutta vain yhden luokan (Java ei tue moniperintää). Rajapinnat sopivat hyvin "sopimuksiksi" olioiden välille.
  * Ero abstraktin luokan ja rajapinnan välillä
  * Tunnistaa milloin perintää kannattaa käyttää, ja milloin koostaminen on parempi vaihtoehto.
  * Tunnistaa polymorfismin merkitys olioiden yhteistyössä. Olio, joka käyttää ylätason tyyppiä (rajapinta, abstrakti luokka) voi toimia erilaisten aliluokkien kanssa.
  * Ylikirjoitus, `@Override`, final
  * Liskovin korvausperiaate: Aliluokan olio voidaan aina käyttää siellä missä yläluokan olio on sallittu.
  * Dynaaminen sidonta: Kutsuttava metodi päätetään ajon aikana olion todellisen tyypin perusteella, ei muuttujan tyypin perusteella.
  * Testaaminen rajapintaa vasten, ei toteutusta vasten. Esimerkki:
 * "Moniperintä" rajapintojen avulla
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

## Viikko 6

Streamit (osa 2), lambda-lausekkeet, funktioparametrit (?), Optional.

Poikkeukset (checked, unchecked), try-catch, finally, heittäminen (throw, throws). Tiedosto-I/O (teksti, CSV). Yksinkertainen JSON-käsittely. Mahdollisesti GUI-asiaa jo tässä kohdassa. 

<details ><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

 * File, Scanner
 * PrintWriter
 * Jokin JSON-kirjasto: Gson, Jackson, org.json???
 * Stream-rajapinta ja lambda-lausekkeiden käyttö
 * Optional-luokka: isPresent, ifPresent, orElse, map, flatMap

</details>

<details><summary>Esimerkkejä: TODO</summary>

 * TODO 

</details>

<details><summary>Tehtäviä: TODO</summary>

 * TODO

</details>

## Viikko 7

Rekursio, perus- ja induktiotapaukset, rekursiivinen tietorakenne?.

Hajota ja hallitse -periaate. Pinon käyttö rekursiossa. Mahdollisesti jotakin dynaamisesta ohjelmoinnista.

<details ><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

TODO

</details>

<details class="todo"><summary>Esimerkkejä: TODO</summary>

TODO

</details>

<details><summary>Tehtäviä: TODO</summary>

TODO

</details>


## Viikko 8

 * Graafinen käyttöliittymä
 * JavaFX
 * SceneBuilder
 * Projektin rakenne
 * GitHub tai GitLab

<details ><summary>Asiasisältö ja tavoitteet hieman tarkemmin</summary>

Toteutetaan pieni ohjelma käyttäen TDD-menetelmää. Ohjelmassa on graafinen käyttöliittymä, joka on toteutettu JavaFX:llä. Ohjelman rakenne noudattaa MVC-mallia (Model-View-Controller). Maven?? Versionhallintaan käytetään Git ja GitHubia.
</details>

<details><summary>Esimerkkejä: TODO</summary>

 * TODO

</details>

## Viikko 9

Koodihaju, SOLID, MVC, johdantoa olioiden suunnittelumalleihin (design patterns) esimerkiksi observer.

## Viikko 10

Harkka 1/3. Vaatii tarkennusta (mikä osa harkasta tehdään viikolla 10, mikä myöhemmin).

## Viikko 11

Harkka 2/3. Vaatii tarkennusta (mikä osa harkasta tehdään viikolla 11, mikä myöhemmin).

## Viikko 12

Harkka 3/3. Vaatii tarkennusta (mikä osa harkasta tehdään viikolla 12; miten tarkastetaan?).