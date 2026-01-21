# Tyyppiparametrit ja geneerisyys

> [!Osaamistavoitteet]
>
> - Osaat hyödyntää tyyppiparametreja toteuttaaksesi yleiskäyttöisiä eli geneerisiä luokkia ja metodeja

Opimme hyvin varhain, että parametrit mahdollistavat toiston vähentämisen
yleistämällä ohjelman toimintaa erilaisille arvoille.
Esimerkiksi, jos haluaisimme selvittää, missä indeksissä haluttu luku sijaitsee...

```java
//-void main() {
int[] luvut1 = {2, 3, 4};
for (int i = 0; i < luvut1.length; i++) {
    if (luvut1[i] == 3) {
        IO.println("Luku 3 on indeksissä " + i);
        break;
    }
}

int[] luvut2 = {-20, 10, 2, 1};
for (int i = 0; i < luvut2.length; i++) {
    if (luvut2[i] == 2) {
        IO.println("Luku 2 on indeksissä " + i);
        break;
    }
}
//-}
```

...voisimme tehdä funktion, joka ottaa taulukon *parametrina*:

```java
int etsiIndeksi(int[] luvut, int etsittava) {
    for (int i = 0; i < luvut.length; i++)
        if (luvut[i] == etsittava) return i;
    return -1;
}

void main() {
    IO.println("Luku 3 on indeksissä " + etsiIndeksi(new int[] {2, 3, 4}, 3));
    IO.println("Luku 2 on indeksissä " + etsiIndeksi(new int[] {-20, 10, 2, 1}, 2));
}
```

Huomaamme kuitenkin nopeasti, että sama `etsiIndeksi` funktio ei kuitenkaan 
toimi muille lukutyypeille, kuten `byte`, `long` taikka `float`.
Java on kuitekin staattisesti tyypitetty, eli kääntäjän pitää tietää muuttujien
tyypit ennen ohjelman ajamista. Jos siis haluaisimme etsiä muiden taulukkojen
suurimpia arvoja, meidän täytyy edelleen kopioida koodia:

```java
int etsiIndeksiInt(int[] luvut, int etsittava) {
    for (int i = 0; i < luvut.length; i++)
        if (luvut[i] == etsittava) return i;
    return -1;
}

int etsiIndeksiLong(long[] luvut, long etsittava) {
    for (int i = 0; i < luvut.length; i++)
        if (luvut[i] == etsittava) return i;
    return -1;
}

int etsiIndeksiDouble(double[] luvut, double etsittava) {
    for (int i = 0; i < luvut.length; i++)
        if (luvut[i] == etsittava) return i;
    return -1;
}

void main() {
    IO.println("Luku 3 on indeksissä " + etsiIndeksiInt(new int[] {2, 3, 4}, 1));
    IO.println("Luku 2.0 on indeksissä " + etsiIndeksiDouble(new double[] {-10.0, 2.0}, 2.0));
    IO.println("Luku -10 on indeksissä " + etsiIndeksiLong(new long[] {-10L, 5L, 1L}, -10L));
}
```

Huomataan, että yllä olevat funktiot eroavat vain tyyppin perusteella.
Oikeastaan `etsiIndeksi`-funktion perusajatus on aina sama:

```java,ignore
int etsiIndeksi(TYYPPI[] luvut, TYYPPI etsittava) {
    for (int i = 0; i < luvut.length; i++)
        if (luvut[i] == etsittava) return i;
    return -1;
}
```

Jos jotenkin pystyisimme "sijoittamaan" `TYYPPI`:n tilalle haluttu tyyppi,
pystyisimme tekemään `etsiIndeksi`-funktion, joka olisi edelleen 
staattisesti tyypitetty, mutta samalla mahdollistaisi toiston vähentämisen
ennestään.


## Tyyppiparametrit 

Nimensä mukaisesti *tyyppiparametrit* ovat parametrit, jonka arvona ovat
tietotyypit. 
Tyyppiparametrien tarkoitus on vähentää toistoa
tapauksissa, jossa sama koodi toimii *erityyppisille*, luopumatta
staattisen tyypityksen antamista hyödyistä.
Lisäksi tyyppiparametrit mahdollistavat ylimääräisten tyyppimuunnosten
välttämistä jossain tapauksissa.

Tyypiparametreja voidaan määrittää metodeille tavallisten parametrien lisäksi.
Erikoisuutena on, että tyyppiparametreja voidaan myös määritellä luokille.
Yhdessä metodien ja luokkien tyyppiparametrit mahdollistavat
*geneeristä ohjelmointia*, eli tyypistä riippumattomien algoritmien
ja tietorakenteiden ohjelmointia.

### Tyyppiparametrit metodeissa

Javassa metodeihin kuuluvat tyyppiparametrit ilmoitetaan nuolisulkeiden (`<` ja `>`)
välissä *ennen metodin palautustyyppiä*.
Esimerkiksi:

```java
// aliohjelma "tulosta", jolla on yksi tyyppiparametri T 
// ja yksi tavallinen parametri "arvo"
<T> void tulosta(T arvo) {
    IO.println("Moikka, olen '" + arvo + "' ja olen luokan '" + arvo.getClass() + "' olio!");
}

void main() {
    tulosta(1.0);
    tulosta(1);
    tulosta("kissa");
}
```

Kuten tavallisia parametrejakin, myös tyyppiparametreja voi olla useita:

```java
<T1, T2> String yhdista(T1 arvo1, T2 arvo2) {
    return arvo1.toString() + ", " + arvo2.toString();
}

void main() {
    IO.println(yhdista(1, 2)); // T1 = Integer, T2 = Integer
    IO.println(yhdista(true, 1.0)); // T1 = Boolean, T2 = Double
}
```

Tyyppiparametrin nimi seuraa samoja vaatimuksia kuin tavallisen parametrin nimi.
Yleisin *käytäntö* tällä hetkellä lienee, että tyypiparametrin nimi
on yleensä yksi isolla kirjoitettu kirjain, joka on johdettu
tyyppiparametrin merkityksestä, kuten
`T` (**T**ype), `E` (**E**lement), `K` (**K**ey), `N` (**N**umber), 
`V` (**V**alue). Jossain tapauksissa tyyppiparametrien nimeen lisätään
myös numero, kuten `T1`, `T2`, `T3`, jne.

> [!HUOMAUTUS]
>
> Huomaa, että yllä olevissa esimerkeissä tyyppiparametri määritellään, mutta
> tyyppiparametreille ei anneta arvoa kutsuttaessa.
> Tämä voitaisiin kyllä tehdä; esimerkiksi yllä oleva `tulosta`-aliohjelman
> kutsulle voidaan määrittää tarkasti tyyppiparametrin tyyppi:
>
> ```java
> //-<T> void tulosta(T arvo) {
> //-    IO.println("Moikka, olen '" + arvo + "' ja olen luokan '" + arvo.getClass() + "' olio!");
> //-}
> //-
> void main() {
>     this.<Double>tulosta(1.0); // sama kuin tulosta(1.0)
>     this.<String>tulosta("kissa"); // tulosta("String")
> }
> ```
>
> Vaikka Java on staattisesti tyypitetty, Javan kääntäjä osaa *päätellä*
> tyyppiparametrien arvoja kontekstin perustella.
> Esimerkiksi `tulosta(1.0)`-kutsun `1.0`-lausekkeen tyyppi on `double`, joten
> Java osaa päätellä, että tyyppiparametrin `T` arvoksi on asetettava `Double`-tyyppi.
>
> Java osaa päätellä tyyppiparametrien arvoja melko hyvin. On kuitenkin hyvä
> pitää mielessä, että tyypiparametrille annetaan arvo, vaikka sitä ei aina näe.

Palataan vielä aiempaan `etsiIndeksi`-esimerkkiin.
Käyttäen tyypiparametreja ja pienellä muutoksella voimme vähentää toistoa:

```java
<T> int etsiIndeksi(T[] luvut, T etsittava) {
    for (int i = 0; i < luvut.length; i++)
        if (luvut[i].equals(etsittava)) return i;
    return -1;
}

void main() {
    IO.println("Luku 3 on indeksissä " + etsiIndeksi(new Integer[] {2, 3, 4}, 1));
    IO.println("Luku 2.0 on indeksissä " + etsiIndeksi(new Double[] {-10.0, 2.0}, 2.0));
    IO.println("Luku -10 on indeksissä " + etsiIndeksi(new Long[] {-10L, 5L, 1L}, -10L));
}
```

Huomaa, että jouduimme tekemään erityisesti pari muutosta:

* `luvut[i] == etsittava` sijaan jouduimme käyttämään viitetietotyyppimuuttujien
  yhtäsuuruuden vertailua `luvut[i].equals(etsittava)`;
* `main`-pääohjelmassa joudumme käyttämään perustietotyyppien `int`, `double` ja
 `long` sijaan käärijäluokkia `Integer`, `Double` ja `Long`.
   
Tämä johtuu Javan tyyppiparametrien eräästä oleellisesta rajoittesta:
**vain viitetietotyyppejä voidaan välittää tyyppiparametreihin**.
Rajoite puolestaan johtuu Javan tavasta toteuttaa viitetietotyyppejä; muissa 
ohjelmointikielissä samaa rajoitetta ei välttämättä ole.
Mainittakoon, että Java-kieltä kehitetään ja on hyvin mahdollista, että
lähitulevaisuudessa tämä rajoite jää pois.

### Tyyppiparametrit luokissa ja rajapinnoissa

Tyyppiparametrien todellinen hyöty tapana tuottaa yleistä koodia ilmenee,
kun tyyppiparametreja määrittää luokalle tai rajapinnalle.
Olemmekin jo käyttäneet kurssilla tyyppiparametreja valmiissa luokissa, kuten
`ArrayList<T>`.

DZ: Joku yksinkertainen esimerkki? Vaikkapa Osassa 1 oleva salasanatehtävä,
mutta se palauttaisi `Tulos(boolean oikein, String virhe)`. Se refaktoroidaan
luokaksi `Pari<T, U>`.

## Tyypiparametrit ja polymorfismi

- Näitä on käytetty mm. listoissa `List<Integer>`
- Mitä geneerisyydellä (generic programming / generics) tarkoitetaan?

- Viittaus edellisen osan polymorfismiasiaan
  - Polymorfismi olio-ohjelmoinnissa tarkoittaa tyypillisesti nimenomaan alityypitystä
- Tyyppiparametrit ja geneerisyys ovat myös polymorfismia, sillä periaate on sama:
  - Mahdollistaa, että yksi arvon tyyppi edustaa useita eri tyyppejä
    - Voi luoda luokkia, rajapintoja ja metodeita jotka hyödyntävät ulkopuolelta (muualta koodista) tulevia arvoja määrittämättä tarkkaa tyyppiä etukäteen.
  - Parametrinen polymorfismi

- Miksi tyyppiparametrit ja geneerisiä tyyppejä (tyyppiparametrisoituja luokkia tai rajapintoja), kun on jo polymorfismi alityypeillä?

- Tarkastellaan metodin parametrin yhteydessä hieman luokkaa `Object`, joka itsessään on "geneerinen", eli yleinen luokka — (kertauksena) kaikki Javan luokat perivät `Object`-luokan eli ovat tyyppiä `Object`.

```java
void main() {
    printWithType(new Object());
    printWithType("tekstiä");
    printWithType(1);
    printWithType(1.0);
}

void printWithType(Object value) {
    System.out.println("Arvo: " + value + ", Tyyppi: " + value.getClass().getSimpleName());
}
```

- Vastaava geneerinen metodi tyyppiparametrilla `T`:

```java
void main() {
    printWithType(new Object());
    printWithType("tekstiä");
    printWithType(1);
    printWithType(1.0);
}

<T> void printWithType(T value) {
    System.out.println("Arvo: " + value + ", Tyyppi: " + value.getClass().getSimpleName());
}
```

- `<T>` syntaksi tuttu esimerkiksi listoista: `List<String> = new ArrayList()<>`.

- Ylemmänkaltaisessa käyttötapauksessa ei vielä eroa.

- Katsotaan seuraavaksi seuraavaksi potentiaalista ongelmaa ohjelmakoodin toteutuksessa alityyppien avulla. Samalla tutustumme _rajoitettuihin_ tyyppiparametreihin.

- Pelkkä alityypitys mahdollistaa:

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    int suurempi = getLargest("1", "2")); // kääntäjälle ok
    System.out.println("Suurempi: " + getLargest("5", 4)); // kääntäjälle ok
}

Comparable getLargest(Comparable a, Comparable b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}
```

- Jos Stream API käyty, heitto [sorted()](https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html#sorted--)-metodiin, jolle kelpaa mikä tahansa tyyppi `olio.stream().sorted().toList()` -> vasta ajonaikainen eikä käännöksenaikainen virhe

-> Ajonaikainen virhe, halutaan yleensä välttää sillä näissä on aina riski päätyä loppukäyttäjälle

- Tyyppiparametrien avulla (ja niiden järkevällä käytöllä) tämänkaltainen metodin väärinkäyttö havaitaan varmasti ajoissa

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    int suurempi = getLargest("1", "2")); // virhe havaitaan viimeistään kääntäessä
    System.out.println("Suurempi: " + getLargest(3, "5")); // virhe havaitaan viimeistään kääntäessä
}

<T extends Comparable> T getLargest(T a, T b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}

- Javan `Comparable` on _geneerinen luokka_ ja ottaa tyyppiparametrin, joten oikeampi käyttö olisi

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    int suurempi = getLargest("1", "2")); // virhe havaitaan viimeistään kääntäessä
    System.out.println("Suurempi: " + getLargest(3, "5")); // virhe havaitaan viimeistään kääntäessä
}

<T extends Comparable<T>> T getLargest(T a, T b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}

- Rajoitettuja tyyppiparametreja voi olla useampia, esim.

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    String suurempi = getLargest("1", "2")); // virhe havaitaan viimeistään kääntäessä
}

<T extends Comparable<T> & Number> T getLargest(T a, T b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}

Tästä päästäänkiin geneerisiin luokkiin ja rajapintoihin.

- Klassinen esimerkki geneerisestä :

```java
class Pair<T> {
    private T first;
    private T second;

    public Pair(T first, T second) {
        this.first = first;
        this.second = second;
    }

    public T getFirst() {
        return first;
    }

    public T getSecond() {
        return second;
    }

    public void setFirst(T first) {
        this.first = first;
    }

    public void setSecond(T second) {
        this.second = second;
    }
}
```

Tyyppiparametreja voi olla useampi

```java
class Pair<T, U> {
    private T first;
    private U second;

    public Pair(T first, U second) {
        this.first = first;
        this.second = second;
    }

    public T getFirst() {
        return first;
    }

    public U getSecond() {
        return second;
    }

    public void setFirst(T first) {
        this.first = first;
    }

    public void setSecond(U second) {
        this.second = second;
    }
}
```


- Geneerisen metodin syntaksi (geneeriset esimerkit vasta ongelman havainnollistuksen jälkeen vai samassa?)
- Tyyppirajoitukset (tämä vasta myöhemmin vai Comparable-esimerkin kanssa?

- Tyyppiparametrit mahdollistavat eritasoista tyyppitarkastusta ja yleiskäyttöisen koodin kehittämistä kuin mitä pelkällä alityypityksellä on mahdollista

- Esimerkkejä milloin geneeriset tyypit ovat kivoja metodeissa
  - Identtinen overloadaus eri tyypeille
    - tässä myös miksi overloadaus on myös polymorfismia?

- Tehtäviä geneerisistä metodeista

- Esimerkkejä milloin geneeriset tyypit ovat kivoja luokissa
- Geneerisen luokan syntaksi

- Tehtäviä geneerisistä luokista

- Ekstrana: jokerimerkki `?` tyyppiparametreissa
  - rajoitetut jokerimerkit
    - `extends` ja `super`
  - `?` sama kuin `? extends Object`
  - Tutkitaan mitä `Collections.sort`

- Ekstramaininta: Javassa geneeriset tyypit muuten ohjelman kääntämisen aikana rajoituksen tyypiksi tai tyypiksi `Object`
- Ekstramaininta: (koska vain Java -asia): Geneerinen tyyppi ei voi olla primitiivi

- Ei unionityyppejä (kuten esimerkiksi Rustissa), täytyy tehdä luokka esim. StringOrInt

```java
class StringOrInt {
    private final Object value;

//    public StringOrInt(Object value) {  // ei näin -> ajonaikaiset virheet voidaan estää helposti kahdella konstruktorilla
//        if (!(value instanceof String) && !(value instanceof Integer)) {
//            throw new IllegalArgumentException("Value must be a String or an Integer");
//        }
//        this.value = value;
//    }

    public StringOrInt(String value) {
        this.value = value;
    }

    public StringOrInt(Integer value) {
        this.value = value;
    }

    public Object getValue() {
        return value;
    }

    public String getStringValue() {
        if (value instanceof String s) {
            return s;
        } else if (value instanceof Integer i) {
            return Integer.toString(i);
        } else {
            throw new IllegalStateException("Value is neither String nor Integer");
        }
    }

    public boolean isString() {
        return value instanceof String;
    }

    public boolean isInteger() {
        return value instanceof Integer;
    }

    public int getIntValue() {
        if (value instanceof Integer i) {
            return i;
        } else if (value instanceof String s) {
            try {
                return Integer.parseInt(s);
            } catch (NumberFormatException e) {
                throw new IllegalStateException("String value cannot be parsed to Integer");
            }
        } else {
            throw new IllegalStateException("Value is neither String nor Integer");
        }
    }
}
```

- Menee kikkailuksi, parempi tyytyä rajapintoihin ja abstrakteihin luokkiin
