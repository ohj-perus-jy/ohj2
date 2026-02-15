Tee funktio `double keskiarvo(int[] luvut, int minimi, int maksimi)`. Funktio
laskee taulukkona annettujen lukujen keskiarvon seuraavilla ehdoilla:

- Jos alkio on pienempi tai yhtä suuri kuin `minimi`, alkio hylätään eikä sitä
  lasketa keskiarvoon mukaan.
- Jos alkio on suurempi tai yhtä suuri kuin `maksimi`, kyseinen alkio ja kaikki
  sitä seuraavat alkiot hylätään.

Esimerkki:

```java,ignore
IO.println(keskiarvo(new int[] { -5, 1, -4, 0, 98 }, -7, 99));
IO.println(keskiarvo(new int[] { 11, 4, 2, 6, 99, 12, 0, -3 }, 3, 99));
```

```text
18.0
7.0
```

Ensimmäinen kutsu palauttaa `18.0`, sillä aineisto on kokonaisuudessaan minimin
ja maksimin välissä. Toinen kutsu palauttaa taas `7.0`, sillä vain luvut 11, 4
ja 6 otetaan keskiarvoon mukaan: luku 2 on pienempi kuin minimi ja kaikki
luvusta 99 alkaen hylätään.

Jos keskiarvoa ei voida laskea, funktio palauttaa `minimi`-parametrin arvon.

**Älä käytä silmukoita**, vaan toteuta funktio käyttäen striimejä.

<details closed><summary>Vinkki</summary>

Tutustu `IntStream`-tyyppiin
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/IntStream.html))
ja sen metodeihin. Voit hyötyä ainakin seuraavista:

- `filter()`: alkioiden suodattaminen pois striimistä
- `takeWhile()`: ottaa alkioita striimistä niin kauan kuin ehto on tosi; heti
  kun ehto on epätosi, striimin käsittely loppuu siihen (kuin "hana", joka
  suljetaan).
- `average()`: laskee keskiarvon

Huomaa, että `average()` palauttaa `OptionalDouble`-olion
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/OptionalDouble.html)).
Olio sisältää `orElse()`-metodin, jonka avulla voit palauttaa joko lasketun
arvon tai vaihtoehtoisen oletusarvon.

</details>

<details closed><summary>Bonustieto</summary>

Samankaltainen tehtävä tehdään Ohjelmointi 1 -kurssilla käyttäen silmukoita (ks.
[Ohjelmointi 1: demo 6, tehtävä
B1](https://tim.jyu.fi/view/kurssit/tie/itkp102/demot/demo6#b1.-keskiarvo-raja-arvolla-1-p.)).
Jos olet suorittanut kyseisen kurssin, voit verrata striimeillä tehtyä
ratkaisuasi aiemmin tekemääsi silmukkaratkaisuun.

</details>