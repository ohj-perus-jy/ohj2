Tee funktio `onkoSalasanaVahva`, joka tarkastaa parametrina
saadun salasanan (`String`)
vahvuuden. Salasanan tulee olla vähintään 8 merkkiä pitkä, sisältää yhden luvun,
sekä vähintään yhden suuren ja pienen kirjaimen. 

Funktio palauttaa `true`, jos merkkijonona annettu salasana täyttää yllä
olevat vaatimukset, muuten se palauttaa `false`.

Kirjoita aliohjelmalle myös sopiva dokumentaatiorivi ja lisää
ainakin yksi toimintaesimerkki `main()`-pääohjelmaan.

<details>
<summary>Vinkki</summary>

Katso Character-luokan metodi
[`isDigit`](https://docs.oracle.com/en/java/javase/25/docs//api/java.base/java/lang/Character.html#isDigit(char)).

Esimerkiksi kutsumalla `Character.isDigit(merkki)` saat paluuarvona `true`,
jos merkki on numero, ja vastaavasti `false`, jos merkki ei ole numero.

Vastaavalla periaatteella toimivat myös metodit `isUpperCase` ja `isLowerCase`,
jotka löytyvät myös samasta luokasta.

</details>

