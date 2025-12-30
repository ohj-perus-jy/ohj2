Tee aliohjelma `pakkaaMerkkijono`,
joka ottaa parametrina `String`-merkkijonon
ja palauttaa uuden `String`-merkkijonon tiivistettynä siten, 
että peräkkäiset samat merkit ilmoitetaan merkillä ja niiden lukumäärällä.

Esimerkiksi:

- `pakkaaMerkkijono("aaaabbbccd")` palauttaisi merkkijonon `"a4b3c2d1"`,
- `pakkaaMerkkijono("00666663332222222")` palauttaisi merkkijonon `"02653327"`,
- `pakkaaMerkkijono("Niiiiiin")` palauttaisi merkkijonon `"N1i5n1"`,
- `pakkaaMerkkijono("nnNNnnnN")` palauttaisi merkkijonon `"n2N2n3N1"`,
- `pakkaaMerkkijono("ohjelmointi")` palauttaisi merkkijonon `"o1h1j1e1l1m1o1i1n1t1i1"`.

Kirjoita aliohjelmalle myös sopiva dokumentaatiorivi ja lisää
ainakin yksi toimintaesimerkki `main()`-pääohjelmaan.

<details>
<summary>Vinkki</summary>

Käytä
[`StringBuilder`-merkkijonoa](02-muuttujat-ja-tietotyypit.md#stringbuilder)
ja sen metodeja merkkijonon rakentamiseen.

</details>