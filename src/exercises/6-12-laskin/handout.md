Tee yksinkertainen laskinohjelma, joka kysyy käyttäjältä toistuvasti kaksi lukua
sekä laskutoimituksen ja tulostaa laskutoimituksen tuloksen.

Ohjelman tulisi toimia suunnilleen seuraavasti:

```text
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

Ohjelman on käsiteltävä käyttäjän syötteessä olevat virheet siten, ettei ohjelma
kaadu virheellisen syötteen vuoksi.

Toteuta peruslaskutoimituksista summa (`+`), erotus (`-`), tulo (`*`) ja
osamäärä (`/`). Keksi lisäksi vähintään kaksi omaa vapaavalintaista
laskutoimitusta ja toteuta ne.

**Älä käytä ehtorakenteita varsinaisten laskutoimitusten valitsemiseen.** Voit
kuitenkin käyttää ehtorakenteita sekä `try/catch`-rakenteita syötteen
oikeellisuuden tarkistamiseen.

<details closed><summary>Vinkki 1</summary>

Voit toteuttaa operaatiot lambdalausekkeina. Käytä lambdalausekkeiden tyyppinä
`BiFunction<Double, Double, Double>`
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/BiFunction.html))
tai `DoubleBinaryOperator`
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/function/DoubleBinaryOperator.html)).

</details>

<details closed><summary>Vinkki 2</summary>

Voit käyttää `Scanner`-luokkaa käyttäjän syötteen lukemiseen:

```java,ignore
Scanner lukija = new Scanner(kayttajanSyote);

double luku1 = lukija.nextDouble();
String laskutoimitus = lukija.next();
double luku2 = lukija.nextDouble();
```

Saatat joutua lisäämään tarvittavat poikkeustenkäsittelyt.

</details>
