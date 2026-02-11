# Poikkeusten hallinta

> [!VAROITUS]
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Poikkeukset (checked, unchecked), try-catch, finally, heittäminen (throw, throws).

*Poikkeus* (engl. *exception*; lyhennetty muoto ilmauksesta *exceptional
event*), on tilanne, joka syntyy ohjelman suorituksen aikana ja keskeyttää
ohjelman normaalin käskynkulun. Poikkeus voi syntyä esimerkiksi seuraavissa
tilanteissa:

- Käyttäjä antaa virheellisen syötteen (esimerkiksi tekstin, kun odotetaan numeroa).
- Yritetään lukea tiedostoa, jota ei ole olemassa.
- Verkko- tai tietokantayhteys katkeaa kesken suorituksen.
- Jaetaan nollalla laskutoimituksessa.
- Viitataan listan tai taulukon indeksiin, jota ei ole olemassa.
- Kutsutaan metodia olion viittauksella, joka on `null`.

Javassa poikkeusten hallintaan on sisäänrakennettu mekanismi, joka mahdollistaa
virhetilanteiden hallitun käsittelyn ohjelmakoodissa. Tämän mekanismin avulla
ohjelmoija voi määritellä, miten ohjelman tulee reagoida erilaisiin virhetilanteisiin
ilman, että koko ohjelma kaatuu.

   
## Poikkeusten heittäminen ja käsittely

Poikkeusten hallinta Javassa perustuu kolmeen pääkomponenttiin:

1. Poikkeusten heittäminen (engl. *throwing exceptions*): Kun virhe tapahtuu,
   luodaan poikkeusolio ja heitetään se ajonaikaiselle järjestelmälle.
2. Poikkeusten käsittely (engl. *catching exceptions*): Ohjelmoija voi määritellä
   koodilohkoja, jotka käsittelevät tiettyjä poikkeuksia `try-catch`-rakenteella.
3. Lopullinen siivous (engl. *finally*): `finally`-lohko, joka suoritetaan aina
   riippumatta siitä, tapahtuiko poikkeus vai ei, esimerkiksi resurssien
   vapauttamiseksi.   

Palaamme esimerkkeihin kohta, mutta pohditaan ensin järjestelmän toimintaa
korkealla tasolla. 

Kun metodin suorituksen aikana tapahtuu virhe, metodi luo virhettä kuvaavan
poikkeusolion ja luovuttaa sen ajonaikaiselle järjestelmälle. Poikkeusolio
sisältää muun muassa poikkeuksen tyypin sekä ohjelman tilan sillä hetkellä, kun
virhe tapahtui. Tätä poikkeusolion luomista ja luovuttamista ajonaikaiselle
järjestelmälle kutsutaan poikkeuksen heittämiseksi.

Kun poikkeus on heitetty, ajonaikainen järjestelmä alkaa etsiä poikkeukselle
sopivaa käsittelijää (engl. *exception handler*) kutsupinosta siinä
järjestyksessä, jossa metodeja on kutsuttu. Käsittelijä on sopiva, jos se pystyy
käsittelemään heitetyn poikkeusolion tyypin mukaisen poikkeusolion. Jos sopiva
käsittelijä löytyy, poikkeus välitetään sille. Tällöin sanotaan, että poikkeus
"otetaan kiinni" (engl. *catch*). 

Jos järjestelmä käy läpi koko kutsupinon löytämättä sopivaa käsittelijää, se
säie (engl. *thread*), jossa virhe tapahtui, pysähtyy. Jos kyseessä on pääsäie
(engl. *main thread*), koko ohjelma kaatuu.

Alla oleva kaavio havainnollistaa karkeasti poikkeuksen heittämisen ja
käsittelyn prosessia. Oletetaan, että `main()`-metodi kutsuu metodia `a()`, joka
puolestaan kutsuu metodia `b()`, ja `b()` edelleen `c()`-metodia. 

```bob
                       +-----.----------------------+
Heittää poikkeuksen ---|c( ) | Metodi, jossa virhe  |
                       |-----' tapahtui             |----.
                       +----------------------------+    | Etsitään
                                     ^                   | sopivaa 
                                     | kutsuu            | käsittelijää
                       +-----.----------------------+    |
Heittää poikkeuksen ---|b( ) | Metodi, jossa ei ole |<---'
          eteenpäin    |-----' poikkeuskäsittelijää |----.
                       +----------------------------+    | Etsitään   
                                     ^                   | sopivaa 
                                     | kutsuu            | käsittelijää
                       +-----.----------------------+    |
  Ottaa poikkeuksen ---|a( ) | Metodi, jossa on     |<---'
             kiinni    |-----' poikkeuskäsittelijä  | 
                       +----------------------------+               
                                     ^ 
                                     | kutsuu 
                       +----------------------------+ 
                       |           main( )          | 
                       +----------------------------+ 
```

Esimerkissä tapahtuu seuraavaa:

 1. Metodi `c()` heittää poikkeuksen, esimerkiksi käsitellessään verkkoyhteyttä,
 mutta metodissa `c()` ei ole sopivaa käsittelijää. 
 2. Ajonaikainen järjestelmä katsoo kutsupinossa seuraavana olevaa metodia, joka
 on `b()`. 
 3. Metodi `b()`:llä ei myöskään ole sopivaa käsittelijää, joten tutkitaan edelleen
 seuraavaa metodia, joka on `a()`. 
 4. `a()`-metodilla on sopiva käsittelijä, joka ottaa poikkeuksen kiinni. 
 5. Ohjelma jatkaa suoritustaan, kun `a()`-metodissa oleva käsittelijä on suoritettu.

## Tarkastetut ja tarkastamattomat poikkeukset

Java jakaa poikkeukset kahteen kategoriaan: tarkastettuihin (engl. *checked*) ja
tarkastamattomiin (engl. *unchecked*). Nimitys tulee siitä, että tarkastettujen
poikkeusten kohdalla käsittelyn olemassaolo tarkastetaan käännösaikana, kun taas
tarkastamattomien poikkeusten käsittelyä ei tarkasteta.

*Tarkastetut poikkeukset* kuvaavat ympäristöstä tai syötteestä johtuvia ongelmia
joihin ohjelma voi usein reagoida hallitusti. Tyypillisiä esimerkkejä ovat
tiedostojen käsittely, verkkoyhteydet ja tietokantatoiminnot. Esimerkiksi
tiedoston avaaminen voi epäonnistua, koska tiedostoa ei ole olemassa tai siihen
ei ole lukuoikeuksia, vaikka ohjelmakoodi itsessään olisi täysin oikein.
Tällaisia poikkeuksia ovat esimerkiksi 

 * `IOException`, joka kuvaa syötteeseen tai tulosteeseen liittyviä ongelmia, kuten tiedoston
   lukemisen epäonnistumista, ja
 * `SQLException`, joka liittyy tietokantatoimintoihin.

Tarkastetut poikkeukset periytyvät `Exception`-luokasta. 

Tällöin kääntäjä ikään kuin ilmoittaa ohjelmoijalle: "*Näen, että olet tekemässä
jotain riskialtista (kuten lukemassa tiedostoa). En käännä ohjelmaasi, ennen
kuin olet osoittanut, että olet ottanut huomioon mahdolliset ongelmat.*"

Tällöin on tehtävä jompikumpi seuraavista:

 1. käsiteltävä poikkeus `try–catch`-rakenteella (vrt. ylemmän kuvion `a()`-metodi), tai
 2. ilmoitettava metodin määrittelyssä `throws`-määreellä, että poikkeus voi
    siirtyä kutsujalle (vrt. ylemmän kuvion `b()`- ja `c()`-metodit).

Jos kumpaakaan ei tehdä, koodi ei käänny. Tätä vaatimusta kutsutaan *catch or
specify* -vaatimukseksi.

*Tarkastamaton poikkeus* on poikkeus, jota ei tarkasteta käännösaikana, eikä
sitä siten tarvitse käsitellä tai ilmoittaa etukäteen. Tällainen poikkeus voi
kuitenkin laueta ohjelman ohjelman suorituksenaikana. Tyypillisiä
tarkastamattomia poikkeuksia ovat
 
 * `NullPointerException`, joka tapahtuu, kun yritetään käyttää olion viitettä, joka on `null`,
 * `IllegalArgumentException`, joka tapahtuu, kun metodille annetaan sopimaton argumentti,
 * `ArrayIndexOutOfBoundsException`, joka tapahtuu, kun yritetään käyttää taulukon indeksiä, joka on taulukon
   raja-arvojen ulkopuolella, ja
 * `ArithmeticException`, joka tapahtuu, kun tapahtuu laskuvirhe, kuten jakaminen nollalla.

Tarkastamattomat poikkeukset periytyvät `RuntimeException`-luokasta.
  
Tarkastamattomat poikkeukset kuvaavat yleensä ohjelmointivirheitä, ja näiden
käsittelemistä `try-catch`-rakenteella ei vaadita lähdekoodissa, eikä se ole
myöskään suositeltavaa. Esimerkiksi `NullPointerException`-poikkeus on usein
selvä merkki ohjelmassa olevasta virheestä. Vaikka `try-catch`-rakenteella
voikin kyllä ottaa `NullPointerException`-poikkeuksen kiinni, se ei yleensä ole
järkevää, koska se vain peittää ohjelman virheen sen sijaan, että korjaisi sen.

## Syntaksi

`try-catch`-rakenne näyttää seuraavalta:

```java
try {
    // Koodilohko, jossa poikkeus voi tapahtua
} catch (Poikkeustyyppi poikkeus) {
    // Koodilohko, joka käsittelee poikkeuksen
}
```

`throws`-määre puolestaan määritellään metodin allekirjoituksessa seuraavasti:

```java
void metodi() throws Poikkeustyyppi {
    // Metodin toteutus, joka voi heittää poikkeuksen
}
```

Poikkeuksia voi olla useita, ja ne voidaan käsitellä erikseen:

```java
try {
    // Koodilohko, jossa poikkeus voi tapahtua
} catch (Poikkeustyyppi1 e1) {
    // Koodilohko, joka käsittelee Poikkeustyyppi1 -poikkeuksen
} catch (Poikkeustyyppi2 e2) {
    // Koodilohko, joka käsittelee Poikkeustyyppi2 -poikkeuksen
}
```

Jos metodi voi heittää useita tarkastettuja poikkeuksia, ne voidaan ilmoittaa
`throws`-määreessä pilkulla erotettuna:

```java
void metodi() throws Poikkeustyyppi1, Poikkeustyyppi2 {
    // Metodin toteutus, joka voi heittää useita poikkeuksia
}
```

## finally

`finally`-lohkoa käytetään tilanteissa, joissa jokin siivousvaihe täytyy tehdä
aina riippumatta siitä, onnistuiko `try`-lohkon suoritus tai tapahtuiko
poikkeus. Tyypillisiä esimerkkejä ovat tiedoston, verkkoyhteyden tai muun
resurssin sulkeminen.

Kun käytössä on `try-catch-finally`, suoritus etenee näin:

 1. `try` suoritetaan.
 2. Jos poikkeus tapahtuu, sopiva `catch` suoritetaan.
 3. Lopuksi `finally` suoritetaan aina.

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

void lueTiedosto(String polku) {
    Scanner lukija = null;

    try {
        lukija = new Scanner(new File(polku));
        while (lukija.hasNextLine()) {
            IO.println(lukija.nextLine());
        }
    } catch (FileNotFoundException e) {
        IO.println("Tiedostoa ei löytynyt: " + polku);
    } finally {
        if (lukija != null) {
            lukija.close();
        }
        IO.println("Lukuoperaatio päättyi.");
    }
}
```

Yllä olevassa esimerkissä `finally` sulkee lukijan myös silloin, kun tiedoston
lukeminen keskeytyy poikkeukseen. Näin vältetään resurssivuodot, kuten
muistivuodot tai tiedostokahvojen jääminen auki.

Nyky-Javassa resurssien hallintaan kannattaa usein käyttää
`try-with-resources`-rakennetta, jolloin resurssit suljetaan automaattisesti.
Otetaan tästä esimerkki myöhemmissä osissa, kun olemme tutustuneet
`Closeable`-rajapintaan.

## Esimerkki tarkastetusta poikkeuksesta

Oletetaan, että haluamme lukea tiedoston sisältöä. Tehdään se käyttäen
modernista Javasta löytyvää `Files.readString()`-metodia.

```java
import java.nio.file.Files;
import java.nio.file.Path;

void main() {
    String sisalto = lueTiedosto("data.txt");
    IO.println(sisalto);
}

String lueTiedosto(String polku) {
    return Files.readString(Path.of(polku));
}
```

Ohjelmamme kaatuu, koska `Files.readString()`-metodi *voi* heittää
`IOException`-poikkeuksen. Tämä on tarkastettu poikkeus. Määritellään
`lueTiedosto()`-metodille `throws IOException` -määre.

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

void main() {
    String sisalto = lueTiedosto("data.txt");
    IO.println(sisalto);
}

String lueTiedosto(String polku) throws IOException {
    return Files.readString(Path.of(polku));
}
```

Ohjelmamme kaatuu edelleen, koska `throws`-määre heittää poikkeuksen edelleen
kutsujalle (vrt. aiemman kuvion `b()`- ja `c()`-metodit). Koska
`main()`-metodissa ei ole sopivaa käsittelijää, ohjelma kaatuu. Käsitellään
poikkeus `main()`-metodissa `try–catch`-rakenteella.

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

void main() {
    try {
        String sisalto = lueTiedosto("data.txt");
        IO.println(sisalto);
    } catch (IOException e) {
        IO.println("Tiedoston lukeminen epäonnistui: " + e.getMessage());
    }
}

String lueTiedosto(String polku) throws IOException {
    return Files.readString(Path.of(polku));
}
```

Nyt ohjelmamme toimii ja tulostaa virheilmoituksen, vaikka `data.txt`-tiedostoa
ei olisikaan olemassa.

## Esimerkki tarkastamattomasta poikkeuksesta

Oletetaan, että meillä on luokka `Henkilo`, jolla on `getNimi()`-metodi, joka
palauttaa henkilön nimen. Luodaan nyt lista henkilöistä.

```java
import java.util.List;

public class Henkilo {
    private String nimi;

    public Henkilo(String nimi) {
        this.nimi = nimi;
    }

    public String getNimi() {
        return nimi;
    }
}

void main() {
    List<Henkilo> henkilot = new ArrayList<>();
    henkilot.add(new Henkilo("Antti-Jussi"));
    henkilot.add(new Henkilo("Denis"));
```

Katsotaan seuraavaksi miten `null`-viittaukset voivat aiheuttaa
`NullPointerException`-poikkeuksia. Oletetaan, että jostain kumman syystä
listalle päätyisi `null`-arvo. Tällainen tilanne voisi syntyä esimerkiksi, jos
henkilöiden tietoja luettaisiin ulkoisesta lähteestä, ja jokin tietue olisi
puutteellinen, mutta se siitä huolimatta lisättäisiin listalle.

```java
//- public class Henkilo {
//-     private String nimi;
//- 
//-     public Henkilo(String nimi) {
//-         this.nimi = nimi;
//-     }
//- 
//-     public String getNimi() {
//-         return nimi;
//-     }
//- }
void main() {
    List<Henkilo> henkilot = new ArrayList<>();
    henkilot.add(new Henkilo("Antti-Jussi"));
    henkilot.add(new Henkilo("Denis"));
    kasitteleListaa(henkilot);

    for (Henkilo h : henkilot) {
        IO.println(h.getNimi());
    }
}

void kasitteleListaa(List<Henkilo> henkilot) {
    // Jostain syystä listalle päätyy null-viittaus
    henkilot.add(null);
}
```

Tämähän ei ole `main()`-metodin näkökulmasta ollenkaan ilmeistä -- se hoitaa
vain omaa hommaansa. Ongelma onkin siinä, että `kasitteleListaa()`-metodi
aiheuttaa sivuvaikutuksen (muuttaa listan sisältöä) nimen omaan sillä tavalla,
joka rikkoo `main()`-metodin odotuksen siitä, että listalla on vain
`Henkilo`-olioita. Ongelma ilmenee, kun `main()`-metodi yrittää kutsua
`getNimi()`-metodia `null`-viittaukselle.

Toki tämä tilanne voitaisiin käsitellä `try-catch`-rakenteella, tai toisaalta
tarkastamalla `if`-lauseella tulostettaessa, onko `h`-olio `null`-viittaus. Tämä on kuitenkin
melkoisen tympeää, eikä ratkaise ongelman juurisyytä. 

## Useat poikkeusoliot

Sama `try`-lohko voi aiheuttaa useita eri poikkeuksia. Tällöin jokaiselle
poikkeustyypille voidaan tehdä oma `catch`-lohko.

Alla `Integer.parseInt()` voi heittää `NumberFormatException`-poikkeuksen, jos
syöte ei ole numero, ja jakolasku voi heittää `ArithmeticException`-poikkeuksen,
jos jakaja on nolla.

```java
void main() {
    laske("42", 2);   // onnistuu
    laske("abc", 2);  // NumberFormatException
    laske("42", 0);   // ArithmeticException
}

void laske(String syote, int jakaja) {
    try {
        int luku = Integer.parseInt(syote);
        int tulos = luku / jakaja;
        IO.println("Tulos: " + tulos);
    } catch (NumberFormatException e) {
        IO.println("Virheellinen luku: " + syote);
    } catch (ArithmeticException e) {
        IO.println("Nollalla ei voi jakaa.");
    }
}
```

Kun poikkeukset ovat eri tyyppisiä olioita, ne kannattaa käsitellä eri tavalla
tilanteen mukaan.

## Omien poikkeusolioiden tekeminen

Joskus valmiit poikkeusluokat eivät kuvaa ongelmaa riittävän tarkasti. Tällöin
voit määritellä oman poikkeusluokan.

Yleensä valinta tehdään näin:

1. Peri luokka `Exception`-luokasta, jos haluat tarkastetun poikkeuksen.
2. Peri luokka `RuntimeException`-luokasta, jos haluat tarkastamattoman poikkeuksen.

Alla on esimerkki tarkastetusta omasta poikkeuksesta:

```java
class EpakelpoSalasanaException extends Exception {
    public EpakelpoSalasanaException(String viesti) {
        super(viesti);
    }
}

void main() {
    try {
        rekisteroiKayttaja("abc");
        IO.println("Käyttäjä rekisteröity.");
    } catch (EpakelpoSalasanaException e) {
        IO.println("Rekisteröinti epäonnistui: " + e.getMessage());
    }
}

void rekisteroiKayttaja(String salasana) throws EpakelpoSalasanaException {
    if (salasana.length() < 8) {
        throw new EpakelpoSalasanaException("Salasanan pitää olla vähintään 8 merkkiä.");
    }
    if (!salasana.matches(".*[A-Z].*")) { // säännöllinen lauseke, joka tarkistaa, onko salasanassa iso kirjain
        throw new EpakelpoSalasanaException("Salasanassa pitää olla vähintään yksi iso kirjain.");
    }
    // ... muita tarkistuksia ...
}
```

Omien poikkeusten etu on se, että virheestä tulee semanttisesti tarkempi:
poikkeuksen nimestä näkee heti, mitä sääntöä rikottiin. Toki salasanan
tarkistamisessa olisi voinut käyttää myös if-lausetta ilman poikkeuksia, mutta
poikkeuksella on se etu, että se pakottaa käsittelemään virhetilanteen, eikä
sitä voi unohtaa.

## Poikkeusten käsittelyn hyödyllisyys

Poikkeukset tuovat merkittäviä etua koodin luettavuuteen ja ylläpidettävyyteen.
Ennen Javaa poikkeusten hallinta oli usein toteutettu erilaisten virhekoodien
palauttamisella. Esimerkiksi C-kielessä funktiot saattoivat palauttaa virheen
merkiksi erikoisarvoja, kuten `-1` tai `NULL`. Tämä lähestymistapa oli altis
virheille ja johti helposti siihen, että ohjelmoijat saattoivat unohtaa
tarkistaa näitä virhekoodiarvoja. Virheentarkistus ja varsinainen toiminta
sekoittuvat ns. "spagettikoodiksi". Alla esimerkki pseudokoodina. 

```
avaaTiedosto;
JOS (onnistui) {
    lueKoko;
    JOS (kokoSelvisi) {
        varaaMuisti;
        JOS (muistiRiitti) {
            lueData;
             // ... jne ...
        } MUUTEN palautaVirhe -2;
    } MUUTEN palautaVirhe -3;
} MUUTEN palautaVirhe -5;
```

Poikkeusten avulla koodin "onnellinen polku" (ns. *happy path*) on selkeästi
luettavissa, ja virheet on siivottu omiin lohkoihinsa.

```java,ignore
try {
    avaaTiedosto();
    selvitaKoko();
    varaaMuisti();
    lueData();
} catch (TiedostoVirhe e) {
    käsitteleVirhe();
} catch (MuistiVirhe e) {
    käsitteleVirhe();
}
```

Joskus virhe tapahtuu syvällä metodikutsujen ketjussa (esim. metodi1
$\rightarrow$ metodi2 $\rightarrow$ metodi3 $\rightarrow$ lueTiedosto). Ilman
poikkeuksia jokaisen välissä olevan metodin (metodi2, metodi3) pitää tarkistaa
paluuarvo ja välittää virhe eteenpäin, vaikka ne eivät itse osaisi tehdä
virheelle mitään. Poikkeusten kanssa välissä olevat metodit voivat "väistää"
(*duck*) poikkeuksen. Virhe "kuplii" automaattisesti ylöspäin kutsupinossa,
kunnes se saavuttaa metodin, joka on kiinnostunut käsittelemään sen.

Koska poikkeukset ovat olioita, ne muodostavat hierarkioita. Tämä mahdollistaa
joustavan virheenkäsittelyn. Voit napata juuri tietyn virheen (esim.
`FileNotFoundException`), jos tiedät miten se korjataan. Voit myös napata
yliluokan (esim. `IOException`), jolloin käsittelet yhdellä kertaa kaikki
tiedonsiirtoon liittyvät ongelmat. Vaarallisena houkutuksena on napata yleinen
yliluokka (esim. `Exception`), jolloin käsittelet kaikki mahdolliset
poikkeukset, mutta et oikeastaan tiedä, miten niitä käsitellään. Tällaista
`catch (Exception e)` -rakennetta tulee välttää, ellei todella aio käsitellä
kaikkia mahdollisia virheitä -- myös odottamattomia bugeja. Käsittely liian
yleisen olion tasolla voi kuitenkin jälleen kerran piilottaa ohjelmointivirheitä
ja vaikeuttaa vianetsintää.

Eri kielissä on erilaisia lähestymistapoja poikkeusten hallintaan. Esimerkiksi
[Pythonissa](https://docs.python.org/3/library/exceptions.html) kaikki
poikkeukset ovat tarkastamattomia, ja ohjelmoijan ei tarvitse ilmoittaa
etukäteen, että metodi voi heittää poikkeuksia.
[C++:ssa](https://en.cppreference.com/w/cpp/error/exception.html) on sekä
tarkastettuja että tarkastamattomia poikkeuksia, mutta niiden käyttö on vähemmän
yleistä kuin Javassa. Rustissa poikkeuksia ei ole lainkaan, vaan virhetilanteet
käsitellään [`Result`-tyypin avulla](https://doc.rust-lang.org/std/result/),
mikä pakottaa ohjelmoijan käsittelemään kaikki mahdolliset virheet
eksplisiittisesti. 

*Osa tämä osan tekstistä pohjautuu [Java-dokumentaatioon poikkeuksista](https://dev.java/learn/exceptions/).*


<task>
  <task-title>Tehtävä 6.6: Poikkeukset, osa 1. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/6-6-poikkeukset-1/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa6/tehtava6">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 6.7: Poikkeukset, osa 2. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/6-7-poikkeukset-2/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa6/tehtava7">Tee tehtävä TIMissä</a></task-link>
</task>
