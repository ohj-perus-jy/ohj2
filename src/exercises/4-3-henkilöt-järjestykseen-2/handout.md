Jatkoa edelliselle tehtävälle. Nyt `Henkilo`-luokassa henkilöiden nimet on jaettu erikseen sukunimeen ja etunimiin.

Muokkaa uudistettua `Henkilo`-luokkaa niin, että `List<Henkilo>`-tyyppiset listat voidaan järjestää `Collections.sort`-metodilla henkilön sukunimen ja etunimien mukaan aakkosjärjestykseen, niin että järjestys tapahtuu ensin sukunimen mukaan.

Esimerkiksi listan

```java
List<Henkilo> henkilot = Arrays.asList(
    new Henkilo("Pacius", "Fredrik"),
    new Henkilo("Mozart", "Wolfgang Amadeus"),
    new Henkilo("Mozart", "Leopold"),
    new Henkilo("Chopin", "Frédéric"),

);
```

pitäisi olla `Collections.sort(henkilot);`-kutsun jälkeen järjestyksessä:

1. Chopin Frédéric
2. Mozart Leopold
3. Mozart Wolfgang Amadeus
4. Pacius Fredrik

