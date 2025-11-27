# Abstraktit luokat ja rajapinnat

> [!Osaamistavoitteet]
>
> - Abstrakti luokka tarjoaa osan toteutuksesta ja määrittelee "rajapinnan" sille, mitä perittävän luokan tulee toteuttaa itse. 
> - Abstraktit luokat (abstrakti metodi)
> - Ymmärrät, että abstraktista luokasta ei voi luoda luokan ilmentymiä

## Abstrakti luokka

*Abstrakti luokka* (engl. *abstract class*) on sellainen luokka, josta ei voi luoda suoria ilmentymiä. Sen sijaan se toimii pohjana muille luokille, jotka perivät sen. Abstrakti luokka voi sisältää sekä *abstrakteja metodeja* (ts. joilla ei ole toteutusta), että *konkreettisia metodeja* (ts. joilla on toteutus). Perivän luokan tulee sitten toteuttaa nuo abstraktit metodit, *ellei* perivä luokka ole myös abstrakti.

## Esimerkki

Älykodissa voisi olla monenlaisia laitteita, kuten valoja, turvakamera sekä tietysti älykahvinkeitin. Sovitaan, että kaikilla laitteilla olisi toiminto `vaihdaTilaa()`, joka suorittaa laitteen päätoiminnon (esim. valot syttyvät, kamera tallentaa videota, kahvinkeitin keittää kahvia). Kukin laite voisi myös raportoida oman tilansa `raportoiTila()`-metodilla.

Lähdemme tässä liikkeelle yksinkertaisesta esimerkistä, jossa laite voi vain vaihtaa tilaa, eikä esimerkiksi valita jotain erityistä tilaa. Palaamme monimutkaisempiin laitteiden säätömahdollisuuksiin myöhemmin. 

```mermaid
classDiagram
    class Laite 

    Laite <|-- Valo
    Laite <|-- Turvakamera
    Laite <|-- Kahvinkeitin
```

```java
//FILE: main.java
public class Main {
    public static void main() {
        Laite[] laitteet = {
            new Valo(),
            new Turvakamera(),
            new Kahvinkeitin()
        };

        for (Laite laite : laitteet) {
            laite.vaihdaTilaa();
            laite.raportoiTila();
        }
    }
}
// FILE_END
// FILE: Laite.java
public class Laite {
    public void vaihdaTilaa() {
    }

    public void raportoiTila() {
    }
}
// FILE_END
// FILE: Valo.java
public class Valo extends Laite {
    private int kirkkaus = 0;

    @Override
    public void vaihdaTilaa() {
        switch (kirkkaus) {
            case 0 -> kirkkaus = 50;
            case 50 -> kirkkaus = 100;
            case 100 -> kirkkaus = 0;
        }
    }
    @Override
    public void raportoiTila() {
        IO.println("Valon kirkkaus on " + kirkkaus + "%.");
    }
}
// FILE_END
// FILE: Turvakamera.java
public class Turvakamera extends Laite {
    private boolean tallennusPäällä = false;

    @Override
    public void vaihdaTilaa() {
        // Kytke tallennus päälle/pois
        tallennusPäällä = !tallennusPäällä;
    }
    @Override
    public void raportoiTila() {
        String tila = tallennusPäällä ? "päällä" : "pois";
        IO.println("Turvakameran tallennus on " + tila + ".");
    }
}
// FILE_END
// FILE: Kahvinkeitin.java
public class Kahvinkeitin extends Laite {

    private boolean kiehumassa = false;

    @Override
    public void vaihdaTilaa() {
        // Keitä kahvia tai kytke keitin pois päältä
        kiehumassa = !kiehumassa;
    }
    @Override
    public void raportoiTila() {
        String tila = kiehumassa ? "päällä" : "pois";
        System.out.println("Kahvinkeittimen pannu on " + tila + ".");
    }
}
// FILE_END
```

Jos katsotaan `Laite`-luokkaa, huomataan, että sen metodit `vaihdaTilaa()` ja `raportoiTila()` eivät tee mitään. Teoriassa voisimme luoda myös `Laite`-luokasta ilmentymän ja kutsua sen metodeja:

```java,ignore
Laite laite = new Laite();
laite.vaihdaTilaa(); // Ei tee mitään
laite.raportoiTila(); // Ei tee mitään
```

Kuten nähdään, mitään ei tapahdu näitä metodeja kutsuttaessa, ja sikäli `Laite`-luokasta tehdyt oliot ovat tavallaan hyödyttömiä. Ei ole oikeastaan järkevää, että olisi olemassa jokin "yleinen laite", ilman, että tiedetään tarkemmin, minkä tyyppisestä laitteesta on kyse. Näin ollen `Laite`-luokka on oikeastaan tarkoitettu *vain* perittäväksi. 

Javassa luokkaa, joka on tarkoitettu vain perittäväksi, kutsutaan *abstraktiksi luokaksi*. 

Muutetaan `Laite`-luokka abstraktiksi luokaksi. Koska myös metodit on tarkoitettu toteutettavaksi perivissä luokissa, määritellään myös metodit abstrakteiksi. Kaikkien perivien luokkein on toteutettava nämä metodit, kuten ne esimerkissämme jo tekevätkin.

```java
// FILE: Laite.java
public abstract class Laite {
    public abstract void vaihdaTilaa();
    public abstract void raportoiTila();
}
// FILE_END
// FILE: Valo.java
public class Valo extends Laite {
    private int kirkkaus = 0;

    @Override
    public void vaihdaTilaa() {
        // Vaihda kirkkaus 0 -> 50 -> 100 -> 0 ...
        switch (kirkkaus) {
            case 0 -> kirkkaus = 50;
            case 50 -> kirkkaus = 100;
            case 100 -> kirkkaus = 0;
        }
    }
    @Override
    public void raportoiTila() {
        IO.println("Valon kirkkaus on " + kirkkaus + "%.");
    }
}
// FILE_END
// FILE: Turvakamera.java
public class Turvakamera extends Laite {
    private boolean tallennusPäällä = false;

    @Override
    public void vaihdaTilaa() {
        // Kytke tallennus päälle/pois
        tallennusPäällä = !tallennusPäällä;
    }
    @Override
    public void raportoiTila() {
        String tila = tallennusPäällä ? "päällä" : "pois";
        IO.println("Turvakameran tallennus on " + tila + ".");
    }
}
// FILE_END
// FILE: Kahvinkeitin.java
public class Kahvinkeitin extends Laite {

    private boolean kiehumassa = false;

    @Override
    public void vaihdaTilaa() {
        // Keitä kahvia tai kytke keitin pois päältä
        kiehumassa = !kiehumassa;
    }
    @Override
    public void raportoiTila() {
        String tila = kiehumassa ? "päällä" : "pois";
        System.out.println("Kahvinkeittimen pannu on " + tila + ".");
    }
}
// FILE_END
// FILE: main.java
public class Main {
    public static void main() {
        Laite[] laitteet = {
            new Valo(),
            new Turvakamera(),
            new Kahvinkeitin()
        };

        for (Laite laite : laitteet) {
            laite.vaihdaTilaa();
            laite.raportoiTila();
        }
    }
}
// FILE_END
```

Nyt `Laite`-luokasta ei voi enää luoda ilmentymiä. Yritettäessä tehdä niin, kääntäjä antaa virheen:

```java,ignore
Laite laite = new Laite(); 
```

```
java: Laite is abstract; cannot be instantiated
```

## Miksi abstrakti luokka on hyödyllinen?

Abstrakti luokka ei ole vain kielto tehdä luokasta ilmentymiä. Sen ensisijainen tarkoitus on:

- määritellä yhteinen sopimus siitä, mitä metodeja kaikkien aliluokkien pitää tarjota, ja 
- tarjota yhteisiä ominaisuuksia ja tarvittaessa myös toteutuksia, jotta aliluokat keskittyvät vain olennaiseen. 

Kun `Laite` on abstrakti, voimme lisätä sille attribuutteja ja metodien valmiita toteutuksia, joita kaikki aliluokat käyttävät. 

Lisätään `Laite`-luokkaan attribuutti `nimi`, joka kertoo laitteen nimen, sekä attribuutti `kytketty`, joka kertoo, onko laite päällä vai pois päältä. Sellainen attribuutti on hyödyllinen kaikille laitteille, joten se sopii hyvin abstraktiin luokkaan. 

Jos kyse olisi verkkolaitteesta, hyödyllisiä tai jopa pakollisia attribuutteja voisivat olla muun muassa MAC-osoite ja IP-osoite. Pidämme kuitenkin tämän esimerkin yksinkertaisena, joten tyydymme tässä vain nimeen ja kytketty-tilan seuraamiseen.

Lisätään myös metodit `kytkePaalle()` ja `kytkePois()`, jotka sisältävät yleisen logiikan laitteen käynnistämiseen ja sammuttamiseen, jota kaikki laitteet voivat noudattavat. 

```java,ignore
public abstract class Laite {
    private String nimi;
    private boolean kytketty;

    protected Laite(String nimi) {
        this.nimi = nimi;
    }

    public void kytkePaalle() {
        if (!kytketty) {
            kytketty = true;
            System.out.println(nimi + " käynnistyy.");
        }
    }

    public void kytkePois() {
        if (kytketty) {
            kytketty = false;
            System.out.println(nimi + " sammuu.");
        }
    }

    public abstract void vaihdaTilaa();
    public abstract void raportoiTila();
}
```

Huomaa, että koska päätimme, että joka laitteella on oltava nimi, siitä seuraa, että nimi on asetettava rakentajan parametrin kautta. Tämän seurauksena emme voi enää luoda ilmentymiä oletusrakentajan avulla. 

```java,ignore
// ...
Valo valo = new Valo();
// ...
```

```
Valo.java
java: constructor Laite in class Laite cannot be applied to given types;
  required: java.lang.String
  found:    no arguments
  reason: actual and formal argument lists differ in length
```

Rakentajan kutsuminen vaatii nyt nimen välittämisen, esimerkiksi `new Valo("PhilipsHue")`. Niinpä kussakin aliluokan rakentajassa on kutsuttava yliluokan rakentajaa. Tehdään tämä muutos kaikkiin aliluokkiin.

```java
// FILE: Laite.java
public abstract class Laite {
    private String nimi;
    private boolean kytketty;

    protected Laite(String nimi) {
        this.nimi = nimi;
    }

    public void kytkePaalle() {
        if (!kytketty) {
            kytketty = true;
            System.out.println(nimi + " käynnistyy.");
        }
    }

    public void kytkePois() {
        if (kytketty) {
            kytketty = false;
            System.out.println(nimi + " sammuu.");
        }
    }

    public abstract void vaihdaTilaa();
    public abstract void raportoiTila();
}
// FILE_END
// FILE: Valo.java
public class Valo extends Laite {
    private int kirkkaus = 0;

    public Valo(String nimi)
    {
        super(nimi);
    }

    @Override
    public void vaihdaTilaa() {
        // Vaihda kirkkaus 0 -> 50 -> 100 -> 0 ...
        switch (kirkkaus) {
            case 0 -> kirkkaus = 50;
            case 50 -> kirkkaus = 100;
            case 100 -> kirkkaus = 0;
        }
    }
    @Override
    public void raportoiTila() {
        System.out.println("Valon kirkkaus on " + kirkkaus + "%.");
    }
}
// FILE_END
// FILE: Turvakamera.java
public class Turvakamera extends Laite {
    private boolean tallennusPaalla = false;

    public Turvakamera(String nimi)
    {
        super(nimi);
    }

    @Override
    public void vaihdaTilaa() {
        // Kytke tallennus päälle/pois
        tallennusPaalla = !tallennusPaalla;
    }
    @Override
    public void raportoiTila() {
        String tila = tallennusPaalla ? "päällä" : "pois";
        System.out.println("Turvakameran tallennus on " + tila + ".");
    }
}
// FILE_END
// FILE: Kahvinkeitin.java
public class Kahvinkeitin extends Laite {
    private boolean kiehumassa = false;

    public Kahvinkeitin(String nimi)
    {
        super(nimi);
    }

    @Override
    public void vaihdaTilaa() {
        // Keitä kahvia tai kytke keitin pois päältä
        kiehumassa = !kiehumassa;
    }
    @Override
    public void raportoiTila() {
        String tila = kiehumassa ? "päällä" : "pois";
        System.out.println("Kahvinkeittimen pannu on " + tila + ".");
    }
}
// FILE_END
// FILE: main.java
public class Main {
    public static void main() {
        Laite[] laitteet = {
                new Valo("PhilipsHue"),
                new Kahvinkeitin("Moccamaster"),
                new Turvakamera("Reolink")
        };

        for (Laite laite : laitteet) {
            laite.kytkePaalle();
            laite.vaihdaTilaa();
            laite.raportoiTila();
            laite.kytkePois();
        }
    }
}
// FILE_END
```

Aliluokat perivät nyt päälle- ja pois-kytkemislogiikan sellaisenaan, mutta niiden on *pakko* toteuttaa laitteen omat, oliokohtaiset toiminnallisuudet. Tämä luo tasapainoa joustavuuden ja pakollisen rakenteen välille: Tilan vaihtaminen ja tilan raportointi ovat pakollisia, mutta niiden toteutus on vapaa. Toisaalta laitteen käynnistys- ja sammutuslogiikka on yhteinen kaikille laitteille.

<details closed><summary>✨ Valinnaista lisätietoa: Abstraktit metodit ja operaatiorunko-malli </summary>

Abstraktissa luokassa voi olla myös konkreettinen metodi, jonka toteutuksessa kutsutaan abstraktia metodia. Tällaista toteutusta kutsutaan ohjelmistosuunnittelussa *operaatiorunko*-suunnittelumalliksi. Abstrakti luokka määrittelee toimenpiteelle "kaavan", mutta delegoi osan vaiheista aliluokkien toteutettavaksi.

Jo aiemmin toteutetut osat on piilotettu koodista. Saat ne esiin klikkaamalla silmä-kuvaketta koodialueen oikeasta yläreunasta. 

```java
// FILE: Laite.java
public abstract class Laite {
//-    private String nimi;
//-    private boolean kytketty;
//-
//-    protected Laite(String nimi) {
//-        this.nimi = nimi;
//-    }

    public final void suoritaPaivitys() {
        kytkePaalle();
        valmistelePaivitys(); // Abstrakti askel, jonka aliluokka toteuttaa
        paivitys();
        kytkePois();
    }

    protected abstract void valmistelePaivitys();

    private void paivitys() {
        IO.println("Haetaan uusin päivitys verkosta...");
        IO.println("Laite päivitetään...");
    }

//-    public void kytkePaalle() {
//-        if (!kytketty) {
//-            kytketty = true;
//-            System.out.println(nimi + " käynnistyy.");
//-        }
//-    }
//-
//-    public void kytkePois() {
//-        if (kytketty) {
//-            kytketty = false;
//-            System.out.println(nimi + " sammuu.");
//-        }
//-    }
//-
//-    public abstract void vaihdaTilaa();
//-    public abstract void raportoiTila();
}
// FILE_END
// FILE: Valo.java
public class Valo extends Laite {
    private int kirkkaus = 0;

//-    public Valo(String nimi)
//-    {
//-        super(nimi);
//-    }
//-
    @Override
    protected void valmistelePaivitys() {
        IO.println("Valmistellaan valoa päivitystä varten...");
        IO.println("Asetetaan valo kirkkauteen 0%...");
    }

//-    @Override
//-    public void vaihdaTilaa() {
//-        // Vaihda kirkkaus 0 -> 50 -> 100 -> 0 ...
//-        switch (kirkkaus) {
//-            case 0 -> kirkkaus = 50;
//-            case 50 -> kirkkaus = 100;
//-            case 100 -> kirkkaus = 0;
//-        }
//-    }
    @Override
    public void raportoiTila() {
        IO.println("Valon kirkkaus on " + kirkkaus + "%.");
    }
}
// FILE_END
// FILE: Kahvinkeitin.java
public class Kahvinkeitin extends Laite {
//-    private boolean kiehumassa = false;
//-
//-    public Kahvinkeitin(String nimi)
//-    {
//-        super(nimi);
//-    }

    @Override
    protected void valmistelePaivitys() {
        IO.println("Valmistellaan keitintä päivitystä varten...");
        IO.println("Keskeytä kiehuminen...");
    }

//-    @Override
//-    public void vaihdaTilaa() {
//-        // Keitä kahvia tai kytke keitin pois päältä
//-        kiehumassa = !kiehumassa;
//-    }
//-    @Override
//-    public void raportoiTila() {
//-        String tila = kiehumassa ? "päällä" : "pois";
//-        System.out.println("Kahvinkeittimen pannu on " + tila + ".");
//-    }
}
// FILE_END
// FILE: main.java
public class Main {
    public static void main() {
        Valo hue =  new Valo("PhilipsHue");
        Kahvinkeitin mocca = new Kahvinkeitin("MoccaMaster");

        hue.suoritaPaivitys();
        // Kokeile myös:
        // mocca.suoritaPaivitys();
    }
}
// FILE_END
```

`suoritaPaivitys()` on nyt ikään kuin valmis resep­ti, jota aliluokat eivät voi muuttaa (`final`). Sen sijaan ne täydentävät reseptin tarvitsemansa tavoilla toteuttamalla abstraktit metodit.

🤔 Pohdittavaksi: Missä tilanteissa haluaisit estää aliluokkaa ylikirjoittamasta tiettyä metodia? 

</details>

## Rajapinta

*Rajapinta* on kuin sopimus: se määrittelee, mitä metodeja luokan on tarjottava, ottamatta kantaa siihen, miten ne on teknisesti toteutettu. Toisin kuin abstrakti luokka, joka luo pohjan luokan metodeille ja attribuuteille, rajapinta keskittyy kuvailemaan olion kyvykkyyksiä. Rajapinta mahdollistaa yhtenevän kyvykkyyksien määrittelyn, vaikka luokat olisivat täysin erilaisia tai periytyisivät eri paikoista luokkahierarkiassa. Kun ohjelmoija sitten käsittelee oliota rajapinnan kautta, hän voi luottaa siihen, että olio tarjoaa sovitun kyvykkyyden riippumatta siitä, mitä luokkaa olio edustaa.

Tärkeä ero perintään on se, että luokka *toteuttaa* (engl. *implements*) rajapinnan, ei peri sitä. Tämän ansiosta yksi luokka voi toteuttaa useita eri rajapintoja samanaikaisesti. 

Javan versiosta 8 alkaen rajapinnat voivat sisältää myös metodien oletustoteutuksia.

## Esimerkki

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

Luokka voi toteuttaa useita rajapintoja. 

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

Huomaa, että emme tiedä emmekä välitä siitä, miten nämä metodit aikanaan toteutetaan. Piirto voi tapahtua graafisella käyttöliittymällä, tekstipohjaisella käyttöliittymällä tai vaikkapa tulostamalla tiedostoon. Meille riittää, että tiedämme, että jokaisella `Piirrettävä`-rajapinnan toteuttavalla luokalla on `piirra()`-metodi, ja jokaisella `Klikattava`-rajapinnan toteuttavalla luokalla on `klikattu()`- ja `asetaKorostus(boolean korostus)`-metodit.

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

Rajapintojen hyöty ei vielä kokonaisuudessaan välity, osittain siksi, että `piirra()`-metodi on ainoa metodi, jota `Piirrettava`-rajapinta tarjoaa. Nyt kuitenkin voimme luoda toisen komponentin, `Painike`, joka on laatikon näköinen klikkattava painike, jossa on tekstiä. `Painike`-luokka toteuttaa molemmat rajapinnat: `Piirrettävä` ja `Klikattava`.

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

**TODO: Muuttujan tyyppinä rajapinta**

Lista olioita jotka toteuttavat rajapinnan. Oliot voisivat olla toisiinsa liittymättömiä. 

**TODO: Parametrina rajapinta-tyyppi**

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

<task>
  <task-title>Tehtävä 3.4: Abstraktit luokat. <points>1 p.</points> </task-title>
  <handout>

  {{#include ../exercises/3-4-abstrakti-luokka-1/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa3/tehtava4">Tee tehtävä TIMissä</a></task-link>
</task>

.


Suunnittele `Hälytettävä`-rajapinta, jossa on metodit `trigger()` ja `reset()`. Toteuta rajapintaa hyödyntävä abstrakti `HälytinLaite`, joka pitää kirjaa siitä, montako kertaa hälytys on aktivoitu. Luo kaksi konkreettista laitetta (esim. `SavuHälytin` ja `VesivuotoHälytin`). Mieti, missä kohtaa sijoitat yhteisen lokituksen: rajapintaan (ei mahdollista) vai abstraktiin luokkaan?

> [!Muista]
> Rajapinta = lupaus. Abstrakti luokka = sekä lupaus että osittainen toteutus. Valitse kumpi sopii tarpeeseesi, tai yhdistä molemmat.
