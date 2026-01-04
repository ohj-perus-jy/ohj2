Tee luokka `Puhelin`, jolla on attribuutit `merkki` (merkkijono) ja `akunVaraus`
(kokonaisluku, joka kuvaa akun varausta prosentteina väliltä 0-100). Lisää
luokkaan seuraavat metodit:

 * `lahetaViesti(String henkilo, String viesti)`: tulostaa viestin muodossa
   "Lähetetään viesti henkilölle \<henkilo\>: \<viesti\>". Viestin lähettäminen
   vähentää akkua 5 prosenttiyksikköä. 
 * `soita(String henkilo, int minuutit)`: tulostaa viestin muodossa "Soitetaan
   puhelu henkilölle \<henkilo\>, kesto: \<minuutit\> minuuttia". Soittaminen
   vähentää akkua 1 prosenttiyksikköä per minuutti.
 * `lataa(int prosentteja)`: lisää akun varausta annetun määrän, mutta akun
   varaus ei voi ylittää 100 prosenttia.
 * `tulostaTiedot()`: tulostaa puhelimen merkin ja akun varauksen muodossa
   "Puhelimen \<merkki\> akun varaus on \<akku\>%".

Korvaa kulmasulkeissa olevat kohdat sopivilla attribuuttien / parametrien
arvoilla.

Akun varaus ei voi mennä alle 0%.

Jos akun varaus on 0%, viestiä ei voida lähettää eikä voi soittaa "Akku tyhjä.
Viestiä ei voida lähettää / ei voi soittaa.".

Testaa sovellustasi luomalla `Puhelin`-olio, lähettämällä viesti, soittamalla
puhelu, lataamalla akkua ja tulostamalla puhelimen tiedot.

<details><summary>Valinnainen lisätehtävä: Jos akku loppuu kesken</summary>

Muokkaa `lahetaViesti`- ja `soita`-metodeja siten, että jos akun varaus ei riitä
koko viestin lähettämiseen tai puhelun soittamiseen, niin lähetetään/soitetaan
niin kauan kuin akku riittää. Jos akku loppuu kesken puhelun / viestin, tulosta
kauanko puhelu onnistui / kuinka paljon viestistä saatiin lähetettyä ennen akun
loppumista. Esimerkiksi "Akku tyhjä. Sait lähetettyä 60% viestistä." tai "Akku
loppui 3 minuutin jälkeen.

</details>