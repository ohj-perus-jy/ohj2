Tee funktio `double keskiarvo(int[] luvut, int minimi, int maksimi)`.
Funktio laskee taulukkona annettujen lukujen keskiarvon seuraavilla ehdoilla:

- Jos alkio on pienempi tai yhtäsuuri kuin `minimi`, alkio hylätään eikä lasketa
  keskiarvoon mukaan
- Jos alkio on suurempi tai yhtäsuuri kuin `maksimi`, alkiota ja kaikki sitä
  seuraavia alkioita hylätään

Esimerkki:

```java,ignore
IO.println(keskiarvo(new int[] { -5, 1, -4, 0, 98 }, -7, 99));
IO.println(keskiarvo(new int[] { 11, 4, 2, 6, 99, 12, 0, -3 }, 3, 99));
```

```
18
7
```

Ensimmäinen kutsu palauttaa `18`, sillä aineisto on kokonaisuudessaan minimin
ja maksimin välissä.
Toinen kutsu palauttaa taas `7`, sillä vain luvut 11, 4 ja 6 otetaan keskiarvoon
mukaan: 2 on alle minimin ja kaikki luvusta 99 eteenpäin olevat luvut hylätään.

Jos keskiarvoa ei voi laskea, funktio palauttaa `minimi`-parametrin arvon.

**Älä käytä silmukoita,** vaan toteuta funktio käyttäen striimeja.

Bonustieto: Samankaltainen tehtävä tehdään Ohjelmointi 1 -kurssilla käyttäen
silmukoita (ks. [Harjoitustehtävät 6 Tehtävä
B1](https://tim.jyu.fi/view/kurssit/tie/itkp102/demot/demo6#b1.-keskiarvo-raja-arvolla-1-p.)).
Mikäli joskus kävit kurssin, voit kokeilla tämän tehtävän tekemisen jälkeen
vertailla vastauksesi Ohjelmointi 1 -kurssin vastaukseen.

<details><summary>Vinkki 1</summary>

Tutustu `IntStream`
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/IntStream.html))
tyyppiin ja sen metodeihin.

Voit hyötyä ainakin seuraavista metodeista:

- `filter()`: alkioiden suodattaminen pois striimistä
- `takeWhile()`: ottaa alkioita striimistä niin kauan kuin ehto on tosi; heti
  kun ehto on epätosi, striimin käsittely loppuu siihen (ikään kuin "hana", joka
  suljetaan)
- `average()`: laskee keskiarvon

Huomaa, että `average()` palauttaa `OptionalDouble`-olion ([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/OptionalDouble.html)).
Olio sisältää `orElse()`-metodin, jonka avulla voi palauttaa joko oliossa
olevan arvon tai vaihtoehtoisen oletusarvon.

</details>