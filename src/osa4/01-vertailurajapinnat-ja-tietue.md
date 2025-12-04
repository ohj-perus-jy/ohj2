# Vertailurajapinnat ja tietue

> [!Osaamistavoitteet]
>
> - Ymmärrät vertailurajapintojen merkityksen Javassa ja osaat järjestää kokoelmia niiden avulla
> - Tunnet Javan Tietue-luokkatyypin ja ymmärrät sen

## Vertailurajapinnat

<!-- Seuraavaksi tutustumme kahteen Javan valmiiseen vertailurajapintaan, [`Comparable`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Comparable.html):en sekä [`Comparator`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Comparator.html):iin. Nämä rajapinnat nimiensä mukaisesti ("vertailtava" ja "vertailija") tarjoavat yhteisen toiminnallisuuden olioiden järjestämiseen Javan valmiilla järjestysmenetelmillä, kuten Javan `Collections.sort`-metodilla. -->

Edellisessä osassa tutustuimme abstrakteihin luokkiin ja rajapinnan käsitteeseen. Seuraavaksi käymme läpi paria valmista Javan rajapintaa, nimittäin `Comparable`- ja `Comparator`-rajapintoja, jotka tarjoavat jaetun toteutuksen olioiden vertailuun ja järjestämiseen.

> [!Vinkki]
>
> Kannattaa vilkaista materiaalissa linkattuihin Javan virallisiin dokumentaatioihin, kuten esimerkiksi alla mainitun `Comparable`-rajapinnan dokumentaatioon (linkin tunnistaa sinisestä koodista tekstissä).
>
> Varaudu kuitenkin siihen, että dokumentaation lukeminen on haastavaa ennen kuin siihen tottuu! Virallinen dokumentaatio myös sisältää usein paljon termejä ja syntaksia, joita ei ole vielä käsitelty ja on vaikea ymmärtää. Tästä ei tarvitse olla huolissaan ja kaikki mitä kurssilla tarvitsee osata käydään läpi näissä kurssimateriaaleissa ellei erikseen toisin mainita.
>
> Dokumentaation lukutaito on kuitenkin tärkeä taito ohjelmoijalle, joten kannattaa pyrkiä totuttelemaan siihen pikkuhiljaa — myös tekoälyn aikana sillä ne eivät välttämättä anna viimeisintä tai edes onnistu toistamaan dokumentaation kertomaa totuudenmukaisesti. Jos oppii luottamaan pelkästään tekoälyyn, siinä vaiheessa kun asiat menee vaikeiksi tulee ongelmia. Tekoäly (erityisesti generatiivinen), toimii nimittäin parhaiten kun ongelmat ovat yleisiä ja tunnettuja eivätkä vaadi suurta asiantuntemusta tai tarkkaa silmää.

### Comparable-rajapinta ja luonnollinen järjestys

Rajapinta [`Comparable`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Comparable.html) määrittelee metodin `compareTo`, jonka avulla olio voi määrittää oman _luonnollisen_ järjestyksensä suhteessa toiseen olioon.

Rajapinnan metodi `compareTo` palauttaa kokonaisluvun, joka ilmaisee olion _järjestyksen_ suhteessa toiseen olioon:

- `olioA.compareTo(olioB) < 0` -> `olioA` on pienempi kuin `olioB` (`olioA < olioB`)
- `olioA.compareTo(olioB) == 0` -> `olioA` on yhtä suuri kuin `olioB` (`olioA == olioB`)
- `olioA.compareTo(olioB) > 0` -> `olioA` on suurempi kuin `olioB` (`olioA > olioB`)

```java
void main() {
  Integer luku1 = 5;
  Integer luku2 = 18;
  int tulos = luku1.compareTo(luku2);

  // Tulostaa negatiivisen arvon (< 0), koska 5 < 18
  IO.println("luku1.compareTo(luku2): " + tulos);
}
```

Luonnollisella järjestyksellä tarkoitetaan ihmisjärjen mukaisesti olion tyypille ominaista ja intuitiivista järjestystä. Esimerkiksi kokonaisluvuille luonnollinen järjestys on pienimmästä suurimpaan: `1 < 2`, `2 < 3` jne. Vastaavasti merkkijonoille luonnollinen järjestys on aakkosjärjestys: `"apina" < "banaani"`, `"banaani" < "cembalo"`.

Tästä esimerkkinä, Javan `String`-luokalla on `Comparable`-rajapinnan toteutus, joka kertoo olioiden järjestyksen aakkosjärjestyksen mukaan.

```java
// Apufunktio, joka tulostaa kahden merkkijonon välisen järjestyksen
void kerroJarjestys(String sana1, String sana2) {
  int tulos = sana1.compareTo(sana2);
  if (tulos < 0) {
      IO.println(sana1 + " on pienempi kuin " + sana2);
  } else if (tulos > 0) {
      IO.println(sana1 + " on suurempi kuin " + sana2);
  } else {
      IO.println(sana1 + " on yhtä suuri kuin " + sana2);
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

Vastaavasti `Integer`-luokalla on toteutus `Comparable`-rajapinnalle, joka kertoo kokonaislukujen luonnollisen järjestyksen.

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

Olennainen `Comparable`-rajapinnan hyöty on, että voimme käyttää Javan valmiita kokoelmien järjestämistoteutuksia, kuten esimerkiksi [`Collections.sort`](<https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Collections.html#sort(java.util.List)>)-metodia. Näin saamme järjestettyä kokoelmia helposti ilman, että meidän tarvitsee itse kirjoittaa järjestämisalgoritmeja.

```java
void main() {
    List<Integer> numerot = Arrays.asList(18, 5, 42);
    List<String> hedelmat = Arrays.asList("omena",  "päärynä", "appelsiini");
    IO.println(numerot); // [18, 5, 42]
    IO.println(hedelmat); // [omena, päärynä, appelsiini]

    // Järjestetään listat
    Collections.sort(hedelmat);
    Collections.sort(numerot);

    IO.println(numerot); // [5, 18, 42]
    IO.println(hedelmat); // [appelsiini, omena, päärynä]
}
```

<details closed><summary>Ekstra: <code>Collections</code> ja <code>Collection</code></summary>

[`Collections`](https://docs.oracle.com/en/java/javase/25/docs/api//java.base/java/util/Collections.html) on Javan valmis luokka, joka tarjoaa yllämainitun `sort`-metodin lisäksi monia yleishyödyllisiä metodeja Javan _kokoelmille_. Mikäli katso linkin, varaudu, että se sisältää paljon vasta myöhemmin käsiteltävää syntaksia.

Javan kokoelmille taas on olemassa rajapinta [`Collection`](https://docs.oracle.com/en/java/javase/25/docs/api//java.base/java/util/Collection.html), joka määrittelee yleisiä toimintoja kokoelmille, kuten lisäämisen, poistamisen ja tarkistamisen, tai onko tietty alkio kokoelmassa.

Lisäksi Javasta löytyy vielä [`AbstractCollection`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/AbstractCollection.html)-luokka helpottamaan `Collection`-rajapinnan toteuttamista. Abstrakti luokka `AbstractCollection` nimittäin tarjoaa valmiin toteutuksen monista `Collection`-rajapinnan metodeista, jolloin rajapinnan toteuttamiseksi riittää periä `Collection` ja kirjoittaa toteutus vain osalle metodeista.

</details>

> <task>
  <task-title>Tehtävä 4.1: Miksi Comparable? <points>1 p.</points> </task-title>
  <handout>
>
> {{#include ../exercises/4-1-miksi-comparable/handout.md}}
>
>   </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä TIMissä</a></task-link>
</task>

### Oma toteutus Comparable-rajapinnalle

Katsotaan seuraavaksi `Comparable`-rajapinnan toteuttamista itsetehdylle luokalle. Otetaan esimerkiksi luokka `Kerailykortti`, joka sisältää keräilykortin nimen ja yksilöivän ykkösestä alkavan tunnistenumeron.

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
    List<Kerailykortti> kortit = Arrays.asList(
        new Kerailykortti("Loistava Lohikäärme", 3),
        new Kerailykortti("Aloittelijan Ameeba", 1),
        new Kerailykortti("Mieletön Merihevonen", 2)
    );

    // TODO: tarkista, että tämä syntaksi esitellään aiemmin
    kortit.forEach(IO::println);
}
// FILE_END
```

Mikäli yritämme järjestää `Kerailykortti`-olioita `Collections.sort`-metodilla, saamme käännöksenaikaisen virheen. Tämä johtuu kaikessa yksinkertaisuudessaan, monimutkaista virheviestiä sen enempää avaamatta, siitä että `Kerailykortti`-luokka ei toteuta `Comparable`-rajapintaa — `Collections.sort` ei saa sen tarvitsemaa tietoa mikä on `Kerailykortti`-olioiden luonnollinen järjestys.

```java
// FILE: main.java
void main() {
    List<Kerailykortti> kortit = Arrays.asList(
        new Kerailykortti("Loistava Lohikäärme", 3),
        new Kerailykortti("Aloittelijan Ameeba", 1),
        new Kerailykortti("Mieletön Merihevonen", 2)
    );

    IO.println("Ennen järjestämistä:");
    kortit.forEach(IO::println);

    Collections.sort(kortit); // käännöksenaikainen virhe

    IO.println("\nJälkeen järjestämisen:");
    kortit.forEach(IO::println);
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

Kun lähdemme toteuttamaan `Comparable`-rajapintaa keräilykortille, joudumme heti pohtimaan mikä on luonnollinen järjestys keräilykorteillemme. Aakkosjärjestys voi olla hyödyllinen, mutta mikäli korteilla on yksilöivät ykkösestä alkavat numerotunnisteet, se lienee loppupeleissä useimpien mielestä luonnollisemman tuntuinen ja yhtälailla tarpeellinen. Oletusjärjestystä kannattaa myös pohtia puhtaasti sovelluksen tarpeen mukaan — mitä rajapinnan käyttäjät (eli rajapintaa hyödyntävät koodit tai niiden ohjelmoijat) kaipaavat?

Toteutetaan tällä pohjustuksella `Comparable`-rajapinta siten, että kortit järjestetään numerotunnisteen mukaan. Tätä varten tarvitsemme rajapinnan toteutuksen luokan määrittelyyn sekä toteutuksen edellä mainitulle `compareTo`-metodille.

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
        return Integer.compare(this.tunnistenumero, other.tunnistenumero);
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
    kortit.forEach(IO::println);

    Collections.sort(kortit);

    IO.println("\nJälkeen järjestämisen:");
    kortit.forEach(IO::println);
}
// FILE_END
```

Huomaa, että `implements Comparable<Kerailykortti>`-osa luokan määrittelyssä tulee kertoa minkä tyypin olioille luokka tarjoaa vertailutoiminnon, samalla tavoin kuin listalle kerrotaan minkätyyppisiä olioita lista sisältää (tyylillä `List<Kerailykortti>`). Tähän on yleensä helppo valita suoraan luokan oma tyyppi ellei ole erityistä syytä valita sen sijaan esimerkiksi yliluokkaa.

> [!Huomautus]
> `compareTo`-metodin toteutuksessa hyödynnetään Javan valmista `Integer.compare`-metodia, joka vertaa kahta kokonaislukua ja palauttaa vertailutuloksen yllä kuvatulla tavalla. Tämä on kätevä apumetodi, joka kannattaa muistaa kun vertailtavat arvot ovat perusdatatyyppejä kuten `int`, `double` tai `char`.
>
> Olennainen syy miksi `Integer.compare`-metodia kannattaa käyttää on, että se käsittelee oikein myös erikoistapaukset kuten ylivuodot, joita voi syntyä suoran vähennyslaskun avulla tehtävässä vertailussa: `this.tunnistenumero - other.tunnistenumero` — mieti mikä on `compareTo`:n antama järjestys, jos `this.tunnistenumero` on `int`:n pienin mahdollinen arvo ja `other.tunnistenumero` on `1` (vihje: ei mitä sen pitäisi olla eli negatiivinen).

### Useamman kentän vertailu

Katsotaan vielä hieman monimutkaisempaa tapausta, missä meillä on keräilykortissa vielä tieto kortin sarjasta (esim. "Eläimet", "Ajoneuvot" jne.).

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

Voisimme tällöin haluta järjestää kortit ensin sarjan nimen mukaan aakkosjärjestykseen ja sitten vasta numerotunnisteen mukaan. Tätä varten meidän täytyy muuttaa `compareTo`-metodia siten, että se vertaa ensin sarjan nimiä ja mikäli ne ovat samat, vertaa sitten numerotunnisteita.

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

> <task>
  <task-title>Tehtävä 4.2: Henkilöt järjestykseen. <points>0.5 p.</points> </task-title>
  <handout>
>
> {{#include ../exercises/4-2-henkilöt-järjestykseen/handout.md}}
>
>   </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä TIMissä</a></task-link>
</task>

> <task>
  <task-title>Tehtävä 4.3: Henkilöt järjestykseen 2. <points>0.5 p.</points> </task-title>
  <handout>
>
> {{#include ../exercises/4-3-henkilöt-järjestykseen-2/handout.md}}
>
>   </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä TIMissä</a></task-link>
</task>

### Comparator-rajapinta

Rajapinta [`Comparator`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Comparator.html) tarjoaa vaihtoehtoisen tavan määritellä olioiden järjestys ilman, että itse luokan tarvitsee toteuttaa `Comparable`-rajapintaa. Merkittävä hyöty on, että `Comparator`-rajapinnan avulla voidaan määritellä useampia erilaisia järjestyksiä saman tyyppisille olioille.

Rajapinnasta löytyy oletusmetodit `comparing` sekä `thenComparing`, joiden avulla voidaan määrittää järjestämisen ehdot. Sekä `comparing`, että `thenComparing` ottavat argumenttina funktion, jonka palauttama arvoa käytetään vertailuun.

Alla esimerkki, jossa määritellään korttien järjestys ensin sarjan nimen ja sitten aakkosjärjestyksen mukaan käyttäen `Comparator`-rajapintaa ja luokan getter-metodeja.

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

Huomaa kaksi merkittävää asiaa. Järjestysmedotille `Collections.sort` annetaan erikseen `Comparator`-olio toisena argumenttina. Toinen merkittävä seikka on, että `Kerailykortti`-luokkaan on lisätty getter-metodit `getNimi` ja `getSarja`, jotta `Comparator`-rajapinnan lambda-lausekkeet voivat käyttää näitä kenttiä vertailuun.

_Comparator_ ei näe luokan yksityisiä kenttiä suoraan, joten getter-metodit ovat välttämättömiä. Tässä on yksi syy miksi getterit ovat hyödyllisiä, vaikka luokan sisällä ei olisikaan tarvetta muuttaa kenttien arvoja.

Vielä yksi asia `Comparator`:sta. Aiemmin käyttämämme `Collections.sort`-metodille hieman lyhyempänä vaihtoehtona voimme käyttää `List`-rajapinnan tarjoamaa [`sort(Comparator)`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/List.html#sort(java.util.Comparator))-metodia listaolioille.

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

Olennainen ero `Collections.sort`:iin verrattuna on, että `List.sort`:lle täytyy antaa `Comparator` parametrina.

> <task>
  <task-title>Tehtävä 4.4: Kortit harvinaisuuden mukaan. <points>0.5 p.</points> </task-title>
  <handout>
>
> {{#include ../exercises/4-4-kortit-comparator/handout.md}}
>
>   </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä TIMissä</a></task-link>
</task>

## Tietue (kannattaako esitellä tässä vai mennäänkö vain luokilla?)

- Erityinen luokkatyyppi kuten luetelma (enum)
- Ei salli arvojen muuttamista

- Tarjoaa valmiin toteutuksen:
  - yksityinen, lopullinen kenttä jokaiselle tietoelementille
  - getter-metodi jokaiselle kentälle
  - julkinen konstruktori, jolla on vastaava argumentti jokaista kenttää varten
  - equals-metodi, joka palauttaa true, jos oliot ovat samaa luokkaa ja kaikki kentät ovat samat
  - hashCode-metodi, joka palauttaa saman arvon, kun kaikki kentät ovat samat (ja mahdollisesti muulloinkin — törmäykset ovat mahdollisia)
  - toString-metodi, joka sisältää luokan nimen sekä jokaisen kentän nimen ja sen vastaavan arvon
