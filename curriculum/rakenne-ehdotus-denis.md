# Ohj2

## OPS-vaatimukset

- Oliopohjaisen ohjelmoinnin perusteet
- Testaaminen, erityisesti TDD
- Graafisen käyttöliittymän suunnittelu
- Java
- Ohjelman suunnittelu
- Rekursio



<details closed><summary><b>Tämänhetkinen Vesan curriculum</b></summary>

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

</details>

## Curriculum v2

### Viikkoaiheet ja tavoitteet

- Kesto: 8 + 4 viikkoa
- Ensimmäinen osa vastaa noin 5 op
    - Aiheina Java, OOP, TDD, I/O
    - Osan loppupuolella Ohjelman suunnittelu ja GUI, jolloin tehdään ohjatusti jokin oma GUI-ohjelma alusta loppuun (vrt. nykyisessä Ohj2 AstiaPeli, RPN-laskin)
- Toinen osa vastaa noin 3 op
    - Oliopohjaisen ohjelman suunnittelun periaatteet, ArrayList, tyyppiparametrit
    - Osassa tehdään oma projekti (esim. tutorialin laajentaminen, tai joku oma GUI-sovellus)

### Suoritustapa

- Jokaisella viikolla 6-10 viikkotehtävää ja ylöspäin eriyttäviä lisätehtäviä
   - Paitsi viikko 12, joka on varattu työn viimeistelyyn ja palauttamiseen
   - Viikoilla 1-8 tehtävät liittyen viikon aiheeseen
   - Viikkojen 9-12 aikana omatoiminen miniprojekti => viikkotehtävät liittyvät oman projektin edistämiseen (esim. suunnittelukaavion piirtäminen), tukevat projektin edistämistä
   - **TODO:** Paljonko % tehtävistä tulee palauttaa?
   - **TODO:** Miten vaikuttaa arvosanaan (tai vaikuttaako)?
- Ohjattu tutorial viikoilla 7-8 ja miniprojekti viikoilla 9-12 => tulee palauttaa
   - Arvioidaan hyväksytty/hylätty
   - 2-3 muun palautuksen vertaisarviointi => tähän valmis tarkistuslista (vrt. Hiven projekti)
- Tentti
   - **TODO:** Miten vaikuttaa arvosanaan?

Lisäksi vaihtoehtona

- Jos osoittaa opetettavien asioiden osaamista, voi tehdä miniprojektin ilman viikkotehtäviä + tentti
- Jos osoittaa opetettavien asioiden osaamista omalla projektilla, joka vastaa miniprojektin vaatimuksia, niin voi suorittaa suoraan tentillä


### Materiaalien rakenteesta

- Materiaalit jaettu viikkoihin
- Jokaisen viikon asia jaettu alaosiin (vrt. Samin rakenne)
   - Jokaisessa alaosassa on materiaali, esimerkkejä, kokeile itse -harjoituksia (esimerkkien muokkaus, ei anna pisteitä), ehkä pätkä luennosta, jossa asia on käyty läpi?
   - Alaosassa on joko lopussa tai seassa selkeä viite viikkotehtäviin (mallia "Aiheeseen liittyvät viikkotehtävät" tai "Sinulla on nyt tarvittavat tiedot näihin tehtäviin" vrt. OpenCS-matskut) => opiskelija voi tehdä tehtäviä palottain edeten materiaaleissa
   - Viimeisenä alaosana on vielä erillinen sivu, jossa on kooste viikkotehtävistä => opiskelija näkee kaikki tehtävät samassa paikassa ja voi valita, haluaako tehdä kaikki tehtävät "nipussa" tai vähän kevyemmin ripoteltuna itse materiaaleihin
- Bonus: voisiko materiaaleissa olla OpenCS tapainen palautepainike, jolla opiskelijat voi kysyä kysymyksiä tai antaa palautetta

### Luennot

- Kolme vaihtoehtoa:
   1. Pidetään 2 kertaa viikossa => 1. luento edellisen viikon "kyselytunti", jossa katsotaan opiskelijoiden palautteita (ks. yllä oleva bonus) ja teetetään interaktiivisesti kyselyjä aiheesta; 2. luento on tämän viikon asioiden läpikäynti **esimerkein**, ei varsinaisesti "opetusta"
   2. Pidetään 1 kerta viikossa => opiskelijan palautteet ja asioiden läpikäynti esimerkein
   3. Ohj1 malli, eli 2 kertaa viikossa, kumpikin enemmän opetusta eli toimivat materiaalien tavoin

- DZ suosii vaihtoehtoa 2 tai kokeilumielessä vaihtoehto 1 ("jos tekee hyvät matskut, niin onko järkeä käydä samat asiat luennolla")




### Viikot ja sisällöt


#### Viikko 1: Java-kielen perusteet, kohti olio-ohjelmointia

Aiheina:

- Yksinkertainen ohjelma Javalla (`void main` + `IO.println`)
- Muuttujat ja vakiot (perustyypit, `final`, `String`)
- Ohjausrakenteet (ehdot, silmukat, erityisesti huomio `String`:lle `==` vs. `equals`)
- Funktiot (määrittely, kirjoitusasu, palautusarvot, ehkä hieman datan käsittelyä kertauksena)
- Luokat, metodit ja oliot (mikä `class` on tiedon koostamisen näkökulmasta ("luokalla voi luoda tietotyyppejä, joka sisältää muita tietotyyppejä", osaa tehdä luokan mallia `Vektori`), mitä `new`)

Osaamistavoitteet (koko viikko):

- Osaat kirjoittaa Ohjelmointi 1 -kurssin tapaisia ohjelmia Javalla
- Tunnet Java-kielen vastineita yleisimmille I/O-operaatioille (tekstin tulostus, lukeminen konsolilta, *ehkä* lukeminen tiedostosta)
- Ymmärrät, että Javassa `String`-tyyppien vertailu tapahtuu `equals`-metodilla
- Osaa koostaa "samaan aiheeseen" liittyvää dataa samaan luokkaan

Bonus: Pitäisikö kertoa, mitä `record` on sellaisena "väliaskeleena" kohti kunnollista luokkaa.

#### Viikko 2: Olio-ohjelmoinnin perusteet

Aiheina:

- Proseduraalisesta ohjelmoinnista ("data+funktio") olio-ohjelmointiin ("tila+metodi+viestit")
- Luokan rakenne ja suhde olioon (konstruktori, attribuutti, metodi, this-viite, "luokka blueprintina oliolle")
- Kapselointi (julkisuus määreet `public` ja `private`, getterit ja setterit, metodi pääasiallisena tapana olioille "viestiä")

Bonus: Pitäisikö vertailuksi näyttää prototyyppipohjainen OOP (eli JavaScript tai PHP)

#### Viikko 3: Olio-ohjelmoinnin ominaisuuksia

Aiheina:

- Perintä ("Kissa on Eläin", metodin ylikirjoitus, `protected`, luokkahierarkia)
- Abstraktit luokat (abstrakti metodi)
- Rajapinnat ("Kissa osaa Puhua, Kävellä, Hyppiä...", rajapintametodin oletustoteutus, abstrakti luokka vs. rajapinta)
- Polymorfismi (dynaaminen sidonta, rajapinnat ja abstraktit luokat voivat olla muuttujan tai parametrin tyyppeinä)
- Oliot ovat viitetyypit

Osaamistavoitteet:

- Ymmärrät, mitä perintä tarkoittaa
- Ymmärrät, että abstraktista luokasta ei voi luoda luokan ilmentymiä
- Ymmärrät, että luokka voi toteuttaa monta rajapintaa, mutta periä vain yhdestä luokasta
- Osaat luoda yksinkertaisen luokkahierarkian, jossa luokka perii toisen luokan ja ylikirjoittaa sen metodeja
- Ymmärrät, että luodut oliot käsitellään Java-kielessä viitteinä, jolloin olion tilan päivittäminen vaikuttaa kaikkiin paikkoihin, jossa olion viite on tallessa

#### Viikko 4: Olio-ohjelmoinnin sovelluskohteita

Aiheina:

- Perinnän ja rajapintojen käyttökohteita (perintä "laajentamisena", rajapinta "sopimuksen määrittämisenä")
- Tyyppitarkistukset ja tyyppimuunnokset (`instanceof`, casting, `switch` expression/pattern matching)
- Perinnän rajaaminen (`final`)
- Esimerkkejä rajapinnoista ja luokista
    - Javan `Object`-luokka ja sen ylikirjoitettavat `toString` sekä `equals` -metodit
    - Vertailurajapintoja (`Comparable<T>`) -> mahdollistaa Javan järjestämismetodien käytön (`Arrays.sort` jne.)
    - `Cloneable` -> mahdollistaa olion todellisen kopioinnin (vrt. viite) (**TODO:** Pitäisikö viitteet käydä tässä(kin))
    - Bonus: Vertailuluokka (`Comparator<T>`) -> mahdollistaa määrittää useita erilaisia vertailutapoja samalle luokalle
- **Ehkä:** Luokkien testaaminen (Arrange, Act, Assert ainakin ComTestin tasolla)


#### Viikko 5: Tietorakenteita ja algoritmeja

Aiheina:

- Java-kielen kokoelmarajapinnat ja sen tietorakenteet: `List`, `Set`, `Map`
    - Tehdään oma `ArrayList<Integer>`
    - **TODO:** Ehkä viikkotehtäväksi oma `HashMap`? (esim. käyttäen `ArrayList` + [linear probing](https://en.wikipedia.org/wiki/Linear_probing) jotta toteutus olisi vielä semihelppo)
- Templaatit luokille ja metodeille (`<T>`, "geneerinen tyyppi" käsitteenä)
    - Laajenetaan oma `ArrayList<Integer>` yleiseksi `ArrayList<T>`:ksi
- Iteraattorit (`Iterable<T>`, `Collections`-luokka, `for each` -silmukka, Stream API)
- Java-kielen valmiit tietorakenteet `ArrayList`, `HashMap`, `LinkedList` (algoritmeja ja suorituskyky)

Bonus: Pitäisikö kertoa, miten geneerisyys on Javassa toteutettu (type erasure) ja miten se vertautuu vaikkapa C#:iin (todellinen ajonaikainen geneerisyys) ja C++:iin (puhtaat templaatit).

#### Viikko 6: Tietorakenteita ja algoritmeja

Aiheina:

- Stream API lisää (funktionaalinen ohjelmointi ehkä tähän lisää, lambdat)
- Tiedostojen käsittely ja siihen liittyvät rajapinnat: tietovirrat (`Stream`), Files API, REPL (`Scanner`)
    - Tiedostomuotojen käsittely "käsin" (CSV) ja kirjastolla (JSON)
- Poikkeukset ja niiden käsittely (liittyen erityisesti IO:hon)
- Rekursio (toteutus, rekursiivinen tietorakenne, `LinkedList`, pino)
- Enumeraattorit (ehkä?)
- Moniulotteinen data (ehkä?)

Bonus: Tietojen hakeminen verkosta (eli HTTP/2 Client API, kuten `HttpClient`, `HttpResponse`)

#### Viikko 7: Projektin hallinta; GUI-alkeet



Ensimmäinen tutorial-viikko: JavaFX-projektin tekeminen
Viikoilla 7-8 edistetään yhtä JavaFX-sovellusta yhdessä.
Muutama ajatus projektiksi (**me päätämme, mikä otetaan**, kaikki opiskelijat tekevät saman):
   - Kulujen seurantasovellus: voi syöttää menoja ja tuottoja; sovellus laskee, kuinka pitkälle rahaa riittää, tallentaa tiedot JSONiin
      -  Viikko 7: Yksinkertainen dialogin, johon voi syöttää 3 menoa ja 3 tuottoa ja se laskee summan 
      -  Viikko 8: Taulukkonäkymä, jossa näkyy kulut ja menot, tiedot tallennetaan JSONiin
   - Muistikorttien tekosovellus: voi tehdä oppimiskortteja termien oppimiseen (vrt. flashcard-kortti)
      - Viikko 7: Dialogi, joka näyttää "kysymyskortin"; painikkeen painaminen "kääntää" vastauksen näkyviin
      - Viikko 8: Dialogi, jolla voi lisätä useita kysymyskortteja, kortit tallenetaan JSONiin
   - Kaupan varastohallinta
      - Viikko 7: Kirjautumisdialogi
      - Viikko 8: Taulukko, jossa on tuotteita, määriä ja hinta; mahdollisuus lisätä tuotteita, muokata määrää jne
   - Joku pelillistetty, esim. "virtuaalisen hahmon luominen" tai joku "D&D-hahmon luominen"
      - Viikko 7: Dialogi, jolla syötetään hahmon tiedot (nimi, voima, taidot, jne.), mahdollisuus satunnaistaa statseja
      - Viikko 8: Useiden hahmojen hallinta  

Aiheina:

- GUI:n perusteet: JavaFX ja sen rakenne (View, Controller, Model)
- Ohjattu JavaFX-projekti, osa 1:
   - JavaFX lisääminen projektiin ja yksinkertaisen ohjelman käynnistäminen
     - **Huom:** Denis testasi tämän, ja vaatii useampia vaiheita jos tekee käsin:
       1. JavaFX-Maven -plugarin lisääminen pom.xml:ään
       2. JavaFX-riippuvuukisen lisääminen pom.xml:ään
       3. maven-ajokonfiguraation lisääminen IntelliJ:hin
     - Vaihtoehtona voi kokeilla Maven Archetype, joka on vähän kuin dotnet start (eli valmis pohja) -> ainakin <https://mvnrepository.com/artifact/io.github.sosuisen/jfx-sss-vanilla> on tuore
     - On melko helppoa ja nopeaa ladata meidän oma pohja Maveniin
   - SceneBuilderin asennus ja käyttö
   - Kontrollit: painikkeet, labelit, syötteet
   - Asettelut: VBox, HBox, BorderPane
   - Tapahtumankäsittely

Tämän viikon tehtävät ovat tutorialin tiettyjen vaiheiden edistäminen ja palauttaminen.
Bonustehtävänä voi olla jonkin toisen yksinkertaisen JavaFX-projektin tekeminen.

Ajatus: Tässä projektin tekeminen on "vaihe" eikä tehtävä, vaihe on pakko suorittaa.
Lisänä voi olla esimerkiksi yksi tai kaksi perustehtävää, jotka seuraavat 50 % suoritusvaatimusta.
Vaihtoehtoisesti osassa ei ole enää yhtään perustehtäviä, jolloin 50 % * 0 tehtävää = 0 tehtävää on pakko tehdä. Sen sijaan vaiheet ovat pakollisia. Vaiheita voi olla vähän, esim. 1-3.

#### Viikko 8: MVC, Käyttöliittymän testaus

Toinen tutorial-viikko: JavaFX-projektin laajentaminen

Aiheina:

- Dialogeja
- MVC
   - Viimeistään tässä mainitaan terminä ja luodaan yhteys JavaFX:n ja MVC:n välillä
   - datan ja GUI:n liimaaminen yhteen, `Observable`-suunnittelumalli
   - datan lataaminen ja tallentaminen soveltamalla edellisen viikkojen aiheita
- JSON, datan hakeminen ja tallentaminen

Tässä jatketaan tutorialin tekemistä ja lopuksi palautetaan. 

Palautettu projekti ei arvioida, lasketaan vaan tehdyksi.


#### Viikko 9: Koodin laatu, suunnittelumallit

Tässä aloitetaan oman itsenäisen projektin tekemistä.
Voidaan tarjota kaksi vaihtoehtoa: joko tekee täysin oman projektin, jossa pitää olla
datan lataamista ja tallentamista, N kpl dialogeja, testejä TAI valitsee
yhden kolmesta laajentamispolusta, jolla laajentaa tutoriaalin suuremmaksi kokonaisuudeksi.

Tässä jotain ideoita mahdollisille laajentamispoluille riippuen valitusta aiheesta:

- Kulujen seurantasovellus:
  1. Analytiikan ja datan visualisoinnin lisäys ulkoisella kirjastolla (esim. JavaFX Charts), analytiikka päivittyy automaattisesti, kun data muuttuu. Kulujen seuranta, ennustaminen, ennustaminen (tähän sopiva kirjasto) -> kiinnostava erityisesti datatieteen opiskelijoille
  2. Toistuvat kulut (esim. vuokra), kuukausittaisten varojen tallentaminen
  3. Valuutanmuunnokset, haetaan netistä valuuttakurssi (joku API) ja sallitaan tallentaa kuluja eri rahayksikköinä
- Muistikorttisovellus:
  1. Toteuta jokin opiskelualgoritmi, joka automaattisesti valitsee, mitä kortteja pitää harjoitella (vrt. Anki) -> algoritmin tutkiminen verkosta ([spaced repetition algorithm](https://faqs.ankiweb.net/what-spaced-repetition-algorithm)) ja toteuttaminen Javalla
  2. Mahdollisuus upottaa kuvia tai jopa audiota (MediaPlayer/ImageView -komponentit)
  3. Tenttimoodi (monivalintatenttien generointi korteista) -> dynaaminen käyttöliittymän tekeminen
  4. Anki-korttipakkojen importtaus: <https://ankiweb.net/shared/decks> -> ZIP-tiedostojen käsittely, yksinkertainen parsiminen, HTTP
- Varastosovellus:
  1. Kojelauta -> mitkä tuotteet lopussa (alle 5 jäljellä), yleinen analytiikka tuotteista
  2. Tietokanta -> korvaa JSON SQL:llä (esim. SQLite käyttäen JDBC)
  3. Tuki useille käyttäjille -> erilaiset roolit (myyjä, hallinto, jne), tapahtumaloki tilanteen seurantaan
- Hahmon luominen -sovellus
  1. Mahdollisuus lisätä esineitä hahmolle ja niiden lukumäärä
  2. Hahmon ulkoasun editori (StackPane + kuvia): voi luoda oman hahmon


Aiheita:

- UML-suunnittelu
- Git-repon setuppaus, olennaiset tiedostot (README, LICENSE, .gitignore, ehkä .gitattributes)
- Git-versiohallinnan kertausta ja harjoittelua
- Testaaminen (JUnit, olio-ohjelmien testaaminen)

Asioita nyt vähän vähemmän, suurempana tehtävänä oman idean valinta, repon setuppaus ja valmistelu.


#### Viikko 10: Suunnittelumalleja

Jatketaan projektin työstämistä. 
Tässä vaiheessa hieman koodin laadusta:


- SOLID
- Koodihaju, refaktorointi
- laadun kannalta hyödyllisiä tekniikoita
    - Muuttumattomuus ja immutable programming, Javan `record`
    - TDD menetelmänä ja *eräänä* tapana vaikuttaa koodin laatuun
        - Tämä soveltuu tähän oikeastaan aika hyvin, jos puhutaan yleisesti laadusta
   - Vastaavasti pöytätestaus myös näkökulmasta "tutkitaan ohjelman oikeellisuus"
- Suunnittelumalleja
  - ehkä tasolla miksi on olemassa
  - itse mallien tutkinta ja sovellus jää oman kiinnostuksen tasolle (esim. tehtävä)

#### Viikko 11: Extraa

Ei pisteellisiä tehtäviä, mutta lisäaiheita omaan tutkintaan mm.

- Moniajo (säie, virtuaalinen säie)
- Suorituskyvyn optimointi
- Hyödyllisiä kirjastoja
  - GraphFx, ControlsFx 


#### Viikko 12: Projektin hallinta

Keskitytään projektin tekemiseen ja viimeistelyyn.

Ajatus: projekti voitaisiin palauttaa tämän viikon puolivälissä (tai jopa viikolla 11)
ja sen jälkeen pitää vertaisarvioida kahden muun henkilön projekteja. 
Vertaisarvioijalla on checklist-tyyppinen lista, jonka avulla antaa arvionsa?
Tuntiopettajalle jää tarkastaa vertaisarviot ja jos kovin eri niin tarkistaa?

Vaihtoehtoisesti viikko 12 varattu työn dokumentoinnille ja näyttämiselle TA:lle,
ei vertaisarviointia.

<details closed>
<summary>
<h2>Curriculum v1</h2>
</summary>


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

</details>