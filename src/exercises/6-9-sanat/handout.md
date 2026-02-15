Lataa aineisto: [sanat.txt](/exercises/6-9-sanat/sanat.txt)

Tallenna tiedosto projektisi työskentelyhakemistoon nimellä `sanat.txt`.

Tiedostossa on yksi sana per rivi. Mukana on tarkoituksella tyhjiä rivejä,
välilyöntejä sanojen alussa/lopussa,  samoja sanoja useaan kertaan,  eri
kirjainkokoja (esim. Java, java, JAVA).

Esimerkki aineiston alusta:

```
  Java
python

JAVA
CSharp
  java  
```


Tee ohjelma, joka:

 * Lukee kaikki rivit.
 * Poistaa sanoista ylimääräiset välilyönnit  ja muuttaa sanat pieniksi
   kirjaimiksi. Vinkki: `String.trim()` ja `String.toLowerCase()`.
 * Poistaa tyhjät rivit.
 * Poistaa duplikaatit.
 * Järjestää sanat aakkosjärjestykseen.
 * Kirjoittaa uuden tiedoston data/sanat-siisti.txt, jossa on siistitty sanalista (yksi sana per rivi).
 * Kirjoittaa lisäksi tiedoston data/raportti.txt, jossa on:
    * alkuperäisten rivien määrä
    * siistittyjen sanojen määrä
    * pisin sana (jos useita, mikä tahansa kelpaa). Vinkki: Jos ratkaiset
      tehtävän Stream API:lla, voit käyttää `Stream.max(Comparator)`-metodia pisimmän sanan löytämiseen.

Vinkki: tee ensin `List<String> siistit = ...`, ja kirjoita lopuksi
`Files.write(...)` kahteen eri tiedostoon.

Tulosteen pitäisi näyttää tältä: 

```
Alkuperäisiä rivejä: 1074
Siistittyjä sanoja: 59
Pisin sana: binarytree
```