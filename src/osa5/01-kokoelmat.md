# Kokoelmat

> [!Osaamistavoitteet]
>
> - Ymmärrät, mitä kokoelma tarkoittaa ja miksi niitä käytetään ohjelmoinnissa.
> - Ymmärrät Javan kokoelmakehyksen (*Collections Framework*) perusrakenteen.
> - Tunnet Javan `Collection`-rajapinnan metodit ja osaat käyttää niitä ohjelmassa.

Ohjelmoinnin ytimessä on usein tiedon koostaminen järkeviksi kokonaisuuksiksi.
Olemme aiemmin käyttäneet taulukoita ja listoja samantyyppisten arvojen, kuten
lämpötilojen tai opiskelijoiden, tallentamiseen. Olemme myös oppineet
olio-ohjelmointia, jonka avulla voimme niputtaa yhteen dataa ja siihen liittyvää
toiminnallisuutta.

Pelkkä listaus ei kuitenkaan aina riitä. Vaikka taulukot ja listat ovat
hyödyllisiä, todellisen maailman ongelmat vaativat usein tarkempia sääntöjä
sille, miten tietoa lisätään, poistetaan tai haetaan.

Javassa termi **kokoelma** (engl. *collection*) viittaa olioon, jonka tehtävänä on
hallita joukkoa muita arvoja tai olioita. Kokoelma ei ole vain säiliö; se on
tietorakenne, joka määrittelee pelisäännöt tiedon käsittelylle. Oikean
tietorakenteen valinta on ohjelmoijalle tärkeä taito, sillä se vaikuttaa sekä
ohjelman tehokkuuteen että koodin luettavuuteen.

Alla on esimerkkejä tilanteista ja niihin soveltuvista kokoelmatyypeistä, kun
taulukko tai lista ei enää ole optimaalinen ratkaisu: 

 - **Jono (Queue)**: Kun soitat asiakaspalveluun, puhelut ohjataan jonoon. Uudet
soittajat tulevat jonon hännille, ja asiakaspalvelija poimii palveltavan aina
jonon kärjestä. Tätä "ensimmäisenä sisään, ensimmäisenä ulos" -rakennetta
kutsutaan jonoksi. Jono on optimoitu tällä tavalla tapahtuviin lisäyksiin ja
poistoihin, toisin kuin tavallinen lista. Vastaavasti *pino* (engl. *stack*)
toimii päinvastoin: viimeisenä lisätty alkio poistetaan ensimmäisenä (kuten
pinossa lautasia). 

 - **Joukko (Set)**: Discord-palvelussa tai puhelinmuistiossa samaa henkilöä ei ole
järkevää lisätä ystäväksi kahta kertaa. Rakennetta, joka huolehtii siitä, että
jokainen alkio esiintyy siellä vain kerran (uniikit arvot), kutsutaan joukoksi.

 - **Hakurakenne (Map)**: Opintotietojärjestelmässä jokaista opiskelijanumeroa vastaa
tietty arvosana. Tässä ei ole kyse vain listasta, vaan *avaimista*
(opiskelijanumero) ja niihin liittyvistä *arvoista* (arvosana). Rakennetta, jossa
tietoa haetaan yksilöllisen avaimen perusteella, kutsutaan hakurakenteeksi tai
assosiaatiotaulukoksi.

Voisimme periaatteessa toteuttaa nämä kaikki logiikat käyttämällä tavallisia
listoja ja kirjoittamalla paljon ylimääräistä koodia (if-lauseita tarkistamaan
duplikaatteja tai silmukoita etsimään tietoa). Javan kokoelmat tarjoavat kuitenkin valmiit, optimoidut ja selkeät työkalut näihin tarpeisiin.

## Kokoelmakehys (Java Collections Framework)

Java tarjoaa valtavan joukon valmiita kokoelmia sekä rajapintoja uusien kokoelmien
toteuttamiseksi osana [Javan
kokoelmakehystä](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/doc-files/coll-overview.html). 

Javan kokoelmaviitekehys perustuu kahteen pääosaan: 

- *kokoelmarajapintoihin*, jotka määrittävät, mitä toimintoja kokoelmalla voi
  tehdä (esim. `List`, `Set`), sekä
- *konkreettisiin toteutusluokkiin*, jotka toteuttavat rajapinnan tai 
  rajapinnat jollakin tavalla (esim. `ArrayList`, `HashSet`, `HashMap`).

Esimerkiksi `List` on kokoelmarajapinta, joka määrittää listalle kuuluvia
metodeja, mutta ei sitä, miten ne varsinaisesti toteutetaan. Puolestaan
`ArrayList` on eräs luokka, joka toteuttaa `List`-rajapinnan käyttämällä
taulukkoja. Muita valmiita listan toteutuksia käsitellään [osassa 5.2](02-listarakenteet.md).

Javan kokoelmakehyksen oleellisin rajapinta on [`Collection`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Collection.html),
joka on yleinen, korkean tason rajapinta. `List`-rajapinta periytyy 
`Collection`-rajapinnasta, joten esimerkiksi edellä mainittu `ArrayList` voidaan 
sijoittaa `Collection`-tyyppiseen muuttujaan:

```java
//-void main() {
Collection<String> marjat = new ArrayList<>(
  List.of("mansikka", "mustikka", "puolukka", "lakka")
);

IO.println(marjat);
//-}
```

`Collection` ei tee oletuksia sen sisältämien alkioiden järjestyksestä tai
sisällöstä. Varsin lukuisa joukko Javan valmiita kokoelmia toteuttavat
`Collection`-rajapinnan. Tutustumme seuraavaksi mitä `Collection`-rajapinnan
toteuttavalla kokoelmalla voi tehdä.

## Lisääminen ja poistaminen

Alkioita lisätään `add`-metodilla ja poistetaan `remove`-metodilla. Molemmat
palauttavat `true`, jos kokoelma muuttui.

```java
//-void main() {
Collection<String> marjat = new ArrayList<>(
  List.of("mansikka", "mustikka", "puolukka", "lakka")
);

marjat.add("kirsikka");
IO.println(marjat);

marjat.remove("mansikka");
IO.println(marjat);
//-}
```

Kaikissa kokoelmissa lisäys ei aina onnistu. Esimerkiksi `Set`-toteutuksessa
samaa alkiota ei voi olla kahta kertaa, joten `add` voi palauttaa `false`.
`remove` puolestaan poistaa yhden `equals`-metodin perusteella löytyvän alkion
ja palauttaa `false`, jos alkiota ei löytynyt.

`Collection`-rajapinta ei tunne indeksien käsitettä. Siksi `remove` poistaa
alkion arvon perusteella, eikä esimerkiksi "kolmatta alkiota". Jos haluat
lisätä tai poistaa indeksin perusteella, tarvitset `List`-rajapinnan.

Yksittäisen alkion poistamisen lisäksi koko kokoelman voi tyhjentää 
`clear`-metodilla.

```java
//-void main() {
Collection<String> marjat = new ArrayList<>(
  List.of("mansikka", "mustikka", "puolukka", "lakka")
);

marjat.clear();
IO.println(marjat);
//-}
```

## Tietyn alkion löytyminen kokoelmasta

`Collection`-rajapinta määrittelee myös `contains`-metodin, jolla voi tarkistaa,
löytyykö kokoelmasta jokin alkio. Tarkistus perustuu `equals`-metodiin, joten
omien olioiden kanssa `equals` tulee toteuttaa järkevästi &ndash; palaamme tähän [osassa 5.2](02-listarakenteet.md).

```java
//-void main() {
Collection<String> marjat = new ArrayList<>(
  List.of("mustikka", "puolukka", "lakka", "kirsikka")
);

IO.println("Löytyykö mustikka: " + marjat.contains("mustikka"));

// Mansikka poistettiin yllä, eli ei löydy
IO.println("Löytyykö mansikka: " + marjat.contains("mansikka"));
//-}
```

## Alkioiden määrä ja tyhjyys

`Collection`-rajapinta määrittelee myös `size`- ja `isEmpty`-metodit, joilla voi
selvittää, kuinka monta alkiota kokoelmassa on ja onko kokoelma tyhjä. 
`isEmpty` on usein selkeämpi tapa ilmaista, että kiinnostaa vain tyhjyys.

```java
//-void main() {
Collection<String> marjat = new ArrayList<>(
  List.of("mustikka", "puolukka", "lakka", "kirsikka")
);

IO.println("Marjoja on: " + marjat.size());
IO.println("Onko marjakokoelma tyhjä: " + marjat.isEmpty());  
//-}
```

## Alkioiden läpikäynti

`Collection`-rajapinta perii `Iterable`-rajapinnan, joten kokoelman alkioita voi
käydä läpi `for each`-silmukalla.

```java
//-void main() {
Collection<String> marjat = new ArrayList<>(
  List.of("mustikka", "puolukka", "lakka", "kirsikka")
);

for (String marja : marjat) {
    IO.println("Marja: " + marja);
}
//-}
```

`Collection`-rajapinta ei tee oletuksia alkioiden järjestyksestä. Tämän vuoksi
läpikäynti ei perustu indekseihin, ja järjestys riippuu aina
konkreettisesta kokoelmasta. `ArrayList` säilyttää lisäysjärjestyksen, kun taas
`HashSet` ei takaa mitään järjestystä.

Sivuhuomautuksena mainittakoon, että `Collection` todellakin *perii*
`Iterable`-rajapinnan. Emme käsitelleet rajapinnan perintää aiemmin, mutta idea
toimii rajapinnoissa samalla tavalla kuin luokissa: kaikki
`Collection`-toteutukset tarjoavat myös `Iterable`-rajapinnan vaatimukset. 
