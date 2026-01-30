Lisää `Auto`-luokkaan attribuutti `int ajokilometrit`. Lisää
`Lentokone`-luokkaan attribuutti `int lentotunnit`. Lisää kummallekin luokalle
uusi konstruktori, jossa nämä attribuutit asetetaan. Muokkaa aiempaa
konstruktoria niin, että nämä attribuutit saavat arvon 0.

Muuta `liiku()`-metodeja siten, että ne kasvattavat näitä arvoja. `Auto`-luokan
`liiku()`-metodi kasvattaa `ajokilometrit`-attribuuttia 10:llä ja
`Lentokone`-luokan `liiku()`-metodi kasvattaa `lentotunnit`-attribuuttia 1:llä.

Ylikirjoita vielä `Ajoneuvo`-luokassa metodi `toString()`, joka palauttaa
tekstin "Ajoneuvon \<merkki\> tiedot: ". Ylikirjoita tämä metodi edelleen
`Auto`- ja `Lentokone`-luokissa siten, että ne palauttavat **lisäksi**
ajokilometrit tai lentotunnit.