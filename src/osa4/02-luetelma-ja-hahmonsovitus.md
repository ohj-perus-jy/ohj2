# Luetelma ja hahmonsovitus

> [!Osaamistavoitteet]
>
> - Tiedät mikä on luetelma tyyppinä ja ymmärrät sen hyödyt
> - Tiedät mitä on hahmonsovitus ja milloin sitä kannattaa käyttää

## Luetelma rajatuille joukoille

Luetelma (eng. enum/enumeration) on erityinen tyyppi, jolla voidaan rajoittaa muuttujan arvoja tiettyyn, ennalta määrättyyn arvojoukkoon. Usein mainittuja hyviä esimerkkejä luetelmille ovat viikonpäivät tai ilmansuunnat, jotka tunnetusti ovat hyvin määritettyä pieniä joukkoja. Luetelman ei tarvitse kuitenkaan vastata yleisesti tunnettua käsitettä. Olennaista on voida olettaa luetelman arvojoukon pysyvän samana, eli vakiona, koko ohjelman käytön ajan.

Jatketaan edellisen osan `Kerailykortti`-luokalla. Katsotaan nyt tapausta, jossa meillä on tiedot `nimi` ja `tunnistenumero`, sekä näiden lisäksi `harvinaisuusaste`, jonka tarkoitus on kertoa esimerkiksi millä todennäköisyydellä kortin voi löytää keräilypakasta. Sovitaan, että meillä on viisi harvinaisuusastetta, joista 1 on yleisin ja 5 harvinaisin.

```java
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private int tunnistenumero;
    private int harvinaisuusaste; // 1-5

    public Kerailykortti(String nimi, int tunnistenumero, int harvinaisuusaste) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
        this.harvinaisuusaste = harvinaisuusaste;
    }

    @Override
    public String toString() {
        return String.format("#%s %s [%d]", tunnistenumero, nimi, harvinaisuusaste);
    }
}
// FILE_END
// FILE: main.java
void main() {
    Kerailykortti kortti1 = new Kerailykortti("Veikeä Vasikka", 42, 1);
    Kerailykortti kortti2 = new Kerailykortti("Pinkeä Pingviini", 7, 3);
    Kerailykortti kortti3 = new Kerailykortti("Lentävä Lehmä", 1, 5);

    IO.println(kortti1);
    IO.println(kortti2);
    IO.println(kortti3);
}
// FILE_END
```

Tässä on hyvä huomata heti potentiaalinen ongelma. Mitä jos jossain päin koodia luodaankin kortti, jonka harvinaisuusaste on 0 tai 6? Tai vaikka -1 tai 100? Mikäli ohjelma on rakennettu olettaman päälle, että harvinaisuusaste on aina välillä 1-5, voi tämä johtaa odottamattomiin virheisiin ohjelman suorituksen aikana.

Myöskään pelkkä numero tässä tapauksessa ei ole kovin kuvaava. Mikäli joku lukee koodia, jossa luodaan kortti harvinaisuusasteella 1 tai 3, ei ole heti selvää, mitä tämä tarkoittaa vaan tähän tarvitaan selitys muualta — kumpi on harvinaisempi, 1 vai 3?

Ratkaisuksi ongelmaan, voimme luoda luetelma-tyypin harvinaisuusasteista, ja käyttää sitä kokonaisluvun sijaan. Luetelma määritetään luokan tavoin ja yksinkertaisimmillaan sisältäen vain luetelman mahdolliset arvot nimettyinä vakioina.

```java,noplayground
enum Harvinaisuusaste {
    PERUS,
    YLEINEN,
    HARVINAINEN,
    ERITTAN_HARVINAINEN,
    TARUNOMAINEN;
}
```

Vakiintunut tyyli on kirjoittaa luetelman nimetyt vakiot, kuten muutkin vakiot, isoin kirjaimin. Näin ero muuttujien ja vakioiden välillä näkyy koodissa selkeästi.
Huomaa myös, että luetelman vakioiden erottimena toimii pilkku ja lopussa tulee olla puolipiste.

Luetelman `Harvinaisuusaste` kanssa `Kerailykortti`-luokka voisi näyttää seuraavalta.

```java
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private int tunnistenumero;
    private Harvinaisuusaste harvinaisuusaste;

    //HIGHLIGHT_GREEN_BEGIN
    public Kerailykortti(
            String nimi,
            int tunnistenumero,
            Harvinaisuusaste harvinaisuusaste
    ) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
        this.harvinaisuusaste = harvinaisuusaste;
    }
    //HIGHLIGHT_GREEN_END

    @Override
    public String toString() {
        return String.format("#%s %s [%s]", tunnistenumero, nimi, harvinaisuusaste);
    }
}
// FILE_END
// FILE: Harvinaisuusaste.java
enum Harvinaisuusaste {
    PERUS,
    YLEINEN,
    HARVINAINEN,
    ERITTAN_HARVINAINEN,
    TARUNOMAINEN;
}
// FILE_END
// FILE: main.java
void main() {
    Kerailykortti kortti1 = new Kerailykortti("Veikeä Vasikka", 42, Harvinaisuusaste.PERUS);
    Kerailykortti kortti2 = new Kerailykortti("Pinkeä Pingviini", 7, Harvinaisuusaste.HARVINAINEN);
    Kerailykortti kortti3 = new Kerailykortti("Lentävä Lehmä", 1, Harvinaisuusaste.TARUNOMAINEN);

    IO.println(kortti1);
    IO.println(kortti2);
    IO.println(kortti3);
}
// FILE_END
```

<!-- Olisikohan tässä kivempi jos monen tiedoston esimerkki olisi purettu osiin ja lopuksi tulisi vasta yhdistetty ajettava versio? -->

Kun katsomme vielä `main.java`-tiedostoa, huomaamme miten saamme luetelman vakion käyttöön kirjoittamalla esimerkiksi `Harvinaisuusaste.PERUS`, eli luetelman nimen ja halutun vakion nimen pisteellä erotettuna. Koodista tulee näin hieman pidempää, mutta samalla selkeämpää ja erityisesti turvallisempaa kehittää, sillä kääntäjä pystyy paremmin ilmoittamaan milloin koodissa yritetään tehdä jotain muuta kuin mihin ohjelma on suunniteltu.

```java
// FILE: main.java
void main() {
    //HIGHLIGHT_GREEN_BEGIN
    Kerailykortti kortti1 = new Kerailykortti("Veikeä Vasikka", 42, Harvinaisuusaste.PERUS);
    Kerailykortti kortti2 = new Kerailykortti("Pinkeä Pingviini", 7, Harvinaisuusaste.HARVINAINEN);
    Kerailykortti kortti3 = new Kerailykortti("Lentävä Lehmä", 1, Harvinaisuusaste.TARUNOMAINEN);
    //HIGHLIGHT_GREEN_END

    IO.println(kortti1);
    IO.println(kortti2);
    IO.println(kortti3);
}
// FILE_END
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private int tunnistenumero;
    private Harvinaisuusaste harvinaisuusaste;

    public Kerailykortti(
            String nimi,
            int tunnistenumero,
            Harvinaisuusaste harvinaisuusaste
    ) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
        this.harvinaisuusaste = harvinaisuusaste;
    }

    @Override
    public String toString() {
        return String.format("#%s %s [%s]", tunnistenumero, nimi, harvinaisuusaste);
    }
}
// FILE_END
// FILE: Harvinaisuusaste.java
enum Harvinaisuusaste {
    PERUS,
    YLEINEN,
    HARVINAINEN,
    ERITTAN_HARVINAINEN,
    TARUNOMAINEN;
}
// FILE_END
```

- Lyhyt maininta luetelmasta ja compareTo-metodista johonkin väliin

```java
enum Arvosana {
    ERINOMAINEN,
    KIITETTAVA,
    HYVA,
    TYYDYTTAVA,
    VALTTAVA,
    HYLATTY
}
```

```java
enum ViikonPaivat {
    MAANANTAI,
    TIISTAI,
    KESKIVIIKKO,
    TORSTAI,
    PERJANTAI,
    LAUANTAI,
    SUNNUNTAI;
}
```

Voimme määritellä esimerkiksi luetelman sienten syötävyysmerkinnöille.

```java
enum SienenSyotavyys {
    ERINOMAINEN,
    HYVA,
    SYOTAVA,
    ARVOTON,
    MYRKYLLINEN,
    VAARALLISEN_MYRKYLLINEN,
    TAPPAVAN_MYRKYLLINEN;
}
```

Kattavaan merkintäluetelmaan tarvitsisimme vielä arvot esikäsiteltäville sienille. Yksinkertaisuuden vuoksi jätämme ne tässä esimerkissä huomiotta.

- Luetelman käytöstä esimerkkiä

- Tehtävä jo tähän?

## Luetelmalle ominaisuuksia ja toiminnallisuutta

- Luetelma on luokka
  - Luetelmalla voi olla metodeja
  - Luetelman vakiolle voi määrittää ominaisuuksia

```java
enum SienenSyotavyys {
    ERINOMAINEN("***"),
    HYVA("**"),
    SYOTAVA("*"),
    ARVOTON("○"),
    MYRKYLLINEN("†"),
    VAARALLISEN_MYRKYLLINEN("††"),
    TAPPAVAN_MYRKYLLINEN("†††");

    final private String symboli;

    SienenSyotavyys(String symboli) {
        this.symboli = symboli;
    }

    public String haeSymboli() {
        return this.symboli;
    }

    public boolean onSyotava() {
        return this == ERINOMAINEN || this == HYVA || this == SYOTAVA;
    }
}
```

- Tehtäviä viimeistään tähän

- Esimerkkejä käytöstä

## Tietue (kannattaako esitellä tässä vai mennäänkö vain luokilla?)

- Erityinen luokkatyyppi kuten luetelma (enum)

- Tarjoaa valmiin toteutuksen:
    - yksityinen, lopullinen kenttä jokaiselle tietoelementille
    - getter-metodi jokaiselle kentälle
    - julkinen konstruktori, jolla on vastaava argumentti jokaista kenttää varten
    - equals-metodi, joka palauttaa true, jos oliot ovat samaa luokkaa ja kaikki kentät ovat samat
    - hashCode-metodi, joka palauttaa saman arvon, kun kaikki kentät ovat samat (ja mahdollisesti muulloinkin — törmäykset ovat mahdollisia)
    - toString-metodi, joka sisältää luokan nimen sekä jokaisen kentän nimen ja sen vastaavan arvon

```java
record Sieni(String nimi, SienenSyotavyys syotavyys) {
}
```

# Tyypintarkastus ja hahmonsovitus

> [!Osaamistavoitteet]
>
> - Tyyppitarkistukset (instanceof)
> - hahmonsovitus `switch`-lausekkeessa

## Dynaaminen tyypintarkistus

- Pitäisikö `instanceof`-operaattori mainita lyhyesti jo perinnässä?
 (voidaan tarkistaa, että `Opiskelija` on tyyppiä `Henkilo`, mutta `Opettaja` ei ole `Opiskelija` jne.)

Java on staattisesti tyypitetty kieli, eli muuttujien tyypit määritellään koodissa etukäteen ja ovat tiedossa koodia kääntäessä. Etukäteen määritetty tyyppi voi kuitenkin olla yleinen, esimerkiksi `Object` tai `Number` ja saada todellisuudessa monentyyppisiä arvoja ([`Number`](https://docs.oracle.com/javase/8/docs/api/java/lang/Number.html) on abstrakti luokka, joka toimii yliluokkana Javan valmiille numerotyyppisille luokille, kuten `Integer` ja `Double`).

Ohjelmaa kehittäessä saattaa tulla vastaan tilanteita, jossa funktiossa tai luokassa on tarve käsitellä saman muuttujan arvoja eri tavalla riippuen siitä, minkä tyyppinen arvo on kyseessä.

Otetaan esimerkiksi tilanne, jossa numeerista dataa tulee eri muodoissa.

Tällöin pitäisi tietää muuttujan arvon tyyppi ajon aikana, kun muuttujan konkreettinen arvo on selvillä. Tälläisia tilanteita varten Javassa on muun muassa `instanceof`-operaattori.

```java
void main() {
    Object olio = 42;
    boolean olio = ehkaNumero instanceof Number;
    IO.println("Onko ehkaNumero numero? " + olio);
}
```

`instanceof`-operaattorin vasemmalle puolelle asetetaan tarkistettava arvo (mikä tahansa lauseke) ja oikealle puolelle tyyppi, jota vastaan tarkistus tehdään: `<lauseke> instanceof <tyyppi>`. Jos vasemman puolen arvo on oikean puolen tyypin ilmentymä (eli kyseinen arvo on kyseisen tyypin tai sen alityypin ilmentymä eli olio), palautetaan `true` ja muuten `false`.

```java
void main() {
    Object olio = "testi";
    IO.println("Onko olio merkkijono? " + (olio instanceof String)); // ilman sulkuja `+`-operaatio tehtäisi ennen `instanceof`-tarkistusta
    IO.println("Onko olio numero? " + (olio instanceof Number));

    olio = 123;
    IO.println("Onko olio merkkijono? " + (olio instanceof String));
    IO.println("Onko olio numero? " + (olio instanceof Number));
}
```

Tällaista ajonaikaista tyyppitarkistusta kutsutaan _dynaamiseksi tyypintarkistukseksi_ — dynaamisella tarkoitetaan ajonaikaista ja staattisella käännöksenaikaista.

<!-- ```java -->
<!-- void kerroOnkoMerkkijono(Object obj) { -->
<!--     if (obj instanceof String) { -->
<!--         IO.println("Annettu arvo on merkkijono"); -->
<!--     } else { -->
<!--         IO.println("Annettu ei arvo ei ole merkkijono vaan tyyppiä " + obj.getClass().getSimpleName()); -->
<!--     } -->
<!-- } -->

<!-- void main() { -->
<!--     Object muuttuja = "✍️"; -->

<!--     kerroOnkoMerkkijono(muuttuja); -->

<!--     muuttuja = 42; -->
<!--     kerroOnkoMerkkijono(muuttuja); -->

<!-- } -->
<!-- ``` -->

> Tehtävä

## switch-lause
switch/case-syntaksi auttaa parantamaan koodin luettavuutta. switch saattaa olla nopeampi ajaa Javassa hakutauluujen (engl. *lookup table*) ansiosta, jos `case`n arvona käytetään primitiivisiä tyyppejä tai enumeja. Java 25:sen mukana tuli nuolisyntaksi, joka nostaa luettavuutta entisestään. (Pitäisikö selittää syntaksista enemmänkin?). Tästä seuraavaksi esimerkki:

```java,editable
void main () {
    int kuukausi = 13;
    int vuosi = 2000;

    IO.println(
        switch(kuukausi) {
            case 1, 3, 5, 7, 8, 10, 12 -> 31;
            case 4, 6, 9, 11 -> 30;
            case 2 -> (vuosi % 4 == 0 && (vuosi % 100 != 0 || vuosi % 400 == 0)) ? 29 : 28; 
            default -> -1;
        }
    );

}
```

## Hahmonsovitus

Hahmonsovitus (engl. pattern matching) on ohjelmointitekniikka, jossa annettua lausekkeen arvoa verrataan _hahmoihin_  eli kuvauksiin arvon tyypistä, rakenteesta tai muista ominaisuuksista. Hahmonsovituksella voidaan sekä tarkistaa vastaako arvo tiettyä hahmoa että määritellä uusia muuttujia sovitetusta hahmosta.

Java-kielessä hahmonsovitus on olennaista erityisesti `switch`-lausekkeissa, joka purkaa käsiteltävän lausekkeen eri haaroihin lausekkeen arvon mukaan.

- Tarjoaa kätevän tavan tarkistaa tyypit ja purkaa arvot suoraan muuttujiksi switch-lauseessa

```java
void main() {
    Object[] taulukko = { "Hei", 123, 45.67, 'A', true };

    for (Object obj : taulukko) {
        switch (obj) {
            case String str -> IO.println("Merkkijono: " + str.toUpperCase());
            case Integer integer -> IO.println("Kokonaisluku: " + (integer * 2));
            case Double dbl -> IO.println("Liukuluku: " + (dbl / 2));
            case Character ch -> IO.println("Merkki: " + Character.toLowerCase(ch));
            case Boolean bool -> IO.println("Boolean: " + !bool);
            default -> IO.println("Odottamaton tyyppi: " + obj.getClass().getSimpleName());
        }
    }
}
```

- TODO: merkityksellisempiä esimerkkejä

- Haarojen täytyy kattaa kaikki mahdolliset tapaukset
- Ylläolevaa `instance of`-tyyliä voi tarvita, mikäli ei halua käsitellä kaikkia haaroja
  - Esimerkki tälle

- Switch on erityisen kätevä enumien kanssa
  - myös kun usea arvo johtavaa samaan käsittelyyn

```java
enum SienenSyotavyys {
    ERINOMAINEN("***"),
    HYVA("**"),
    SYOTAVA("*"),
    ARVOTON("○"),
    MYRKYLLINEN("†"),
    VAARALLISEN_MYRKYLLINEN("††"),
    TAPPAVAN_MYRKYLLINEN("†††");

    final private String symboli;

    SienenSyotavyys(String symboli) {
        this.symboli = symboli;
    }

    public String haeSymboli() {
        return this.symboli;
    }

    public boolean onSyotava() {
        return switch (this) {
            case ERINOMAINEN, HYVA, SYOTAVA -> true;
            default -> false;
        };
    }
}
```

- TODO: Pura ylempi kahteen esimerkkiin ja `onSyotava`-metodi erikseen

## Switch ja rajattu sovitus

- guarded pattern `when`-avainsanalla (rajattu sovitus)
  - onkohan tälle suomennosta jossain?

```java
class Hill {
    private String name;
    private double kPoint;

    public Hill(String name, double kPoint) {
        this.name = name;
        this.kPoint = kPoint;
    }

    public String getName() {
        return name;
    }

    public double getKPoint() {
        return kPoint;
    }

    // https://assets.fis-ski.com/f/252177/x/c0404a825e/icr-ski-jumping-2024_e_markedup.pdf 443.2 (page 70)
    public double getDistancePointsPerMeter() {
        return switch ((Double) kPoint) {
            case Double k when k < 20 -> -1;
            case Double k when k < 70 -> {
                var vahennysKerroin = Math.floor((20 - k) / 5);
                var distancePoints = (4.8 - 0.4 * vahennysKerroin);
                yield Math.round(distancePoints * 10) / 10.0; // korjataan liukulukulaskun pyöristysvirhe
            }
            case Double k when k >= 70 && k <= 79 -> 2.2;
            case Double k when k >= 80 && k <= 99 -> 2.0;
            case Double k when k >= 100 && k <= 134 -> 1.8;
            case Double k when k >= 135 && k <= 180 -> 1.6;
            default -> 1.2;
        };
    }

    public void setKPoint(double kPoint) {
        this.kPoint = kPoint;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return name + " (" + kPoint + " m)";
    }
}
```

```java
void main() {
    Object[] taulukko = { "Hei", 123, 45.67, 'A', true };

    List<Double> numerot = new ArrayList<>();

    for (Object obj : taulukko) {
        if (obj instanceof Number num) {
            IO.println("Lisätään numero" + num +  "liukulukulistaan.");
            numerot.add(num.doubleValue());
        } else {
            IO.println("Odottamaton tyyppi: " + obj.getClass().getSimpleName());
        }
    }
}
```

>- extrainfo? vanhemmilla javan versioilla piti tehdä vielä tyyppimuunnos tarkistuksen jälkeen, esim.
> ```java.ignore
> if (obj instanceof String) {
>     String str = (String) obj; // tyyppimuunnos
>     // käytä str-muuttujaa
> }
> ```

