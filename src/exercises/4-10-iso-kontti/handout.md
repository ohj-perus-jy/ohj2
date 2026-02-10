Luo luokka `IsoKontti`, joka toimii säiliönä usealle minkä tahansa tyypin
oliolle. Konttiin pakataan esineitä niin, että viimeisimpänä lisätty 
otetaan aina ensimmäiseksi pois.

Lisää luokkaan attribuutiksi lista, johon oliot tallennetaan.

Lisää myös seuraavat metodit: 

- `lisaa` lisää parametrina annetun olion listan loppuun.

- `ota` palauttaa viimeisimmän olion ja ottaa sen pois listasta.
 
- `katso` palauttaa viimeisimmän olion, mutta ei ota sitä pois listasta.

- `sisaltaa` ottaa parametrina olion ja palauttaa `true`, jos olio löytyy 
  kontista. Muussa tapauksessa se palauttaa `false`.

- `tulosta` tulostaa kontin sisällön. Voit itse päättää, missä muodossa sisältö
  tulostetaan.

Tehtävässä on valmiiksi pääohjelma, jolla voit kokeilla luokan toimintaa.
