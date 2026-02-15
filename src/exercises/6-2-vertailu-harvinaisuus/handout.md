Laajenna `Kerailykortti`-luokkaa lisäämällä sille attribuutti `String
harvinaisuus`. Keräilykortin harvinaisuus voi olla yksi seuraavista arvoista
(vähiten harvinaisesta harvinaisimpaan): `C`, `U`, `R`, `RR`, `RRR`, `SR`, `AR`,
`SAR`, `UR`.

Kirjoita vertailija, joka järjestää listassa olevat kortit niiden harvinaisuuden
mukaan. Voit käyttää seuraavaa valmista korttikokoelmaa koodisi testaamiseen:

<details closed><summary>Mallilista erilaisista korteista</summary>

```java,ignore
List<Kerailykortti> kortit = new ArrayList<>(List.of(
    new Kerailykortti("Kadonnut Puolipiste", "Koodiviidakko", 101, "C"),
    new Kerailykortti("Loputon Silmukka", "Koodiviidakko", 102, "U"),
    new Kerailykortti("Bugimetsästäjä", "Koodiviidakko", 103, "R"),
    new Kerailykortti("Spagettikoodi-Hirviö", "Koodiviidakko", 104, "RR"),
    new Kerailykortti("Ylikellotettu Prosessori", "Koodiviidakko", 105, "SR"),
    new Kerailykortti("Pyhä Stack Overflow", "Koodiviidakko", 106, "RRR"),
    new Kerailykortti("Null Pointer -Ninja", "Koodiviidakko", 107, "U"),
    new Kerailykortti("Sininen Kuolemanruutu", "Koodiviidakko", 108, "AR"),

    new Kerailykortti("Opiskelijakortti", "Kampus-Saaga", 201, "C"),
    new Kerailykortti("Unelias Luennoitsija", "Kampus-Saaga", 202, "C"),
    new Kerailykortti("Haalaribileet", "Kampus-Saaga", 203, "U"),
    new Kerailykortti("Ylisuorittaja", "Kampus-Saaga", 204, "R"),
    new Kerailykortti("Ilmainen Ämpäri", "Kampus-Saaga", 205, "SAR"),
    new Kerailykortti("Myöhästynyt Palautus", "Kampus-Saaga", 206, "RR"),
    new Kerailykortti("Akateeminen Vartti", "Kampus-Saaga", 207, "SR"),
    new Kerailykortti("Gradu-Ahdistus", "Kampus-Saaga", 208, "AR"),
    new Kerailykortti("Semman Pannukakku", "Kampus-Saaga", 209, "UR"),

    new Kerailykortti("Vihainen Hirvi", "Suomi-Myytit", 301, "C"),
    new Kerailykortti("Ikuinen Marraskuu", "Suomi-Myytit", 302, "RR"),
    new Kerailykortti("Saunaklonkku", "Suomi-Myytit", 303, "SR"),
    new Kerailykortti("Salmiakkisade", "Suomi-Myytit", 304, "U"),
    new Kerailykortti("Väinämöisen Kantele", "Suomi-Myytit", 305, "SAR"),
    new Kerailykortti("Sisu", "Suomi-Myytit", 306, "RRR"),
    new Kerailykortti("Laser-Löylykauha", "Suomi-Myytit", 307, "UR"),
    new Kerailykortti("Toripoliisi", "Suomi-Myytit", 308, "R")
));
```
</details>

Kirjoita `main()`-ohjelma, joka järjestää ja tulostaa keräilykortit
harvinaisuuden mukaan (yleisimmät kortit ensin, harvinaisimmat viimeiseksi).
Kortit, joiden harvinaisuus on jokin muu kuin yllä mainitut tai `null`, tulee
sijoittaa listan alkuun.
