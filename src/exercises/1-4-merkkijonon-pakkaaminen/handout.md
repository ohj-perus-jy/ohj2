Tee aliohjelma `pakkaaMerkkijono`,
joka ottaa parametrina `String`-merkkijonon
ja palauttaa uuden `String`-merkkijonon tiivistettynä siten, 
että peräkkäiset samat merkit ilmoitetaan merkillä ja niiden lukumäärällä.

Esimerkiksi:

- `pakkaaMerkkijono("aaaabbbccd")` palauttaisi merkkijonon `"a4b3c2d1"`,
- `pakkaaMerkkijono("00666663332222222")` palauttaisi merkkijonon `"02653327"`,
- `pakkaaMerkkijono("Niiiiiin")` palauttaisi merkkijonon `"N1i6n1"`,
- `pakkaaMerkkijono("nnNNnnnN")` palauttaisi merkkijonon `"n2N2n3N1"`,
- `pakkaaMerkkijono("ohjelmointi")` palauttaisi merkkijonon `"o1h1j1e1l1m1o1i1n1t1i1"`.

Kirjoita aliohjelmalle myös sopiva dokumentaatiorivi ja lisää
ainakin yksi toimintaesimerkki `main()`-pääohjelmaan.

<details>
<summary>Vinkki 1</summary>

Käytä
[`StringBuilder`-merkkijonoa](https://ohjelmointi2.it.jyu.fi/osa1/02-muuttujat-ja-tietotyypit.html#stringbuilder)
ja sen metodeja merkkijonon rakentamiseen.

</details>

<details>
<summary>Vinkki 2</summary>

Kokeile ratkaista ongelma ensin paperilla käsin lyhyelle jonolle
(esim. `"aabb"`). Mistä asioista on pidettävä kirjaa (muuttujat)?

</details>

<details>
<summary>Vinkki 3</summary>

Voi olla helpompaa aloittaa toisesta merkistä ja verrata
se aina edeltävään:

```svgbob
  0   1   2   3 = jono.length
+---+---+---+---+
| a | a | b | b |
+---+---+---+---+
  ^   ^
  |   |
i - 1 |
      i = 1
```

</details>

