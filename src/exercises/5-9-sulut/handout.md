Kirjoita aliohjelma, joka tarkistaa merkkijonon sisältämien sulkujen
oikeellisuuden. Aliohjelman tulee tunnistaa, sulkeutuvatko kaikki sulut oikeassa
järjestyksessä ja onko jokaisella alkavalla sululla vastaava lopettava pari.

Tuetut sulkutyypit ovat kaarisulut `( )`, hakasulut `[ ]` ja aaltosulut `{ }`. 

Toimintalogiikka ja säännöt:

 * **Sisäkkäisyys:** Sulut voivat olla sisäkkäin (esim. `([]))`, mutta ne eivät saa
   mennä ristiin. Esimerkiksi `([)]` on virheellinen, koska sulut menevät
   ristiin.
 * **Järjestys:** Sulun on aina alettava ennen kuin se sulkeutuu.
 * **Muut merkit** kuten kirjaimet tai numerot tulee jättää huomiotta.
 * **Tyhjä merkkijono** katsotaan oikeelliseksi, ja siinä on 0 paria.

Paluuarvo:

 * Jos sulutus on kunnossa, palauta löydettyjen sulkuparien lukumäärä (kokonaisluku).
 * Jos sulutus on virheellinen (yksikin pari puuttuu tai järjestys on väärä), palauta luku -1.

Esimerkit:

| Merkkijono | Tulos | Selite                                             |
| ---------- | ----- | -------------------------------------------------- |
| ""         | 0     | Tyhjä syöte on validi, 0 paria.                    |
| "()"       | 1     | Yksi ehjä pari.                                    |
| "(())"     | 2     | Kaksi sisäkkäistä paria.                           |
| "([{}])"   | 3     | Kolme sisäkkäistä paria.                           |
| "()[]{}"   | 3     | Kolme vierekkäistä paria.                          |
| "a(b)c"    | 1     | Kirjaimet sivuutetaan, yksi pari.                  |
| "("        | -1    | Sulkeva pari puuttuu.                              |
| "(()"      | -1    | Yksi sulkeva pari puuttuu.                         |
| "()}"      | -1    | Ylimääräinen sulkeva sulku.                        |
| ")("       | -1    | Väärä järjestys (alkava sulku puuttuu alussa).     |
| "([)]"     | -1    | Sulut menevät ristiin (virheellinen sisäkkäisyys). |

Aliohjelma tulee toteuttaa niin, että *jos* sulkuihin lisättäisin uusia
sulkutyyppejä, niin varsinaisessa logiikassa ei tarvitsisi tehdä muutoksia.
Esimerkiksi merkkijonon `a<(b)>c` käsittelemiseen tulisi vain lisätä tuki
kulmasuluille `< >`, mutta muuten logiikka pysyisi samana (lue: ei ylimääräisiä
`if`-lauseita).