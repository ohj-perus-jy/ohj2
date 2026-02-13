# Tiedostojen käsittely

> [!VAROITUS]
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Osaat käsitellä tiedostoja Javan valmiiden rajapintojen kautta (Tiedostomuotojen käsittely "käsin" (CSV) ja kirjastolla (JSON))
> - Files API
> - Tietovirrat (Stream) ja sen oheisluokat (BufferedReader/Writer, Scanner)
> - Yksinkertaisen tiedoston lukeminen (CSV-tyylinen)
> - Jokin JSON-kirjasto ja JSON-tiedoston lukeminen: Gson, Jackson, org.json???

Scanner-asian voisi selittää alussa niin , että 

 - tiedosto avataan
 - kuvitteelinen "kursori", joka ikään kuin siirtyy joko merki tai rivi kerrallaan
 - on lopuksi suljettava.

Scannerissa on valmiina olemassa myös nextInt ja nextDouble, joka auttaa lukujen
lukemisessa ja parsimisessa samalla. 

Tämän jälkeen voisi siirtyä files.Apiin. 

BufferedReader?? Onko syytä selittää ollenkaan? Kun tarttee tehokkaasti lukea
tavuja, niin se  ovi olla hyvä... Ehkä bonustiedoksi? 