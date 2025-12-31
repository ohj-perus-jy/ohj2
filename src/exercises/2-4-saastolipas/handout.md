Toteuta luokka `Saastolipas`, jonka tarkoituksena on säilyttää rahaa.

Attribuutit:

 * `private double saldo`: Säästölippaan nykyinen rahamäärä.
 * `private String omistaja`: Lippaan omistajan nimi.
 * `private final String SALASANA`: Salasana, joka tarvitaan rahojen nostamiseen.

Konstruktori: Ottaa vastaan `omistaja` ja `SALASANA` -arvot. Asettaa
alkusaldoksi 0.0.

Metodit:

 * `public void talleta(double maara)`: Lisää rahaa vain, jos maara on positiivinen.
 * `public double nosta(double maara, String annettuSalasana)`: Tarkistaa, onko annettuSalasana oikein. Tarkistaa, onko lippaassa tarpeeksi rahaa. Jos molemmat täyttyvät, vähentää saldon ja palauttaa nostetun määrän. Muuten palauttaa 0.0 ja tulostaa virheilmoituksen.
 * `public void tulostaSaldo()`: Tulostaa saldon, mutta ei paljasta salasanaa.