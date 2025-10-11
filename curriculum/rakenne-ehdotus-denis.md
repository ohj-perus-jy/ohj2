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
| 1 | Java-kielen perusteet, IO | - Muistaa ohjelmoinnin peruskäsitteet
- Muistaa, miten käytetään ehtoja, silmukoita, muuttujia
- Osaa avata ja lukea tiedostoja yksinkertaisesti (Files API + for each) |
| 2 | OOP-perusteet | - Oppii, mitä on luokka ja olio
- Ymmärtää, että oliot välittyvät viitteenä
- Ymmärtää OOP:n tarkoituksen ⇒ olioiden yhteistyö |
| 3 | OOP | - Ymmärtää perintää ja rajapintoja
- Ymmärtää, mitä polymorfismi tarkoittaa ja osaa soveltaa
- Osaa saada useamman luoken pelittämään toisensa kanssa |
| 4 | Algoritmit, tietorakenteet  | - Tietorakenteet (List, HashMap)
- Tietovirrat ja scannerit
- OOP:n soveltaminen jatkuu tehtävissä |
| 5 | Algoritmit, tietorakenteet, lambdat, rekursio | - Javan Streams API ja siihen liittyvät kaverit (esim. Files API)
- Funktio-oliot
- Rekursio
- OOP:n soveltaminen jatkuu tehtävissä |
| 6 | Testaaminen ja lisää IO | - Oliopohjaisen ohjelman testaus, TDD, (ehkä pöytätestit) |
| 7 | GUI | - JavaFX, SceneBuilder
- Miten GUI-ohjelmat yleensä toimii (esim. MVC)
- Tapahtumat
- Tässä ehkä “tutorialin” aloitus |
| 8 | GUI | - Komponentteja, dialogeja, GUI:n layout
- Datan ja GUIn yhdistäminen |
| 9 | Tietorakenteet, tyyppiparametrit | - Osaa tehdä oman ArrayList, LinkedList, ehkä HashMap
- Osaa käyttää tyyppiparametreja (eli tehdä ArrayList<T>) |
| 10 | OO-pohjainen suunnittelu | - Oman projektin suunnittelu
- UML, CRC (class-responsibility-collaboration) -kortit
- Jotain design patterneja ehkä |
| 11 | Oma projekti | - Oman projektin työstäminen |
| 12 | Oma projekti | - Oman projektin työstäminen |