Tee ohjelma, joka kysyy käyttäjältä kaksi desimaalilukua ja laskutoimituksen
sekä tulostaa laskutoimituksen tuloksen seuraavasti:

```
Luku 1 > 12.0
Luku 2 > 3.0
Laskutoimitus (+, -, *, /) > +
12.0 + 3.0 = 15.0
```

Tässä vaiheessa sinun ei tarvitse käsitellä virheellisiä syötteita, vaan
voit olettaa, että luvut annetaan aina lukuina.
Sallitut laskutoimitukset ovat summa (`+`), erotus (`-`), kertolasku (`*`)
ja jakolasku (`/`). Voit olettaa, että vain nämä laskutoimituksia käytetään
syötteenä.

**Älä käytä yhtään silmukkaa tai ehtorakennetta.**
Sen sijaan tee laskutoimituksia vastaavat lambdalausekkeet ja tallenna
ne hakurakenteeseen käyttäen laskutoimituksen merkkiä avaimena.


<details><summary>Vinkki 1</summary>

Voit käyttää lambdalausekkeiden tyyppinä `BiFunction<Double, Double, Double>`
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/BiFunction.html))
tai `DoubleBinaryOperator`
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/DoubleBinaryOperator.html)).

</details>

<details><summary>Vinkki 2</summary>

Voit käyttää hakurakenteen tyyppinä 
`Map<String, BiFunction<Double, Double, Double>>`
tai
`Map<String, DoubleBinaryOperator>`.

Voit joko valita hakurakenteelle tietyn toteutuksen tai alustaa
muuttumattoman hakurakenteen `Map.of`-metodilla:

```java,ignore
Map<String, BiFunction<Double, Double, Double>> laskutoimitukset = Map.of(
    "+", ...,
    "-", ...,
    "*", ...,
    "-", ...
);
```

`...` tilalle riittää asettaa sopiva lambdalauseke.

</details>







