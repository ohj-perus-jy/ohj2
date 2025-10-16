# Ohj2

## OPS-vaatimukset

- Oliopohjaisen ohjelmoinnin perusteet
- Testaaminen, erityisesti TDD
- Graafisen käyttöliittymän suunnittelu
- Java
- Ohjelman suunnittelu
- Rekursio

## Yleistä

- Kesto: 8 + 4 viikkoa
  - 5 op + 3op
    - Alku lähelle uuden 5+5+5 mallin kakkososiota ja 3op viimeistä?
- Vahvasti ohjattu harjoitustyö ja oma arvoitava harjoitustyö

### Arviointi

- Viikkotehtävät (40%) + harjoitustyö ja vertaisarvioinnit (hyväksytty/hylätty) + tentti (60%)
   - Kaksi projektia
   - Viikkotehtävät eivät ole pakollisia
   - Ei deadlineja versus deadlinet ja laskeva pistemäärä?
   - Ei minimi-viikkotehtäväpisteitä, aina voi tenttiä
   - 2-3 muun palautuksen vertaisarviointi valmiilla tarkistuslistalla (vrt. Hiven projekti / [Ohjelmistotestauskurssi](https://opencs.it.jyu.fi/software-testing/8-old-projects/2-practical-project-2025s/#self--and-peer-assessment))

- Ei arvosanaan vaikuttavia ekstratehtäviä — ekstratehtävistä lisänoppia? (vrt. HY:n ohjelmointihaasteita)

- Jos osoittaa opetettavien asioiden osaamista omalla projektilla tai työkokemuksella niin ei tarvitse tehdä harjoitustyötä erikseen
- Työkokemuksella täydet viikkotehtäväpisteet + tentti?

### Harjoitustyö(t)

- Ensimmäinen ja vahvasti ohjattu / määritetty (vk 8-10): Esim. ohjelma, joka hakee verkosta mm. numeerista dataa ja visualisoi graafisella käyttöliittymällä erilaisten kuvaajien avulla. Interaktiivisuutta napeilla esim. suodatus, eri kuvaajat yms.
- Toinen ja vapaampi harjoitustyö (vk 10-12)

Tulevaisuuden 5+5+5 mallissa voisi ensimmäinnen harjoitustyö alkaa aikaisemmin. Toisessa voisi olla lisänoppien myötä enemmän aikaa harjoitustyölle ja esim. suunnittelumalleille.

### Opetustilaisuudet

Yksi tai kaksi flipped-/vastaanottotilaisuus/luento viikossa. 
- Vastaanottoaikana väh. yksi vastuuopettaja aina fyysisesti tavoitettavissa
- Luennolla käytäisi viikon olennaisimmat asiat läpi tiivistetysti (sekä edellisen viikon mahdollisia vaikeuksia / opiskelijoiden nostamia ongelmia). 

## Viikot ja sisällöt

Materiaali jaettu viikoittain. Tehtävät voisi olla lomitettuna sisällön kanssa (iframe tms) sekä erikseen omalla sivullaan (viikoille omat tehtäväsivut vai kaikki könttänä?). Tehtävää ennen aina esitetään opeteltava asia havainnollistavin esimerkein. 

Tarinamainen rakenne kokonaisuudelle olisi hieno (vrt. A-J:n ehdotus). Jokin jatkuva tehtävä/esimerkki, joka rakentuu viikkojen yli heti alusta alkaen voisi sitoa eri osiot yhteen. Tässäkin on omat haasteensa.

### 1. Java-kielen perusteet

#### Osaamistavoitteet

- Tiedät miten Java-ohjelma käännetään ja ajetaan (komentoriviohjelmat `javac`, `java` ja `jshell`, IDE-säädöt)
- Tiedät mikä on JVM
- Osaat tehdä ohjelmointi 1 -kurssin tasoisia ohjelmia Javalla
  - Tulostaminen ja syötteen lukeminen
  - Aliohjelmat
  - Toistolauseet, ja listatyyppiset tietorakenteet
  - Dokumentaatiokommentit

#### Tehtäviä

- Tulostamisesta kohti (b)rainfall-tasoista tehtävää

### 2. Olio-ohjelmoinnin perusteet

#### Osaamistavoitteet

- Ymmärrät luokkien ja olioiden roolin olio-ohjelmoinnissa
  - Tieto ja toiminnallisuus yhdessä paketissa
- Osaat määritellä ja hyödyntää omia luokkia Javalla
- Ymmärrät kapseloinnin ja sen hyödyt 
  - Decoupling/Coupling
  - näkyvyysmääreet: `public`, `private`, `protected`
- Ymmärrät Javan perustietotyyppien ja viitetyyppien eron (oliot ovat aina viitteen takana)

### 3. Abstrahointi ja polymorfismi 

(vähemmän latinaa otsikossa parempi?)

#### Osaamistavoitteet

- Ymmärrät mitä on polymorfismi
- Ymmärrät miten luokat ja oliot voivat periä toistensa ominaisuuksia
- Ymmärrät miten metodeja voi ylikirjoittaa luokan sisällä ja luokkien yli
- Osaat hyödyntää rajapintoja ja abstrakteja luokkia luokkienvälisen riippuvuuden välttämiseksi
  - "Composition over inheritance"



### 4. Hyödyllisiä menetelmiä

#### Osaamistavoitteet

- Osaat hyödyntää geneerisiä tyyppejä ja tyyppiparametreja toteuttaaksesi yleiskäyttöisiä luokkia ja metodeja
- Tyyppitarkistukset ja tyyppimuunnokset (`instanceof`, casting)
- `switch`-lauseke, pattern matching
- Tiedät mitä ovat enumeraattorit ja milloin niitä kannattaa käyttää
- Esimerkkejä Javan valmiista rajapinnoista ja luokista (Deniksen ehdotus, hieman eri paikassa)
    - Javan `Object`-luokka ja sen ylikirjoitettavat `toString` sekä `equals` -metodit
    - Vertailurajapintoja (`Comparable<T>`) -> mahdollistaa Javan järjestämismetodien käytön (`Arrays.sort` jne.)
    - `Cloneable` -> mahdollistaa olion todellisen kopioinnin (vrt. viite) (**TODO:** Pitäisikö viitteet käydä tässä(kin))
    - Bonus: Vertailuluokka (`Comparator<T>`) -> mahdollistaa määrittää useita erilaisia vertailutapoja samalle luokalle

### 5: Tietorakenteita ja algoritmeja

#### Osaamistavoitteet:

- Tunnet Java-kielen kokoelmarajapinnat ja niitä toteuttavia tietorakenteita: `List`, `Set`, `Map`
- Templaatit luokille ja metodeille (`<T>`, "geneerinen tyyppi" käsitteenä)
    - Laajenetaan oma `ArrayList<Integer>` yleiseksi `ArrayList<T>`:ksi
- Tunnet Java-kielen yleisimmät valmiit tietorakenteet `ArrayList`, `HashMap`, `LinkedList`, `Stack`, `Queue`
- Ymmärrät ym. tietorakenteiden keskeisimmät operaatiot ja niiden aikakompleksisuudet
- Ymmärrät miten rekursio toimii ja osaat mallintaa rekursiota pinon avulla

(Moniulotteinen data tänne? Konseptuaalisesti sopisi, mutta tässä lienee jo tosin aika paljon asiaa) 

#### Tehtäviä

- Tehdään oma `ArrayList<T>` taulukoilla (monimutkaisempi HashMap esimerkkinä?)
- Rekursiotehtäviä
- Monivalintoja tietorakenteiden operaatioista ja niiden aikakompleksisuuksista 

### 6. Hyödyllisiä menetelmiä 2

#### Osaamistavoitteet

- Tunnet eri tapoja hallita poikkeuksia
  - null ja `Optional`
  - `throw` ja `throws`
  - try-catch-finally
- Build-työkalut (Gradle/Maven) ja Kolmannen osapuolen riippuvuuksia
- Osaat käsitellä tiedostoja Javan valmiiden rajapintojen kautta
    - Tiedostomuotojen käsittely "käsin" (CSV) ja kirjastolla (JSON)
- Osaat hakea verkosta dataa Javalla (ekstra?)

### 7. Ohjelmointisuuntauksia eli -paradigmoja

#### Osaamistavoitteet

- Tunnet yleisiä ohjelmointisuuntauksia ja tiedät miten niitä on mahdollista toteuttaa Javalla
- Ymmärrät, että on monia hyviä ja perustavanlaatuisesti erilaisia tapoja toteuttaa mielivaltaisia tietokoneohjelmia 
- Tiedät mitä on imperatiivinen ja funktionaalinen/ohjelmointi (paradigmat konseptina voi olla hyvä ekstra-infoinakin tms mainittuna eikä osaamistavoitteina)
  - Imperatiivinen: lauseet muokkaavat ohjelman tilaa
  - Puhtaan funktion määritelmä
  - Streamit ja lambdat
- Tiedät mitä on proseduraalinen ohjelmointi ja miten se eroaa olio-ohjelmoinnista
  - Ohjelma koostuu proseduureista (aliohjelma), viesteistä (aliohjelmat kutsuvat toisiaan) ja erillisistä tietorakenteista (Javassa `record`). (Kannattaako tässä vielä ottaa mukaan moduulit?)
  - Tieto ja toiminnallisuus omissa paketeissaan (olioissa)
  - metodi vs aliohjelma

#### Tehtäviä

- Samantyylisiä tehtäviä eri paradigmojen avulla
- Monivalintoja teoriasta


### 8. Projektin hallinta

- Versiohallinta gitissä (yhdelle henkilölle)
- Luokkakaaviot, UML
- Johdatus suunnittelumalleihin
- Automaattinen testaus JUnitilla
- Koodin laatu, koodihajut ja koodin refaktorointi

#### Tehtäviä

- Monivalintoja luokkakaavioista ja UML:stä sekä koodin laadusta
- Käytännön asiat: Yksinkertainen GUI-ohjelma esiharjoitustehtävänä vahvasti ohjattuna, esim. äänestys (osa 1 — ei GUI:ta vielä) 

### 9. Graafinen käyttöliittymä 1

- JavaFX:n perusteet
- Komponentit ja layoutit
- Tapahtumankäsittely
- MVC-malli

#### Tehtäviä

- Yksinkertainen GUI-ohjelma esiharjoitustehtävä vahvasti ohjattuna (osa 2)

### 10. Graafinen käyttöliittymä 2

- Dialogeja
- MVC lisää (datan ja GUI:n liimaaminen yhteen, `Observable` pattern ja API JavaFX:ssä)

#### Tehtäviä

- Yksinkertainen GUI-ohjelma esiharjoitustehtävä viimeinen osa (osa 3)
- Oman projektin suunnittelu ja aloittaminen

### 11. Extroja 1

Ei pisteellisiä tehtäviä, työstetään omaa projektia

- Biteistä merkitystä
- Luvut ja teksti bitteinä
- Suorituskyvyn optimointi
- Monisäikeisyys

### 12. Extroja 2 

Ei pisteellisiä tehtäviä, työstetään omaa projektia

- SOLID-periaatteista yms suunnittelumalleista tarkemmin
- Rajapinta natiiviin koodiin (JNI)
- Erilaisia ohjelmointikieliä
- Ohjelmistokehitys eri alustoille

### 13. Tentti



