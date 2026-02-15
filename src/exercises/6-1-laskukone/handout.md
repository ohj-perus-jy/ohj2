Tee ohjelma, joka kysyy käyttäjältä kaksi desimaalilukua sekä laskutoimituksen
ja tulostaa lopputuloksen seuraavasti:

```text
Luku 1 > 12.0
Luku 2 > 3.0
Laskutoimitus (+, -, *, /) > +
12.0 + 3.0 = 15.0
```

Tässä vaiheessa sinun ei tarvitse käsitellä virheellisiä syötteitä, vaan voit
olettaa, että luvut annetaan aina lukuina. Sallitut laskutoimitukset ovat summa
(`+`), erotus (`-`), tulo (`*`) ja osamäärä (`/`). Voit olettaa, että vain näitä
laskutoimituksia käytetään syötteenä.

**Älä käytä silmukoita tai ehtorakenteita.** Sen sijaan toteuta laskutoimitukset
lambdalausekkeina ja tallenna ne hakurakenteeseen käyttäen laskutoimituksen
merkkiä avaimena.

Ohjelman suoritus päättyy tuloksen näyttämisen jälkeen.

<details closed><summary>Vinkki 1</summary>

Voit käyttää lambdalausekkeiden tyyppinä `BiFunction<Double, Double, Double>`
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/BiFunction.html))
tai `DoubleBinaryOperator`
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/DoubleBinaryOperator.html)).

</details>

<details closed><summary>Vinkki 2</summary>

Voit käyttää hakurakenteen tyyppinä `Map<String, BiFunction<Double, Double,
Double>>` tai `Map<String, DoubleBinaryOperator>`.

Voit joko valita hakurakenteelle tietyn toteutuksen tai alustaa muuttumattoman
hakurakenteen `Map.of`-metodilla:

```java,ignore
Map<String, BiFunction<Double, Double, Double>> laskutoimitukset = Map.of(
    "+", ...,
    "-", ...,
    "*", ...,
    "/", ...
);
```

`...`-kohdan tilalle riittää asettaa sopiva lambdalauseke.

</details>
