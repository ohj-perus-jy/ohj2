Laajenna aiemmin tekemääsi verkkokaupan luokkahierarkiaa siten, että lisäät kaksi uutta aliluokkaa `Puhelin` ja `Pakaste`, jotka perivät olemassa olevat luokat `Elektroniikka` ja `Ruoka`.

 1. `Puhelin` (perii `Elektroniikka`)
    * Luo luokka `Puhelin`, joka perii luokan `Elektroniikka`.
    * Lisää luokkaan:
        * attribuutti `String kayttojarjestelma` (esim. "Android" tai "iOS")
        * attribuutti `boolean onko5G`
    * Lisää metodi:
        * `public void soita(String numero)`
        * Metodi tulostaa esimerkiksi: `Soitetaan numeroon 0401234567 (Appleroid, 4G)`
    * Lisäksi:
        * Määrittele `Puhelin`-luokkaan oma versio metodista `tulostaPerustiedot()`
        * Metodin tulee kutsua ensin yliluokan versiota (`super.tulostaPerustiedot();`), ja sitten tulostaa puhelimeen liittyvät lisätiedot (käyttöjärjestelmä ja 5G-tuki).

 2. `Pakaste` (perii `Ruoka`)
    * Luo luokka `Pakaste`, joka perii luokan `Ruoka`.
    * Lisää luokkaan:
        * attribuutti `int lampotilaSuositus` (esim. -18)
    * Lisää metodi:
        * `private void sulata(int minuutit)` (huomaa private-määre)
        * Kun metodia kutsutaan, se tulostaa esimerkiksi: `Sulatat pakastetta 10 minuuttia. Säilytyssuositus: -18 C.`
    * Lisää metodi:
        * `public void sulataJaNauti(int minuutit)`
        * Metodi kutsuu ensin `sulata(minuutit)`-metodia ja sitten `syo()`-metodia.
        * Metodi tulostaa esimerkiksi:
```
Sulatit pakastetta Hernepussi 10 minuuttia. Säilytyssuositus on -18 astetta C.
Syödään Hernepussi.
Parasta ennen oli 31.5.2026, toivottavasti on hyvää.
```

Kokeile luokkia luomalla olioita ja kutsumalla metodeja. Dokumentoi luokat ja metodit huolellisesti.

Tehtäväsivulla on valmiiksi annettuna pääohjelma, jota voit käyttää luokkiesi testaamiseen.