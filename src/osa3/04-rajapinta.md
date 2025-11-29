## Rajapinta

> [!Osaamistavoitteet]
> - Ymmärrät, mitä rajapinta (interface) tarkoittaa olio-ohjelmoinnissa.
> - Osaat määritellä ja käyttää rajapintoja Javassa.
> - Ymmärrät, milloin kannattaa käyttää rajapintaa perinnän sijaan.

*Rajapinta* toimii sitovana sopimuksena: Se määrittelee, mitä metodeja luokan on tarjottava, ottamatta kantaa siihen, miten ne on teknisesti toteutettu. Toisin kuin abstrakti luokka, joka luo pohjan luokan metodeille ja attribuuteille, rajapinta keskittyy kuvailemaan olion kyvykkyyksiä. Rajapinta mahdollistaa yhtenevän kyvykkyyksien määrittelyn, vaikka luokat olisivat täysin erilaisia tai periytyisivät eri paikoista luokkahierarkiassa. Kun ohjelmoija sitten käsittelee oliota rajapinnan kautta, hän voi luottaa siihen, että olio tarjoaa sovitun kyvykkyyden riippumatta siitä, mitä luokkaa olio edustaa.

Tehdään pieni ajatusharjoitus. Kuvittele kotisi seinässä olevaa pistorasiaa. Pistorasia tarjoaa sähkövirtaa, mutta se ei anna sitä mihin tahansa. Se vaatii, että laitteessa on sopiva pistotulppa, joka sopii pistorasiaan.

Tässä analogiassa rajapinta on se standardi (sopimus), jonka laitteen täytyy täyttää, jotta se voi käyttää pistorasiaa. Asiaa voidaan tarkastella myös niin päin, että *jos* laitteessa on standariin pistorasiaan sopiva pistotulppa, niin sillä *täytyy* olla kyky toimia siinä tilanteessa, että se kytketään pistorasiaan. 

Pistorasiaa ei kiinnosta, kytketkö siihen pölynimurin vai leivänpaahtimen.
Laitteet ovat itse asiassa täysin erilaisia, eikä niillä ole yhteistä "esi-isää" laitehierarkiassa samalla tavalla kuin vaikkapa Auto ja Moottoripyörä voisivat periä luokan Ajoneuvo. Toinen tekee ruokaa, toinen siivoaa. Ainoa pölynimuria ja leivänpaahdinta yhdistävä tekijä on kyky kytkeytyä verkkovirtaan.

Jos yrittäisimme mallintaa tämän perinnällä, joutuisimme ongelmiin heti, kun haluaisimme käyttää vaikkapa pölynimuria. Onko pölynimuri `Sähkölaite`, `Siivouslaite`, vai kenties molempia? Javassa luokka ei kuitenkaan voi periä kahta yliluokkaa. 

Rajapinta ratkaisee tämän ongelman tyylikkäästi: 
 * `Pölynimuri` on `Siivouslaite` (perintä), mutta se myös *toteuttaa*  `Verkkovirtalaite`-rajapinnan. 
 * Samoin `Leivänpaahdin` voisi olla vaikkapa `Keittiölaite` (perintä), joka myöskin toteuttaa saman `Verkkovirtalaite`-rajapinnan.

Näin pistorasia voi hyväksyä kumman tahansa laitteen, koska molemmat täyttävät sopimuksen eli toteuttavat rajapinnan vaatiman kytkennän.

Toteutamme tämän esimerkin koodina hieman myöhemmin, mutta otetaan ensin hieman toisenlainen esimerkki.

> [!HUOMAUTUS]
> TODO : Toistaiseksi jätetty mainitsematta: 
>  - Javan versiosta 8 alkaen rajapinnat voivat sisältää myös metodien oletustoteutuksia.

## Älykoti

Jotkin älykotimme laitteet voisivat olla säädettäviä, eli niillä voisi asettaa suoraan arvon, kuten kirkkauden, lämpötilan tai äänenvoimakkuuden. Näinhän periaatteessa toimimmekin jo esimerkkimme `Valo`-luokassa, jossa kirkkaus vaihtelee kolmen arvon välillä. Olion käyttäjän kannalta olisi kuitenkin kätevämpää, jos voisi asettaa kirkkauden suoraan haluttuun arvoon (esim. 33%), sen sijaan, että pitäisi kutsua `vaihdaTilaa()`-metodia useita kertoja ja toivoa, että arvo osuu kohdalleen. Loppukäyttäjän kannalta tätä voisi verrata tilanteeseen, jossa käyttäjä voisi asettaa vaikkapa mobiilisovelluksesta suoraan haluamansa kirkkauden sen sijaan, että pitäisi klikkailla *Lisää kirkkautta*- tai *Vähennä kirkkautta* -painikkeita useita kertoja. 

Määritellään rajapinta `Saadettava`, jossa on metodi `asetaArvo(int arvo)`. Tiedosto tallennetaan nimellä `Saadettava.java`, eli samaan tapaan kuin luokat.

```java,ignore
public interface Saadettava {
    void asetaArvo(int arvo);
}
```

Tämän voi lukea seuraavasti: Jokaisella `Saadettava`-rajapinnan toteuttavalla luokalla tulee olla `asetaArvo`-metodi.

Nyt voimme muokata `Valo`-luokkaa toteuttamaan `Saadettava`-rajapinnan:

Lisätään `Valo`-luokkaan rajapinnan toteutus:

```java
// FILE: Valo.java
public class Valo extends Laite implements Saadettava {
    private int kirkkaus = 0;

    @Override
    public void asetaArvo(int arvo)
    {
        if (arvo < 0) arvo = 0;
        if (arvo > 100) arvo = 100;
        this.kirkkaus = arvo;
    }

    @Override
    public void vaihdaTilaa() {
        // Yksinkertainen päälle-pois
        if (kirkkaus == 100) kirkkaus = 0;
        else kirkkaus = 100;
    }

    @Override
    public void raportoiTila() {
        IO.println("Valon kirkkaus on " + kirkkaus + "%.");
    }
}
// FILE_END
// FILE: Laite.java
public abstract class Laite {
    abstract public void vaihdaTilaa();

    abstract public void raportoiTila();
}
// FILE_END
// FILE: Saadettava.java
public interface Saadettava {
    void asetaArvo(int arvo);
}
// FILE_END
// FILE: main.java
public class Main {
    public static void main() {
        Valo valo = new Valo();
        valo.asetaArvo(33);
        valo.raportoiTila();

        valo.vaihdaTilaa();
        valo.raportoiTila();
    }
}
// FILE_END
```

## Usean rajapinnan toteuttaminen

Luokka voi toteuttaa useita rajapintoja. Esimerkiksi Javan sisäänrakennettu `ArrayList`-luokka toteuttaa rajapintoja: `List`, `RandomAccess`, `Cloneable` ja `Serializable` (ks. myös [`ArrayList`-luokan dokumentaatio](https://docs.oracle.com/javase/8/docs/api/java/util/ArrayList.html)).

 * `List`-rajapinta määrittelee listan perustoiminnot, kuten elementtien lisäämisen, poistamisen ja hakemisen.
 * `RandomAccess`-rajapinta määrittelee, että listan alkioihin tulee päästä käsiksi nopeasti indeksien avulla. 
 * `Cloneable`-rajapinta sallii olion kloonauksen eli kopioinnin.
 * `Serializable`-rajapinta sallii olion tallentamisen tiedostoon tai lähettämiseen verkon yli.

Luodaan nyt itse kaksi rajapintaa ja luokkia, jotka toteuttaa molemmat rajapinnat.

Otetaan esimerkki käyttöliittymäkomponenteista, joita voi piirtää näytölle ja joita voi klikata hiirellä. Määritellään kaksi rajapintaa: `Piirrettava` ja `Klikattava`. Näiden rajapintojen avulla voitaisiin määritellä, millaisia komponentteja käyttöliittymässä on. Sovitaan niin, että piirrettävä komponentti osaa piirtää itsensä, ja klikattava komponentti osaa käsitellä klikkauksia ja korostaa itsensä, kun hiiri on sen päällä. 

```java,ignore
// FILE: Piirrettava.java
/**
 * Käyttöliittymään piirrettävä komponentti.
 */
public interface Piirrettava {
    public void piirra();
}
// FILE_END
// FILE: Klikattava.java
/**
 * Käyttöliittymän komponentti, jota voi klikata.
 */
public interface Klikattava {
    public void klikattu();

    public void asetaKorostus(boolean korostus);
}
// FILE_END
```

Huomaa, että emme tiedä emmekä välitä siitä, miten nämä metodit aikanaan toteutetaan. Piirto voi tapahtua graafisella käyttöliittymällä, tekstipohjaisella käyttöliittymällä tai vaikkapa tulostamalla tiedostoon. Meille riittää, että tiedämme, että jokaisella `Pirrettava`-rajapinnan toteuttavalla luokalla on `piirra()`-metodi, ja jokaisella `Klikattava`-rajapinnan toteuttavalla luokalla on `klikattu()`- ja `asetaKorostus(boolean korostus)`-metodit.

Mennään eteenpäin. Toteutetaan `Teksti`, joka on pelkkää tekstiä näyttävä käyttöliittymäkomponentti.

```java,ignore
/**
 * Pelkkää tekstiä esittävä piirrettävä komponentti.
 */
public class Teksti implements Piirrettava {
    private String sisalto;
    public Teksti(String sisalto)
    {
        this.sisalto = sisalto;
    }

    @Override
    public void piirra() {
        // Piirretään vain pelkkä tekstisisältö ilman kehyksiä
        IO.println(sisalto);
    }
}
```

Rajapintojen hyöty ei vielä kokonaisuudessaan välity, osittain siksi, että `piirra()`-metodi on ainoa metodi, jota `Piirrettava`-rajapinta tarjoaa. Nyt kuitenkin voimme luoda toisen komponentin, `Painike`, joka on laatikon näköinen klikkattava painike, jossa on tekstiä. `Painike`-luokka toteuttaa molemmat rajapinnat: `Pirrettava` ja `Klikattava`.

```java,ignore
/**
 * Laatikon näköinen klikkattava painike,
 * jossa on tekstiä.
 */
public class Painike implements Piirrettava, Klikattava {

    private String sisalto;
    private boolean korostettu;

    public Painike(String sisalto)
    {
        this.sisalto = sisalto;
        this.korostettu = false;
    }

    @Override
    public void piirra() {
        // Piirretään suorakulmio ja teksti
        if (!korostettu) {
            IO.println("[ " + sisalto + " ]");
        } else {
            IO.println("[*" + sisalto + "*]");
        }
    }

    /**
     * Käsitellään klikkaustapahtuma
     */
    @Override
    public void klikattu() {
        IO.println("(Klikattiin painiketta, jossa lukee \"" + sisalto + "\")");
    }

    /**
     * Asetetaan korostustila. Jos tila muuttuu, piirretään komponentti uudestaan.
     */
    @Override
    public void asetaKorostus(boolean korostus) {
        if (this.korostettu == korostus) {
            return;
        }
        this.korostettu = korostus;
        this.piirra();
    }
}
```

Nyt meillä on kaksi erilaista käyttöliittymäkomponenttia, jotka molemmat voidaan piirtää näytölle. `Painike`-komponentti on lisäksi klikattava. Käytetään näitä komponentteja pääohjelmassa.

```java
// FILE: Piirrettava.java
/**
 * Käyttöliittymään piirrettävä komponentti.
 */
public interface Piirrettava {
    public void piirra();
}
// FILE_END
// FILE: Klikattava.java
/**
 * Käyttöliittymän komponentti, jota voi klikata.
 */
public interface Klikattava {
    public void klikattu();

    public void asetaKorostus(boolean korostus);
}
// FILE_END
// FILE: Teksti.java
/**
 * Pelkkää tekstiä näyttävä komponentti.
 */
public class Teksti implements Piirrettava {
    private String sisalto;
    public Teksti(String sisalto)
    {
        this.sisalto = sisalto;
    }

    @Override
    public void piirra() {
        // Piirretään vain pelkkä tekstisisältö ilman kehyksiä
        IO.println(sisalto);
    }
}
// FILE_END
// FILE: Painike.java
/**
 * Laatikon näköinen klikkattava painike,
 * jossa on tekstiä.
 */
public class Painike implements Piirrettava, Klikattava {

    private String sisalto;
    private boolean korostettu;

    public Painike(String sisalto)
    {
        this.sisalto = sisalto;
        this.korostettu = false;
    }

    @Override
    public void piirra() {
        // Piirretään suorakulmio ja teksti
        if (!korostettu) {
            IO.println("[ " + sisalto + " ]");
        } else {
            IO.println("[*" + sisalto + "*]");
        }
    }

    /**
     * Käsitellään klikkaustapahtuma
     */
    @Override
    public void klikattu() {
        IO.println("(Klikattiin painiketta, jossa lukee \"" + sisalto + "\")");
    }

    /**
     * Asetetaan korostustila.
     */
    @Override
    public void asetaKorostus(boolean korostus) {
        this.korostettu = korostus;
    }
}
// FILE_END
// FILE: main.java
public class Main {
    public static void main(String[] args) {
        Teksti otsikko = new Teksti("Haluatko aloittaa rajapintojen opiskelun?");
        otsikko.piirra();

        Painike okPainike = new Painike("OK!");
        okPainike.piirra();

        // Simuloidaan hiiren vieminen painikkeen päälle
        // Korostamisen jälkeen piirretään painike uudestaan
        okPainike.asetaKorostus(true);
        okPainike.piirra();

        // Simuloidaan klikkaus
        okPainike.klikattu();
    }
}
// FILE_END
```

Jos haluat testata tätä koodia omalla koneellasi, voit ladata tämänkin esimerkin [GitHubista](https://github.com/ohj-perus-jy/ohj2-mdbook-esimerkit/tree/main/E32_Rajapinnat2/src).

<details closed><summary>✨ Valinnaista lisätietoa: Piirtämisvastuun siirtäminen pois komponenteista </summary>

Yllä oleva esimerkkimme on siinä mielessä aavistuksen epätodellinen, että käyttöliittymäkomponentit eivät yleensä huolehdi itse itsensä piirtämisestä, vaan piirtämisvastuu on usein erotettu muuhun osaan järjestelmää. Tällöin komponentit vain tarjoavat tiedot, jotka tarvitaan piirtämiseen, ja joku muu osa järjestelmää huolehtii siitä, että komponentit piirretään oikein näytölle (tai muuhun esitystapaan).

Muokataan esimerkkiämme tämän ajatuksen mukaisesti. Tehdään `Naytto`-luokka, joka pitää kirjaa kaikista näytöllä näkyvistä käyttöliittymäkomponenteista. 

```java,ignore
/**
 * Naytto-luokka hallinnoi piirrettäviä komponentteja.
 */
public class Naytto {
    private ArrayList<Piirrettava> komponentit = new ArrayList<>();

    public void lisaaKomponentti(Piirrettava p) {
        komponentit.add(p);
    }

    public void poistaKomponentti(Piirrettava p) {
        komponentit.remove(p);
    }
}
```

Tehdään myös `Piirturi`-luokka, joka toimii välikerroksena `Naytto`-luokan ja käyttöliittymäkomponenttien välillä. `Piirturi`-luokka huolehtii siitä, että komponentit piirretään oikein näytölle. Tässä esimerkissä ne tulostetaan konsolille, mutta oikeassa käyttöliittymässä ne piirrettäisiin graafiselle näytölle.

```java,ignore
/**
 * Piirturi-luokka vastaa piirtoalueen piirtämisestä.
 */
public class Piirturi {
    public void piirraPainike(String teksti, boolean korostettu) {
        if (!korostettu) {
            IO.println("[ " + teksti + " ]");
        } else {
            IO.println("[*" + teksti + "*]");
        }
    }

    public void piirraTeksti(String teksti) {
            IO.println(teksti);
    }

    public void tyhjaa() {
        IO.println("Tyhjennetään piirtoalue");
        // Jätetään tässä toteuttamatta        
    }
}
```

Nyt `Naytto`-luokka voi käyttää `Piirturi`-luokkaa piirtämään ne tarvittaessa. Lisätään `Naytto`-luokkaan metodi `paivita()`, joka käy läpi kaikki näytöllä olevat komponentit ja pyytää niitä piirtämään itsensä `Piirturi`-olion avulla.

```java,ignore
import java.util.ArrayList;

/**
 * Naytto-luokka hallinnoi piirrettäviä komponentteja.
 */
public class Naytto {
    private ArrayList<Piirrettava> komponentit = new ArrayList<>();
    // HIGHLIGHT_GREEN_BEGIN
    private Piirturi piirturi = new Piirturi();
    // HIGHLIGHT_GREEN_END

    public void lisaaKomponentti(Piirrettava p) {
        komponentit.add(p);
    }

    public void poistaKomponentti(Piirrettava p) {
        komponentit.remove(p);
    }

    // HIGHLIGHT_GREEN_BEGIN
    public void paivita() {
        piirturi.tyhjaa();
        for (Piirrettava p : komponentit) {
            p.piirra(piirturi);
        }
    }
    // HIGHLIGHT_GREEN_END
}
```

Huomaa, että `Piirrettava`-rajapinnan `piirra()`-metodin tulee nyt ottaa parametrina `Piirturi`-olio. Tämän avulla komponentit voivat käyttää `Piirturi`-oliota piirtämiseen.

```java,ignore
public interface Piirrettava {
    // HIGHLIGHT_GREEN_BEGIN
    public void piirra(Piirturi piirturi);
    // HIGHLIGHT_GREEN_END
}
```

Ja nyt se oleellinen kohta: Tämän seurauksena `Teksti`- ja `Painike`-luokkien `piirra()`-metodit eivät enää itse tulosta mitään, vaan ne kutsuvat `Piirturi`-olion metodeja.

```java,ignore
/**
 * Pelkkää tekstiä esittävä piirrettävä komponentti.
 */
public class Teksti implements Piirrettava {
    private String sisalto;
    public Teksti(String sisalto)
    {
        this.sisalto = sisalto;
    }

    /**
     * Piirrä komponentti
     * @param piirturi Piirturi
     */
    @Override
    // HIGHLIGHT_GREEN_BEGIN
    public void piirra(Piirturi piirturi) {
        piirturi.piirraTeksti(sisalto);
    }
    // HIGHLIGHT_GREEN_END
}
```

Vastaava muutos tulee tehdä `Painike`-luokkaan.

Tässä meidän yksinkertaisessa esimerkissämme kaikki tietysti tapahtuu konsolille tulostamalla, mutta oikeassa graafisessa käyttöliittymässä `Piirturi`-luokka voisi käyttää jotain graafista kirjastoa, kuten JavaFX:ää tai Swingiä.

Esimerkki on pitkähkö, ja jos haluat ajaa sen omalla tietokoneellasi, lataa se [GitHubista](https://github.com/ohj-perus-jy/ohj2-mdbook-esimerkit/tree/main/E32_Rajapinnat3/src).

</details>

## Rajapinta aliohjelman parametrina

Palataan nyt alussa esitettyyn `Verkkovirtalaite`-ajatukseen. 

Yksinkertaisimmillaan `Verkkovirtalaite`-rajapinnan sisältö olisi määritelmä siitä, että laitteen on pystyttävä reagoimaan siihen, kun se kytketään pistorasiaan ja virta alkaa kulkea johdossa. 

```java,ignore
public interface Verkkovirtalaite {
    // Tämä metodi on "pistotulppa". 
    // Kun pistorasia aktivoi tämän, laite saa sähköä.
    void kytkeVirta();
}
```

Nyt `Sirkkeli` ja `Leivanpaahdin` ovat aivan eri puolelta luokkahierarkiaa (toinen on työkalu, toinen keittiölaite), mutta molemmat reagoivat virtaan omalla tavallaan.

`Tyokalu` ja `Keittiolaite` jätetään tässä esimerkissä määrittelmättä, mutta ne voisivat olla abstrakteja luokkia, jotka tarjoavat perustan työkalu- ja keittiölaitteille.

```java,ignore
// Sirkkeli on Työkalu, joka toimii verkkovirralla
public class Sirkkeli extends Tyokalu implements Verkkovirtalaite {
    
    @Override
    public void kytkeVirta() {
        // Sirkkelin oma tapa reagoida virtaan:
        System.out.println("Sirkkeli: Moottori alkaa pyörittää terää 4000 rpm.");
    }
}

// Leivänpaahdin on Keittiölaite, joka toimii verkkovirralla
public class Leivanpaahdin extends Keittiolaite implements Verkkovirtalaite {
    
    @Override
    public void kytkeVirta() {
        // Leivänpaahtimen oma tapa reagoida virtaan:
        System.out.println("Leivänpaahdin: Vastukset alkavat hehkua punaisena.");
    }
}
```

Tämä on tärkein kohta ymmärryksen kannalta. Pistorasia on luokka, joka **käyttää** rajapintaa.

```java,ignore
public class Pistorasia {
    
    // Pistorasiaan voi kytkeä MINKÄ TAHANSA verkkovirtalaitteen.
    // Pistorasiaa ei kiinnosta, onko se sirkkeli vai paahdin.
    public void kytkeLaite(Verkkovirtalaite laite) {
        System.out.println("--- Pistorasia antaa sähköä ---");
        
        // Pistorasia kutsuu sopimuksen mukaista metodia.
        // Tässä tapahtuu polymorfismi: 
        // laite reagoi oikealla, sille ominaisella tavalla.
        laite.kytkeVirta();
    }
}
```

## Rajapinta muuttujan tyyppinä

Jotta `Pistorasia`-luokka pääsisi tositoimiin, tarvitsemme vielä pääohjelman, jossa luomme `Pistorasia`-olion ja kytkemme siihen erilaisia laitteita. Luodaan nyt pääohjelma, jossa kytketään ensin `Leivanpaahdin` pistorasiaan.

> [!HUOMAUTUS]
> Jotta esimerkki ei leviäisi käsiin, oletamme tässä, että `Leivanpaahdin` ja `Sirkkeli`-luokat peritään jostakin järkevistä yliluokista, kuten `Keittiolaite` ja `Tyokalu`. Näitä yliluokkia ei ole määritelty tässä esimerkissä, koska ne eivät ole olennaisia rajapinnan kannalta ja vain monimutkaistaisivat esimerkkiä. Oleellista on, että ne edustavat eri puolilta luokkahierarkiaa olevia olioita, jotka molemmat toteuttavat saman rajapinnan.

```java
// FILE: main.java
public class KodinSahkot {

    public static void main(String[] args) {

        // 1. Luodaan infrastruktuuri: Pistorasia
        // Tässä kohtaa Pistorasia-olio syntyy tietokoneen muistiin.
        Pistorasia keittionPistoke = new Pistorasia();

        // 2. Luodaan laitteet
        Leivanpaahdin paahdin = new Leivanpaahdin();
        Sirkkeli sirkkeli = new Sirkkeli();

        // 3. Käytetään laitteita pistorasian kautta
        System.out.println("--- Aamu keittiössä ---");

        // Kytketään paahdin seinään
        keittionPistoke.kytkeLaite(paahdin);
        System.out.println("\n--- Remontti alkaa ---");

        // Kytketään sirkkeli SAMAAN pistorasiaan
        // Koska yhdessä pistorasiassa voi olla yksi laite kerrallaan,
        // paahdin irrotetaan, vaikka sitä ei erikseen
        // tässä esitetäkään.
        keittionPistoke.kytkeLaite(sirkkeli);
    }
}
// FILE_END
// FILE: Verkkovirtalaite.java
public interface Verkkovirtalaite {
    void kytkeVirta();
}
// FILE_END
// FILE: Leivanpaahdin.java
// Leivänpaahdin on Keittiölaite, joka toimii verkkovirralla
public class Leivanpaahdin implements Verkkovirtalaite {

    @Override
    public void kytkeVirta() {
        // Leivänpaahtimen oma tapa reagoida virtaan:
        System.out.println("Leivänpaahdin: Vastukset alkavat hehkua punaisena.");
    }
}
// FILE_END
// FILE: Sirkkeli.java
// Sirkkeli on Työkalu, joka toimii verkkovirralla
public class Sirkkeli implements Verkkovirtalaite {

    @Override
    public void kytkeVirta() {
        // Sirkkelin oma tapa reagoida virtaan:
        System.out.println("Sirkkeli: Moottori alkaa pyörittää terää 4000 rpm.");
    }
}
// FILE_END
// FILE: Pistorasia.java
public class Pistorasia {

    // Pistorasiaan voi kytkeä MINKÄ TAHANSA (yhden) verkkovirtalaitteen.
    // Pistorasiaa ei kiinnosta, onko se sirkkeli vai paahdin.
    public void kytkeLaite(Verkkovirtalaite laite) {
        System.out.println("--- Pistorasia antaa sähköä ---");

        // Pistorasia kutsuu sopimuksen mukaista metodia.
        // Tässä tapahtuu polymorfismi: oikea laite reagoi oikealla tavalla.
        laite.kytkeVirta();
    }
}
// FILE_END
```

Meidän ei olisi kuitenkaan pakko määritellä `paahdin`- ja `sirkkeli`-muuttujia omiksi tyypeikseen. Voisimme määritellä ne molemmat `Verkkovirtalaite`-tyyppisiksi, koska meitä kiinnostaa pistorasiaan kytkemisen näkökulmasta vain se, että ne toteuttavat kyseisen rajapinnan.

```java,ignore
public class KodinSahkot {

    public static void main(String[] args) {

        // 1. Luodaan infrastruktuuri: Pistorasia
        // Tässä kohtaa Pistorasia-olio syntyy tietokoneen muistiin.
        Pistorasia keittionPistoke = new Pistorasia();

        // 2. Luodaan laitteet
        // HIGHLIGHT_GREEN_BEGIN
        Verkkovirtalaite paahdin = new Leivanpaahdin();
        Verkkovirtalaite sirkkeli = new Sirkkeli();
        // HIGHLIGHT_GREEN_END

        // 3. Käytetään laitteita pistorasian kautta
        System.out.println("--- Aamu keittiössä ---");

        // Kytketään paahdin seinään
        keittionPistoke.kytkeLaite(paahdin);
        System.out.println("\n--- Remontti alkaa ---");

        // Kytketään sirkkeli SAMAAN pistorasiaan
        // Koska yhdessä pistorasiassa voi olla yksi laite kerrallaan,
        // paahdin irrotetaan, vaikka sitä ei erikseen
        // tässä esitetäkään.
        keittionPistoke.kytkeLaite(sirkkeli);
    }
}
```

Miksi on hyödyllistä määritellä rajapinta muuttujan tyypiksi? Yksi syy on se, että voimme nyt käsitellä erilaisia laitteita yhtenäisenä joukkona. Voimme esimerkiksi luoda listan erilaisista verkkovirtalaitteista ja kytkeä ne kaikki pistorasiaan silmukassa.

```java,ignore
List<Verkkovirtalaite> laitteet = List.of(
    new Leivanpaahdin(),
    new Sirkkeli(),
    new Imuri()
);

Pistorasia pistorasia = new Pistorasia();

for (Verkkovirtalaite v : laitteet) {
    pistorasia.kytkeLaite(v);
}
```

Jos jokainen laite olisi määritelty omaksi tyypikseen, meidän täytyisi kirjoittaa seuraavasti (oletetaan jälleen, että `Keittiolaite` ja `Tyokalu` ovat olemassa olevia yliluokkia).

```java,ignore
List<Keittiolaite> keittionLaitteet = ...;
List<Tyokalu> tyokalut = ...;

Pistorasia pistorasia = new Pistorasia();

for (Keittiolaite k : keittionLaitteet) {
    pistorasia.kytkeLaite(k);
}

for (Tyokalu t : tyokalut) {
    pistorasia.kytkeLaite(t);
}
```

Toinen syy on helppo vaihdettavuus, josta käytetään englanninkielistä termiä *loose coupling*. Kun koodi käyttää rajapintaa muuttujan tyyppinä, se ei ole sidottu tiettyyn toteutukseen. Tämä tarkoittaa, että voimme helposti vaihtaa yhden toteutuksen toiseen ilman, että meidän tarvitsee muuttaa koodia, joka käyttää kyseistä rajapintaa.

Kuvitellaan, että teemme ohjelmaa, joka testaa sähkölaitteita. Kun muuttuja määritellään rajapintana, voimme helposti luoda erilaisia testilaitteita, jotka toteuttavat saman rajapinnan, ja käyttää niitä testauksessa ilman, että meidän tarvitsee muuttaa testikoodia.

```java,ignore
Leivanpaahdin testattavaLaite = new Leivanpaahdin();

// .. suoritetaan laitteen testaus ..

// Vaihdetaan testattava laite toiseen toteutukseen
testattavaLaite = new Sirkkeli(); // Ei onnistu, koska tyypit eivät täsmää
```

Sen sijaan, jos määrittelemme muuttujan tyypiksi rajapinnan, voimme vaihtaa konkreettisen toteutuksen vapaasti.

```java,ignore
Verkkovirtalaite testattavaLaite = new Leivanpaahdin();
// .. suoritetaan laitteen testaus ..

// Vaihdetaan testattava laite toiseen toteutukseen
testattavaLaite = new Sirkkeli(); 

// Tämä onnistuu, koska molemmat toteuttavat 
// Verkkovirtalaite-rajapinnan
```

Kolmas syy liittyy ohjelmiston suunnitteluun ja käytännön kirjoittamiseen. Kun määrittelet muuttujan tyypiksi `Verkkovirtalaite`, kääntäjä estää sinua kutsumasta metodeja, jotka ovat spesifejä vain leivänpaahtimille (kuten `saadaKuumuus()`) tai sirkkelille (kuten `asetaTeranKorkeus()`). Vaikka tällainen itsensä rajoittaminen saattaa tuntua oudolta, se auttaa pitämään koodin selkeänä ja estää virheitä, joissa yritetään käyttää laitetta tavalla, joka ei ole yhteensopiva sen rajapinnan kanssa. 

## Abstrakti luokka vai rajapinta?

| Kysymys                              | Abstrakti luokka                              | Rajapinta                                                 |
| ------------------------------------ | --------------------------------------------- | --------------------------------------------------------- |
| Voiko sisältää attribuutteja?        | Kyllä                                         | Ei                                                        |
| Voiko sisältää metodien toteutuksia? | Kyllä                                         | Ei (Java v8 alkaen mahdollisuus ns. `default`-metodeihin) |
| Kuinka monta voi periä/toteuttaa?    | Luokka voi periä vain yhden abstraktin luokan | Luokka voi toteuttaa useita rajapintoja                   |
| Käyttötarkoitus                      | Yhteinen runko ja osittainen toteutus         | Yhteinen sopimus käyttäytymisestä                         |

Monesti molemmat yhdistyvät: abstrakti luokka tarjoaa rungon ja toteuttaa yhden tai useampia rajapintoja.

```java
// FILE: Säädettävä.java
public interface Saadettava {
    void asetaArvo(int arvo);
}
// FILE_END

// FILE: SaadettavaLaite.java
public abstract class SaadettavaLaite extends Laite implements Saadettava {
    protected int nykyinenArvo = 0;

    @Override
    public void raportoiTila() {
        IO.println("Nykyinen arvo: " + nykyinenArvo);
    }
}
// FILE_END

// FILE: Termostaatti.java
public class Termostaatti extends SaadettavaLaite {
    public Termostaatti() {
        super("Termostaatti");
    }

    @Override
    public void vaihdaTilaa() {
        nykyinenArvo = (nykyinenArvo + 1) % 5;
    }

    @Override
    public void asetaArvo(int arvo) {
        nykyinenArvo = Math.max(0, Math.min(arvo, 4));
    }
}
// FILE_END
```

`Termostaatti` saa valmiin `raportoiTila()`-metodin abstraktilta luokaltaan, mutta toteuttaa rajapinnan vaatimuksen (`asetaArvo`). Tämä osoittaa, miten abstrakti luokka ja rajapinta täydentävät toisiaan.

## Esimerkit

Löydät kaikki tällä sivulla esitellyt esimerkit [GitHubista](https://github.com/ohj-perus-jy/ohj2-mdbook-esimerkit) (E32-alkuiset kansiot).

## Tehtävät

Kesken.

<task>
  <task-title>Tehtävä 3.4: Abstraktit luokat. <points>1 p.</points> </task-title>
  <handout>

  {{#include ../exercises/3-4-abstrakti-luokka-1/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa3/tehtava4">Tee tehtävä TIMissä</a></task-link>
</task>

.

Suunnittele `Hälytettävä`-rajapinta, jossa on metodit `trigger()` ja `reset()`. Toteuta rajapintaa hyödyntävä abstrakti `HälytinLaite`, joka pitää kirjaa siitä, montako kertaa hälytys on aktivoitu. Luo kaksi konkreettista laitetta (esim. `SavuHälytin` ja `VesivuotoHälytin`). Mieti, missä kohtaa sijoitat yhteisen lokituksen: rajapintaan (ei mahdollista) vai abstraktiin luokkaan?
