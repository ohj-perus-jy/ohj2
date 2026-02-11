Tässä tehtävässä rakennat järjestelmän, joka valvoo rakennusten sähkönkulutusta
ja estää sulakkeiden palamisen. Tehtävä koostuu vaiheista.

<details><summary>Vaihe 1: Sähkölaite</summary>

Tee luokka `Sahkolaite`. Laitteilla on kaksi muuttumatonta ominaisuutta: nimi ja
virrankulutus ampeereina.

Lisää attribuutit: `private final String NIMI` ja `private final double VIRTA`.
Oletetaan, että virrankulutus on aina positiivinen luku.

Tee konstruktori, joka asettaa nämä arvot. 

Lisää `private boolean kytketty`, joka kertoo, onko laite päällä.

Tee metodit `kytke()` ja `irrota()`, jotka muuttavat `kytketty`-muuttujan tilaa.
Tee myös `getVirta()`-metodi, joka palauttaa laitteen virrankulutuksen,
vastaavasti `getNimi()`.

Kokeile luokkaasi pääohjelmassa luomalla muutama laite ja kytkemällä niitä
päälle ja pois.

</details>

<details><summary> Vaihe 2: Keskus ja oliolista</summary>

Luo `Sahkokeskus`-luokka. Tämän luokan tarkoituksena on hallita sähkölaitteita. 

Lisää luokkaan attribuutti `final double SULAKKEEN_KOKO`. Sulakkeen koko voi
olla esimerkiksi 16 ampeeria tai 35 ampeeria. Lisää myös `private boolean
sulakePaalla`, joka kertoo, onko sulake ehjä (true) vai palanut (false). Aluksi
sulake on päällä.

Luo `List<Sahkolaite> paallaOlevatLaitteet` (käytä ArrayListia).

Tee metodi `double laskeNykyinenVirta()`, joka käy listan läpi ja laskee laitteiden `VIRTA`-arvojen summan. 

</details>

<details><summary> Vaihe 3: Valvova logiikka ja tilan hallinta</summary>

Keskuksen on päätettävä, saako laitteen kytkeä päälle.

Tee metodi `boolean kytke(Sahkolaite laite)`. Metodin tulee tarkistaa, onko nykyinen virta + uuden laitteen virta <= sulakekoko. Jos on, laite lisätään listaan ja sille kutsutaan `laite.kytke()`. Muussa tapauksessa sulake palaa: `aseta sulakePaalla = false`, sammuta kaikki listan laitteet (`irrota()`) ja tyhjennä päälläolevien laitteiden lista.

Tee myös metodi `void irrota(Sahkolaite laite)`, joka poistaa laitteen listasta ja kutsuu `laite.irrota()`.

</details>

<details><summary> Vaihe 4: Globaali seuranta</summary>

Sähköyhtiö haluaa seurata kaikkien keskusten tilannetta.

Lisää `Sahkokeskus`-luokkaan `static double kokonaisKulutusValtakunnassa`.

Päivitä tätä muuttujaa aina, kun jokin laite missä tahansa keskuksessa kytketään päälle, irrotetaan sähkökeskuksesta tai kun sulake palaa.

Lisää static-metodi `tulostaValtakunnanTilanne()`, joka tulostaa kokonaiskulutuksen.
</details>

Voit testata ohjelmaasi TIMissä olevalla valmiilla pääohjelmalla, tai voit kirjoittaa oman testiohjelmasi.

