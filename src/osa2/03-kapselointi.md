# Kapselointi

> [!Osaamistavoitteet]
>
> - Ymmärrät kapseloinnin ja sen hyödyt (Decoupling/Coupling)
> - Toteutetaan olioiden yhteistyö pienessä olioverkossa. Pidetään kytkentä löyhänä, eli olioiden välinen riippuvuus on vain rajapinnan (metodien) varassa, ei sisäisen toteutuksen varassa.
> - julkisuusmääreet `public` ja `private`, getterit ja setterit, metodi pääasiallisena tapana olioille "viestiä"
> - Kutsuja ei tiedä (eikä voi riippua siitä) miten olion tila on toteutettu. Toteutusta voi muuttaa ilman että kutsujan tarvitsee muuttaa koodiaan.

![Autoa ajetaan, vaikka emme tiedä miten moottori toimii](images/auto.png)

Julkisuusmääreet ja niiden merkitys Javassa
- attribuutit, metodit ja luokat
- koodiesimerkki

Kapseloinnin käsitteen selitys (encapsulation)
- sisäinen data on piilossa, mutta on olemassa (rajoitettu) rajapinta sen käsittelyyn -> olion attribuutteja ei suoraan voi muuttaa, mutta olion tilaa voi käsitellä kontrolloidusti metodien kautta
- miksi kannattavaa?
- koodiesimerkki, kaavio?

Coupling/Decoupling käsitteiden selitys
- coupling on riippuvuus eri komponenttien eli tässä kontekstissa luokkien välillä
- riippuvuuksia syntyy luokkien välille, kun yksi luokka on sidoksissa toisen toteutusyksityiskohtiin
- miksi syytä välttää? ylläpidettävyys, pienet muutokset voivat aiheuttaa suuria ongelmia, ym.
- decoupling, kuinka riippuvuuksia voidaan vähentää -> esimerkiksi kapselointi, eli toteutusyksityiskohtien piilottaminen ja julkisten rajapintojen käyttäminen

Aliotsikointi tarpeen mukaan


## Näkyvyysmääreet

Java tarjoaa kolme pääasiallista näkyvyysmäärettä: `public`, `protected` ja `private`. Näkyvyysmääreet määrittelevät, mistä luokan jäseniin voidaan päästä käsiksi. 

Javassa oletuksena luokan jäsenet ovat ns. `package-private`-näkyvyydellä, mikä tarkoittaa, että ne ovat näkyvissä vain samassa pakkauksessa oleville luokille. Alla olevassa taulukossa on yhteenveto eri näkyvyysmääreiden vaikutuksista; Oletus-sarake viittaa `package-private`-näkyvyyteen.

|                            | Luokka | Pakkaus | Aliluokka | Muu maailma |
| -------------------------- | ------ | ------- | --------- | ----------- |
| `public`                   | Kyllä  | Kyllä   | Kyllä     | Kyllä       |
| `protected`                | Kyllä  | Kyllä   | Kyllä     | Ei          |
| `package-private` (oletus) | Kyllä  | Kyllä   | Ei        | Ei          |
| `private`                  | Kyllä  | Ei      | Ei        | Ei          |

Ensimmäinen sarake ilmaisee, onko luokan oliolla itsellään pääsy määritellyn näkyvyystason jäseneen. Kuten näet, oliolla on aina pääsy omiin jäseniinsä. Toinen sarake ilmaisee, onko muilla samassa pakkauksessa olevilla oliolla pääsy jäseneen. Kolmas sarake ilmaisee, onko luokasta perityillä aliluokan olioilla, jotka sijaitsevat pakkauksen ulkopuolella, pääsy jäseneen. Neljäs sarake ilmaisee, onko millä tahansa oliolla pääsy jäseneen.

Jos ja kun muut ohjelmoijat (tai sinä itse) käyttävät tekemääsi luokkaa, näkyvyysmääreet auttavat varmistamaan, että luokkaasi käytetään sillä tavalla, jolla olet suunnitellut sen käytettävän. Pääsääntö on, että ohjelmoijan tulisi käyttää mahdollisimman rajoittavaa näkyvyysmäärettä, ellei ole erityistä syytä käyttää jotain muuta. Tämä auttaa suojaamaan luokan sisäistä tilaa ja estämään tahalliset tai tahattomat väärinkäytökset luokan jäseniin. Vältä julkisia attribuutteja, ellei kyseessä ole vakio. (Tässä materiaalissa saatetaan hetkittäin käyttää esimerkinomaisesti julkisia attribuutteja. Tämä voi auttaa havainnollistamaan joitakin kohtia tiiviisti, mutta sitä ei suositella tuotantokoodissa.) 


## Tehtäviä

Perustaidot:
- korjaa ongelmallinen esimerkkiohjelma niin, että luokat eivät riipu toistensa toteutusyksityiskohdista

Bonus:
-
