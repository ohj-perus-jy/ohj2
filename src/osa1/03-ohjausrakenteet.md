# Ohjausrakenteet ja perustietorakenteet

> [!Osaamistavoitteet]
>
> - Ehtolauseet (`if`, `switch`)
> - Toistolauseet (`for`, `while`, `do-while`), ja listatyyppiset tietorakenteet
> - Tiedostat, että Javassa merkkijonot verrataan `equals`-aliohjelmalla eikä `==`

Ohjelmointi on harvoin pelkkää koodirivien suorittamista peräkkäin. Jotta
ohjelmista saadaan hyödyllisiä, niiden täytyy pystyä tekemään päätöksiä,
toistamaan asioita ja hallinnoimaan tietoa järkevästi. Tässä luvussa käymme läpi
Javan logiikan, toistorakenteet sekä kaksi tapaa säilöä tietoa: perinteiset
taulukot ja joustavat listat. 

## Vertailuoperaattorit

Ennen kuin voimme opettaa ohjelmaa tekemään valintoja ("jos tämä, niin tuo"),
meidän täytyy ymmärtää, miten tietokone näkee maailman. Tietokoneen logiikka on
binääristä: väittämät ovat joko totta (true) tai epätotta (false).
Vertailuoperaattorit ovat kuin kysymyksiä, jotka palauttavat vastaukseksi
totuusarvon. Tässä ovat yleisimmät vertailuoperaattorit Javassa:

| Operaattori | Merkitys                | Esimerkki (kun x=5, y=3) | Tulos |
| ----------- | ----------------------- | ------------------------ | ----- |
| ==          | Yhtä suuri kuin         | x == y                   | false |
| !=          | Eri suuri kuin          | x != y                   | true  |
| >           | Suurempi kuin           | x > y                    | true  |
| <           | Pienempi kuin           | x < 4                    | false |
| >=          | Suurempi tai yhtä suuri | x >= 5                   | true  |
| <=          | Pienempi tai yhtä suuri | y <= 3                   | true  |

Usein päätökset riippuvat useammasta kuin yhdestä asiasta. Esimerkiksi: "Menen
ulos, JOS ei sada JA minulla on vapaa-aikaa". Tätä varten tarvitsemme loogisia
operaattoreita yhdistämään ehtoja.

 * && (JA / AND): Lauseke on tosi vain, jos molemmat ehdot ovat tosi.

 * || (TAI / OR): Lauseke on tosi, jos edes toinen ehdoista on tosi.

 * ! (EI / NOT): Kääntää totuusarvon päinvastaiseksi (tosi muuttuu epätodeksi).

> [!VAROITUS] 
> Älä sekoita toisiinsa sijoitusoperaattoria `=` ja
> vertailuoperaattoria `==`.
>  * `if (x = 5)` yrittää asettaa x:n arvoksi 5 (virhe)
>  * `if (x == 5)` kysyy, onko x:n arvo 5 (oikein)

## Merkkijonojen vertailu

Toisin kuin primitiivisillä tyypeillä (`int`, `double`, jne.), Javassa
`==`-operaattori vertaa olioiden kohdalla viitteitä, eivät sisältöä. Tästä
syystä merkkijonojen sisällön vertailuun tulee käyttää `equals()`-metodia.

```java
void main() {
    String mjono1 = "Slush";
    String mjono2 = new String("Slush"); // Luodaan pakolla uusi olio

    // VÄÄRIN: Vertaa muistiosoitteita -> tulostaa false
    System.out.println(mjono1 == mjono2); 

    // OIKEIN: Vertaa sisältöä -> tulostaa true
    System.out.println(mjono1.equals(mjono2));
}
```

## Ehtolauseet

Kun osaamme muodostaa ehtoja, voimme käyttää niitä ohjaamaan koodin suoritusta.

### If-rakenne

Perusmuotoinen ehtolause on if. Sen sisällä oleva koodilohko suoritetaan vain, jos sulkeissa oleva vertailu on tosi (true). Usein tarvitsemme myös vaihtoehtoisia reittejä, jolloin käytämme else if (muuten jos) ja else (muuten) -rakenteita.

If-lauseiden syntaksi Javassa on seuraavanlainen: 
```java.ignore
if (pisteet >= 90) {
    System.out.println("Arvosana: 5");
} else if (pisteet >= 50) {
    System.out.println("Arvosana: Läpi");
} else {
    // Suoritetaan, jos mikään yllä olevista ei toteutunut
    System.out.println("Arvosana: Hylätty");
}
```

### Switch-rakenne

Kun meillä on yksi muuttuja, jota halutaan verrata useisiin yksittäisiin
arvoihin (esimerkiksi valikon valinta), switch-rakenne voi olla selkeämpi kuin
pitkä if-else if -ketju.

```java,ignore
int valinta = 2;

switch (valinta) {
    case 1:
        System.out.println("Valitsit vaihtoehdon 1");
        break; // Tärkeä: lopettaa suorituksen tässä lohkossa
    case 2:
        System.out.println("Valitsit vaihtoehdon 2");
        break;
    default:
        System.out.println("Tuntematon valinta");
}
```

### Kolmiarvoinen operaattori

Yksinkertaisissa "joko-tai" -tilanteissa, joissa halutaan sijoittaa arvo
muuttujaan ehdon perusteella, voidaan käyttää kolmiarvoista operaattoria
(*ternary operator*) `?.` Se tiivistää koodia merkittävästi.

Syntaksi: `(ehto) ? arvo_jos_tosi : arvo_jos_epätosi;`

Koodiesimerkki:
```java,ignore
void main() {
    int luku1 = 5;
    int luku2 = 8;
    
    // Perinteisen if-else -rakenteen sijaan voimme kirjoittaa:
    int suurempi = (luku1 > luku2) ? luku1 : luku2;

    System.out.println("Suurempi luvuista on: " + suurempi);
}
```


## Silmukat

Javassa on neljä päätapaa toteuttaa toistoja eli "looppeja". 

### For

Käytä for-silmukkaa, kun tiedät etukäteen toistojen määrän tai tarvitset
indeksiä (järjestysnumeroa) toiston aikana.

Rakenne: 

``` 
for (alustus; toistoehto; päivitys) {
    // silmukan runko
}
```

Alla esimerkki summan laskemisesta `for`-silmukassa.

```java
//-void main () {
int[] luvut = {1, 2, 3, 4};
int summa = 0;

// Käydään taulukko läpi indeksien 0, 1, 2, 3 avulla
for (int i = 0; i < luvut.length; i++) {
    summa += luvut[i];
}
System.out.println("Summa on: " + summa);
//-}
```

Alustus, toistoehto ja päivitys voidaan periaatteessa jättää jopa tyhjiksi,
mutta puolipisteiden on pakko olla paikallaan. For-silmukalla voidaan tehdä
ikuinen silmukka jättämällä toistoehto tyhjäksi, joskin tämä on harvoin
tarkoituksenmukaista.

### For-Each

For-each-silmukka on usein luettavin ja myös turvallisin tapa käydä läpi koko
tietorakenne. Kun et tarvitse indeksiä etkä aio muokata rakenteen kokoa, käytä
for-each-silmukkaa.

Rajoitukset: Et tiedä monennessako alkiossa olet menossa, etkä voi korvata
alkiota toisella silmukan sisällä.

```java
void main () {
    int[] luvut = {1, 2, 3, 4};
    int summa = 0;

    // "Jokaiselle luvulle taulukossa luvut..."
    for (int luku : luvut) {
        summa += luku;
    }
    System.out.println(summa);
}
```

### While

While-silmukka on paras valinta silloin, kun et tiedä etukäteen, kuinka monta
kertaa toisto pitää suorittaa. Se jatkuu niin kauan kuin ehto on tosi.
Tyypillinen esimerkki on tietojen lukeminen tiedostosta rivi riviltä tai
pelisilmukka.


```java
import java.util.Scanner; // Tarvitaan syötteen lukemiseen

void main() {
    Scanner lukija = new Scanner(System.in);
    String syote = "";

    System.out.println("Tervetuloa peliin! (Kirjoita 'lopeta' poistuaksesi)");

    // Huomaa "!" (EI-operaattori) ja .equals() merkkijonolle
    // Silmukka jatkuu niin kauan kuin syöte EI ole "lopeta"
    while (!syote.equals("lopeta")) {
        System.out.print("> ");
        syote = lukija.nextLine(); // Pysähtyy odottamaan käyttäjän kirjoitusta

        System.out.println("Kaiku: " + syote);
    }
    
    System.out.println("Peli päättyi.");
}
```

### Do-While

Tämä toimii kuten while, mutta yhdellä merkittävällä erolla: silmukan runko suoritetaan aina vähintään kerran, koska ehto tarkistetaan vasta lopussa.

Do-while on ainoa silmukka, jonka lopettavaan sulkeeseen tulee puolipiste. Alla
pseudokoodina esimerkki, jossa omenan sijainti arvotaan uudestaan, jos se on
liian lähellä pelaajaa.

```java,ignore
void main () {
    Vector2D pelaajanSijainti = new Vector2D(0, 0);
    Vector2D omenanSijainti = new Vector2D(0, 0);
    do {
        // Arvo omenalle uusi sijainti
        omenanSijainti.x = Math.random() * 10;
        omenanSijainti.y = Math.random() * 10;        
        // Jos omena on liian lähellä pelaajaa, arvotaan uudestaan
    } while (omenanSijainti.distanceTo(pelaajanSijainti) < 2.0);
}
```

## Taulukot

Edellisissä silmukkaesimerkeissä käytimme jo tietotyyppiä `int[]`. Kyseessä on
taulukko (engl. *array*), joka on yksi tapa säilöä useita arvoja yhden muuttujan
alle.

Taulukko on kuin lokerikko: kun se on rakennettu, siinä on tietty määrä
lokeroita, eikä määrää voi muuttaa. Jokaisessa lokerossa on tietty indeksi
(numero), joka alkaa aina nollasta.

```java
// Tapa 1: Luodaan taulukko ja annetaan arvot heti
int[] luvut = {10, 20, 30, 40}; 

// Tapa 2: Varataan tilaa 5:lle merkkijonolle (aluksi tyhjiä)
String[] nimet = new String[5]; 

nimet[0] = "Matti"; // Ensimmäinen lokero
nimet[1] = "Teppo"; // Toinen lokero

System.out.println("Taulukon pituus: " + nimet.length);
```

valinta silloin, kun tiedät varmasti datan määrän etukäteen. Jos haluamme lisätä
tietorakenteeseen tietoa ohjelman ajon aikana, parempi vaihtoehto on käyttää
listoja.

Lue lisää taulukoista Javan dokumentaatiosta: <https://docs.oracle.com/javase/tutorial/java/nutsandbolts/arrays.html>

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
