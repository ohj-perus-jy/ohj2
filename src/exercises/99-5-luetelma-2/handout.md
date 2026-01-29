Toteuta luetelma `Tulos`, jolla on vakioarvot: `VOITTO`, `TAPPIO`, `TASAPELI`.

Lisää vielä vakioarvoille tuloksesta saatavat pisteet siten, että 

- voitosta saa kolme pistettä
- tasapelistä saa yhden pisteet
- tappiosta saa nolla pistettä

Luetelman vakoiden pistetiedot tulisi saada muiden olioiden käyttöön metodilla `pisteet`

Käyttöesimerkki:

```java
void main() {
    print(Tulos.VOITTO.pisteet()); // tulostaa 3
    print(Tulos.TASAPELI.pisteet()); // tulostaa 1
    print(Tulos.TAPPIO.pisteet()); // tulostaa 0
}
```
