# Muuttujat ja tietotyypit

> [!Osaamistavoitteet]
>
> - Kerrataan lyhyesti rakenteisen ohjelmoinnin perusteet
> - Muuttujat ja vakiot (perustyypit, `final`, String)

## Rakenteisesta ohjelmoinnista
- Rakenteinen ohjelmointi on ohjelmointiparadigma joka painottaa ohjelman hajottamista lohkoihin, jotta ohjelman järjestyslogiikkaa on helpompi ymmärtää. 
- Syntyi alun perin poistamaan tarpeen `goto`-lauseille
- Pitäisiköhän olla jokin abstrakti versio siitä, mitä rakenteisella ohjelmoinnilla haetaan ja sen jälkeen jokin pieni koodiesimerkki? Pitäisikö koodiesimerkki olla pseudokoodia vai ei?

## Bool
```java
void main() {
    boolean totta = true;
    IO.println(Boolean.toString(totta));
}
```

## Merkkijonot

- `String`
- `StringBuilder` (kannattaako edes käyttää?)
- `StringBuffer`
- `CharBuffer`
- `Segment`

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

## Numeeriset muuttujat

Javassa on seuraavat C#:stakin tutut muuttujatyypit:

- `Byte`
- `Short`
- `Int`
- `Long`
- `Float`
- `Double`

```java
void main() {
    byte tavu = Byte.MAX_VALUE;
    short kaksiTavua = Short.MAX_VALUE;
    IO.println(tavu);
    IO.println(kaksiTavua);
}
```

Pitäisikö mainita myös muita, kuten `LongAccumulator` dokumentaatiosta: https://docs.oracle.com/javase/8/docs/api/java/lang/Number.html ?

## Vakiot
Vakiot esitellään javassa käyttäen avainsanaa `final` ja tyyliin kuuluu, että kaikki kirjaimet kirjoitetaan isolla ja sanat erotellaan toisistaan alaviivalla. Esimerkiksi;

```java.ignore
final int PAIVIA_VIIKOSSA = 7;
```