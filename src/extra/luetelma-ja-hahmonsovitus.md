# Luetelma ja hahmonsovitus

> [!TODO]
>
> Tämä luku voisi olla jossain myöhemmässä osassa tai muuten jättää ekstraksi.
>
> Enumit voinee ainakin mainita asiana jossain kohti "vaihtoehtona"
> booleaneille.

> [!Osaamistavoitteet]
>
> - Tiedät mikä on luetelma tyyppinä ja ymmärrät sen hyödyt
> - Tiedät mitä on hahmonsovitus ja milloin sitä kannattaa käyttää


## Luetelma rajatuille joukoille

Luetelma (eng. enum/enumeration) on erityinen tyyppi, jolla voidaan rajoittaa muuttujan mahdolliset arvot tiettyyn joukkoon nimettyjä vakioita. Usein mainittuja esimerkkejä luetelmille ovat esimerkiksi viikonpäivät (ma, ti, ke, to, pe, la, su) tai ilmansuunnat (pohjoinen, itä, etelä, länsi) sekä pelikorttien maat (hertta, ruutu, risti, pata).

<!-- Olennaista on voida olettaa luetelman arvojoukon pysyvän samana, eli vakiona, koko ohjelman käytön ajan. -->

Jatketaan edellisen osan `Kerailykortti`-luokalla. Katsotaan tapausta, jossa meillä on tiedot `nimi` ja `tunnistenumero`, sekä näiden lisäksi `arvoluokka`, jonka tarkoitus on kertoa kuinka arvokas tai harvinainen kortti on. Olkoon arvoluokkia tasan viisi, joista 1 on yleisin ja 5 harvinaisin.


```java
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private int tunnistenumero;
    private int arvoluokka; // 1-5

    public Kerailykortti(String nimi, int tunnistenumero, int arvoluokka) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
        this.arvoluokka = arvoluokka;
    }

    // getterit...
//-    public String nimi() {
//-        return nimi;
//-    }
//-
//-    public int tunnistenumero() {
//-        return tunnistenumero;
//-    }
//-
//-    public int arvoluokka() {
//-        return arvoluokka;
//-    }

    @Override
    public String toString() {
        return String.format("#%s %s [%d]", tunnistenumero, nimi, arvoluokka);
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

Yllä olevasta `Kerailykortti`-luokan koodista on hyvä huomata heti potentiaalinen ongelma. Mitä jos jossain päin koodia luodaankin kortti, jonka arvoluokka on 0 tai 6? Tai vaikka -1 tai 100? Mikäli ohjelma on rakennettu sillä oletuksella, että arvoluokka on aina välillä 1-5, voi seurata odottamattomia virheitä ohjelman suorituksen aikana tai ohjelman kaatuminen, jos oletus ei jostain syystä pädekään. Esimerkin luokassa mikään ei estä luomasta korttia, jonka arvoluokka on vaikkapa 10:

```java
// FILE: main.java
String[] arvoluokkienKuvaukset = {
    "Perus",
    "Yleinen",
    "Harvinainen",
    "Erittäin harvinainen",
    "Tarunomainen"
};

void tulostaArvoluokka(Kerailykortti kortti) {
    // Tulostaa arvoluokan kuvauksen ongelmitta, kun arvoluokka on välillä 1-5
    String arvoluokkaKuvaus = arvoluokkienKuvaukset[kortti.arvoluokka() - 1];
    IO.println(arvoluokkaKuvaus);
}

void main() {
    Kerailykortti kortti1 = new Kerailykortti("Veikeä Vasikka", 42, 1);
    Kerailykortti kortti2 = new Kerailykortti("Pinkeä Pingviini", 7, 3);
    Kerailykortti kortti3 = new Kerailykortti("Lentävä Lehmä", 1, 5);
    Kerailykortti kortti4 = new Kerailykortti("Viheliäinen Varis", 99, 10);

    tulostaArvoluokka(kortti1);
    tulostaArvoluokka(kortti2);
    tulostaArvoluokka(kortti3);
    tulostaArvoluokka(kortti4);
}
// FILE_END
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private int tunnistenumero;
    private int arvoluokka; // 1-5

    public Kerailykortti(String nimi, int tunnistenumero, int arvoluokka) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
        this.arvoluokka = arvoluokka;
    }

    // getterit...
//-    public String nimi() {
//-        return nimi;
//-    }
//-
//-    public int tunnistenumero() {
//-        return tunnistenumero;
//-    }
//-
//-    public int arvoluokka() {
//-        return arvoluokka;
//-    }

    @Override
    public String toString() {
        return String.format("#%s %s [%d]", tunnistenumero, nimi, arvoluokka);
    }
}
// FILE_END
```

> [!Tärkeää — invariantti]
> Tietojenkäsittelytieteessä on olemassa hieno termi ohjelman tai sen osan ominaisuuksille, jotka ovat _tosia_ eli paikkansapitäviä ohjelman jonkin suoritusvaiheen tai koko suorituksen ajan: _invariantti_ (suora käännös: ei muuttuva). Esimerkiksi ajatus siitä, että kortin arvoluokka on aina välillä 1-5, on invariantti jos ja vain jos tämä ajatus on ohjelmassa (varmasti) totta koko ohjelman suorituksen ajan.
>
> Invarianttien ymmärtäminen (mitä oletamme koodistamme todeksi?) ja varmistaminen on tärkeä osa ohjelmiston suunnittelua ja toteutusta. Mikäli emme ole hyvin perillä siitä, mitä oletuksia koodistamme voimme tehdä, on vaarallisen helppoa kirjoittaa koodia, joka pettää tosipaikan tullen.

Pelkkä numero ei myöskään ole erityisen kuvaava tunniste, kun numerolla on muukin merkitys kuin numero itse. Mikäli joku lukee koodia, jossa luodaan kortti arvoluokalla 1 tai 3, ei ole heti selvää, mitä tämä tarkoittaa vaan tähän tarvitaan selitys muualta — kumpi on harvinaisempi, 1 vai 3?

Ratkaisuksi edellämainittuihin ongelmiin, voimme luoda uuden luetelma-tyypin arvoluokille, ja käyttää sitä kokonaisluvun sijaan. Luetelma määritetään luokan tavoin ja yksinkertaisimmillaan sisältäen vain luetelman mahdolliset arvot nimettyinä vakioina.

```java,noplayground
enum Arvoluokka {
    PERUS,
    YLEINEN,
    HARVINAINEN,
    ERITTAN_HARVINAINEN,
    TARUNOMAINEN;
}
```

Vakiintunut tyyli on kirjoittaa luetelman nimetyt vakiot, kuten muutkin vakiot, isoin kirjaimin (esim. `PERUS`). Näin ero muuttujien ja vakioiden välillä näkyy koodissa selkeästi.
Huomaa myös, että luetelman vakioiden erottimena toimii pilkku ja lopussa tulee olla puolipiste.

Luetelman `Arvoluokka` kanssa `Kerailykortti`-luokka voisi näyttää seuraavalta.

```java
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private int tunnistenumero;
    private Arvoluokka arvoluokka;

    //HIGHLIGHT_GREEN_BEGIN
    public Kerailykortti(
            String nimi,
            int tunnistenumero,
            Arvoluokka arvoluokka
    ) {
        this.nimi = nimi;
        this.tunnistenumero = tunnistenumero;
        this.arvoluokka = arvoluokka;
    }
    //HIGHLIGHT_GREEN_END

    @Override
    public String toString() {
        return String.format("#%s %s [%s]", tunnistenumero, nimi, arvoluokka);
    }
}
// FILE_END
// FILE: Arvoluokka.java
enum Arvoluokka {
    PERUS,
    YLEINEN,
    HARVINAINEN,
    ERITTAN_HARVINAINEN,
    TARUNOMAINEN;
}
// FILE_END
// FILE: main.java
void main() {
    //HIGHLIGHT_GREEN_BEGIN
    Kerailykortti kortti1 = new Kerailykortti("Veikeä Vasikka", 42, Arvoluokka.PERUS);
    Kerailykortti kortti2 = new Kerailykortti("Pinkeä Pingviini", 7, Arvoluokka.HARVINAINEN);
    Kerailykortti kortti3 = new Kerailykortti("Lentävä Lehmä", 1, Arvoluokka.TARUNOMAINEN);
    //HIGHLIGHT_GREEN_END

    IO.println(kortti1);
    IO.println(kortti2);
    IO.println(kortti3);
}
// FILE_END
```

<!-- Olisikohan tässä kivempi jos monen tiedoston esimerkki olisi purettu osiin ja lopuksi tulisi vasta yhdistetty ajettava versio? -->

Kun katsomme vielä ylläolevan esimerkin `main.java`-tiedostoa, huomaamme miten saamme luetelman vakion käyttöön kirjoittamalla esimerkiksi `Arvoluokka.PERUS`, eli luetelman nimen ja halutun vakion nimen pisteellä erotettuna. Koodista tulee näin hieman pidempää, mutta samalla selkeämpää ja erityisesti turvallisempaa kehittää; kääntäjä pystyy paremmin ilmoittamaan milloin koodissa yritetään tehdä jotain muuta kuin mihin ohjelma on suunniteltu.

> [!Huomautus]
>
> - Lyhyt maininta luetelmasta ja compareTo-metodista johonkin väliin

<task>
  <task-title num="4.5">Oma luetelma.<points>0.25 p.</points></task-title>
  <handout>

{{#include ../exercises/4-5-luetelma/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä TIMissä</a></task-link>
</task>

## Luetelmalle ominaisuuksia ja toiminnallisuutta

Voimme Javassa käyttää luetelmia monin samoin tavoin kuin tavallisia luokkia, kuten määrittää luetelman vakioille dataa attribuuteilla ja konstruktoreilla, sekä toteuttaa toiminnallisuutta metodeilla.

Katsotaan seuraavaksi esimerkkiä, jossa luomme luettelon `Suunta`, joka sisältää neljä suuntaa: ylös, alas, vasen ja oikea. Jokaisella suunnalla on lisäksi kaksi attribuuttia: `xMuutos` ja `yMuutos`, jotka määrittävät kuinka paljon kyseinen suunta muuttaa koordinaatteja x- ja y-akselilla.

```java,noplayground
enum Suunta {
    YLOS(0, 1),
    ALAS(0, -1),
    VASEN(-1, 0),
    OIKEA(1, 0);

    private final int xMuutos;
    private final int yMuutos;

    Suunta(int xMuutos, int yMuutos) {
        this.xMuutos = xMuutos;
        this.yMuutos = yMuutos;
    }

    public int xMuutos() {
        return xMuutos;
    }

    public int yMuutos() {
        return yMuutos;
    }
}
```

Voimme nyt käyttää `Suunta`-luetteloa esimerkiksi pelin hahmon liikuttamiseen koordinaatistossa.

```java
// FILE: main.java
void main() {
    Hahmo hahmo = new Hahmo(0, 0);
    IO.println(hahmo);
    hahmo.liiku(Suunta.YLOS);
    IO.println(hahmo);
    hahmo.liiku(Suunta.OIKEA);
    IO.println(hahmo);
    hahmo.liiku(Suunta.ALAS);
    IO.println(hahmo);
    hahmo.liiku(Suunta.VASEN);
    IO.println(hahmo);
}
// FILE_END
// FILE: Hahmo.java
class Hahmo {
    private int x;
    private int y;

    public Hahmo(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void liiku(Suunta suunta) {
        this.x += suunta.xMuutos();
        this.y += suunta.yMuutos();
    }

    @Override
    public String toString() {
        return String.format("Hahmon sijainti: (%d, %d)", x, y);
    }
}
// FILE_END
// FILE: Suunta.java
enum Suunta {
    YLOS(0, 1),
    ALAS(0, -1),
    VASEN(-1, 0),
    OIKEA(1, 0);

    private final int xMuutos;
    private final int yMuutos;

    Suunta(int xMuutos, int yMuutos) {
        this.xMuutos = xMuutos;
        this.yMuutos = yMuutos;
    }

    public int xMuutos() {
        return xMuutos;
    }

    public int yMuutos() {
        return yMuutos;
    }
}
// FILE_END
```

<task>
  <task-title num="4.6">Luetelma arvoilla.<points>0.25 p.</points></task-title>
  <handout>

{{#include ../exercises/4-6-luetelma-2/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä TIMissä</a></task-link>
</task>

## Hahmonsovitus

Hahmonsovitus (engl. pattern matching) on ohjelmointitekniikka, jossa annettua lausekkeen arvoa verrataan _hahmoihin_ eli kuvauksiin arvon tyypistä, rakenteesta tai muista ominaisuuksista. Hahmonsovituksella voidaan sekä tarkistaa vastaako arvo tiettyä hahmoa että määritellä uusia muuttujia sovitetusta hahmosta.

Java-kielessä hahmonsovitus on olennaista erityisesti `switch`-lausekkeissa, joka purkaa käsiteltävän lausekkeen eri haaroihin lausekkeen arvon mukaan. Katsotaan tästä esimerkkiä aiemmin käyttämällemme `Suunta`-luetelmalle.

```java
// FILE: main.java
void main() {
    Suunta suunta = Suunta.OIKEA;

    String suuntaKuvaus = switch (suunta) {
        case YLOS -> "Suunta on ylös";
        case ALAS -> "Suunta on alas";
        case VASEN -> "Suunta on vasemmalle";
        case OIKEA -> "Suunta on oikealle";
    };

    IO.println(suuntaKuvaus);
}
// FILE_END
// FILE: Suunta.java
enum Suunta {
    YLOS(0, 1),
    ALAS(0, -1),
    VASEN(-1, 0),
    OIKEA(1, 0);

    private final int xMuutos;
    private final int yMuutos;

    Suunta(int xMuutos, int yMuutos) {
        this.xMuutos = xMuutos;
        this.yMuutos = yMuutos;
    }

    public int xMuutos() {
        return xMuutos;
    }

    public int yMuutos() {
        return yMuutos;
    }
}
// FILE_END
```

Kuten yllä olevasta esimerkistä on nähtävissä, `switch`-lausekkeen syntaksiin kuuluu käsiteltävä lauseke sulkeissa (`(suunta)`). Tämän jälkeen määritellään mahdolliset haarat aaltosulkeiden . Jokaisessa haarassa määritetään `case` avainsanan perään hahmo, mihin käsiteltävää lauseketta sovitetaan (esim. `YLÖS`), jonka jälkeen tulee nuoli (`->`) ja lopuksi haaraa vastaava arvo.

Hahmoja voi niputtaa pilkulla erotettuna samaan haaraan, mikäli halutaan käsitellä useampi arvo samalla tavalla. Esimerkiksi:

```java
// FILE: main.java
void main() {
    Suunta suunta = Suunta.OIKEA;

    String suuntaKuvaus = switch (suunta) {
        case YLOS, ALAS -> "Suunta on pystyakselilla";
        case VASEN, OIKEA -> "Suunta on vaaka-akselilla";
    };

    IO.println(suuntaKuvaus);
}
// FILE_END
// FILE: Suunta.java
enum Suunta {
    YLOS(0, 1),
    ALAS(0, -1),
    VASEN(-1, 0),
    OIKEA(1, 0);

    private final int xMuutos;
    private final int yMuutos;

    Suunta(int xMuutos, int yMuutos) {
        this.xMuutos = xMuutos;
        this.yMuutos = yMuutos;
    }

    public int xMuutos() {
        return xMuutos;
    }

    public int yMuutos() {
        return yMuutos;
    }
}
// FILE_END
```

Huomionarvoista on, että haarojen tulee olla _kattavia_, eli kaikki mahdolliset käsiteltävän lausekkeen arvot tulee olla katettuina jossain haarassa. Mikäli näin ei ole, kääntäjä antaa virheen.

```java
// FILE: main.java
void main() {
    Suunta suunta = Suunta.OIKEA;

    String suuntaKuvaus = switch (suunta) {
        case YLOS, ALAS -> "Suunta on pystyakselilla";
        // VIRHE: VASEN ja OIKEA puuttuvat
    };

    IO.println(suuntaKuvaus);
}
// FILE: Suunta.java
enum Suunta {
    YLOS(0, 1),
    ALAS(0, -1),
    VASEN(-1, 0),
    OIKEA(1, 0);

    private final int xMuutos;
    private final int yMuutos;

    Suunta(int xMuutos, int yMuutos) {
        this.xMuutos = xMuutos;
        this.yMuutos = yMuutos;
    }

    public int xMuutos() {
        return xMuutos;
    }

    public int yMuutos() {
        return yMuutos;
    }
}
// FILE_END
```

Mikäli kaikkia arvoja ei voida tai haluta käsitellä erikseen, voidaan käyttää oletushaaraa `default`-avainsan avulla. Oletushaara toimii samoin kuin `else`-haara `if-else`-rakenteessa. Esimerkiksi:

```java
// FILE: main.java
void main() {
    Suunta suunta = Suunta.OIKEA;

    String suuntaKuvaus = switch (suunta) {
        case YLOS, ALAS -> "Suunta on pystyakselilla";
        default -> "Suunta on vaaka-akselilla";
    };

    IO.println(suuntaKuvaus);
}
// FILE_END
// FILE: Suunta.java
enum Suunta {
    YLOS(0, 1),
    ALAS(0, -1),
    VASEN(-1, 0),
    OIKEA(1, 0);

    private final int xMuutos;
    private final int yMuutos;

    Suunta(int xMuutos, int yMuutos) {
        this.xMuutos = xMuutos;
        this.yMuutos = yMuutos;
    }

    public int xMuutos() {
        return xMuutos;
    }

    public int yMuutos() {
        return yMuutos;
    }
}
// FILE_END
```

Luetelmien vakioiden lisäksi voimme sovittaa `switch`-lausekkeessa myös alkeistietotyyppejä, kuten kokonaislukuja. Alla on esimerkki, jossa lasketaan kuukausien päivien määrät.

```java
int kuukaudenPaivat(int kuukausi) {
    int paivat = switch (kuukausi) {
        case 1, 3, 5, 7, 8, 10, 12 -> 31;
        case 4, 6, 9, 11 -> 30;
        case 2 -> 28; // Ei oteta huomioon karkausvuosia (vielä)
        default -> -1; // Virheellinen kuukausi
    };

    return paivat;
}

void main() {
    for (int kk = 1; kk <= 13; kk++) {
        IO.println("Kuukaudessa " + kk + " on " + kuukaudenPaivat(kk) + " päivää.");
    }
}
```

### Hieman monimutkaisempi esimerkki

Tähän asti esimerkeissämme haaroja vastaavat arvot olleet yksinkertaisia literaaliarvoja, vaikka voisimme aivan hyvin käyttää mitä tahansa oikean arvon palauttavaa lauseketta.

Seuraavassa esimerkissä otamme huomioon karkausvuodet helmikuun päivien määrää laskettaessa.

```java
boolean onKarkausvuosi(int vuosi) {
    return vuosi % 4 == 0 && (vuosi % 100 != 0 || vuosi % 400 == 0);
}

int kuukaudenPaivat(int kuukausi, int vuosi) {
    int paivat = switch (kuukausi) {
        case 1, 3, 5, 7, 8, 10, 12 -> 31;
        case 4, 6, 9, 11 -> 30;
        case 2 -> onKarkausvuosi(vuosi) ? 29 : 28;
        default -> -1; // Virheellinen kuukausi
    };

    return paivat;
}

void main() {
    for (int kk = 1; kk <= 13; kk++) {
        IO.println("Kuukaudessa " + kk + " on " + kuukaudenPaivat(kk, 2020) + " päivää.");
    }
}
```

> [!todo]
> Alla oleva erikoisuus lisäinfoksi?

Yllä olevassa esimerkissä olemme eriyttäneet karkausvuoden tarkistuksen omaan `onKarkausvuosi`-funktioon, jota käytämme `helmikuunPaivat`-funktiossa. Voisimme kuitenkin kirjoittaa karkausvuoden tarkistuksen suoraan `switch`-lausekkeeseen, kuten alla olevassa esimerkissä:

```java
int kuukaudenPaivat(int kuukausi, int vuosi) {
    int paivat = switch (kuukausi) {
        case 1, 3, 5, 7, 8, 10, 12 -> 31;
        case 4, 6, 9, 11 -> 30;
        case 2 -> {
            boolean karkaus = vuosi % 4 == 0 && (vuosi % 100 != 0 || vuosi % 400 == 0);
            yield karkaus ? 29 : 28; // yield avainsana palauttaa arvon switch-haarasta
        }
        default -> -1; // Virheellinen kuukausi
    };

    return paivat;
}

void main() {
    for (int kk = 1; kk <= 13; kk++) {
        IO.println("Kuukaudessa " + kk + " on " + kuukaudenPaivat(kk, 2020) + " päivää.");
    }
}
```

Tässä syntaksissa erikoisuutena on `yield`-avainsanan käyttö tutun `return`:n sijaan. Javassa `yield`-avainsanaa käytetään palauttamaan arvo `switch`-lausekkeen haarasta, kun kyseinen haara on määritelty aaltosulkeiden sisällä. Tämä mahdollistaa palautettavan lausekkeen jakamisen useampaan lauseeseen, ja voimme käyttää muun muassa apumuuttujia luettavuuden parantamiseksi.

> [!Vinkki]
> Sen lisäksi, että switch:n käyttö voi auttaa parantamaan koodin luettavuutta ja kehittäjäkokemusta verrattuna vastaavan toiminnallisuuden toteuttamiseen `if-else`-rakenteellla, switch on myös huomattavasti tehokkaampi vaihtoehto. Siinä missä kääntäjä käy `if-else`-tyylisiä rakenteita yksi kerrallaan läpi, kunnes sopiva haara löytyy, `switch`-lausekkeen tapauksessa kääntäjä voi luoda ennalta tiedossa olevien _kattavien_ haarojen perusteella _hakutaulun_ (engl. _lookup table_). Hakutaulun — näistä lisää osiossa TODO ja algoritmikurssilla — avulla sopiva haara voidaan hakea arvon (tai sille lasketun paikan) perustella suoraan muistista sen enempää vertailematta eri vaihtoehtoja.

<task>
  <task-title num="4.8">Hahmonsovitus 2<points>0.25 p.</points></task-title>
  <handout>

{{#include ../exercises/4-7-hahmonsovitus-2/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä TIMissä</a></task-link>
</task>

### Hahmonsovitus muuttujiin

Hahmonsovituksen määritelmässä mainittiin, että hahmonsovituksella voidaan määritellä uusia muuttujia sovitetusta hahmosta. Javan `switch`-lausekkeessa tämä onnistuu lisäämällä haluttu muuttujan nimi hahmon määritelmään, jolloin muuttujaa voidaan hyödyntää haarassa.

Seuraavassa esimerkissä on funktio `kokonaisluku` joka muuttaa annetut arvot eri tavoin kokonaisluvuksi riippuen arvon tyypistä.

<!-- TODO: tähän yksinkertaisempi esimerkki -->

```java
Integer kokonaisluku(Object olio) {
    return switch (olio) {
        case Integer luku -> luku;
        case Float liukuluku -> Math.round(liukuluku);
        case Boolean totuusarvo -> totuusarvo ? 1 : 0;
        case String merkkijono -> {
            try {
                yield Math.round(Float.parseFloat(merkkijono));
            } catch (NumberFormatException e) {
                yield null;
            }
        }
        default -> null;
    };
}

void main() {
    Object[] taulukko = {"Hei", 123, 45.67, 'A', true, "301"};

    for (Object o : taulukko) {
        Integer kokonaisluku = kokonaisluku(o);
        IO.println(kokonaisluku);
    }
}
```

Jokaisessa haarassa, oletushaara poislukien, määritetään uudentyyppinen muuttuja. Esimerkiksi toisessa haarassa `case Float luku` määritellään uusi `numero`-muuttuja, joka on tyyppiä `Float`. Muuttuja sisältää saman arvon kuin käsiteltävällä lausekkeella, mutta uuden muuttujan tyyppi on tarkempi, jolloin meillä on enemmän toiminnallisuutta tarjolla kuin yleisemmillä luokilla. Tässä tapauksessa käytämme `Math.round`-metodia pyöristämään liukuluvun kokonaisluvuksi.

### Rajattu sovitus

Hahmonsovituksen haaroille voi määrittää myös ehtoja itse hahmon lisäksi. Tätä kutsutaan rajatuksi sovitukseksi (engl. _guarded pattern matching_) ja onnistuu Javassa `when`-avainsanan avulla muuttujan määrityksen yhteydessä mallilla `case <hahmo> <muuttuja> when <ehto> -> <lauseke>` eli esimerkiksi `case Float liukuluku when liukuluku > 0 -> IO.println(liukuluku + "on tyyppiä Float ja suurempi kuin 0")`. Rajatulla hahmonsovituksella voisimme muun muassa toteuttaa aiemman karkausvuoden tarkistuksen seuraavasti:

```java
boolean onKarkausvuosi(int vuosi) {
    return vuosi % 4 == 0 && (vuosi % 100 != 0 || vuosi % 400 == 0);
}

int kuukaudenPaivat(int kuukausi, int vuosi) {
    boolean karkaus = onKarkausvuosi(vuosi);

    int paivat = switch ((Integer) kuukausi) {
        case Integer k when Set.of(1, 3, 5, 7, 8, 10, 12).contains(k) -> 31;
        case Integer k when Set.of(4, 6, 9, 11).contains(k) -> 30;
        case Integer k when k == 2 && karkaus -> 29;
        case Integer k when k == 2 -> 28;
        default -> -1; // Virheellinen kuukausi
    };

    return paivat;
}

void main() {
    for (int kk = 1; kk <= 13; kk++) {
        IO.println("Kuukaudessa " + kk + " on " + kuukaudenPaivat(kk, 2020) + " päivää.");
    }
}
```

Javan hahmonsovituksessa on valitettavasti merkittäviä rajoituksia. Jokaisessa ylläolevan esimerkin haarassa on määritettynä uusi `Integer k`-muuttuja, sillä Javan rajattu sovitus toimii vain muuttujien sovittamisen yhteydessä (Java ei esimerkiksi salli haaraa `case 2 when karkaus -> 29`). Vastaavasti `switch`-lausekkeen käsiteltävä lauseke muunnetaan eksplisiittisesti oliotyypiksi `Integer`, sillä rajattu Javan hahmonsovitus ei toimi alkeistyyppien, kuten `int`, kanssa.

Rajatun hahmonsovitukset hyödyt eivät kuitenkaan vielä oikein näy kuukauden päivät -esimerkin tapauksessa, kun sitä vertaa aiempaan alkeistyyppiseen hahmonsovitukseen (`case 1, 3, 5...`), joka on kyseiseen tarkoitukseen täysin riittävä ja yksinkertaisuutensa puolesta erinomaisesti sopiva ratkaisu.

Katsotaan vielä hieman laajempaa esimerkkiä, missä rajattua hahmonsovitusta kaivataan enemmän, nyt mäkihypyn kontekstissa. Jokaisella virallisella mäkihyppymäellä on määritelty k-piste eli mäen loiventumiskohta, ja hyppysuorituksen pituudesta saatavat pisteet riippuvat hypätyn mäen k-pisteestä. Alla on taulukko, joka listaa hyppypituuden pisteytyksen mäen k-pisteen mukaan (lähde: [kansainvälinen hiihtoliitto FIS](https://assets.fis-ski.com/f/252177/x/c0404a825e/icr-ski-jumping-2024_e_markedup.pdf)):

| K-piste (m) | Pisteet per metri |
| ----------- | ----------------- |
| 20 - 24     | 4.8               |
| 25 - 29     | 4.4               |
| 30 - 34     | 4.0               |
| 35 - 39     | 3.6               |
| 40 - 49     | 3.2               |
| 50 - 59     | 2.8               |
| 60 - 69     | 2.4               |
| 70 - 79     | 2.2               |
| 80 - 99     | 2.0               |
| 100 - 134   | 1.8               |
| 135 - 180   | 1.6               |
| 180+        | 1.2               |

Toteutetaan metodi `pisteetPerMetri`, joka palauttaa pisteet per metri k-pisteen perusteella käyttäen `switch`-lauseketta ja rajattua sovitusta yllä olevan taulukon mukaisesti.

```java,editable
double pisteetPerMetri(double kPoint) {
    return switch ((Double) kPoint) {
        case Double kp when (kp >= 20 && kp <= 24) -> 4.8;
        case Double kp when (kp >= 25 && kp <= 29) -> 4.4;
        case Double kp when (kp >= 30 && kp <= 34) -> 4.0;
        case Double kp when (kp >= 35 && kp <= 39) -> 3.6;
        case Double kp when (kp >= 40 && kp <= 49) -> 3.2;
        case Double kp when (kp >= 50 && kp <= 59) -> 2.8;
        case Double kp when (kp >= 60 && kp <= 69) -> 2.4;
        case Double kp when (kp >= 70 && kp <= 79) -> 2.2;
        case Double kp when (kp >= 80 && kp <= 99) -> 2.0;
        case Double kp when (kp >= 100 && kp <= 134) -> 1.8;
        case Double kp when (kp >= 135 && kp <= 180) -> 1.6;
        case Double kp when (kp > 180) -> 1.2;
        default -> -1.0; // Määrittämätön k-piste
    };
}

void main() {
    double kPoint = 120.0;
    double pisteet = pisteetPerMetri(kPoint);
    IO.println("Hypystä saa " + pisteet + " pistettä per metri, kun mäen k-piste on " + kPoint + " metrissä.");
}
```

<task>
  <task-title num="4.8">Hahmonsovitus 2<points>0.25 p.</points></task-title>
  <handout>

{{#include ../exercises/4-7-hahmonsovitus-2/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/TODO">Tee tehtävä TIMissä</a></task-link>
</task>
