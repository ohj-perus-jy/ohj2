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
totuusarvon. Tässä ovat yleisimmät vertailuoperaattorit Javassa.

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

 * `&&` (JA / AND): Lauseke on tosi vain, jos molemmat ehdot ovat tosi.

 * `||` (TAI / OR): Lauseke on tosi, jos edes toinen ehdoista on tosi.

 * `!` (EI / NOT): Kääntää totuusarvon päinvastaiseksi (tosi muuttuu epätodeksi).

> [!VAROITUS] 
> Älä sekoita toisiinsa sijoitusoperaattoria `=` ja
> vertailuoperaattoria `==`.
>  * `if (x = 5)` yrittää asettaa x:n arvoksi 5 (virhe)
>  * `if (x == 5)` kysyy, onko x:n arvo 5 (oikein)

## Merkkijonojen vertailu

Toisin kuin primitiivityypeillä (`int`, `double`, jne.), Javassa
`==`-operaattori vertaa olioiden kohdalla viitteitä, eivät sisältöä. Tästä
syystä merkkijonojen sisällön vertailuun tulee käyttää `equals()`-metodia.

```java
void main() {
    String mjono1 = "Slush";
    String mjono2 = new String("Slush"); // Luodaan pakolla uusi olio

    // VÄÄRIN: Vertaa viitteitä -> tulostaa false
    IO.println(mjono1 == mjono2); 

    // OIKEIN: Vertaa olioiden sisältöjä -> tulostaa true
    IO.println(mjono1.equals(mjono2));
}
```

## Ehtolauseet

Ehtolauseilla ohjataan ohjelman kulkua. Ehtolauseiden muodostamiseen tarvitaan
aina yksi tai useampi totuusarvoinen ehtolauseke.

### If-rakenne

Perusmuotoinen ehtolause on if. Sen sisällä oleva koodilohko suoritetaan vain,
jos sulkeissa oleva vertailu on tosi (true). Usein tarvitsemme myös
vaihtoehtoisia reittejä, jolloin käytämme else if ("muuten jos") ja else
("muuten") -rakenteita.

If-lauseiden syntaksi Javassa on seuraavanlainen: 
```java.ignore
if (pisteet >= 90) {
    IO.println("Arvosana: 5");
} else if (pisteet >= 50) {
    IO.println("Arvosana: Läpi");
} else {
    // Suoritetaan, jos mikään yllä olevista ei toteutunut
    IO.println("Arvosana: Hylätty");
}
```

### Switch-rakenne

Kun halutaan verrata yhden muuttujan sisältämää arvoa useisiin yksittäisiin
arvoihin (esimerkiksi valikon valinta), switch-rakenne voi olla selkeämpi kuin
pitkä if-else-ketju.

```java,ignore
int valinta = 2;

switch (valinta) {
    case 1:
        IO.println("Valitsit vaihtoehdon 1");
        break; // Tärkeä: lopettaa suorituksen tässä lohkossa
    case 2:
        IO.println("Valitsit vaihtoehdon 2");
        break;
    default:
        IO.println("Tuntematon valinta");
}
```

### Kolmiarvoinen operaattori

Yksinkertaisissa "joko-tai"-tilanteissa, joissa halutaan sijoittaa arvo
muuttujaan ehdon perusteella, voidaan käyttää kolmiarvoista operaattoria
(*ternary operator*) `?.` Se tiivistää koodia merkittävästi.

Syntaksi: `(ehto) ? arvo_jos_tosi : arvo_jos_epätosi;`

Koodiesimerkki:
```java,ignore
void main() {
    int luku1 = 5;
    int luku2 = 8;
    
    // Luetaan: Jos luku1 on suurempi kuin luku2, 
    // sijoita suurempi-muuttujaan luku1, muuten luku2
    int suurempi = (luku1 > luku2) ? luku1 : luku2;

    IO.println("Suurempi luvuista on: " + suurempi);
}
```

## Silmukat

Silmukoita tarvitaan, kun halutaan suorittaa asioita toistuvasti. Javassa on
neljä päätapaa toteuttaa toistorakenteita: `for`, `for-each`, `while` ja
`do-while`. 

### For

Käytä for-silmukkaa, kun tiedät etukäteen toistojen määrän tai tarvitset
indeksiä (järjestysnumeroa) toiston aikana. Rakenne on seuraava.

``` 
for (alustus; toistoehto; päivitys) {
    // silmukan runko
}
```

Alla on esimerkki summan laskemisesta `for`-silmukassa.

```java
//-void main () {
int[] luvut = {1, 2, 3, 4};
int summa = 0;

// Käydään taulukko läpi indeksien 0, 1, 2, 3 avulla
for (int i = 0; i < luvut.length; i++) {
    summa += luvut[i];
}
IO.println("Summa on: " + summa);
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

For-each-silmukassa on joitain rajoituksia: Et tiedä monennessako alkiossa olet
menossa, etkä voi tehdä muutoksia tietorakenteeseen, kuten poistaa tai lisätä
alkioita.

```java
void main () {
    int[] luvut = {1, 2, 3, 4};
    int summa = 0;

    // "Jokaiselle luvulle taulukossa luvut..."
    for (int luku : luvut) {
        summa += luku;
    }
    IO.println(summa);
}
```

### While

While-silmukka on hyvä valinta silloin, kun et tiedä etukäteen, kuinka monta
kertaa toisto pitää suorittaa. Se jatkuu niin kauan kuin ehto on tosi.
Tyypillinen esimerkki on tietojen lukeminen tiedostosta rivi riviltä tai
pelisilmukka.

```java
import java.util.Scanner; // Tarvitaan syötteen lukemiseen

void main() {
    Scanner lukija = new Scanner(System.in);
    String syote = "";

    IO.println("Tervetuloa peliin! (Kirjoita 'lopeta' poistuaksesi)");

    // Huomaa "!" (EI-operaattori) ja .equals() merkkijonolle
    // Silmukka jatkuu niin kauan kuin syöte EI ole "lopeta"
    while (!syote.equals("lopeta")) {
        IO.print("> ");
        syote = lukija.nextLine(); // Pysähtyy odottamaan käyttäjän kirjoitusta

        IO.println("Kaiku: " + syote);
    }
    
    IO.println("Peli päättyi.");
}
```

### Do-While

Tämä toimii kuten while, mutta yhdellä merkittävällä erolla: silmukan runko
suoritetaan aina vähintään kerran, koska ehto tarkistetaan vasta lopussa.

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

## Tehtävät 

<task>
<task-title>Tehtävä 1.2: Sanojen määrä <points>1 p.</points> </task-title>
<handout>

{{#include ../exercises/1-2-sanojen-maara/handout.md}}

</handout>
<task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa1/tehtava2">Tee tehtävä TIMissä</a></task-link>
</task>

