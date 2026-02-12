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
automaattisesti internetin varastoista ja lataa ne projektiisi. Riippuvuuksien
hallinta on keskeinen osa modernia Java-kehitystä, ja se auttaa varmistamaan,
että projekti käyttää oikeita versioita kirjastoista ja että kaikki tarvittavat
osat ovat saatavilla.


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

## Ensimmäinen Java-projekti Gradlella

Kokeillaan tehdä itse ensimmäinen Java-projekti Gradlella. 

 1. Aloita luomalla uusi projekti. 
 2. Anna projektin nimeksi "EkaGradleProjekti". 
 3. Valitse IDEAssa Build System -kohdassa Gradle. 
 4. Valitse DSL-kohdassa Kotlin -- tämä valinta liittyy siihen, millä
syntaksilla build-tiedosto kirjoitetaan, ei siihen, millä kielellä oma koodisi
kirjoitetaan. 
5. Klikkaa sitten Create.

Hetken mietittimisen jälkeen sinulle pitäisi syntyä projekti, jossa on melkoinen
läjä tiedostoja ja kansioita. Katsotaan näitä nyt lähemmin.

```bob

.gradle
 |
 '-..
.idea
 |
 '-..
gradle
 |
 '-..
src
 |
 +-main
 +-java
 |  |
 |  '- org.example
 |      |
 |      '-Main.java
 +- test
 |  |
 |  '-..
 +-.gitignore
build.gradle.kts
gradlew
gradlew.bat
settings.gradle.kts
```

Tässä vaiheessa tärkeimmät näistä ovat `build.gradle.kts` ja
`settings.gradle.kts`. Näissä määritellään, miten projekti rakennetaan, mitä
riippuvuuksia se tarvitsee, ja muita tärkeitä asetuksia. `src`-kansio puolestaan
sisältää varsinaisen Java-koodin. `gradle`-kansio sisältää Gradlen omat
tiedostot, joita ei tarvitse muuttaa. `gradlew` ja `gradlew.bat` ovat Gradle
Wrapper -tiedostoja, jotka mahdollistavat Gradlen käytön ilman, että käyttäjällä
tarvitsee olla Gradlea asennettuna. Käytännössä nämä tiedostot lataavat ja
asentavat oikean Gradle-version automaattisesti, kun projekti avataan.

Katsotaan aluksi `settings.gradle.kts`-tiedostoa. Siinä on nyt määritelty
projektin nimi:

```kotlin
rootProject.name = "EkaGradleProjekti"
```

Tässä tiedostossa voit määritellä myös moniprojektirakenteen, jos haluat jakaa
projektisi useampaan osaan. Mutta nyt keskitytään vain tähän yksinkertaiseen
projektiin.

Avaa sitten `build.gradle.kts`-tiedosto. 

 * `plugin`-osiossa on määritetty,
että käytetään Java-kieltä. 
 * `group`- ja `version`-osioissa on määritetty
projektin "ryhmä", eli organisaatio, joka projektia kehittää, sekä projektin versio. 
 * `repositories`-osiossa on määritetty, että riippuvuudet haetaan Maven Central
-varastosta. 
 * `dependencies`-osiossa on määritetty, että projekti tarvitsee JUnit-kirjaston
-testaukseen. Tässä vaiheessa ei ole vielä muita riippuvuuksia, mutta tähän
kohtaan lisätään myöhemmin kaikki ne kirjastot, joita projektisi tarvitsee. Kun
aikanaan käytämme JavaFX:ää, tähän kohtaan ilmestyvät JavaFX:n riippuvuudet.
 * `tasks.test`-osiossa on määritetty, että testit ajetaan JUnit Platformilla, joka
on JUnit 5:n testialusta.

Avaa nyt `Main.java`-tiedostoa. Lisätään sinne seuraava koodi, joka tekee
HTTP-kutsun GitHubin julkiseen API-osoitteeseen ja tulostaa vastauksen. Tämä
esimerkki käyttää OkHttp-kirjastoa, joka on suosittu HTTP-asiakas Javaan.

```java
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class Main {

    public static void main(String[] args) {

        // Luodaan HTTP-asiakas. Tämä olio vastaa yhteyksien hallinnasta.
        OkHttpClient client = new OkHttpClient();

        // Rakennetaan HTTP GET -pyyntö GitHubin julkiseen API-osoitteeseen.
        // User-Agent -otsake lisätään, koska GitHub API vaatii sen.
        Request request = new Request.Builder()
                .url("https://api.github.com/zen")
                .header("User-Agent", "Gradle-Demo")
                .build();

        // Vastaus-olio alustetaan nulliksi, jotta se voidaan sulkea finally-lohkossa.
        Response response = null;

        try {
            // Lähetetään HTTP-pyyntö palvelimelle (synkroninen kutsu).
            response = client.newCall(request).execute();

            // Tulostetaan HTTP-statuskoodi (esim. 200 = OK).
            IO.println("HTTP status: " + response.code());

            // Tulostetaan vastauksen runko 
            IO.println("Response body:");
            IO.println(response.body().string());

        } catch (Exception e) {
            // Jos verkko- tai muu virhe tapahtuu, tulostetaan virheilmoitus.
            IO.println("Virhe HTTP-kutsussa: " + e.getMessage());

        } finally {
            // Varmistetaan, että vastaus suljetaan.
            // Tämä vapauttaa resurssit (esim. yhteyden).
            if (response != null) {
                response.close();
            }
        }
    }
}
```

Projekti ei kuitenkaan käänny vielä, koska OkHttp-kirjasto ei ole vielä
projektin riippuvuuksissa. Lisätään siis `build.gradle.kts`-tiedostoon OkHttp:n
riippuvuus.

```kotlin
dependencies {
    [...]
    implementation("com.squareup.okhttp3:okhttp:4.10.0")
}
```

Tallenna tiedosto ja käännä projekti uudestaan. Nyt Gradle hakee
OkHttp-kirjaston Maven Central -varastosta, lataa sen ja liittää sen
projektiisi. Tämän jälkeen käännös onnistuu, ja voit ajaa `Main`-luokan
`main`-metodia, jolloin näet HTTP-kutsun tulokset konsolissa.

> [!HUOMAUTUS]
> Jotta IDE tunnistaa riippuvuudet, saatat joutua lataamaan projektin tiedostot
> uudelleen sync- tai reload-toiminnolla. Käynnistä tarvittaessa IDE
> uudestaan, jos ongelmia ilmenee.

## Kääntäminen ja testaaminen

Build-työkalut hoitavat myös käännösprosessin...

## Pakkaaminen ja jakelu

Build-työkalut voivat pakata käännetyn koodin ja kaikki tarvittavat riippuvuudet
yhdeksi tiedostoksi, kuten JAR- tai WAR-tiedostoksi...

## Kolmannen osapuolen riippuvuudet

Java-projekteissa on usein tarpeen käyttää kolmannen osapuolen kirjastoja, jotka
tarjoavat valmiita toiminnallisuuksia ja säästävät kehitysaikaa...


## Pakkaukset Javassa

