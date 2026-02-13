Toteuta oma yksinkertainen hajautustaulu.

Käytä hajautustaulun päätietorakenteena taulukkoa. Voit käyttää törmäysten
käsittelyyn esimerkiksi listaa, eli samaan indeksiin osuvat alkiot laitetaan
siinä indeksissä sijaitsevaan listaan alkioista. Alkioita ei saa kadota
törmäysten yhteydessä.

Hajautustaulun kapasiteetilla voi olla oletusarvona 10 tai se voi ottaa arvon 
parametrina muodostajassa. Kapasiteetin ei tarvitse muuttua missään vaiheessa 
ohjelman suorituksen aikana, eli taulun käyttöastetta ei tarvitse huomioida tai
toteuttaa.

Javan `hashCode` voi palauttaa negatiivisen arvon, joten kannattaa käyttää 
itseisarvoa negatiivisen indeksin välttämiseksi.

Lisää metodi `hae`, joka hakee alkion hajautustaulusta sen avaimen perusteella.
Lisää myös metodit `lisaa` ja `poista` alkioiden lisäämistä ja poistamista
varten.
