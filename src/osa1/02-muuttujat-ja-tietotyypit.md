# Muuttujat ja tietotyypit

> [!Osaamistavoitteet]
>
> - Kerrataan lyhyesti rakenteisen ohjelmoinnin perusteet
> - Muuttujat ja vakiot (perustyypit, `final`, String)

## Rakenteisesta ohjelmoinnista
- Rakenteinen ohjelmointi on ohjelmointiparadigma joka painottaa ohjelman hajottamista lohkoihin, jotta ohjelman järjestyslogiikkaa on helpompi ymmärtää. 
- Syntyi alun perin poistamaan tarpeen `goto`-lauseille
- TODO: Pitäisiköhän olla jokin abstrakti versio siitä, mitä rakenteisella ohjelmoinnilla haetaan ja sen jälkeen jokin pieni koodiesimerkki? Pitäisikö koodiesimerkki olla pseudokoodia vai ei?

## Javan perustietotyypeistä
Kullekin Javan perustietotyypeistä on olemassa käärijäluokka, joka on nimeltään sama kuin tyypin nimi, mutta isolla kirjaimella. Poikkeuksena `int`, jonka käärijäluokka on `Integer`.

## boolean
Binäärisen muuttujan saa javassa avainsanalla `boolean` ja jonka arvo on joko `true` tai `false`

```java
void main() {
    boolean totta = true;
    String mjonona = Boolean.toString(totta);
    IO.println(mjonona[0]);
}
```

## Numeeriset muuttujat

Javassa on seuraavat C#:stakin tutut numeeriset muuttujatyypit:

- `int`
- `long`
- `float`
- `double`

```java
void main() {
    byte tavu = Byte.MAX_VALUE;
    short kaksiTavua = Short.MAX_VALUE;
    IO.println(tavu);
    IO.println(kaksiTavua);
}
```

Javan dokumentaatiosta löytyy myös esimerkkejä muista perustietotyypeistä, joita on tarjolla Javassa: https://docs.oracle.com/javase/8/docs/api/java/lang/Number.html ?


## Taulukot
TODO: mitä käytetään (sulut, [], {}?) merkitsemään, että jokin pitää vaihtaa johonkin arvoon?

Javan taulukot esitellään syntaksilla 
```java.ignore
(tyyppi)[] (nimi) = new (tyyppi)[(koko)];
```
Tai jos sisältö on jo tiedossa taulukkoa luotaessa, niin esimerkiksi kokonaislukutaulukon voi alustaa suoraan syntaksilla

```java.ignore
void main () {
    int[] luvut = {1,2,3,4};
}
```

Java täyttää taulukon oletusarvoilla riippuen taulukon tyypistä. Voit alla olevassa TODO: (ikkunassa)? kokeilla mitkä ovat kunkin taulukkotyypin oletusarvot. 

```java,editable
void main () {
    char[] luvut = new char[4];
    luvut[0] = 'a';
    IO.println(luvut[0]);
    IO.println(luvut[1]);
}
```

## Yksittäinen merkki ja merkkijonot

- `char`
- `String`
- `StringBuilder`

## char

## String
Jotain esimerkkejä String-luokan metodeista?

```java
void main() {
    String muuttumaton = "Tämä on muuttumaton";
    IO.println(muuttumaton);
    muuttumaton.concat(" merkkijono.");
    IO.println(muuttumaton);
}
```

Ylemmässä esimerkissä metodi `.concat()` luo uuden merkkijonon, jota ei nyt tallenneta mihinkään.

Javassa, jos halutaan tarkastella tiettyä kirjainta merkkijonossa, se tapahtuu seuraavasti:

```java
void main() {
    String mjono = "esimerkki";
    IO.println(mjono.charAt(0));
}
```

## StringBuilder

```java
void main() {
    Byte tavu;
    IO.println(tavu);
    StringBuilder muuttuva = new StringBuilder("Tämä on muuttuva");
    IO.println(muuttuva);
    muuttuva.append(" merkkijono.");
    IO.println(muuttuva);
}
```

## Vakiot
Vakiot esitellään javassa käyttäen avainsanaa `final` ja tyyliin kuuluu, että kaikki kirjaimet kirjoitetaan isolla ja sanat erotellaan toisistaan alaviivalla. Esimerkiksi;

```java.ignore
final int PAIVIA_VIIKOSSA = 7;
```