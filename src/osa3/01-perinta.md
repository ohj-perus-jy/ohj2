# Perintä

> [!Osaamistavoitteet]
>
> - Perintä ("Kissa on Eläin", metodin ylikirjoitus, protected, luokkahierarkia)
> - Käytetään perintää olioiden yhteistyössä
> - Ymmärrät miten luokat ja oliot voivat periä toistensa ominaisuuksia
> - Ymmärrät miten metodeja voi ylikirjoittaa luokan sisällä ja luokkien yli
> - Ylikirjoitus, @Override, final
> - Osaat luoda yksinkertaisen luokkahierarkian, jossa luokka perii toisen luokan ja ylikirjoittaa sen metodeja
> - Konkreettinen esimerkki: Javan Object-luokka ja sen ylikirjoitettavat metodit
>    - Ymmärtää, että kaikki Javan luokat perivät `Object`-luokasta
>    - Tuntee hyödylliset ylikirjoitettavat metodit `Object`-luokassa: `equals`, `toString`, (ehkä `hashCode`?)

## Määritelmä

*Perintä* tarkoittaa mekanismia, jossa luokkaan voidaan sisällyttää toisen luokan ominaisuuksia ja toiminnallisuuksia. Tämä mahdollistaa koodin uudelleenkäytön ja luokkien välisen hierarkian luomisen. 

Perivästä luokasta käytetään termiä *aliluokka* (engl. *subclass*) ja peritystä luokasta termiä *yliluokka* (engl. *superclass*).

Javassa perintä toteutetaan käyttämällä `extends`-avainsanaa.

## Esimerkki

Käytännössä olioilla on usein yhteisiä piirteitä ja toimintoja. Otetaan keksitty esimerkki eläinklinikkajärjestelmästä: `Kissa`, `Koira` ja `Marsu` voisivat kaikki olla olioita kuvitteellisessa Kisu-klinikkajärjestelmässä. Kaikilla näillä on eläimille yhteisiä ominaisuuksia, kuten nimi, paino ja energia. Jokaisella on myös yhteisiä toimintoja, kuten syöminen (joka kasvattaa painoa ja lisää energiaa), äänteleminen (eläin kertoo nimensä) ja liikkuminen (vähentää energiaa).

Kullakin eläimellä on kuitenkin myös omia erityispiirteitään: Kissalla on hännän pituus, koiralla rotu ja säkäkorkeus, marsulla juoksupyörän koko, lempiruoka ja karvan väri. 
Kissa saalistaa hiiriä, koira noutaa keppejä ja marsu kaivaa tunneleita. (Ominaisuudet ja toiminnot ovat tässä tietenkin vain esimerkkejä, eivätkä ole välttämättä järkeviä tai kattavia.) 

Voisimme nyt luoda kolme erillistä luokkaa: `Kissa`, `Koira` ja `Marsu`. Tutki alla olevia luokkia, niissä olevia attribuutteja ja metodeja. 

### [Kissa.java](#tab/kissa)

```java
class Kissa {
    String nimi;
    double ika;
    double paino;
    double energia;

    String hannanPituus;

    void syo() {
        IO.println(nimi + " syö.");
        paino += 0.1;
        energia += 10;
    }

    void aantele() {
        IO.println("Miau!, sanoo " + nimi + ".");
    }

    void liiku() {
        IO.println(nimi + " loikkii aidan päällä.");
        energia -= 5;
    }

    void saalista() {
        IO.println(nimi + " saalistaa hiiriä.");
        energia -= 15;
    }
}
```

***

### [Koira.java](#tab/koira)

```java
class Koira {
    String nimi;
    double ika;
    double paino;
    double energia;

    void syo() {
        IO.println(nimi + " syö.");
        paino += 0.1;
        energia += 10;
    }

    void aantele() {
        IO.println("Hau!, sanoo " + nimi + ".");
    }

    void liiku() {
        IO.println(nimi + " juoksee pihalla.");
        energia -= 5;
    }

    void nouda() {
        IO.println(nimi + " noutaa kepin.");
        energia -= 10;
    }
}
```

***

### [Marsu.java](#tab/marsu)

```java
class Marsu {
    String nimi;
    double ika;
    double paino;
    double energia;

    void syo() {
        IO.println(nimi + " syö.");
        paino += 0.05;
        energia += 5;
    }

    void aantele() {
        IO.println("Pii!, sanoo " + nimi + ".");
    }

    void liiku() {
        IO.println(nimi + " juoksee juoksupyörässä.");
        energia -= 3;
    }

    void kaiva() {
        IO.println(nimi + " kaivaa tunnelia.");
        energia -= 8;
    }
}
```

*** 

Huomaat, että kaikissa kolmessa luokassa on samat attribuutit `nimi` ja `kayttajatunnus`, sekä sama metodi `kirjaudu()`. Toki näiden luokkien välillä on myös eroja, mutta tämä toisto on ongelmallista, koska:

 * jokaisessa luokassa on määriteltävä samat ominaisuudet ja toiminnot uudelleen, 
 * jos haluamme muuttaa jotain yhteistä ominaisuutta tai toimintoa, meidän täytyy tehdä se kolmessa eri paikassa,
 * uuden luokan lisääminen, jolla on samat ominaisuudet, vaatii saman koodin kopioimisen uudelleen taas uuteen paikkaan.

Jos nyt haluaisimme muuttaa esimerkiksi `nimi`-attribuuttia niin, että `etunimi` ja `sukunimi` tallennetaan erikseen kahteen attribuuttiin, meidän pitäisi tehdä tämä muutos kaikissa näissä luokissa. Tämä lisää virheiden mahdollisuutta ja tekee koodin ylläpidosta hyvin hankalaa. 

## Luokkahierarkia

Toistamisen välttämiseksi voimme luoda yliluokan nimeltä `Henkilo`, joka sisältää kaikki yhteiset ominaisuudet ja toiminnot. Sitten `Opiskelija`, `Opettaja` ja `Sihteeri` voivat *periä* `Henkilo`-luokan, jolloin ne saavat *automaattisesti* kaikki sen määrittelemät ominaisuudet ja metodit. Näin voimme lisätä vain erityispiirteet kuhunkin aliluokkaan ilman koodin toistamista.

Toteutetaan nyt yllä kuvattu tilanne uudestaan niin, että kirjoitetaan kaikissa luokissa esiintyvät ominaisuudet ja toiminnot *uuteen* `Henkilo`-luokkaan, ja muut luokat perivät kyseisen luokan.

### [Henkilo.java](#tab/henkilo)

```java
class Henkilo {
    String nimi;
    String kayttajatunnus;
    boolean kirjautunut;

    void kirjaudu() {
        kirjautunut = true;
    }

    void kirjauduUlos() {
        kirjautunut = false;
    }
}
```

***

### [Opiskelija.java](#tab/opiskelija-extends)

```java
class Opiskelija extends Henkilo {
    List<String> kurssit;
    int opintopisteet;

    void ilmoittauduKurssille(String kurssi) {
        // Kurssille ilmoittautumisen logiikka
    }
}
```

***

### [Opettaja.java](#tab/opettaja-extends)

```java
class Opettaja extends Henkilo {
    String tehtavanimike;
    List<String> opetettavatKurssit;

    void lisaaKurssi(String kurssi) {
       // Kurssin lisäämisen logiikka
    }
}
``` 

***

### [Sihteeri.java](#tab/sihteeri-extends)

```java
class Sihteeri extends Henkilo {

    void kirjaaOpintosuoritus(String opiskelija, String kurssi) {
        // Opintosuorituksen kirjaamisen logiikka
    }
}
```    

*** 

Huomaa, että `Opiskelija`, `Opettaja` ja `Sihteeri`-luokat eivät enää määrittele `nimi`- ja `kayttajatunnus`-attribuutteja tai `kirjaudu()`-metodia, koska ne perivät nämä `Henkilo`-luokasta, eikä sitä koodia enää tarvitse uudelleen kirjoittaa. Tämä tekee koodista huomattavasti siistimpää ja helpommin ylläpidettävää.

Periytymistä voidaan kuvata alla olevan tapaisella kuviolla. Tässä `Henkilo` on yliluokka (superclass) ja `Opiskelija`, `Opettaja` ja `Sihteeri` ovat aliluokkia (subclasses), jotka perivät `Henkilo`-luokan ominaisuudet ja metodit.

```mermaid
classDiagram
    Henkilo <|-- Opiskelija
    Henkilo <|-- Opettaja
    Henkilo <|-- Sihteeri
```

> [!TODO]
> Tässä esimerkissä on vielä se ongelma jatkon kannalta, että `Henkilo`-luokka itsessään on melko yleinen, eikä siitä ainakana tässä esimerkissä ole mielekästä luoda suoria ilmentymiä. Voisi olla fiksua keksiä sellainen esimerkki, jossa myös kantaluokka on konkreettinen ja ilmentymien tekemiselle on tarve. 

Yllä oleva kuvio on tehty mukaillen niin sanottua UML-kuvauskieltä (engl. Unified Modelling Language). Tarkkaan ottaen UML:ssä kunkin luokan kohdalle lisätään myös muutakin tietoa, kuten attribuuttien ja metodien nimet ja tieto näkyvyydestä. Jätämme ne kuitenkin tässä esimerkissä yksinkertaisuuden vuoksi pois ja käytämme UML:ää tässä sopivasti soveltaen; palaamme UML:ään tarkemmin myöhemmissä osissa.

Jatketaan vielä esimerkkiä hieman pidemmälle. Oletetaan, että järjestelmässämme olisi kahdenlaisia opiskelijoita: Tutkinto-opiskelijoita sekä Avoimen yliopiston opiskelijoita. Tutkinto-opiskelijalla on oma tutkinto-ohjelma, kun taas Avoimen opiskelijalla ei ole tutkinto-ohjelmaa. Toisaalta Avoimen opiskelijan täytyy suorittaa maksu ennen kuin hän voi saada opintopisteitä. Toteutetaan nämä luokat perimällä `Opiskelija`-luokasta.

### [TutkintoOpiskelija.java](#tab/tutkinto-opiskelija)

```java
class TutkintoOpiskelija extends Opiskelija {
    String tutkintoOhjelma;
}
```

***

### [AvoinOpiskelija.java](#tab/avoin-opiskelija)

```java
class AvoinOpiskelija extends Opiskelija {
    boolean maksutSuoritettu;

    void suoritaMaksu(double summa) {
        // Otetaan yhteys maksujärjestelmään ja käsitellään maksu ...
        // Kun on todennettu, että maksu on suoritettu:
        maksutSuoritettu = true;
    }
}
```

***

Luokkahierarkia näyttäisi nyt seuraavalta:

```mermaid
classDiagram
    class Henkilo
    Henkilo <|-- Opiskelija
    Henkilo <|-- Opettaja
    Henkilo <|-- Sihteeri
    Opiskelija <|-- TutkintoOpiskelija
    Opiskelija <|-- AvoinOpiskelija
``` 

Kun luokka perii toisen luokan, tästä suhteesta käytetään englanninkielistä termiä *is-a*-suhde. Voimmekin sanoa, että `Opiskelija` *on* `Henkilo`, `Opettaja` *on* `Henkilo` ja `Sihteeri` *on* `Henkilo` -- nimen omaan näin päin. Edelleen, myös `TutkintoOpiskelija` *on* `Henkilo`, koska se perii `Opiskelija`-luokan, joka puolestaan perii `Henkilo`-luokan. 

Kuitenkin, `Opettaja` ei ole `Sihteeri`, vaikkakin molemmat perivät `Henkilo`-luokan. 

## Rakentajat ja super-avainsana

Kun aliluokka perii yliluokan, sen on usein tarpeen kutsua yliluokan rakentajaa alustamaan perityt ominaisuudet. Tämä tehdään käyttämällä `super`-avainsanaa aliluokan rakentajassa.

Yllä olevassa esimerkissämme emme kirjoittaneet rakentajia, joten ne sisälsivät vain parametrittoman oletusrakentajan. Lisätään nyt `Henkilo`-luokkaan rakentaja, joka ottaa `nimi`- ja `kayttajatunnus`-parametrit, ja päivitetään `Opiskelija`-luokan rakentaja kutsumaan tätä yliluokan rakentajaa.

### [Henkilo.java](#tab/henkilo-rakentaja)

```java
class Henkilo {

    // ...

    public Henkilo(String nimi, String kayttajatunnus) {
        this.nimi = nimi;
        this.kayttajatunnus = kayttajatunnus;
    }
}
```

***

### [Opiskelija.java](#tab/opiskelija-rakentaja)

```java
class Opiskelija extends Henkilo {

    // ...

    public Opiskelija(String nimi, String kayttajatunnus) {
        super(nimi, kayttajatunnus); // Kutsutaan yliluokan rakentajaa
        this.kurssit = new ArrayList<>();
        this.opintopisteet = 0;
    }
}
```

***

Vastaavasti voisimme lisätä rakentajat myös `Opettaja`- ja `Sihteeri`-luokkiin, jotka kutsuvat `Henkilo`-luokan rakentajaa samalla tavalla. 

`super`-avainsanalla kutsutaan nimen omaan luokan välitöntä yliluokkaa, "yli hyppiminen" ei ole mahdollista. Esimerkiksi `TutkintoOpiskelija`-luokan rakentaja voisi kutsua vain `Opiskelija`-luokan rakentajaa, ei suoraan `Henkilo`-luokan rakentajaa.

## Ylikirjoittaminen

Perityn luokan metodeja voidaan *ylikirjoittaa* (override) aliluokassa, mikä tarkoittaa, että aliluokka voi määritellä oman version peritystä metodista. Tämä on hyödyllistä, kun haluamme muuttaa perityn metodin käyttäytymistä aliluokassa.

Lisätään yllä olevaan `Opiskelija`-esimerkkimme attribuutti `boolean opintoOikeusVoimassa`, joka ilmaisee, onko opiskelijalla voimassa oleva opinto-oikeus. Jos opinto-oikeus ei ole voimassa, opiskelija ei voi kirjautua järjestelmään. Ylikirjoitetaan `kirjaudu()`-metodi `Opiskelija`-luokassa tarkistamaan tämä ehto ennen kirjautumista.

```java
class Opiskelija extends Henkilo {

    // ...

    boolean opintoOikeusVoimassa;

    @Override
    void kirjaudu() {
        if (opintoOikeusVoimassa) {
            super.kirjaudu(); // Kutsutaan yliluokan kirjaudu-metodia
        } else {
            System.out.println("Opinto-oikeus ei ole voimassa. Et voi kirjautua.");
        }
    }
}
```

Muissa `Henkilo`-luokan aliluokissa, kuten `Opettaja` ja `Sihteeri`, `kirjaudu()`-metodi toimii edelleen alkuperäisellä tavalla, koska niitä ei ole ylikirjoitettu.

Yksi tyypillinen tapa käyttää ylikirjoittamista on muokata `toString()`-metodia, joka tarjoaa merkkijonoesityksen oliosta.
`toString()`-metodi on määritelty Javan `Object`-luokassa, josta kaikki luokat perivät. Voimme ylikirjoittaa tämän metodin omassa luokassamme, jotta se palauttaa luokallemme sopivan merkkijonoesityksen.

```java

class Opiskelija extends Henkilo {

    // ...

    @Override
    public String toString() {
        return "Opiskelija: " + nimi + ", Käyttäjätunnus: " + kayttajatunnus;
    }
}
```

## Final-avainsana

`final`-avainsanaa voidaan käyttää estämään luokan periminen tai metodin ylikirjoittaminen. Kun luokka on merkitty `final`-avainsanalla, sitä ei voi periä. Vastaavasti, kun metodi on merkitty `final`-avainsanalla, sitä ei voi ylikirjoittaa aliluokassa. 

## Näkyvyysmääreet

Java tarjoaa kolme pääasiallista näkyvyysmäärettä: `public`, `protected` ja `private`. Näkyvyysmääreet määrittelevät, mistä luokan jäseniin voidaan päästä käsiksi. 

Javassa oletuksena luokan jäsenet ovat ns. `package-private`-näkyvyydellä, mikä tarkoittaa, että ne ovat näkyvissä vain samassa paketissa oleville luokille. Alla olevassa taulukossa on yhteenveto eri näkyvyysmääreiden vaikutuksista; Oletus-sarake viittaa `package-private`-näkyvyyteen.

|                            | Luokka | Pakkaus | Aliluokka | Muu maailma |
| -------------------------- | ------ | ------- | --------- | ----------- |
| `public`                   | Kyllä  | Kyllä   | Kyllä     | Kyllä       |
| `protected`                | Kyllä  | Kyllä   | Kyllä     | Ei          |
| `package-private` (oletus) | Kyllä  | Kyllä   | Ei        | Ei          |
| `private`                  | Kyllä  | Ei      | Ei        | Ei          |

Ensimmäinen sarake ilmaisee, onko luokalla itsellään pääsy määritellyn näkyvyystason jäseneen. Kuten näet, luokalla on aina pääsy omiin jäseniinsä. Toinen sarake ilmaisee, onko luokilla, jotka ovat samassa pakkauksessa kuin kyseinen luokka (riippumatta niiden luokkarakenteesta), pääsy jäseneen. Kolmas sarake ilmaisee, onko luokasta perityillä aliluokilla, jotka sijaitsevat pakkauksen ulkopuolella, pääsy jäseneen. Neljäs sarake ilmaisee, onko millä tahansa luokalla pääsy jäseneen.

Jos ja kun muut ohjelmoijat (tai sinä itse) käyttävät tekemääsi luokkaa, näkyvyysmääreet auttavat varmistamaan, että luokkaasi käytetään sillä tavalla, jolla olet suunnitellut sen käytettävän. 
Pääsääntö on, että ohjelmoijan tulisi käyttää mahdollisimman rajoittavaa näkyvyysmäärettä -- mielellään `private`-määrettä -- ellei ole erityistä syytä käyttää jotain muuta. Tämä auttaa suojaamaan luokan sisäistä tilaa ja estämään tahalliset tai tahattomat väärinkäytökset luokan jäseniin. 
Vältä julkisia kenttiä, ellei kyseessä ole vakio. (Tässä materiaalissa saatetaan käyttää esimerkinomaisesti julkisia kenttiä. Tämä voi auttaa havainnollistamaan joitakin kohtia tiiviisti, mutta sitä ei suositella tuotantokoodissa.) 

... 

Muutetaan Henkilo-luokan `nimi`- ja `kayttajatunnus`-attribuutit `protected`-määritteisiksi:

```java
class Henkilo {
    public String nimi;
    protected String kayttajatunnus;

    public void kirjaudu() {
        // Kirjautumislogiikka
    }

    protected void muutaKayttajatunnus(String uusiTunnus) {
        this.kayttajatunnus = uusiTunnus;
    }
}
```

Nyt `nimi`-attribuutti näkyy myös muissa luokissa. Kuitenkin `kayttajatunnus`-attribuutin sisältämän arvon käyttäminen jostain muusta luokasta, joka ei ole `Henkilo`-luokan aliluokka, saamme käännösvirheen:

```java
class JokuMuuLuokka { 
    void jokuMetodi() {
        Henkilo henkilo = new Henkilo();
        henkilo.muutaKayttajatunnus("uusiTunnus"); // Käännösvirhe: ei pääsyä protected-jäseneen
    }
}
```

## Tehtävät

Tehtävä 1: Tee luokkahierarkia ajoneuvoille. Yliluokasta `Ajoneuvo` periytyvät aliluokat `Auto`, `Moottoripyora` ja `Polkupyora`. 

Määrittele yhteiset ominaisuudet (`nopeus`, `paino`, `kayttovoima`, `renkaidenLukumaara`)
ja metodit (`kiihdyta()`, `jarruta()`) `Ajoneuvo`-luokassa. 

Kiihdyttäminen kasvattaa ajoneuvon nopeutta ja jarruttaminen vähentää sitä. Käyttövoima voi olla esimerkiksi "bensiini", "sähkö" tai "reisilihakset". TODO: Tehdäänkö tästä enum?

Lisää erityispiirteitä kuhunkin aliluokkaan:

 * `Auto`: `ovienLukumaara`
 * `Moottoripyora`: `sivuvaunu`
 * `Polkupyora`: `vaihteidenLukumaara`

Testaa luokkia luomalla olioita ja kutsumalla metodeja.

Tehtävä 2: Laajenna edellistä ajoneuvojen luokkahierarkiaa lisäämällä uusi aliluokka `Sähköauto`, joka perii `Auto`-luokasta. Lisää `Sähköauto`-luokkaan ominaisuus `akunKapasiteetti` ja metodi `lataaAkku()`, joka simuloi akun lataamista. Jos akku on täynnä, ei ladata enää lisää. 

Testaa `Sähköauto`-luokkaa luomalla olio ja kutsumalla metodeja.

Bonus 1: TODO: Keksi tehtävä johon liittyy `final`-avainsanan käyttö. 

## Lähteitä
 
<https://docs.oracle.com/javase/tutorial/java/concepts/inheritance.html>

<https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html>