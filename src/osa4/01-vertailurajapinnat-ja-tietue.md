# Vertailurajapinnat ja tietue

> [!Osaamistavoitteet]
>
> - Ymmärrät vertailurajapintojen merkityksen Javassa
> - Osaat hyödyntää vertailurajapintoja itsetehtyjen tyyppien järjestämiseen
>   kokoelmissa

## Vertailurajapinnat

<!-- Seuraavaksi tutustumme kahteen Javan valmiiseen vertailurajapintaan, [`Comparable`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Comparable.html):en sekä [`Comparator`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Comparator.html):iin. Nämä rajapinnat nimiensä mukaisesti ("vertailtava" ja "vertailija") tarjoavat yhteisen toiminnallisuuden olioiden järjestämiseen Javan valmiilla järjestysmenetelmillä, kuten Javan `Collections.sort`-metodilla. -->

Osan 3 luvussa 3.2 huomasimme, että olioiden yhtäsuuruus voidaan 
tarkistaa `Object`-luokan `equals`-metodilla.
Yhtäsuuruuden tarkistuksen lisäksi on mielekästä *vertailla* 
olioita yleisemmin. 
Seuraavaksi käymme läpi paria valmista Javan rajapintaa, nimittäin
`Comparable`- ja `Comparator`-rajapintoja, jotka tarjoavat jaetun toteutuksen
olioiden vertailuun ja järjestämiseen.

### Comparable-rajapinta ja luonnollinen järjestys

Rajapinta
[`Comparable`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Comparable.html)
määrittelee metodin `compareTo`, jonka avulla luokan olioille voi määrittää oman
_luonnollisen_ järjestyksensä suhteessa toiseen olioon.

Rajapinnan ainoa metodi `compareTo` palauttaa kokonaisluvun, joka ilmaisee olion
_järjestyksen_ suhteessa toiseen olioon:

| Tapaus                        | Merkitys         | Tulkinta                           |
| ----------------------------- | ---------------- | ---------------------------------- |
| `olioA.compareTo(olioB) < 0`  | `olioA < olioB`  | `olioA` on pienempi kuin `olioB`   |
| `olioA.compareTo(olioB) == 0` | `olioA == olioB` | `olioA` on yhtä suuri kuin `olioB` |
| `olioA.compareTo(olioB) > 0`  | `olioA > olioB`  | `olioA` on suurempi kuin `olioB`   |

Esimerkikiksi `Integer`-tyyppi toteuttaa `Comparable`-rajapinnan
`Integer`-olioille, eli kaksi kokonaislukuoliota voidaan vertailla
keskenään `compareTo`-metodilla.

```java
void main() {
  Integer luku1 = 5;
  Integer luku2 = 18;
  int tulos = luku1.compareTo(luku2);

  // Tulostaa negatiivisen arvon (< 0), koska 5 < 18
  IO.println("luku1.compareTo(luku2): " + tulos);
}
```

Luonnollisella järjestyksellä tarkoitetaan ihmisjärjen mukaisesti olion tyypille
ominaista ja intuitiivista järjestystä. 
Esimerkiksi merkkijonoille on Javassa luonnollinen järjestys määritelty
aakkosjärjestyksenä: 

```java
// Apufunktio, joka tulostaa kahden merkkijonon välisen järjestyksen
void kerroJarjestys(String sana1, String sana2) {
  int tulos = sana1.compareTo(sana2);
  if (tulos < 0) {
      IO.println("Merkkijono '" + sana1 + "' on järjestyksessä ennen merkkijonoa '" + sana2 + "'");
  } else if (tulos > 0) {
      IO.println("Merkkijono '" + sana1 + "' on järjestyksessä merkkijonon '" + sana2 + "' jälkeen");
  } else {
      IO.println("'" + sana1 + " on yhtä suuri kuin '" + sana2 + "'");
  }
}

void main() {
  String sana1 = "omena";
  String sana2 = "appelsiini";
  String sana3 = "banaani";
  kerroJarjestys(sana1, sana2);
  kerroJarjestys(sana1, sana3);
  kerroJarjestys(sana2, sana3);
}
```

Vastaavasti `Integer`-luokalla on toteutus `Comparable`-rajapinnalle, joka
kertoo kokonaislukujen luonnollisen järjestyksen, joka on suuruusjärjestys.

```java
//-int kerroJarjestys(Integer luku1, Integer luku2) {
//-  int tulos = luku1.compareTo(luku1);
//-  if (tulos < 0) {
//-      IO.println(luku1 + " on pienempi kuin " + luku2);
//-  } else if (tulos > 0) {
//-      IO.println(luku1 + " on suurempi kuin " + luku2);
//-  } else {
//-      IO.println(luku1 + " on yhtä suuri kuin " + luku2);
//-  }
//-  return tulos;
//-}
//-
void main() {
  Integer luku1 = 5;
  Integer luku2 = 18;
  Integer luku3 = 5;
  kerroJarjestys(luku1, luku2);
  kerroJarjestys(luku1, luku3);
  kerroJarjestys(luku2, luku3);
}
```

Olennainen `Comparable`-rajapinnan hyöty on, että voimme kirjoittaa
ohjelmia ja käyttää vertailuja vaativia algoritmeja, jotka toimivat
yleisesti kaikille olioille, jotka toteuttavat `Comparable`-rajapinnan.
Esimerkiksi voimme käyttää Javan valmiita
kokoelmien järjestämistoteutuksia, kuten esimerkiksi
[`Collections.sort`](<https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Collections.html#sort(java.util.List)>)-metodia.
Näin saamme järjestettyä kokoelmia helposti ilman, että meidän tarvitsee itse
kirjoittaa järjestämisalgoritmeja jokaiselle luokalle erikseen.

```java
void main() {
    List<Integer> numerot = Arrays.asList(18, 5, 42);
    List<String> hedelmat = Arrays.asList("omena",  "päärynä", "appelsiini");
    IO.println(numerot); // [18, 5, 42]
    IO.println(hedelmat); // [omena, päärynä, appelsiini]

    // Järjestetään listat alkioiden luontaisen järjestyksen mukaan
    Collections.sort(hedelmat);
    Collections.sort(numerot);

    IO.println(numerot); // [5, 18, 42]
    IO.println(hedelmat); // [appelsiini, omena, päärynä]
}
```

<details closed><summary>Ekstra: <code>Collections</code>-luokka</summary>

[`Collections`](https://docs.oracle.com/en/java/javase/25/docs/api//java.base/java/util/Collections.html)
on Javan valmis luokka, joka tarjoaa yllämainitun `sort`-metodin lisäksi monia
yleishyödyllisiä metodeja Javan _kokoelmille_. 
Kokoelma on Javassa käytetty yleistys alkioita sisältäville tietorakenteille,
kuten taulukoille, listoille ja sanakirjoille.

Käsittelemme kokoelmia tarkemmin [osassa 5](../osa5/index.md).
Voit kuitenkin halutessasi tutkia jo `Collections`-luokkaa, joka
sisältää yleispäteviä metodeja kokoelmien käsittelyyn. 
Mikäli katsot linkin, varaudu, että se sisältää paljon vasta myöhemmin 
käsiteltävää syntaksia.

Monet `Collections`-luokan metodit perustuvat siihen, että kokoelman alkiot toteuttavat erilaisia
rajapintoja, kuten edellä mainittu `Comparable`. Yhdistämällä Javan
kokoelmille ja alkioille tarkoitettuja rajapintoja
onkin mahdollista kirjoittaa hyvin yleisiä algoritmeja, jotka toimivat
riippumatta siitä, onko parametrina lista numeroita tai vaikkapa
taulukko opiskelijoita.

<!-- Javan kokoelmille taas on olemassa rajapinta
[`Collection`](https://docs.oracle.com/en/java/javase/25/docs/api//java.base/java/util/Collection.html),
joka määrittelee yleisiä toimintoja kokoelmille, kuten lisäämisen, poistamisen
ja tarkistamisen, tai onko tietty alkio kokoelmassa.

Lisäksi Javasta löytyy vielä
[`AbstractCollection`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/AbstractCollection.html)-luokka
helpottamaan `Collection`-rajapinnan toteuttamista. Abstrakti luokka
`AbstractCollection` nimittäin tarjoaa valmiin toteutuksen monista
`Collection`-rajapinnan metodeista, jolloin rajapinnan toteuttamiseksi riittää
periä `Collection` ja kirjoittaa toteutus vain osalle metodeista. -->

</details>

<task>
  <task-title>Tehtävä 4.1: Miksi Comparable? <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-1-miksi-comparable/handout.md}}

  </handout>
  
  <task-link>
<a
  href="https://tim.jyu.fi/view/kurssit/tie/itkp102/demot/demo1#tehtava_tulostaminen_header">Tee
  tehtävä TIMissa</a>
  </task-link>
  
</task>


### Oma toteutus Comparable-rajapinnalle

Kokeillaan `Comparable`-rajapinnan toteuttamista omassa luokassamme.

Otetaan esimerkiksi luokka `Kerailykortti`, joka mallintaa eräässä
keräilypelissä käytettäviä kortteja.
Meidän keräilykorttti sisältää alkuun vain keräilykortin 
nimen ja yksilöivän, ykkösestä alkavan tunnistenumeron:

```java
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private int tunnistenumero;

    public Kerailykortti(String nimi, int tunnistenumero) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
    }

    @Override
    public String toString() {
        return "Kortti: " + nimi + " (#" + tunnistenumero + ")";
    }
}
// FILE_END
// FILE: main.java
void main() {
    List<Kerailykortti> kortit = List.of(
        new Kerailykortti("Loistava Lohikäärme", 3),
        new Kerailykortti("Aloittelijan Ameeba", 1),
        new Kerailykortti("Mieletön Merihevonen", 2)
    );

    for (Kerailykortti kortti : kortit) {
        IO.println(kortti);
    }
}
// FILE_END
```

Mikäli nyt yritämme järjestää `Kerailykortti`-olioita
`Collections.sort()`-metodilla, saamme käännöksenaikaisen virheen,
koska se ei toteuta `Comparable`-rajapintaa: 

```java,ignore
// FILE: main.java
void main() {
    List<Kerailykortti> kortit = Arrays.asList(
        new Kerailykortti("Loistava Lohikäärme", 3),
        new Kerailykortti("Aloittelijan Ameeba", 1),
        new Kerailykortti("Mieletön Merihevonen", 2)
    );

    IO.println("Ennen järjestämistä:");
    for (Kerailykortti kortti : kortit) {
        IO.println(kortti);
    }

    Collections.sort(kortit);

    IO.println();

    IO.println("Jälkeen järjestämisen:");
    for (Kerailykortti kortti : kortit) {
        IO.println(kortti);
    }
}
// FILE_END
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private int tunnistenumero;

    public Kerailykortti(String nimi, int tunnistenumero) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
    }

    @Override
    public String toString() {
        return "Kortti: " + nimi + " (#" + tunnistenumero + ")";
    }
}
// FILE_END
```

```
main.java:11: error: no suitable method found for sort(List<Kerailykortti>)
    Collections.sort(kortit);
```

Virheilmoitus on vähintäänkin kryptinen.
Yksinkertaistetusti virhe johtuu perimmäisesti siitä, että
`Collections.sort()` ei voi meidän puolestamme arvata, mikä on
`Kerailykortti`-olioiden luonnollinen järjestys. 
Onko se kenties kortin nimen
aakkosjärjestys vai kenties numerotunnisteen mukainen nouseva järjestys?
Vastataksemme tähän kysymykseen meidän täytyy toteuttaa `Comparable`-rajapinta
`Kerailykortti`-luokalle.

Kun lähdemme toteuttamaan `Comparable`-rajapintaa keräilykortille, joudumme heti
pohtimaan, mikä on luonnollinen järjestys keräilykorteillemme.
Esimerkiksi aakkosjärjestys nimen mukaan voi olla hyödyllinen.
Toisaalta koska korteilla on numeeriset ykkösestä alkavat
numerotunnisteet, numerojärjestys tunnisteen mukaan voidaan myös
mieltää luonnollisemman tuntuiseksi ja yhtälailla tarpeelliseksi.
Luonnollista järjestystä valittaessa on lisäksi syytä
pohtia kohdealueen ja sovelluksen tarpeen — mitä luokkaa käyttäjät 
muut ohjelmoijat tai sovelluksen lopulliset käyttäjät kaipaavat
tai olettavat keräilykorttien oletusjärjestyksestä?

Päättäkäämme tämän esimerkin puiteissa, että järjestys yksilöllisen tunnisteen
mukaan on tässä tapauksessa järkevin luonnollinen järjestys.
Toteutetaan tällä pohjustuksella `Comparable`-rajapinta siten, että kortit
järjestetään numerotunnisteen mukaan. Tätä varten tarvitsemme rajapinnan
toteutuksen luokan määrittelyyn sekä toteutuksen edellä mainitulle
`compareTo`-metodille.

Käytämme toteutuksessa luvun alussa olevaa [palautustaulukkoa](#comparator-rajapinta):

```java
// FILE: Kerailykortti.java
// HIGHLIGHT_GREEN_BEGIN
class Kerailykortti implements Comparable<Kerailykortti> {
// HIGHLIGHT_GREEN_END
    private String nimi;
    private int tunnistenumero;

    public Kerailykortti(String nimi, int tunnistenumero) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
    }

    // HIGHLIGHT_GREEN_BEGIN
    @Override
    public int compareTo(Kerailykortti other) {
        if (tunnistenumero > other.tunnistenumero) {
            return 1;
        }
        if (tunnistenumero < other.tunnistenumero) {
            return -1;
        }
        return 0;
    }
    // HIGHLIGHT_GREEN_END

    @Override
    public String toString() {
        return "Kortti: " + nimi + " (#" + tunnistenumero + ")";
    }
}
// FILE_END
// FILE: main.java
void main() {
    List<Kerailykortti> kortit = Arrays.asList(
        new Kerailykortti("Loistava Lohikäärme", 3),
        new Kerailykortti("Aloittelijan Ameeba", 1),
        new Kerailykortti("Mieletön Merihevonen", 2)
    );

    IO.println("Ennen järjestämistä:");
    for (Kerailykortti kortti : kortit) {
        IO.println(kortti);
    }

    Collections.sort(kortit);

    IO.println();

    IO.println("Jälkeen järjestämisen:");
    for (Kerailykortti kortti : kortit) {
        IO.println(kortti);
    }
}
// FILE_END
```

Huomaa, että `implements Comparable<Kerailykortti>`-osa luokan määrittelyssä
tulee kertoa minkä tyypin olioille luokka tarjoaa luonnollisen järjestyksen, samalla
tavoin kuin listalle kerrotaan minkätyyppisiä olioita lista sisältää (tyylillä
`List<Kerailykortti>`). Tähän on yleensä helppo valita suoraan luokan oma tyyppi
ellei ole erityistä syytä valita sen sijaan esimerkiksi yliluokkaa.
Toisaalta tämä myös tarkoittaa erityisesti, että samalle luokalle voi 
toteuttaa useita eri `Comparable<T>`-rajapintoja, jossa `T` on mikä tahansa muu
tyyppi.

### Valmiiden vertailumetodien käyttö

Yllä olevassa tapauksessa toteutimme `compareTo`-metodin käyttäen suoraan
`Comparable`-rajapinnan määritelmää.
Kuitenkin Javan valmiit tyypit useimmiten tarjoavat jo
valmiita vertailumetodeja, joita voi hyödyntää `Comparable`-rajapinnan toteuttamiseksi.

Esimerkiksi `int`-kokonaisluvuille Java tarjoaa valmiin `Integer.compare`-metodin 
([JavaDoc]()), jolla `Kerailykortti`-luokan `compareTo`-metodin toteutus
voidaan yksinkertaistaa yhden rivin funktioksi:

```java
class Kerailykortti implements Comparable<Kerailykortti> {
    private String nimi;
    private int tunnistenumero;

    public Kerailykortti(String nimi, int tunnistenumero) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
    }

    @Override
    public int compareTo(Kerailykortti other) {
        // HIGHLIGHT_GREEN_BEGIN
        return Integer.compare(tunnistenumero, other.tunnistenumero);
        // HIGHLIGHT_GREEN_END
    }
 
    @Override
    public String toString() {
        return "Kortti: " + nimi + " (#" + tunnistenumero + ")";
    }
}
//-
//-void main() {
//-    List<Kerailykortti> kortit = Arrays.asList(
//-        new Kerailykortti("Loistava Lohikäärme", 3),
//-        new Kerailykortti("Aloittelijan Ameeba", 1),
//-        new Kerailykortti("Mieletön Merihevonen", 2)
//-    );
//-
//-    IO.println("Ennen järjestämistä:");
//-    IO.println(kortit);
//-
//-    Collections.sort(kortit);
//-
//-    IO.println("Jälkeen järjestämisen:");
//-    IO.println(kortit);
//-}
```

Toteuttaessa `Comparable`-rajapintaa itse tehdyille luokille onkin syytä suosia 
valmiita vertailumetodeja ja niiden yhdistämistä.
Esimerkiksi `Integer.compare` osaa käsitellä kaikkia erikoistapauksia,
kuten lukualueen ylivuotoja. Vastaavasti `Double.compare` osaa
käsitellä kaikkia liukulukutyyppien erikoisarvoja, kuten äärettömyyttä tai
"Not a Number" -arvoja.

<task>
  <task-title>Tehtävä 4.2: Henkilöt järjestykseen, osa 1 <points>0,5 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-2-henkilöt-järjestykseen/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/itkp102/demot/demo1#tehtava_tulostaminen_header">Tee tehtävä TIMissa</a></task-link>
</task>


### Useamman attribuutin vertailu

Monesti luonnollinen järjestys voi määräytyä useamman luokan attribuutin
mukaan.

Mitä jos kohdealueen kannalta nyt olisikin järkevämpi, että kortit
järjestetäänkin ensin aakkosjärjestyksen ja sitten vasta numerotunnisteen
mukaan?
Tätä varten meidän
täytyy muuttaa `compareTo`-metodia siten, että ensin verrataan `nimi`
aakkosjärejstyksen mukaan käyttäen `String`-luokan omaa `compareTo`-metodia.
Jos merkkijonot ovat samat (eli `compareTo` palauttaa `0`), tehdään vertailu
`tunnistenumero`-attribuutille:

```java
// FILE: Kerailykortti.java
class Kerailykortti implements Comparable<Kerailykortti> {
    private String nimi;
    private int tunnistenumero;

    public Kerailykortti(String nimi, int tunnistenumero) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
    }

    @Override
    public int compareTo(Kerailykortti other) {
        // HIGHLIGHT_GREEN_BEGIN
        int sarjaVertailu = this.sarja.compareTo(other.sarja);
        if (sarjaVertailu != 0) {
            return sarjaVertailu;
        }
        return Integer.compare(this.tunnistenumero, other.tunnistenumero);
        // HIGHLIGHT_GREEN_END
    }

    @Override
    public String toString() {
        return "Kortti: " + nimi + " (Sarja: " + sarja + ", #" + tunnistenumero + ")";
    }
}
// FILE_END
// FILE: main.java
void main() {
    List<Kerailykortti> kortit = Arrays.asList(
        new Kerailykortti("Loistava Lohikäärme", 3),
        new Kerailykortti("Aloittelijan Ameeba", 1),
        new Kerailykortti("Mieletön Merihevonen", 2)
    );

    IO.println("Ennen järjestämistä:");
    for (Kerailykortti kortti : kortit) {
        IO.println(kortti);
    }

    Collections.sort(kortit);

    IO.println();

    IO.println("Jälkeen järjestämisen:");
    for (Kerailykortti kortti : kortit) {
        IO.println(kortti);
    }
}
// FILE_END
```


<task> 
<task-title>
Tehtävä 4.3: Henkilöt järjestykseen, osa 2. 
<points>0.5 p.</points> 
</task-title> 
  
  <handout>

{{#include ../exercises/4-3-henkilöt-järjestykseen-2/handout.md}}

  </handout> 
  
<task-link>
<a
  href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä
TIMissä</a>
</task-link> 

</task>

### Comparator-rajapinta

Kuten totesimme ylempänä, toisinaan voi olla vaikeaa valita yksittäinen
järkevä järjestys. 
Yleisestikin, luonnollisen järjestyksen lisäksi voi olla järkevää
pystyä määrittämään *vaihtoehtoisia* järjestystapoja samalla luokalle.

Esimerkiksi, vaikka kokonaislukujen suuruusjärjestys on järkevä luonnolliseksi
järjestykselle, joskus lukuja saatetaan haluta järjestää niiden suuruusluokan
mukaan tai vaikkapa sen mukaan, kuinka lähellä luvut ovat lähellä jotakin toista 
tiettyä lukua. Vastaavasti, vaikka yllä oleville keräilykorteille voisi olla
järkevää määrätä järjestys tunnisteen mukaan, voi olla mielekästä
pystyä järjestämään niitä kortin nimen mukaan.

Javan `Comparator`-rajapinta
[JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Comparator.html)
tarjoaa tavan määrittää *vaihtoehtoisia* järjestystapoja tyypeille.
Liäksi rajapinta tarjoaa mahdollisuuden määrittää järjestystapoja
ilman, että alkuperäisen luokan tarvitsisi toteuttaa `Comparable`-rajapintaa.

Rajapinta sisältää ainoastaan yhden pakollisen metodin `compare`, joka
ottaa parametriksi kaksi samantyyppistä oliota ja palauttaa 
vertailuluvun samoilla säännöillä kuin `Comparable`-rajapinnan `compareTo`:

| Tapaus                             | Merkitys         | Tulkinta                           |
| ---------------------------------- | ---------------- | ---------------------------------- |
| `cmp.compareTo(olioA, olioB) < 0`  | `olioA < olioB`  | `olioA` on pienempi kuin `olioB`   |
| `cmp.compareTo(olioA, olioB) == 0` | `olioA == olioB` | `olioA` on yhtä suuri kuin `olioB` |
| `cmp.compareTo(olioA, olioB) > 0`  | `olioA > olioB`  | `olioA` on suurempi kuin `olioB`   |


Laajenetaan hieman `Kerailykortti`-luokkaa lisäämällä attribuutti
`sarja`, joka kuvaa korttisarjaa (esim. eläimet, ajoneuvot, jne.):


```java,
class Kerailykortti implements Comparable<Kerailykortti> {
    private String nimi;
    // HIGHLIGHT_GREEN_BEGIN
    private String sarja;
    // HIGHLIGHT_GREEN_END
    private int tunnistenumero;
    
    // HIGHLIGHT_GREEN_BEGIN
    public Kerailykortti(String nimi, String sarja, int tunnistenumero) {
    // HIGHLIGHT_GREEN_END
        this.nimi = nimi;
    // HIGHLIGHT_GREEN_BEGIN
        this.sarja = sarja;
    // HIGHLIGHT_GREEN_END
        this.tunnistenumero = tunnistenumero;
    }
//-
//-    @Override
//-    public int compareTo(Kerailykortti other) {
//-        int sarjaVertailu = this.sarja.compareTo(other.sarja);
//-        if (sarjaVertailu != 0) {
//-            return sarjaVertailu;
//-        }
//-        return Integer.compare(this.tunnistenumero, other.tunnistenumero);
//-    }
//-    
//-    public String getNimi() {
//-        return nimi;
//-    }
//-
//-    public String getSarja() {
//-        return sarja;
//-    }
//-    
//-
//-    @Override
//-    public String toString() {
//-        return "Kortti: " + nimi + " (Sarja: " + sarja + ", #" + tunnistenumero + ")";
//-    }
//-}
//-
//-void main() {
//-    List<Kerailykortti> kortit = Arrays.asList(
//-        new Kerailykortti("Loistava Lohikäärme", "Eläimet", 3),
//-        new Kerailykortti("Vauhdikas Vespajetti", "Ajoneuvot", 1),
//-        new Kerailykortti("Aloittelijan Ameeba", "Eläimet", 1),
//-        new Kerailykortti("Mieletön Merihevonen", "Eläimet", 2),
//-        new Kerailykortti("Nopea Nopsa", "Ajoneuvot", 2)
//-    );
//-
//-    IO.println("Ennen järjestämistä:");
//-    for (Kerailykortti kortti : kortit) {
//-        IO.println(kortti);
//-    }
//-
//-    Collections.sort(kortit);

//-    IO.println();
//-
//-    IO.println("Jälkeen järjestämisen:");
//-    for (Kerailykortti kortti : kortit) {
//-        IO.println(kortti);
//-    }
//-}
```

Tällä hetkellä keräilykorteille on määritelty luonnollinen järjestys siten, että
ensin keräilykortit järjestetään nimen ja sitten tunnisteen mukaan.
Haluaisimme kuitenkin tarjota vaihtoehtoisen tavan järjestää keräilykortteja
sarjan nimen mukaan.
Tätä varten voimme luoda uuden vertailuluokan, joka toteuttaa
`Comparator`-rajapinnan:

```java
// FILE: KerailykorttiVertailuSarajanMukaan.java
import java.util.Comparator;

class KerailykorttiSarjaVertailija implements Comparator<Kerailykortti> {
    @Override
    public int compare(Kerailykortti kortti1, Kerailykortti kortti2) {
        return kortti1.getSarja().compareTo(kortti2.getSarja());
    }
}
// FILE_END
// FILE: Kerailykortti.java
class Kerailykortti implements Comparable<Kerailykortti> {
    private String nimi;
    private String sarja;
    private int tunnistenumero;
    
    public Kerailykortti(String nimi, String sarja, int tunnistenumero) {
        this.nimi = nimi;
        this.sarja = sarja;
        this.tunnistenumero = tunnistenumero;
    }

    // HIGHLIGHT_GREEN_BEGIN
    public String getSarja() {
        return sarja;
    }
    // HIGHLIGHT_GREEN_END

    @Override
    public int compareTo(Kerailykortti other) {
        int sarjaVertailu = this.sarja.compareTo(other.sarja);
        if (sarjaVertailu != 0) {
            return sarjaVertailu;
        }
        return Integer.compare(this.tunnistenumero, other.tunnistenumero);
    }

    @Override
    public String toString() {
        return "Kortti: " + nimi + " (Sarja: " + sarja + ", #" + tunnistenumero + ")";
    }
}
// FILE_END
// FILE: main.java
void main() {
    List<Kerailykortti> kortit = Arrays.asList(
        new Kerailykortti("Loistava Lohikäärme", "Eläimet", 3),
        new Kerailykortti("Vauhdikas Vespajetti", "Ajoneuvot", 1),
        new Kerailykortti("Aloittelijan Ameeba", "Eläimet", 1),
        new Kerailykortti("Mieletön Merihevonen", "Eläimet", 2),
        new Kerailykortti("Nopea Nopsa", "Ajoneuvot", 2)
    );

    IO.println("Ennen järjestämistä:");
    for (Kerailykortti kortti : kortit) {
        IO.println(kortti);
    }

    // HIGHLIGHT_GREEN_BEGIN
    KerailykorttiSarjaVertailija vertailija = new KerailykorttiSarjaVertailija();
    Collections.sort(kortit, vertailija);
    // HIGHLIGHT_GREEN_END

    IO.println();

    IO.println("Jälkeen järjestämisen:");
    for (Kerailykortti kortti : kortit) {
        IO.println(kortti);
    }
}
// FILE_END
```

Huomaa erityisesti, että:

- Vaihtoehtoinen vertailu on nyt toteutettu omaan luokkaan `KerailykorttiSarjaVertailija`.
  Tämä on tarkoituksellista ja se mahdollistaa, että vertailijoita voi tehdä
  myös sellaisille luokille, jonka koodia ei voi suoraan muokata (esim.
  Javan sisäänrakennetut luokat).
- Koska `KerailykorttiSarjaVertailija` on oma luokkansa, määritimme `Kerailykortti`-luokkaan
  saantimetodin `getSarja()`.
- Jotta vertailijaa voi käyttää, siitä tulee alustaa olio. Alustuksen jälkeen
  vertailijaolio voidaan käyttää `Collections.sort`-metodin ylikuormituksen
  kanssa, joka joka ottaa `Comparator`-olion toisena parametrina.

> [!VAROITUS]
>
> Yllä olevasa esimerkissä toteutimme `Comparator`-rajapinnan luokassa, jotta esimerkki
> voidaan pitää yksinkertaisena.
> 
> Modernissa Java on kuitenkin yleistä, että *vertailuluokkia ei luoda käsin*.
> `Comparator` on nimittäin ns. *funktiorajapinta*, jonka ansiosta mikä tahansa
> luokkametodi, jonka määrittely vastaa `compare`-metodia voidaan sijoittaa
> suoraan `Comparator`-tyyppiseen muuttujaan tekemättä luokkaa:
>
> ```java
> //-void main() {
> List<Integer> luvut = new ArrayList<>(List.of(5, 4, 2, 1, 3));
> Comparator<Integer> vertailija = Integer::compare;
> Collections.sort(luvut, vertailija);
> IO.println(luvut);
> //-}
> ```
>
> Tutustumme funktiorajapintoihin ja palaamme taas `Comparator`-tyyppiin tarkemmin
> [osassa 6](../osa6/index.md).
 
`Comparator`-rajapinta tarjoaa lisäksi muutaman hyödyllisen metodin, jotka
auttavat algoritmien suunnittelussa.

`Comparator.naturalOrder()` palauttaa `Comparator`-tyyppisen vertailuolion,
joka järjestää oliot niiden *luonnollisen järjestyksen* mukaan.
Toisin sanoin, tämä mahdollistaa ns. eristää `Comparable`-rajapintaa
toteuttavan olion `compareTo`-metodin toteutuksen vertailuolioksi.
Esimerkiksi merkkijonojen aakkosjärjestystä vastaavan vertailuolion saa tälla
tavoin:

```java
void main() {
    List<String> jonoja = new ArrayList<>(List.of("Denis", "Antti-Jussi", "Karri", "Rauli", "Sami"));
    Comparator<String> aakkosjarjestys = Comparator.naturalOrder();
    Collections.sort(jonoja, aakkosjarjestys);
    IO.println(jonoja);
}
```

`Comparator.reversed()` luo uuden vertailuolion, joka kääntää
vertailujärjestyksen.
Tämän avulla esimerkiksi pystyy helposti järjestämään merkkijonot
käänteiseen aakkosjärjestykseen:

```java
void main() {
    List<String> jonoja = new ArrayList<>(List.of("Denis", "Antti-Jussi", "Karri", "Rauli", "Sami"));
    Comparator<String> aakkosjarjestys = Comparator.naturalOrder();
    // HIGHLIGHT_GREEN_BEGIN
    Comparator<String> kaanteinenAkkosjarjestys = aakkosjarjestys.reversed();
    // HIGHLIGHT_GREEN_END
    Collections.sort(jonoja, kaanteinenAkkosjarjestys);

    IO.println(jonoja);
}
```

Kun olioita vertailee käyttäen luonnollista tai vaihtoehtoista järjestystä,
ei voi olla varma siitä, että `null`-viite on käsitelty järkevästi
tai ollenkaan.
Esimerkiksi jopa Javassa määritelty `String`-merkkijonojen luonnollinen
järjestys ei käsittele tapausta, jos jompikumpi verrattavista merkijonoista
on `null`:

```java,ignore
//-void main() {
String[] jono = {"Ohjelmointi 1", null,  "Ohjelmointi 2"};
Arrays.sort(jono);
IO.println(Arrays.toString(jono));
//-}
```

```
java.lang.NullPointerException: Cannot invoke "java.lang.Comparable.compareTo(Object)" because "a[runHi]" is null
```

Tätä varten on olemassa `Comparator.nullsFirst()` ja `Comparator.nullsLast()`:
ne ottavat parametriksi vertailuolion ja palauttavat uuden vertailijan,
joka osaa käsitellä `null`-viitteitä. Nimensä mukaan `nullsFirst()`
asettaa `null`-viitteet pienemmäksi kuin muut arvot (ja siten järjestyksessä
ensimmäiseksi), kun taas `nullsLast` asettaa `null`-viitteet suuremmaksi kuin
muut arvot (eli järjestyksessä viimeiseksi):

```java
//-void main() {
String[] jono = {"Ohjelmointi 1", null,  "Ohjelmointi 2"};
Comparator<String> aakkosjarjestys = Comparator.naturalOrder();

Comparator<String> nullitEnsimmaiseksi = Comparator.nullsFirst(aakkosjarjestys);
Arrays.sort(jono, nullitEnsimmaiseksi);
IO.println(Arrays.toString(jono));

Comparator<String> nullitViimeiseksi = Comparator.nullsLast(aakkosjarjestys);
Arrays.sort(jono, nullitViimeiseksi);
IO.println(Arrays.toString(jono));
//-}
```

<task> 

<task-title>
Tehtävä 4.4: Kortit harvinaisuuden mukaan. <points>1 p.</points> </task-title> 

<handout>

{{#include ../exercises/4-4-kortit-comparator/handout.md}}

  </handout> 
  
<task-link>
<a
  href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä TIMissä</a>
</task-link> 

</task>

<!-- ## Tietue (kannattaako esitellä tässä vai mennäänkö vain luokilla?)

DZ: IMO tämä myöhempään osaan, ehkä osa 7?

- Erityinen luokkatyyppi kuten luetelma (enum)
- Ei salli arvojen muuttamista

- Tarjoaa valmiin toteutuksen:
  - yksityinen, lopullinen kenttä jokaiselle tietoelementille
  - getter-metodi jokaiselle kentälle
  - julkinen konstruktori, jolla on vastaava argumentti jokaista kenttää varten
  - equals-metodi, joka palauttaa true, jos oliot ovat samaa luokkaa ja kaikki
    kentät ovat samat
  - hashCode-metodi, joka palauttaa saman arvon, kun kaikki kentät ovat samat
    (ja mahdollisesti muulloinkin — törmäykset ovat mahdollisia)
  - toString-metodi, joka sisältää luokan nimen sekä jokaisen kentän nimen ja
    sen vastaavan arvon

- Miksi Javassa on haluttu tehdä tietue muuttumattomaksi?
- Mitä hyötyä ja mahdollista harmia tästä on? -->
