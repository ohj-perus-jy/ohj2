# Kapselointi

> [!Osaamistavoitteet]
>
> - Ymmärrät kapseloinnin ja sen hyödyt (Decoupling/Coupling)
> - Toteutetaan olioiden yhteistyö pienessä olioverkossa. Pidetään kytkentä löyhänä, eli olioiden välinen riippuvuus on vain rajapinnan (metodien) varassa, ei sisäisen toteutuksen varassa.
> - julkisuusmääreet `public` ja `private`, getterit ja setterit, metodi pääasiallisena tapana olioille "viestiä"
> - Kutsuja ei tiedä (eikä voi riippua siitä) miten olion tila on toteutettu. Toteutusta voi muuttaa ilman että kutsujan tarvitsee muuttaa koodiaan.

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

## Tehtäviä

Perustaidot:
- korjaa ongelmallinen esimerkkiohjelma niin, että luokat eivät riipu toistensa toteutusyksityiskohdista

Bonus:
-
