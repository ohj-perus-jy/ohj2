# Luokka ja olio

> [!Osaamistavoitteet]
>
> - Luokka ja olio
> - Konstruktori, metodi, attribuutti
> - Luokan rakenne ja suhde olioon (konstruktori, attribuutti, metodi, this-viite, "luokka blueprintina oliolle")
> - `final` attribuuttien kanssa
> - Osaat määritellä ja hyödyntää omia luokkia Javalla

## Luokka

Ensimmäinen askel olio-ohjelmointiin on luokan määritteleminen. Luokkaa voi ajatella kaavana tai muottina, jonka pohjalta olioita luodaan. Luokka kertoo, mitä tietoja olio sisältää (attribuutit) ja mitä se voi tehdä (metodit). 

Esimerkiksi yhden rakennuspiirustuksen pohjalta voidaan rakentaa monta rakennusta. Ne olisivat rakenteeltaan samanlaisia, sillä ne ovat saman kaavan mukaan tehty, mutta jokaisella rakennuksella olisi kuitenkin oma tila; eri omistaja, väri, sisustus, jne. Rakennuspiirustus on kuin luokka ja rakennukset sen pohjalta tehtyjä olioita. Luokan nimi kertoo, *mikä* olio on, joten jos tekisimme luokan rakennuksille, sen nimeksi tulisi `Rakennus`. Huomaa, että Javassa on tapana aloittaa luokkien nimet aina isolla kirjaimella.

```java
public class Rakennus {
    // Attribuutit - mitä tietoja rakennuksesta pitää tallentaa?
    private String omistaja;
    private String väri;

    // Metodit - mitä rakennus voi tehdä?
    public void setOmistaja(String omistaja) {
        this.omistaja = omistaja;
    }
}
```

### Attribuutit

Luokan sisällä esiteltyjä muuttujia kutsutaan *attribuuteiksi*. 

Attribuutit ovat käytännössä aivan kuin tavallisetkin muuttujat, eli samat säännöt pätevät niihinkin; attribuutti voi olla alkeistietotyyppi tai viitemuuttuja ja se nimetään kuin muuttujat yleensä. Attribuuteilla on kuitenkin muutama erikoisominaisuus - esimerkiksi näkyvyysmääreet. Attribuutit ovat aina näkyvissä saman luokan sisällä, mutta näkyvyys niiden oman luokan ulkopuolelle on hallittavissa - palaamme tähän pian, kun tutustumme tarkemmin näkyvyysmääreisiin.

Jokaisella samasta luokasta tehdyllä oliolla on aina samat attribuutit, mutta niillä omat arvot, sillä jokaisella oliolla on oma tila. Olion tilan voidaan siis ajatella olevan tallessa sen attribuuteissa. Attribuuttien elinikä on sama kuin olion, sillä olion tilan täytyy olla olemassa olion tuhoutumiseen asti. Attribuutille voidaan antaa oletusarvo, jolloin luokasta luodut oliot saavat sen myös oman attribuuttinsa alkuarvoksi.

Huom! Luokassa olevien aliohjelmien sisällä esitellyt muuttujat eivät ole attribuutteja, vaan aliohjelman *lokaaleja muuttujia*. Vain suoraan luokan alla olevat muuttujat ovat attribuutteja. Lokaalien muuttujien sisältämä tieto katoaa aliohjelman päätyttyä, eli ne eivät ole osa olion tilaa. Paikallisella muuttujalla voi olla sama nimi kuin attribuutilla. Jos aliohjelman näkyvissä on saman niminen attribuutti ja paikallinen muuttuja, käytetään ensisijaisesti paikallista muuttujaa - paikallinen muuttuja siis peittää attribuutin. Tässä tapauksessa attribuuttiin päästään käsiksi käyttämällä `this`-viitettä. Palaamme tähän myöhemmin tässä osassa.

```java
public class Rakennus {
    // Nämä muuttujat ovat attribuutteja. Jokaisella rakennuksella on omistaja ja väri, mutta ne eivät välttämättä ole kaikilla olioilla arvoiltaan samat.
    private String omistaja;
    private String väri = "sininen"; // Värin oletusarvo on sininen, joten kaikilla tämän luokan pohjalta tehdyillä olioilla on aluksi värin arvona sininen.

    public void teeJotain()
    {
        int luku = 5; // Tämä muuttuja ei ole luokan attribuutti, sillä se on esitelty aliohjelman sisällä.

        String väri = "punainen"; // Tämä lokaali muuttuja peittää tämän funktion sisällä saman nimen omaavan attribuutin.
        IO.println(väri); // Tulostaa "punainen". Tunniste väri viittaa ensisijaisesti lokaaliin muuttujaan, koska sellainen on näkyvissä.
        IO.println(this.väri); // Tulostaa "sininen" - this-määritteen avulla voidaan viitata aina attribuuttiin.
    }
}
```

TODO: Siisti esimerkkiä

### Metodit

Luokassa määriteltyjä, olion tilaan käsiksi pääseviä aliohjelmia kutsutaan *metodeiksi*. Jos attribuutti on olion sisältämää tietoa, metodeja voisi kuvailla olion kyvyiksi tehdä jotain. Metodien määrittely ei syntaksiltaan juurikaan eroa muista aliohjelmista ja niissä käytetään myös samanlaisia nimeämiskäytänteitä. Kuten yleensä aliohjelmia tehdessä, metodin tehtävä on yleensä suorittaa jokin yksi asia. Liian suuret tehtävät on hyvä jakaa pienempiin osiin. Metodeja voi myös kuormittaa aivan kuin muitakin aliohjelmia. Olio-ohjelmoinnissa uutena ominaisuutena tulee olemassa olevan metodin toteutuksen korvaaminen uudella. Tämä ilmaistaan `@Override`-notaatiota käyttämällä. Palaamme tähän aiheeseen, kun lähdemme tutustumaan perintään ja rajapintoihin seuraavassa osassa.

Jotta voimme kutsua olion metodia, meillä täytyy ensin olla olio ja siihen viite. Teimme itse asiassa jo edellisessä kohdassa metodin `Rakennus`-luokkaan. Tehdään luokkaan pari yksinkertaista metodia tilan käsittelyyn ja kutsutaan näitä.

```java
public class Rakennus {
    private String omistaja;
    private String väri;

    // Metodi, joka ottaa vastaan merkkijonon ja sijoittaa sen attribuuttiin. Huomaa tässä, että parametrin attribuutin nimi on sama, joten käytämme this-viitettä.
    public void setVäri(String väri) {
        this.väri = väri;
    }

    // Metodi, joka antaa attribuutin arvon kutsujalle.
    public String getVäri() {
        return this.väri;
    }
}

void main() {
    // Luodaan kaksi rakennusta
    Rakennus rakennus1 = new Rakennus();
    Rakennus rakennus2 = new Rakennus();

    // Käytetään olioiden metodeja muuttamaan niiden tilaa.
    rakennus1.setVäri("vihreä");
    rakennus2.setVäri("valkoinen")

    // Tulostetaan olioiden värit saantimetodien avulla.
    IO.println(rakennus1.getVäri()); // Tulostaa "vihreä"
    IO.println(rakennus2.getVäri()); // Tulostaa "valkoinen"
}
```

TODO: Onko tarpeen enää kerrata tässä olioviitteen välittämistä aliohjelmalle?

### Muodostaja eli konstruktori

TODO: Konstruktori, parametriton, parametrisoitu, copy-konstruktori

Muodostaja eli konstruktori on erikoismetodi, jota kutsutaan automaattisesti uuden olion luomisen yhteydessä ja jolla voidaan asettaa olion alkuperäinen tila. Muodostajilla ei ole palautustyyppiä ja niiden nimen täytyy olla sama kuin luokan. 

Jos emme määrittele luokalle muodostajaa, Java käyttää automaattisesti tyhjää, parametritonta oletusmuodostajaa, joka osaa kyllä luoda olion, mutta ei tee mitään se tilan alustamiseksi. Joissain tapauksissa tämä riittää, mutta yleensä haluamme lisätä itse omia muodostajia, joilla voimme luoda olioita eri tavoin. Jos määrittelemme luokalle yhdenkin muodostajan, meidän täytyy määritellä myös parametriton perusmuodostaja itse. Jos luokalla on useampi muodostaja eri parametreilla, oikea muodostaja valitaan automaattisesti olion luomisen yhteydessä annettujen argumenttien avulla.

Käytimme aikaisemmassa esimerkissä `Rakennus`-luokkaa määrittelemättä muodostajaa. Otetaan metodit hetkeksi pois selkeyden vuoksi ja katsotaan, mitä olioita luodessa tapahtuu.

```java
public class Rakennus {
    private String omistaja;
    private String väri;
}

void main() {
    Rakennus rakennus = new Rakennus();
}
```

Tässä tapauksessa olio muodostetaan oletusmuodostajaa käyttäen, koska yhtään muodostajaa ei ole määritelty. Voimme tehdä vastaavan perusmuodostajan itsekin:

```java
public class Rakennus {
    private String omistaja;
    private String väri;

    // Parametriton perusmuodostaja. Tämä ei ole tässä tapauksessa pakollinen.
    public Rakennus() {
        // Tässä voisimme alustaa olion tilan jollain tavalla.
    }
}

void main() {
    // Olio luodaan perusmuodostajaa käyttäen.
    Rakennus rakennus = new Rakennus();
}
```

Määritellään luokalle vielä oma muodostaja, joka ottaa omistajan ja värin parametrina vastaan, jotta voimme luoda `Rakennus`-olion helpommin suoraan oikealla tilaan.

```java
public class Rakennus {
    private String omistaja;
    private String väri;

    // Parametriton perusmuodostaja. Tämä on nyt pakollinen, koska määrittelimme luokkaan toisenkin muodostajan.
    public Rakennus() {
        // Tässä voisimme alustaa olion tilan jollain tavalla.
    }

    public Rakennus(String omistaja, String väri) {
        // Alustetaan olion tila parametrien avulla. Huomaa this-viitteen käyttö, sillä parametrit ja attribuutit käyttävät samoja nimiä.
        this.omistaja = omistaja;
        this.väri = väri;
    }
}

void main() {
    // Ensimmäiselle oliolle ei anneta luonnin yhteydessä argumentteja - sulut jäävät tyhjäksi. Kääntäjä valitsee parametrittoman perusmuodostajan.
    Rakennus rakennus1 = new Rakennus();

    // Toiselle oliolle annetaan kaksi merkkijonoa argumentteina. Nämä vastaavat määrittelemäämme parametrillista muodostajaa, joten sitä käytetään olion alustamiseen.
    Rakennus rakennus2 = new Rakennus("DVV", "valkoinen");

    // Tämä ei onnistuisi, sillä emme ole määritelleet muodostajaa, jossa on vain yksi parametri. 
    // Rakennus rakennus3 = new Rakennus("DVV");
}
```

Voimme lopuksi vielä lisätä hieman erikoisemman muodostajan, joka ottaa vastaan toisen saman luokan olion ja kopioi sen arvot muodostettavalle oliolle. Tällaista muodostajaa kutsutaan usein copy-muodostajaksi.

```java
public class Rakennus {
    private String omistaja;
    private String väri;

    public Rakennus() {}

    public Rakennus(String omistaja, String väri) {
        this.omistaja = omistaja;
        this.väri = väri;
    }

    // Muodostaja, joka ottaa vastaan toisen olion ja kopioi sen arvot tälle oliolle.
    public Rakennus(Rakennus kopioitava) {
        this.omistaja = kopioitava.omistaja;
        this.väri = kopioitava.väri;
    }
}

void main() {
    Rakennus rakennus1 = new Rakennus("DVV", "valkoinen");

    // Antamalla argumenttina toisen Rakennus-tyyppisen olion, käytämme uutta muodostaa, joka kopioi olion arvot. Molemmilla rakennuksilla on nyt sama omistaja ja väri.
    Rakennus rakennus2 = new Rakennus(rakennus1);
}
```

### Muita erikoismetodeja

Oletusmuodostajan lisäksi kaikilla Javan olioilla on myös muita metodeja olemassa, vaikka emme näitä omaan luokkaamme määrittelisi. Voimme kuitenkin muuttaa näiden toimintaa oman luokkamme osalta kirjoittamalle niille uuden toteutuksen. Palaamme näihin metodeihin ja siihen, mistä nämä kaikkiin olioihin tulevat seuraavassa osassa, kun tutustumme luokkien perintään.

Valmiiksi määritellyistä metodeista `toString` on ehkä hyödyllisin. Tämän metodin tarkoitus on antaa olion tiedot merkkijonona. Erikoisen metodista tekee se, että sitä kutsutaan automaattiseti, jos oliota ollaan muuttamassa merkkijonoksi joko tarkoituksella tai implisiittisesti. `toString` on olemassa kaikilla olioilla, mutta jos sille ei ole tehty omaa toteutusta, se palauttaa merkkijonona yhdistelmän olion luokan nimestä sekä olion hajautusarvosta. Palaamme hajautusarvon käsitteeseen myöhemmin. Voimme tässä vaiheessa ajatella tätä olion yksilöivänä tunnisteena ohjelman tämänhetkisen suorituskerran aikana.

```java
public class Rakennus {
    private String omistaja;
    private String väri;

    public Rakennus() {}

    public Rakennus(String omistaja, String väri) {
        this.omistaja = omistaja;
        this.väri = väri;
    }

    // Tehdään oma toteutus toString-metodille.
    @Override
    public String toString() {
        return omistaja + " - " + väri;
    }
}

void main() {
    Rakennus rakennus1 = new Rakennus("DVV", "valkoinen");
    IO.println(rakennus1.toString()); // Tulostaa "DVV - valkoinen".
    IO.println(rakennus1); // println yrittää muuttaa olion implisiittisesti merkkijonoksi, jolloin toString-metodia käytetään automaattisesti.
}
```

TODO: `equals` ja `hashCode`

## Static-määrite

Havainnollistimme tämän osan alussa luokkia ja olioita näin:

![Luokka ja oliot](images/luokka_ja_oliot.png)

Jokainen kuvassa esiintyvä olio sisältää omat, luokassa määriteltyä rakennetta vastaavat attribuutit ja metodit. Jokaisella oliolla on oma tila, eli omat attribuuttien arvot. Voimme määritellä luokkaan myös muuttujia ja aliohjelmia, joiden *ei* ole tarkoitus olla kiinnitetty minkään yhden olion tilaan. Tämä onnistuu `static`-avainsanaa käyttämällä, eli tekemällä muuttujista tai aliohjelmista *staattisia*.

Staattisia aliohjelmia ja muuttujia voidaan käyttää ilman luokan ilmentymiä eli olioita, sillä ne eivät ole osa minkään yksittäisen olion tilaa. Voimme havainnolistaa tätä niin, että nämä attribuutit ja metodit sijaitsevat vain luokassa - ja niitä yleensä kutsutaankin *luokan* muuttujiksi ja aliohjelmiksi.

![Luokka, oliot ja staattisuus](images/luokka_ja_oliot_static.png)

Tämäkään havainnollistus ei täysin vastaa todellisuutta, mutta se auttaa toivottavasti ymmärtämään staattisuuden käsitettä olioiden osalta.

Oliot pääsevät käsiksi aina oman luokkansa staattisiin muuttujiin ja aliohjelmiin. Staattiset muuttujat ovat kuitenkin jaettuja kaikkien olioiden kesken, sillä ne eivät kuulu yhdellekään oliolle. Jos yksi olio muuttaa luokkansa staattisen muuttujan arvoa, tämä muutos näkyy kaikissa olioissa. Vastaavasti staattiset aliohjelmat eivät voi nähdä yksittäisen olion tilaa edes silloin, kun niitä kutsutaan jonkin olion sisältä, sillä ne eivät kuulu yhdellekään oliolle. Staattiset aliohjelmat pääsevät toki käsiksi kaikkiin staattisiin muuttujiin.

Staattisuutta voi ajatella yksinkertaistettuna niin, että staattisesta muuttujasta on ohjelman muistissa vain yksi ilmentymä, eikä siitä koskaan voida tehdä enempää, joten se täytyy jakaa kaikkien kesken. Staattisia aliohjelmia voisi myös ajatella olevan vain se yksi kappale, jota ei voi kiinnittää minkään olion tilaan.

Katsotaan muutamaa esimerkkiä.

```java

```

Koska staattiset aliohjelmat eivät kuulu millekään oliolle, niiden sisällä ei myöskään voi käyttää `this`-viitettä. Tutustutaan tähän seuraavaksi.

## this-viite

TODO:

## Olion elinkaari

Olion elinkaari lyhyesti; olion rakenne määritellään ensin luokalla. Ohjelman ajon aikana luokasta luodaan ilmentymä eli olio. Olion luonnin yhteydessä sille varataan ensin sopiva tila Javan virtuaalikoneen kekomuistista. Tyypiltään sopiva viitemuuttuja asetetaan osoittamaan tähän muistipaikkaan. Olioon päästään käsiksi viitemuuttujan kautta ja sen tilaa voidaan tarkastella ja muokata metodien avulla. Viitemuuttujat tuhoutuvat, kun niiden näkyvyysalue loppuu. Kun olioon ei enää ole yhtään viitettä olemassa, myös olio tuhoutuu. Javassa ohjelmoijan ei tarvitse itse pitää huolta muistin varaamisesta tai vapauttamisesta. Tuhoutuneiden olioiden varaama muisti vapautetaan lopulta Javan automaattisen roskienkeräyksen toimesta.

Käydään vielä olion koko elinkaari läpi esimerkkien avulla. Tarvitsemme olioiden luomista varten ensimmäiseksi luokan. Tehdään esimerkkejä varten yksinkertainen luokka `Henkilo`, johon voimme tallentaa henkilön nimen ja syntymävuoden.

```java
public class Henkilo {
    private String nimi; // Nimen oletusarvo on null, sillä kyseessä on viitemuuttuja.
    private int syntymavuosi; // Syntymävuoden oletusarvo on 0, sillä kyseessä on kokonaislukumuuttuja.

    // Parametriton muodostaja. Tämä täytyy määritellä, koska olemme määritelleet muodostajan, jolla on parametreja.
    public Henkilo() {
        // Jos emme alusta attribuutteja täällä, yllä mainitut oletusarvot pysyvät voimassa tämän muodostajan avulla luoduilla olioilla.
    }

    // Parametrillinen muodostaja.
    public Henkilo(String nimi, int vuosi) {
        this.nimi = nimi;
        this.syntymavuosi = vuosi;
    }

    public String getNimi() { 
        return nimi; 
    }

    public void setNimi(String nimi) { 
        this.nimi = nimi; 
    }

    public int getSyntymavuosi() { 
        return syntymavuosi; 
    }

    public void setSyntymavuosi(int vuosi) { 
        this.syntymavuosi = vuosi; 
    }
}
```

Olion luominen tapahtuu new-avainsanalla. Se varaa muistista oliolle sopivan tilan, valitsee ja suorittaa sopivan muodostajan, ja palauttaa viitteen juuri luotuun olioon. Sijoitamme tämän viitten muuttujaan, jotta pääsemme olioon sitä kautta käsiksi. Viitemuuttujan tyyppi kertoo, _minkälainen_ olio muistisijainnissa täytyy olla - eli mitä _luokkaa_ se edustaa. Käytämme siis luokkaa muuttujan tyyppinä.

On tärkeää pitää mielessä, että viitemuuttuja ja olio ovat kaksi eri asiaa. Viitemuuttuja on kuin nuoli, joka voi osoittaa olioon. Sen ei kuitenkaan ole pakko osoittaa mihinkään, jolloin sen arvo on null. Olio on vastaavasti mahdollista luoda ilman siihen viittaavaa muuttujaa, mutta jos olioon osoittavia viitteitä ei ole, siihen ei päästä käsiksi ja se tuhoutuu. Useampi viitemuuttuja voi viitata samaan olioon, mutta viitemuuttuja voi osoittaa vain yhteen olioon kerrallaan. Voimme toki tehdä listan viitteistä, joista jokainen osoittaa eri olioon. Tämä onkin täysin tavallista, kun teemme listan "olioista".

Määrittelimme `Henkilo`-luokassa, että parametriton muodostaja antaa oletusasetukset, kun taas parametrillinen muodostaja alustaa tilan annettujen arvojen perusteella. Käytetään molempia muodostajia luomaan eri olioita ja kerrataan samalla hieman viitemuuttujien käyttöä:

```java
void main() {
    // Voimme luoda viitemuuttujan ilman että se viittaa mihinkään olioon. Oliota ei tässä luoda.
    Henkilo h0 = null;

    // Tässä luodaan olio ja sijoitetaan viite h0-muuttujaan. Kääntäjä valitsee käytettäväksi parametrittoman perusmuodostajan, sillä muodostajalle ei anneta argumentteja.
    h0 = new Henkilo(); 

    // Tässä luodaan olio, mutta viitettä ei sijoiteta mihinkään. Emme pääse tähän olioon enää käsiksi ja se merkitään tuhottavaksi.
    new Henkilo();

    // Yleensä on suoraviivaisempaa esitellä viitemuuttuja ja luoda siihen sijoitettava olio yhdessä.
    Henkilo h1 = new Henkilo();

    // Voimme käyttää parametrillista muodostajaa antamalla muodostajalle parametreja vastaavat arvot - nimi ja syntymävuosi.
    Henkilo h2 = new Henkilo("Anna", 1995);

    // Tämä ei käy, sillä emme määritelleet luokalle muodostajaa, jolla on vain nimi parametrina.
    // Henkilo h3 = new Henkilo("Mikko");

    // Voimme luoda toisenkin viitteen Anna-olioon. Sekä h2 että h3 osoittavat nyt samaan olioon.
    Henkilo h3 = h2;
}
```

Kun olemme luoneet olioita, voimme tarkastella ja muokata niiden tilaa ohjelman suorituksen aikana. Jatketaan hieman yllä olevan esimerkin pohjalta ja tarkastellaan olioiden tilaa.

```java
void main() {
    Henkilo h1 = new Henkilo();
    Henkilo h2 = new Henkilo("Anna", 1995);

    IO.println(h1.getNimi()); // Tämä tulostaa "null", sillä parametriton muodostaja ei alusta nimeä millään tavalla.
    IO.println(h1.getSyntymavuosi()); // Tämä vastaavasti tulostaa "0". Alustamattoman kokonaisluvun oletusarvo on Javassa 0.

    IO.println(h2.getNimi()); // Tulostaa "Anna"
    IO.println(h2.getSyntymavuosi()); // // Tulostaa "1995"

    // Annetaan nyt ensimmäiselle henkilölle oikea nimi ja syntymävuosi.
    h1.setNimi("Joni");
    h1.setSyntymavuosi(1995);

    // Olion tila on muuttunut ja saamme nyt uudet arvot tulostumaan.
    IO.println(h1.getNimi());
    IO.println(h1.getSyntymavuosi());
}
```

Tarkastellaan lopuksi olioiden elinkaaren loppua, eli niiden tuhoutumista. Kun olioon ei enää ole yhtään viitettä, se merkitään "roskaksi", jonka Javan automaattinen roskienkeräys (engl. *garbage collection*) voi aikanaan poistaa muistista vapauttaen sitä varten varten varatun tilan.

```java
void main() {
    // Luomme taas kaksi oliota.
    Henkilo h1 = new Henkilo();
    Henkilo h2 = new Henkilo("Anna", 1995);

    // Muuttuja h1 on tällä hetkellä ainoa viite ensimmäiseen olioon.
    // Jos sijoitamme h1-muuttujaan jonkin muun viitten tai asetamme sen arvoksi null, ensimmäinen olio merkitään tuhottavaksi, sillä siihen ei ole enää viitteitä.
    h2 = null;

    // Aliohjelman näkyvyysalueen päättyessä kaikki sen sisällä luodut lokaalit muuttujat (h1 ja h2) tuhoutuvat.
    // Tässä tapauksessa olioihin ei ole enää muita viitteitä, joten nekin tuhoutuvat.
}
```

Emme tällä kurssilla perehdy kovin syvällisesti Javan automaattiseen roskienkeräykseen tai muistin hallintaan. Tämän kurssin kannalta riittää, että tiedämme milloin olio muuttuu roskaksi ja tuhoutuu. Jos haluat tutustua aiheeseen hieman tarkemmin, voit aloittaa lukemalla täältä [täältä](https://www.geeksforgeeks.org/java/jvm-heap-area/) lisää kekomuistista ja sen varaamisesta sekä [täältä](https://www.geeksforgeeks.org/java/garbage-collection-in-java/) Javan roskienkeräyksestä suhteellisen helposti lähestyttävässä muodossa.

### Olioiden vertaileminen

Jokaisella oliolla on oma identiteetti. Vaikka kahden olion tilat olisivat täysin samat, ne eivät silti ole sama olio. Tämä aiheuttaa toisinaan hieman päänvaivaa olio-ohjelmointiin tutustumisen alkuvaiheissa. Olemme tottuneet vertailemaan muuttujien arvoja `==`-operaattorilla (pl. liukuluvut), mutta tämä ei toimi olioiden tapauksessa toivotulla tavalla, sillä se vertaa itse asiassa olioiden *identiteettiä*. Sama koskee myös `!=`-operaattoria.

Katsotaan, mitä tämä käytännössä tarkoittaa ottamalla taas esimerkiksi yksinkertaistettu `Henkilo`-luokka:

```java
public class Henkilo {
    private String nimi;
    private int syntymavuosi;

    public Henkilo() {}

    public Henkilo(String nimi, int vuosi) {
        this.nimi = nimi;
        this.syntymavuosi = vuosi;
    }

    // ...
}

void main() {
    Henkilo h1 = new Henkilo("Anna", 1995);
    Henkilo h2 = new Henkilo("Anna", 1995);
    Henkilo h3 = h1; // Viittaa samaan olioon kuin h1.

    IO.println(h1 == h2); // False. Olioilla on sama sisältö (tila), mutta ne eivät ole sama olio.
    IO.println(h1 == h3); // True. Molemmat viitteet osoittava samaan olioon, eli identiteetti on sama.
}
```

Parempi tapa vertailla olioita on käyttää `equals`-metodia. Metodista on jo toteutus olemassa kaikilla olioilla (palaamme tähän seuraavassa osassa), mutta valitettavasti Java ei voi tietää, kuinka itse luomiemme luokkien yhdenvertaisuus määritellään, joten meidän täytyy toteuttaa se itse. Lisätään sellainen `Henkilo`-luokkaamme.

```java
public class Henkilo {
    private String nimi;
    private int syntymavuosi;

    public Henkilo() {}

    public Henkilo(String nimi, int vuosi) {
        this.nimi = nimi;
        this.syntymavuosi = vuosi;
    }

    // ...

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;

        // Vertaillaan olioita ominaisuuksien perusteella ja palautetaan true, jos oliot voidaan tulkita yhdenvertaisiksi.
        Henkilo toinen = (Henkilo)obj;
        return Objects.equals(nimi, toinen.nimi) && syntymavuosi == toinen.syntymavuosi;
    }
}

void main() {
    Henkilo h1 = new Henkilo("Anna", 1995);
    Henkilo h2 = new Henkilo("Anna", 1995);

    IO.println(h1 == h2); // False. Olioilla on edelleen eri identiteetti.
    IO.println(h1.equals(h2)); // True

    IO.println(Objects.equals(h1, h2));
}
```

Metodista on olemassa myös staattinen versio `Objects.equals`, joka on turvallisempi käyttää tietyissä tilanteissa. Jos viitemuuttuja `h1` olisi arvoltaan `null` eli ei osoittaisi mihinkään olioon, emme voisi yrittää kutsua olion `equals`-metodia normaalisti. `Objects.equals` kuitenkin vaatii myös `equals`-metodin toteutuksen toimiakseen oikein.

```java
void main() {
    Henkilo h1 = new Henkilo("Anna", 1995);
    Henkilo h2 = new Henkilo("Anna", 1995);
    Henkilo h3 = null;

    IO.println(Objects.equals(h1, h2)); // True
    IO.println(Objects.equals(h3, h1)); // False

}
```

Joidenkin Javan sisäänrakennettujen oliotyyppien tapauksessa `==`-operaattori *voi* toimia, vaikka edellä mainitun perusteella sen ei pitäisi. Esimerkiksi kokonaislukujen oliotyyppi `Integer` sekä erityisesti merkkijono `String`. Java pyrkii välttämään täysin samanlaisten olioiden luomista turhaan uudelleenkäyttämällä saman sisällön omaavia, muuttumattomia olioita parhaansa mukaan. Tämä on melko yleinen ominaisuus ohjelmointikielissä. Voit halutessasi lukea lisää aiheesta täältä; [*string interning*](https://www.geeksforgeeks.org/java/interning-of-string/). Varmuuden vuoksi on paras käyttää aina olion `equals`-metodia tai `Objects.equals`-funktiota.

TODO: HUOM! Jos toteutamme oman `equals`-metodin, meidän täytyy toteuttaa myös luokalle oma `toHash`-metodi.

TODO: compareTo ja Objects.compare

TODO: getClass() ja instanceOf

### Olioiden yhteistoiminta

TODO: Siirrä osan 2.3 loppuun, käytetään kapselointia ja näkyvyysmääritteitä

Olemme tähän mennessä käyttäneet selkeyden vuoksi esimerkeissä lähinnä yhtä luokkaa kerrallaan. Olioiden hyödyt tulevat kuitenkin paremmin esille, kun alamme rakentamaan ohjelmaan useampia luokkia, jotka toimivat yhdessä. Jos olio-ohjelmoinnin ideana on, että olio sisältää yhteen kuuluvat tiedot ja toiminnallisuudet, eri luokat voisivat siis olla vastuussa vain niille kuuluvista asioista. Voimme käyttää tätä käytäntöä organisoimaan koodia paremmin.

Oliot voivat toimia yhdessä eri tavoin. Oliot voivat sisältää toisia olioita - tai tarkemmin ilmaistuna viitteitä toisiin olioihin. Kun olio koostuu olioista, joista jokainen tuo oman toiminnallisuutensa, tätä kutsutaan usein kompositioksi. Oliot voivat kutsua toistensa metodeja ja näin delegoida tehtäviä toiselle oliolle, jolle tehtävän vastuu kuuluu, tai kommunikoida esimerkiksi tapahtumien yhteydessä. Oliot voivat myös sisältää kokoelmia olioista - esimerkiksi Javan sisäänrakennetut tietorakenteet ovat olioita, jotka sisältävät kokoelman olioista.

Katsotaan esimerkkiä, jossa haluamme mallintaa ohjelmallamme rakennuksia, niissä sijaitsevia tiloja sekä tiloihin tehtäviä varauksia. Jokaisessa rakennuksessa voi olla monta tilaa ja jokaisessa tilassa voi olla monta varausta. Emme välitä vielä tässä esimerkissä siitä, voiko varauksia olla samassa tilassa päällekkäin. Pidetään myös luokat vielä suhteellisen yksinkertaisina.

Aloitetaan määrittelemällä tarvittavat luokat `Rakennus`, `Tila` ja `Varaus`.

```java
public class Rakennus {
    private String nimi;
    // ...
}

public class Tila {
    private String nimi;
    // ...
}

public class Varaus {
    private String varaaja;
    private boolean peruttu;
    // ...
}

void main() {

}
```

TODO: Kompositio (rakennus -> tila -> varaus)

TODO: Delegointi (peru kaikki rakennuksen tapahtumat)

TODO: Tapahtumat ja viestit?
