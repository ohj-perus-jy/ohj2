# Aliohjelmat

> [!Osaamistavoitteet]
>
> - Käsitellään dataa funktioiden avulla (Ohj1-kurssin tapaan)
> - Funktiot (määrittely, kirjoitusasu, palautusarvot, ehkä hieman datan käsittelyä kertauksena)
> - Ymmärrät Javan perustietotyyppien ja viitetyyppien eron funktion kutsussa (oliot ovat aina viitteen takana)
> - Dokumentaatiokommentit
> - Osaat kirjoittaa Ohjelmointi 1 -kurssin tapaisia ohjelmia Javalla

## Datan käsittely
TODO:
- Taulukko, merkkijono jne? Millaista dataa ja miten?

## Funktiot
Funktion yleinen esittelyrivi Javassa:
```java.ignore
public static tyyppi ([parametrit]) {
    ...
}
```

Jos funktio ei palauta, mitään on palautettavan tyyppi `void`. Palautettava voi olla tyypiltään jokin Javan perustietotyyppi tai olio. 


## Javan perustietotyypin ja viitetyyppien ero funktion kutsussa
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