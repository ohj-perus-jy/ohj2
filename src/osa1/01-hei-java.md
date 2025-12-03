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

1. Java-ohjeman suoritus alkaa `main`-nimisestä aliohjelmasta. `void` tarkoittaa, että aliohjelma ei palauta mitään arvoja. Koska pääohjelma ei ota parametreja, sulut voidaan jättää tyhjäksi. Javassa samalla rivillä aloitetaan myös aliohjelman runko aaltosululla`{`.

2. Javassa lause loppuu yleensä puolipisteeseen `;`. Tekstin tulostaminen onnistuu `IO.println`-metodilla.

3. Aliohjelman runko lopetetaan aaltosululla `}`.

## Javan koodauskäytänteistä

Tässä olennaisimmat Javan koodauskäytänteet, joita on hyvä pitää mielessä:

- Aliohjelman runkoa aloittava aaltosulku `{` laitetaan yleensä samalle riville kuin aliohjelman määrittely. Sama pätee muille rakenteille, jossa käytetään aaltosulkuja, kuten `if`-, `for`-, `while` ja `do-while` -rakenteille.

- Aliohjelmien nimeämisessä käytetään camelCasing-tyyliä, eli ensimmäinen kirjain on pienellä ja seuraavat sanat aloitetaan isolla kirjaimella. Esimerkiksi `tamaOnFunktionNimi`. Samaa tyyliä käytetään myös muuttujien nimeämisessä.

- Tiedostot ja myöhemmin kurssilla käytettävät luokat, rajapinnat ja listaukset nimitetään PascalCasing-tyylillä, Esimerkiksi `HeiMaailma.java`, (TODO: vaihda enum esimerkki kurssilla esitellyyn) `public class Opiskelija {...`, `public interface Saadettava {...` tai `public enum Viikonpaiva { ...`.

### Kurssikohtaiset IntelliJ asetukset
TODO: Tähän täydentyy kurssikohtaiset asetukset IntelliJ-ideä varten

## Java ohjelmien kääntäminen ja ajaminen
Tallenna yllä oleva esimerkki tietokoneellesi tiedostonimellä Hei.java

### java
`java` on komento, jolla ajetaan .java päätteisiä tiedostoja. Voit nyt ajaa kääntämäsi tiedoston komentorivillä ajamalla komennon `java Hei.java`. Java 11:sta jälkeen on ollut mahdollista ajaa komennolla `java` javalähdekooditiedostoja ilman, että ensin kääntää lähdekooditiedostoa Java-tavukoodiksi. Sisäisesti JVM siis tarkistaa, että onko lähdetiedosto(i)sta olemassa käännöksiä, jos ei, kääntää ja sen jälkeen ajaa saadut bittikooditiedostot. 

### jshell
jshell on interaktiivinen tulkki Javaohjelmoinnin opetteluun. Interaktiivisuus tarkoittaa, että voit kokeilla eri komentoja rivi/lohko kerrallaan ilman erillistä kääntämistä ja ajamista, luokkia tai `main`-metodia. Pääset kokeilemaan jshelliä ajamalla komennon `jshell`. Nyt voit esimerkiksi kirjoittaa komennon `IO.println("Hei maailma!");` ja painaa `Enter`, jolloin näet heti tulostuksen komentorivillä. Vastaavasti voit luoda muuttujia ja näet heti, mitä niihin on sijoitettu.

jshellistä poistutaan ajamalla komento `/exit`

<details closed><summary>Extra: javac </summary>
Java on <i>käännettävä</i> ohjelmointikieli, joten lähdekoodi tulee kääntää, jotta se voidaan ajaa.

Jotta tämä prosessi olisi mahdollista, täytyy tietokoneelle asentaa Java-kehitysympäristö, joka tunnetaan nimellä <i>Java Development Kit</i> (JDK). 
Kokeillaan seuraavaksi ohjelmamme kääntämistä JDK:n sisältämällä <code>javac</code> -kääntäjäohjelmalla.

Avaa komentorivi ja siirry siihen kansioon, johon tallensit <code>Hei.java</code>-ohjelman. Kirjoita komento <code>javac Hei.java</code>.

Kääntämisen seurauksena syntyy niin sanottua *tavukoodia* sisältävä tiedosto <code>Hei.class</code>. 
Tavukoodi ei ole suoraan prosessorilla ajettava ohjelma, vaan eräänlainen välivaihe. 
Java 11:sta mukana tuli mahdollisuus kirjoittaa Javaohjelmia ilman luokkaa, niinkuin yllä olevassa esimerkissä. javac komennon jälkeen huomataan kuitenkin, että ohjelma kääritään käännettäessä silti luokkaan. Mahdollisuus tuotiin Javaan, jotta yhden tiedoston lähdekoodiohjelmat olisivat helpompia kirjoittaa.

Isommissa Java-ohjelmissa käytetään usein myös erillisiä hallintatyökaluja, kuten
Gradle tai Maven. Näihin tutustutaan osassa 6 (TODO: Linkki?).

</details>

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
Yhden rivin kommentteja, jonka syntaksi on `//` voidaan käyttää esimerkiksi merkitsemään TODO-kohtia koodissa:

```java
void main() {
    // TODO: Tarkista millaisia ongelmia tästä ratkaisusta voi tulla
    String syote = IO.readln();
    IO.println("Kirjoitit: " + syote);
}
```

Yleisesti hyvä periaate on se, että ohjelmoija pyrkii kirjoittamaan koodia, joka selittää itse itseään. Tällöin asiat, jotka voidaan nimetä (kuten muuttujat, luokat, funktiot), pyritään nimeämään mahdollisimman kuvaavasti, jolloin yksittäisten rivien kommentointi ei välttämättä ole tarpeen. Joskus tältä ei voi välttyä, koska jotakin operaatiota ei voida olettaa itsestäänselväksi tai muuttujan nimestä tulisi kohtuuttoman pitkä:

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

> [!Huomautus]
> Dokumentaatiokommentit alkavat `/**` ja päättyvät `*/`, eli ovat syntaksiltaan hyvin lähellä monirivistä kommenttia.

```java
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

Aliohjelman dokumentaatiokommentin runko syntyy automaattisesti sovelluskehittimessä, kun aliohjelman esittelyrivin yläpuolelle kirjoittaa merkit `/**` ja painaa `Enter`. 

<details closed><summary>Extra: miltä Javan dokumentaatio näyttää? </summary>
Oletetaan nyt, että tallennat ylläolevan tiedostoon <code>Summa.java</code> ja ajat sen jälkeen komennon <code>javadoc Summa.java</code>. Nyt voit avata luodun <code>index.html</code> -tiedoston selaimessa, klikata selaimessa luokkaa <code>Summa</code> ja pääset seuraavanlaiseen näkymään:

![Juuri tehdystä dokumentaatiosta kuva, joka voi näyttää tutulta jos on käynyt tutkimassa Javan omaa dokumentaatiota ](images/summaDokumentaatio.png)

Näyttääkö tutulta? Vertaa esimerkiksi [Javan dokumentaatioon IO-luokasta](https://docs.oracle.com/javase/8/docs/api/java/lang/Object.html)
</details>