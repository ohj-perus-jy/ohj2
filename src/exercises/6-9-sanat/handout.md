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
 * Poistaa duplikaatit. (Vinkki: `distinct()`-metodi Stream API:lla, tai
   `Set`-kokoelma.)
 * Järjestää sanat aakkosjärjestykseen. (Vinkki: `sorted()`-metodi Stream
   API:lla, tai `Collections.sort()`-metodi Listalla.)
 * Kirjoittaa uuden tiedoston `output/sanat-siisti.txt`, jossa on siistitty sanalista (yksi sana per rivi).
 * Kirjoittaa lisäksi tiedoston `output/raportti.txt`, jossa on:
    * alkuperäisten rivien määrä
    * siistittyjen sanojen määrä
    * pisin sana (jos useita, mikä tahansa kelpaa). Vinkki: Jos ratkaiset
      tehtävän Stream API:lla, voit käyttää `Stream.max(Comparator)`-metodia pisimmän sanan löytämiseen.

Vinkki: tee ensin `List<String> siistit = ...`, ja kirjoita lopuksi
`Files.write(...)` kahteen eri tiedostoon.

`raportti.txt`:n pitäisi näyttää tältä: 

```
Alkuperäisiä rivejä: 1074
Siistittyjä sanoja: 59
Pisin sana: binarytree
```
