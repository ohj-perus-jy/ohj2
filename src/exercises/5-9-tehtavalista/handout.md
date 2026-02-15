Tee luokka `Tehtavalista`, joka toimii todo-listana. Tehtävät voivat olla
yksinkertaisia merkkijonoja.

Tehtävälista pitää kirjaa sekä tekemättömistä että tehdyistä tehtävistä.
Tehtävät suoritetaan siinä järjestyksessä, missä ne ovat tehtävälistaan lisätty.
Poikkeustapauksia varten tulee olla mahdollista lisätä kiireellisiä tehtäviä
heti tehtävälistan alkuun. 

Ohjelmassa pitää olla myös mahdollisuus kumota tehtävän merkitseminen 
suoritetuksi siltä varalta, että tehtävän merkitsee vahingossa tehdyksi liian 
aikaisin. Kumoaminen palauttaa suoritetuksi merkityn tehtävän takaisin 
tehtävälistan alkuun.

Lisää luokkaan seuraavat metodit:

- `lisaaTehtava`, joka lisää tehtävän tehtävälistaan. Uusi tehtävä menee
  tehtävälistan viimeiseksi.

- `lisaaTarkeaTehtava`, joka lisää kiireellisen tehtävän tehtävälistaan.
  Kiireellinen tehtävä menee aina tehtävälistan ensimmäiseksi.

- `merkitseTehdyksi`, joka merkitsee seuraavana tehtävälistalla olevan tehtävän
  suoritetuksi.

- `kumoaTehty`, joka palauttaa viimeksi tehdyn tehtävän suoritettujen
  tehtävienlistalta takaisin tehtävälistan alkuun.

- `tulosta`, joka tulostaa tekemättömät ja tehdyt tehtävät omina
  listoinaan. Tulostusmuoto ei ole hirveän tärkeä, kunhan tulosteesta näkee
  selvästi eri listat.

Voit testata luokan toimintaa valmiin pääohjelman avulla.
