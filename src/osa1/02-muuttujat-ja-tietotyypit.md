# Muuttujat ja tietotyypit

> [!Osaamistavoitteet]
>
> - Kerrataan lyhyesti rakenteisen ohjelmoinnin perusteet
> - Muuttujat ja vakiot (perustyypit, `final`, String)

## Rakenteisesta ohjelmoinnista
- Rakenteinen ohjelmointi on ohjelmointiparadigma joka painottaa ohjelman hajottamista lohkoihin, jotta ohjelman järjestyslogiikkaa on helpompi ymmärtää. 
- Syntyi alun perin poistamaan tarpeen `goto` -lauseille
- TODO: Pitäisiköhän olla jokin abstrakti versio siitä, mitä rakenteisella ohjelmoinnilla haetaan ja sen jälkeen jokin pieni koodiesimerkki? Pitäisikö koodiesimerkki olla pseudokoodia vai ei?

## Javan alkeistietotyypeistä

Kullekin Javan alkeistietotyypille (engl. *primitive data types*) on olemassa niin sanottu käärijäluokka (engl. *wrapper class*). Kokonaislukutyypin `int` käärijäluokka on `Integer`, `char`-tyypin käärijäluokka on `Character`. Muut käärijäluokat ovat saman nimisiä kuin alkeistietotyypit, mutta alkavat isolla kirjaimella, esimerkiksi `Double`, `Boolean` jne. Käärijäluokasta löytyy hyödyllisiä metodeja, kuten `toString()` sekä vakioita, kuten `MAX_VALUE` alkeistietotyyppien käsittelyyn.

Java käyttää staattista tyypitystä, eli muuttujan ja olion tyyppi tarkistetaan käännöshetkellä. Lisäksi Java on vahvasti tyypitetty, joten eri tyyppisiä arvoja ei voi sekoittaa tai muuntaa toiseksi ilman nimenomaista ja turvallista tyyppimuunnosta.

```java
void main() {
    byte tavu = Byte.MAX_VALUE;
    short kaksiTavua = Short.MAX_VALUE;
    IO.println(tavu);
    IO.println(kaksiTavua);
    IO.println(Short.toString(kaksiTavua).charAt(0));
}
```

Tässä käytetään tietotyypin käärijäluokassa olevaa vakiota MAX_VALUE ja muunnetaan käärijäluokan avulla muuttujan `kaksiTavua` ensin merkkijonoksi ja sen jälkeen tulostetaan merkkijonon ensimmäinen merkki.

## Numeeriset tietotyypit

Javassa on seuraavat C#:stakin tutut numeeriset muuttujatyypit:

- `int`
- `long`
- `float`
- `double`

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

Javasta löytyy myös enemmän [numeerisia](https://docs.oracle.com/javase/8/docs/api/java/lang/Number.html) tietotyyppejä, mutta tällä kurssilla et (välttämättä) tarvitse muita kuin yllä mainittuja.

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

TODO: esimerkkejä hyödyllisistä char-luokan metodeista


### String

Monissa kielissä merkkijono on muuttumaton muistin tehokkuuden, säikeiden turvallisuuden ja paremman suorituskyvyn takia. Myös Javassa `String` on muuttumaton, eli jos jos yrität suorittaa jonkin operaation merkkijonolle, saat tulokseksi uuden merkkijonon, eikä alkuperäinen merkkijono täten muuttunut. Katsotaan tästä esimerkki:

```java
void main() {
    String muuttumaton = "Tämä on muuttumaton";
    IO.println(muuttumaton);
    muuttumaton.concat(" merkkijono.");
    IO.println(muuttumaton);
}
```

Esimerkissä metodi `concat()` luo uuden merkkijonon, jota ei nyt tallenneta mihinkään.

Javassa, jos halutaan tarkastella tiettyä kirjainta merkkijonossa, se tapahtuu seuraavasti:

```java
void main() {
    String mjono = "esimerkki";
    IO.println(mjono.charAt(0));
    IO.println(mjono[0]);
}
```

TODO: Joitain yleisimpiä esimerkkejä String-luokan metodeista?

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

TODO: StringBuilderin hyödyllisiä metodeja

## boolean
Binääristä `boolean` -muuttujaa käytetään merkityksen selkeyttämiseen, vähentämään virheitä, luettavuuden parantamiseen, optimisaatioon, automaattisia työkaluja varten ja ovat luonnollinen tapa esittää binäärisiä tiloja. Esimerkiksi jokin on päällä tai pois päältä.

Binäärisen muuttujan saa javassa avainsanalla `boolean` ja jonka arvo on joko `true` tai `false`

```java
void main() {
    boolean totta = true;
    String mjonona = Boolean.toString(totta);
    IO.println(mjonona.charAt(0));
}
```

Klassinen esimerkki `boolean` -muuttujien käytöstä jossain ohjelmassa:

```java
boolean ohjelmaOnPaalla = true;

while (ohjelmaOnPaalla) {
    // Tehdään ohjelmaan liittyviä asioita
    if (/* Jokin lopettamiseen liittyvä ehto */) {
        ohjelmaOnPaalla = false;
    }
}
```

## Muut perustietotyypit

Javan dokumentaatiosta löytyy myös esimerkkejä [muista perustietotyypeistä](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html), joita on tarjolla Javassa.


## Taulukot

Taulukkoja käytetään tallentamaan joukkoa samantyyppisiä alkioita muuttujaan, joka helpottaa datan tehokasta hallintaa ja organisointia.  

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

Java täyttää taulukon oletusarvoilla riippuen taulukon tyypistä. Voit alla olevassa TODO: (ikkunassa)? kokeilla mitkä ovat kunkin taulukkotyypin oletusarvot vaihtamalla `char` tilalle esimerkiksi `int` tai `double`. 

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

Vakioita tarvitaan mm. koodin lukemisen helpottamiseksi, toisteisen koodin vähentämiseksi, luotettavuuden parantamiseksi, parantamaan suorituskykyä jne. Kuvitellaan, että olet luomassa jotain järjestelmää, jossa tarvitaan tietokantayhteyttä ja saat kehittäessä virheen `2001`. Mitä sen olisi tarkoitus tarkoittaa? Oletetaan nyt, että joku on ajatellut asiaa etukäteen ja nimennyt virhekoodin järkevästi. Käyt lukemassa koodipohjaa ja löydät sieltä rivin:

```java.ignore
final int VIRHE_TIETOKANTAYHTEYDESSA = 2001;
```

Nyt on selvää, että kyseessä on nimenomaan virhe tietokantayhteydessä, eikä jokin muu virhe. Toisaalta ehkä koodipohjassa on useampi tilanne, jossa halutaan käyttää kyseistä virhettä. Ei olisi fiksua käyttää literaalia `2001`.