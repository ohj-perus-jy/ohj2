# Hei, Java!

> [!Osaamistavoitteet]
>
> - Java-kielen perusteet
> - Tiedät miten Java-ohjelma käännetään ja ajetaan (komentoriviohjelmat javac, java ja jshell, IDE-säädöt)
> - Tiedät mikä on (J)VM ja miten kääntäminen eroaa tulkkauksesta 
> - Tunnet Java-kielen vastineita yleisimmille I/O-operaatioille (tekstin tulostus, lukeminen konsolilta)

Lähteenä: https://dev.java/learn/

## Java-kielen perusteet

Lähdetäänpä liikkeelle esimerkillä, jossa kirjoitetaan konsoliin Javan versio.

```java
void main() {
    int versioNumero = Runtime.version().feature();
    IO.println("Hei, maailma! Tässä on Java " + versioNumero);
}
```
Käydään tämä esimerkki paloittain läpi. 

```java.ignore
void main() { ...
```

Kaikissa Java-ohjelmissa tulee olla `main`-metodi, joka toimii ohjelman aloituspisteenä. Pääohjelman palautuksen tyyppinä tulee olla `void`, eli pääohjelma ei palauta mitään. Nyt pääohjelma ei ota vastaan parametreja, joten jätetään sulut tyhjäksi. 

```java.ignore
int versioNumero = Runtime.version().feature();
```
Tällä rivillä otetaan kokonaislukutyyppiseen muuttujaan `int` talteen Javan ajonaikainen versionumero.

```java.ignore
IO.println("Hei, maailma! Tässä on Java " + versioNumero);
```
Tulostetaan konsoliin teksti ja versionumero

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

```java
// Tämä on yhden rivin kommentti

/*
 * Tämä on usean rivin
 * kommentti
 */

//Esimerkki dokumentaatiosta
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

Dokumentaatiorungon saa aliohjelmalle, kun kirjoittaa `/**` aliohjelman esittelyrivin yhtä ylemmälle riville ja painaa `Enter` IntelliJ:ssä
