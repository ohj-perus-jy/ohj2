# Ulkoiset kirjastot ja Java-projektien hallintatyökalut

> [!VAROITUS]
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Build-työkalut (Gradle/Maven)
> - Kolmannen osapuolen riippuvuuksia (miten etsitään ja lisätään kirjasto)
> - Pakkaukset Javassa? (Vai jo luvussa 2?)

## Build-työkalut

Kun ohjelmistoa kehitetään, koodin kirjoittaminen on vasta ensimmäinen askel.
Koodi täytyy myös kääntää, siihen täytyy liittää muiden tekemiä apukirjastoja,
linkittää mahdollisesti muita tiedostoja, ja lopulta se on pakattava muotoon,
jota voidaan ajaa tietokoneella tai palvelimella.

Tätä prosessia hoitavat **rakennustyökalut** (engl. *build tools*), kuten Apache
Maven ja Gradle. Mutta mitä ne oikeastaan tekevät?

## Analogia: Huonekalusuunnittelija

Ajattele rooliasi ohjelmoijana ikään kuin IKEAn huonekalusuunnittelijana. Et
itse rakenna jokaista huonekalua asiakkaalle, vaan luot tarkan
rakennesuunnitelman, kokoamisohjeet (koodin) ja laadit *osaluettelon* siitä,
mitä huonekalun kokoamiseen tarvitaan. Henkilöä, joka lopulta ostaa huonekalun
ja alkaa koota sitä, voidaan puolestaan verrata Java-virtuaalikoneeseen tai
muuhun ajoympäristöön: hän avaa myyntipakkauksen, lukee ohjeesi, suorittaa
vaiheet järjestyksessä ja herättää huonekalun henkiin.

Mutta miten suunnittelijan työpöydällä olevista piirustuksista ja ohjeista tulee
asiakkaan ostama valmis myyntipakkaus? Et voi vain postittaa pelkkiä ohjeita
asiakkaalle ja toivoa, että hän käy itse etsimässä rautakaupasta juuri
oikeanlaiset lastulevyt, mutterit, pultit ja saranat.

Suunnittelijana toimitat ohjeesi ja osaluettelosi tehtaalle ja pakkaamoon.
Siellä kerätään automaattisesti yhteen kaikki vaaditut osat ja pakataan ne
yhdessä ohjeidesi kanssa siistiin, litteään pahvilaatikkoon, jotta paketti
voidaan helposti kuljettaa ja myydä eteenpäin.

Tässä astuvat kuvaan **rakennustyökalut**.

Rakennustyökalut, kuten **Maven**, **Gradle** ja vanhempi **Apache Ant**,
toimivat ohjelmistoprojektisi automaattisena tehtaana ja pakkaamona. Niiden
päätehtävät jaetaan kolmeen kategoriaan:

**1. Riippuvuuksien hallinta (Mutterien ja pulttien tilaaminen)**

Ohjelmoijana et kirjoita kaikkea alusta asti itse (esimerkiksi
tietokantayhteyksiä tai salasanan salausta), vaan käytät muiden tekemiä
"valmiita osia", eli koodikirjastoja. Näitä kutsutaan *riippuvuuksiksi*
(dependencies). Rakennustyökalu lukee kirjoittamasi osaluettelon (esim.
`pom.xml` tai `build.gradle`), etsii tarvittavat standardikirjastot
automaattisesti internetin varastoista ja lataa ne projektiisi.

**2. Kääntäminen ja testaaminen (Laadunvalvonta)**

Ennen kuin paketti laitetaan kiinni, työkalu varmistaa, että kaikki toimii. Se
kääntää ihmiskielisen koodisi koneen ymmärtämään muotoon ja ajaa mahdolliset
automaattiset testit. Se siis tarkistaa laadunvalvontalinjastolla, ettei
laatikosta puutu tärkeitä osia, osat sopivat toisiinsa ja että ohjeissa on
järkeä.

**3. Pakkaaminen ja jakelu (Litteä pahvilaatikko)**

Kun kaikki osat on kerätty ja ohjeet todettu toimiviksi, rakennustyökalu pakkaa
koko komeuden yhdeksi helposti käsiteltäväksi tiedostoksi, kuten **JAR-** tai
**WAR-tiedostoksi** (Java Archive).

Lopuksi rakennustyökalu voi auttaa paketin julkaisemisessa (deployment) eli sen
toimittamisessa sinne, missä ohjelmaa tullaan lopulta käyttämään. Tämä voi
tarkoittaa esimerkiksi pilvipalvelinta, kuten AWS tai Azure, sovelluskauppaa,
kuten Google Play tai Apple App store, taikka yrityksen sisäistä palvelinta.
IKEA-vertauksessa tämä on se vaihe, kun tehdas laittaa valmiit litteät laatikot
rekkaan ja ne kuljetetaan paikallisen tavaratalon noutovaraston hyllylle
asiakkaiden haettavaksi.

## Riippuvuuksien hallinta

Gradle ja Maven tarjoavat tehokkaat mekanismit riippuvuuksien hallintaan. Ne
automaattisesti hakevat ja lataavat tarvittavat kirjastot, mikä säästää
kehittäjältä aikaa ja vaivaa. Riippuvuuksien hallinta on keskeinen osa modernia
Java-kehitystä, ja se auttaa varmistamaan, että projekti käyttää oikeita
versioita kirjastoista ja että kaikki tarvittavat osat ovat saatavilla.

## Kääntäminen ja testaaminen

Build-työkalut hoitavat myös käännösprosessin...

## Pakkaaminen ja jakelu

Build-työkalut voivat pakata käännetyn koodin ja kaikki tarvittavat riippuvuudet
yhdeksi tiedostoksi, kuten JAR- tai WAR-tiedostoksi...

## Kolmannen osapuolen riippuvuudet

Java-projekteissa on usein tarpeen käyttää kolmannen osapuolen kirjastoja, jotka
tarjoavat valmiita toiminnallisuuksia ja säästävät kehitysaikaa...


## Pakkaukset Javassa

