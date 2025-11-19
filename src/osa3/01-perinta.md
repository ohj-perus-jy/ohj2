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

Perivästä luokasta käytetään termiä *aliluokka* (subclass) ja peritystä luokasta termiä *yliluokka* (superclass).

Javassa perintä toteutetaan käyttämällä `extends`-avainsanaa.

## Esimerkki

Käytännössä olioilla on usein yhteisiä piirteitä. Otetaan keksitty esimerkki henkilötietojärjestelmästä: Maija Opiskelija, Olli Opettaja ja Satu Sihteeri voisivat kaikki olla olioita kuvitteellisessa Kisu-opintotietojärjestelmässä. Kaikilla näillä on kaikille käyttäjille tyypillisiä ominaisuuksia, kuten nimi ja käyttäjätunnus. Jokaisen pitäisi myös päästä kirjautumaan sisään järjestelmään ja sieltä ulos. 

Kullakin käyttäjällä on kuitenkin myös omia erityispiirteitään: Opiskelijalla voisi olla lista kursseista, joille hän on ilmoittautunut, sekä hänen suorittamansa opintopisteet. Opettajalla on kurssit, joita hän opettaa sekä tehtävänimike, mutta hänellä ei ole opintopisteitä. Sihteeri on vastuussa opintosuoritusten kirjaamisesta ja tutkinnon antamisesta, mutta hänellä ei ole opiskelijanumeroa tai opetettavia kursseja.

Lähdetään kuitenkin aluksi liikkeelle pienesti -- opiskelijasta ja opettajasta. Alla on `Opiskelija`- ja `Opettaja`-luokat, joihin olemme tehneet pari attribuuttia ja metodia. Tutki näitä luokkia.

> [!VAROITUS]
> Alla oleva esimerkki on tarkoitettu havainnollistamaan perinnän syntaksia, eikä siitä syystä noudata (vielä) parhaita käytäntöjä, kuten tiedon kapselointia. Erityisesti nimen asettaminen julkisella `setNimi`-metodilla rikkoo kapseloinnin periaatetta. Korjaamme tämän asian kuitenkin esimerkin edetessä.

```java
// FILE: Opiskelija.java  
import java.util.ArrayList;

class Opiskelija {
    private String nimi;
    private ArrayList<String> kaynnissaOlevatKurssit;

    public Opiskelija() {
        this.kaynnissaOlevatKurssit = new ArrayList<>();
    }

    String getNimi() {
        return this.nimi;
    }

    void setNimi(String nimi) {
        this.nimi = nimi;
    }

    void naytaOpintoOhjelma() {
        String kurssit = String.join(", ", kaynnissaOlevatKurssit);
        IO.println(this.nimi + " opiskelee kursseilla: " + kurssit);
    }

    void ilmoittauduKurssille(String kurssi) {
        IO.println(this.nimi + " ilmoittautui kurssille: " + kurssi);
        kaynnissaOlevatKurssit.add(kurssi);
    }

}
// FILE_END  

// FILE: Opettaja.java  
import java.util.ArrayList;

class Opettaja {
    private String nimi;
    private ArrayList<String> opetettavatKurssit;

    public Opettaja() {
        this.opetettavatKurssit = new ArrayList<>();
    }

    String getNimi() {
        return this.nimi;
    }

    void setNimi(String nimi) {
        this.nimi = nimi;
    }

    void naytaOpetettavatKurssit() {
        String kurssit = String.join(", ", opetettavatKurssit);
        IO.println(this.nimi + " opettaa kursseja: " + kurssit);
    }

    void lisaaKurssi(String kurssi) {
        opetettavatKurssit.add(kurssi);
    }
}

// FILE_END  

//FILE: main.java  
public class Main {
    public static void main() {
        Opiskelija opiskelija = new Opiskelija();
        opiskelija.setNimi("Olli Opiskelija");
        opiskelija.ilmoittauduKurssille("Ohjelmointi 2");

        Opettaja opettaja = new Opettaja();
        opettaja.setNimi("Maija Opettaja");
        opettaja.lisaaKurssi("Ohjelmointi 1");
        opettaja.lisaaKurssi("Ohjelmointi 2");
        opettaja.naytaOpetettavatKurssit();
    }
}
// FILE_END  
```

Huomaat, että kummassakin luokassa on samat attribuutti `nimi` sekä metodit `getNimi` ja `setNimi`. Näiden luokkien välillä on toki myös eroja, mutta nimen omaan toisto on ongelmallista, koska:

 * jokaisessa luokassa on määriteltävä samat ominaisuudet ja toiminnot uudelleen, 
 * jos haluamme muuttaa jotain yhteistä ominaisuutta tai toimintoa, meidän täytyy tehdä se kolmessa eri paikassa,
 * uuden luokan lisääminen, jolla on samat ominaisuudet, vaatii saman koodin kopioimisen uudelleen taas uuteen paikkaan.

Jos nyt haluaisimme muuttaa esimerkiksi `nimi`-attribuuttia niin, että `etunimi` ja `sukunimi` tallennetaan erikseen kahteen attribuuttiin, meidän pitäisi tehdä tämä muutos kaikissa näissä luokissa. Tämä lisää virheiden mahdollisuutta ja tekee koodin ylläpidosta hyvin hankalaa. Yksi ohjelmistokehityksen periaatteista onkin *älä toista itseäsi* (*Don't Repeat Yourself*, lyh. DRY; ks. [Wikipedia](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)). 

## Luokkahierarkia

Toistamisen välttämiseksi voimme luoda yliluokan nimeltä `Henkilo`, joka sisältää kaikki yhteiset ominaisuudet ja toiminnot. Sitten `Opiskelija` ja `Opettaja` voivat *periä* `Henkilo`-luokan, jolloin ne saavat *automaattisesti* kaikki sen määrittelemät ominaisuudet ja metodit. Näin voimme lisätä vain erityispiirteet kuhunkin aliluokkaan ilman koodin toistamista.

Toteutetaan nyt yllä kuvattu tilanne uudestaan niin, että kirjoitetaan kaikissa luokissa esiintyvät ominaisuudet ja toiminnot *uuteen* `Henkilo`-luokkaan, ja muut luokat perivät kyseisen luokan.

```java
// FILE: Henkilo.java
public class Henkilo {
    String nimi;

    String getNimi()
    {
        return this.nimi;
    }

    void setNimi(String nimi) {
        this.nimi = nimi;
    }
}
// FILE_END
// FILE: Opiskelija.java
import java.util.ArrayList;

class Opiskelija extends Henkilo {
    private ArrayList<String> kaynnissaOlevatKurssit;

    public Opiskelija() {
        this.kaynnissaOlevatKurssit = new ArrayList<>();
    }

    void naytaOpintoOhjelma() {
        String kurssit = String.join(", ", kaynnissaOlevatKurssit);
        IO.println(this.nimi + " opiskelee kursseilla: " + kurssit);
    }

    void ilmoittauduKurssille(String kurssi) {
        IO.println(this.nimi + " ilmoittautui kurssille: " + kurssi);
        kaynnissaOlevatKurssit.add(kurssi);
    }
}
// FILE_END
// FILE: Opettaja.java
import java.util.ArrayList;

class Opettaja extends Henkilo {
    private ArrayList<String> opetettavatKurssit;

    public Opettaja() {
        this.opetettavatKurssit = new ArrayList<>();
    }

    void naytaOpetettavatKurssit() {
        String kurssit = String.join(", ", opetettavatKurssit);
        IO.println(this.nimi + " opettaa kursseja: " + kurssit);
    }

    void lisaaKurssi(String kurssi) {
        opetettavatKurssit.add(kurssi);
    }
}
// FILE_END
// FILE: main.java
public class Main {
    public static void main() {
        Opiskelija opiskelija = new Opiskelija();
        opiskelija.setNimi("Olli Opiskelija");
        opiskelija.ilmoittauduKurssille("Ohjelmointi 2");

        Opettaja opettaja = new Opettaja();
        opettaja.setNimi("Maija Opettaja");
        opettaja.lisaaKurssi("Ohjelmointi 1");
        opettaja.lisaaKurssi("Ohjelmointi 2");
        opettaja.naytaOpetettavatKurssit();
    }
}
// FILE_END
``` 

Huomaa, että `Opiskelija`- ja `Opettaja`-luokat eivät enää määrittele `nimi`--attribuuttia tai `getNimi`- ja `setNimi`-metodeja, koska ne perivät nämä `Henkilo`-luokasta, eikä sitä koodia enää tarvitse uudelleen kirjoittaa. Tämä tekee koodista huomattavasti siistimpää ja helpommin ylläpidettävää.

Periytymistä voidaan kuvata alla olevan tapaisella kuviolla. Tässä `Henkilo` on yliluokka (superclass) ja `Opiskelija` ja `Opettaja` ovat aliluokkia (subclasses), jotka perivät `Henkilo`-luokan ominaisuudet ja metodit.

```mermaid
classDiagram
    Henkilo <|-- Opiskelija
    Henkilo <|-- Opettaja
```

Yllä oleva kuvio on tehty mukaillen niin sanottua UML-kuvauskieltä (engl. *Unified Modelling Language*). Tarkkaan ottaen UML:ssä kunkin luokan kohdalle lisätään myös muutakin tietoa, kuten attribuuttien ja metodien nimet ja tieto näkyvyydestä. Jätämme ne kuitenkin tässä esimerkissä yksinkertaisuuden vuoksi pois ja käytämme UML:ää tässä sopivasti soveltaen; palaamme UML:ään tarkemmin myöhemmissä osissa.

## Rakentajat ja super-avainsana

Yllä olevassa esimerkissämme on pari ongelmaa. Ensinnäkin, `Henkilo`-luokassa ei ole rakentajaa, nimen alustaminen tapahtuu `setNimi`-metodin kautta. Tämän seurauksena olioiden luomisen seurauksena `nimi`-attribuutti on aina `null`, ennen kuin se asetetaan erikseen. Tämä ei ole hyvä käytäntö kahdestakin syystä: Ensinnäkin, on parempi, että olio on käyttökelpoinen heti luomisen jälkeen ilman, että erillisiä asettamisia tarvitsee tehdä. Toiseksi, nimen asettaminen julkisen `setNimi`-metodin kautta ei ole hyvä idea, sillä nimen asettaminen suoraan luokan ulkopuolelta ei pitäisi olla sallittua, vaan se pitäisi tapahtua huomattavasti hallitumman prosessin kautta. 

Asetetaan aluksi nuo `Henkilo`-luokan attribuutit yksityisiksi. Lisätään sitten `Henkilo`-luokkaan rakentaja, joka ottaa `nimi`-parametrin, ja alustaa attribuutin arvon vastaavasti. Tämän jälkeen voimme poistaa `setNimi`-metodin kokonaan, jolloin nimen asettaminen onnistuu vain rakentajan kautta. Muutetaan olioiden rakentaminen pääohjelmassa vastaamaan tätä uutta rakentajaa.

```java,noplayground
// FILE: Henkilo.java
class Henkilo {

    // HIGHLIGHT_GREEN_BEGIN
    private String nimi;

    public Henkilo(String nimi) {
        this.nimi = nimi;
    }
    // HIGHLIGHT_GREEN_END

    // HIGHLIGHT_RED_BEGIN
    void setNimi(String nimi) {
        this.nimi = nimi;
    }
    // HIGHLIGHT_RED_END

    public String getNimi() {
        return this.nimi;
    }
}
// FILE_END
// FILE: main.java
public class Main {
    public static void main() {
        // HIGHLIGHT_GREEN_BEGIN
        Opiskelija opiskelija = new Opiskelija("Matti Meikäläinen", "matti123");        
        // HIGHLIGHT_GREEN_END
        // HIGHLIGHT_RED_BEGIN
        opiskelija.setNimi("Matti Meikäläinen");
        // HIGHLIGHT_RED_END
        opiskelija.ilmoittauduKurssille("Ohjelmointi 2");
        opiskelija.naytaKurssit();

        // ...
    }
}
// FILE_END
```

Nyt koska `Henkilo`-luokassa on määritelty rakentaja, joka ottaa parametreja, Java ei enää luo oletusrakentajaa automaattisesti, mikä aiheuttaa käännösvirheen. 
Tässä tuleekin tärkeä huomio: Ne luokat, jotka perivät `Henkilo`-luokan, eivät peri sen rakentajaa.
Tämän vuoksi meidän on lisättävä myös `Opiskelija`, `Opettaja` ja `Sihteeri`-luokkiin rakentajat vastaamaan tätä muutosta. 

Toisaalta nyt kun määrittelimme `nimi`-attribuutin yksityiseksi, emme voi myöskään asettaa niitä perivästä luokasta käsin, esimerkiksi seuraavasti.

```java,noplayground
class Opiskelija extends Henkilo {
    public Opiskelija(String nimi) {
        this.nimi = nimi;               
        // Käännösvirhe: nimi ja kayttajatunnus ovat yksityisiä!
    }
}
```

Ainoa tapa tallentaa arvot näihin attribuutteihin on tehdä se kutsumalla aliluokasta yliluokan rakentajaa ja välittämällä tuossa kutsussa tarvittavat parametrit.
Tämä kutsuminen toteutetaan käyttämällä `super`-avainsanaa. Tehdään tämä muutos kumpaankin aliluokkaan.

```java
// FILE: Henkilo.java
class Henkilo {
    private String nimi;

    public Henkilo(String nimi)
    {
        this.nimi = nimi;
    }

    public String getNimi()
    {
        return nimi;
    }
}
// FILE_END
// FILE: Opiskelija.java
import java.util.ArrayList;
class Opiskelija extends Henkilo {
    // HIGHLIGHT_GREEN_BEGIN
    private ArrayList<String> kaynnissaOlevatKurssit;
    // HIGHLIGHT_GREEN_END

    // HIGHLIGHT_GREEN_BEGIN
    public Opiskelija(String nimi) {
        super(nimi);
        kaynnissaOlevatKurssit = new ArrayList<>();
    }
    // HIGHLIGHT_GREEN_END

    void ilmoittauduKurssille(String kurssi) {
        kaynnissaOlevatKurssit.add(kurssi);
    }

    public void naytaKurssit(){
        String kaikkiKurssit = String.join(", ", kaynnissaOlevatKurssit);
        IO.println(this.nimi + " opiskelee kursseilla: " + kaikkiKurssit);
    }
}
// FILE_END
// FILE: Opettaja.java
import java.util.ArrayList;
class Opettaja extends Henkilo {
    // HIGHLIGHT_GREEN_BEGIN
    private ArrayList<String> opetettavatKurssit;
    // HIGHLIGHT_GREEN_END

    // HIGHLIGHT_GREEN_BEGIN
    public Opettaja(String nimi)
    {
        super(nimi);
        this.opetettavatKurssit = new ArrayList<>();
    }
    // HIGHLIGHT_GREEN_END

    void lisaaKurssi(String kurssi) {
        opetettavatKurssit.add(kurssi);
    }

    void naytaOpetettavatKurssit() {
        String kurssit = String.join(", ", opetettavatKurssit);
        IO.println(this.nimi + " opettaa kursseja: " + kurssit);
    }
}
// FILE_END
// FILE: main.java
public class Main {
    public static void main() {
        Opiskelija opiskelija = new Opiskelija("Olli Opiskelija");
        opiskelija.ilmoittauduKurssille("Ohjelmointi 2");
        opiskelija.naytaKurssit();

        Opettaja opettaja = new Opettaja("Maija Opettaja");
        opettaja.lisaaKurssi("Ohjelmointi 1");
        opettaja.lisaaKurssi("Ohjelmointi 2");
        opettaja.naytaOpetettavatKurssit();
    }
}
// FILE_END
```

Jatketaan vielä esimerkkiä hieman pidemmälle. 

Oletetaan, että järjestelmässämme olisi kahdenlaisia opiskelijoita: Tutkinto-opiskelijoita sekä Avoimen yliopiston opiskelijoita. Tutkinto-opiskelijalla on oma tutkinto-ohjelma, kun taas Avoimen opiskelijalla ei ole tutkinto-ohjelmaa. Toisaalta Avoimen opiskelijan täytyy suorittaa maksu ennen kuin hän voi saada opintopisteitä. Toteutetaan nämä luokat perimällä `Opiskelija`-luokasta.

```java,noplayground
// FILE: TutkintoOpiskelija.java
class TutkintoOpiskelija extends Opiskelija {
    private String tutkintoOhjelma;
    
    // Rakentaja tässä välissä... (jätetty pois tilan säästämiseksi)
}
// FILE_END
// FILE: AvoinOpiskelija.java
class AvoinOpiskelija extends Opiskelija {
    private boolean maksutSuoritettu;

    // Rakentaja tässä välissä... (jätetty pois tilan säästämiseksi)

    void suoritaMaksu(double summa) {
        // Otetaan yhteys maksujärjestelmään ja käsitellään maksu ...
        // Kun on todennettu, että maksu on suoritettu:
        maksutSuoritettu = true;
    }
}
// FILE_END
```

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

Perintäsuhteesta käytetään englanninkielistä termiä *is-a*-suhde. Voimmekin sanoa, että `Opiskelija` *on* `Henkilo`, `Opettaja` *on* `Henkilo` ja `Sihteeri` *on* `Henkilo` -- nimen omaan näin päin. Edelleen, myös `TutkintoOpiskelija` *on* `Henkilo`, koska se perii `Opiskelija`-luokan, joka puolestaan perii `Henkilo`-luokan. 

Tämän ansiosta voimme käsitellä `Opiskelija`, `Opettaja` ja `Sihteeri`-olioita koodissamme `Henkilo`-tyyppisinä, kun ei ole tarpeen tietää tarkasti, minkä tyyppisiä olioita käsittelemme. Tämä on hyödyllistä esimerkiksi silloin, kun haluamme käsitellä erilaisia henkilöitä yhtenä ryhmänä, esimerkiksi lisäämällä kaikki tekemämme oliot `Henkilo`-taulukkoon:

```java,noplayground
Opiskelija opiskelija = new Opiskelija();
Opettaja opettaja = new Opettaja();
Sihteeri sihteeri = new Sihteeri();

Henkilo[] henkilot = {opiskelija, opettaja, sihteeri};
```

Nyt koska `Henkilo`-luokassa on määritelty muun muassa `kirjauduUlos()`-metodi, voimme kutsua tätä metodia kaikille `henkilot`-taulukon olioille ilman, että meidän tarvitsee tietää tarkasti, minkä tyyppisiä olioita taulukossa on:

```java,noplayground
for (Henkilo henkilo : henkilot) {
    henkilo.kirjauduUlos();
}
```

Huomionarvoista on *is-a*-suhteen suunta; `Opettaja` ei ole `Sihteeri`, vaikkakin molemmat perivät `Henkilo`-luokan. Javassa on mahdollista tarkistaa, onko olio tietyn luokan ilmentymä käyttämällä `instanceof`-operaattoria:

```java,noplayground
Henkilo[] henkilot = {opiskelija, opettaja, sihteeri};
for (Henkilo henkilo : henkilot) {
    IO.println("Käsitellään henkilöä: " + henkilo.nimi);
    if (henkilo instanceof Opettaja) {
        IO.println(henkilo.nimi + " on opettaja.");
    }
}
```

Huomautetaan vielä, että `super`-avainsanalla kutsutaan nimen omaan luokan välitöntä yliluokkaa. Luokkarakenteessa "yli hyppiminen" ei ole mahdollista. Esimerkiksi `TutkintoOpiskelija`-luokan rakentaja voisi kutsua vain `Opiskelija`-luokan rakentajaa, ei `Henkilo`-luokan rakentajaa.

## Ylikirjoittaminen

Perityn luokan metodeja voidaan *ylikirjoittaa* (engl. *override*) aliluokassa, mikä tarkoittaa, että aliluokka voi määritellä oman version peritystä metodista. Tämä on hyödyllistä, kun haluamme muuttaa perityn metodin käyttäytymistä aliluokassa.

Lisätään yllä olevaan `Opiskelija`-esimerkkimme attribuutti `boolean opintoOikeusVoimassa`, joka ilmaisee, onko opiskelijalla voimassa oleva opinto-oikeus. Jos opinto-oikeus ei ole voimassa, opiskelija ei voi kirjautua järjestelmään. Ylikirjoitetaan `kirjaudu()`-metodi `Opiskelija`-luokassa tarkistamaan tämä ehto ennen kirjautumista.

```java,noplayground
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

Voidaan ajatella, että ylikirjoitettu metodi korvaa tai piilottaa yliluokan metodin aliluokassa. Tähän liittyy pari sääntöä: 

 * Ylikirjoittaminen korvaa aina hierarkiassa lähimmän yliluokan metodin.
 * Aliluokassa metodin kutsuminen viittaa aina lähimpään ylikirjoitettuun versioon.

Alla oleva kuva havainnollistaa ylikirjoittamisen periaatetta:

![](images/override_.svg)

## Object-luokka

Javassa kaikilla luokilla on yhteinen yliluokka nimeltä `Object`. Tämä tarkoittaa, että kaikki luokat perivät automaattisesti `Object`-luokan ominaisuudet ja metodit, ellei toisin määritellä. `Object`-luokassa on useita hyödyllisiä metodeja, joita voidaan ylikirjoittaa aliluokissa.

Yksi tyypillinen tapa käyttää ylikirjoittamista on muokata `Object`-luokan [`toString()`-metodia](https://docs.oracle.com/javase/8/docs/api/java/lang/Object.html#toString--), joka tarjoaa olion merkkijonoesityksen. Oletusarvoisesti `toString()` palauttaa olion luokan nimen ja sen hajautusarvon, mikä ei ole kovin informatiivista. Voimme ylikirjoittaa tämän metodin omassa luokassamme, jotta se palauttaa juuri meidän tarpeisiimme sopivan merkkijonoesityksen. Lisätään `toString()`-metodi `Henkilo`-luokkaan.

```java,noplayground
class Henkilo {

    // ...

    @Override
    public String toString() {
        return "Henkilö: " + nimi + ", Käyttäjätunnus: " + kayttajatunnus;
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

Tehtävä 1

Tee luokkahierarkia ajoneuvoille. Yliluokasta `Ajoneuvo` periytyvät aliluokat `Auto`, `Moottoripyora` ja `Polkupyora`. 

Määrittele yhteiset ominaisuudet (`nopeus`, `paino`) ja metodit (`kiihdyta()`, `jarruta()`) `Ajoneuvo`-luokassa. Määrittele myös renkaiden lukumäärä, jonka tulee olla vakio. 

Kiihdyttäminen kasvattaa ajoneuvon nopeutta ja jarruttaminen vähentää sitä. 

<!-- Käyttövoima voi olla esimerkiksi "bensiini", "sähkö" tai "reisilihakset". TODO: Tehdäänkö tästä enum? -->

Lisää erityispiirteitä kuhunkin aliluokkaan:

 * `Auto`: `ovienLukumaara`
 * `Moottoripyora`: `sivuvaunu`
 * `Polkupyora`: `vaihteidenLukumaara`

Testaa luokkia luomalla olioita ja kutsumalla metodeja. Dokumentoi luokat ja metodit huolellisesti.

Tehtävä 2

Laajenna edellistä ajoneuvojen luokkahierarkiaa lisäämällä uusi aliluokka `Sähköauto`, joka perii `Auto`-luokasta. Lisää `Sähköauto`-luokkaan ominaisuus `akunKapasiteetti` ja metodi `lataaAkku()`, joka simuloi akun lataamista. Jos akku on täynnä, ei ladata enää lisää. 

Testaa kumpaakin auto-luokkaa luomalla niistä olio ja kutsumalla metodeja.

Bonus 1

Lisää `Auto`-luokalle vakio `RANGE_MAX`, joka ilmaisee maksimietäisyyden kilometreinä, jonka auto voi kulkea yhdellä latauksella tai tankkauksella. Lisää `Auto`-luokkaan metodi `tankkaaKayttovoimaa()`, joka lisää ajoneuvolle käyttövoimaa (bensiiniä tai sähköä). 

Lisää sitten `Sahkoauto`-luokkaan attribuutti `akunKunto` (prosentteina; väliltä 0-100) sekä `range` (kilometreinä). Kun autoa ladataan, akun kunto heikkenee 0.1%:lla jokaisella latauskerralla. Niinpä `range` tulee laskea akun kunnon perusteella `akunKunto` / 100 * `RANGE_MAX`.

## Lähteitä
 
<https://docs.oracle.com/javase/tutorial/java/concepts/inheritance.html>

<https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html>