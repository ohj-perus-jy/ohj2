
 1. Muuta `Ajoneuvo`-luokka abstraktiksi luokaksi. 
 2. Määrittele `Ajoneuvo`-luokkaan abstrakti metodi `aloitaAjaminen()`. Metodi ei palauta mitään eikä ota parametreja.
 3. Toteuta `aloitaAjaminen()`-metodi kaikissa aliluokissa (`Auto`, `Moottoripyora`, `Polkupyora`) siten, että se tulostaa konsoliin kyseiselle ajoneuvolle sopivan tekstin (esim. Auto: "Moottori hörähtää käyntiin", Polkupyörä: "Polkaisu vauhtiin").
 4. Luo lista, jonka alkioiden tyyppi on `Ajoneuvo`, ja lisää sinne eri aliluokkien olioita. Käy lista läpi silmukalla ja kutsu jokaiselle `aloitaAjaminen()`-metodia.

