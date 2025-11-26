# Polymorfismi

> [!Osaamistavoitteet]
>
> - Polymorfismi (dynaaminen sidonta, rajapinnat ja abstraktit luokat voivat olla muuttujan tai parametrin tyyppeinä)
> - Tunnistaa polymorfismin merkitys olioiden yhteistyössä. Olio, joka käyttää ylätason tyyppiä (rajapinta, abstrakti luokka) voi toimia erilaisten aliluokkien kanssa.
> - Kutsuttava metodi päätetään ajon aikana olion todellisen tyypin perusteella, ei muuttujan tyypin perusteella.
> - Osaat hyödyntää rajapintoja ja abstrakteja luokkia luokkienvälisen riippuvuuden välttämiseksi 

*Polymorfismi* viittaa olio-ohjelmoinnissa kykyyn käsitellä erilaisia olioita yhtenäisellä tavalla. Kun metodia kutsutaan, päätös siitä, mikä metodi tosiasiallisesti suoritetaan, tehdään ajon aikana olion todellisen tyypin perusteella. Polymorfismi mahdollistaa joustavan koodin kirjoittamisen, jossa uusia olioita voidaan lisätä ilman, että olemassa olevaa koodia tarvitsee muuttaa.

Polymorfismi jaetaan yleensä kahteen päätyyppiin: käännösaikaiseen polymorfismiin ja ajon aikaiseen polymorfismiin. Käännösaikaisella polymorfismilla tarkoitetaan Javassa metodin kuormitusta (engl. *method overloading*), jota on käsitelty Ohjelmointi 1 -kurssilla, emmekä sitä tässä käsittele tarkemmin. 

## Polymorfismin tyypit

Polymorfismi voidaan jakaa kahteen päätyyppiin:

1. *Käännösaikainen polymorfismi* (compile-time polymorphism), joka tunnetaan myös nimellä *staattinen polymorfismi*. Tämä saavutetaan yleensä metodin ylikuormituksella (method overloading) tai operatorin ylikuormituksella (operator overloading). Käännösaikaisessa polymorfismissa päätös siitä, mikä metodi tai operaatio suoritetaan, tehdään käännösaikana.

2. *Ajon aikainen polymorfismi* (run-time polymorphism), joka tunnetaan myös nimellä *dynaaminen polymorfismi*. Tämä saavutetaan yleensä perinnän ja metodin ylikirjoittamisen (method overriding) kautta. Ajon aikaisessa polymorfismissa päätös siitä, mikä metodi suoritetaan, tehdään ajon aikana olion todellisen tyypin perusteella.

## Dynaaminen sidonta

Polymorfismi toteutuu usein dynaamisen sidonnan (engl. *dynamic binding*) kautta. Dynaaminen sidonta tarkoittaa sitä, että metodikutsun sitominen tiettyyn metodin toteutukseen tapahtuu ajon aikana, ei käännösaikana. Tämä mahdollistaa sen, että sama metodikutsu voi johtaa eri toteutuksiin riippuen siitä, minkä tyyppinen olio sitä kutsuu.

## Huomautus instanceof-operaattorista

Javassa on mahdollista tarkistaa, onko olio tietyn luokan ilmentymä käyttämällä `instanceof`-operaattoria. Esimerkiksi:

On kuitenkin niin, että `instanceof`-operaattorin käyttö tarkoittaa varsin usein sitä, ettei perintää ja polymorfismia ole hyödynnetty optimaalisella tavalla, jonka seurauksena koodiin tulee runsaasti ehtolauseita, jotka tarkistavat olion tyypin ja suorittavat sen perusteella erilaisia toimintoja. Tällöin menetetään olio-ohjelmoinnin keskeinen etu, eli se, että olioiden erilaiset toteutukset voidaan piilottaa niiden käyttäjiltä. Käytännössä ainoa, missä kyseistä operaattoria tarvitsee, on, jos käsitellään `Object`-olioita jonkin hyvin matalan tason yleisluokan kautta. 