Tee ohjelma, joka lukee käyttäjältä ei-negatiivisia kokonaislukuja yksi rivi kerrallaan
silmukassa käyttäen
`IO.readln()`-metodia, kunnes käyttäjä antaa tyhjän merkkijonon. 
Tallenna nämä luvut listaan. 

Tee sitten aliohjelmat `summa`, `keskiarvo`, `pienin` ja `suurin`, jotka
laskevat listan pienimmän luvun, suurimman luvun, lukujen summan ja lukujen
keskiarvon. Tulosta aliohjelmien palauttamat arvot käyttäjälle. 
Lisää aliohjelmiin sopiva käsittely tyhjille listoille ja dokumentoi ne.

Voit olettaa, että käyttäjä kirjoittaa vain ei-negatiivisia kokonaislukuja
syötteenä. Jos aliohjelma saa syötteenä tyhjän listan, sen tulee palauttaa
arvo -1.

Valmiiden `Collections`-luokan metodien, kuten `Collections.min()` ja
`Collections.max()`, käyttö on kielletty.

<details><summary>Vinkki</summary>

Voit muuntaa merkkijonon numeroksi käyttäen
[`Integer.parseInt(luku)`](https://docs.oracle.com/en/java/javase/25/docs//api/java.base/java/lang/Integer.html#parseInt(java.lang.String))-metodia.

</details>