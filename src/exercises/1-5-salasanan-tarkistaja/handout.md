Tehtävänäsi on tehdä funktio, joka tarkastaa parametrina saadun salasanan
vahvuuden. Salasanan tulee olla vähintään 8 merkkiä pitkä, sisältää yhden luvun,
sekä vähintään yhden suuren ja pienen kirjaimen. 

Vinkki: Katso Character-luokan metodi
[`isDigit`](https://docs.oracle.com/en/java/javase/25/docs//api/java.base/java/lang/Character.html#isDigit(char)).
Esimerkiksi:  kutsumalla `Character.isDigit(merkki)` saat paluuarvona `true`,
jos merkki on numero, ja vastaavasti `false`, jos merkki ei ole numero.
Vastaavalla periaatteella toimivat myös metodit `isUpperCase` ja `isLowerCase`,
jotka löytyvät myös samasta luokasta.