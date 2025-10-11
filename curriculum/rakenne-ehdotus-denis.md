# Ohj2

## OPS-vaatimukset

- Oliopohjaisen ohjelmoinnin perusteet
- Testaaminen, erityisesti TDD
- Graafisen käyttöliittymän suunnittelu
- Java
- Ohjelman suunnittelu
- Rekursio

## Tämänhetkinen Ohj2 Vesan curriculum

- Viikko 1: Ohjelman suunnittelu
    - Agile, Algoritmeja (lajittelualgoritmit, binäärihaku)
    - Demoissa: Harjoitustyön vaihe 1, algoritmin suunnittelu sanallisesti, aikakompleksisuus, Javan oppiminen Ohj1 tehtävien kautta
- Viikko 2: Aikakompleksisuus, GUI:n teko SceneBuilderilla
    - O-notaatio, aikakompleksisuus, kertaus syntaksista (ehtolauseet, silmukat, muuttujat), pöytätestaus
    - Demoissa: Aikakompleksisuus, binäärihaku, algoritmin suunnittelu, pöytätestaus, taulukko taulukoista (T[][]), boolean-algebraa, regex
- Viikko 3: Java-kieli, Viitteet, GUI
    - Eri ohjelmointikieliä, viitteiden perusteet, olio-ohjelmoinnin pohjustus, GUI-ohjelman teko
    - Demoissa: globbing (algoritmin suunnittelu ja Java-toteutus yhden kirjaimen wildcardille), yksinkertaisen luokan tekeminen, GUI-ohjelman tekeminen, koodin refaktorointi, viitteet, RPN-laskin
- Viikko 4: Olio-ohjelmointi, pöytätestaus
    - Perintä, testaaminen JUnitilla, ComTest, näkyvyysalueet
    - Demoissa: Viitteet, GUI, Java-kielen harjoittelua, pöytätestaus, koodin refaktorointi, luokan kirjoittaminen, RPN-laskin
- Viikko 5: Olio-ohjelmointi, GUI
    - Metodit, usean olion välinen toiminta, GUI-ohjelman teko
    - Demossa: constructorit ja niiden ylikuormitus, parsiminen, luokan kirjoittaminen, GUI-ohjelma (äänestys), luokan suunnittelu, OutputStream (yleisesti Stream), bittioperaatiot, koodin refaktorointi
- Viikko 6: Olioiden suunnittelu, Dialogit GUI:ssa, polymorfismi
    - CRC-kortit, Oliokaavio (”melkein UML”), rajapinnat, polymorfismi
    - Demoissa: luokan toteutus, Javan compareTo ja equals -metodit, rajapinnan tekeminen, CRC-kortit ja oliokaavio, Mock-luokat, Astiapeli
- Viikko 7: GUI, MVC
    - GUI-ohjelman tekeminen alusta loppuun, tietorakenteen ja GUI:n yhteistyö
    - Demoissa: Javan String-luokka, algoritmien suunnittelu (if-lauseet vs. lookup-taulu), StringBuilder, luokkien suunnittelu, GUI-ohjelman tekeminen, Astiapeli
- Viikko 8: ArrayList tekeminen, Javan valmiit tietorakenteet
    - Oman ArrayList tekeminen, Javan Vector, ArrayList
    - Demoissa: Luokat, Koodin refaktorointi, T[][], Astiapeli, julkisuusmääreet
- Viikko 9: I/O, Iteraattori
    - Tiedostojen IO (Stream, Scanner, jne.), Iteraattorirajapinta, GUI, linkitetyt listat
    - Demoissa: pöytätesti, IO, luokan tekeminen, GUI
- Viikko 10: Kertausta, lambdat
    - Lambdat, Olio-ohjelmoinnin kertausta
    - Demoissa: Viitteet, IO, oma ArrayList, tyyppiparametrit, oma linkitetty lista, iteraattorit, luokat
- Viikko 11: GUI (erityisesti MVC/tiedon näyttäminen), ORM
    - GUI, oma ORM GUI:hin
    - Stream API, Ohjelman luominen, GUI, IO, kutsupino, lambdat, Astiapeli
- Viikko 12: Algoritmit, oikeellisuustarkistus
    - Oikeellisuustarkistus, GUI, haku- ja lajittelualgoritmit GUI-ohjelmaan
    - Demoissa: TreeMap, Ohjelman luominen, IO, parsiminen, Viitteet, GUI, koodin refaktorointi

## Curriculum

- Kesto: 8 + 4 viikkoa
- Ensimmäinen osa vastaa noin 5 op
    - Aiheina Java, OOP, TDD, I/O
    - Osan loppupuolella Ohjelman suunnittelu ja GUI, jolloin tehdään ohjatusti jokin oma GUI-ohjelma alusta loppuun (vrt. nykyisessä Ohj2 AstiaPeli, RPN-laskin)
- Toinen osa vastaa noin 3 op
    - Oliopohjaisen ohjelman suunnittelun periaatteet, ArrayList, tyyppiparametrit
    - Osassa tehdään oma projekti (esim. tutorialin laajentaminen, tai joku oma GUI-sovellus)

| Viikko | Aihe | Osaamistavoitteet |
| --- | --- | --- |
| 1 | Java-kielen perusteet, IO | <ul><li>Muistaa ohjelmoinnin peruskäsitteet</li><li>Muistaa, miten käytetään ehtoja, silmukoita, muuttujia</li><li>Osaa avata ja lukea tiedostoja yksinkertaisesti (Files API + for each)</li></ul> |
| 2 | OOP-perusteet | <ul><li>Oppii, mitä on luokka ja olio</li><li>Ymmärtää, että oliot välittyvät viitteenä</li><li>Ymmärtää OOP:n tarkoituksen ⇒ olioiden yhteistyö</li></ul> |
| 3 | OOP | <ul><li>Ymmärtää perintää ja rajapintoja</li><li>Ymmärtää, mitä polymorfismi tarkoittaa ja osaa soveltaa</li><li>Osaa saada useamman luokan pelittämään toisensa kanssa</li></ul> |
| 4 | Algoritmit, tietorakenteet | <ul><li>Tietorakenteet (List, HashMap)</li><li>Tietovirrat ja scannerit</li><li>OOP:n soveltaminen jatkuu tehtävissä</li></ul> |
| 5 | Algoritmit, tietorakenteet, lambdat, rekursio | <ul><li>Javan Streams API ja siihen liittyvät kaverit (esim. Files API)</li><li>Funktio-oliot</li><li>Rekursio</li><li>OOP:n soveltaminen jatkuu tehtävissä</li></ul> |
| 6 | Testaaminen ja lisää IO | <ul><li>Oliopohjaisen ohjelman testaus, TDD, (ehkä pöytätestit)</li></ul> |
| 7 | GUI | <ul><li>JavaFX, SceneBuilder</li><li>Miten GUI-ohjelmat yleensä toimii (esim. MVC)</li><li>Tapahtumat</li><li>Tässä ehkä “tutorialin” aloitus</li></ul> |
| 8 | GUI | <ul><li>Komponentteja, dialogeja, GUI:n layout</li><li>Datan ja GUIn yhdistäminen</li></ul> |
| 9 | Tietorakenteet, tyyppiparametrit | <ul><li>Osaa tehdä oman ArrayList, LinkedList, ehkä HashMap</li><li>Osaa käyttää tyyppiparametreja (eli tehdä ArrayList<T>)</li></ul> |
| 10 | OO-pohjainen suunnittelu | <ul><li>Oman projektin suunnittelu</li><li>UML, CRC (class-responsibility-collaboration) -kortit</li><li>Jotain design patterneja ehkä</li></ul> |
| 11 | Oma projekti | <ul><li>Oman projektin työstäminen</li></ul> |
| 12 | Oma projekti | <ul><li>Oman projektin työstäminen</li></ul> |