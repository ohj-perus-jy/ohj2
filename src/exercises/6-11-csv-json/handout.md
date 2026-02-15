Tee ohjelma, joka lukee tiedoston [henkilot.csv](/exercises/6-12-csv-json/henkilot.csv) (muoto `nimi,ika,kaupunki`) ja
kirjoittaa siitä saman tapainen JSON-tiedoston `henkilot.json` kuin edellisessä
tehtävässä oli annettu valmiiksi. Jos rivi on virheellinen (esim. ikä ei ole
numero), ohita rivi ja jatka käsittelyä.

Tulostiedoston pitäisi näyttää tältä. Ei haittaa, jos sisennykset tai
rivinvaihdot eivät ole täsmälleen samanlaisia. 

```json
[
  {
    "nimi": "Maija Laine",
    "ika": 25,
    "kaupunki": "Jyväskylä"
  },
  {
    "nimi": "Matti Virtanen",
    "ika": 30,
    "kaupunki": "Tampere"
  },
  ...
]
```