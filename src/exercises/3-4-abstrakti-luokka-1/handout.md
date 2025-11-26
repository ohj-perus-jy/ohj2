Pelkän `Ajoneuvo`-luokan olion luominen ei ole järkevää, sillä jokainen ajoneuvo on todellisuudessa jokin tietty tyyppi (kuten auto tai pyörä). 

Lisäksi kaikilla ajoneuvoilla on jokin tapa käynnistyä tai lähteä liikkeelle, mutta se tapahtuu eri tavalla.

 1. Muuta `Ajoneuvo`-luokka abstraktiksi luokaksi. 
 2. Määrittele `Ajoneuvo`-luokkaan abstrakti metodi `aloitaAjaminen()`. Metodi ei palauta mitään eikä ota parametreja.
 3. Toteuta `aloitaAjaminen()`-metodi kaikissa aliluokissa (`Auto`, `Moottoripyora`, `Polkupyora`) siten, että se tulostaa konsoliin kyseiselle ajoneuvolle sopivan tekstin (esim. Auto: "Moottori hörähtää käyntiin", Polkupyörä: "Polkaisu vauhtiin").
 4. Kokeile pääohjelmassa: Yritä luoda olio luokasta `Ajoneuvo`. Mitä tapahtuu?
 5. Luo lista, jonka alkioiden tyyppi on `Ajoneuvo`, ja lisää sinne eri aliluokkien olioita. Käy lista läpi silmukalla ja kutsu jokaiselle `aloitaAjaminen()`-metodia.

