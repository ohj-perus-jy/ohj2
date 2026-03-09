Palauta osan 8.5 perusteella edistetty projekti. Kertaus tämän osan vaiheista:

- Lisää projektiin yksikkötestit.
- Eriytä tehtävien tallennus ja lataus erilliseen luokkaan, joka toteuttaa `TehtavaRepository`-rajapinnan.
- Tee testipakkaukseen mock-luokka, joka toteuttaa `TehtavaRepository`-rajapinnan, mutta tallentaa datan vain muistissa.
- Testaa tiedoston tallennus/lataus.

Kun vaihe on valmis, tee `git add` muuttuneille tiedostoille ja `git commit`.

Palauta `TehtavaRepository`-rajapinta sekä `JsonTehtavaRepository`, 
`MockTehtavaRepository` ja `TehtavakokoelmaTest`-luokat. Muita luokkia tai 
FXML-tiedostoja ei tarvitse palauttaa.
