Tee luokkahierarkia verkkokaupalle. Yliluokasta `Tuote` periytyvät aliluokat `Elektroniikka`, `Vaate` ja `Ruoka`. 

Määrittele `Tuote`-luokkaan yhteiset ominaisuudet `nimi`, `hinta` sekä metodi `tulostaPerustiedot()`.

Lisää erityispiirteitä kuhunkin aliluokkaan:

 * `Vaate`: attribuutti `String koko` (esim. "M", "L", jne.), metodi `sovita(String sovittajanKoko)`, joka tulostaa, onko vaate sopiva sovittajalle.
 * `Elektroniikka`: attribuutti `int takuuKuukausina` (esim. 24), metodi `testaaLaite()`, joka tulostaa "Laite toimii moitteettomasti vielä X kuukautta." (X on `takuuKuukausina`-arvo).
 * `Ruoka`: attribuutti `String parastaEnnen` (esim. "2026-01-31"), ja metodi `syo()`, joka tulostaa "Nautit ruoan, jonka viimeinen käyttöpäivä on YYYY-MM-DD." (korvaa YYYY-MM-DD `parastaEnnen`-arvolla).

Kokeile luokkia luomalla olioita ja kutsumalla metodeja. Dokumentoi luokat ja metodit huolellisesti.

Tehtäväsivulla on valmiiksi annettuna pääohjelma, jota voit käyttää luokkiesi testaamiseen.