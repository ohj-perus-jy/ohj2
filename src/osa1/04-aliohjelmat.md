# Aliohjelmat

> [!Osaamistavoitteet]
>
> - Käsitellään dataa funktioiden avulla (Ohj1-kurssin tapaan)
> - Funktiot (määrittely, kirjoitusasu, palautusarvot, ehkä hieman datan käsittelyä kertauksena)
> - Ymmärrät Javan perustietotyyppien ja viitetyyppien eron funktion kutsussa (oliot ovat aina viitteen takana)
> - Dokumentaatiokommentit
> - Osaat kirjoittaa Ohjelmointi 1 -kurssin tapaisia ohjelmia Javalla

## Aliohjelmat

Aliohjelma on itsenäinen koodinpätkä, joka suorittaa tietyn tehtävän. Aliohjelmat helpottavat ohjelman jäsentämistä ja uudelleenkäyttöä. Aliohjelma voi ottaa vastaan syötteitä, suorittaa tehtävänsä ja palauttaa tuloksen. Aliohjelmia kutsutaan joskus myös funktioiksi, ja olio-ohjelmoinnin yhteydessä myös metodeiksi. Nimeäminen riippuu kontekstista, mutta tässä yhteydessä käytämme termiä aliohjelma.

Kutsutaan `Keskiarvo`-aliohjelmaa, joka laskee lukujoukon keskiarvon:

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

Aliohjelman ensimmäistä riviä kutsutaan *määrittelyriviksi*. Määrittelyrivissä on seuraavat osat:

 * Julkisuus ja staattisuus (esimerkissämme `public static`): Kertovat, että metodi on kaikkien käytettävissä ja toimii ilman olioita. Nämä osat vaihtelevat tai voivat jopa puuttua sen mukaan, missä kontekstissa aliohjelmaa käytetään. Ilman olioita toimivat aliohjelmat määritellään kuitenkin yleensä juuri näin.
 * Paluuarvon tyyppi (`double`): Kertoo, minkä tyyppistä tietoa metodi palauttaa. Jos metodi ei palauta mitään, tyyppi on `void`. Paluuarvon tyyppi voi olla mikä tahansa Javan perustietotyyppi tai olio.
 * Aliohjelman nimi (`Keskiarvo`): Kertoo mitä aliohjelma tekee. Nimen tulee olla kuvaava ja noudattaa Javan nimeämiskäytäntöjä sekä [tämän kurssin tyyliohjetta](../tyyliohje.md).
 * Parametrit (`int[] luvut`): Sulkeiden sisään määritellään muuttujat, jotka aliohjelma tarvitsee toimiakseen.

## Paluuarvot ja datan käsittely

Aliohjelmaa voi ajatella *mustana laatikkona*: sinne syötetään raaka-ainetta (parametrit), laatikon sisällä tapahtuu prosessointia, ja lopuksi ulos tulee valmis tuote (paluuarvo).

**Return-komento**

Avainsana `return` lopettaa metodin suorituksen välittömästi ja palauttaa arvon kutsujalle. Arvon tyypin on vastattava metodin määrittelyssä annettua tyyppiä.

**Void-aliohjelma**

Joskus metodia tarvitaan vain tekemään jokin toimenpide, kuten tulostamaan tekstiä ruudulle, tai aiheuttamaan muu sivuvaikutus. Tällaisessa tapauksessa aliohjelman ei tarvitse palauttaa arvoa. Tällöin paluuarvon tyypiksi merkitään `void`.

## Javan perustietotyypin ja viitetyyppien ero funktion kutsussa

Yksi Javan tärkeimmistä ominaisuuksista on ymmärtää, miten tieto liikkuu, kun kutsumme metodia. Tämä riippuu siitä, onko kyseessä alkeistietotyyppi vai viitetietotyyppi.

Alkeistietotyypit (Primitive Types)
Alkeistietotyyppejä ovat mm. int, double, boolean, char. Ne ovat yksinkertaisia "laatikoita", jotka sisältävät suoraan arvon.

Kun alkeistietotyyppi annetaan parametrina metodille, tapahtuu arvon kopioiminen (pass-by-value).

Metodi saa käyttöönsä kopion alkuperäisestä arvosta.

Jos metodi muuttaa tätä arvoa, alkuperäinen muuttuja ei muutu.

Esimerkki:

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

**Viitetyypit (Reference Types)**

Javassa kaikki tyypit, mitkä eivät ole alkeistietotyyppejä, ovat *viitetyyppejä*. Tässä vaiheessa opintoja tutuimpia viitetyyppejä ovat taulukot (esim. `int[]`) ja `String`-oliot.

Viitetyypin muuttuja ei sisällä itse dataa (kuten taulukon lukuja), vaan viitteen paikkaan, jossa data sijaitsee. Voi ajatella, että muuttuja on kaukosäädin, ja itse data on televisio. Ihan kuten televisiota ohjaillaan kaukosäätimellä, viitetyyppisiä muuttujia käytetään olion sisältämän datan käsittelyyn. 

Kun viitetyyppi annetaan parametrina metodille, kopioidaan viite (kopio kaukosäätimestä). Metodi saa käyttöönsä ``kaukosäätimen'', joka osoittaa samaan dataan kuin pääohjelma. Jos metodi sitten muokkaa datan sisältöä (esim. taulukon alkioita) viitteen kautta, muutos näkyy myös pääohjelmassa.

```java
public static void nollaaTaulukko(int[] taulukko) {
    // Tämä muutos tapahtuu alkuperäiselle taulukolle!
    // Koska "taulukko"-muuttuja viittaa samaan muistipaikkaan.
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

Javassa funktion olioparametrit kulkevat aina viitteinä. Se tarkoittaa, että funktiossa olioon tehdyt muutokset näkyvät myös sitä kutsuvassa ohjelmassa, eli funktio aiheuttaa sivuvaikutuksia. Tämä kannattaa pitää mielessä, kun haluaa ohjelmoida sivuvaikutuksettomia puhtaita funktioita. 

(TODO: Onko mainin paikalle tiedostossa mitään ohjeistusta? Onko se ensimmäisenä vai c:n tapaan viimeisenä?)
```java
void main() {
    StringBuilder muuttuva = new StringBuilder("Esimerkki");
    int luku = 1;

    lisaaJaTulosta(muuttuva, luku);
    IO.println(muuttuva);
    IO.println(luku);
}

public static void lisaaJaTulosta(StringBuilder mjono, int luku){
    luku += 1;
    mjono.append(" 1");
    IO.println(mjono);
    IO.println(luku);
}
```

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