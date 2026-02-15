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
HTTP-kutsulla. Löydät netistä seuraavan esimerkkikoodin. 

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
        IO.println(response.body().string());
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
(dependency). Äskeisessä esimerkissä riippuvuus on OkHttp-kirjasto. 

Riippuvuuksien hallinta tarkoittaa:

 * kirjaston oikean version hakemista,
 * sen lisäämistä projektin *classpathiin*,
 * kirjaston omien riippuvuuksien huomioimista, ja
 * versioristiriitojen estämistä.

Kirjastojen hallinta käsin on kovin työlästä, ja siksi on kehitetty työkaluja,
jotka hoitavat tämän puolestasi. Näitä työkaluja kutsutaan *build-työkaluiksi*.
Vapaa suomennos voisi olla *rakennustyökalu*, mutta käytämme tässä yhteydessä
vakiintunutta englanninkielistä termiä build-työkalu. Niistä tunnetuimpia
Java-maailmassa ovat **Maven** ja **Gradle**. Build-työkalu automatisoi yllä
mainitun riippuvuuksien hallintatyön. Build-työkalu voi tehdä muutakin: se voi
ajaa mahdolliset testit ja myös pakata valmiin ohjelman jakelukuntoon.

Esittelemme seuraavaksi Maven-työkalun käyttöä IDEAssa. Aivan hyvin saman asian
voisi tehdä myös [Gradlella](https://gradle.org/) tai
[Antilla](https://ant.apache.org/). Maven on alkuvaiheessa ehkä aavistuksen
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

## Ensimmäinen projekti Mavenilla

Kokeillaan tehdä itse ensimmäinen Java-projekti Mavenilla. 

 1. Aloita luomalla uusi projekti. 
 2. Anna projektin nimeksi "EkaMavenProjekti". 
 3. Valitse IDEAssa Build System -kohdassa Maven. 
 4. Klikkaa Create.

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
tiedston näet XML-muotoista tekstiä. Tämä tiedosto määrittelee projektisi
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
joukossa. 

 * `groupId` toimii projektin "organisaatiotunnisteena". Se on usein käänteinen
   verkkotunnus, kuten `fi.jyu.ohjelmointi`. 
 * `artifactId` on projektin nimi, ja 
 * `version` kertoo projektin version. 

Näiden kolmen yhdistelmä muodostaa projektin yksilöllisen tunnisteen. Tässä
vaiheessa näillä tunnisteilla ei ole hirveästi merkitystä, mutta jos julkaiset
projektisi esimerkiksi Maven Central -varastoon, nämä tunnisteet ovat tärkeitä. 

Loput rivit määrittelevät projektin Java-version sekä koodin merkistökoodauksen. 

Avaa nyt `Main.java`-tiedostoa. Lisää sinne sivun alussa esitetty HTTP-kutsun
esimerkkikoodi ja yritä kääntää se. Projekti ei kuitenkaan käänny vielä, koska
OkHttp-kirjasto ei ole vielä projektin riippuvuuksissa. Riippuvuuksien
lisääminen Maven-projektiin tapahtuu muokkaamalla `pom.xml`-tiedostoa. Etsi
tiedostosta `<dependencies>`-elementti. Lisää se (ja sen vastinpari
`</dependencies>`), mikäli kyseistä elementtiä ei vielä ole. 

```xml
<dependency>
    <groupId>com.squareup.okhttp3</groupId>
    <artifactId>okhttp-jvm</artifactId>
    <version>5.3.2</version>
</dependency>
```

IDEA valittaa vielä, että okhttp-jvm-pakettia ei löydy. Riippuvuuksien
lisäämisen jälkeen Maven-projekti täytyy virkistää klikkaamalla
projektinäkymässä projektin nimen päältä hiiren oikealla, valitsemalla Maven ja
Sync project. Tämän jälkeen IDEA lataa tarvittavat okhttp-riippuvuuden, ja myös
kyseisen kirjaston itsensä vaatimat muut riippuvuudet. 

Lisää myös aivan koodin alkuun `package org.example;`, jotta koodi on oikeassa
pakkauksessa. Palaamme pakkauksen tarkempaan merkitykseen hieman alempana. 

Tallenna tiedosto ja käännä projekti. Nyt Maven hakee OkHttp-kirjaston Maven
Central -varastosta ja linkittää sen projektiisi. Tämän jälkeen käännös
onnistuu, ja näet HTTP-kutsun tulokset konsolissa.

## Maven Central

Riippuvuus-XML:iä ei tarvitse itse keksiä. Yksi suosituimmista Java-kirjastojen
varastoista on Sonatype-yrityksen ylläpitämä [Maven
Central](https://central.sonatype.com/), joka on julkinen varasto, josta voit
hakea ja ladata Java-kirjastoja sekä liittää niitä projektiisi. 

Voit etsiä tarvitsemasi kirjastot ja niiden riippuvuudet helposti Maven
Centralista, ja kopioida sieltä suoraan XML-koodin `pom.xml`-tiedostoosi.
Kokeillaan etsiä äsken mainittu okHttp-kirjasto Maven Centralista. 

 1. Mene osoitteeseen <https://central.sonatype.com/>
 2. Kirjoita hakukenttään "okhttp" ja paina Enter.
 3. Ensimmäinen hakutulos vie vanhempaan okHttp-kirjastoon, joka on nimeltään
    "okhttp". Valitse sen sijaan toinen hakutulos, joka on uudempi. 
 4. Näet Snippets-kohdassa valmiin XML-koodin, jonka *yleensä* voit kopioida suoraan
    `pom.xml`-tiedostoosi.
 5. Kopioi XML-koodi ja liitä se `pom.xml`-tiedostoon `<dependencies>`-elementin
    sisälle.

Aivan kaikkien kirjastojen kohdalla XML:ää ei voi välttämättä suoraan kopioida,
vaan sinun täytyy tarkistaa kirjaston dokumentaatiosta, onko XML
Maven-yhteensopiva. Juurikin [okHttp-kirjaston
kohdalla](https://square.github.io/okhttp/#maven-and-jvm-projects) on niin, että
XML:ää tarvitsee hivenen muuttaa, koska tarvitsemme nimen omaan
`okhttp-jvm`-version, joka on Maven-yhteensopiva. 

Tässä tapauksessa riittää, että vaihdetaan `artifactId`-elementti
`okhttp-jvm`:ksi, ja XML on valmis.

Riippuvuuden sisältämien luokkien käyttäminen edellyttää vielä, että lisäät
luokan alkuun `import`-lauseen, joka tuo tarvittavat luokat näkyviin.
Esimerkiksi OkHttp-kirjaston `OkHttpClient`-luokan käyttämiseksi sinun täytyy
lisätä `import okhttp3.OkHttpClient;`-lause luokan alkuun. Joskus voi olla
tarvetta tuoda useita luokkia samasta paketista, jolloin voit käyttää
jokerimerkkiä, kuten `import okhttp3.*;`, joka tuo kaikki `okhttp3`-paketin
luokat näkyviin.

## Kolmannen osapuolen riippuvuudet

Java-projekteissa on usein tarpeen käyttää kolmannen osapuolen kirjastoja, jotka
tarjoavat valmiita toiminnallisuuksia ja säästävät kehitysaikaa.
Maven-projekteissa on oletuksena käytettävissä Maven Central -varasto 
sekä käyttäjän *paikallinen* varasto. Jos haluamme käyttää jotain riippuvuutta,
joka ei sijaitse Maven Central -varastossa, voimme lisätä muitakin varastoja 
projektin käyttöön määrittelemällä ne `pom.xml`-tiedostossa seuraavasti.

```
<repositories>
    <repository>
        <id>varaston-tunnus</id>
        <url>varaston-url</url>
        <!-- Muut asetukset -->
    </repository>

    <!-- Muut varastot -->
</repositories>
```

Projektin käytössä olevien varastojen lista löytyy Intellij IDEA:n asetuksista: 

`File > Settings > Build, Execution, Deployment > Build Tools > Maven > Repositories`

### Paikalliset riippuvuudet

Maven asentaa kaikki lataamansa riippuvuudet paikalliseen kansioon, minkä 
jälkeen ne ovat kaikkien projektien käytettävissä. Tämä kansio löytyy 
käyttäjähakemiston alta polusta `.m2/repository`. Tähän paikalliseen varastoon 
on myös mahdollista lisätä itse paketteja, jolloin niihin voi viitata 
tavalliseen tapaan `pom.xml`-tiedostosta. 

Minkä tahansa jar-tiedoston voi lisätä paikalliseen repositorioon esimerkiksi 
seuraavalla komennolla. Tämä kuitenkin vaatii Maven-komentorivityökalujen 
asentamisen, joten emme tällä kurssilla tule sitä käyttämään.

```
mvn install:install-file \
   -Dfile=<tiedostopolku> \
   -DgroupId=<organisaatiotunniste> \
   -DartifactId=<projektitunniste> \
   -Dversion=<versionumero> \
   -Dpackaging=jar \
   -DgeneratePom=true
```

Kannattaa kuitenkin pitää mielessä, että nämä riippuvuudet ovat tällöin 
käytettävissä vain laitteella, jossa tämä manuaalinen lisääminen paikalliseen 
varastoon on suoritettu.

Voimme myös lisätä paikallisen riippuvuuden projektiin ilman, että se lisätään
paikalliseen varastoon. Tämä mahdollistaa esimerkiksi riippuvuuden sijoittamisen
projektin kansioon, jolloin se on helpompi lisätä myös projektin versionhallintaan.

Riippuvuus lisätään `pom.xml`-tiedostoon tavalliseen tapaan, mutta lisäämme 
`scope`-asetuksen ja annamme sen arvoksi `system`, jotta voimme käyttää 
`systemPath`-asetusta määrittämään paikallisen riippuvuuden tiedostopolun.

Muuttuja `${project.basedir}` viittaa projektin juureen, joten tässä esimerkissä
riippuvuuden tiedostopolku on projektin hakemistossa sijaitseva `lib/tiedosto.jar`.

```
<dependencies>
    <dependency>
        <groupId>organisaatiotunniste</groupId>
        <artifactId>projektitunniste</artifactId>
        <version>1.0</version>
        <scope>system</scope>
        <systemPath>${project.basedir}/lib/tiedosto.jar</systemPath>
    </dependency>
</dependencies>
```

## Pakkaukset Javassa

Kun Java-ohjelma kasvaa useista luokista koostuvaksi kokonaisuudeksi, luokkien
järjestäminen satunnaisesti samaan kansioon ei enää riitä. Tarvitsemme tavan
ryhmitellä toisiinsa liittyvät luokat loogisiksi kokonaisuuksiksi. Tätä varten
Java tarjoaa pakkaukset (engl. *packages*). Pakkaus on nimetty luokkien
kokoelma. Se toimii samalla sekä loogisena ryhmittelykeinona että teknisenä
nimialueena (*namespace*), joka estää nimikonfliktit. 

Luokan alussa voidaan määrittää `package`-lause, joka määrittelee pakkauksen,
johon luokka kuuluu.

```java,ignore
package fi.jyu.ohjelmointi; 

class User
{
    // ...
}
```

Nyt `User`-luokka kuuluu pakkaukseen `fi.jyu.ohjelmointi`. Luokan täydellinen
nimi on `fi.jyu.ohjelmointi.User`, mutta samassa pakkauksessa olevat luokat
voivat käyttää toistensa jäseniä suoraan ilman täydellisiä nimiä. Samaan
pakkaukseen kuuluvat luokat voivat käyttää toistensa jäseniä ilman erillisiä
`import`-lauseita, ja ilman tarvetta käyttää luokkien täydellisiä nimiä. 

```java,ignore
package fi.jyu.ohjelmointi;

class Main
{
    static void main() {
        User user = new User();
        // ...
        // Voidaan myös tehdä näin, mutta se on turhaa, koska Main ja User kuuluvat samaan pakkaukseen:
        fi.jyu.ohjelmointi.User user2 = new User();
    }
}
```

Pakkaus liittyy suoraan myös projektin kansiorakenteeseen. Jokainen pakkauksen
osa vastaa yhtä kansiota. Esimerkiksi pakkaus `org.example` vastaa
kansiorakennetta `src/main/java/org/example/Main.java`. Tämä ei ole pelkkä
suositus, vaan Java-kääntäjä edellyttää, että tiedoston sijainti vastaa sen
pakkausmäärittelyä.

Pakkauksia käytetään myös muiden kirjastojen luokkien hyödyntämiseen. Kun
kirjasto lisätään projektiin, sen luokat sijaitsevat omissa pakkauksissaan.
Näiden luokkien käyttäminen edellyttää `import`-lausetta. Esimerkiksi
OkHttp-kirjaston `OkHttpClient`-luokka kuuluu pakkaukseen okhttp3, ja sen
käyttämiseksi kirjoitetaan `import okhttp3.OkHttpClient;`. `Import`-lause ei
kopioi luokkaa omaan projektiisi, vaan kertoo kääntäjälle, mistä paketista
luokka löytyy. Ilman `import`-lausetta luokkaa voisi käyttää vain sen
täydellisellä nimellä:

```
okhttp3.OkHttpClient client = new okhttp3.OkHttpClient();
```

Palataan vielä `User`-luokan esimerkkiin. Samassa projektissa voisi olla
toinenkin pakkaus, nimieltään `com.example.library`, joka sisältää
`User`-luokan.

```java,ignore
package com.example.library;

class User
{
    // ...
}
```

Vaikka projektissa on nyt kaksi `User`-luokkaa, niiden täydelliset nimet
eroavat, eikä ristiriitaa synny. Joskus voidaan haluta käyttää molempia
`User`-luokkia samassa kooditiedostossa. Tällöin luokat tuodaan projektiin
`import`-lauseilla, ja niitä käytetään täydellisillä nimillä, jotta voidaan
erottaa, kumpaa `User`-luokkaa tarkoitetaan.

```java,ignore
import fi.jyu.ohjelmointi.User;
import com.example.library.User;

void main() {
    fi.jyu.ohjelmointi.User user1 = new fi.jyu.ohjelmointi.User();
    com.example.library.User user2 = new com.example.library.User();
}
```

Tällainen tilanne on ehkä käytännössä harvinainen, mutta se korostaa pakkauksen
merkitystä nimialueena.

Pakkausten nimissä käytetään vakiintunutta käytäntöä, joka perustuu
käänteiseen verkkotunnukseen. Esimerkiksi Jyväskylän yliopiston projektissa
pakkauksen nimi voisi olla

```
fi.jyu.ohj2.munekamavenprojekti
```

Tämä käytäntö auttaa varmistamaan, että pakkausten nimet ovat
maailmanlaajuisesti yksilöllisiä, mikä on erityisen tärkeää, jos kirjasto
julkaistaan muiden käytettäväksi.

Aivan pienissä ohjelmissa pakkauksia ei käytännössä tarvita, ja compact Java
-tyylisen ohjelman kaikki luokat voidaan sijoittaa samaan kansioon ilman
pakkauksia. Pakkaukset ovat kuitenkin keskeinen osa suurten Java-ohjelmien
rakennetta. Ne auttavat pitämään koodin järjestyksessä ja estävät
nimikonfliktit. Ne muodostavat myös perustan Java-kirjastojen ja
build-työkalujen, kuten Mavenin, käyttämälle standardoidulle kansiorakenteelle.
Tämä rakenne varmistaa, että sekä kehitystyökalut että ajoympäristö löytävät
luokat oikeista paikoista ja voivat käyttää niitä oikein. 

IDEAssa pakkauksen saa näppärästi määritettyä Maven-projektia luotaessa.
Tehdessäsi uutta projektia, valitse Advanced settings, ja kirjoita
GroupID-kenttään haluamasi pakkauksen nimi. IDEA tekee näin automaattisesti
oikean kansiorakenteen ja lisää `Main.java`-tiedoston määrittelemääsi
pakkaukseen.

## Tehtävät

<task>
  <task-title>Tehtävä 6.8: Riippuvuudet. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/6-8-riippuvuudet/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa6/tehtava8">Tee tehtävä TIMissä</a></task-link>
</task>
