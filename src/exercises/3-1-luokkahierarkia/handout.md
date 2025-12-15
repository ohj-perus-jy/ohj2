Tee luokkahierarkia verkkokaupalle. Yliluokasta `Tuote` periytyvät aliluokat `Elektroniikka`, `Vaate` ja `Ruoka`. 

Määrittele yhteiset ominaisuudet `nimi`, `hinta` sekä metodi `tulostaPerustiedot()` `Tuote`-luokassa. 

<!-- Tämä ei toimi, koska meillä ei ole vielä abstrakteja luokkia: Määrittele myös renkaiden lukumäärä, jonka tulee olla vakio.  -->

<!-- Käyttövoima voi olla esimerkiksi "bensiini", "sähkö" tai "reisilihakset". TODO: Tehdäänkö tästä enum? -->

Lisää erityispiirteitä kuhunkin aliluokkaan:

 * `Vaate`: attribuutti `koko` (esim. "M", "L", jne.), metodi `sovita(String sovittajanKoko)`, joka tulostaa, onko vaate sopiva sovittajalle.
 * `Elektroniikka`: attribuutti `takuuKuukausina` (esim. 24), metodi `testaaLaite()`, joka tulostaa "Laite toimii moitteettomasti vielä X kuukautta." (X on `takuuKuukausina`-arvo).
 * `Ruoka`: attribuutti `parastaEnnen` (esim. "2026-01-31"), ja metodi `syo()`, joka tulostaa "Nautit ruoan, jonka viimeinen käyttöpäivä on YYYY-MM-DD." (korvaa YYYY-MM-DD `parastaEnnen`-arvolla).

Testaa luokkia luomalla olioita ja kutsumalla metodeja. Dokumentoi luokat ja metodit huolellisesti.