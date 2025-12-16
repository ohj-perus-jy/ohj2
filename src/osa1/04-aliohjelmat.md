# Aliohjelmat

> [!Osaamistavoitteet]
>
> - Käsitellään dataa funktioiden avulla (Ohj1-kurssin tapaan)
> - Funktiot (määrittely, kirjoitusasu, palautusarvot, ehkä hieman datan käsittelyä kertauksena)
> - Ymmärrät Javan perustietotyyppien ja viitetyyppien eron funktion kutsussa (oliot ovat aina viitteen takana)
> - Dokumentaatiokommentit
> - Osaat kirjoittaa Ohjelmointi 1 -kurssin tapaisia ohjelmia Javalla

Aliohjelma on ohjelman osa, joka suorittaa tietyn tehtävän. Aliohjelmat helpottavat ohjelman jäsentämistä, sillä niiden avulla ohjelma voidaan jakaa pienempiin, hallittavampiin osiin. Aliohjelmat helpottavat myös uudelleenkäyttöä, sillä samaa aliohjelmaa voidaan kutsua useita kertoja eri kohdissa ohjelmaa ilman, että koodia tarvitsee kirjoittaa uudelleen. 

Aliohjelmia kutsutaan joskus myös funktioiksi, ja olio-ohjelmoinnin yhteydessä myös metodeiksi. Nimeäminen riippuu kontekstista, mutta tässä yhteydessä käytämme termiä aliohjelma.

Aliohjelma voi ottaa vastaan *syötteitä*, joita sanotaan *parametreiksi*. Tehtävän suoritettuaan aliohjelma voi palauttaa tuloksen. Kutsutaan alla `Keskiarvo`-aliohjelmaa, joka laskee kokonaislukujen joukon keskiarvon. Tässä siis parametrina annetaan yksi kokonaislukutaulukko, ja aliohjelma palauttaa keskiarvon `double`-tyyppisenä arvona.

```java
void main () {
    int[] luvut = {4, 8, 15, 16, 23, 42};
    double keskiarvo = Keskiarvo(luvut);
    IO.println("Lukujen keskiarvo on: " + keskiarvo);
}

public static double Keskiarvo(int[] luvut) {
    if (luvut.length == 0) {
        return 0; 
    }
    double summa = 0;
    for (int luku : luvut) {
        summa += luku;
    }
    return summa / luvut.length;
}
```

## Aliohjelman määrittelyrivi

Aliohjelman ensimmäistä riviä kutsutaan *määrittelyriviksi*. Määrittelyrivissä on seuraavat osat:

 * Julkisuus ja staattisuus (esimerkissämme `public static`): Kertovat, että metodi on kaikkien käytettävissä ja toimii ilman olioita. Nämä osat vaihtelevat tai voivat jopa puuttua sen mukaan, missä kontekstissa aliohjelmaa käytetään. Ilman olioita toimivat aliohjelmat määritellään kuitenkin yleensä juuri näin.
 * Paluuarvon tyyppi (`double`): Kertoo, minkä tyyppistä tietoa metodi palauttaa. Jos metodi ei palauta mitään, tyyppi on `void`. Paluuarvon tyyppi voi olla mikä tahansa Javan perustietotyyppi tai olio.
 * Aliohjelman nimi (`Keskiarvo`): Kertoo mitä aliohjelma tekee. Nimen tulee olla kuvaava ja noudattaa Javan nimeämiskäytäntöjä sekä [tämän kurssin tyyliohjetta](../tyyliohje.md).
 * Parametrit (`int[] luvut`): Sulkeiden sisään määritellään muuttujat, jotka aliohjelma tarvitsee toimiakseen.

## Paluuarvot ja datan käsittely

Aliohjelmaa voi ajatella *mustana laatikkona*: sinne syötetään raaka-ainetta (parametrit), laatikon sisällä tapahtuu prosessointia, ja lopuksi ulos tulee valmis tuote (paluuarvo). Avainsana `return` lopettaa metodin suorituksen välittömästi ja palauttaa arvon kutsujalle. Arvon tyypin on vastattava metodin määrittelyssä annettua tyyppiä.

Toisen tekemää aliohjelmaa käytettäessä emme välttämättä tiedä, mitä laatikon sisällä tapahtuu, vaan luotamme siihen, että se toimii määritellyllä tavalla. Tämä on tyypillistä ohjelmoinnissa, jossa käytämme valmiita kirjastoja ja aliohjelmia. 

## Void-aliohjelma

Joskus metodia tarvitaan vain tekemään jokin toimenpide, kuten tulostamaan tekstiä ruudulle, tai aiheuttamaan muu sivuvaikutus. Tällaisessa tapauksessa aliohjelman ei tarvitse palauttaa arvoa. Tällöin paluuarvon tyypiksi merkitään `void`.

## Parametrin välitys: alkeistietotyypit ja viitetyypit

On tärkeää ymmärtää, mitä itse asiassa annamme aliohjelmalle parametrina kun kutsumme sitä. Javassa kaikki parametrit välitetään arvona (ns. *pass-by-value*), mutta välitettävän arvon luonne riippuu parametrin tyypistä.

 * Jos parametrin tyyppi on alkeistietotyyppi (kuten `int`, `double`, `char`, `boolean`), aliohjelmalle annetaan *kopio alkuperäisestä arvosta*.
 * Jos parametrin tyyppi on viitetyyppi (kuten taulukko tai olio), aliohjelmalle annetaan *kopio viitteestä olioon*. 

Kun alkeistietotyyppi (ks. [Luku 1.2](02-muuttujat-ja-tietotyypit.md)) annetaan parametrina metodille, kyseisen muuttujan arvo kopioidaan ja välitetään kutsuttavalle aliohjelmalle. Jos aliohjelma muuttaa tätä kopiota, alkuperäinen muuttuja ei muutu. Alla esimerkki, jossa annamme `int`-tyyppisen muuttujan parametrina. 

```java
public static void yritaMuuttaa(int luku) {
    luku = 99; // Muutetaan vain kopiota
    System.out.println("Metodissa: " + luku);
}

public static void main(String[] args) {
    int x = 10;
    yritaMuuttaa(x);
    System.out.println("Mainissa: " + x); // Tulostaa edelleen 10
}
```

Javassa kaikki tyypit, mitkä eivät ole alkeistietotyyppejä, ovat *viitetyyppejä*. Tässä vaiheessa opintoja tutuimpia viitetyyppejä ovat taulukot (esim. `int[]`) ja `String`-oliot. Myös kaikki itse määritellyt oliot, joihin tutustutaan Luvussa 3, ovat viitetyyppejä. 

Viitetyypin muuttuja ei sisällä itse dataa (kuten taulukon lukuja), vaan viitteen olioon, joka sisältää datan. Voi ajatella, että muuttuja on kaukosäädin, ja itse data on televisio. Ihan kuten televisiota ohjaillaan kaukosäätimellä, viitetyyppisiä muuttujia käytetään olion sisältämän datan käsittelyyn. 

Analogiamme hieman hajoaa tässä kohden, mutta viedään se silti loppuun, kun kerran aloitimme: Kun viitetyyppi annetaan parametrina aliohjelmalle, kopioidaan viite; siis kopio kaukosäätimestä, eikä alkuperäistä kaukosäädintä. Aliohjelma saa kyllä käyttöönsä samanlaisen ``kaukosäätimen'', joka osoittaa samaan ``televisioon'' kuin pääohjelman kaukosäädin. Jos aliohjelma sitten muokkaa olion sisältöä (esim. taulukon alkioita) viitteen kautta, muutos näkyy myös pääohjelmassa. Alla esimerkki tällaisesta tilanteesta, jossa annamme `int[]`-tyyppisen taulukon parametrina, ja aliohjelma muokkaa taulukon alkioita.

```java
public static void nollaaTaulukko(int[] taulukko) {
    // Tämä muutos tapahtuu alkuperäiselle taulukolle!
    // Koska "taulukko"-muuttuja viittaa samaan olioon.
    for (int i = 0; i < taulukko.length; i++) {
        taulukko[i] = 0;
    }
}

public static void main(String[] args) {
    int[] luvut = {1, 2, 3};
    
    nollaaTaulukko(luvut);
    
    // Alkuperäinen taulukko on muuttunut
    System.out.println(luvut[0]); // Tulostaa 0
}
```

Aliohjelmaa, joka muokkaa parametrina annettua oliota, sanotaan usein aiheuttavan *sivuvaikutuksia*. Sivuvaikutukset voivat olla hyödyllisiä, mutta ne voivat myös tehdä ohjelmasta vaikeammin ymmärrettävän. Siksi on erittäin tärkeää olla tietoinen siitä, miten aliohjelmat käsittelevät parametreja.

## B1
- Tehtävänäsi on Monty hallin ongelman simulointi neljällä ovella. Jos ongelma ei ole tuttu, 

Monty hallin ongelma neljällä ovella:
Kilpailijalla on edessään neljä ovea. Yhden oven takana on palkinto ja muiden ovien takana ei ole mitään. Kilpailija valitsee yhden ovista, jonka jälkeen juontaja paljastaa yhden ovista, jonka takana ei ole mitään. Kannattaako kilpailijan vaihtaa ovea suljettuun oveen, vai pitäytyä alkuperäisessä valinnassa?

Tehtävänäsi on simuloida molemmat vaihtoehdot:
1. Kilpailija pitäytyy alkuperäisessä valinnassaan
2. Kilpailija vaihtaa johonkin jäljellä olevista ovista, jotka eivät ole vielä auki ja joka ei ollut kilpailijan ensimmäinen valinta

ja valita vaihtoehdoista se, jolla voittaa todennäköisimmiten.

## B2
- Vakioaikainen haku taulukosta. Esimerkiksi, että kuinka monta päivää on kuukaudessa?

(Teoriatausta se, että laskennallista nopeutta voidaan lisätä käyttämällä enemmän muistia. Tähän esimerkiksi HashMap perustuu)

## B3
- Raa-alla voimalla sanakirjahyökkäys salasanaa vastaan?

## G1

- Linkitetty lista käänteiseksi?

## G2

- Neliömatriisin eli n x n, n $\in \mathbb{N}$ matriisin pyöräyttäminen 90-astetta. 
- In ([[1,2],[3,4]], oikealle) --> [[3,1],[4,2]]