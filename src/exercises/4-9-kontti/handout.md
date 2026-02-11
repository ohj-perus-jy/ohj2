Tee luokka `Kontti`, joka hyödyntää geneerisyyttä ja toimii yksinkertaisena
säiliönä yhdelle minkä tahansa tyypin oliolle.

Lisää luokkaan attribuutti `sisalto`, joka voi sisältää minkä tahansa
tyyppisen olion. Lisää myös merkkijono `omistaja`. Tee luokkaan muodostaja, joka
ottaa nämä arvot vastaan parametreina.

Lisää lisäksi saantimetodit `getOmistaja`, `getSisalto` ja `getTyyppi`, joista
viimeinen palauttaa kontin sisällön tyypin merkkijonona. Tee myös override
`toString`-metodille, joka palauttaa nämä tiedot yhdessä merkkijonossa.

Tehtävässä on valmiiksi pääohjelma, jolla voit kokeilla luokan toimintaa.

<details><summary>Vinkki</summary>

Olion tyypin saa merkkijonona metodilla `olio.getClass().getSimpleName()`.

</details>
