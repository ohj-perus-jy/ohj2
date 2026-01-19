# Funktiorajapinnat ja lambda-lausekkeet

> [!VAROITUS]
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Funktionaalinen ohjelmointi
> - Funktionaalinen rajapinta ja Javan `Function`, `BiFunction`
> - lambda-lausekkeet


### Esimerkki: Comparator-rajapinta

> [!WIP]
>
> Tämä osio on kirjoitettava hieman uusiksi lambdoja ja funktioviitteitä
> käyttäen. 
> `Comparator`-rajapintaa käytetään Javassa nykyään aikalailla vain funktiorajapintana.
> 

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
