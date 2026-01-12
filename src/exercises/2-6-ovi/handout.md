Toteuta luokka `Ovi`, joka mallintaa ovea, joka voi olla joko lukossa tai auki.

Attribuutit: 

 * `private boolean lukossa`
 * `private String avainkoodi`

Muodostaja saa oven avainkoodin parametrina: `LukittuOvi(String avainkoodi)`

Muodostajan pitää asettaa avainkoodi ja asettaa ovi aluksi lukkoon.

Metodit:

 * `boolean avaa(String koodi)`: avaa oven vain, jos koodi on oikein **ja** ovi on
   lukossa. Palauttaa `true`, jos ovi avattiin, muuten `false`.
 * `boolean lukitse()`: lukitsee oven vain, jos se on auki. Palauttaa `true`, jos
   lukitseminen onnistui, muuten `false`.
 * `boolean vaihdaKoodi(String vanha, String uusi)`: vaihtaa avainkoodin uuteen,
   jos vanha koodi on oikein **ja** ovi on auki. Uusi koodi ei voi olla tyhjä
   merkkijono. Palauttaa `true`, jos vaihto onnistui, muuten `false`. 
 * `String tila()`: palauttaa merkkijonon "Ovi on lukossa" tai "Ovi on auki"

Vain `tila()` saa tulostaa jotain. Muut metodit eivät.

Kirjoita pääohjelma, jossa 

 * luot oven
 * lukitset oven
 * yrität avata ovea väärällä koodilla
 * avaat oven oikealla koodilla
 * yrität avata jo avointa ovea
 * yrität lukita jo lukittua ovea
 * yrität vaihtaa koodia kun ovi on lukossa
 * vaihdat koodin väärällä vanhalla koodilla
 * vaihdat koodin oikealla vanhalla koodilla
 * tulostat oven tilan

---