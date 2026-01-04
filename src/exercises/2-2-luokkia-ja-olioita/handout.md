Tee luokka `Puhelin`, jolla on attribuutit `merkki` (merkkijono) ja `akunVaraus`
(kokonaisluku, joka kuvaa akun varausta prosentteina väliltä 0-100). Lisää
luokkaan seuraavat metodit:

 * `lahetaViesti(String viesti)`: tulostaa viestin muodossa "Lähetetään viesti: \<viesti\>". Vähentää akkua 5 prosenttiyksikköä.
 * `soita(int minuutit)`: tulostaa viestin muodossa "Soitetaan puhelu, kesto: \<minuutit\> minuuttia". Vähentää akkua 1 prosenttiyksikköä per minuutti.
 * `lataa(int prosentteja)`: lisää akun varausta annetun määrän, mutta akun varaus ei voi ylittää 100 prosenttia.
 * `tulostaTiedot()`: tulostaa puhelimen merkin ja akun varauksen muodossa "Puhelinmerkki: \<merkki\>, akun varaus: \<akku\>%".

Korvaa kulmasulkeissa olevat kohdat sopivilla attribuuttien / parametrien
arvoilla.

Testaa sovellustasi luomalla `Puhelin`-olion, lähettämällä viesti, soittamalla
puhelu, lataamalla akkua ja tulostamalla puhelimen tiedot.
