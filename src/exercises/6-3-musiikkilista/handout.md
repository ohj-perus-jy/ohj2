Olkoon käytössä luokka `Kappale`, joka edustaa yksittäistä musiikkikappaletta.
Kappaleella on nimi, genre ja kesto sekunteina:

```java,ignore
class Kappale {
    String nimi;
    String genre;
    int kestoSekunteina;
}
```

Lisää luokalle tarvittavat näkyvyysmääreet, muodostaja, tarpeelliset
saantimetodit (getterit) sekä sopiva `toString()`-metodin toteutus.

Tee funktio `teeSoittolista(kappaleet, genre, kappaleita)`, joka palauttaa
korkeintaan `kappaleita`-muuttujan ilmoittaman määrän kappaleita, joiden genre
vastaa annettua `genre`-parametria. Kappaleiden tulee olla järjestettynä keston
mukaan lyhyemmästä pisimpään.

Voit käyttää seuraavaa mallilistaa koodisi testaamiseen:

<details closed><summary>Lista mallikappaleista</summary>

```java
List<Kappale> biisilista = List.of(
    new Kappale("Bohemian Rhapsody", "Rock", 354),
    new Kappale("Levitating", "Pop", 203),
    new Kappale("Sandstorm", "Electronic", 225),
    new Kappale("Paranoid", "Metal", 168),
    new Kappale("Toxic", "Pop", 198),
    new Kappale("Master of Puppets", "Metal", 515),
    new Kappale("Cha Cha Cha", "Pop", 175),
    new Kappale("Hotel California", "Rock", 390),
    new Kappale("Stay", "Pop", 141),
    new Kappale("Enter Sandman", "Metal", 331),
    new Kappale("Bad Romance", "Pop", 295),
    new Kappale("Midnight City", "Electronic", 243),
    new Kappale("Billie Jean", "Pop", 294),
    new Kappale("Hard Rock Hallelujah", "Metal", 247),
    new Kappale("Thriller", "Pop", 357),
    new Kappale("As It Was", "Pop", 167),
    new Kappale("Paint It, Black", "Rock", 202),
    new Kappale("Hollywood Hills", "Rock", 210),
    new Kappale("Get Lucky", "Electronic", 369),
    new Kappale("Shake It Off", "Pop", 219),
    new Kappale("Ace of Spades", "Metal", 169),
    new Kappale("Rolling in the Deep", "Pop", 228),
    new Kappale("Sweet Child O' Mine", "Rock", 356),
    new Kappale("Borderline", "Pop", 210),
    new Kappale("Back in Black", "Rock", 255),
    new Kappale("Shape of You", "Pop", 233),
    new Kappale("Fear of the Dark", "Metal", 438),
    new Kappale("Blinding Lights", "Pop", 200),
    new Kappale("Stairway to Heaven", "Rock", 482),
    new Kappale("Uptown Funk", "Pop", 269),
    new Kappale("Smells Like Teen Spirit", "Rock", 301),
    new Kappale("Short Pop Song", "Pop", 120)
);
```

</details>

**Älä käytä silmukoita**, vaan toteuta `teeSoittolista` käyttäen striimejä.

<details closed><summary>Vinkki</summary>

Saatat tarvita ainakin seuraavia `Stream`-metodeja:

- `filter()`: alkioiden suodatus
- `sorted()`: alkioiden järjestäminen
- `limit()`: alkioiden lukumäärän rajaaminen
- `toList()`: alkioiden kerääminen listaksi

</details>
