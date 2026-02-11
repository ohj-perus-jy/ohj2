Tee aliohjelma `keskiarvo`, joka palauttaa kokonaislukutaulukon lukujen
keskiarvon. Kirjoita ensin suoraviivainen versio, joka olettaa että taulukossa
on ainakin yksi alkio.

Tee `main`, joka testaa ainakin nämä tapaukset:

 * `new int[] { 2, 4, 6 }`
 * `new int[] { }` (tyhjä taulukko)

Heitä tyhjän taulukon kohdalla `IllegalArgumentException`-poikkeus. Käsittele
poikkeus `main`-metodissa `try-catch`-rakenteella ja tulosta käyttäjälle informatiivinen viesti.