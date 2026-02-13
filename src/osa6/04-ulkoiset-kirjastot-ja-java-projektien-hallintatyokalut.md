# Ulkoiset kirjastot ja Java-projektien hallintatyökalut

> [!VAROITUS]
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Build-työkalut (Gradle/Maven)
> - Kolmannen osapuolen riippuvuuksia (miten etsitään ja lisätään kirjasto)
> - Pakkaukset Javassa? (Vai jo luvussa 2?)

Oletetaan, että haluat tehdä Java-ohjelman, joka hakee tietoa verkosta
HTTP-kutsulla. Kirjoitat seuraavan koodin:

```java
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class Main {
    public static void main(String[] args) throws Exception {
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder()
                .url("https://api.github.com/zen")
                .header("User-Agent", "Demo")
                .build();

        Response response = client.newCall(request).execute();
        System.out.println(response.body().string());
        response.close();
    }
}
```

Yrität kääntää ohjelman, mutta saat virheilmoituksen, että `okhttp3`-pakettia ei
löydy. Kysymys kuuluu: mistä tämä kirjasto pitäisi saada? Jos löydätkin sen
jostain, ja lataat sen `.jar`-tiedostona, niin mihin tuo tiedosto pitäisi
laittaa? Entä jos kirjasto tarvitsee itse tuekseen muita kirjastoja?

Tässä kohtaa törmätään modernin ohjelmistokehityksen ytimeen: oma koodi ei
riitä. Tarvitsemme muiden kirjoittamia kirjastoja. Kun käytät toisen kehittäjän
tekemää kirjastoa, projektisi *riippuu* siitä; Tätä kutsutaan riippuvuudeksi
(dependency). HTTP-esimerkissä riippuvuus on OkHttp-kirjasto. 

Riippuvuuksien hallinta tarkoittaa:

 * kirjaston oikean version hakemista
 * sen lisäämistä projektin *classpathiin*
 * kirjaston omien riippuvuuksien huomioimista
 * versioristiriitojen estämistä

Kirjastojen hallinta käsin on kovin työlästä, ja siksi on kehitetty työkaluja,
jotka hoitavat tämän puolestasi. Näitä työkaluja kutsutaan build-työkaluiksi, ja
niistä tunnetuimpia Java-maailmassa ovat **Maven** ja **Gradle**. Build-työkalu
automatisoi koko prosessin: se hakee tarvittavat kirjastot, huolehtii niiden
versioista ja kääntää koodisi. Build-työkalu voi tehdä muutakin: se ajaa
mahdolliset testit ja pakkaa lopulta valmiin ohjelman jakelukuntoon.

<details><summary>Analogia: Huonekalusuunnittelija</summary>

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

</details>

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

src
 ├─ main --> java
 └─ test --> java
build.gradle.kts
settings.gradle.kts
gradlew
```

Tässä vaiheessa tärkeimmät näistä ovat 

 * `settings.gradle.kts`: määrittelee esimerkiksi projektin nimen,
 * `build.gradle.kts`: määrittelee, miten projekti rakennetaan, mitä riippuvuuksia se tarvitsee, ja muita tärkeitä asetuksia.
 * `src`-kansio: sisältää varsinaisen Java-koodin.
 * `gradlew` ja `gradlew.bat`: Ns. *wrapper*-tiedostoja, jotka mahdollistavat
   Gradlen käytön ilman, että käyttäjällä tarvitsee olla Gradlea asennettuna.

Katsotaan aluksi `settings.gradle.kts`-tiedostoa. Siinä on nyt määritelty
projektin nimi:

```kotlin
rootProject.name = "EkaGradleProjekti"
```

Tässä tiedostossa voidaan määritellä myös niin sanottu moniprojektirakenteen,
jos haluat jakaa projektisi useampaan osaan. Keskitytään kuitenkin tällä kertaa
yksinkertaiseen projektiin.

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

Avaa nyt `Main.java`-tiedostoa. Lisää sinne sivun alussa esitetty HTTP-kutsun
esimerkkikoodi ja yritä kääntää se. Projekti ei kuitenkaan käänny vielä, koska
OkHttp-kirjasto ei ole vielä projektin riippuvuuksissa. Lisätään siis
`build.gradle.kts`-tiedostoon OkHttp:n riippuvuus.

```kotlin
dependencies {
    [...]
    implementation("com.squareup.okhttp3:okhttp:4.10.0")
}
```

Lisää myös aivan koodin alkuun `package org.example;`, jotta koodi on oikeassa
paketissa. Palaamme tämän tarkempaan merkitykseen hieman alempana. 

Tallenna tiedosto ja käännä projekti uudestaan. Nyt Gradle hakee
OkHttp-kirjaston Maven Central -varastosta, lataa sen ja liittää sen
projektiisi. Tämän jälkeen käännös onnistuu, ja voit ajaa `Main`-luokan
`main`-metodia, jolloin näet HTTP-kutsun tulokset konsolissa.

> [!HUOMAUTUS]
> Jotta IDE tunnistaa riippuvuudet, saatat joutua lataamaan projektin tiedostot
> uudelleen sync- tai reload-toiminnolla. Käynnistä tarvittaessa IDE
> uudestaan, jos ongelmia ilmenee.

TODO: Mitä käännöksessä tapahtuu...

TODO: Gradle-wrapperin käyttäminen

```bash
./gradlew compileJava
./gradlew test
./gradlew build
./gradlew clean
```

TODO: Miksi käyttäisin gradle-wrapperia

## Pakkaaminen ja jakelu

Build-työkalut voivat pakata käännetyn koodin ja kaikki tarvittavat riippuvuudet
yhdeksi tiedostoksi, kuten JAR- tai WAR-tiedostoksi...

## Kolmannen osapuolen riippuvuudet

Java-projekteissa on usein tarpeen käyttää kolmannen osapuolen kirjastoja, jotka
tarjoavat valmiita toiminnallisuuksia ja säästävät kehitysaikaa...


## Pakkaukset Javassa


## Tehtävät

Tee Maven-projekti. Lisää siihen riippuvuudet okHttp-kirjastoon sekä
Jackson-kirjastoon. 
