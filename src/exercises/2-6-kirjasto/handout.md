Toteuta luokka `Kirja`, joka pitää kirjaa yksittäisistä kirjoista, mutta myös seuraa kirjaston tilastoja globaalisti.
Luo luokalle seuraavat muuttujat:

Oliomuuttujat: 

 * `String nimi`: Kirjan nimi.
 * `String kirjoittaja`: Kirjan kirjoittaja.
 * `boolean onLainassa`: Kertoo, onko kyseinen kirja tällä hetkellä lainassa.

Luokkamuuttujat (static):

 * `static int kirjojenMaara`: Kuinka monta kirjaa on luotu yhteensä.
 * `static int lainassaOlevat`: Kuinka monta kirjaa on tällä hetkellä lainassa.

Muodostajan tulee ottaa vastaan nimi ja kirjoittaja. Aina kun uusi kirja luodaan, `kirjojenMaara`-muuttuja kasvaa yhdellä.

Tee oliometodit `lainaa()` ja `palauta`: Nämä muuttavat kirjan `onLainassa`-tilaa ja päivittävät staattisen `lainassaOlevat`-laskurin.

Tee staattinen metodi `tulostaTilastot()`, joka tulostaa ruudulle kirjaston tilastot: "Kirjasto sisältää X kirjaa, joista Y on lainassa."

Saat valmiina pääohjelman, jota voit käyttää ohjelmasi testaamiseen