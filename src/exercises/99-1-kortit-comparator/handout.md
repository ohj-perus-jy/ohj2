Tehtävässä on pohjana luokka `Kerailykortti`, jolla on attribuutit `nimi` ja
`harvinaisuusluokka` sekä niiden getterit.

Tee vertailuluokka `KortitHarvinaisuudenMukaanVertailu`, joka toteuttaa
`Comparator<Kerailukortti>` rajapinnan.
Rajapinnan `compare`-metodin tulee järjestää kortit
harvinaisuuden mukaan siten, että harvinaisimmat kortit tulevat ensin.

Tämän jälkeen toteuta `Main.java`-tiedostoon metodi
`void kortitHarvinaisuudenMukaan(List<KerailyKortti> kortit)`,
joka ottaa parametrina listan keräilykorteista ja järjestää
ne harvinaisuuden mukaan käyttäen `KortitHarvinaisuudenMukaanVertailu`-vertailuluokkaa.
