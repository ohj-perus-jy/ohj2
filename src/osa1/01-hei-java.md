# Hei, Java!

> [!Osaamistavoitteet]
>
> - Java-kielen perusteet
> - Tiedät miten Java-ohjelma käännetään ja ajetaan (komentoriviohjelmat javac, java ja jshell, IDE-säädöt)
> - Tiedät mikä on (J)VM ja miten kääntäminen eroaa tulkkauksesta 
> - Tunnet Java-kielen vastineita yleisimmille I/O-operaatioille (tekstin tulostus, lukeminen konsolilta)

Ohjelmointi 2 -kurssilla käytämme Java-ohjelmointikieltä. Java on
yleiskäyttöinen olio-ohjelmointia tukeva kieli, joka on tarkoitettu alustasta
riippumattomien ohjelmien kirjoittamiseen. Java on suosittujen
ohjelmointikielten kärkilistoilla (ks. esim. 
[TIOBE index](https://www.tiobe.com/tiobe-index/), 
[StackOverflow 2025 developer survey](https://survey.stackoverflow.co/2025/technology), 
[suosituimmat kielet GitHub-palvelussa](https://madnight.github.io/githut)). 
Javan syntaksi muistuttaa paljon 
[Ohjelmointi 1 -kurssilla](https://ohjelmointi1.it.jyu.fi)
käytettyä C#-kieltä.

## Java-kielen perusteet

Lähdetään liikkeelle perinteisellä 'Hei, maailma' -esimerkillä Javalla:

```java
/* 1 */ void main() {
/* 2 */     IO.println("Hei, maailma!");
/* 3 */ }
```

Käydään läpi ohjelma rivi riviltä:

1. Java-ohjelman suoritus alkaa `main`-nimisestä aliohjelmasta. `void`
   tarkoittaa, että aliohjelma ei palauta mitään arvoja. Koska pääohjelma ei ota
   parametreja, sulut voidaan jättää tyhjäksi. Javassa samalla rivillä
   aloitetaan myös aliohjelman runko aaltosululla `{`.

2. Javassa lause loppuu yleensä puolipisteeseen `;`. Tekstin tulostaminen
   onnistuu `IO.println`-metodilla.

3. Aliohjelman runko lopetetaan aaltosululla `}`.

## Javan koodauskäytänteistä

Kuten eri kielissä on tapana, Javassa on oma joukko vakiintuneita
koodauskäytänteitä. Tutustumme erilaisiin käytänteisiin tämän materiaalin
edetessä. Mainittakoon, että Javan koodauskäytänteet poikkeavat hieman C#-kielen
käytänteistä aliohjelmien nimeämisessä ja aaltosulkujen asettamisessa.

Tässä olennaisimmat Javan koodauskäytänteet, joita on tässä vaiheessa hyvä pitää
mielessä:

- Aliohjelman runkoa aloittava aaltosulku `{` laitetaan yleensä samalle riville
  kuin aliohjelman määrittely. Sama pätee muihin rakenteisiin, joissa käytetään
  aaltosulkuja, kuten `if`-, `for`-, `while` ja `do-while` -rakenteille.

- Aliohjelmien nimeämisessä käytetään camelCasing-tyyliä, eli ensimmäinen
  kirjain on pienellä ja seuraavat sanat aloitetaan isolla kirjaimella.
  Esimerkiksi `tamaOnFunktionNimi`. Samaa tyyliä käytetään myös muuttujien
  nimeämisessä.

- Tiedostot ja myöhemmin kurssilla käytettävät luokat, rajapinnat ja listaukset
  nimetään PascalCasing-tyylillä. Esimerkiksi `HeiMaailma.java`, `public class
  Opiskelija {...`, `public interface Saadettava {...` tai `public enum
  Viikonpaiva { ...`.


## Opas: Java-ohjelmien kääntäminen ja ajaminen

> [!TÄRKEÄÄ]
>
> Tässä osiossa tarvitset opintojakson työkaluja. Käy ensin asentamassa kaikki
> työkalut [Työkaluohjeesta](../tyokalut.md).

Tässä materiaalissa käytämme IntelliJ IDEA -kehitysympäristöä Java-ohjelmien
luomiseen, ajamiseen ja virheenjäljitykseen.

### Luo uusi Java-projekti

Luodaan seuraavaksi yksinkertainen Java-projekti IDEAssa.
Projekti on IDEA-kehitysympäristön tapa koostaa lähdekooditiedostoja,
testeja, kirjastoja ja muita lisätiedostoja yhteen kokonaisuuteen.

Tee seuraavasti:

1. Avaa IntelliJ IDEA ja avaa uuden projektin dialogi.

    Jos sinulle avautui *Welcome to IntelliJ IDEA*, valitse
    **New Project**.
    
    Jos sinulle avautui jokin valmis Java-projekti, valitse yläpalkissa 
      **File** <i class="bi bi-chevron-right"></i>
      **New** <i class="bi bi-chevron-right"></i>
      **Project**.
      
      <img src="images/intellij-new-project.png" width="500">

      Yläpalkin valinnat saattavat olla hampurilaisvalikkopainikkeen (<i class="bi bi-list"></i>) takana.

2. Uuden projektin dialogissa aseta seuraavat tiedot:

    * Valitse vasemmalla puolella olevasta listasta projektityypiksi **Java**.

    * Aseta projektin nimeksi **Name**-kenttään `HelloWorld`. Projektien nimet yleensä
      kirjoitetaan ilman välilyöntejä.

    * Aseta projektin sijainti **Location**-kenttään. Klikkaa kentän oikealla puolella 
      olevaa kansiokuvaketta (<i class="bi bi-folder2"></i>) ja valitse
      projektille sopiva kansio. Valitse sellainen kansio, jonka löydät tulevaisuudessakin
      helposti omalta tietokoneelta.

    * Valitse **Build system**-rivillä **IntelliJ**.  
      Tutustumme muihin projektien rakennusjärjestelmiin myöhemmissä osissa.

    * Varmista, että **JDK**-kentässä on sama JDK-versio kuin minkä olet asentanut [Työkaluohjeissa](../tyokalut.md#java-development-kit-jdk).

    * Laita ruksi **Add sample code** pois päältä. Lisäämme kooditiedoston itse.

    * Laita ruksi **Create Git repository** pois päältä. Emme tarvitse vielä versiohallintaa tässä vaiheessa.

    Yllä olevien muutosten jälkeen tuloksen pitäisi näyttää seuraavalta:

    <img src="images/intellij-new-project-dialog.png" width="600">
    
3. Paina **Create**. Tämän jälkeen IDEA luo uuden projektin valitsemaasi kansioon.

    Käydään pikaisesti läpi IDEAn olennaisimmat osat:

    <img src="images/intellij-main-view-parts.png" width="600">


    1. **Koodialue**: projektissa olevien tiedostojen sisällöt näkyvät tässä, kun ne avataan.
       Kukin avattu tiedosto avautuu omaan välilehteen.
    2. **Projektiselain**: projektissa olevat kansiot ja tiedostot näkyvät tässä.
       Selaimen kautta voidaan lisätä, poistaa, siirtää tai uudelleennimetä tiedostoja ja kansioita.
    3. **Projektin ajaminen ja debuggaus**: tässä näkyy ajettavan Java-ohjelman nimi,
       ohjelman ajopainike (<i class="bi bi-play-fill"></i>) ja debuggauspainike (<i class="bi bi-bug"></i>).
    4. **Valikot ja näkymät**: IDEAssa on erilaisia näkymiä, jotka ovat oletuksella piilossa.
       Sivupalkin avulla voidaan avata ja piilottaa näkymät tarpeen mukaan. Esimerkiksi
       projektiselaimen voi piilottaa painamalla sivupalkissa olevasta kansiokuvakkeesta (<i class="bi bi-folder2"></i>).

### Luo lähdekooditiedosto

IntelliJ-projektissa kaikki koodi laitetaan `src`-kansioon.
Luodaan seuraavaksi yksinkertainen Java-lähdekooditiedosto, johon
voidaan kirjoittaa koodi.

Tee seuraavasti:

1. Projektiselaimessa klikkaa oikealla hiiren painikkeella `src`-kansiosta
   ja valitse **New** <i class="bi bi-chevron-right"></i> **Java Compact File**.

2. Aseta avautuneessa dialogissa lähdekooditiedoston nimeksi `Ohjelma` ja paina <kbd>Enter</kbd>.

<video src="images/intellij-new-java-file.mp4" controls></video>

IDEA luo uuden `Ohjelma.java`-nimisen tiedoston `src`-kansioon. IDEA myös lisää
automaattisesti `main`-aliohjelman määrittelyn lähdekooditiedostoon.

Samalla IDEA avaa lähdekooditiedoston koodialueelle. Voit jatkossa avata
tiedoston myös klikkaamalla se kahdesti projektinäkymästä.

### Kirjoita koodi

Kirjoitetaan seuraavaksi yksinkertainen "Hei, maailma" -ohjelma alusta alkaen
juuri luotuun `Ohjelma.java`-tiedostoon.

Tee seuraavasti:

1. Poista kaikki koodi `Ohjelma.java` -tiedostosta.

   IDEA lisää yleensä valmista pohjakoodia uusiin lähdekooditiedostoihin.
   Tätä harjoitusta varten kirjoitamme kuitenkin koodia itse.

2. *Kirjoita* seuraava koodi `Ohjelma.java` -tiedostoon:

    ```java,noplayground
    void main() {
        IO.println("Hei, maailma!");
    }
    ```

    *Vältä kopioimasta koodia*, vaan kirjoita se itse. Kirjoittaminen itse
    usein auttaa muistamaan, mistä eri ohjelmoinnissa käytettävät merkit,
    kuten aaltosulut, kaarisulut ja puolipiste löytyvät.

<details closed>
<summary><i class="bi bi-stars jyu-gold"></i> Bonus: IDEAn täydennysominaisuuksien käyttäminen</summary>

IDEA tarjoaa lisäksi erilaisia aikaa säästäviä täydennysominaisuuksia, 
joiden käyttöä on hyvä harjoitella.

Voit kokeilla seuraavia täydennysominaisuuksia:

* `main`-pääohjelman automaattinen lisääminen: Aloita kirjoittamalla `main`.
    Paina sen jälkeen <kbd>Ctrl</kbd>+<kbd>Space</kbd> (macOS: <kbd>⌘</kbd>+<kbd>Space</kbd>).
    Valitse nuolinäppäimillä `main`-pohja ja paina <kbd>Enter</kbd>:

    <video src="images/intellij-main-template.mp4" controls></video>
    
    IDEA sisältää erilaisia valmiita pohjia, jotka nopeuttavat
    koodin kirjoittamista ja helpottavat yleisempien rakenteiden muistamista.
    Näet kaikki koodipohjat painamalla <kbd>Ctrl</kbd>+<kbd>J</kbd>
    (macOS: <kbd>⌘</kbd>+<kbd>J</kbd>).

* `println`-aliohjelman automaattinen täydentäminen: Siirrä kursori 
`main`-pääohjelmaan tyhjälle riville. 

Kirjoita alkuun kirjain `I`, minkä jälkeen IDEA automaattisesti näyttää
kaikki kursorin kohdalle sopivat rakenteet, jotka alkavat kirjaimella I.
Valitse nuolipainikkeilla `IO` ja paina <kbd>Enter</kbd>. Tämä 
täydentää `IO` kursorin kohdalle.

Kirjoita sen jälkeen `.` (piste), minkä jälkeen IDEA automaattisesti näyttää
kaikki `IO`-luokassa olevat aliohjelmat. Siirry listassa nuolipainikkeilla
`println`-aliohjelman kohdalle ja paina <kbd>Enter</kbd>.
Tämä täydentää `println`-tekstin kursorin kohdalle.

Kirjoita sen jälkeen kaarisulku `(`. IDEA automaattisesti täydentää
lopettavan kaarisulun `)`. Siirry nuolipainikkeilla kaarisulkujen väliin
ja kirjoita `"Hei, maailma!"`. Lopuksi siirry rivin loppuun painamalla <kbd>End</kbd>
tai nuolinäppäimiä käyttäen ja lisää loppuun puolipiste `;`.

<video src="images/intellij-auto-completion.mp4" controls></video>

IDEA osaa automaattisesti siis ehdottaa luokkien ja aliohjelmien nimiä
kontekstin perusteella. Voit myös aina erikseen avata automaattisen
täydennyksen painamalla

</details>
        
### Ohjelman ajaminen

Kooditiedostoja, jotka sisältävät `main`-aliohjelman, voidaan suorittaa.
Suorittaminen onnistuu ajopainikkeella (<i class="bi bi-play-fill"></i>),
joka sijaitsee `main`-aliohjelman vieressä sekä IDEA:n yläpalkissa.

Tee seuraavasti:

1. Klikkaa `main`-aliohjelman vasemmalla puolella olevaa ajopainiketta (<i class="bi bi-play-fill"></i>).

   IDEA ensin kääntää ohjelmasi. Kun ohjelma on käännetty, koodieditorin alapuolelle
   avautuu **Run**-ikkuna, ja IDEA ajaa ohjelmasi.

   Ensimmäinen rivi ikkunassa näyttää komennon, jota IDEA käytti käännetyn tiedoston
   ajamiseksi.
   Seuraavalla rivillä näet ohjelman tulosteen, tässä tapauksessa
   `IO.println`-aliohjelmalla tulostettu `Hei, maailma!`.
   Viimeinen rivi näyttää poistumiskoodin `0` sen merkiksi, että ohjelman suoritus
   päättyi ilman virheitä.

   <video src="images/intellij-run-gutter.mp4" controls></video>

2. Kokeile vielä ohjelman ajamista luodulla ajokonfiguraatiolla.

   Kun ajat kooditiedoston ensimmäistä kertaa, IDEA luo erikoisen 
   *ajokonfiguraation*, jonka perusteella koodi käännetään ja ajetaan.
   
   Kun ajokonfiguraatio on luotu ensimmäisen ajon jälkeen, voit jatkossa
   ajaa koodin aina IDEA:n yläpalkissa olevalla ajopainikkeella. Tällä tavoin
   voit helposti ajaa samoja ohjelmia ilman, että kooditiedostoa tarvitsisi
   erikseen avata.

   IDEAn yläpalkissa pitäisi nyt näkyä `Ohjelma`-konfiguraation nimi,
   jonka vieressä on ajopainike (<i class="bi bi-play-fill"></i>).
   Kokeile sulkea `Ohjelma.java` ja suorittaa ohjelma yläpalkin kautta.

   <video src="images/intellij-run-config.mp4" controls></video>

   Ajokonfiguraatioiden avulla voit kirjoittaa useita ohjelmia samaan kansioon
   ilman, että tarvitsisi tehdä uusia projekteja.
   Myöhemmin materiaalissa tutustumme lisäksi Gradle-hallintatyökaluun,
   jonka avulla teemme muun muassa erillisiä ajokonfiguraatioita projektin
   ajamiselle, testaamiselle ja kääntämiselle.


## Miten Java-ohjelmat ajetaan?

Java on lähtökohtaisesti *käännettävä* ohjelmointikieli: ennen kuin
IDEA varsinaisesti ajaa ohjelman, se käännetään ajettavaan muotoon.
Tutkitaan seuraavaksi, mitä tämä käytännössä tarkoittaa kääntämällä
ja ajamalla ohjelma suoraan komentoriviltä.


<details closed><summary>Miten voin seurata mukana?</summary>

Tee alkuun yksinkertainen ohjelma [yllä olevan oppaan](#opas-java-ohjelmien-kääntäminen-ja-ajaminen)
mukaisesti IDEA-kehitysympäristössä.

Sen jälkeen avaa IDEA:n vasemmasta näkymäpalkista komentorivi painamalla komentorivipainikkeesta 
(<i class="bi bi-terminal"></i>).
Tämä avaa käyttöjärjestelmän komentorivin (zsh macOS:lla, Powershell Windowsilla,
oletuskomentorivi Linuxilla).

Jos latasit Java-kehitysympäristön seuraamalla [työkaluohjeita](../tyokalut.md#java-development-kit-jdk),
komentorivi ei löydä mitään Javan kääntämiseen tarkoitettuja työkaluja.
Ota työkalut käyttöön kopioimalla ja liittämällä alla oleva komento:

#### [Windows](#tab/win)

```bash
Get-ChildItem -Path "$env:USERPROFILE\.jdks" -Directory | Sort-Object Name -Descending | Select-Object -First 1 | ForEach-Object { $env:JAVA_HOME = $_.FullName; $env:PATH = "$_.FullName\bin;$env:PATH" }
```

***

#### [macOS](#tab/macos)

```bash
export JAVA_HOME=$(/usr/libexec/java_home) && export PATH="$JAVA_HOME/bin:$PATH"
```

***

### [Linux](#tab/linux)

```bash
export JAVA_HOME=$(printf "%s\n" ~/.jdks/* | sort -V | tail -n 1) && export PATH="$JAVA_HOME/bin:$PATH"
```

***

### [Valitse](#tab/default)

Valitse käyttöjärjestelmäsi yllä olevista vaihtoehdoista.

***

</details>

Avataan nyt komentorivi ja siirrytään alkuun projektikansioon.
Tarkastellaan vielä, mitä tiedostoja projektista löytyy:

<asciinema src="images/rec_ls_files.cast" rows="3" poster="npt:2"></asciinema>

Koska käytössämme on IntelliJ-projekti, sieltä löytyy vain muutama olennainen tiedosto ja kansio:

- `HelloWorld.iml` on projektin konfiguraatio, jolla IDEA tunnistaa kansion olevan Java-projekti
- `src` on lähdekoodikansio, jossa kaikki lähdekooditiedostot sijaitsevat
- `out` on kansio, joka sisältää käännetyt ohjelmat

Siirrytään nyt `src` kansioon ja tarkastellaan sen sisältö:

<asciinema src="images/rec_cd_project.cast" rows="4" poster="npt:5"></asciinema>

`.java`-tiedostopäätettä käytettävät tiedostot ovat Javan *lähdekooditiedostoja*.
Ne sisältävät ohjelman lähdekoodia tekstinä eivätkä ne ole vielä suoraan
ajettavissa.

Jotta ohjelma voidaan ajaa, se pitää kääntää.
Java-lähdekoodin kääntäminen onnistuu Java-kehitysympäristön (Java Development Kit, JDK)
kanssa tulleen `javac`-kääntäjäohjelman avulla.
Kokeillaan kääntää `Ohjelma.java`:

<asciinema src="images/rec_javac.cast" rows="2" poster="npt:5"></asciinema>

`javac`-komento ei tulosta oletuksella mitään, jos kääntäminen tapahtuu 
onnistuneesti.
Tutkitaan vielä kansion rakenne `ls`-komennolla:

<asciinema src="images/rec_javac_ls.cast" rows="3" poster="npt:5"></asciinema>

Kääntämisen seurauksena siis syntyy `.class`-päätteinen tiedosto.
Tämä tiedosto sisältää ns. *tavukoodia*, joka on tiedoston käännetty muoto.
Tavukoodi ei ole suoraan prosessorilla ajettava ohjelma, vaan eräänlainen välivaihe.
Tavukoodia voidaan kuitenkin suorittaa Javan virtuaalikoneella (JVM, Java Virtual Machine),
joka on erillinen ohjelma, joka osaa tulkita ja suorittaa tavukoodia.
Vaikka tämä voi kuulostaa turhan monimutkaiselta, hyöty on siinä, että 
ohjelma joka on käännetty Java-tavukoodiksi voidaan nyt ajaa alustariippumattomasti (Windows, macOS, Linux, jne.), kunhan JVM on toteutettu kyseisellä alustalla. 
JVM voi puolestaan optimoida tavukoodia juuri alustalle ja prosessorille
sopivaan muotoon tai tarvittaessa tulkata tavukoodia suoraan 
ns. skriptauskielten tapaan, kuten Python tai Lua.
Javalla onkin iskulause: "Write Once, Run Anywhere", jolla viitataan tähän periaatteeseen.

<!-- DZ: Onko tarpeellinen tähän? Yllä vähän tiivistetty versio.
Käytetyin JVM:n spesifikaation toteutus on nimeltään HotSpot, joka sisältää sekä tulkin että JIT (**J**ust **I**n **T**ime) kääntäjän. Tulkki käynnistää ohjelman ja JVM etsii koodista toistuvia pätkiä, jotka käännetään kyseisen alustan konekieliseksi koodiksi JIT kääntäjällä, jotta ohjelma pyörisi nopeammin. Alustakohtainen käännetty konekieli on aina nopeampi ajaa kuin tulkattava kieli. Javan tyyli käyttää sekä tulkkausta, että kääntämistä on kompromissi alustariippumattomuuden ja suoritusnopeuden välillä. -->

JDK:n kanssa tulee myös valmiiksi Java-virtuaalikone sekä Javan ajoympäristö (JRE, Java Runtime Environment), joka sisältää yleisempiä toimintoja, joita Java-ohjelma saattaa käyttää.
Tavukooditiedosto voidaan ajaa JVM:llä käyttäen `java`-komentoa:

<asciinema src="images/rec_java.cast" rows="3" poster="npt:5"></asciinema>

Huomaa, että `java`-komentoa antaessa kirjoitetaan tavukooditiedoston nimi
ilman `.class`-päätettä.
Myöhemmin materiaalissa tutustumme Gradle-projektinhallintaohjelmaan, jolla
pystyy kääntämään useita lähdekooditiedostoja yhteen `.jar`-tiedostoon, johon
voidaan pakata kaikki ohjelman ajamiseen tarvittavat tiedostot.
Myös `.jar`-tiedostot voidaan suorittaa `java`-komennolla.

> [!VINKKI]
>
> Alkaen Javan versiosta 11 `java`-komento osaa myös automaattisesti kääntää 
> ja suorittaa `.java`-lähdekooditiedostot ilman erillistä `javac`-kääntäjän
> ajamista.
>
> Lisäksi tässä materiaalissa käytämme pääosin IDEA-kehitysympäristöä, joka
> hoitaa lähdekooditiedostojen kääntämisen automaattisesti ja tehokkaasti.

<details closed>
<summary><i class="bi bi-stars jyu-gold"></i> Bonus: <code>jshell</code>-tulkkiohjelma</summary>

Vaikka Java lasketaan käännettäväksi kieleksi, toisinaan voi olla hyödyllistä
kokeilla Java-ohjelmien kirjoittamista interaktiivisesti ilman jatkuvaa
kääntämistä.
Interaktiivisuus tässä tarkoittaa, että voit kokeilla eri komentoja rivi/lohko
kerrallaan ilman erillistä kääntämistä ja ajamista, luokkia tai `main`-pääohjelmaa.

Tätä varten JDK sisältää `jshell`-ohjelman, joka on Java-ohjelman 
komentorivitulkki eli ns. REPL-tulkki (read-evaluate-print-loop).

`jshell` tarjoaa useita hyödyllisiä toimintoja, kuten:

- Luokkien ja aliohjelmien nimien täydennys ja haku <kbd>Tab</kbd>-painikkeella
- Lausekkeiden suorittaminen ilman tarvetta `main`-aliohjelmalle

`jshell`-ohjelmasta voi poistua `/exit`-komennolla.

<asciinema src="images/rec_jshell.cast" rows="25" poster="npt:60" controls></asciinema>

</details>

<!-- ### jshell
jshell on interaktiivinen tulkki Java-ohjelmoinnin opetteluun. Interaktiivisuus tarkoittaa, että voit kokeilla eri komentoja rivi/lohko kerrallaan ilman erillistä kääntämistä ja ajamista, luokkia tai `main`-metodia. Pääset kokeilemaan jshelliä ajamalla komennon `jshell`. Nyt voit esimerkiksi kirjoittaa komennon `IO.println("Hei maailma!");` ja painaa `Enter`, jolloin näet heti tulostuksen komentorivillä. Vastaavasti voit luoda muuttujia ja näet heti, mitä niihin on sijoitettu.

jshellistä poistutaan ajamalla komento `/exit` -->

## Tekstin tulostaminen ja lukeminen

Jatkossa voi olla hyödyllistä tulostaa erilaisia asioita komentoriviin
ja toisaalta lukea tietoa sieltä.  
Javan `IO`-luokka tarjoaa kolme perustoimintoa tekstin tulostamiseen ja lukemiseen
komentorivillä:

| Aliohjelma | Esimerkki                       | Selitys                                                                  |
| ---------- | ------------------------------- | ------------------------------------------------------------------------ |
| `println`  | `[java] IO.println("Moi!");`           | Tulostaa parametrina annetun arvon ja lisää loppuun rivinvaihdon         |
|            | `[java] IO.println();`                 | Tulostaa rivinvaihdon                                                    |
| `print`    | `[java] IO.print("Samalla rivillä!");` | Tulostaa parametrina annetun arvon ilman rivinvaihtoa                    |
| `readln`   | `[java] IO.readln();`                  | Lukee käyttäjän syötettä komentoriviltä rivinvaihtoon asti               |
|            | `[java] IO.readln("Anna sana > ");`    | Sama kuin `readln`, mutta tulostaa ensin annetun tekstin ennen syötettä. |


Katsotaan vielä näiden yhteistoimintaa.
Voit muokata alla olevaa esimerkkiä vapaasti ja kokeilla, miten erilainen
tulostus toimii.

```java,editable
void main() {
    String nimi = IO.readln("Anna nimesi: > ");
    IO.println();
    IO.println("Moi, " + nimi + "!");

    IO.print("Tämä teksti");
    IO.print(" menee samalle");
    IO.print(" riville");
    
    IO.println(); // Kokeile ottaa tämä pois ja katso, mitä tapahtuu

    IO.println("Tervetuloa Ohjelmointi 2 -kurssille!");
}
```

## Kommentointi ja dokumentointi

Ennen kuin päästään varsinaisesti koodaamaan, otetaan vielä kertaus koodin
kommentoinnista.

Lähdekoodiin voi kirjoittaa tekstiä, joka ei ole varsinaista koodia, vaan
selittää sitä. Tällaista selitystekstiä on kahdentyyppisiä: (1) koodin sekaan
kirjoitettavia kommentteja (nimitetään näitä lyhyesti *kommenteiksi*) sekä (2)
dokumentaatiokommentteja. 

Kommenttien tarkoitus on palvella *kehityksen aikaista* tekemistä. Ne näkyvät
sisäisesti, eli ohjelmoijalle itselleen.  Dokumentaatiokommenttien tarkoitus on
palvella kaikkia, jotka *käyttävät* koodia. Ne näkyvät paitsi ohjelmoijalle
itselleen, myös niille, jotka hyödyntävät koodia esimerkiksi API:n (*application
programming interface*) kautta.

### Yhden rivin kommentointi
Yhden rivin kommentteja, jonka syntaksi on `//` voidaan käyttää esimerkiksi
merkitsemään TODO-kohtia koodissa:

```java
void main() {
    // TODO: Tarkista millaisia ongelmia tästä ratkaisusta voi tulla
    String syote = IO.readln();
    IO.println("Kirjoitit: " + syote);
}
```

Yleisesti hyvä periaate on se, että ohjelmoija pyrkii kirjoittamaan koodia, joka
selittää itse itseään. Tällöin asiat, jotka voidaan nimetä (kuten muuttujat,
luokat, funktiot), pyritään nimeämään mahdollisimman kuvaavasti, jolloin
yksittäisten rivien kommentointi ei välttämättä ole tarpeen. Joskus tältä ei voi
välttyä, koska jotakin operaatiota ei voida olettaa itsestäänselväksi tai
muuttujan nimestä tulisi kohtuuttoman pitkä:

```java
void main() {
    int n = 9;
    // Pyöristää alaspäin lähimpään neljällä jaolliseen lukuun
    int pyoristetty = n & ~3; 
    IO.println(pyoristetty);
}
```

Nyt muuttujan `pyoristetty` tilalla voisi olla
`pyoristaaAlaspainLahimpaanNeljallaJaolliseenLukuun`, joka ei sekään ole oikein
järkevä vaihtoehto.

### Monirivinen kommentti

Javassa monirivinen kommentti tulee `/*` ja  `*/` väliin. Tällaista suositellaan
käytettäväksi, kun jokin monimutkaisempi logiikka vaatii tarkempaa avaamista
ja/tai on järkevää selittää miksi juuri kyseinen ratkaisu on valittu. Tätä
kommenteissa olevaa tarkempaa avaamista ei kuitenkaan ole tarkoitus näyttää
koodin käyttäjille.

```java,noplayground
if (kayttaja.kayttaaVanhaa) {
    /* 
     * Vanhat käyttäjät (rekisteröityneet ennen vuotta 2022) käyttävät 
     * toistaiseksi vanhaa käyttöoikeusmallia.
     * Älä poista tarkistusta, ennen kuin kaikki tilit on siirretty.
     */
    return kaytaVanhojaKayttooikeuksia(kayttaja);
}
```

### Dokumentaatiokommentti

Dokumentaatiokommentit alkavat `/**` ja päättyvät `*/`, eli ovat
syntaksiltaan hyvin lähellä monirivistä kommenttia.

```java
//- void main() {
//-   IO.println("summa(1, 2) ==> " + summa(1, 2));
//- }
//-
/**
 * Laskee kahden kokonaisluvun summan.
 * 
 * @param a Ensimmäinen luku
 * @param b Toinen luku
 * @return Lukujen summa
 */
public int summa(int a , int b) {
    return a + b;
}
```

Aliohjelman dokumentaatiokommentin runko syntyy automaattisesti
IDEA-kehitysympäristössä, kun aliohjelman esittelyrivin yläpuolelle kirjoittaa
merkit `/**` ja painaa <kbd>Enter</kbd>. 

<video src="images/intellij-docstring.mp4" controls></video>


<details closed><summary><i class="bi bi-stars jyu-gold"></i> Bonus: miltä Javan dokumentaatio näyttää? </summary>

Oletetaan nyt, että tallennat yllä olevan tiedostoon `Summa.java`
ja ajat sen jälkeen komennon `javadoc Summa.java`
Nyt voit avata luodun `index.html` -tiedoston selaimessa, 
klikata selaimessa luokkaa `Summa` ja pääset seuraavanlaiseen näkymään:

![Juuri tehdystä dokumentaatiosta kuva, joka voi näyttää tutulta jos on käynyt
tutkimassa Javan omaa dokumentaatiota ](images/summaDokumentaatio.png)

Näyttääkö tutulta? Vertaa esimerkiksi [Javan dokumentaatioon
IO-luokasta](https://docs.oracle.com/javase/8/docs/api/java/lang/Object.html)
</details>

## Tehtävät

<task>
<task-title>Tehtävä 1.1: Oma ohjelma Javalla <points>1 p.</points> </task-title>
<handout>

Tee uusi IDEA-projekti nimeltään `OmatTiedot`. Lisää projektiin uusi
Java-tiedosto (Java Compact File) nimeltään `OmatTiedot.java`
ja kirjoita ohjelma, joka tulostaa *kullekin eri riville*

- Nimesi
- Puhelimesi merkin
- Puhelimesi mallin

</handout>
<task-link><a href="#">Tee tehtävä TIMissä</a></task-link>
</task>