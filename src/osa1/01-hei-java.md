# Hei, Java!

> [!Osaamistavoitteet]
>
> - Java-kielen perusteet
> - Tiedät miten Java-ohjelma käännetään ja ajetaan (komentoriviohjelmat javac, java ja jshell, IDE-säädöt)
> - Tiedät mikä on (J)VM ja miten kääntäminen eroaa tulkkauksesta 
> - Tunnet Java-kielen vastineita yleisimmille I/O-operaatioille (tekstin tulostus, lukeminen konsolilta)

Lähteenä: https://dev.java/learn/

## Java-kielen perusteet

Tässä esimerkki, jolla kirjoitetaan konsoliin javan versio:

```java
void main() {
    var feature =  Runtime.version().feature();
    IO.println("Hei, maailma! Tässä on Java " + feature);
}
```
Mainin palautuksen tyyppinä pitää olla `void`, koska muuten se ei ole JVM:n mukaan pätevä
koodiesimerkki

Kenties ensimmäisenä Javassa C#:iin verrattuna syntaksista voidaan huomata, että uuden näkyvyysalueen ilmaiseva aaltosulku alkaakin samalta riviltä, kuin esittelyrivi. Tämä on osa Javan koodauskäytäntöä. 

Javassa käytetään funktioiden nimeämisessä Camel Casingia, eli aloitetaan pienellä kirjaimella ja sanojen vaihtuessa ensimmäinen kirjain on isolla, eli esimerkiksi: `tamaOnFunktionNimi`.

Tiedostot taas nimetään käyttäen Pascal Casingia, eli samoin, kuin Camel Casing, mutta myös ensimmäinen kirjain on iso. Esimerkiksi `Hei.java`

## Java ohjelmien kääntäminen ja ajaminen
Kirjoitetaan ensin tiedosto esimerkiksi `Hei.java`, jonka sisällöksi tulee

```java
void main() {
    var feature =  Runtime.version().feature();
    IO.println("Hei, maailma! Tässä on Java " + feature);
}
```

### javac
javac on ensisijainen javan kääntäjä, joka tulee Java Development Kit:in (JDK) mukana. Nyt voidaan kääntää aiemmin tehty tiedosto `Hei.java` ajamalla komento `javac Hei.java` Javabittikoodiksi. Javabittikoodi on eri asia kuin alustakohtainen konekieli. Voidaan huomata, että nyt kansioon on ilmestynyt tiedosto `Hei.class`. Java 11:sta mukana tuli mahdollisuus kirjoittaa Javaohjelmia ilman luokkaa, niinkuin yllä olevassa esimerkissä. javac komennon jälkeen huomataan kuitenkin, että ohjelma kääritään käännettäessä silti luokkaan. Mahdollisuus tuotiin Javaan, jotta yhden tiedoston lähdekoodiohjelmat olisivat helpompia kirjoittaa.

Isommissa ohjelmissa kannattaa käyttää jotain Java-projektin hallintatyökalua, kuten Gradle/Maven. Näihin tutustutaan osassa 6. 

### java
`java` on komento, jolla ajetaan .java päätteisiä tiedostoja. Voit nyt ajaa kääntämäsi tiedoston komentorivillä ajamalla komennon `java Hei.java`. Java 11:sta jälkeen on ollut mahdollista ajaa komennolla `java` javalähdekooditiedostoja ilman, että ensin kääntää lähdekooditiedostoa Javabittikoodiksi. Sisäisesti JVM siis tarkistaa, että onko lähdetiedosto(i)sta olemassa käännöksiä, jos ei, kääntää ja sen jälkeen ajaa saadut bittikooditiedostot. 

### jshell
jshell on interaktiivinen työkalu Javaohjelmoinnin ja prototyyppien opetteluun. Ajamalla komennon `jshell` pääset kokeilemaan eri komentoja rivi kerrallaan ilman erillistä kääntämistä ja ajamista. Voit esimerkiksi kirjoittaa komennon `IO.println("Hei maailma!");` ja painaa `Enter`, jolloin näet heti tulostuksen komentorivillä.

jshellistä poistutaan ajamalla komento `/exit`

### Kurssikohtaiset IntelliJ asetukset
TODO: Tähän täydentyy kurssikohtaiset asetukset IntelliJ-ideä varten

## (J)VM
JVM tulee sanoista **J**ava **V**irtual **M**achine joka tarkoittaa abstraktia virtuaalikonetta, jolla voidaan ajaa Javabittikoodia. Hyöty on siinä, että ohjelma joka on käännetty Javabittikoodiksi voidaan nyt ajaa alustariippumattomasti (Windows, Apple, Linux, jne.), kunhan JVM pyörii kyseisellä alustalla. Javalla onkin iskulause: "Write Once, Run Anywhere", jolla viitataan tähän periaatteeseen.

Käytetyin JVM toteutus on nimeltään HotSpot, joka sisältää sekä tulkkaajan, että JIT (**J**ust **I**n **T**ime) kääntäjän. Tulkkaaja käynnistää ohjelman ja JVM etsii koodista toistuvia pätkiä, jotka käännetään kyseisen alustan konekieliseksi koodiksi JIT kääntäjällä, jotta ohjelma pyörisi nopeammin. Alustakohtainen käännetty konekieli on aina nopeampi ajaa kuin tulkattava kieli. Javan tyyli käyttää sekä tulkkausta, että kääntämistä on kompromissi alustariippumattomuuden ja suoritusnopeuden välillä.

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