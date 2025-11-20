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

Kullekin Javan primitiivitietotyypille (TODO: Vai perustietotyyppi) on olemassa niin sanottu käärijäluokka. Kokonaislukutyypin `int` käärijäluokka on `Integer`, `char`-tyypin käärijäluokka on `Character`. Muut käärijäluokat ovat saman nimisiä kuin primitiivityypit, mutta alkavat isolla kirjaimella, esimerkiksi `Double`, `Boolean` jne. Käärijäluokasta löytyy hyödyllisiä metodeja, kuten `toString()` sekä vakioita, kuten `MAX_VALUE` primitiivityyppien käsittelyyn.

TODO: Lyhyt esimerkki käärijäluokan käytöstä.

## Numeeriset tietotyypit

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

Numeroliteraalin tyypin saa vaihdettua 
```java
void main() {
    double desimaali = (double)1/3;
    System.out.format("1/3 on desimaalilukuna %.3f%n",desimaali);
    int leikattu = (int)1.3;
    IO.println(leikattu);
    Double kaaritty = desimaali;
    int kokonaislukuna = kaaritty.intValue();
    IO.println(kokonaislukuna);
}
```

## Yksittäinen merkki ja merkkijonot

- `char`
- `String`
- `StringBuilder`

### char
Javassa voit luoda yksittäisiä merkkejä avainsanan `char` avulla: 

```java
void main() {
    char tabulaattoriMerkki = '\u0009';
    IO.println(Character.isWhitespace(tabulaattoriMerkki));
}
```


### String
TODO: Joitain yleisimpiä esimerkkejä String-luokan metodeista?

```java
void main() {
    String muuttumaton = "Tämä on muuttumaton";
    IO.println(muuttumaton);
    muuttumaton.concat(" merkkijono.");
    IO.println(muuttumaton);
}
```

Ylemmässä esimerkissä metodi `.concat()` luo uuden merkkijonon, jota ei nyt tallenneta mihinkään.

Huomaa, että Javassa, jos halutaan tarkastella tiettyä kirjainta merkkijonossa, se tapahtuu seuraavasti:

```java
void main() {
    String mjono = "esimerkki";
    IO.println(mjono.charAt(0));
    IO.println(mjono[0]);
}
```

### StringBuilder
Jos tarvitsee muunneltavan merkkijonon, käytä StringBuilderia:

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

## boolean
Binäärisen muuttujan saa javassa avainsanalla `boolean` ja jonka arvo on joko `true` tai `false`

```java
void main() {
    boolean totta = true;
    String mjonona = Boolean.toString(totta);
    IO.println(mjonona.charAt(0));
}
```

Javan dokumentaatiosta löytyy myös esimerkkejä muista perustietotyypeistä, joita on tarjolla Javassa: https://docs.oracle.com/javase/8/docs/api/java/lang/Number.html ?


## Taulukot
TODO: mitä käytetään (sulut, [], {}?) merkitsemään, että jokin pitää vaihtaa johonkin arvoon?

Javan taulukot esitellään syntaksilla 
```java.ignore
Tyyppi[] nimi = new Tyyppi[koko];
```
Tai jos sisältö on jo tiedossa taulukkoa luotaessa, niin esimerkiksi kokonaislukutaulukon voi alustaa suoraan aaltosulkeiden sisään.

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

## Vakiot
Muuttuja, jolle voi sijoittaa arvon vain alustuksen yhteydessä esitellään käyttäen `final`-avainsanaa. Javan koodauskäytänteisiin kuuluu, että `final`-muuttujat kirjoitetaan suuraakkosin ja sanat erotellaan toisistaan alaviivalla.

```java.ignore
final int PAIVIA_VIIKOSSA = 7;
```