Tehtävässä on pohjana `Henkilo`-luokka omassa tiedostossaan sekä `jarjestaHenkilot`-metodi `main.java`-tiedostossa. Kyseinen metodi ei kuitenkaan toimi, sillä se käyttää Javan valmista `Collections.sort`-metodia ja `Henkilo`-luokasta puuttuu sille tuki.

Muokkaa `Henkilo`-luokkaa niin, että `List<Henkilo>`-tyyppiset listat voidaan järjestää `Collections.sort`-metodilla henkilön nimen mukaan aakkosjärjestykseen.

Esimerkiksi listan

```java
List<Henkilo> henkilot = Arrays.asList(
    new Henkilo("Joukahainen"),
    new Henkilo("Ilmatar"),
    new Henkilo("Kyllikki")
    new Henkilo("Kokko")
);
```

pitäisi olla `Collections.sort(henkilot);`-kutsun jälkeen järjestyksessä:

1. Ilmatar
2. Joukahainen
3. Kokko
4. Kyllikki

