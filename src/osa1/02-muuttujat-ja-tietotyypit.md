# Muuttujat ja tietotyypit

> [!Osaamistavoitteet]
>
> - Kerrataan lyhyesti rakenteisen ohjelmoinnin perusteet
> - Muuttujat ja vakiot (perustyypit, `final`, String)

Ohjelmat käsittelevät muistiin tallennettua tietoa. Konekielessä tietoon viitataan numeerisilla muistiosoitteilla, mutta korkean tason kielissä, kuten Javassa, käytetään selkokielisiä nimiä. Tällaista nimeä, joka viittaa muistissa olevaan tietoon, kutsutaan muuttujaksi (engl. *variable*). Ohjelmoijan tarvitsee muistaa vain nimi; tietokone huolehtii tiedon todellisesta sijainnista muistissa.

Javassa muuttujaan asetetaan tietoa käyttämällä sijoituslausetta. 

```java,ignore
tyyppi muuttuja = lauseke;
```

Kun tietokone suorittaa sijoituslauseen, se laskee yhtäsuuruusmerkin oikealla puolella olevan lausekkeen (engl. *expression*) arvon ja tallentaa sen vasemmalla puolella nimettyyn muuttujaan.

```java,ignore
double korkokerroin = 0.05;
double paaoma = 150.0;
```
Tässä luku 0.05 sijoitetaan `double`-tyyppiseen muuttujaan nimeltä `korkokerroin`, ja luku 150.0 `double`-tyyppiseen muuttujaan nimeltä `paaoma`. Jos muuttujissa oli aiemmin jotain muita arvoja, ne korvataan uusilla. Muuttujan tyyppi määritellään muuttujan nimen edessä, ja se kertoo, millaista tietoa muuttuja voi sisältää. 

Muuttuja voi olla myös lausekkeen osana, ja siten sen arvoa voidaan käyttää osana sijoitettavaa lauseketta. Huomaa, että tyyppiä ei tarvitse toistaa, kun viitataan olemassa olevaan muuttujaan.

```java,ignore
double paaomaKorolla = (1 + korkokerroin) * paaoma;
```

Tässä siis ohjelma lukee muuttujien `korkokerroin` ja `paaoma` sisältämät arvot, summaa ne keskenään, ja tallentaa tuloksen muuttujaan, jonka nimi on `paaomaKorolla`.

Ohjelmoinnissa sijoitus on *lause*, ei matemaattinen yhtälö. Lause `double paaoma = 150.0;` on totta vain suoritushetkellä. Muuttujan arvo voi vaihtua myöhemmin ohjelman edetessä, toisin kuin matematiikan vakioissa. Lausetta voi ajatella myös käskynä; yllä oleva lause kuuluisi kutakuinkin "tallenna luku 150.0 muistiin paikkaan, jota kutsutaan tästä eteenpäin nimellä `paaoma`".

## Javan tyyppijärjestelmä

Javan tietotyypit voidaan jakaa kahteen pääryhmään: alkeistietotyyppeihin (engl. *primitive data types*) ja viitetietotyyppeihin (engl. *reference data types*). Kaikki tieto tallennetaan tietokoneen muistiin binäärilukuina (nollien ja ykkösten sarjana), ja tietotyypit eroavat toisistaan siinä, kuinka paljon muistia ne varaavat ja millaista dataa ne esittävät. Alkeistietotyypit sisältävät yksinkertaisia arvoja, kuten kokonaislukuja ja totuusarvoja, kun taas viitetietotyypit voivat sisältää monimutkaisempia rakenteita, kuten olioita, taulukoita ja merkkijonoja. 

### Alkeistietotyypit

Javassa on kahdeksan sisäänrakennettua [alkeistietotyyppiä](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html). Lisäksi `String`-tyyppi muistuttaa alkeistietotyyppiä, vaikka teknisesti ottaen se ei sellainen olekaan. Käydään läpi nämä tyypit yksi kerrallaan.

**Kokonaisluvut**: Kokonaisluvuille on neljä tyyppiä, jotka eroavat toisistaan lukualueen ja muistinkulutuksen perusteella. Yleisimmin käytetty kokonaislukutyyppi on `int`. 

| Tyyppi | Koko (tavua /bittiä) | Lukualue (suuntaa antava)       |
| ------ | -------------------- | ------------------------------- |
| byte   | 1 tavu (8 bittiä)    | -128 ... 127                    |
| short  | 2 tavua (16 bittiä)  | -32 768 ... 32 767              |
| int    | 4 tavua (32 bittiä)  | n. -2 miljardia ... 2 miljardia |
| long   | 8 tavua (64 bittiä)  | n. +/- 9 * 10^18                |

TODO: Esimerkki siitä, mitä tapahtuu kun operoidaan luvuilla jotka ylittävät lukualueen. Python, C#. 

**Liukuluvut**: Desimaaliluvuille käytetään liukulukutyyppejä. Yleisin näistä on `double`.

| Tyyppi | Koko (tavua)        | Tarkkuus                  |
| ------ | ------------------- | ------------------------- |
| float  | 4 tavua (32 bittiä) | n. 7 merkitsevää numeroa  |
| double | 8 tavua (64 bittiä) | n. 15 merkitsevää numeroa |


Koska Java käyttää IEEE 754 standardia desimaalilukujen`double` ja `float` esittämiseen, niillä on muutama mielenkiintoinen ja kenties yllättävä ominaisuus:

```java
void main() {
    float negatiivinenAarettomyys = -1.0f / 0.0f;
    IO.println(negatiivinenAarettomyys);
    double positiivinenAarettomyys = 1.0 / 0.0;
    IO.println(positiivinenAarettomyys);
    double nan = 0.0 / 0.0;
    IO.println(nan);
}
```

Eli desimaaliluvuille on erikseen määritelty $-\infty, \infty$ ja `NaN` = **N**ot **A** **N**umber. Huomaa myös, että jos haluat erikseen `float` tyyppisen desimaaliluvun, luvun perässä pitää olla `f`. Muutoin se tulkitaan `double`ksi.

Javasta löytyy myös enemmän [numeerisia](https://docs.oracle.com/javase/8/docs/api/java/lang/Number.html) tietotyyppejä, mutta tällä kurssilla riittänevät käytännössä `int` ja `double`. Hyvin isoja kokonaislukuja varten on tarjolla [`BigInteger`](https://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html) ja hyvin tarkkoja desimaalilukuja varten [`BigDecimal`](https://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html), mutta niitä tuskin tällä opintojaksolla tarvitsemme. 

**Merkit**: Yksi merkki tallennetaan `char`-tyyppiseen muuttujaan, joka käyttää 2 tavua muistia.

**Totuusarvot**: Totuusarvoja varten on `boolean`-tyyppi, jolla on kaksi mahdollista arvoa: `true` (tosi) tai `false` (epätosi).

**Merkkijono**: Vaikka `String`-tyyppi ei teknisesti ottaen olekaan alkeistietotyyppi, se käyttäytyy monin tavoin kuin alkeistietotyyppi. Siten sen voidaan katsoa kuuluvan tähän kategoriaan. `String`-tyyppiä käytetään merkkijonojen, eli tekstin, tallentamiseen.

### Viitetietotyypit

Viitetietotyypit sisältävät monimutkaisempia tietorakenteita, kuten olioita, taulukoita ja merkkijonoja. 
Esimerkiksi `String` on viitetietotyyppi, kuten myös kaikki taulukot, esimerkiksi `int[]`. 

Viitetietotyyppinen muuttuja eroaa alkeistietotyyppisestä muuttujasta erityisesti siinä, että se ei sisällä itse dataa, vaan se on viite (engl. *reference*) olioon. Java-aiheisessa kirjallisuudessa saatetaan esittää, että viite on osoitin siihen keskusmuistin paikkaan, jossa olio sijaitsee. Asia on kuitenkin hieman monimutkaisempi, sillä Java ei salli osoitinten suoraa käsittelyä ohjelmoijan toimesta. Voit kuitenkin ajatella viitettä siten, että se on tapa päästä käsiksi olioon, joka sijaitsee "jossakin muualla" muistissa.

<details><summary>✨ Valinnaista lisätietoa: Miksi viitetietotyyppejä on olemassa?</summary>

On useampia syitä siihen, miksi nämä kaksi eri kategoriaa tietotyypeille on olemassa.

Ensimmäinen liittyy suorituskykyyn ja muistin hallintaan. Jos kaikki muuttujat olisivat arvopohjaisia (kuten alkeistietotyypit), se aiheuttaisi valtavasti turhaa muistin kulutusta ja hidastaisi ohjelman suorituskykyä, erityisesti suurten tietorakenteiden kohdalla. Jos meillä olisi vaikkapa `kirja`, joka sisältäisi 1000 sivua tekstiä, niin joka ikinen kerta kun haluamme käsitellä `kirja`-muuttujaa, meidän pitäisi kopioida kaikki 1000 sivua muistissa. Tämä olisi erittäin tehotonta. Sen sijaan viitetietotyypit mahdollistavat sen, että me vain viittaamme `kirja`-olioon, joka sijaitsee jossakin muualla muistissa, ilman että tarvitsee kopioida koko kirjaa joka kerta.

Toinen syy liittyy jaettuun tilaan. Usein haluamme, että useampi ohjelman osa muokkaa samaa tietoa. Esimerkiksi on järkevää, että `pankkitili`-olio on jaettu useiden eri toimintojen kesken, kuten talletus, nosto ja tilin saldo. Arvopohjaisessa maailmassa joutuisimme kopioimaan `pankkitili`-olion joka kerta, kun tililtä halutaan nostaa rahaa, tehdä tilisiirto tai vaikkapa tarkistaa saldo. Tämä johtaisi helposti siihen, että eri kopiot olisivat eri tilassa, mikä saattaisi aiheuttaa virheitä.

Kolmas syy on dynaaminen koko. Viitetietotyypit mahdollistavat dynaamisesti kasvavien ja kutistuvien tietorakenteiden, kuten linkitettyjen listojen, pinojen ja jonoiden, luomisen. Näitä rakenteita ei voida helposti toteuttaa arvopohjaisina, koska arvopohjaisten muuttujien koko on kiinteä käännösaikana.

Neljäs syy liittyy erityisesti olio-ohjelmointiin, ja liittyy osittain myös kolmanteen kohtaan. Javassa viitteet mahdollistavat polymorfismin. Koska muuttuja on vain viite, se voi osoittaa mihin tahansa, joka "näyttää" oikealta tyypiltä. 

```java,ignore
Elain lemmikki = new Koira();
lemmikki = new Kissa();
```

Jos nämä olisivat puhtaita arvotyyppejä, `Elain`-tyyppiselle muuttujalle pitäisi varata kiinteä määrä muistia. Jos `Kissa` sitten tarvitsisikin enemmän muistia kuin `Elain` on varannut, koodi hajoaisi. Viitteiden avulla muuttujan koko on aina sama (viitteen koko), riippumatta siitä kuinka valtava olio viitteen päässä on.

</details>

## Literaalit

Literaali (engl. *literal*) tarkoittaa ohjelmakoodiin kirjoitettua kiinteää arvoa. Eri tietotyypeillä on omat kirjoitussääntönsä literaaleille.

 * **Merkit** (`char`): Kirjoitetaan yksittäisen lainausmerkin sisään, esimerkiksi `'A'`,  `'*'` ja `'x'`. Erikoismerkit alkavat kenoviivalla: `'\n'` (rivinvaihto), `'\u03A9'` (kreikkalainen iso omega) ja `'\t'` (tabulaattori).
 * **Kokonaisluvut** (`byte`, `short`, `int`, `long`): Kirjoitetaan suoraan numerona, esimerkiksi `42`, `-7` ja `0`. `long`-luvun literaali päättyy isoon tai pieneen kirjaimeen `L` tai `l`, esimerkiksi `12345678901L`.
 * **Liukuluvut** (`float`, `double`): Kirjoitetaan desimaalipisteellä erotettuna, esimerkiksi `3.14`, `-0.001` ja `2.0`. Voidaan käyttää myös tieteellistä muotoa: `1.5e3` (eli 1.5 × 10³ = 1500) ja `2.0E-4` (eli 2.0 × 10⁻⁴ = 0.0002). Oletuksena desimaaliluvut ovat `double`-tyyppiä. Jos haluat luoda `float`-luvun, literaalin tulee päättyä isoon tai pieneen kirjaimeen `F` tai `f`, esimerkiksi `3.14f`.
 * **Totuusarvot** (`boolean`): Kirjoitetaan avainsanoina `true` ja `false`.

## Käärijäluokat

Javassa kullekin alkeistietotyypille on olemassa niin sanottu käärijäluokka (engl. *wrapper class*). Käärijäluokasta löytyy hyödyllisiä metodeja, kuten `toString()` sekä vakioita, kuten `MAX_VALUE` alkeistietotyyppien käsittelyyn. Alkeistietotyypit ja niitä vastaavat käärijäluokat on esitetty alla olevassa taulukossa. 

| Alkeistietotyyppi | Käärijäluokka |
| ----------------- | -------------- |
| byte              | Byte           |
| short             | Short          |
| int               | Integer        |
| long              | Long           |
| float             | Float          |
| double            | Double         |
| char              | Character      |
| boolean           | Boolean        |

Tässä käytetään tietotyypin käärijäluokassa olevaa vakiota MAX_VALUE ja muunnetaan käärijäluokan avulla muuttujan `kaksiTavua` ensin merkkijonoksi ja sen jälkeen tulostetaan merkkijonon ensimmäinen merkki.

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

## Huomautuksia String-tyypistä

**Muuttumattomuus.** Javassa, kuten monissa muissakin kielissä merkkijono on
muuttumaton. Tämä liittyy muun muassa muistinkäytön tehokkuuteen ja sitä kautta
parempaan suorituskykyyn. Jos yrität suorittaa jonkin operaation merkkijonolle,
saat tulokseksi uuden merkkijonon, eikä alkuperäinen merkkijono muutu. Katsotaan
tästä esimerkki:

```java
//-void main() {
String muuttumaton = "Tämä on muuttumaton.";
IO.println(muuttumaton);
muuttumaton.concat("Vai onko sittenkään?");
IO.println(muuttumaton);
//-}
```

Metodin `concat()` palauttamaa *uutta* merkkijonoa ei nyt tallenneta mihinkään,
ja alkuperäinen merkkijono pysyy ennallaan. 

**Merkin hakeminen merkkijonosta.** Jos haluat tarkastella tiettyä kirjainta
merkkijonossa, se tapahtuu seuraavasti:

```java
//-void main() {
String mjono = "esimerkki";
IO.println(mjono.charAt(0));
// IO.println(mjono[0]); // Tämä ei toimi Javassa
//-}
```

## StringBuilder

Jos tarvitsee muunneltavan merkkijonon, käytä `StringBuilder`-luokkaa. Se
tarjoaa menetelmiä merkkijonon muokkaamiseen ilman, että joka kerta luodaan uusi
merkkijono.

```java
void main() {
    Byte tavu;
    IO.println(tavu);
    StringBuilder muuttuva = new StringBuilder("Tämä on muuttuva");
    IO.println(muuttuva);
    muuttuva.append(" merkkijono.");
    IO.println(muuttuva);
}
```

## Taulukot

Taulukkoja (engl. *array*) käytetään tallentamaan joukkoa samantyyppisiä
alkioita muuttujaan. Tämä helpottaa datan tehokasta hallintaa ja organisointia.  

Javan taulukot esitellään seuraavalla syntaksilla.

```java,ignore
Tyyppi[] nimi = new Tyyppi[koko];
```

Jos sisältö on jo tiedossa taulukkoa luotaessa, niin esimerkiksi kokonaislukutaulukon voi alustaa suoraan aaltosulkeiden sisään.

```java,ignore
void main () {
    int[] luvut = {1, 2, 3, 4 };
}
```

Indeksointi alkaa nollasta, eli ensimmäinen alkio on indeksissä 0, toinen indeksissä 1, ja niin edelleen. Taulukon viimeisen alkion indeksi on aina `taulukko.length - 1`.

Java täyttää taulukon oletusarvoilla riippuen taulukon tyypistä. Voit alla
kokeilla mitkä ovat kunkin taulukkotyypin oletusarvot vaihtamalla `char` tilalle
esimerkiksi `int` tai `double`. 

```java,editable
void main () {
    char[] luvut = new char[4];
    luvut[0] = 'a';
    IO.println(luvut[0]);
    IO.println(luvut[1]);
}
```

Jos haluamme lisätä tietorakenteeseen tietoa ohjelman ajon aikana, parempi
vaihtoehto on käyttää listoja.

Lue lisää taulukoista Javan dokumentaatiosta: <https://docs.oracle.com/javase/tutorial/java/nutsandbolts/arrays.html>


## Vakiot

Muuttuja, jolle voi sijoittaa arvon vain alustuksen yhteydessä esitellään käyttäen `final`-avainsanaa. Javan koodauskäytänteisiin kuuluu, että `final`-muuttujat kirjoitetaan suuraakkosin ja sanat erotellaan toisistaan alaviivalla.

```java,ignore
final int PAIVIA_VIIKOSSA = 7;
```

Vakioita tarvitaan mm. koodin lukemisen helpottamiseksi, toisteisen koodin vähentämiseksi, luotettavuuden parantamiseksi ja parantamaan suorituskykyä

## Listat

Kun emme tiedä datan määrää etukäteen tai se muuttuu jatkuvasti, käytämme listaa. Javan yleisin lista on ArrayList. Se on "älykäs taulukko", joka osaa venyttää itseään tarpeen mukaan.

ArrayList on osa Javan java.util-pakettia, joten se täytyy importata.

Alkioita lisätään listaan `add()`-metodilla, poistetaan `remove()`-metodilla ja
haetaan `get()`-metodilla. Listan koko saadaan `size()`-metodilla. 

Javassa `add()`-metodille on kaksi toteutusta, joista `add(lisättava)` lisää
listan loppuun ja `add(indeksi, lisättävä)` lisää tiettyyn indeksiin taulukossa
siirtäen loput alkiot yhden oikealle. Myös `remove()` metodille on kaksi
toteutusta, joista `remove(indeksi)` poistaa tietyssä indeksissä olevan alkion
ja `remove(poistettavaAlkio)` poistaa tietyn alkion listasta, jos alkio löytyy. 

```java
import java.util.ArrayList;

void main () {
    // Luodaan tyhjä merkkijonolista
    ArrayList<String> mjonoLista = new ArrayList<>();

    // Lisätään alkioita listaan
    mjonoLista.add("Matti");
    mjonoLista.add("Teppo");
    mjonoLista.add("Liisa");

    // Tulostetaan listan koko
    System.out.println("Listan koko: " + mjonoLista.size());
    System.out.println("------");
    // Haetaan alkio indeksistä 1 (toinen alkio)
    String toinen = mjonoLista.get(1);
    System.out.println("Toinen alkio: " + toinen);
    System.out.println("------");

    // Poistetaan alkio indeksistä 0 (ensimmäinen alkio)
    mjonoLista.remove(0);
    System.out.println("Poistettiin ensimmäinen alkio.");
    System.out.println("------");
    // Tulostetaan kaikki alkiot
    for (String mjono : mjonoLista) {
        System.out.println(mjono);
    }
    System.out.println("------");

    // Tulostetaan listan koko
    System.out.println("Listan koko: " + mjonoLista.size());


    //Kaksi esimerkkiä kuinka luoda listaan heti sisältöä
    List<String> elaimet = new ArrayList<>(List.of("koira", "kissa", "kala"));
    List<String> varit = Arrays.asList("punainen", "sininen", "keltainen");

    //For-Each on hyvä listojen tulostamiseen
    for (String mjono : mjonoLista) {
            IO.println(mjono);
    }

    for (String mjono : elaimet) {
        IO.println(mjono);
    }

    for (String mjono : varit) {
        IO.println(mjono);
    }
}
```


Huomaa ainakin nämä erot Javan, C# ja Pythonin välillä listoja käytettäessä:

| Toiminto                    | Java                 | C#                     | Python            |
| --------------------------- | -------------------- | ---------------------- | ----------------- |
| Lukeminen tietystä paikasta | list.get(indeksi)    | list[indeksi]          | list[indeksi]     |
| Listan koko                 | list.size()          | list.Count             | len(list)         |
| Poistaminen                 | list.remove(indeksi) | list.RemoveAt(indeksi) | list.pop(indeksi) |


Muista metodeista voi lukea dokumentaatiosta: <https://docs.oracle.com/javase/8/docs/api/java/util/List.html>


## Vahva ja staattinen tyypitys

Java on vahvasti ja staattisesti tyypitetty kieli. *Vahva tyypitys* tarkoittaa, että Java valvoo tiukasti tyyppisääntöjen noudattamista eikä salli mielivaltaisia tyyppien välisiä sekoituksia. Eri tietotyyppejä ei voi käyttää toistensa sijaan, ellei kieli nimenomaisesti salli sitä. Esimerkiksi totuusarvoa (boolean) ei voi käyttää lukuarvona, eikä viitetyyppistä arvoa voi käsitellä kokonaislukuna. Jos ohjelmoija yrittää rikkoa näitä sääntöjä, seurauksena on käännösvirhe. Esimerkki alla.

```java,editable
void main() {
  long sairaanIsoLuku = 40000000000L;
  IO.println("Iso, long-tyyppinen luku: " +sairaanIsoLuku);
  // int normaaliIntti = sairaanIsoLuku; // Ei onnistu, koska vahva tyypitys
  int katkaistu = (int)sairaanIsoLuku;
  IO.println("int-luku eksplisiittisen tyyppimuunnoksen jälkeen: " + katkaistu);
}
```

Yllä olevassa esimerkissä käytännössä otetaan `long`-luvun 32 oikeanpuoleisinta bittiä ja sijoitetaan ne `int`-tyyppiseen muuttujaan. Tämä on mahdollista siksi, että ohjelmoija on nimenomaisesti ("eksplisiittisesti") pyytänyt tyyppimuunnosta. Ilman eksplisiittistä tyyppimuunnosta kääntäjä antaisi virheen. 

Vahva tyypitys vähentää virheellisten oletusten mahdollisuutta ja parantaa ohjelman luotettavuutta. Tämä on selkeä ero heikosti tyypitettyihin kieliin, kuten JavaScriptiin, jossa vaikkapa `1 + true` palauttaa `2`. 

*Staattinen tyypitys* tarkoittaa, että muuttujien tyypit määräytyvät käännösaikana, ei ohjelman ajon aikana. Jos yrität sijoittaa muuttujaan väärän tyyppistä tietoa, ohjelma ei käänny, ja kääntäjä antaa virheilmoituksen. 

Yhdessä staattinen ja vahva tyypitys tarkoittavat Javassa sitä, että ohjelman tyyppivirheet pyritään estämään jo ennen ohjelman suorittamista. Kääntäjä toimii eräänlaisena turvaverkkona, joka varmistaa, että arvot, muuttujat ja operaatiot ovat keskenään yhteensopivia.