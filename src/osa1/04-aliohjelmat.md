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
- Taulukko, merkkijono jne.?

## Funktiot
Funktion yleinen esittelyrivi javassa:
```java.ignore
public static [palautettava] ([parametrit]) {
    ...
}
```

Kuten C#:ssa, jos funktio ei palauta, mitään on palautettavan tyyppi `void`


## Javan perustietotyypin ja viitetyyppien ero funktion kutsussa
- Kun aliohjelmakutsussa parametrina on olio, parametrina kulkee olion viite, ei itse olio.
- Jokin hyvä havainnointi

## Kommentointi

```java
// Tämä on yhden rivin kommentti

/*
 * Tämä on usean rivin
 * kommentti
 */

//Esimerkki dokumentaatiosta
/**
 * Laskee kahden kokonaisluvun summan.
 * 
 * @param a Ensimmäinen luku
 * @param b Toinen luku
 * @return Lukujen summa
 */
int summa(int a , int b) {
    return a + b;
}
```

Dokumentaation saa aliohjelmalle, kun kirjoittaa `/**` aliohjelman esittelyrivin yhtä ylemmälle riville ja painaa `Enter` IntelliJ:ssä

## B1
- (Verkko viikon konsepteista?)

- Monty hall ongelman simulointi neljällä ovella

## B2
- Vakioaikainen haku taulukosta. Esimerkiksi, että kuinka monta päivää on kuukaudessa?

## B3
- Raa-alla voimalla sanakirjahyökkäys salasanaa vastaan?

## G1

- Linkitetty lista käänteiseksi?

## G2

- Neliömatriisin eli n x n, n $\in \mathbb{N}$ matriisin pyöräyttäminen 90-astetta. 
- In ([[1,2],[3,4]], oikealle) --> [[3,1],[4,2]]