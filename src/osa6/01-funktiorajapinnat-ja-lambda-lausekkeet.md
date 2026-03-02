# Funktiorajapinnat ja lambdalausekkeet

> [!Osaamistavoitteet]
>
> - Ymmärrät funktionaalisen rajapinnan käsitteen
> - Osaat käyttää lambdalausekkeita ja funktioviitteitä funktiorajapintojen
>   toteuttamiseen
> - Tunnet Javan yleisimmät valmiit funktiorajapinnat (esim. `Function`,
>   `Consumer`)
> - Osaat määrittää olioille vaihtoehtoisia järjestyksiä `Comparator`-rajapinnan
>   ja lambdalausekkeiden avulla

*Funktionaalinen rajapinta* (engl. *functional interface*) on rajapinta, joka
sisältää vain yhden pakollisen metodin. Sen tarkoituksena on edustaa yksittäistä
toimintoa tai kyvykkyyttä.

Esimerkiksi seuraava rajapinta on funktionaalinen:

```java,ignore
/**
 * Rajapinta, joka edustaa funktiota. Se ottaa parametrina luvun
 * ja palauttaa toisen luvun.
 */
public interface NumeroFunktio {
    int laske(int luku);
}
```

Myös osassa 4.1 esimerkkinä tehty
[Saadettava-rajapinta](../osa4/01-rajapinta.md#alykoti-saadettava) on
funktionaalinen, sillä se sisältää vain yhden metodin: `asetaArvo`.

Java tarjoaa yksinkertaistetun tavan luoda olioita, jotka toteuttavat
funktionaalisia rajapintoja. Tämä mahdollistaa koodin, jossa voimme käsitellä
funktioita lähes samalla tavalla kuin käsittelemme dataa.

## Olion alustaminen funktiorajapinnasta

Jos haluamme luoda olion, joka toteuttaa `NumeroFunktio`-rajapinnan, voimme
määritellä luokan, joka toteuttaa rajapinnan ja sitten ylikirjoittaa metodin
`laske`.

```java
// FILE: main.java
public class KerroKahdella implements NumeroFunktio {
    @Override
    public int laske(int luku) {
        return luku * 2;
    }
}

void main() {
    NumeroFunktio kerroKahdella = new KerroKahdella();
    IO.println(kerroKahdella.laske(3));
}
// FILE_END
// FILE: NumeroFunktio.java
public interface NumeroFunktio {
    int laske(int luku);
}
// FILE_END
```

Tässä jouduimme kirjoittamaan melko paljon koodia (uusi luokka, metodin
ylikirjoitus) vain yhtä pientä oliota varten. Nyt on kuitenkin niin, että
`NumeroFunktio` on funktionaalinen rajapinta: sillä on vain yksi pakollinen
metodi. Javassa on mahdollista käyttää olemassa olevaa metodia *ilman* luokan
rakentelua ikään kuin tämä metodi olisi kyseisen rajapinnan toteuttava olio.
Tätä kutsutaan *funktioviitteeksi* (engl. *method reference*).

```java
// FILE: main.java
int kerroKahdella(int luku) {
    return luku * 2;
}

void main() {
    // Käytetään olemassa olevaa metodia rajapinnan toteutuksena
    // HIGHLIGHT_GREEN_BEGIN
    NumeroFunktio funktio = this::kerroKahdella;
    // HIGHLIGHT_GREEN_END
    
    IO.println(funktio.laske(3));
}
// FILE_END
// FILE: NumeroFunktio.java
public interface NumeroFunktio {
    int laske(int luku);
}
// FILE_END
```

Huomaa erityisesti syntaksi `this::kerroKahdella`. Se ei kutsu metodia, vaan se
ikään kuin luo viitteen metodiin. Java osaa automaattisesti luoda rajapinnan
toteuttavan olion, koska `kerroKahdella`-metodin parametrit ja palautusarvo
täsmäävät rajapinnan ainoan metodin kanssa. Jos yritämme tulostaa
`funktio`-muuttujan arvon, kokonaisluvun sijaan tulostuukin olion tiedot:

```java
//-public interface NumeroFunktio {
//-    int laske(int luku);
//-}
//-
//-int kerroKahdella(int luku) {
//-    return luku * 2;
//-}
//-
//-void main() {
NumeroFunktio funktio = this::kerroKahdella;
IO.println(funktio);
//-}
```

Toiseksi, funktioviitteen yhteydessä käytetään `::`-merkintää viittaamaan joko
olion tai luokan metodiin. Toisin sanoen, `this::kerroKahdella` tarkoittaa, että
funktioviite koskee nykyisen olion `kerroKahdella`-metodia. `this`-viitteen
sijaan voidaan käyttää olioviitettä tai luokkametodien tapauksessa luokkaa:


```java
// FILE: main.java
class Ohjelma {
    public static int kerroKahdellaStatic(int luku) {
        IO.println("Olen luokkametodi!");
        return luku * 2;
    }

    public int kerroKahdellaEiStatic(int luku) {
        IO.println("Olen oliometodi!");
        return luku * 2;
    }

    void main() {
        // Nyt kerroKahdella on luokkametodi, joten käytetään luokan nimeä
        // olioviitteen sijaan.
        NumeroFunktio funktio = Ohjelma::kerroKahdellaStatic;
        // Tavallisen metodin viite saadaan olioviitteen kautta
        NumeroFunktio funktio2 = this::kerroKahdellaEiStatic;
        IO.println(funktio.laske(2));
        IO.println(funktio2.laske(2));
    }
}
// FILE_END
// FILE: NumeroFunktio.java
/**
 * Rajapinta, joka kuvastaa funktiota, joka ottaa parametrina luvun
 * ja palauttaa toisen luvun.
 */
public interface NumeroFunktio {
    int laske(int luku);
}
// FILE_END
```

<details>
<summary><i class="bi bi-stars jyu-gold"></i> Bonus: Miten funktioviite toimii?</summary>

Saatat miettiä, miten funktio voi yhtäkkiä "muuttua" olioksi. Javassa kyseessä
on oikeastaan tekninen temppu. Ennen funktioviitteitä sama asia Javassa tehtiin
*anonyymeillä luokilla*. 

Kääntäjä muuttaa funktioviitteen `this::kerroKahdella` suunnilleen tällaiseksi
rakenteeksi:

```java,ignore
int kerroKahdella(int luku) {
    return luku * 2;
}

NumeroFunktio funktio = new NumeroFunktio() {
    @Override
    public int laske(int luku) {
        return kerroKahdella(luku);
    }
};
```

Lambdalauseke on siis todellisuudessa olio, joka toteuttaa halutun rajapinnan.
Tästä syystä niitä voidaan käyttää vain sellaisten rajapintojen kanssa, joissa
on tasan yksi metodi (funktionaaliset rajapinnat).

Mainittakoon, että vaikka anonyymejä luokkia käytetään nykyään vähemmän, voivat
olla silti hyödyllisiä tapauksissa, jossa toteutettava rajapinta ei ole
funktionaalinen.

</details>

## Lambdalausekkeet

Javassa on mahdollista kirjoittaa funktion toteutus ilman erillistä metodia,
suoraan siinä kohdassa, missä funktio tarvitaan. Tällaista lausekemuodossa
kirjoitettua funktiota kutsutaan *lambdalausekkeeksi* (engl. *lambda
expression*). 

Lambdalausekkeen perusrakenne on seuraava:

```java,ignore
(tyyppi parametri) -> {
    // funktion runko
    return tulos;
}
```

Jos parametreja on useampi, ne erotetaan pilkulla:

```java,ignore
(tyyppi1 parametri1, tyyppi2 parametri2) -> {
    // funktion runko
    return tulos;
}
```

Lambdalausekkeelle ei tarvitse antaa erikseen nimeä. Tästä syystä niitä
kutsutaan myös *anonyymeiksi funktioiksi* (engl. *anonymous function*). Alla
esimerkki, tulostetaan listan alkioita lambdalausekkeella. 

```java
// FILE: main.java
void main() {
    // Välitetään anonyymi funktio suoraan forEach-metodille
    List<String> marjoja = List.of("mansikka", "mustikka", "puolukka", "mansikka");
    // tulosta vain mansikat
    marjoja.forEach(marja -> {
        if (marja.equals("mansikka")) {
            IO.println(marja);
        }
    });
    
}
// FILE_END
```

Tämähän olisi voitu kirjoittaa myös perinteisellä aliohjelmakutsulla:

```java,ignore
void main() {
    List<String> marjoja = List.of("mansikka", "mustikka", "puolukka");
    tulostaMansikat(marjoja);
}

void tulostaMansikat(List<String> marjoja) {
    for (String marja : marjoja) {
        if (marja.equals("mansikka")) {
            IO.println(marja);
        }
    }
}
```

Oleellinen ajatus on tämä: lambdalauseke ei ole irrallinen koodinpätkä, vaan se
on olio, joka toteuttaa funktionaalisen rajapinnan. Kullekin parametrille tulee
määritellä tyyppi, joka vastaa funktionaalisen rajapinnan metodin parametreja.
Palataan esimerkkiimme `NumeroFunktio`-rajapinnasta. Toteutetaan nyt
lambdalausekkeena funktio, joka kertoo syötetyn luvun kahdella. Tällaisen
lausekkeen tulee ottaa parametrina yksi kokonaisluku ja palauttaa kokonaisluku.
Muoto on seuraava: 

```java,ignore
(int luku) -> {
    return luku * 2;
}
```

Koska tällainen lambdalauseke toteuttaa `NumeroFunktio`-rajapinnan, voimme
sijoittaa sen `NumeroFunktio`-tyyppiseen muuttujaan:

```java,ignore
NumeroFunktio funktio = (int luku) -> {
    return luku * 2;
};
```

Nyt voimme kutsua `funktio`-muuttujan `laske`-metodia, koska olemme toteuttaneet
`NumeroFunktio`-rajapinnan.


```java
// FILE: main.java
void main() {
    NumeroFunktio funktio = (int luku) -> {
        return luku * 2;
    };
    IO.println(funktio.laske(1));
    IO.println(funktio.laske(2));
    IO.println(funktio.laske(3));
    IO.println(funktio.laske(4));
}
// FILE_END
// FILE: NumeroFunktio.java
/**
 * Rajapinta, joka kuvastaa funktiota, joka ottaa parametrina luvun
 * ja palauttaa toisen luvun.
 */
public interface NumeroFunktio {
    int laske(int luku);
}
// FILE_END
```

Emme siis tarvinneet erillistä luokkaa, emmekä edes erillistä metodia!

Lambdalausekkeiden suurin etu on juuri niiden tiiviys. Java osaa päätellä monta
asiaa automaattisesti, jolloin koodia vielä tästäkin voidaan lyhentää.
Ensinnäkin parametrien tyypit voidaan päätellä funktiorajapinnan parametrien
tyypeistä, joten tyypit voidaan usein jättää pois. Yllä olevassa esimerkissämme
voimme jättää pois `int`-tyypin, koska `NumeroFunktio.laske`-metodi ottaa
parametrina kokonaisluvun, eikä tätä tarvitse erikseen mainita lambdalausekkeessa.

```java
//-public interface NumeroFunktio {
//-    int laske(int luku);
//-}
//-
//-void main() {
NumeroFunktio funktio = (luku) -> {
    return luku * 2;
};
//-IO.println(funktio.laske(1));
//-IO.println(funktio.laske(2));
//-IO.println(funktio.laske(3));
//-IO.println(funktio.laske(4));
//-}
```

Toiseksi, jos lambdalausekkeen runko sisältää vain yhden lauseen, aaltosulut ja
`return`-sanan voi jättää pois.

```java
//-public interface NumeroFunktio {
//-    int laske(int luku);
//-}
//-
//-void main() {
NumeroFunktio funktio = (luku) -> luku * 2;
//-IO.println(funktio.laske(1));
//-IO.println(funktio.laske(2));
//-IO.println(funktio.laske(3));
//-IO.println(funktio.laske(4));
//-}
```

Lopuksi, jos lambdalausekkeessa on tasan yksi parametri, myös kaarisulut voi
jättää pois.

```java
//-public interface NumeroFunktio {
//-    int laske(int luku);
//-}
//-
//-void main() {
NumeroFunktio funktio = luku -> luku * 2;
//-IO.println(funktio.laske(1));
//-IO.println(funktio.laske(2));
//-IO.println(funktio.laske(3));
//-IO.println(funktio.laske(4));
//-}
```

Lambdalausekkeissa on lisäksi tapana käyttää tavallista lyhyempiä parametrien
nimiä, sillä parametrien merkitys dokumentoidaan funktionaalisessa rajapinnassa. 

```java
//-public interface NumeroFunktio {
//-    int laske(int luku);
//-}
//-
//-void main() {
NumeroFunktio kerroKahdella = x -> x * 2;
//-IO.println(kerroKahdella.laske(1));
//-IO.println(kerroKahdella.laske(2));
//-IO.println(kerroKahdella.laske(3));
//-IO.println(kerroKahdella.laske(4));
//-}
```

### Funktiot parametreina

Koska lambdalauseke on olio, voimme välittää sen aliohjelmalle parametrina. Tämä
mahdollistaa korkeamman abstraktiotason funktioiden kirjoittamisen. Voimme tehdä
vaikkapa aliohjelman, joka osaa laskea kahden eri funktion summan:

```java
//-public interface NumeroFunktio {
//-    int laske(int luku);
//-}
//-
/**
 * Laskee kahden funktion summan tietylle arvolle.
 */
int summaaFunktiot(NumeroFunktio f1, NumeroFunktio f2, int x) { 
    return f1.laske(x) + f2.laske(x);
}

void main() {
    // Välitetään kaksi eri funktiota (x*2 ja x*x) summattavaksi
    int tulos = summaaFunktiot(x -> x * 2, x -> x * x, 3);
    IO.println("Tulos: " + tulos); // (3*2) + (3*3) = 6 + 9 = 15
}
```

## Valmiita funktiorajapintoja

Javassa on joukko valmiita yleisiä funktiorajapintoja, jotka löytyvät
`java.util.function`-paketista (ks.
[JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/package-summary.html#class-summary)).

**`Function<T, R>`**
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/Function.html))
esittää funktiota, joka ottaa yhden parametrin tyyppiä `T` ja palauttaa
parametrin tyyppiä `R`. Esimerkiksi yllä oleva esimerkki voidaan yksinkertaistaa
käyttämällä valmista `Function`-rajapintaa `NumeroFunktio`-rajapinnan sijaan:

```java
//-void main() {
Function<Integer, Integer> kerroKahdella = x -> x * 2;
Function<Integer, Integer> potenssiinKaksi = x -> x * x;

IO.println(kerroKahdella.apply(1));
IO.println(potenssiinKaksi.apply(2));
//-}
```

`Function`-rajapinta sisältää myös apumetodit `andThen` ja `compose`, joiden
avulla funktioita voidaan ketjuttaa:

```java
//-void main() {
Function<Integer, Integer> kerroKahdella = x -> x * 2;
Function<Integer, Integer> potenssiinKaksi = x -> x * x;

// Laskee: (x^2) * 2
Function<Integer, Integer> potenssiinJaKerro = kerroKahdella.compose(potenssiinKaksi);
// Laskee: (x * 2)^2
Function<Integer, Integer> kerroJaPotenssiin = kerroKahdella.andThen(potenssiinKaksi);

IO.println(potenssiinJaKerro.apply(2));
IO.println(kerroJaPotenssiin.apply(2));
//-}
```

Vastaavasti **`BiFunction<T, U, R>`**
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/BiFunction.html))
edustaa funktiota, joka ottaa kaksi parametria ja palauttaa yhden arvon.

**`Consumer<T>`**
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/Consumer.html))
ja **`BiConsumer<T, U>`**
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/BiConsumer.html))
puolestaan vastaavat funktioita, jotka ottavat parametreja mutta eivät palauta
mitään (palautustyyppi on `void`). Esimerkiksi useat kokoelmat sisältävät
`forEach`-metodin, jolle välitetään `Consumer`-olio:

```java
//-void main() {
List<String> marjoja = List.of("mansikka", "mustikka", "puolukka");

// IO.println sopii Consumer<T>:hen, sillä 
// se ottaa yhden parametrin eikä palauta mitään
marjoja.forEach(IO::println);

Map<String, Integer> arvosanat = new HashMap<>(
            Map.of( "Denis",        1,
                    "Antti-Jussi",  3,
                    "Sami",         5,
                    "Karri",        5)
    );
// BiConsumer ottaa kaksi parametria (avain ja arvo)
arvosanat.forEach((nimi, arvosana) -> IO.println(nimi + " => " + arvosana));
//-}
```

<task>
  <task-title>Tehtävä 6.1: Laskukone <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/6-1-laskukone/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa6/tehtava1">Tee tehtävä TIMissa</a></task-link>
</task>

### Comparator-rajapinta

Palataan [luvussa 4.2](../osa4/02-vertailurajapinta.md) esiteltyyn
`Comparable<T>`-rajapintaan. Sen avulla määritimme olioille *luonnollisen
järjestyksen*. Toisinaan haluamme kuitenkin järjestää samoja olioita eri
tilanteissa eri tavoin (esim. henkilöt nimen mukaan TAI iän mukaan).

Javan `Comparator`-rajapinta
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Comparator.html))
tarjoaa tavan määrittää *vaihtoehtoisia* järjestystapoja. Rajapinta sisältää
vain yhden pakollisen metodin (`compare`), eli se on funktionaalinen rajapinta.
Rajapinnan `compare` toimii samalla periaatteella kuin `Comparable.compareTo`:


| Tapaus                   | Merkitys | Tulkinta                            |
| ------------------------ | -------- | ----------------------------------- |
| `cmp.compare(a, b) < 0`  | `a < b`  | `a` on järjestyksessä ennen `b`:tä  |
| `cmp.compare(a, b) == 0` | `a == b` | `a` ja `b` ovat samanarvoisia       |
| `cmp.compare(a, b) > 0`  | `a > b`  | `a` on järjestyksessä `b`:n jälkeen |

Koska `Comparator` on funktionaalinen, voimme määrittää vertailun erittäin
tiiviisti lambdalausekkeena:

```java
//-void main() {
List<String> nimet = Arrays.asList("Ville", "Aino", "Matti");

// Järjestetään nimet pituuden mukaan (lyhyin ensin)
nimet.sort((s1, s2) -> Integer.compare(s1.length(), s2.length()));

IO.println(nimet); // [Aino, Ville, Matti]
//-}
```

Palataan vielä osassa 4.2 olevaan
[keräilykorttiesimerkkiin](../osa4/02-vertailurajapinta.md#oma-toteutus-comparable-rajapinnalle).
Laajennetaan hieman `Kerailykortti`-luokkaa lisäämällä attribuutti `sarja`, joka
kuvaa korttisarjaa (esim. eläimet, ajoneuvot, jne.):


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
ensin keräilykortit järjestetään nimen ja sitten tunnisteen mukaan. Haluaisimme
kuitenkin tarjota vaihtoehtoisen tavan järjestää keräilykortteja sarjan nimen
mukaan. Tätä varten voimme käyttää Javan valmista `sort`-metodin versiota, joka
ottaa parametrina `Comparator`-vertailijan:

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

    // Collections.sort tarjoaa version, jossa toiseksi parametrina voi antaa
    // järjestyksen, jonka mukaan alkioita järjestetään.
    Comparator<Kerailykortti> sarjanMukaan = 
        (kortti1, kortti2) -> kortti1.getSarja().compareTo(kortti2.getSarja());
    Collections.sort(kortit, sarjanMukaan);

    IO.println();

    IO.println("Jälkeen järjestämisen:");
    kortit.forEach(IO::println);
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
```

Huomaa erityisesti, että nyt järjestäminen tehdään `sarjanMukaan`-vertailijan
mukaan, joka on määritelty lambdalausekkeena. Koska vertailija on määritelty
`Kerailykortti`-luokan ulkopuolella, lisäsimme myös saantimetodin `getSarja()`.

Javan `Comparator`-luokka tarjoaa myös valmiita apumetodeja vertailijoiden
yhdistämiseksi.

`Comparator.comparing()`-metodi ottaa parametrina lambdalausekkeen, joka
palauttaa oliosta lasketun arvon, jonka perusteella vertailu tehdään. Metodi
soveltuu tilanteisiin, kun olio halutaan vertailla olion metodin palauttaman
arvon luonnollisen järjestyksen mukaan. Esimerkiksi keräilykorttien
`sarjanMukaan`-vertailija voidaan toteuttaa suoraviivaisemmin:

```java
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
//-    kortit.forEach(IO::println);
//-
Comparator<Kerailykortti> sarjanMukaan = 
    Comparator.comparing(Kerailykortti::getSarja);
//-    Collections.sort(kortit, sarjanMukaan);
//-
//-    IO.println();
//-
//-    IO.println("Jälkeen järjestämisen:");
//-    kortit.forEach(IO::println);
//-}
//-
//-class Kerailykortti implements Comparable<Kerailykortti> {
//-    private String nimi;
//-    private String sarja;
//-    private int tunnistenumero;
//-    
//-    public Kerailykortti(String nimi, String sarja, int tunnistenumero) {
//-        this.nimi = nimi;
//-        this.sarja = sarja;
//-        this.tunnistenumero = tunnistenumero;
//-    }
//-
//-    public String getSarja() {
//-        return sarja;
//-    }
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
//-    @Override
//-    public String toString() {
//-        return "Kortti: " + nimi + " (Sarja: " + sarja + ", #" + tunnistenumero + ")";
//-    }
//-}
```

Puolestaan `Comparator.thenComparing()`-metodi palauttaa vertailijan, joka
yhdistää kaksi vertailijaa yhteen: ensin verrataan olioita ensimmäisen
vertailijan mukaan ja jos ensimmäinen vertailija palauttaa `0`, vertaillaan
toisen vertailijan mukaan. Esimerkiksi keräilykorttien omaa `compareTo`-metodia
voidaan toteuttaa oliomaisemmin seuraavasti:

```java,ignore
@Override
public int compareTo(Kerailykortti other) {
    // Vertailija, joka vertaa kortteja sarjan mukaan
    Comparator<Kerailykortti> sarjanMukaan = Comparator.comparing(k -> k.sarja);
    // Vertailija, joka vertaa kortteja tunnistenumeron mukaan
    Comparator<Kerailykortti> tunnistenumeronMukaan = Comparator.comparing(k -> k.tunnistenumero);
    
    // vertaillaan ensin sarjan mukaan ja sitten tunnistenumeron mukaan
    Comparator<Kerailykortti> vertailu = sarjanMukaan.thenComparing(tunnistenumeronMukaan);
    return vertailu.compare(this, other);
}
```

`Comparator.naturalOrder()` palauttaa `Comparator`-vertailijan, joka järjestää
oliot niiden *luonnollisen järjestyksen* mukaan. Toisin sanoen, tämä
mahdollistaa ns. eristää `Comparable`-rajapintaa toteuttavan olion
`compareTo`-metodin toteutuksen vertailuolioksi. Esimerkiksi merkkijonojen
aakkosjärjestystä vastaavan vertailijan saa tällä tavoin:

```java
void main() {
    List<String> jonoja = new ArrayList<>(List.of("Denis", "Antti-Jussi", "Karri", "Rauli", "Sami"));
    Comparator<String> aakkosjarjestys = Comparator.naturalOrder();
    Collections.sort(jonoja, aakkosjarjestys);
    IO.println(jonoja);
}
```

`Comparator.reversed()` luo uuden vertailijan, joka kääntää
vertailujärjestyksen. Tämän avulla esimerkiksi pystyy helposti järjestämään
merkkijonot käänteiseen aakkosjärjestykseen:

```java
void main() {
    List<String> jonoja = new ArrayList<>(List.of("Denis", "Antti-Jussi", "Karri", "Rauli", "Sami"));
    Comparator<String> aakkosjarjestys = Comparator.naturalOrder();
    // HIGHLIGHT_GREEN_BEGIN
    Comparator<String> kaanteinenAakkosjarjestys = aakkosjarjestys.reversed();
    // HIGHLIGHT_GREEN_END
    Collections.sort(jonoja, kaanteinenAakkosjarjestys);

    IO.println(jonoja);
}
```

Oletuksena monet vertailijat eivät käsittele `null`-viitteitä, mikä voi johtaa
erilaisiin virheisiin ja odottamattomiin tilanteisiin. Esimerkiksi jopa Javassa
määritelty `String`-merkkijonojen luonnollinen järjestys ei käsittele tapausta,
jos jompikumpi verrattavista merkkijonoista on `null`:

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

`Comparator.nullsFirst()` ja `Comparator.nullsLast()` -metodit auttavat
tällaisissa tilanteissa: ne ottavat parametriksi vertailuolion ja palauttavat
uuden vertailijan, joka osaa käsitellä `null`-viitteitä. Nimensä mukaan
`nullsFirst()` asettaa `null`-viitteet pienemmäksi kuin muut arvot (ja siten
järjestyksessä ensimmäiseksi), kun taas `nullsLast` asettaa `null`-viitteet
suuremmaksi kuin muut arvot (eli järjestyksessä viimeiseksi):

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

Yhdistämällä eri `Comparator`-vertailijoiden metodeja voidaan toteuttaa hyvin
monipuolisia vertailijoita ilman ehtorakenteita:

```java
//-void main() {
List<String> nimet = Arrays.asList("Ville", "Aino", "Matti", null);

// Rakennetaan monimutkaisempi vertailija:
// 1. Huomioi null-arvot (laita ne loppuun)
// 2. Järjestä pituuden mukaan
// 3. Jos pituus on sama, käytä aakkosjärjestystä (naturalOrder)
Comparator<String> vertailija = Comparator.nullsLast(
    Comparator.comparingInt(String::length)
              .thenComparing(Comparator.naturalOrder())
);

nimet.sort(vertailija);
IO.println(nimet);
//-}
```

<task>
  <task-title>Tehtävä 6.2: Vertailu harvinaisuuden mukaan <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/6-2-vertailu-harvinaisuus/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa6/tehtava2">Tee tehtävä TIMissa</a></task-link>
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
