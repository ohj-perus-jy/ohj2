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
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/itkp102/demot/demo1#tehtava_tulostaminen_header">Tee tehtävä TIMissa</a></task-link>
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

    IO.println(kortit);
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
    IO.println(kortit);

    Collections.sort(kortit);

    IO.println("Jälkeen järjestämisen:");
    IO.println(kortit);
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
    IO.println(kortit);

    Collections.sort(kortit);

    IO.println("Jälkeen järjestämisen:");
    IO.println(kortit);
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

> [!Huomautus] 
>
> Yllä olevassa tapauksessa toteutimme `compareTo`-metodin käyttäen suoraan
> `Comparable`-rajapinnan määritelmää.
> Kuitenkin Javan valmiit tyypit useimmiten tarjoavat jo
> valmiita vertailumetodeja, joita voi hyödyntää `Comparable`-rajapinnan toteuttamiseksi.
>
> Esimerkiksi `int`-kokonaisluvuille Java tarjoaa valmiin `Integer.compare`-metodin 
> ([JavaDoc]()), jolla `Kerailykortti`-luokan `compareTo`-metodin toteutus
> voidaan yksinkertaistaa yhden rivin funktioksi:
>
> ```java
> //-class Kerailykortti implements Comparable<Kerailykortti> {
> //-    private String nimi;
> //-    private int tunnistenumero;
> //-
> //-    public Kerailykortti(String nimi, int tunnistenumero) {
> //-        this.nimi = nimi;
> //-        this.tunnistenumero = tunnistenumero;
> //-    }
> //-
> @Override
> public int compareTo(Kerailykortti other) {
>     return Integer.compare(tunnistenumero, other.tunnistenumero);
> }
> //- 
> //-    @Override
> //-    public String toString() {
> //-        return "Kortti: " + nimi + " (#" + tunnistenumero + ")";
> //-    }
> //-}
> //-
> //-void main() {
> //-    List<Kerailykortti> kortit = Arrays.asList(
> //-        new Kerailykortti("Loistava Lohikäärme", 3),
> //-        new Kerailykortti("Aloittelijan Ameeba", 1),
> //-        new Kerailykortti("Mieletön Merihevonen", 2)
> //-    );
> //-
> //-    IO.println("Ennen järjestämistä:");
> //-    IO.println(kortit);
> //-
> //-    Collections.sort(kortit);
> //-
> //-    IO.println("Jälkeen järjestämisen:");
> //-    IO.println(kortit);
> //-}
> ```
> 
> Toteuttaessa `Comparable`-rajapintaa itse tehdyille luokille onkin syytä suosia 
> valmiita vertailumetodeja ja niiden yhdistämistä.
> Esimerkiksi `Integer.compare` osaa käsitellä kaikkia erikoistapauksia,
> kuten lukualueen ylivuotoja. Vastaavasti `Double.compare` osaa
> käsitellä kaikkia liukulukutyyppien erikoisarvoja, kuten äärettömyyttä tai
> "Not a Number" -arvoja.

<task>
  <task-title>Tehtävä 4.2: Henkilöt järjestykseen, osa 1 <points>0,5 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-2-henkilöt-järjestykseen/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/itkp102/demot/demo1#tehtava_tulostaminen_header">Tee tehtävä TIMissa</a></task-link>
</task>


### Useamman kentän vertailu

Katsotaan vielä hieman monimutkaisempaa tapausta, missä meillä on
keräilykortissa vielä tieto kortin sarjasta (esim. "Eläimet", "Ajoneuvot" jne.).

```java
// FILE: Kerailykortti.java
class Kerailykortti implements Comparable<Kerailykortti> {
    private String nimi;
    // HIGHLIGHT_GREEN_BEGIN
    private String sarja;
    // HIGHLIGHT_GREEN_END
    private int tunnistenumero;

    public Kerailykortti(String nimi, String sarja, int tunnistenumero)
    {
        this.nimi = nimi;
        this.sarja = sarja;
        this.tunnistenumero = tunnistenumero;
    }

    @Override
    public int compareTo(Kerailykortti other) {
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
    kortit.forEach(IO::println);

    Collections.sort(kortit);

    IO.println("\nJälkeen järjestämisen:");
    kortit.forEach(IO::println);
}
// FILE_END
```

Voisimme tällöin haluta järjestää kortit ensin sarjan nimen mukaan
aakkosjärjestykseen ja sitten vasta numerotunnisteen mukaan. Tätä varten meidän
täytyy muuttaa `compareTo`-metodia siten, että se vertaa ensin sarjan nimiä ja
mikäli ne ovat samat, vertaa sitten numerotunnisteita.

```java
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
        new Kerailykortti("Loistava Lohikäärme", "Eläimet", 3),
        new Kerailykortti("Vauhdikas Vespajetti", "Ajoneuvot", 1),
        new Kerailykortti("Aloittelijan Ameeba", "Eläimet", 1),
        new Kerailykortti("Mieletön Merihevonen", "Eläimet", 2),
        new Kerailykortti("Nopea Nopsa", "Ajoneuvot", 2)
    );

    IO.println("Ennen järjestämistä:");
    kortit.forEach(IO::println);

    Collections.sort(kortit);

    IO.println("\nJälkeen järjestämisen:");
    kortit.forEach(IO::println);
}
// FILE_END
```


<task> <task-title>Tehtävä 4.3: Henkilöt järjestykseen 2. <points>0.5
  p.</points> </task-title> <handout>

{{#include ../exercises/4-3-henkilöt-järjestykseen-2/handout.md}}

  </handout> <task-link><a
  href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä
TIMissä</a></task-link> </task>

### Comparator-rajapinta

Rajapinta
[`Comparator`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Comparator.html)
tarjoaa vaihtoehtoisen tavan määritellä olioiden järjestys ilman, että itse
luokan tarvitsee toteuttaa `Comparable`-rajapintaa. Merkittävä hyöty on, että
`Comparator`-rajapinnan avulla voidaan määritellä useampia erilaisia
järjestyksiä saman tyyppisille olioille.

Rajapinnasta löytyy oletusmetodit `comparing` sekä `thenComparing`, joiden
avulla voidaan määrittää järjestämisen ehdot. Sekä `comparing`, että
`thenComparing` ottavat argumenttina funktion, jonka palauttama arvoa käytetään
vertailuun.

Alla esimerkki, jossa määritellään korttien järjestys ensin sarjan nimen ja
sitten aakkosjärjestyksen mukaan käyttäen `Comparator`-rajapintaa ja luokan
getter-metodeja.

```java
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
    kortit.forEach(IO::println);

    //HIGHLIGHT_GREEN_BEGIN
    Collections.sort(
            kortit,
            Comparator.comparing(Kerailykortti::getSarja)
                    .thenComparing(Kerailykortti::getNimi)
    );
    //HIGHLIGHT_GREEN_END

    IO.println("\nJälkeen järjestämisen nimen mukaan:");
    kortit.forEach(IO::println);
}
// FILE_END
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private String sarja;
    private int tunnistenumero;

    public Kerailykortti(String nimi, String sarja, int tunnistenumero) {
        this.nimi = nimi;
        this.sarja = sarja;
        this.tunnistenumero = tunnistenumero;
    }

    // HIGHLIGHT_GREEN_BEGIN
    public String getNimi() {
        return nimi;
    }

    public String getSarja() {
        return sarja;
    }
    // HIGHLIGHT_GREEN_END

    @Override
    public String toString() {
        return "Kortti: " + nimi + " (Sarja: " + sarja + ", #" + tunnistenumero + ")";
    }
}
// FILE_END
```

Huomaa kaksi merkittävää asiaa. Järjestysmedotille `Collections.sort` annetaan
erikseen `Comparator`-olio toisena argumenttina. Toinen merkittävä seikka on,
että `Kerailykortti`-luokkaan on lisätty getter-metodit `getNimi` ja `getSarja`,
jotta `Comparator`-rajapinnan lambda-lausekkeet voivat käyttää näitä kenttiä
vertailuun.

_Comparator_ ei näe luokan yksityisiä kenttiä suoraan, joten getter-metodit ovat
välttämättömiä. Tässä on yksi syy miksi getterit ovat hyödyllisiä, vaikka luokan
sisällä ei olisikaan tarvetta muuttaa kenttien arvoja.

Vielä yksi asia `Comparator`:sta. Aiemmin käyttämämme
`Collections.sort`-metodille hieman lyhyempänä vaihtoehtona voimme käyttää
`List`-rajapinnan tarjoamaa
[`sort(Comparator)`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/List.html#sort(java.util.Comparator))-metodia
listaolioille.

```java
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
    kortit.forEach(IO::println);

    //HIGHLIGHT_GREEN_BEGIN
    kortit.sort(Comparator.comparing(Kerailykortti::getSarja)
            .thenComparing(Kerailykortti::getNimi));
    //HIGHLIGHT_GREEN_END

    IO.println("\nJälkeen järjestämisen nimen mukaan:");
    kortit.forEach(IO::println);
}
// FILE_END
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private String sarja;
    private int tunnistenumero;

    public Kerailykortti(String nimi, String sarja, int tunnistenumero) {
        this.nimi = nimi;
        this.sarja = sarja;
        this.tunnistenumero = tunnistenumero;
    }

    public String getNimi() {
        return nimi;
    }

    public String getSarja() {
        return sarja;
    }

    @Override
    public String toString() {
        return "Kortti: " + nimi + " (Sarja: " + sarja + ", #" + tunnistenumero + ")";
    }
}
// FILE_END
```

Olennainen ero `Collections.sort`:iin verrattuna on, että `List.sort`:lle täytyy
antaa `Comparator` parametrina.

<task> <task-title>Tehtävä 4.4: Kortit harvinaisuuden mukaan. <points>0.5
  p.</points> </task-title> <handout>

{{#include ../exercises/4-4-kortit-comparator/handout.md}}

  </handout> <task-link><a
  href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä
TIMissä</a></task-link> </task>

## Tietue (kannattaako esitellä tässä vai mennäänkö vain luokilla?)

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
- Mitä hyötyä ja mahdollista harmia tästä on?
