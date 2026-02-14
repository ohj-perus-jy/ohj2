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
jotka hoitavat tämän puolestasi. Näitä työkaluja kutsutaan *build-työkaluiksi*.
Niistä tunnetuimpia Java-maailmassa ovat **Maven** ja **Gradle**. Build-työkalu
automatisoi koko prosessin: se hakee tarvittavat kirjastot, huolehtii niiden
versioista ja kääntää koodisi. Build-työkalu voi tehdä muutakin: se ajaa
mahdolliset testit ja pakkaa lopulta valmiin ohjelman jakelukuntoon.

Esittelemme seuraavaksi Maven-työkalun käyttöä IDEAssa. Aivan hyvin saman asian
voisi tehdä myös Gradlella tai Antilla. Maven on alkuvaiheessa ehkä hieman
helppokäyttöisempi, joten valitsemme sen tähän esimerkkiin.

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

## Ensimmäinen Java-projekti Mavenilla

Kokeillaan tehdä itse ensimmäinen Java-projekti Mavenilla. 

 1. Aloita luomalla uusi projekti. 
 2. Anna projektin nimeksi "EkaMavenProjekti". 
 3. Valitse IDEAssa Build System -kohdassa Maven. 
 4. Klikkaa sitten Create.

Jos jostain syystä Mavenia ei ole valittavissa, asenna se IDEAn pluginien
hallinnan kautta: File <i class="bi bi-chevron-right"></i> Settings <i class="bi
bi-chevron-right"></i> Plugins <i class="bi bi-chevron-right"></i>Marketplace <i
class="bi bi-chevron-right"></i> Etsi "Maven" <i class="bi
bi-chevron-right"></i> Install <i class="bi bi-chevron-right"></i> Käynnistä
IDEA uudestaan.

Pienen miettimisen jälkeen sinulle pitäisi syntyä projekti, jossa on läjä
tiedostoja ja kansioita. Katsotaan näitä nyt lähemmin. Projektisi
kansiorakenne näyttää suunnilleen tältä:

```bob
src
 ├─ main --> java
 └─ test --> java
pom.xml
```

 * `src`-kansio: sisältää varsinaisen Java-koodin (`main/.../java`) ja testikoodin
   (`test/java`).
 * `pom.xml`-tiedosto: Mavenin konfiguraatiotiedosto, jossa määritellään
   projektin riippuvuudet, rakennusasetukset ja muut tärkeät tiedot.
 * Lisäksi projektiin syntyy automaattisesti `.gitignore`-tiedosto, sekä
   `.mvn`-kansio, johon tutustumme myöhemmin. 

Vilkaistaan `pom.xml`-tiedostoa, joka on Maven-projektin sydän. Avatessasi
tiedston, näet XML-muotoista tekstiä. Tämä tiedosto määrittelee projektisi
rakenteen, riippuvuudet ja muut asetukset. "Vanilla"-Java-projektin (ts.
projekti, joka ei käytä ulkoisia kirjastoja) `pom.xml`-tiedosto näyttää suunnilleen tältä:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>EkaMaven</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>25</maven.compiler.source>
        <maven.compiler.target>25</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

</project>
```

Tiedoston alussa määritellään tyypillistä XML-rakennetta, jonka jälkeen tulee
`<groupId>`, `<artifactId>` ja `<version>`-elementit. Nämä ovat ikään kuin
projektisi tunniste, joka yksilöi juuri sinun projektisi muiden Maven-projektien
joukossa. Tässä vaiheessa näillä tunnisteilla ei ole hirveästi merkitystä, mutta
jos julkaiset projektisi esimerkiksi Maven Central -varastoon, nämä tunnisteet
ovat tärkeitä. 

Loput rivit määrittelevät projektin Java-version sekä koodin merkistökoodauksen. 

Avaa nyt `Main.java`-tiedostoa. Lisää sinne sivun alussa esitetty HTTP-kutsun
esimerkkikoodi ja yritä kääntää se. Projekti ei kuitenkaan käänny vielä, koska
OkHttp-kirjasto ei ole vielä projektin riippuvuuksissa. Riippuvuuksien
lisääminen Maven-projektiin tapahtuu muokkaamalla `pom.xml`-tiedostoa. Etsi
tiedostosta `<dependencies>`-elementti. Lisää se (ja sen vastinpari
`</dependencies>`), mikäli kyseistä elementtiä ei vielä ole. 

```xml
<dependencies>
    <!-- Source: https://mvnrepository.com/artifact/com.squareup.okhttp3/okhttp -->
    <dependency>
        <groupId>com.squareup.okhttp3</groupId>
        <artifactId>okhttp</artifactId>
        <version>4.12.0</version>
        <scope>compile</scope>
    </dependency>
</dependencies>
```
IDEA valittaa vielä, että okhttp-pakettia ei löydy. Riippuvuuksien lisäämisen
jälkeen Maven-projekti täytyy virkistää klikkaamalla projektinäkymässä projektin
nimen päältä hiiren oikealla, valitsemalla Maven ja Sync project. Tämän jälkeen
IDEA lataa tarvittavat okhttp-riippuvuuden, ja myös kyseisen kirjaston
itsensä vaatimat muut riippuvuudet. 

Lisää myös aivan koodin alkuun `package org.example;`, jotta koodi on oikeassa
paketissa. Palaamme tämän tarkempaan merkitykseen hieman alempana. 

Tallenna tiedosto ja käännä projekti uudestaan. Nyt Maven hakee
OkHttp-kirjaston Maven Central -varastosta, lataa sen ja liittää sen
projektiisi. Tämän jälkeen käännös onnistuu, ja voit ajaa `Main`-luokan
`main`-metodia, jolloin näet HTTP-kutsun tulokset konsolissa.

## Maven Central

Riippuvuuksien

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
