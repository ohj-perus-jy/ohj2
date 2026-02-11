Lisää edellisen tehtävän `IsoKontti`-luokkaan kaksi metodia.

1. Luokan metodi (*static*) `summaaNumerot` ottaa parametrina `IsoKontti`-olion, 
   joka sisältää numeroita eli `Number`-luokan **tai sen alityyppien** olioita. 
   Metodi palauttaa kontin numeroiden summan.

1. Olion metodi `siirraKaikki` ottaa parametrina toisen `IsoKontti`-olion ja 
   siirtää metodia suorittavan kontin sisällön sinne. Toisen kontin täytyy olla 
   tyypiltään sellainen, että se voi sisältää tämän kontin tyypin olioita.

Tehtävässä on valmiiksi pääohjelma, jolla voit kokeilla luokan toimintaa.

<details><summary>Vinkki</summary>

Tarvitset tässä tehtävässä tyyppirajoituksia.

1. Kaikilla `Number`-luokan olioilla on `doubleValue()`-metodi, joka palauttaa
   sen arvon `double`-muodossa.

2. Huomaa, että konttien tyyppien ei tarvitse olla täysin samat; `Number`-kontti
   voi sisältää `Integer`-olioita, sillä `Integer` on sen alityyppi.

</details>
