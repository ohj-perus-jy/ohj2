# Muuttujat ja tietotyypit

> [!Osaamistavoitteet]
>
> - Muistat, mitä ovat muuttujat ja vakiot
> - Muistat, mitä ovat merkkijonot ja listat
> - Tunnet Javan alkeistietotyypit
> - Tunnet, miten merkkijonot, taulukot ja listat käytetään Javassa

Ohjelmat käsittelevät muistiin tallennettua tietoa. Konekielessä tietoon
viitataan numeerisilla muistiosoitteilla, mutta korkean tason kielissä, kuten
Javassa käytetään selkokielisiä nimiä. Tällaista nimeä, joka viittaa muistissa
olevaan tietoon, kutsutaan muuttujaksi (engl. *variable*). Ohjelmoijan tarvitsee
muistaa vain nimi; tietokone huolehtii tiedon todellisesta sijainnista
muistissa.

Javassa muuttuja tulee ensin *määritellä* ennen kuin sitä voi käyttää:

```java,ignore
tyyppi muuttujanNimi;
```

Muuttujan tyyppi määritellään muuttujan nimen edessä, ja se kertoo, millaista
tietoa muuttuja voi sisältää.
Muuttujan nimi voi sisältää kirjaimia ja alaviivoja. Muuttujan nimi
ei kuitenkaan voi olla Java-kielessä varattu avainsana
eikä muuttujan nimi saa alkaa numerolla.
Javassa useasta osasta koostuvat muuttujien nimet kirjoitetaan
yhteen `camelCase`-kirjoitustyylillä.

Muuttujan määrittelyn jälkeen muuttujaan voi *sijoittaa* lausekkeiden
arvoja:

```java,ignore
muuttujanNimi = lauseke;
```

Yhtäsuuruusmerkin oikealla puolella olevan
lausekkeen (engl. *expression*) arvo tallennetaan sen vasemmalla puolella
nimettyyn muuttujaan.
Jos muuttujissa oli aiemmin jotain muita arvoja, ne korvataan uusilla.

```java
//-void main() {
double korkokerroin; // Muuttujan määrittely, double = desimaalikuku
double paaoma; // Muuttujan määrittely

korkokerroin = 0.05; // Arvon sijoitus muuttujaan
paaoma = 150.0; // Arvon sijoitus muuttujaan
//- IO.println("korkokerroin = " + korkokerroin);
//- IO.println("paaoma = " + korkokerroin);
//- }
```

Muuttujaa ei voi käyttää ennen kuin siihen sijoittaa arvon ainakin kerran.
Tätä varten voi käyttää yhdistettyä määrittely- ja sijoituslausetta, joka
yhdistää muuttujan määrittelyn ja alkuarvon sijoittamisen samalle riville:

```java,ignore
double paaoma = 0.05; 
// Yllä oleva on sama kuin:
double paaoma;
paaoma = 0.05;
```

Muuttuja voi olla myös lausekkeen osana, ja siten sen arvoa voidaan käyttää
osana sijoitettavaa lauseketta. 

```java
//-void main() {
double korkokerroin = 0.05;
double paaoma = 150.0;

double paaomaKorolla = (1 + korkokerroin) * paaoma;
//- IO.println("korkokerroin = " + korkokerroin);
//- IO.println("paaoma = " + korkokerroin);
//- IO.println("paaomaKorolla = " + paaomaKorolla);
//-}
```

Ohjelmoinnissa sijoitus on *lause*, eli yksittäinen suoritettava käsky.
Esimerkiksi lausetta `double paaoma = 150.0;` voi ajatella tarkoittavan:
"tallenna luku 150.0 muistiin paikkaan, jota kutsutaan tästä eteenpäin nimellä
`paaoma`". Muuttujan arvo pysyy samana kunnes jokin toinen lause muokkaa
muuttujan arvoa.

Javan tietotyypit voidaan jakaa kahteen pääryhmään: alkeistietotyyppeihin (engl.
*primitive data types*) ja viitetietotyyppeihin (engl. *reference data types*).
Kaikki tieto tallennetaan tietokoneen muistiin binäärilukuina (nollien ja
ykkösten sarjana), ja tietotyypit eroavat toisistaan siinä, kuinka paljon
muistia ne varaavat, millaista dataa ne esittävät ja millä säännöillä dataa voi
käsitellä. Alkeistietotyypit sisältävät yksinkertaisia arvoja, kuten
kokonaislukuja ja totuusarvoja, kun taas viitetietotyypit sisältävät
monimutkaisempia rakenteita, kuten olioita, taulukoita ja merkkijonoja. 

## Alkeistietotyypit

Javassa on kahdeksan sisäänrakennettua alkeistietotyyppiä, joita 
voi karkeasti jakaa neljään kategoriaan: kokonaisluvut, liukuluvut, merkit
ja totuusarvot.

### Kokonaisluvut 

Kokonaisluvuille on olemassa neljä tyyppiä, jotka eroavat toisistaan
lukualueen ja muistinkulutuksen perusteella. Yleisimmin käytetty
kokonaislukutyyppi on `int`. 

| Tyyppi  | Koko (tavua /bittiä) | Lukualue (suuntaa antava)       |
| ------- | -------------------- | ------------------------------- |
| `byte`  | 1 tavu (8 bittiä)    | -128 ... 127                    |
| `short` | 2 tavua (16 bittiä)  | -32 768 ... 32 767              |
| `int`   | 4 tavua (32 bittiä)  | n. -2 miljardia ... 2 miljardia |
| `long`  | 8 tavua (64 bittiä)  | n. +/- 9 * 10^18                |


<details><summary><b><i class="bi bi-info-circle"></i> Huomautus:</b> Muuttujan tyyppi ei vaihdu lennosta</summary>

Useissa dynaamisissa ohjelmointikielissä, kuten Pythonissa tai JavaScriptissa,
kokonaisluvuille ei välttämättä ole suurinta arvoa: suurille luvuille varataan
joko lisää tilaa tai vähemmän merkitseviä numeroita pyöristetään.
**Tämä ei päde Javassa.** Jos laskutoimituksen tuloksena kokonaisluku ylittää 
muuttujan tyypin lukualueen, luku *vuotaa yli* (engl. overflow) ja "pyörähtää lukualueen ympäri":

```java
//-void main() {
int suuriLuku = 2000000000;
IO.println("suuriLuku = " + suuriLuku);

suuriLuku += 1000000000;
IO.println("suuriLuku = " + suuriLuku);
//-}
```

Siispä mahdollinen lukualue on otettava huomioon ohjelmaa kirjoittaessa.
Jos on mahdollisuus, että laskutoimitus ylittää tyypin lukualueen, on syytä
vaihtaa toiseen tietotyyppiin.

Javasta löytyy myös suuria lukuja käsittelevä
[`BigInteger`](https://docs.oracle.com/en/java/javase/25/docs/api//java.base/java/math/BigInteger.html)
-tyyppi, jota ei tällä opintojaksolla käsitellä.

</details>

### Liukuluvut

Desimaaliluvuille käytetään liukulukutyyppejä. Yleisin näistä on
`double`.

| Tyyppi | Koko (tavua)        | Tarkkuus                  |
| ------ | ------------------- | ------------------------- |
| float  | 4 tavua (32 bittiä) | n. 7 merkitsevää numeroa  |
| double | 8 tavua (64 bittiä) | n. 15 merkitsevää numeroa |

<details><summary><b><i class="bi bi-info-circle"></i> Huomautus:</b> Liukuluvut ovat epätarkkoja!</summary>

Java käyttää liukulujuja desimaalilukujen `double` ja `float`
esittämiseen. Liukulukuja voidaan ajatella esittävän desimaalilukujen
likiarvoja. Liukulukujen tarkka toiminta on standardoitu (IEEE 754 -standardi);
vaikka ne on tarkoitettu desimaalilukujen esittämiseen, niillä on silti joitain
mielenkiintoisia ja kenties yllättäviä eroja tavallisiin desimaalilukuihin:

```java
void main() {
    // Laskutoimitukset voivat erota desimaaliluvuista pyöristysvirheiden takia
    double pyoristysVirhe = 0.1 + 0.2;
    IO.println("pyoristysVirhe = " + pyoristysVirhe);

    // Jakaminen nollalla on määritelty eikä aiheuta virhettä
    double negatiivinenAarettomyys = -1.0 / 0.0;
    IO.println("negatiivinenAarettomyys = " + negatiivinenAarettomyys);
    double positiivinenAarettomyys = 1.0 / 0.0;
    IO.println("positiivinenAarettomyys = " + positiivinenAarettomyys);

    // Jakolasku 0/0 ei aiheuta virhettä
    double nan = 0.0 / 0.0;
    IO.println("nan = " + nan);
}
```

Liukuluvuille on siten erikseen määritelty $-\infty, \infty$ ja `NaN` =
**N**ot **A** **N**umber. Lisäksi liukulukujen väliset laskutoimitukset
voivat sisältää pieniä virheitä johtuen liukulukujen esitystavasta ja 
pyöristysvirheistä.

Hyvin tarkkoja laskuja vaativille ohjelmille löytyy myös
[`BigDecimal`](https://docs.oracle.com/en/java/javase/25/docs/api//java.base/java/math/BigDecimal.html)
-tyyppi, jota ei tällä opintojaksolla käsitellä.

</details>

### Merkit

Yksi merkki tallennetaan `char`-tyyppiseen muuttujaan, joka käyttää
2 tavua muistia.

### Totuusarvot

Totuusarvoja varten on `boolean`-tyyppi, jolla on kaksi
mahdollista arvoa: `true` (tosi) tai `false` (epätosi).


## Viitetietotyypit

Toisin kuin alkeistietotyypit, 
viitetietotyyppinen muuttuja sisältää varsinaisen tiedon sijaan vain pienen, 
kiinteän kokoisen arvon eli *viitteen* (engl. reference).
Viitteen avulla ohjelma pääsee käsiksi varsinaiseen dataan,  
jonka kokoa tai sisältöä ei välttämättä tiedetä ennen kuin ohjelma ajetaan.  

Javassa käytännössä kaikki muut tietotyypit kuin alkeistietotyypit ovat
viitetietotyyppejä. Esimerkiksi `String` on viitetietotyyppi, kuten myös kaikki
taulukot ja listat. Alkaen luvusta 2 tutustumme olio-ohjelmointiin; Javassa
kaikki oliot ovat viitetietotyypit.

Kaikkiin viitetyyppimuuttujiin on sallittua sijoittaa erikoisarvo `null`
Tämä niin sanottu *null-viite* merkitsee, että muuttuja ei sisällä viitettä
mihinkään tietoon. Yritys muokata tai lukea muuttujaa, jonka arvo on `null`,
tuottaa yleensä virheen ohjelman ajon aikana:

```java,ignore
String teksti = null;
String tekstiIsolla = teksti.toUpperCase();
IO.println(tekstiIsolla);
```
```
java.lang.NullPointerException: Cannot invoke "String.toUpperCase()" because "<local1>" is null
	at main.main(main.java:3)
```

Koska virhe tapahtuu vasta ajon aikana, Javassa on yleensä ohjelmoijan vastuulla
varmistaa, että muuttujan tai funktion parametrin arvona ei ole null-viite.
Varmistus voidaan tehdä esimerkiksi ehtorakenteella, jotka esitetään seuraavassa
alaluvussa.

<details><summary>✨ Valinnaista lisätietoa: Miksi viitetietotyyppejä on olemassa?</summary>

On useita syitä sille, miksi nämä kaksi eri kategoriaa tietotyypeille on
olemassa.

Ensimmäinen liittyy suorituskykyyn ja muistin hallintaan. Jos kaikki muuttujat
olisivat arvopohjaisia (kuten alkeistietotyypit), se aiheuttaisi valtavasti
turhaa muistin kulutusta ja hidastaisi ohjelman suorituskykyä, erityisesti
suurten tietorakenteiden kohdalla. Jos meillä olisi vaikkapa `kirja`, joka
sisältäisi 1000 sivua tekstiä, niin joka ikinen kerta kun haluamme käsitellä
`kirja`-muuttujaa, meidän pitäisi kopioida kaikki 1000 sivua muistissa. Tämä
olisi erittäin tehotonta. Sen sijaan viitetietotyypit mahdollistavat sen, että
vain viittaamme `kirja`-olioon, joka sijaitsee jossakin muualla muistissa,
ilman että tarvitsee kopioida koko kirjaa joka kerta.

Toinen syy liittyy jaettuun tilaan. Usein haluamme, että useampi ohjelman osa
muokkaa samaa tietoa. Esimerkiksi on järkevää, että `pankkitili`-olio on jaettu
useiden eri toimintojen kesken, kuten talletus, nosto ja tilin saldo.
Arvopohjaisessa maailmassa joutuisimme kopioimaan `pankkitili`-olion joka kerta,
kun tililtä halutaan nostaa rahaa, tehdä tilisiirto tai vaikkapa tarkistaa
saldo. Tämä johtaisi helposti siihen, että eri kopiot olisivat eri tilassa, mikä
saattaisi aiheuttaa virheitä.

Kolmas syy on dynaaminen koko. Viitetietotyypit mahdollistavat dynaamisesti
kasvavien ja kutistuvien tietorakenteiden, kuten linkitettyjen listojen, pinojen
ja jonoiden, luomisen. Näitä rakenteita ei voida helposti toteuttaa
arvopohjaisina, koska arvopohjaisten muuttujien koko on kiinteä käännösaikana.

Neljäs syy liittyy erityisesti olio-ohjelmointiin, ja liittyy osittain myös
kolmanteen kohtaan. Javassa viitteet mahdollistavat polymorfismin. Koska
muuttuja on vain viite, se voi osoittaa mihin tahansa, joka "näyttää" oikealta
tyypiltä. 

```java,ignore
Elain lemmikki = new Koira();
lemmikki = new Kissa();
```

Jos nämä olisivat puhtaita arvotyyppejä, `Elain`-tyyppiselle muuttujalle pitäisi
varata kiinteä määrä muistia. Jos `Kissa` sitten tarvitsisikin enemmän muistia
kuin `Elain` on varannut, koodi hajoaisi. Viitteiden avulla muuttujan koko on
aina sama (viitteen koko), riippumatta siitä kuinka valtava olio viitteen päässä
on.

</details>

## Literaalit

Literaali (engl. *literal*) tarkoittaa ohjelmakoodiin kirjoitettua kiinteää
arvoa. Eri tietotyypeillä on omat kirjoitussääntönsä literaaleille.

 * **Merkit** (`char`): Kirjoitetaan yksittäisen lainausmerkin sisään,
   esimerkiksi `'A'`,  `'*'` ja `'x'`. Erikoismerkit alkavat kenoviivalla:
   `'\n'` (rivinvaihto), `'\u03A9'` (kreikkalainen iso omega) ja `'\t'`
   (tabulaattori).
 * **Kokonaisluvut** (`byte`, `short`, `int`, `long`): Kirjoitetaan suoraan
   numerona, esimerkiksi `42`, `-7` ja `0`. `long`-luvun literaali päättyy isoon
   tai pieneen kirjaimeen `L` tai `l`, esimerkiksi `12345678901L`.
 * **Liukuluvut** (`float`, `double`): Kirjoitetaan desimaalipisteellä
   erotettuna, esimerkiksi `3.14`, `-0.001` ja `2.0`. Voidaan käyttää myös
   tieteellistä muotoa: `1.5e3` (eli 1.5 × 10³ = 1500) ja `2.0E-4` (eli 2.0 ×
   10⁻⁴ = 0.0002). Oletuksena desimaaliluvut ovat `double`-tyyppiä. Jos haluat
   luoda `float`-luvun, literaalin tulee päättyä isoon tai pieneen kirjaimeen
   `F` tai `f`, esimerkiksi `3.14f`.
 * **Totuusarvot** (`boolean`): Kirjoitetaan avainsanoina `true` ja `false`.

```java
//-void main() {
char merkki = 'A';
//-IO.println("merkki = " + merkki);

int luku = 123;
//-IO.println("luku = " + luku);
long isoLuku = 12345678901L;
//-IO.println("isoLuku = " + isoLuku);

double liukuluku = -2.0;
//-IO.println("liukuluku = " + liukuluku);
float pieniLiukuluku = 2.0f;
//-IO.println("pieniLiukuluku = " + pieniLiukuluku);
double tieteellinenMuoto = 1.5e-2;
//-IO.println("tieteellinenMuoto = " + tieteellinenMuoto);

boolean totuusarvo = true;
//-IO.println("totuusarvo = " + totuusarvo);
//-}
```

## Käärijäluokat

Javassa kullekin alkeistietotyypille on olemassa niin sanottu käärijäluokka
(engl. *wrapper class*). Käärijäluokasta löytyy hyödyllisiä metodeja, kuten
`toString()` sekä vakioita, kuten `MAX_VALUE` alkeistietotyyppien käsittelyyn.
Alkeistietotyypit ja niitä vastaavat käärijäluokat on esitetty alla olevassa
taulukossa. 

| Alkeistietotyyppi | Käärijäluokka |
| ----------------- | ------------- |
| byte              | Byte          |
| short             | Short         |
| int               | Integer       |
| long              | Long          |
| float             | Float         |
| double            | Double        |
| char              | Character     |
| boolean           | Boolean       |

Tässä käytetään tietotyypin käärijäluokassa olevaa vakiota MAX_VALUE ja
muunnetaan käärijäluokan avulla muuttujan `kaksiTavua` ensin merkkijonoksi ja
sen jälkeen tulostetaan merkkijonon ensimmäinen merkki.

```java
void main() {
    byte tavu = Byte.MAX_VALUE;
    short kaksiTavua = Short.MAX_VALUE;
    IO.println(tavu);
    IO.println(kaksiTavua);
    IO.println(Short.toString(kaksiTavua).charAt(0));

    int maksimi = Integer.MAX_VALUE;
    IO.println(maksimi + " On suurin luku, jonka voi tallettaa int tyyppiseen muuttujaan" );
    int ylivuoto = Integer.MAX_VALUE + 1;
    IO.println("Ylitetään lukualue:");
    IO.println(ylivuoto);
}
```



## Merkkijonot

Javassa merkkijonoja ei lasketa alkeistietotyypiksi.
Java-kieli tarjoaa kuitenkin merkkijonoille oman syntaksin: uuden merkkijonon
voi luoda kirjoittamalla merkkejä lainausmerkkien `"` väliin:

```java
//-void main() {
String jono = "Opiskelen ohjelmointia!";
//-IO.println("jono = " + jono);
//-}
```
Javassa merkkijono on muuttumaton. Jos yrität suorittaa jonkin operaation
merkkijonolle, saat tulokseksi uuden merkkijonon, eikä alkuperäinen merkkijono
muutu. Katsotaan tästä esimerkki:

```java
//-void main() {
String muuttumaton = "Tämä on muuttumaton.";
//-IO.println("muuttumaton = " + muuttumaton);

muuttumaton.concat("Vai onko sittenkään?");
//-IO.println("muuttumaton = " + muuttumaton);
//-}
```

Metodin `concat()` palauttamaa *uutta* merkkijonoa ei nyt tallenneta mihinkään,
ja alkuperäinen merkkijono pysyy ennallaan. Toisin sanoen, merkkijonomuuttujien
arvoa voi muuttaa vain sijoittamalla:

```java
//-void main() {
String muuttumaton = "Tämä on muuttumaton.";
//-IO.println("muuttumaton = " + muuttumaton);

// HIGHLIGHT_GREEN_BEGIN
muuttumaton = muuttumaton.concat("Vai onko sittenkään?");
// HIGHLIGHT_GREEN_END
//-IO.println("muuttumaton = " + muuttumaton);
//-}
```

`String`-tyyppi sisältää lukuisia hyödyllisiä metodeja. Alla on lueteltu joitain
niistä. 

| Metodi                         | Selitys                                                                                                |
| ------------------------------ | ------------------------------------------------------------------------------------------------------ |
| `jono.charAt(paikka)`          | Palauttaa jonossa olevan yksittäisen merkin indeksistä `paikka`.                                       |
| `jono.length()`                | Palauttaa jonossa olevien merkkien määrän eli jonon pituuden.                                          |
| `jono.trim()`                  | Palauttaa kopion jonosta ilman alussa ja lopussa olevia ylimääräisiä tyhjiä merkkejä.                  |
| `jono.replace(mitä, millä)`    | Palauttaa kopion jonosta, jossa jonot/merkit `mitä` on korvattu jonolla/merkillä `millä`.              |
| `jono.split(haku)` | "Pilkkoo" jonon osiin `haku`-jonon esiintymien kohdalla ja palauttaa taulukon pilkotuista osajonoista. Huomaa, että `haku` on ns. [säännöllinen lauseke](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/regex/Pattern.html#sum). |
| `jono.contains(etsittävä)`     | Palauttaa `true`, jos `etsittävä` löytyy jonosta.                                                      |
| `jono.indexOf(etsittävä)`      | Palauttaa indeksin, jossa `etsittävä` esiintyy ensimmäistä kertaa.                                     |
| `jono.substring(mistä, mihin)` | Palauttaa osan jonosta alkaen indeksistä `mistä` päättyen indeksiin `mihin`.                           |
| `String.join(merkki, jonot)`   | Palauttaa jonon, jossa taulukossa `jonot` olevat jonot ovat peräkkäin yhdistettynä merkillä `merkki`). |

Kaikki toiminnot ja niiden tarkat selitykset löytyvät JavaDocs-sivulta (ks. [Class
`Sting`](https://docs.oracle.com/en/java/javase/25/docs/api//java.base/java/lang/String.html)).
Katsotaan vielä, miten yllä olevia esimerkkejä voi käyttää:

```java
void main() {
    String mjono = "Opiskelen ohjelmointia java-kielellä.";
    IO.println("mjono = " + mjono);
    IO.println("Ensimmäinen merkki: " + mjono.charAt(0));
    IO.println("Jonon pituus: " + mjono.length());

    IO.println(); // Lisää ylimääräisen rivivaihdon

    // Merkkijonojen yhdistäminen onnistuu + operaattorilla
    mjono = mjono + " Hei maailma!";
    IO.println("mjono (lisäyksen jälkeen) = " + mjono);

    // Tekstin korvaaminen merkkijonossa
    mjono = mjono.replace("java", "Java");
    IO.println("mjono (korvattu java -> Java) = " + mjono);

    IO.println();

    // "Pilkkoo" jonon kahteen osajonoon viivan kohdalla
    // HUOM: split-metodissa merkit \^$.|?*+()[]{}
    // vaativat, että niiden eteen laitetaan kenoviiva \\
    // Eli jos haluttaisiin pilkkoa pisteen kohdalla, tulisi kirjoittaa
    // mjono.split("\\.") eikä mjono.split(".");
    // jälkimmäinen versio on ns. säännöllinen lauseke (regular expression),
    // joka pilkkoo jonon jokaisen merkin kohdalla
    String[] lauseet = mjono.split("\\.");
    IO.println("lauseet = " + Arrays.toString(lauseet));

    IO.println();

    // indexOf etsii indeksin, jossa annettu jono löytyy
    int ohjelmointiaPaikka = mjono.indexOf("ohjelmointia");
    IO.println("ohjelmointiaPaikka = " + ohjelmointiaPaikka);

    // substring palauttaa osajonon annettusta jonosta indeksin perusteella
    String osajono = mjono.substring(ohjelmointiaPaikka, ohjelmointiaPaikka + 12);
    IO.println("osajono = " + osajono);

    IO.println();

    // Operaatio "String + lauseke" muuntaa lausekkeen arvon merkkijonoksi
    String toinenJono = "1/2 = " + (1.0 / 2);
    IO.println("toinenJono = \"" + toinenJono + "\"");
}
```

### Luvun parsiminen merkkijonosta

Merkkijono voidaan muuntaa luvuksi käyttämällä käärijäluokkien
`parse`-alkuisia metodeja. Esimerkiksi `Integer.parseInt` muuntaa merkkijonon
kokonaisluvuksi ja `Double.parseDouble` muuntaa merkkijonon desimaaliluvuksi.

```java,ignore
void main() {
    String kokonaislukuJono = "42";
    int kokonaisluku = Integer.parseInt(kokonaislukuJono);
    IO.println("kokonaisluku = " + kokonaisluku);

    String desimaalilukuJono = "3.14";
    double desimaaliluku = Double.parseDouble(desimaalilukuJono);
    IO.println("desimaaliluku = " + desimaaliluku);
}
```

## StringBuilder

Käytä `StringBuilder`-luokkaa, kun tarvitset muunneltavan merkkijonon. Se
tarjoaa menetelmiä merkkijonon muokkaamiseen ilman uusien merkkijono-olioiden
luomista, mikä tehostaa muistin käyttöä. 

Alla on lueteltu joitain StringBuilder-luokan hyödyllisiä metodeja. 

| Metodi              | Selitys                                                          |
| ------------------- | ---------------------------------------------------------------- |
| `sb.charAt(paikka)` | Palauttaa jonossa olevan yksittäisen merkin indeksistä `paikka`. |
| `sb.length()`       | Palauttaa jonossa olevien merkkien määrän eli jonon pituuden.    |
| `sb.append(arvo)`   | Lisää arvon nykyisen jonon loppuun.                              |
| `sb.toString()`     | Palauttaa kopion tästä jonosta `String`-merkkijonona.            |

Kaikki toiminnot ja niiden tarkat selitykset löytyvät JavaDocs-sivulta (ks. [Class
`StingBuilder`](https://docs.oracle.com/en/java/javase/25/docs/api//java.base/java/lang/StringBuilder.html)).
Alla on esimerkkejä metodien käytöstä.

```java
void main() {
    StringBuilder muuttuva = new StringBuilder("Tämä on muuttuva");
    IO.println("muuttuva = " + muuttuva);
    IO.println("muuttuva.length() = " + muuttuva.length());

    IO.println();

    muuttuva.append(" merkkijono.");
    IO.println("muuttuva = " + muuttuva);
    IO.println("muuttuva.length() = " + muuttuva.length());

    IO.println();

    String muuttumatonKopio = muuttuva.toString();
    IO.println("muuttumatonKopio = " + muuttumatonKopio);
}
```

## Taulukot

Taulukkoja (engl. *array*) käytetään tallentamaan joukkoa samantyyppisiä
alkioita muuttujaan. Tämä helpottaa datan tehokasta hallintaa ja organisointia.  

Uuden taulukon määrittely ja luominen Javassa onnistuu seuraavasti:

```java,ignore
tyyppi[] nimi = new tyyppi[koko];
```

Tässä `new tyyppi[koko]` luo taulukon, joka sisältää `koko` kappaletta
alkioita, joiden tyyppi on `tyyppi`.
Taulukon luomisen jälkeen alkioiden arvoja voi asettaa käyttäen sijoituslausetta
seuraavasti:

```java
//-void main() {
int[] arvosanat = new int[4];
arvosanat[0] = 4;
arvosanat[1] = 2;
arvosanat[2] = 2;
arvosanat[3] = 5;
//-IO.println("arvosanat = " + Arrays.toString(arvosanat));
//-}
```

Sijoituslauseessa `\[numero]` tarkoittaa alkion paikkaa eli *indeksiä*
taulukossa.
Javassa indeksointi alkaa nollasta, eli ensimmäinen alkio on indeksissä 0, toinen
indeksissä 1, ja niin edelleen. Taulukon viimeisen alkion indeksi on aina
`taulukko.length - 1`.

Jos alkioiden arvot tunnetaan etukäteen, taulukon voi myös luoda seuraavasti

```java
//-void main () {
int[] arvosanat = new int[] {4, 2, 2, 5};
//-IO.println("arvosanat = " + Arrays.toString(arvosanat));
//-}
```

Yhdistetyssä muuttujan määrittely- ja sijoituslauseessa `new T[]` osa
on myös sallittua pudottaa pois, jolloin yllä oleva voi tiivistää lisää:

```java
//-void main () {
int[] arvosanat = {4, 2, 2, 5};
//-IO.println("arvosanat = " + Arrays.toString(arvosanat));
//-}
```

Javassa taulukkojen kokoa ei voi muuttaa taulukon luomisen jälkeen.
Sijoittaminen paikkaan, jota ei ole taulukossa, aiheuttaa virheen
ohjelman ajon aikana:

```java,ignore
int[] arvosanat = new int[] {4, 2, 2, 5};
arvosanat[5] = 3;
```
```
java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 4
	at main.main(main.java:3)
```

Javassa taulukon pituuden voi aina tarkistaa `length`-attribuutilla.
Lisäksi taulukon voi tulostaa käyttämällä `Arrays.toString`-metodia (ks. [JavaDocs](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Arrays.html#toString(java.lang.Object[])))

```java
//-void main() {
int[] arvosanat = new int[] {4, 2, 2, 5};
IO.println("Taulukon pituus: " + arvosanat.length);
IO.println("Taulukon sisältö: " + Arrays.toString(arvosanat));
//-}
```

### Moniulotteiset taulukot 

Toisin kuin esimerkiksi C#-kielessä, Javassa ei ole erillisiä moniulotteisia
taulukkoja. Sen sijaan Javassa voi luoda taulukon, jonka alkioina
ovat taulukot, eli `T[][]`:

```java
//-void main() {
int[][] taulukko2D = new int[][] {
    new int[] {1, 2, 3},
    new int[] {4, 5, 6, 7},
    new int[] {8, 9, 0},
};

// Taulukon pituus on tässä siten taulukkojen lukumäärä, eli "rivien" määrä.
IO.println("Taulukossa on " + taulukko2D.length + " taulukkoa.");

// Indeksointi toimii normaalisti; alkiona on nyt kokonainen taulukko
IO.println("taulukko2D[0] on taulukko: " + Arrays.toString(taulukko2D[0]));
IO.println("taulukko2D[1] on taulukko: " + Arrays.toString(taulukko2D[1]));
IO.println("taulukko2D[2] on taulukko: " + Arrays.toString(taulukko2D[2]));

// Myös yksittäisen taulukon indeksointi toimii normaalisti,
// mutta huomaa syntaksi!
int ensimmainenAlkio = taulukko2D[0][0];
IO.println("Ensimmäisen rivin ensimmäinen alkio: " + ensimmainenAlkio);

IO.println("Rivillä 2 (indeksi 1) kolmas alkio (indeksi 2) on: " + taulukko2D[1][2]);
//-}
```

Huomaa, että yllä olevassa esimerkissä `taulukko2D[0][0]` viittaa
ensimmäisen taulukon (`taulukko2D[0]`) ensimmäiseen alkioon
`(taulukko2D[0])[0]`. Yllä oleva taulukko ja siinä olevat alkiot voisi kuvata
siis seuraavasti:

```bob
                      [0]                [1]                [2]
              +------------------+------------------+------------------+
              | taulukko2D[0][0] | taulukko2D[0][1] | taulukko2D[0][2] |
taulukko2D[0] |                  |                  |                  |
              |        1         |        2         |        3         |
              +------------------+------------------+------------------+

              +------------------+------------------+------------------+------------------+
              | taulukko2D[1][0] | taulukko2D[1][1] | taulukko2D[1][2] | taulukko2D[1][3] |
taulukko2D[1] |                  |                  |                  |                  |
              |        4         |        5         |        6         |        7         |
              +------------------+------------------+------------------+------------------+

              +------------------+------------------+------------------+
              | taulukko2D[2][0] | taulukko2D[2][1] | taulukko2D[2][2] |
taulukko2D[2] |                  |                  |                  |
              |        8         |       9          |        0         |
              +------------------+------------------+------------------+
```

Huomaa erityisesti, että "rivitaulukkojen" ei tarvitse olla välttämättä
samanpituuisia.

## Vakiot

Muuttuja, jolle voidaan sijoittaa arvo vain alustuksen yhteydessä, määritellään
käyttämällä `final`-avainsanaa. Javan koodauskäytänteisiin kuuluu, että
`final`-muuttujat kirjoitetaan suuraakkosin ja sanat erotellaan toisistaan
alaviivalla.

Javassa `final`-avainsanaa voi käyttää sekä alkeistietotyyppien että
viitetietotyyppien kanssa. On kuitenkin huomattava, että viitetietotyyppisen
muuttujan tapauksessa `final`-sana tarkoittaa, että viitettä ei voi muuttaa
osoittamaan uuteen dataan. Viitteen päässä olevaa dataa voi silti muuttaa, jos
tietotyyppi sallii sen.

```java,ignore
final int PAIVIA_VIIKOSSA = 7;
final int[] PAIVIA_KUUKAUDESSA_KARKAUSVUOSI = new int[] {31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

// PAIVIA_VIIKOSSA = 8; // Tämä aiheuttaa käännösvirheen
PAIVIA_KUUKAUDESSA_KARKAUSVUOSI[0] = 30; // Tämä on sallittu
```

Vakioita tarvitaan mm. koodin lukemisen helpottamiseksi, toisteisen koodin
vähentämiseksi, luotettavuuden parantamiseksi ja suorituskyvyn parantamiseksi.

## Listat

Lista on tietorakenne, joka voi kasvaa ja kutistua tarpeen mukaan. Kuten
taulukko, lista voi sisältää vain yhden tyypin mukaisia alkioita. Listan koko ei
ole kiinteä, mikä tekee siitä joustavamman tilanteisiin, joissa alkioiden määrä
ei ole etukäteen tiedossa. Javan listat vastaavat siten JavaScriptin taulukkoja.

Javan yleisin listan tyyppi on `ArrayList<T>`, jossa `T` on listassa olevien
alkioiden tyyppi. Jotta listoja voi käyttää koodissa, tulee ne ensin tuoda 
kääntäjän näkyville lisäämällä tiedoston ensimmäiselle riville `import`-määre:

```java,ignore
import java.util.*;

// Varsinainen ohjelma
void main() ...
```

`import`-määre kertoo kääntäjälle, että ohjelmassa käytetään tyyppejä, jotka
löytyvät `java.util`-pakkauksesta. Pakkauksiin palataan tarkemmin myöhemmissä
osissa; tässä vaiheessa riittää tiedostaa, että kääntäjä ei välttämättä tiedä
tyyppien olemassaolosta ellei ne tuo näkyviin `import`-määreellä.

Kun `java.util`-pakkauksen sisältö on tuotu ohjelmaan, voidaan listoja alustaa
seuraavasti:

```java
import java.util.*;

void main() {
    // Tapa 1: Tyhjä lista ilman alkioita
    List<Integer> arvosanat = new ArrayList<Integer>();
    // Lisätään alkiot yksi kerrallaan
    arvosanat.add(4);
    arvosanat.add(2);
    arvosanat.add(2);
    arvosanat.add(5);
    //-IO.println("arvosanat = " + arvosanat);

    // Tapa 2: Lista, jossa alkiot annettu valmiiksi
    List<Integer> arvosanatValmis = new ArrayList<Integer>(List.of(4, 2, 2, 5));
    //-IO.println("arvosanatValmis = " + arvosanatValmis);
}
```

> [!HUOMAUTUS]
>
> Javan rajoituksista johtuen listojen **alkioiden tyypin on aina oltava
> viitetyyppi.** Täten esimerkiksi `int`-alkioita sisältävän listan
> ei voi kirjoittaa muodossa `ArrayList<int>`:
> 
> ```java,ignore
> List<int> lista = new ArrayList<int>();
> ```
> ```
> error: unexpected type
> List<int> lista = new ArrayList<int>();
>      ^
>   required: reference
>   found:    int
> ```
>
> Jos tarvitset listoja, jonka alkioina ovat alkeistietotyypit, käytä
> alkioiden tyyppinä [alkeistietotyyppien käärijäluokat](#käärijäluokat),
> jotka ovat viitetyyppejä, mutta toimivat kuten niitä vastaavat alkeistietotyypit.
> Toisin sanoen, `ArrayList<Integer>` on sallittu, kun taas `ArrayList<int>` ei ole.
> Puolestaan `ArrayList<String>` on sallittu, koska merkkijono on viitetietotyyppi.

> [!HUOMAUTUS]
>
> Javan *koodauskäytänteisiin* kuuluu, että lista*muuttujien* tyyppinä käytetään
> `List<T>`, kun taas muuttujien arvojen alustuksessa käytetään
> tarkempaa tyyppiä, kuten `ArrayList<T>`.
>
> Toisin sanoen, vaikka alla oleva on sallittu
>
> ```java
>
> 
> //-void main() {
> ArrayList<String> nimet = new ArrayList<String>(List.of("Matti", "Teppo"));
> //-IO.println("nimet = " + nimet);
> //-}
> ```
>
> **koodauskäytänteiden** mukaisesti on yleisempää esittää muuttuja seuraavasti:
>
> ```java
>
> 
> //-void main() {
> List<String> nimet = new ArrayList<String>(List.of("Matti", "Teppo"));
> //-IO.println("nimet = " + nimet);
> //-}
> ```
>
> Lisäksi, jos alkioiden tyyppi on muuttujan määrittelyrivin perusteella selvä,
> alkioiden tyyppi saatetaan usein jättää pois listan alustuksesta:
>
> ```java
> //-void main() {
> // Kääntäjä päättelee, että ArrayList<> = ArrayList<String> 
> // muuttujan tyypin perusteella
> List<String> nimet = new ArrayList<>(List.of("Matti", "Teppo"));
> //-IO.println("nimet = " + nimet);
> //-}
> ```
>
> Palaamme tarkemmin `List<T>` ja `ArrayList<T>` -tyyppien välisiin eroihin
> [osassa 5](../osa5/index.md). Voit tässä vaiheessa kuitenkin miettiä,
> että `List<T>` on yleinen tyyppi listoille, kun taas `ArrayList<T>` on
> (eräs) Javan tarjoama tapa esittää lista.

Katsotaan vielä listojen eräitä hyödyllisiä metodeja.

| Metodi                    | Selitys                                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------------------ |
| `size()`                  | Palauttaa listassa olevien alkioiden lukumäärän.                                                       |
| `add(lisättävä)`          | Lisää alkion listan loppuun.                                                                           |
| `add(indeksi, lisättävä)` | Lisää alkion listan indeksiin `indeksi` siirtäen loput alkiot yhden paikan eteenpäin.                  |
| `get(indeksi)`            | Palauttaa indeksissä `indeksi` olevan alkion.                                                          |
| `remove(poistettava)`     | Poistaa listasta `poistettava`:n ensimmäisen esiintymän siirtäen loput alkiot yhden paikan taaksepäin. |
| `remove(indeksi)`         | Poistaa listasta paikassa `indeksi` olevan alkion.                                                     |

Löydät lisää metodeja JavaDocs-sivustolla (ks. [Class `ArrayList<E>`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/ArrayList.html)).

```java
import java.util.*;

void main () {
    // Luodaan tyhjä merkkijonolista
    List<String> nimet = new ArrayList<>();
    // Lisätään alkioita listaan
    nimet.add("Matti");
    nimet.add("Teppo");
    nimet.add("Liisa");

    // Tulostetaan listan koko
    IO.println("Listan koko: " + nimet.size());
    IO.println("------");
    // Haetaan alkio indeksistä 1 (toinen alkio)
    String toinen = nimet.get(1);
    IO.println("Toinen alkio: " + toinen);
    IO.println("------");

    // Poistetaan alkio indeksistä 0 (ensimmäinen alkio)
    nimet.remove(0);
    IO.println("Poistettiin ensimmäinen alkio.");
    IO.println("------");
    // Tulostetaan kaikki alkiot
    IO.println("nimet = " + nimet);
    IO.println("------");

    // Tulostetaan listan koko
    IO.println("Listan koko: " + nimet.size());


    // Kaksi esimerkkiä siitä, kuinka luoda listaan heti sisältöä
    List<String> elaimet = new ArrayList<>(List.of("koira", "kissa", "kala"));
    List<String> varit = Arrays.asList("punainen", "sininen", "keltainen");
    IO.println("elaimet = " + elaimet);
    IO.println("varit = " + elaimet);
}
```

Huomaa ainakin nämä erot Javan, C# ja Pythonin välillä listoja käytettäessä.
Muuttuja `i` viittaa listan indeksiin.

| Toiminto                    | Java                                    | C#                 | Python                              |
| --------------------------- | --------------------------------------- | ------------------ | ----------------------------------- |
| Lukeminen tietystä paikasta | `list.get(i)`                           | `list[i]`          | `list[i]`                           |
| Listan koko                 | `list.size()`                           | `list.Count`       | `len(list)`                         |
| Poistaminen                 | `list.remove(i)`                        | `list.RemoveAt(i)` | `list.pop(i)`                       |
| Onko lista tyhjä?           | `list.isEmpty()` tai `list.size() == 0` | `list.Count == 0`  | `if not list:` tai `len(list) == 0` |

## Javan tyyppijärjestelmä

Java on *staattisesti tyypitetty* kieli, mikä tarkoittaa, että muuttujien 
tyypit määräytyvät käännösaikana, ei ohjelman ajon aikana.
Jos yrität sijoittaa muuttujaan väärän
tyyppistä tietoa, ohjelma ei käänny, ja kääntäjä antaa virheilmoituksen.

Käytännössä Javassa eri tietotyyppejä ei voi käyttää
toistensa sijaan, ellei kieli nimenomaisesti salli sitä. Esimerkiksi totuusarvoa
(`boolean`) ei voi käyttää lukuarvona, eikä viitetyyppistä arvoa voi käsitellä
kokonaislukuna. Jos ohjelmoija yrittää rikkoa näitä sääntöjä, seurauksena on
käännösvirhe.

```java,ignore
void main() {
    boolean totuusarvo = false;
    totuusarvo = 1;
}
```
```
error: incompatible types: int cannot be converted to boolean
    totuusarvo = 1;
                 ^
1 error
error: compilation failed
```

Yllä oleva käännösvirhe kertoo, että kokonaislukua (`int`) ei voida muuntaa
totuusarvoksi (`boolean`).
Tämä on selkeä ero dynaamisesti tyypitettyihin kieliin, kuten Pythoniin tai
JavaScriptiin, jossa samaan muuttujaan voi sijoittaa erityyppisiä arvoja:

```javascript
// Tämä on sallittu koodi JavaScriptissa
let totuusarvo = true;
//-console.log(`totuusarvo = ${totuusarvo}`);
totuusarvo = 1;
//-console.log(`totuusarvo = ${totuusarvo}`);
```

On kuitenkin väistämätöntä, että ohjelmassa tulee käsitellä useita erityyppisiä
arvoja. Tätä varten Javassa on valmiiksi määritelty joitain automaattisia
sääntöjä, joiden perusteella kääntäjä osaa tehdä *implisiittisen*
tyyppimuunnoksen. Esimerkiksi

- kokonaislukuja (`int`) saa muuntaa desimaaliluvuksi (`double`),
- pienempiä kokonaislukuja (esim. 8-bittinen kokonaisluku `byte`) saa muuntaa
  enemmän tilaa vievään kokonaislukuun (esim. 32-bittinen kokonaisluku `int`).

Tyyppimuunnossääntöjä on paljon lisääkin; yleisperiaate on, että jos
muunnos ei aiheuta tiedon menetystä, sille on varmasti olemassa automaattinen muunnos.
Automaattinen muunnos tapahtuu sijoituksissa ja lausekkeiden yhteydessä.

```java
void main() {
    int kokonaisluku = 23;
    //-IO.println("kokonaisluku = " + kokonaisluku);
    double desimaaliluku = kokonaisluku; // OK: int -> double muunnos on implisiittinen
    //-IO.println("desimaaliluku = " + desimaaliluku);

    // HUOM: jakolasku on int / int => desimaalit häviävät
    double puoletVirhe = 1 / 2; 
    //-IO.println("puoletVirhe = " + puoletVirhe);

    // OIKEIN: jakolasku on int / double -> double / double
    double puoletOikein = 1 / 2.0;
    //-IO.println("puoletOikein = " + puoletOikein);
}
```

Lisäksi ohjelmoija voi erikseen pakottaa ns. *eksplisiittinsen* tyyppimuunnoksen
käyttämällä syntaksia `(uusiTyyppi)muuttujanNimi`.
Tämä soveltuu tilanteisiin, jossa muunnos ei olisi mahdollista implisiittisesti:

```java
void main() {
  long sairaanIsoLuku = 40000000000L; // long = 64-bittinen luku
  IO.println("Iso, long-tyyppinen luku: " + sairaanIsoLuku);
  // long -> int ei ole implisiittinen, mutta se onnistuu eksplisiittisesti
  int katkaistu = (int)sairaanIsoLuku; // int = 32-bittinen luku
  IO.println("int-luku eksplisiittisen tyyppimuunnoksen jälkeen: " + katkaistu);
}
```

Staattinen tyypitys tarkoittaa Javassa käytännössä sitä, että tyyppeihin
liittyvät virheet pyritään estämään jo ennen ohjelman suorittamista. Kääntäjä toimii
eräänlaisena turvaverkkona, joka varmistaa, että arvot, muuttujat ja operaatiot
ovat keskenään yhteensopivia.
