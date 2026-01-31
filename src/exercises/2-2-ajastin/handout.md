Tee luokka `Ajastin`, jolla on attribuutit `minuutit` ja `sekunnit`
kokonaislukuina. 

Lisää luokkaan metodit `lisaaMinuutteja` ja `lisaaSekunteja`, jotka ottavat
parametrina ajastimeen lisättävät minuutit ja sekunnit. Lisää myös metodi
`annaMerkkijono`, joka antaa ajastimen minuutit ja sekunnit merkkijonona.

Minuutteja voi olla kuinka monta tahansa, mutta sekuntien täytyy olla välillä
0-59. Jos sekunnit ylittävät rajan, muutetaan ne minuuteiksi. Sekunnit voi
muuttaa minuuteiksi + sekunneiksi esimerkiksi näin:

```java
int sekunteja = 75; // Esimerkki parametrina tulevasta arvosta

// Tämä antaa this.minuutteja-attribuuttiin _lisättävät_ minuutit
int lisattaviaMinuutteja = (this.sekunteja + sekunteja) / 60; 

// Tämä antaa this.sekunteja-attribuuttiin _sijoitettavat_ sekunnit
int jaljelleJaavatSekunnit = (this.sekunteja + sekunteja) % 60;  
```

Voit testata luokan toimintaa valmiin pääohjelman avulla.
