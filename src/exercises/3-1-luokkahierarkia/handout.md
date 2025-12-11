Tee luokkahierarkia ajoneuvoille. Yliluokasta `Ajoneuvo` periytyvät aliluokat `Auto`, `Moottoripyora` ja `Polkupyora`. 

Määrittele yhteiset ominaisuudet (`nopeus`, `paino`) ja metodit (`kiihdyta()`, `jarruta()`) `Ajoneuvo`-luokassa. 

<!-- Tämä ei toimi, koska meillä ei ole vielä abstrakteja luokkia: Määrittele myös renkaiden lukumäärä, jonka tulee olla vakio.  -->

Kiihdyttäminen kasvattaa ajoneuvon nopeutta ja jarruttaminen vähentää sitä. Mitä raskaampi ajoneuvo on, sitä hitaammin se kiihtyy (vaikkapa kaavalla `nopeus += 1000 / paino;`) ja sitä tehokkaammin se jarruttaa (kaavalla `nopeus = nopeus - 1000 / paino`). Nopeus ei saa mennä negatiiviseksi.

<!-- Käyttövoima voi olla esimerkiksi "bensiini", "sähkö" tai "reisilihakset". TODO: Tehdäänkö tästä enum? -->

Lisää erityispiirteitä kuhunkin aliluokkaan:

 * `Auto`: `ovienLukumaara`
 * `Moottoripyora`: `sivuvaunu`
 * `Polkupyora`: `vaihteidenLukumaara`

Testaa luokkia luomalla olioita ja kutsumalla metodeja. Dokumentoi luokat ja metodit huolellisesti.
