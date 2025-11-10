# Hei, Java!

> [!Osaamistavoitteet]
>
> - Java-kielen perusteet
> - Tiedät miten Java-ohjelma käännetään ja ajetaan (komentoriviohjelmat javac, java ja jshell, IDE-säädöt)
> - Tiedät mikä on (J)VM ja miten kääntäminen eroaa tulkkauksesta 
> - Tunnet Java-kielen vastineita yleisimmille I/O-operaatioille (tekstin tulostus, lukeminen konsolilta)

## Java-kielen perusteet

Tässä esimerkki, miten Javalla voidaan kirjoittaa konsoliin:

```java
public static void main() {
    var feature =  Runtime.version().feature();
    IO.println("Hei, maailma! Tässä on Java " + feature);
}
```

Javassa käytetään funktioiden nimeämisessä Camel Casingia, eli aloitetaan pienellä kirjaimella ja sanojen vaihtuessa ensimmäinen kirjain on isolla, eli esimerkiksi: tamaOnFunktionNimi.

Maininta siitä, että nykyään voidaan kirjoittaa Javaa luokattomasti?

- Main selitystä:
- Miten main toimii, eli että pitää olla nimenomaan public static void main()
- Ei voi olla `private`, koska muutoin JVM ei löydä mainia
- Ei voi olla `static`, koska JVM kutsuu sitä, luomatta oliota
- Palautuksen tyyppinä pitää olla `void`, koska muuten se ei ole JVM:n mukaan pätevä
Koodiesimerkki

## Java ohjelmien kääntäminen ja ajaminen
Kirjoitetaan ensin tiedosto esimerkiksi `hei.java`, jonka sisällöksi tulee

```java
public static void main() {
    var feature =  Runtime.version().feature();
    IO.println("Hei, maailma! Tässä on Java " + feature);
}
```

### javac
javac on ensisijainen javan kääntäjä, joka tulee Java Development Kit:in (JDK) mukana. Nyt voidaan kääntää aiemmin tehty tiedosto `hei.java` ajamalla komento `javac hei.java`. Voidaan huomata, että nyt kansioon on ilmestynyt tiedosto `hei.class`

### java
java on komento, jolla ajetaan .java päätteisiä tiedostoja. Voit nyt ajaa kääntämäsi tiedoston ajamalla komennon `java hei.java`.

### jshell
Jshell on interaktiivinen työkalu Javaohjelmoinnin ja prototyyppien opetteluun.

### Kurssikohtaiset IntelliJ asetukset
Tähän täydentyy kurssikohtaiset asetukset IntelliJ-ideä varten

## (J)VM
JVM tulee sanoista **J**ava **V**irtual **M**achine joka tarkoittaa abstraktia virtuaalikonetta, jo
- Miten java toimii
- Kääntäminen vs. tulkkaus

## Java I/O operaatioita
Täydentyy

Javan IO-luokalla voidaan käyttäjältä lukea syötettä näin:

```java
public static void main() {
        String syote = IO.readln();
        IO.println("Kirjoitit: " + syote);
}
```