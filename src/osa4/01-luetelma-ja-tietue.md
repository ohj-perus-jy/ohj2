# Luetelma ja tietue

> [!Osaamistavoitteet]
>
> - Tyyppitarkistukset ja tyyppimuunnokset (instanceof, casting)
> - `switch`-lauseke, tyyppikaava sovitus


## Luetelma tyyppinä

- Luetelma (eng. enum/enumeration) on erityinen luokkatyyppi, jolla on ennaltamäärätyt arvot
  - Kätevää, kun halutaan muuttuja, jonka mahdollinen arvojoukko on hyvin määritelty ja muuttumaton eli vakio, esim. viikonpäivät tai perusvärit.

- Luetelma määritetään luokan tavoin ja yksinkertaisimmillaan sisältäen vain luetelman mahdolliset arvot vakioina.

```java
enum Arvosana {
    ERINOMAINEN,
    KIITETTAVA,
    HYVA,
    TYYDYTTAVA,
    VALTTAVA,
    HYLATTY
}
```

```java
enum ViikonPaivat {
    MAANANTAI,
    TIISTAI,
    KESKIVIIKKO,
    TORSTAI,
    PERJANTAI,
    LAUANTAI,
    SUNNUNTAI;
}
```


Voimme määritellä esimerkiksi luetelman sienten syötävyysmerkinnöille. 

```java
enum SienenSyotavyys {
    ERINOMAINEN,
    HYVA,
    SYOTAVA,
    ARVOTON,
    MYRKYLLINEN,
    VAARALLISEN_MYRKYLLINEN,
    TAPPAVAN_MYRKYLLINEN;
}
```

- Huomaa luetelman vakioiden erottimena pilkku ja lopuksi puolipiste


Kattavaan merkintäluetelmaan tarvitsisimme vielä arvot esikäsiteltäville sienille. Yksinkertaisuuden vuoksi jätämme ne tässä esimerkissä huomiotta.

- Luetelman käytöstä esimerkkiä

- Tehtävä jo tähän?

## Luetelmalle ominaisuuksia ja toiminnallisuutta

- Luetelma on luokka
  - Luetelmalla voi olla metodeja
  - Luetelman vakiolle voi määrittää ominaisuuksia

```java
enum SienenSyotavyys {
    ERINOMAINEN("***"),
    HYVA("**"),
    SYOTAVA("*"),
    ARVOTON("○"),
    MYRKYLLINEN("†"),
    VAARALLISEN_MYRKYLLINEN("††"),
    TAPPAVAN_MYRKYLLINEN("†††");

    final private String symboli;

    SienenSyotavyys(String symboli) {
        this.symboli = symboli;
    }

    public String haeSymboli() {
        return this.symboli;
    }

    public boolean onSyotava() {
        return this == ERINOMAINEN || this == HYVA || this == SYOTAVA;
    }
}
```

- Tehtäviä viimeistään tähän

- Esimerkkejä käytöstä

## Tietue (kannattaako esitellä tässä vai mennäänkö vain luokilla?)

- Erityinen luokkatyyppi kuten luetelma (enum)
- Ei salli arvojen muuttamista

- Tarjoaa valmiin toteutuksen:
    - yksityinen, lopullinen kenttä jokaiselle tietoelementille
    - getter-metodi jokaiselle kentälle
    - julkinen konstruktori, jolla on vastaava argumentti jokaista kenttää varten
    - equals-metodi, joka palauttaa true, jos oliot ovat samaa luokkaa ja kaikki kentät ovat samat
    - hashCode-metodi, joka palauttaa saman arvon, kun kaikki kentät ovat samat (ja mahdollisesti muulloinkin — törmäykset ovat mahdollisia)
    - toString-metodi, joka sisältää luokan nimen sekä jokaisen kentän nimen ja sen vastaavan arvon

```java
record Sieni(String nimi, SienenSyotavyys syotavyys) {
}
```
