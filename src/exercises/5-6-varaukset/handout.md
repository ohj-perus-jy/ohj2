Tee luokka `Varaukset`, joka tallentaa varauksia. Yhdelle päivämäärälle voi olla
**vain yksi** varaus ja varauksen tekijän nimi täytyy myös tallentaa. 

Päivämääränä voit tässä tehtävässä käyttää merkkijonoa, jonka muoto on 
`YYYY-MM-DD` eli vuodet, kuukaudet ja päivät. Voit myös olettaa, että 
päivämäärät ovat aina oikeassa muodossa.

Toteuta luokkaan seuraavat metodit:

- `lisaaVaraus` ottaa parametrina päivämäärän ja varaajan nimen 
  merkkijonona ja lisää varauksen tietorakenteeseen. Jos päivämäärälle on jo
  varaus, uusi varaus ei saa korvata sitä. Metodi palauttaa `true`, jos uusi
  varaus lisätään tietorakenteeseen , muuten `false`.

- `poistaVaraus` ottaa parametrina päivämäärän ja poistaa sille päivälle
  sijoittuvan varauksen. Metodi palauttaa `true`, jos varaus poistetaan
  tietorakenteesta, muuten `false`.

- `tulostaVaraukset` ottaa parametrina alku- ja loppupäivämäärän ja tulostaa
  kaikki näiden väliin sijoittuvat varaukset 
  **varauksen päivämäärän mukaan järjestettynä**.

Voit testata luokan toimintaa valmiin pääohjelman avulla.

<details><summary>Vinkki</summary>

Tietorakennetta ei tässä tapauksessa kannata järjestää itse. Yksi 
`Map`-rajapinnan toteuttavista luokista pitää alkiot aina järjestyksessä.

</details>
