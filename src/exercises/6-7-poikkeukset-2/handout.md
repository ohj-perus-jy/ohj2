Tee ohjelma, joka tarkistaa, onko käyttäjän syöttämä ikä riittävä tiettyyn
toimintaan, esimerkiksi ajokortin hankkimiseen. 

Tee aliohjelma `onkoIkaa`, joka ottaa parametrina iän (`int`) ja palauttaa
`true`, jos ikä on riittävä. Jos ikä on alle 18, heitä poikkeus `IkaException`,
joka on oma tarkastettu poikkeusluokka. Anna sopiva poikkeusviesti, esimerkiksi
"Ikä ei riitä.". Ohessa vinkiksi metodin esittelyrivi.

```java,ignore
static boolean onkoIkaa(int ika) throws IkaException
```

Jos ikä on negatiivinen, heitä poikkeus `IkaException` viestillä "Ikä ei voi olla negatiivinen.".

Muokkaa `main`-metodia niin, että se kääntyy. 