Tee yksinkertainen laskinohjelma, joka kysyy jatkuvasti käyttäjältä
kaksi lukuja sekä laskutoimituksen ja tulostaa laskutuloksen.
Ohjelman tulisi toimia suunnilleen seuraavasti:

```
Anna laskutoimitus muodossa <luku> <operaattori> <luku>.
Kirjoita "sulje" sulkeaksesi ohjelman.

> 1 + 1
2.0
> 10 - 1
9.0
> 0.5 * 100
50.0
> 10 / 2
5.0
> 10
Anna laskutoimitus muodossa <luku> <operaattori> <luku>.
> kissa
Anna laskutoimitus muodossa <luku> <operaattori> <luku>.
> sulje
Ohjelma sulkeutuu.
```

Ohjelman on käsiteltävä käyttäjän syötteessä olevia virheitä.
Ohjelma ei saa kaatua käyttäjän virheellisesti muodostetun syötteen takia.

Toteuta peruslaskutoimituksista summa (`+`), erotus (`-`), tulo (`*`) ja osamäärä
(`/`). Keksi lisäksi vähintään kaksi omaa vapaavalintaista laskutoimitusta ja toteuta ne.

**Älä käytä ehtorakenteita laskutoimitusten toteuttamisessa.** 
Voit kuitenkin käyttää ehtorakenteita ja `try/catch`-rakenteita
oikeellisuustarkistusten yhteydessä.

<details><summary>Vinkki 1</summary>

Voit toteuttaa operaatiot lambdalausekkeina.
Käytä lambdalausekkeiden tyyppinä `BiFunction<Double, Double, Double>`
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/BiFunction.html))
tai `DoubleBinaryOperator`
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/DoubleBinaryOperator.html)).

</details>

<details><summary>Vinkki 2</summary>

Voit käyttää `Scanner`-tyyppiä käyttäjän syötteen lukemiseksi:

```java,ignore
Scanner lukija = new Scanner(kayttajanSyote);

double luku1 = lukija.nextDouble();
String laskutoimitus = lukija.next();
double luku2 = lukija.nextDouble();
```

Saatat joutua lisäämään tarvittavat poikkeustenkäsittelyt.

</details>







