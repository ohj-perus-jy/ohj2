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
import static java.lang.System.out;

public static void main() {
    var feature =  Runtime.version().feature();
    out.println("Hei, maailma! Tässä on Java " + feature);
}
```

Javassa käytetään funktioiden nimeämisessä Camel Casingia, eli aloitetaan pienellä kirjaimella ja sanojen vaihtuessa ensimmäinen kirjain on isolla, eli esimerkiksi: tamaOnFunktionNimi.

Pitäisikö mainita siitä, että miten javan main eroaa monesta muusta kielestä?

- JVM selitystä
- Miten main toimii, eli että pitää olla nimenomaan public static void main()
- Ei voi olla `private`, koska muutoin JVM ei löydä mainia
- Ei voi olla `static`, koska JVM kutsuu sitä, luomatta oliota
- Palautuksen tyyppinä pitää olla `void`, koska muuten se ei ole JVM:n mukaan pätevä
Koodiesimerkki

## Java ohjelmien kääntäminen ja ajaminen

### javac
javac on ensisijainen javan kääntäjä, joka tulee Java Development Kit:in (JDK) mukana. 

### java
java on javaohjelmien lähdekooditiedoston tiedostotyyppi.

### jshell
Jshell on interaktiivinen työkalu Javaohjelmoinnin ja prototyyppien opetteluun.

### Kurssikohtaiset IntelliJ asetukset
Tähän täydentyy kurssikohtaiset asetukset IntelliJ-ideä varten

## (J)VM
- Miten java toimii
- Kääntäminen vs. tulkkaus

## Java I/O operaatioita
Täydentyy
