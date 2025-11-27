# Polymorfismi

> [!Osaamistavoitteet]
>
> - Polymorfismi (dynaaminen sidonta, rajapinnat ja abstraktit luokat voivat olla muuttujan tai parametrin tyyppeinä)
> - Tunnistaa polymorfismin merkitys olioiden yhteistyössä. Olio, joka käyttää ylätason tyyppiä (rajapinta, abstrakti luokka) voi toimia erilaisten aliluokkien kanssa.
> - Kutsuttava metodi päätetään ajon aikana olion todellisen tyypin perusteella, ei muuttujan tyypin perusteella.
> - Osaat hyödyntää rajapintoja ja abstrakteja luokkia luokkienvälisen riippuvuuden välttämiseksi 

*Polymorfismi* viittaa olio-ohjelmoinnissa kykyyn käsitellä erilaisia olioita yhtenäisellä tavalla. Kun metodia kutsutaan, päätös siitä, mikä metodi tosiasiallisesti suoritetaan, tehdään ajon aikana olion todellisen tyypin perusteella. Polymorfismi mahdollistaa joustavan koodin kirjoittamisen, jossa uusia olioita voidaan lisätä ilman, että olemassa olevaa koodia tarvitsee muuttaa.

Polymorfismi jaetaan yleensä kahteen päätyyppiin: (1) käännösaikaiseen polymorfismiin, jota kutsutaan myös *dynaamiseksi sidonnaksi* (engl. *dynamic binding*) ja (2) ajon aikaiseen polymorfismiin. Käännösaikaisella polymorfismilla tarkoitetaan Javassa aliohjelman kuormitusta (engl. *method overloading*). Asiaa on käsitelty Ohjelmointi 1 -kurssilla, emmekä sitä tässä käsittele tarkemmin, mutta lyhyesti: aliohjelman kuormitus tarkoittaa sitä, että aliohjelmalla voi olla useita samannimisiä toteutuksia, jotka eroavat toisistaan parametrien lukumäärän, parametrien tyyppien tai aliohjelman paluuarvon perusteella. Lue lisää Ohjelmointi 1 -kurssin materiaalista. (TODO: Linkki)

## Esimerkki

Tarkastellaan abstraktia `Muoto`-luokkaa, jolla on metodi `laskeAla()`. 

```java
public abstract class Muoto {
    public abstract double laskeAla();
}
```

## Huomautus instanceof-operaattorista

Javassa on mahdollista tarkistaa, onko olio tietyn luokan ilmentymä käyttämällä `instanceof`-operaattoria. Esimerkiksi:

On kuitenkin niin, että `instanceof`-operaattorin käyttö tarkoittaa varsin usein sitä, ettei perintää ja polymorfismia ole hyödynnetty optimaalisella tavalla, jonka seurauksena koodiin tulee runsaasti ehtolauseita, jotka tarkistavat olion tyypin ja suorittavat sen perusteella erilaisia toimintoja. Tällöin menetetään olio-ohjelmoinnin keskeinen etu, eli se, että olioiden erilaiset toteutukset voidaan piilottaa niiden käyttäjiltä. Käytännössä ainoa, missä kyseistä operaattoria tarvitsee, on, jos käsitellään `Object`-olioita jonkin hyvin matalan tason yleisluokan kautta. 