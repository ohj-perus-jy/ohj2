# Muuttujat ja tietotyypit

> [!Osaamistavoitteet]
>
> - Kerrataan lyhyesti rakenteisen ohjelmoinnin perusteet
> - Muuttujat ja vakiot (perustyypit, `final`, String)

## Rakenteisesta ohjelmoinnista
- Rakenteinen ohjelmointi on ohjelmointiparadigma, joka painottaa ohjelman hajottamista lohkoihin, jotta ohjelman järjestyslogiikkaa on helpompi ymmärtää. Tätä olet jo oppinut ohjelmointi 1 -kurssilla.
- Rakenteinen ohjelmointiparadigma syntyi alun perin poistamaan tarpeen `goto` -lauseille, joista lisää kurssilla "ITKA2030 Käyttöjärjestelmien ja pilvipalveluiden perusteet"

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

Javassa on seuraavat tutut numeeriset muuttujatyypit:

- `int` $\in$[$-2^{31}, 2^{31}-1$]
- `long` $\in$[$-2^{63}, 2^{63}-1$]
- `float` IEEE 754 yksinkertainen tarkkuus (TODO: vai pitäisikö jättää mainitsematta?)
- `double` IEEE 754 kaksinkertainen tarkkuus

Javassa numeeriset alkeistietotyypit ovat aina etumerkillisiä, eli niistä jokaisella pystyy esittämään myös negatiivisia lukuja. Lisäksi ne ovat kahden komplementteja, eli ylivuodossa pyörähdetään lukuvälin ympäri. Havainnoidaan näitä esimerkillä: (TODO: KA hyvä esimerkki vai ei?)

```java
void main() {
    int maksimi = Integer.MAX_VALUE;
    IO.println(maksimi + " On suurin luku, jonka voi tallettaa int tyyppiseen muuttujaan" );
    int ylivuoto = Integer.MAX_VALUE + 1;
    IO.println(ylivuoto + " Tapahtui ylivuoto");
    int n = 2;
    int keskiarvo = (ylivuoto) / n;
    IO.println(keskiarvo + " Saatiin, vaikka odotettiin lukua 1073741824");
}
```
Huomataan nyt, että kun yritettiin sijoittaa `int` -tyyppiseen muuttujaan `ylivuoto` yhtä suurempi kokonaisluku kuin mitä Javassa 32-bittisellä kokonaisluvulla pystytään esittämään, päädyttiin lukuun `Integer.MIN_VALUE` $= -2147483648 = -2^{31}$.

Koska Java käyttää IEEE 754 standardia desimaalilukujen`double` ja `float` esittämiseen, niillä on muutama mielenkiintoinen ja kenties yllättävä ominaisuus:

```java
void main() {
    float negatiivinenAarettomyys = -1.0f / 0.0f;
    IO.println(negatiivinenAarettomyys);
    double positiivinenAarettomyys = 1.0 / 0.0;
    IO.println(positiivinenAarettomyys);
    double nan = 0.0 / 0.0;
    IO.println(nan);
}
```

Eli desimaaliluvuille on erikseen määritelty $-\infty, \infty$ ja `NaN` = **N**ot **A** **N**umber. Huomaa myös, että jos haluat erikseen `float` tyyppisen desimaaliluvun, luvun perässä pitää olla `f`. Muutoin se tulkitaan `double`ksi.

```java,editable
void main() {
    long neljakymmentaMiljardia = 40000000000L;
    IO.println(neljakymmentaMiljardia);
    int inttina = (int)neljakymmentaMiljardia;
    IO.println(inttina);
}
```
Huomaa, että Java tulkitsee luvun `40 000 000 000` (neljäkymmentä miljardia) `int` -tyyppisenä, jos luvun perässä ei ole isoa `L` -kirjainta, eikä koodi tällöin edes käänny. 

Nyt `40 000 000 000` (neljäkymmentä miljardia) on binäärilukuna tavun kokoisiin pätkiin jaoteltuna `00001001 01010000 00101111 10010000 00000000`. 

| Tyyppi | 5        | 4        | 3        | 2        | 1        |
| ------ | -------- | -------- | -------- | -------- | -------- |
| long   | 00001001 | 01010000 | 00101111 | 10010000 | 00000000 |
| int    |          | 01010000 | 00101111 | 10010000 | 00000000 |

Ylläolevasta taulukosta huomataan, että kun `40 000 000 000` muunnetaan `int` -tyyppiseksi kokonaisluvuksi, siitä huomioidaan vain neljä ensimmäistä tavua oikealta laskettuna, eli `01010000 00101111 10010000 00000000` = 1345294336
```java
//-void main() {
double desimaali = (double)1/3;
System.out.format("1/3 on desimaalilukuna %.3f%n",desimaali);
int leikattu = (int)1.3;
IO.println(leikattu);
Double kaaritty = desimaali;
int kokonaislukuna = kaaritty.intValue();
IO.println(kokonaislukuna);
//-}
```

Javasta löytyy myös enemmän [numeerisia](https://docs.oracle.com/javase/8/docs/api/java/lang/Number.html) tietotyyppejä, mutta tällä kurssilla riittänevät käytännössä `int` ja `double`. Hyvin isoja kokonaislukuja varten on tarjolla [`BigInteger`](https://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html) ja hyvin tarkkoja desimaalilukuja varten [`BigDecimal`](https://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html), mutta niitä tuskin tällä opintojaksolla tarvitsemme. 

## Yksittäinen merkki ja merkkijonot

Javan merkkijonotyyppejä ovat `String` ja `StringBuilder`, joista kumpikin koostuu `char`-tyyppisistä merkeistä. 

### char

Sisäisesti Javassa yksittäiset merkit `char` ovat 16-bittisiä luonnollisia lukuja (välillä [0-65535]). Tätä voidaan havainnoida esimerkiksi seuraavasti:

```java
void main() {
    IO.println((int)'A'); //Muunnetaan merkki A kokonaisluvuksi
    IO.println((char)65535); //Muunnetaan kokonaisluku merkiksi
}
```
Javassa `char` on yksittäinen 16-bittinen Unicode-merkki, joita käytetään tyypillisesti yksittäisen merkin tallentamiseen muuttujaan tai kun tarkastelet merkkijonoa merkki kerrallaan 

```java
//-void main() {
char tabulaattoriMerkki = '\u0009';
IO.println(Character.isWhitespace(tabulaattoriMerkki));
//-}
```

Aritmeettiset operaatiot ovat Javassa mahdollisia `char` -tyypille:
```java
void main() {
    char a = 'A';
    IO.println(Character(a + 1));
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

Entä jos sinun tarvitsee kuitenkin tulostaa merkkejä, jotka eivät mahdu yhteen 16-bittiseen `char` muuttujaan?
```java
void main() {
    IO.println("\uD83D\uDE00");
    // Tai vaihtoehtoisesti:
    IO.println(new String(Character.toChars(0x1F600)));
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

Nyt on selvää, että kyseessä on nimenomaan virhe tietokantayhteydessä, eikä jokin muu virhe. Toisaalta ehkä koodipohjassa on useampi tilanne, jossa halutaan käyttää kyseistä virhettä. Ei olisi fiksua käyttää literaalia `2001` (TODO: Onko tämä oikea ongelma, koska säännölliset lausekkeet?).