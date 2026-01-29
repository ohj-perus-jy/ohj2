Tee luokka `Ajoneuvo`, jolla on attribuutti `String merkki` ja konstruktori joka
asettaa tämän arvon. Lisää myös metodi `liiku()`, joka ei tee mitään.

Peri `Ajoneuvo`-luokasta luokat `Auto` ja `Lentokone`. Tee `Auto`- ja
`Lentokone`-luokkiin `liiku()`-metodi, joka ylikirjoittaa `Ajoneuvo`-luokan
`liiku()`-metodin. `Auto`-olio tulostaaa "Auto \<merkki\> ajaa maantiellä
renkaat vinkuen.", ja `Lentokone`-olio "Lentokone \<merkki\> nousee kiitotieltä
ja lentää pilvien päällä.".

Tee pääohjelma, jossa luot kaksi `Ajoneuvo`-muuttujaa (ei siis `Auto`- tai
`Lentokone`-tyyppisiä), ja sijoitat niihin `Auto`-olion ja `Lentokone`-olion.
Kutsut kummankin olion `liiku()`-metodia.
