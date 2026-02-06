# Funktiorajapinnat ja lambdalausekkeet

> [!VAROITUS]
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Funktionaalinen ohjelmointi
> - Funktionaalinen rajapinta ja Javan `Function`, `BiFunction`
> - lambdalausekkeet


*Funktionaalinen rajapinta* on rajapinta, joka sisältää vain yhden pakollisen
metodin.
Esimerkiksi, seuraava rajapinta on funktionaalinen:

```java,ignore
/**
 * Rajapinta, joka kuvastaa jotain funktiota, joka ottaa parametrina luvun
 * ja palauttaa toisen luvun.
 */
public interface NumeroFunktio {
    int laske(int luku);
}
```

Lisäksi esimerkiksi [luvussa
4.1](../osa4/01-rajapinta.md#älykoti-säädettävät-laitteetalykoti-saadettava)
`Saadattava`-rajapinta on funktionaalinen, koska se sisältää ainoan
pakollisen metodin `asetaArvo`.

Java tarjoaa erityisen tavan luoda olioita, jotka toteuttavat
funktiorajapintoja.
Tämä puolestaan mahdollistaa funktioiden välittämisen
toisten funktioiden parametrina.

## Olion alustaminen funktiorajapinnasta

Jos haluaisimme luoda olion, jonka voisi sijoittaa `LukuLauseke`-tyyppiseen
muuttujaan, joutusimme tekemään uuden luokan:

```java
// FILE: main.java
public class KerroKahdella implements NumeroFunktio {
    public int laske(int luku) {
        return luku * 2;
    }
}

void main() {
    NumeroFunktio kerroKahdella = new KerroKahdella();
    IO.println(kerroKahdella.laske(1));
    IO.println(kerroKahdella.laske(2));
    IO.println(kerroKahdella.laske(3));
    IO.println(kerroKahdella.laske(4));
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

Tässä siis jouduimme määrittelemään uuden luokan `KerroKahdella`, joka
sisältää halutun funktion. Sitten jouduimme alustamaan olion luokasta, jotta
`laske`-funktiota voidaan käyttää.

Koska `NumeroFunktio` on funktionaalinen rajapinta, Java sallii *funktion
käyttämisen oliona suoraan*:

```java
// FILE: main.java
int kerroKahdella(int luku) {
    return luku * 2;
}

void main() {
    NumeroFunktio funktio = this::kerroKahdella;
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

Nyt siis emme määritä enää erillistä luokkaa `KerroKahdella`, vaan riittää
määrittää suoraan metodi `kerroKahdella`. Metodi voidaan sijoittaa suoraan
`NumeroFunktio`-tyyppiseen muuttujaan. Koska metodin parametrien ja
palautusarvon tyypit täsmäävät `NumeroFunktio`-funktiorajapinnan
ainoan metodin kanssa, Java osaa automaattisesti luoda olion, joka toteuttaa
funktiorajapinnan.

Huomaa erityiesti syntaksi ja miten se eroaa funktion kutsusta. Ensinnäkin,
`this::kerroKahdella` ei kutsu funktiota, vaan kyseessä on ns. *funktioviite*.
 Tästä syystä rivillä ei ole funktiokutsulle ominaista
parametrien välitystä `()`-sulkuja käyttäen.
Varsinainen kutsu tapahtuu vasta `funktio.laske()`-riveillä, joka kutsuu
`kerroKahdella`-funktion.
Jos `funktio`-muuttujan arvoa tulostaa, kokonaisluvun sijaan tulostuukin
olion tiedot:

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

Toiseksi, funktioviitteen yhteydessä käytetään `::`-merkintää viittaamaan
joko olion tai luokan metodiin. Toisin sanoen, `this::kerroKahdella` tarkoittaa,
että funktioviite koskee nykyisen olion `kerroKahdella`-metodia.
`this`-viitteen sijaan voidaan käyttää olioviitettä tai luokkametodien
tapauksessa luokkaa:


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

Alkuun voisi ajatella, että funktioviitteet kirjaimellisesti viittaavaat toiseen
funktioon. Tällainen toteutus on yleistä esimerkiksi matalamman tason kielissä,
kuten C:ssa, C++:ssa tai Rustissa. 
Javassa kuitenkin kyseessä on vanhan ominaisuuden hyväksikäyttö: anonyymit
luokat.

Yllä oleva koodi voitaisiin kirjoittaa Javan vanhalla syntaksilla seuraavasti:

```java
// FILE: main.java
int kerroKahdella(int luku) {
    return luku * 2;
}

void main() {
    // HIGHLIGHT_GREEN_BEGIN
    NumeroFunktio funktio = new NumeroFunktio() {
        @Override
        public int laske(int luku) {
            return kerroKahdella(luku);
        }
    };
    // HIGHLIGHT_GREEN_END

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

Tässä luodaan uusi *luokka*, joka toteuttaa rajapinnan `NumeroFunktio`
ja määrittää metodin `laske`, joka kutsuu `kerroKahdella`-funktiota.
Samalla `new`-määreellä luodaan luokasta uusi olio.

Funktioviite onkin siis tarkemmin sanottuna *funktio-olio*, joka toteuttaa
funktiorajapinnan kutsumalla viitattu funktio.

Mainittakoon, että vaikka anonyymejä funktioita käytetään nykyään vähemmän,
voivat olla silti hyödyllisiä tapauksissa, jossa toteutettava rajapinta 
ei ole funktionaalinen.

</details>


## lambdalausekkeet

Yllä oleva `kerroKahdella`-funktion esimerkki voidaan tiivistää lisää
siirtämällä `kerroKahdella`-funktion toteutus suoraan `funktio`-muuttujan
sijoitukseen:

```java
// FILE: main.java
void main() {
    // HIGHLIGHT_GREEN_BEGIN
    NumeroFunktio funktio = (int luku) -> {
        return luku * 2;
    };
    // HIGHLIGHT_GREEN_END
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

Yllä `funktio`-muuttujaan sijoitettu lauseke on nimeltään
*lambdalauseke* tai *anonyymi funktio*. Kyseessä on siis funktio, jolle
ei ole annettu nimeä. Lambdalausekkeen rakenne vastaa tavallisen funktion rakennetta:

```java,ignore
(Tyyppi parametri, Tyyppi parametri2, Tyyppi parametri3) -> {
    // Funktion runko
    return tulos; // ei pakollinen; vain jos palauttaa jonkun arvon
}
```

Huomaa erityisesti, että kokonaisuus on *lauseke*, jonka voi sijoittaa
funktiorajapintatyyppisen muuttujan arvoksi.

Lamdalausekkeiden määrittelyä monesti tiivistetään muutamalla tavalla.
Ensinnäkin, Java osaa päätellä parametrien tyypit automaattisesti
funktiorajapinnan parametrien tyypeistä, jolloin parametrit voidaan
jättää usein pois:

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

Toiseksi, *jos lambdalauseke sisältää vain yhden lauseen*, voidaan aaltosulut,
`return`-määreen ja lopettavan puolipisteen jättää pois. Näin syntyy
yksirivinen lambdalauseke:

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

Lopuksi, *jos lambdalausekkeessa on täsmälleen yksi parametri*, voidaan
parametrin ympärillä olevat sulut jättää pois:

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

Lambdalausekkeiden yhteydessä on yleistä käyttää myös tavallista lyhyempiä
parametrien nimiä, sillä parametrien merkitys on tapana dokumentoida
funktiorajapinnassa. Täten yllä oleva voidaan tiivistää lopulliseen muotoon:

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

Lambdalausekkeita on voi käyttää muuttujien lisäksi parametreina.
Tämän myötä on mahdollista tehdä funktioita, jotka käsittelevät muita
funktioita, kuten esimerkiksi:

```java
//-public interface NumeroFunktio {
//-    int laske(int luku);
//-}
//-
/**
 * Laskee kahden funktion summan tietylle arvolle.
 *
 * @param fun1 Ensimmäinen funktio
 * @param fun2 Toinen funktio
 * @param arvo Arvo, josta lasketaan summa
 * @return Funktioiden summa arvolla.
 */
int summaaFunktiot(NumeroFunktio fun1, NumeroFunktio fun2, int arvo) { 
    return fun1.laske(arvo) + fun2.laske(arvo);
}

void main() {
    IO.println("3 * 2 + 3 * 3 = " + 
                summaaFunktiot(x -> x * 2, 
                               x -> x * x, 
                               3));
}
```

Lambdalausekkeiden runko määrittää oman näkyvyysalueen. Erityisesti
lambdalausekkeissa saa käyttää lausekkeiden ulkopuolella näkyviä muuttujia
ja arvoja. Tämä mahdollistaa esimerkiksi funktioita palauttavien funktioiden
tekemisen:

```java
//-public interface NumeroFunktio {
//-    int laske(int luku);
//-}
//-
NumeroFunktio kerroLuvulla(int kerrottava) { 
    // Tämä palauttaa uuden lambdalausekkeen, joka ottaa parametrina luvun
    // ja kertoo tämän funktion parametrina annetulla luvulla.
    return x -> x * kerrottava;
}

NumeroFunktio summa(NumeroFunktio fun1, NumeroFunktio fun2) {
    return x -> fun1.laske(x) + fun2.laske(x);
}

void main() {
    // Funktio, joka laskee x * 2
    NumeroFunktio kerroKahdella = kerroLuvulla(2);
    // Funktio, joka laskee x * 5
    NumeroFunktio kerroViidella = kerroLuvulla(5);
    // Funktio, joka laskee kerroKahdella(x) + kerroViidella(x)
    NumeroFunktio summaFunktio = summa(kerroKahdella, kerroViidella);

    IO.println("2 * 2 = " + kerroKahdella.laske(2));
    IO.println("2 * 5 = " + kerroViidella.laske(2));
    IO.println("2 * 2 + 2 * 5 = " + summaFunktio.laske(2));
}
```

## Esimerkkejä

### Valmiita funktiorajapintoja

Javassa on joukko valmiita yleisiä funktiorajapintoja, jotka löytyvät
`java.util.function`-paketista (ks.
[JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/package-summary.html#class-summary)).

**`Function<T, R>`** ([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/Function.html)) esittää funktiota, joka ottaa yhden parametrin tyyppiä
`T` ja paluttaa parametrin tyyppiä `R`.
Esimerkiksi yllä oleva esimerkki voidaan yksinkertaistaa käyttämällä valmista
`Function`-rajapintaa `NumeroLauseke`-rajapinnan sijaan:

```java
//-void main() {
Function<Integer, Integer> kerroKahdella = x -> x * 2;
Function<Integer, Integer> potenssiinKaksi = x -> x * x;

IO.println(funktio.apply(1));
IO.println(funktio2.apply(2));
//-}
```

`Function`-rajapinta sisältää apumetodeja `andThen` ja `compose`, joiden
avulla funktioita voidaan yhdistää toisiinsa:

```java
//-void main() {
Function<Integer, Integer> kerroKahdella = x -> x * 2;
Function<Integer, Integer> potenssiinKaksi = x -> x * x;

// Palauttaa funktion, joka vastaa kutsua kerroKahdella(potenssiinKaksi(x))
Function<Integer, Integer> kerroJaPotenssiin = kerroKahdella.andThen(potenssiinKaksi);
// Palauttaa funktion, joka vastaa kutsua potenssiinKaksi(kerroKahdella(x))
Function<Integer, Integer> potenssiinJaKerro = kerroKahdella.compose(potenssiinKaksi);

IO.println(kerroJaPotenssiin.apply(2));
IO.println(potenssiinJaKerro.apply(2));
//-}
```

Vastaavasti **`BiFunction<T, U, R>`**
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/BiFunction.html))
vastaa funktiota, joka ottaa kaksi parametria ja paluttaa yhden arvon.

**`Consumer<T>`**
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/Consumer.html))
ja **`BiConsumer<T, U>`**
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/BiConsumer.html))
puolestaan vastaavat metodeja, jotka ottavat yhden tai kaksi parametria eivätkä
palauta mitään arvoa.
Esimerkiksi useat kokoelmat sisältävät `forEach`-funktion, jonka avulla
voidaan toteuttaa yksinkertaista alkioiden käsittelyä:

```java
//-void main() {
List<String> marjoja = List.of("mansikka", "mustikka", "puolukka", "karpalo");

// Huom: IO.println sopii Consumer<T>:hen, 
// koska se ottaa yhden parametrin eikä palauta mitään
marjoja.forEach(IO::println);

// Sama kuin
// for (String marja : marjoja) {
//     IO.println(marja);
// }

Map<String, Integer> arvosanat = new HashMap<>(
            Map.of( "Denis",        1,
                    "Antti-Jussi",  3,
                    "Sami",         5,
                    "Karri",        5)
    );
// Myös lambdalausekkeet ovat OK
arvosanat.forEach((nimi, arvosana) -> IO.println(nimi + " => " + arvosana));
//-}
```

### Comparator-rajapinta

Kuten totesimme ylempänä, toisinaan voi olla vaikeaa valita yksittäinen
järkevä järjestys. 
Yleisestikin, luonnollisen järjestyksen lisäksi voi olla järkevää
pystyä määrittämään *vaihtoehtoisia* järjestystapoja samalle luokalle.

Esimerkiksi, vaikka kokonaislukujen suuruusjärjestys on järkevä luonnolliseksi
järjestykselle, joskus lukuja saatetaan haluta järjestää niiden suuruusluokan
mukaan tai vaikkapa sen mukaan, kuinka lähellä luvut ovat jotakin toista
tiettyä lukua. Vastaavasti, vaikka yllä oleville keräilykorteille voisi olla
järkevää määrätä järjestys tunnisteen mukaan, voi olla mielekästä
pystyä järjestämään niitä kortin nimen mukaan.

Javan `Comparator`-rajapinta
[JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Comparator.html)
tarjoaa tavan määrittää *vaihtoehtoisia* järjestystapoja tyypeille.
Lisäksi rajapinta tarjoaa mahdollisuuden määrittää järjestystapoja
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
// FILE: KerailykorttiSarjaVertailija.java
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
  myös sellaisille luokille, joiden koodia ei voi suoraan muokata (esim.
  Javan sisäänrakennetut luokat).
- Koska `KerailykorttiSarjaVertailija` on oma luokkansa, määritimme `Kerailykortti`-luokkaan
  saantimetodin `getSarja()`.
- Jotta vertailijaa voi käyttää, siitä tulee alustaa olio. Alustuksen jälkeen
  vertailijaolio voidaan käyttää `Collections.sort`-metodin ylikuormituksen
  kanssa, joka joka ottaa `Comparator`-olion toisena parametrina.

> [!VAROITUS]
>
> Yllä olevassa esimerkissä toteutimme `Comparator`-rajapinnan luokassa, jotta esimerkki
> voidaan pitää yksinkertaisena.
> 
> Modernissa Javassa on kuitenkin yleistä, että *vertailuluokkia ei luoda käsin*.
> `Comparator` on nimittäin ns. *funktiorajapinta*, jonka ansiosta mikä tahansa
> luokkametodi, jonka määrittely vastaa `compare`-metodia, voidaan sijoittaa
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
Toisin sanoen, tämä mahdollistaa ns. eristää `Comparable`-rajapintaa
toteuttavan olion `compareTo`-metodin toteutuksen vertailuolioksi.
Esimerkiksi merkkijonojen aakkosjärjestystä vastaavan vertailuolion saa tällä
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
    Comparator<String> kaanteinenAakkosjarjestys = aakkosjarjestys.reversed();
    // HIGHLIGHT_GREEN_END
    Collections.sort(jonoja, kaanteinenAakkosjarjestys);

    IO.println(jonoja);
}
```

Kun olioita vertailee käyttäen luonnollista tai vaihtoehtoista järjestystä,
ei voi olla varma siitä, että `null`-viite on käsitelty järkevästi
tai ollenkaan.
Esimerkiksi jopa Javassa määritelty `String`-merkkijonojen luonnollinen
järjestys ei käsittele tapausta, jos jompikumpi verrattavista merkkijonoista
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
