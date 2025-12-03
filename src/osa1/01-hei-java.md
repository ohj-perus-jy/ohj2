# Hei, Java!

> [!Osaamistavoitteet]
>
> - Java-kielen perusteet
> - Tiedät miten Java-ohjelma käännetään ja ajetaan (komentoriviohjelmat javac, java ja jshell, IDE-säädöt)
> - Tiedät mikä on (J)VM ja miten kääntäminen eroaa tulkkauksesta 
> - Tunnet Java-kielen vastineita yleisimmille I/O-operaatioille (tekstin tulostus, lukeminen konsolilta)

## Java-kielen perusteet

Lähdetäänpä liikkeelle perinteisellä 'Hei, maailma' -esimerkillä kirjoittamalla se Javalla:

```java
/* 1 */ void main() {
/* 2 */     IO.println("Hei, maailma!");
/* 3 */ }
```
Käydään läpi ohjelma rivi riviltä:

1. Java-ohjeman suoritus alkaa `main`-nimisestä aliohjelmasta. `void` tarkoittaa, että aliohjelma ei palauta mitään arvoja.
Javassa samalla rivillä aloitetaan myös aliohjelman runko aaltosululla`{`.

2. Javassa lause loppuu yleensä puolipisteeseen `;`. Tekstin tulostaminen onnistuu `IO.println`-metodilla.

3. Aliohjelman runko lopetetaan aaltosululla `}`.

## Javan koodauskäytänteistä

Kenties ensimmäisenä Javassa C#:iin verrattuna syntaksista voidaan huomata, että uuden näkyvyysalueen ilmaiseva aaltosulku alkaakin samalta riviltä, kuin esittelyrivi. Tämä on osa Javan koodauskäytäntöä. 

Javassa käytetään funktioiden nimeämisessä camelCasingia, eli aloitetaan pienellä kirjaimella ja sanojen vaihtuessa ensimmäinen kirjain on isolla, eli esimerkiksi: `tamaOnFunktionNimi`.

Tiedostot taas nimetään käyttäen PascalCasingia, eli samoin, kuin camelCasing, mutta myös ensimmäinen kirjain on iso. Esimerkiksi `Hei.java`

## Java ohjelmien kääntäminen ja ajaminen
Tallenna yllä oleva esimerkki tietokoneellesi tiedostonimellä Hei.java

### javac
Java on *käännettävä* ohjelmointikieli, joten lähdekoodi tulee kääntää, jotta se voidaan ajaa. 
[Tähän väliin voisi HYVIN lyhyesti selittää .java -> .class -> virtuaalikone -> konekielinen ohjelma.]
Jotta tämä prosessi olisi mahdollista, täytyy tietokoneelle asentaa Java-kehitysympäristö, joka tunnetaan nimellä *Java Development Kit* (JDK). 
Kokeillaan seuraavaksi ohjelmamme kääntämistä JDK:n sisältämällä `javac`-kääntäjäohjelmalla.

Avaa komentorivi ja siirry siihen kansioon, johon tallensit `Hei.java`-ohjelman. Kirjoita komento `javac Hei.java`.

Kääntämisen seurauksena syntyy niin sanottua *tavukoodia* sisältävä tiedosto `Hei.class`. 
Tavukoodi ei ole suoraan prosessorilla ajettava ohjelma, vaan eräänlainen välivaihe. 
Java 11:sta mukana tuli mahdollisuus kirjoittaa Javaohjelmia ilman luokkaa, niinkuin yllä olevassa esimerkissä. javac komennon jälkeen huomataan kuitenkin, että ohjelma kääritään käännettäessä silti luokkaan. Mahdollisuus tuotiin Javaan, jotta yhden tiedoston lähdekoodiohjelmat olisivat helpompia kirjoittaa.

Isommissa ohjelmissa kannattaa käyttää jotain Java-projektin hallintatyökalua, kuten Gradle/Maven. Näihin tutustutaan osassa 6. 

### java
`java` on komento, jolla ajetaan .java päätteisiä tiedostoja. Voit nyt ajaa kääntämäsi tiedoston komentorivillä ajamalla komennon `java Hei.java`. Java 11:sta jälkeen on ollut mahdollista ajaa komennolla `java` javalähdekooditiedostoja ilman, että ensin kääntää lähdekooditiedostoa Java-tavukoodiksi. Sisäisesti JVM siis tarkistaa, että onko lähdetiedosto(i)sta olemassa käännöksiä, jos ei, kääntää ja sen jälkeen ajaa saadut bittikooditiedostot. 

### jshell
jshell on interaktiivinen tulkki Javaohjelmoinnin opetteluun. Interaktiivisuus tarkoittaa, että voit kokeilla eri komentoja rivi/lohko kerrallaan ilman erillistä kääntämistä ja ajamista, luokkia tai `main`-metodia. Pääset kokeilemaan jshelliä ajamalla komennon `jshell`. Nyt voit esimerkiksi kirjoittaa komennon `IO.println("Hei maailma!");` ja painaa `Enter`, jolloin näet heti tulostuksen komentorivillä. Vastaavasti voit luoda muuttujia ja näet heti, mitä niihin on sijoitettu.

jshellistä poistutaan ajamalla komento `/exit`

### Kurssikohtaiset IntelliJ asetukset
TODO: Tähän täydentyy kurssikohtaiset asetukset IntelliJ-ideä varten

## (J)VM
JVM tulee sanoista **J**ava **V**irtual **M**achine joka tarkoittaa abstraktia virtuaalikonetta, jolla voidaan ajaa Java-tavukoodia. Hyöty on siinä, että ohjelma joka on käännetty Java-tavukoodiksi voidaan nyt ajaa alustariippumattomasti (Windows, macOS, Linux, jne.), kunhan JVM pyörii kyseisellä alustalla. Javalla onkin iskulause: "Write Once, Run Anywhere", jolla viitataan tähän periaatteeseen.

Käytetyin JVM toteutus on nimeltään HotSpot, joka sisältää sekä tulkin, että JIT (**J**ust **I**n **T**ime) kääntäjän. Tulkki käynnistää ohjelman ja JVM etsii koodista toistuvia pätkiä, jotka käännetään kyseisen alustan konekieliseksi koodiksi JIT kääntäjällä, jotta ohjelma pyörisi nopeammin. Alustakohtainen käännetty konekieli on aina nopeampi ajaa kuin tulkattava kieli. Javan tyyli käyttää sekä tulkkausta, että kääntämistä on kompromissi alustariippumattomuuden ja suoritusnopeuden välillä.

## Java I/O operaatioita
Javan IO-luokalla voidaan käyttäjältä lukea syötettä näin:

```java
void main() {
    String syote = IO.readln();
    IO.println("Kirjoitit: " + syote);
}
```

Yllä opittiinkin jo kirjoittamaan konsoliin rivinvaihdollisesti. IO-luokasta löytyy myös perinteinen `print`, joka kirjoittaa standardiin ulostuloon tekstiä ilman rivinvaihtoa. Esimerkiksi:

```java
void main() {
    IO.print("Samalle");
    IO.print(" riville");
}
```

## Kommentointi ja dokumentointi

Lähdekoodiin voi kirjoittaa tekstiä, joka ei ole varsinaista koodia, vaan selittää sitä. Tällaista selitystekstiä on kahdentyyppisiä: (1) koodin sekaan kirjoitettavia kommentteja (nimitetään näitä lyhyesti *kommenteiksi*) sekä (2) dokumentaatiokommentteja. 

Kommenttien tarkoitus on palvella *kehityksen aikaista* tekemistä. Ne näkyvät sisäisesti, eli ohjelmoijalle itselleen.  Dokumentaatiokommenttien tarkoitus on palvella kaikkia, jotka *käyttävät* koodia. Ne näkyvät paitsi ohjelmoijalle itselleen, myös niille, jotka hyödyntävät koodia esimerkiksi API:n (*application programming interface*) kautta.

### Yhden rivin kommentointi
Yhden rivin kommentteja, jonka syntaksi on `//` voidaan käyttää esimerkiksi merkitsemään TODO-kohtia koodissa.

```java
void main() {
    // TODO: Tarkista millaisia ongelmia tästä ratkaisusta voi tulla
    String syote = IO.readln();
    IO.println("Kirjoitit: " + syote);
}
```

Yleisesti hyvä periaate on se, että ohjelmoija pyrkii kirjoittamaan koodia, joka selittää itse itseään, jolloin tarvetta erityisesti yhden rivin kommentoinnille ei olisi. Tämä tarkoittaa, että muuttujat pyritään nimeämään järkevästi, jolloin yhden rivin kommentointi ei ole tarpeellista. Joskus tältä ei voi välttyä, kun ei voida olettaa jonkin operaation olevan itsestäänselvää ja muuttujan nimestä tulisi todella pitkä:

```java,editable
void main() {
    int n = 9;
    // Pyöristää alaspäin lähimpään neljällä jaolliseen lukuun
    int pyoristetty = n & ~3; 
    IO.println(pyoristetty);
}
```
Nyt muuttujan `pyoristetty` tilalla voisi olla `pyoristaaAlaspainLahimpaanNeljallaJaolliseenLukuun`, joka ei sekään ole oikein järkevä vaihtoehto.

### Monirivinen kommentti

Javassa monirivinen kommentti tulee `/*` ja  `*/` väliin. Tällaista suositellaan käytettäväksi, kun jokin monimutkaisempi logiikka vaatii tarkempaa avaamista ja/tai on järkevää selittää miksi juuri kyseinen ratkaisu on valittu. Tätä kommenteissa olevaa tarkempaa avaamista ei kuitenkaan ole tarkoitus näyttää koodin käyttäjille.

```java.ignore
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

TODO: (pitäisikö laittaa seuraava teksti johonkin huomiotaherättävämpään versioon?)
Huomaa nyt, että dokumentaatiokommentit alkavat `/**` ja päättyvät `*/`, eli ovat syntaksiltaan hyvin lähellä monirivistä kommenttia.

```java
/**
 * Laskee kahden kokonaisluvun summan.
 * 
 * @param a Ensimmäinen luku
 * @param b Toinen luku
 * @return Lukujen summa
 */
int summa(int a , int b) {
    return a + b;
}
```

Aliohjelman dokumentaatiokommentin runko syntyy automaattisesti sovelluskehittimessä, kun aliohjelman esittelyrivin yläpuolelle kirjoittaa merkit `/**` ja painaa `Enter`. 
