# Comparable-rajapinta ja luonnollinen järjestys

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

Esimerkiksi `Integer`-tyyppi toteuttaa `Comparable`-rajapinnan
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
  <task-title>Tehtävä 4.5: Miksi Comparable. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-5-miksi-comparable/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa4/tehtava5">Tee tehtävä TIMissä</a></task-link>
</task>

## Oma toteutus Comparable-rajapinnalle

Kokeillaan `Comparable`-rajapinnan toteuttamista omassa luokassamme.

Otetaan esimerkiksi luokka `Kerailykortti`, joka mallintaa eräässä
keräilypelissä käytettäviä kortteja. Meidän keräilykortti sisältää alkuun vain
keräilykortin nimen ja yksilöivän, ykkösestä alkavan tunnistenumeron:

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

Virheilmoitus on vähintäänkin kryptinen. Yksinkertaistetusti virhe johtuu
perimmäisesti siitä, että `Collections.sort()` ei voi meidän puolestamme arvata,
mikä on `Kerailykortti`-olioiden luonnollinen järjestys. Onko se kenties kortin
nimen aakkosjärjestys vai kenties numerotunnisteen mukainen nouseva järjestys?
Vastataksemme tähän kysymykseen meidän täytyy toteuttaa `Comparable`-rajapinta
`Kerailykortti`-luokalle.

Kun lähdemme toteuttamaan `Comparable`-rajapintaa keräilykortille, joudumme heti
pohtimaan, mikä on luonnollinen järjestys keräilykorteillemme. Esimerkiksi
aakkosjärjestys nimen mukaan voi olla hyödyllinen. Toisaalta koska korteilla on
numeeriset ykkösestä alkavat numerotunnisteet, numerojärjestys tunnisteen mukaan
voidaan myös mieltää luonnollisemman tuntuiseksi ja yhtälailla tarpeelliseksi.
Luonnollista järjestystä valittaessa on lisäksi syytä pohtia kohdealueen ja
sovelluksen tarpeen — mitä luokkaa käyttäjät muut ohjelmoijat tai sovelluksen
lopulliset käyttäjät kaipaavat tai olettavat keräilykorttien
oletusjärjestyksestä?

Päättäkäämme tämän esimerkin puiteissa, että järjestys yksilöllisen tunnisteen
mukaan on tässä tapauksessa järkevin luonnollinen järjestys.
Toteutetaan tällä pohjustuksella `Comparable`-rajapinta siten, että kortit
järjestetään numerotunnisteen mukaan. Tätä varten tarvitsemme rajapinnan
toteutuksen luokan määrittelyyn sekä toteutuksen edellä mainitulle
`compareTo`-metodille.

Käytämme toteutuksessa luvun alussa olevaa [palautustaulukkoa](#comparable-rajapinta-ja-luonnollinen-järjestys):

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

`Comparable` on niin sanottu *geneerinen rajapinta*, eli se ei itsessään kerro
minkä tyyppisiin olioihin vertailu kohdistuu. 
Käsittelemme geneeristä ohjelmointia tarkemmin [osassa
4.4](04-tyyppiparametrit-ja-geneerisyys.md).
Tästä syystä `Comparable`-rajapinnan toteuttamisessa meidän täytyy kertoa minkä
tyypin olioille luonnollinen järjestys määritellään. Tässä tapauksessa toteutamme
järjestyksen keräilykorteille, joten määrittelemme `implements Comparable<Kerailykortti>`. 

## Valmiiden vertailumetodien käyttö

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

## Useamman attribuutin vertailu

Monesti luonnollinen järjestys voi määräytyä useamman luokan attribuutin
mukaan.

Mitä jos kohdealueen kannalta nyt olisikin järkevämpi, että kortit
järjestetäänkin ensin aakkosjärjestyksen ja sitten vasta numerotunnisteen
mukaan?
Tätä varten meidän
täytyy muuttaa `compareTo`-metodia siten, että ensin verrataan `nimi`
aakkosjärjestyksen mukaan käyttäen `String`-luokan omaa `compareTo`-metodia.
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
        int nimiVertailu = this.nimi.compareTo(other.nimi);
        if (nimiVertailu != 0) {
            return nimiVertailu;
        }
        return Integer.compare(this.tunnistenumero, other.tunnistenumero);
        // HIGHLIGHT_GREEN_END
    }

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

## Tehtävät


<task>
  <task-title>Tehtävä 4.6: Henkilöt järjestykseen, osa 1. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-6-henkilot-jarjestykseen-1/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa4/tehtava6">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 4.7: Henkilöt järjestykseen, osa 2. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-7-henkilot-jarjestykseen-2/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa4/tehtava7">Tee tehtävä TIMissä</a></task-link>
</task>

