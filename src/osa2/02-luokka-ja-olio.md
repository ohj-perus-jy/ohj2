# Luokka ja olio

> [!Osaamistavoitteet]
>
> - Luokka ja olio
> - Konstruktori, metodi, attribuutti
> - Luokan rakenne ja suhde olioon (konstruktori, attribuutti, metodi, this-viite, "luokka blueprintina oliolle")
> - `final` attribuuttien kanssa
> - Osaat määritellä ja hyödyntää omia luokkia Javalla

## Luokka

Ensimmäinen askel olio-ohjelmointiin on luokan määritteleminen. Luokkaa voi ajatella kaavana, jonka pohjalta olioita luodaan. Luokka kertoo, mitä tietoja olio sisältää (attribuutit) ja mitä se voi tehdä (metodit).

...

Esimerkiksi yhden rakennuspiirustuksen pohjalta voidaan rakentaa monta rakennusta. Ne olisivat rakenteeltaan samanlaisia, sillä ne ovat saman kaavan mukaan tehty, mutta jokaisella rakennuksella olisi kuitenkin oma tila; eri omistaja, väri, sisustus, jne. Rakennuspiirustus on kuin luokka ja rakennukset sen pohjalta tehtyjä olioita. Luokan nimi kertoo, *mikä* olio on, joten jos tekisimme luokan rakennuksille, sen nimeksi tulisi `Rakennus`.

```java
public class Rakennus {
    private String omistaja;
    private String väri;

    // ...
}
```

### Attribuutit

Luokan sisällä esiteltyjä muuttujia kutsutaan *attribuuteiksi*. Jokaisella samasta luokasta tehdyllä oliolla on aina samat attribuutit, mutta niillä omat arvot, sillä jokaisella oliolla on oma tila. Olion tilan voidaan siis ajatella olevan tallessa sen attribuuteissa. Attribuuttien elinikä on sama kuin olion, sillä olion tilan täytyy olla olemassa sen tuhoutumiseen asti.

TODO:
- Attribuutit ovat näkyvissä kaikissa luokan omissa metodeissa
- Attribuutit ovat muuten kuin muutkin muuttujat; voi olla viitemuuttuja (toiseen olioon), voi antaa oletusarvoja, tapana sijoittaa luokan alkuun (julkisuus osassa 2.3)

Huom! Luokassa olevien aliohjelmien sisällä esitellyt muuttujat eivät ole attribuutteja, vaan aliohjelman lokaaleja muuttujia. Vain suoraan luokan alla olevat muuttujat ovat attribuutteja. Lokaalien muuttujien sisältämä tieto katoaa aliohjelman päätyttyä, eli ne eivät ole osa olion tilaa.

```java
public class Rakennus {
    // Nämä muuttujat ovat attribuutteja.
    private String omistaja;
    private String väri = "sininen";

    private void teeJotain()
    {
        int toistoja = 5; // Tämä muuttuja ei ole luokan attribuutti, sillä se on esitelty aliohjelman sisällä.
    }
}
```

### Metodit

TODO: Metodit (get/set ja omat metodit, kapseloinnin käsite ja julkisuus osassa 2.3)

#### Muodostaja eli konstruktori

TODO: Konstruktori, destruktori (ei käytössä Javassa, mutta yleisesti ottaen hyvä tietää)

#### Muita erikoismetodeja

TODO:
- toString
- equals
- toHash (ei ehkä tässä vielä relevantti)
- Override esiintyy näissä, joten hyvä mainita lyhyesti. Tähän palataan myöhemmässä osassa.

## Static-määrite

TODO:
- Staattiset attribuutit, metodit, luokat
- Kuva selkeyttää huomattavasti

Staattisuudesta on hyvä jatkaa this-viitteeseen.

## this-viite

TODO:

## Oliot

TODO:
- Edellä opittua kooten; olioiden luominen ja tuhoutuminen, näkyvyysalue, roskaksi muuttuminen, todennäköisesti aliotsikoihin
- Olioviitteet, tähän sopii useamman luokan yhteistyö ja attribuuttien final. Tästä voi siirtyä sujuvasti olioiden vertailuun

### Olioiden vertaileminen

TODO: == vs equals

## Tehtäviä

Perustaidot:
- oman luokan luonti esimerkkien avulla (attribuutteja, konstruktori ja get/set-metodit sekä muut metodit)
- olioiden luominen sekä niiden tilan tarkistaminen ja muuttaminen (get/set)
- equals-metodin toteuttaminen (valmiiksi annetulle luokalle)
- oliotaulukko tai -lista ja sen läpikäynti

Bonus:
-
