# Kapselointi

> [!Osaamistavoitteet]
>
> - Tiedät, mitä näkyvyysmääreet kuten `public` ja `private` tarkoittavat.
> - Ymmärrät, että metodit ovat olioiden pääasiallinen tapa viestiä.
> - Ymmärrät kapseloinnin periaateet ja hyödyt, ja miten olion sisäinen toteutus
>   eroaa sen ulkoisesta käytöstä. 
> - Osaat toteuttaa ohjelman, jossa oliot toimivat yhdessä niin, että ne
>   eivät ole riippuvaisia toistensa sisäisestä toteutuksesta.

![Autoa ajetaan, vaikka emme tiedä miten moottori toimii](images/auto.png)

## Näkyvyysmääreet

Java tarjoaa kolme pääasiallista näkyvyysmäärettä: `public`, `protected` ja
`private`. Näkyvyysmääreet määrittelevät, mistä luokan jäseniin voidaan päästä
käsiksi.  

Javassa oletuksena luokan jäsenet ovat ns. `package-private`-näkyvyydellä, mikä
tarkoittaa, että ne ovat näkyvissä vain samassa pakkauksessa oleville luokille.
Alla olevassa taulukossa on yhteenveto eri näkyvyysmääreiden vaikutuksista;
Oletus-sarake viittaa `package-private`-näkyvyyteen. 

|                            | Luokka | Pakkaus | Aliluokka | Muu maailma |
| -------------------------- | ------ | ------- | --------- | ----------- |
| `public`                   | Kyllä  | Kyllä   | Kyllä     | Kyllä       |
| `protected`                | Kyllä  | Kyllä   | Kyllä     | Ei          |
| `package-private` (oletus) | Kyllä  | Kyllä   | Ei        | Ei          |
| `private`                  | Kyllä  | Ei      | Ei        | Ei          |

Ensimmäinen sarake ilmaisee, onko luokan oliolla itsellään pääsy määritellyn
näkyvyystason jäseneen. Kuten näet, oliolla on aina pääsy omiin jäseniinsä.
Toinen sarake ilmaisee, onko muilla samassa pakkauksessa olevilla oliolla pääsy
jäseneen. Kolmas sarake ilmaisee, onko luokasta perityillä aliluokan olioilla,
jotka sijaitsevat pakkauksen ulkopuolella, pääsy jäseneen. Neljäs sarake
ilmaisee, onko millä tahansa oliolla pääsy jäseneen. 

Jos ja kun muut ohjelmoijat (tai sinä itse) käyttävät tekemääsi luokkaa,
näkyvyysmääreet auttavat varmistamaan, että luokkaasi käytetään sillä tavalla,
jolla olet suunnitellut sen käytettävän. Pääsääntö on, että ohjelmoijan tulisi
käyttää mahdollisimman rajoittavaa näkyvyysmäärettä, ellei ole erityistä syytä
käyttää jotain muuta. Tämä auttaa suojaamaan luokan sisäistä tilaa ja estämään
tahalliset tai tahattomat väärinkäytökset luokan jäseniin. Vältä julkisia
attribuutteja, ellei kyseessä ole vakio.  

> [!HUOMAUTUS]
> Tässä materiaalissa saatetaan hetkittäin käyttää esimerkinomaisesti julkisia
> attribuutteja. Tämä voi auttaa havainnollistamaan joitakin kohtia tiiviisti,
> mutta sitä ei suositella tuotantokoodissa. 

Attribuutille tai metodille voi antaa näkyvyysmääreen lisäämällä sen
esittelyriville. Luokalle voidaan myös asettaa näkyvyysmääre. 

```java,ignore
// FILE: Henkilo.java
class Henkilo {
    // Näkyvyysmääre 'private' piilottaa attribuutin niin, että sitä ei voi 
    // tarkastella luokan ulkopuolelta.
    private String etunimi;
    private String sukunimi;

    // Näkyvyysmääre 'public' mahdollistaa metodin kutsumisen luokan ulkopuolelta.
    public String annaMerkkijono() {
        return etunimi + " " + sukunimi;
    }
}
// FILE_END
```

## Kapselointi ja koheesio

Kapselointi (engl. *encapsulation*) on yksi keskeisimmistä käsitteistä
olio-ohjelmoinnissa. Se tarkoittaa luokkien suunnittelua mahdollisimman
itsenäiseksi ja modulaariseksi. Jokaisella luokalla on oma tehtävänsä, jota
varten tarvittavat tiedot ja toiminnallisuudet *kapseloidaan* olion sisälle. Osa
näistä tiedoista ja toiminnallisuuksista voidaan piilottaa vain olion sisäistä
käyttöä varten. Olioiden tilan käsittelyä varten luokka tarjoaa käyttäjälleen
tavallisesti julkisista metodeista koostuvan rajapinnan, mikä parantaa ohjelman
muokattavuutta ja laajennettavuutta vähentämällä luokan sisäisistä muutoksista
johtuvia sivuvaikutuksia.

Yhteen kuuluvan tiedon ja toiminnallisuuden sijoittaminen saman rakenteen
sisälle on kapseloinnin ensimmäinen periaate. Olemmekin jo tehneet näin
määritellessämme luokkia ja niille sopivia attribuutteja ja metodeja. Luokan
koheesio (engl. *cohesion*) kuvastaa sitä, kuinka *hyvin* luokan attribuutit ja
metodit sopivat yhteen luokan tarkoituksen kanssa. Luokkien suunnittelun
tavoitteena on mahdollisimman korkea koheesio; luokan jäsenten tulisi olla
sopivia sen tarkoitukseen. 

Jos tekisimme esimerkiksi luokan kuvaamaan autoa, ei ehkä olisi kovin järkevää
lisätä tähän luokkaan jäseneksi auton omistajan nimeä, osoitetta,
puhelinnumeroa, jne. Omistajan tiedot ja niihin liittyvät toiminnallisuudet voi
olla parempi laittaa omaan luokkaan. 

Tehdään nyt luokka `Auto`, johon voimme soveltaa kapseloinnin periaatteita.
Lisätään aluksi vain attribuutit ja yksinkertaiset muodostajat. 

```java,ignore
// FILE: Auto.java
class Auto {
    String malli;
    String valmistenumero;
    double ajetutKilometrit;

    public Auto(String malli, String valmistenumero, double ajetutKilometrit) {
        this.malli = malli;
        this.valmistenumero = valmistenumero;
        this.ajetutKilometrit = ajetutKilometrit;
    }
}
// FILE_END
```

Haluaisimme tallentaa myös tietoja auton eri osista. Moottorista voisimme
tallentaa esimerkiksi mallin ja nykyisen kierrosluvun. Renkaista olisi hyvä
tietää ainakin malli, rengaspaine ja ehkä myös tyyppi, jolla voimme erottaa
kesä- ja talvirenkaat. Nämä *voisi* lisätä suoraan `Auto`-luokkaan
attribuuttina, mutta attribuuttien määrä kasvaisi aika suureksi, sillä
jokaisella renkaalla on omat tietonsa. Jos käyttäisimme taulukoita tai listoja,
tarvitsisimme niitäkin useita. Voi myös olla, että autossa ei välttämättä aina
ole moottoria kiinni. Renkaatkin on mahdollista ottaa irti tai niiden lukumäärä
voisi vaihdella automallien välillä.  

Auton ei oikeastaan tarvitse olla tietoinen sen moottorin tai renkaiden
sisäisestä toiminnasta, joten meidän on parempi tehdä useampi luokka, joista
jokainen on vastuussa omista tiedoistaan ja toiminnoistaan. 

Lisätään nyt `Moottori` ja `Rengas` -luokat ja määritellään näille sopivia
attribuutteja sekä muodostajat. 

```java,ignore
// FILE: Moottori.java
class Moottori {
    String malli;
    double kierrosluku;

    public Moottori(String malli, double kierrosluku) {
        this.malli = malli;
        this.kierrosluku = kierrosluku;
    }
}
// FILE_END
// FILE: Rengas.java
class Rengas {
    String malli;
    String tyyppi;
    double rengaspaine;

    public Rengas(String malli, String tyyppi, double rengaspaine) {
        this.malli = malli;
        this.tyyppi = tyyppi;
        this.rengaspaine = rengaspaine;
    }
}
// FILE_END
```

Lisätään lopuksi moottori ja lista renkaista `Auto`-luokan attribuuteiksi. Nämä
sisältävät viitteet moottori- ja rengasolioihin. Muistetaan, että viitteet eivät
oletuksena osoita mihinkään, vaan meidän täytyy luoda myös oliot ja asettaa
viitteet osoittamaan niihin. `Auto` sisältää nyt muiden luokkien olioita, jotka
hoitavat omat vastuualueensa auton kokonaisuudessa. Tällaista rakennetta
kutsutaan kompositioksi (engl. *composition*). Yksi etu tässä on se, että auton
moottorin tai renkaat voisi vaihtaa helposti uusin asettamalla viiteattribuutit
osoittamaan uuteen olioon. 

Lisätään myös pieni pääohjelma, jossa voimme luoda yhden auton oletusarvoilla ja
tulostaa sen tietoja. Käytämme tässä vielä olion attribuuttien arvoja suoraan,
mikä ei ole hyvän tavan mukaista. Teemme pian tämän paremmin. 

```java
// FILE: Moottori.java
class Moottori {
    String malli;
    double kierrosluku;

    public Moottori(String malli, double kierrosluku) {
        this.malli = malli;
        this.kierrosluku = kierrosluku;
    }
}
// FILE_END
// FILE: Rengas.java
class Rengas {
    String malli;
    String tyyppi;
    double rengaspaine;

    public Rengas(String malli, String tyyppi, double rengaspaine) {
        this.malli = malli;
        this.tyyppi = tyyppi;
        this.rengaspaine = rengaspaine;
    }
}
// FILE_END
// FILE: Auto.java
import java.util.ArrayList;

class Auto {
    String malli;
    String valmistenumero;
    double ajetutKilometrit;
    Moottori moottori;
    ArrayList<Rengas> renkaat = new ArrayList<>();

    public Auto(String malli, String valmistenumero, double ajetutKilometrit) {
        this.malli = malli;
        this.valmistenumero = valmistenumero;
        this.ajetutKilometrit = ajetutKilometrit;

        // Lisätään autolle moottori luomalla uusi moottori-olio.
        moottori = new Moottori("M100", 0);

        // Lisätään autolle neljä rengasta luomalla näille oliot ja lisäämällä 
        // viitteet renkaat-listaan.
        renkaat.add(new Rengas("R1", "nastarengas", 100.0));
        renkaat.add(new Rengas("R2", "nastarengas", 100.0));
        renkaat.add(new Rengas("R3", "nastarengas", 100.0));
        renkaat.add(new Rengas("R4", "nastarengas", 100.0));
    }
}
// FILE_END
// FILE: main.java
void main() {
    Auto auto = new Auto("ABC", "123A", 0);

    IO.println("Auton malli: " + auto.malli);
    IO.println("Auton valmistenumero: " + auto.valmistenumero);

    IO.println("Moottori:");
    IO.println("- " + auto.moottori.malli);
    
    IO.println("Renkaat:");
    for (Rengas rengas : auto.renkaat) {
        IO.println("- " + rengas.malli);
    }
}
// FILE_END
```

Kapseloinnin toinen periaate on luokan sisäisen tiedon *piilottaminen* ja sen
käsittelyn rajoittaminen niin, että siihen päästään käsiksi vain tarkkaan
määritetyn *julkisen rajapinnan* kautta. Oliolla voi olla sen tilan
tallentamista varten paljon sisäistä tietoa, jonka ei ole tarkoitus olla
tarkasteltavissa tai muokattavissa olion ulkopuolelta. Itse asiassa kaikki olion
attribuutit tavallisesti piilotetaan, jotta oliota ei olisi mahdollista
vahingossa saattaa attribuutteja suoraan muuttamalla virheelliseen tilaan.
Oliolla voi myös olla sisäiseen käyttöön apumetodeja, joita ei ole tarkoitus
voida kutsua ulkopuolelta. 

Olion sisäisen tilan muokkaamista varten luokkaan määritellään julkisia
metodeja, joita voidaan kutsua muualta ohjelmasta. Nämä metodit muodostavat
edellä mainitun julkisen rajapinnan ja kaikki muutokset olion tilaan tapahtuvat
niiden kautta, jolloin virheellisiin muutoksiin voidaan reagoida metodin sisällä
sopivalla tavalla.  

Se, mitä attribuutteja luokalla on tai miten niitä käsitellään luokan sisällä
ovat yleensä toteutusyksityiskohtia, joita luokkaa käyttävän ohjelmoijan ei
tarvitse tietää. Tällaisten toteutusyksityiskohtien piilottamisen tavoite on
helpottaa ohjelmoijan työtä; kun luokan toteutusyksityiskohdat ovat piilotettuja
ja tilaa käsitellään vain julkisen rajapinnan kautta, luokan sisäiseen
toimintaan voidaan helpommin tehdä muutoksia niin, että luokan käyttäjä ei edes
huomaa niiden tapahtuneen. Tämä on yksi kapseloinnin suurimmista höydyistä. 

Lisätään `Auto`-luokalle muutama metodi yksinkertaista julkista rajapintaa
varten. Piilotetaan myös attribuutit, että emme voi muuttaa auton tilaa enää
suoraan. Luokan jäsenten näkyvyyttä luokan ja sen olioiden ulkopuolelle voidaan
muuttaa käyttämällä niiden esittelyn yhteydessä *näkyvyysmääreitä* kuten
`public` ja `private`. `Moottori` ja `Rengas` pysyvät vielä samana. 

```java
// FILE: Auto.java
import java.util.ArrayList;

public class Auto {
    private String malli;
    private String valmistenumero;
    private double ajetutKilometrit;
    private Moottori moottori;
    private ArrayList<Rengas> renkaat = new ArrayList<>();

    public Auto(String malli, String valmistenumero, double ajetutKilometrit) {
        this.malli = malli;
        this.valmistenumero = valmistenumero;
        this.ajetutKilometrit = ajetutKilometrit;

        // Lisätään autolle moottori luomalla uusi moottori-olio.
        moottori = new Moottori("M100", 0);

        // Lisätään autolle neljä rengasta luomalla näille oliot ja lisäämällä 
        // viitteet renkaat-listaan.
        renkaat.add(new Rengas("RR", "nastarengas", 100.0));
        renkaat.add(new Rengas("RR", "nastarengas", 100.0));
        renkaat.add(new Rengas("RR", "nastarengas", 100.0));
        renkaat.add(new Rengas("RR", "nastarengas", 100.0));
    }

    public void aja(double kilometrit) {
        if (kilometrit < 0) return;
        this.ajetutKilometrit += kilometrit;
    }

    public void lisaaMoottori(Moottori moottori) {
        this.moottori = moottori;
    }

    public void lisaaRengas(Rengas rengas) {
        this.renkaat.add(rengas);
    }

    public void tulostaTiedot() {
        IO.println("Malli: " + malli);
        IO.println("Valmistenumero: " + valmistenumero);
        IO.println("Ajetut kilometrit: " + ajetutKilometrit);
        
        // Lisätään moottorin ja renkaiden tulostus seuraavaksi.
    }
}
// FILE_END
// FILE: main.java
void main() {
    Auto auto = new Auto("ABC", "123A", 0);
    auto.aja(100);
    auto.tulostaTiedot();
}
// FILE_END
// FILE: Moottori.java
class Moottori {
    String malli;
    double kierrosluku;

    public Moottori(String malli, double kierrosluku) {
        this.malli = malli;
        this.kierrosluku = kierrosluku;
    }
}
// FILE_END
// FILE: Rengas.java
class Rengas {
    String malli;
    String tyyppi;
    double rengaspaine;

    public Rengas(String malli, String tyyppi, double rengaspaine) {
        this.malli = malli;
        this.tyyppi = tyyppi;
        this.rengaspaine = rengaspaine;
    }
}
// FILE_END
```

Piilotimme `Auto`-luokan attribuutit `private`-näkyvyymääritteellä ja auton
tilaa käsitellään nyt yksinkertaisten saantimetodien avulla. Siirsimme myös
tulostamisen luokan vastuulle. Meidän tulisi tehdä vielä samanlaiset muutokset
`Moottori` ja `Rengas` -luokille, jotta voimme käyttää niiden julkisia
rajapintoja `Auto`-luokan sisällä. 

```java
// FILE: Auto.java
import java.util.ArrayList;

public class Auto {
    private String malli;
    private String valmistenumero;
    private double ajetutKilometrit;
    private Moottori moottori;
    private final int maxRenkaat = 4;
    private ArrayList<Rengas> renkaat = new ArrayList<>();

    public Auto(String malli, String valmistenumero, double ajetutKilometrit) {
        this.malli = malli;
        this.valmistenumero = valmistenumero;
        this.ajetutKilometrit = ajetutKilometrit;
    }

    public void aja(double kilometrit) {
        if (kilometrit < 0) return;
        this.ajetutKilometrit += kilometrit;
    }

    public void lisaaMoottori(Moottori moottori) {
        this.moottori = moottori;
    }

    public void lisaaRengas(Rengas rengas) {
        if (renkaat.size() < maxRenkaat) {
            this.renkaat.add(rengas);
        }
    }

    public void tulostaTiedot() {
        IO.println("Auton malli: " + malli);
        IO.println("Auton valmistenumero: " + valmistenumero);
        IO.println("Ajetut kilometrit: " + ajetutKilometrit);
        
        // Välitetään tulostuskomento moottorille, joka tulostaa itse omat tietonsa.
        IO.println();
        IO.println("Moottori:");
        IO.println();
        if (moottori != null) {
            moottori.tulostaTiedot();
        }

        // Välitetään tulostuskomento myös jokaiselle renkaalle.
        IO.println();
        IO.println("Renkaat:");
        for (Rengas rengas : renkaat) {
            IO.println();
            rengas.tulostaTiedot();
        }
    }
}
// FILE_END
// FILE: Moottori.java
public class Moottori {
    private String malli;
    private double kierrosluku;

    public Moottori(String malli, double kierrosluku) {
        this.malli = malli;
        this.kierrosluku = kierrosluku;
    }

    public void tulostaTiedot() {
        IO.println("Malli: " + malli);
        IO.println("Kierrosluku: " + kierrosluku);
    }
}
// FILE_END
// FILE: Rengas.java
public class Rengas {
    private String malli;
    private String tyyppi;
    private double rengaspaine;

    public Rengas(String malli, String tyyppi, double rengaspaine) {
        this.malli = malli;
        this.tyyppi = tyyppi;
        this.rengaspaine = rengaspaine;
    }

    public void tulostaTiedot() {
        IO.println("Malli: " + malli);
        IO.println("Tyyppi: " + tyyppi);
        IO.println("Paine: " + rengaspaine);
    }
}
// FILE_END
// FILE: main.java
void main() {
    Auto auto = new Auto("ABC", "123A", 0);
    auto.lisaaMoottori(new Moottori("M1", 0));
    auto.lisaaRengas(new Rengas("R1", "nasta", 10));
    auto.lisaaRengas(new Rengas("R2", "nasta", 10));
    auto.lisaaRengas(new Rengas("R3", "nasta", 10));
    auto.lisaaRengas(new Rengas("R4", "nasta", 10));
    
    auto.aja(100.0);

    auto.tulostaTiedot();
}
// FILE_END
```

Nyt `Auto`-luokkamme ei enää ole riippuvainen `Moottori` tai `Rengas` -luokkien
sisäisistä toteutusyksityiskohdista. 

### Vastuu olion tilasta kuuluu oliolle itselleen

Joissain tähän mennessä nähdyissä esimerkeissä attribuutteja piilotettiin, mutta 
niitä voitiin edelleen muokata lähes suoraan metodin kautta.
Tämä ei ole täysin olio-ohjelmoinnin tavoitteiden mukaista; julkisen rajapinnan 
ei ole tarkoitus olla vain väliaskel attribuutin muuttamisessa. Julkisen rajapinnan 
idea on välittää oliolle käsky tehdä jotain, jolloin olio suorittaa käskyn itse 
parhaaksi näkemällään tavalla.  

Hyvä esimerkki tästä voisi olla esimerkiksi pelihahmo, jolla on sijaintia varten
attribuutteina koordinaatit `X` ja `Y`. Sen sijaan, että muuttaisimme pelihahmon
sijaintia suoraan yksinkertaisilla `setX` tai `setY` -metodeilla, voisimme
määritellä hahmolle `liiku`-metodin, joka ottaa tavoitekoordinaatit vastaan ja
sallii pelihahmon itse suorittaa tavoitekoordinaatteihin liikkumisen oman
sisäisen toteutuksensa ja rajoitteidensa mukaisesti. Tällöin vastuu
liikkumisesta kuuluu pelihahmolle itselleen. Jos pelihahmo ei esimerkiksi
kykenisi sillä hetkellä liikkumaan, metodi voi käsitellä tilanteen itse, jolloin
metodin kutsujan ei tarvitse ottaa tällaisia erikoistilanteita huomioon. 

Todellisuudessa yksinkertaisia saantimetodeja käytetään usein myös
tuotantokoodissa, sillä olioiden hyvä suunnittelu vie paljon aikaa ja vaivaa.
Joskus voi olla myös ihan perusteltua muuttaa yksinkertaisen attribuutin arvoa
suoraan metodin kautta. Metodi tuntuu tässä tapauksessa aika turhalta, mutta sen
olemassaolo kuitenkin mahdollistaa sen, että luokan sisäistä toteutusta voidaan
muuttaa ilman, että luokkaa käyttävä ohjelmakoodi hajoaa.  

Tällä kurssilla emme valitettavasti ehdi käydä oliosuunnittelun teoriaa
perusteellisesti läpi. Suosittelemme olio-ohjelmoinnin teorian oppimiseen tämän
osan alussa mainittua kurssia. 

## Olioiden yhteistoiminta

Kerrataan vielä esimerkin avulla olioiden ja niiden yhteistyön suunnittelua
tässä osassa opittuja käsitteitä käyttäen. Olioiden hyödyt tulevat paremmin
esille, kun alamme rakentamaan ohjelmaan useampia luokkia, jotka tekevät
yhteistyötä. Nyt kun olemme myös oppineet kapseloinnin periaatteista, voimme
käyttää niitä organisoimaan ohjelmakoodia fiksummin. 

Oliot voivat toimia yhdessä eri tavoin. Oliot voivat esimerkiksi sisältää toisia 
olioita - tai tarkemmin ilmaistuna viitteitä toisiin olioihin. Kun olio koostuu 
olioista, joista jokainen tuo oman toiminnallisuutensa, tätä kutsutaan usein
*kompositioksi*. Oliot voivat kutsua toistensa metodeja ja näin delegoida tehtäviä
toiselle oliolle, jolle tehtävän vastuu kuuluu, tai kommunikoida esimerkiksi
tapahtumien yhteydessä. Oliot voivat myös sisältää kokoelmia olioista;
esimerkiksi Javan sisäänrakennetut tietorakenteet ovat olioita, jotka sisältävät
kokoelman olioista. 

Katsotaan esimerkkiä, jossa haluamme mallintaa ohjelmallamme rakennuksia, niissä
sijaitsevia tiloja sekä tiloihin tehtäviä varauksia. Jokaisessa rakennuksessa
voi olla monta tilaa ja jokaisessa tilassa voi olla monta varausta. Emme välitä
vielä tässä esimerkissä siitä, voiko varauksia olla samassa tilassa päällekkäin.
Pidetään myös luokat vielä suhteellisen yksinkertaisina. 

Aloitetaan määrittelemällä tarvittavat luokat `Rakennus`, `Tila` ja `Varaus`.
Tehdään näille myös muodostajat, jotka alustavat olion heti käyttökelpoiseen 
tilaan.

```java,ignore
// FILE: Rakennus.java
import java.util.*;

public class Rakennus {
    private String nimi;
    private List<Tila> tilat = new ArrayList<>();
    
    public Rakennus(String nimi) { 
        this.nimi = nimi;
    }
}
// FILE_END
// FILE: Tila.java
import java.util.*;

public class Tila {
    private String nimi;
    private List<Varaus> varaukset = new ArrayList<>(); 
    
    public Tila(String nimi) { 
        this.nimi = nimi; 
    } 
    
    public String getNimi() { 
        return nimi; 
    }
}
// FILE_END
// FILE: Varaus.java
public class Varaus {
    private String varaaja;
    private int ajankohta;
    private int kesto;

    public Varaus(String varaaja, int ajankohta, int kesto) { 
        this.varaaja = varaaja;
        this.ajankohta = ajankohta;
        this.kesto = kesto;
    }
}
// FILE_END
```

Lisätään nyt rakennukselle sopivat metodit tilojen lisäämiseen. Haluaisimme
löytää oikean tilan myöhemmin sen nimen perusteella, joten rakennuksessa ei
saisi olla saman nimisiä tiloja. Tarvitsemme siis myös keinon hakea tila sen
nimen perusteella. Tilan lisäämiseen tarvitsemme vain tilan nimen.

```java,ignore
// FILE: Rakennus.java
import java.util.*;

public class Rakennus {
    private String nimi;
    private List<Tila> tilat = new ArrayList<>();
    
    public Rakennus(String nimi) { 
        this.nimi = nimi;
    }

    public Tila haeTila(String tilanNimi) {
        for (Tila tila : tilat) { 
            if (tila.getNimi().equals(tilanNimi)) {
                return tila;
            }
        }
        return null;
    }

    public void lisaaTila(String tilanNimi) { 
        Tila tila = haeTila(tilanNimi); 
        if (tila != null) {
            IO.println("Rakennus " + nimi + " sisältää jo tilan " + tilanNimi);
            return;
        } 
        tilat.add(new Tila(tilanNimi)); 
    }
}
// FILE_END
// FILE: Tila.java
import java.util.*;

public class Tila {
    private String nimi;
    private List<Varaus> varaukset = new ArrayList<>(); 
    
    public Tila(String nimi) { 
        this.nimi = nimi; 
    } 
    
    public String getNimi() { 
        return nimi; 
    }
}
// FILE_END
// FILE: Varaus.java
public class Varaus {
    private String varaaja;
    private int ajankohta;
    private int kesto;

    public Varaus(String varaaja, int ajankohta, int kesto) { 
        this.varaaja = varaaja;
        this.ajankohta = ajankohta;
        this.kesto = kesto;
    }
}
// FILE_END
```

Tilaan pitäisi voida tehdä varauksia. Lisätään tämä ominaisuus, mutta pidetään 
esimerkki yksinkertaisena tekemällä varaukset tasatunneille. Ohjelman tila 
voisi kuvastaa esimerkiksi seuraavan päivän tilavarauksia. 

Tarvitsemme varauksen tekemiseen varaajan nimen sekä varauksen alkamistunnin ja 
keston. Lisätään oheinen metodi `Tila`-luokkaan.

```java,ignore
public void lisaaVaraus(String varaaja, int ajankohta, int kesto) { 
    varaukset.add(new Varaus(varaaja, ajankohta, kesto)); 
}
```

Lisätään vielä mahdollisuus lisätä varauksia *rakennuksen* kautta niin, että
käyttäjän ei tarvitse edes tietää, että `Tila`-luokka on olemassa. Se miten
`Rakennus` tallentaa tiedot tiloista jää sen toteutusyksityiskohdaksi.

Tarvitsemme varauksen lisäämiseen tilan ja varaajan nimet sekä varauksen
alkamistunnin ja keston.

Lisätään myös yksinkertaiset `tulosta`-metodit kaikkiin luokkiin, jotta voimme 
nähdä kaikki rakennuksen tilat ja varaukset helposti.

```java
// FILE: Rakennus.java
import java.util.*;

public class Rakennus {
    private String nimi;
    private List<Tila> tilat = new ArrayList<>();
    
    public Rakennus(String nimi) { 
        this.nimi = nimi;
    }

    public Tila haeTila(String tilanNimi) {
        for (Tila tila : tilat) { 
            if (tila.getNimi().equals(tilanNimi)) {
                return tila;
            }
        }
        return null;
    }

    public void lisaaTila(String tilanNimi) { 
        Tila tila = haeTila(tilanNimi); 
        if (tila != null) {
            IO.println("Rakennus '" + nimi + "' sisältää jo tilan '" + tilanNimi + "'");
            return;
        } 
        tilat.add(new Tila(tilanNimi)); 
    }

    public void lisaaVaraus(String tilanNimi, String varaaja, int ajankohta, int kesto) { 
        Tila tila = haeTila(tilanNimi); 
        if (tila == null) {
            IO.println("Rakennuksessa '" + nimi + "' ei ole tilaa '" + tilanNimi + "'");
            return;
        } 
        tila.lisaaVaraus(varaaja, ajankohta, kesto);
    }

    public void tulosta() {
        IO.println(nimi);
        for (Tila tila : tilat) {
            tila.tulosta();
        }
    }
}
// FILE_END
// FILE: Tila.java
import java.util.*;

public class Tila {
    private String nimi;
    private List<Varaus> varaukset = new ArrayList<>(); 
    
    public Tila(String nimi) { 
        this.nimi = nimi; 
    } 
    
    public String getNimi() { 
        return nimi; 
    }

    public void lisaaVaraus(String varaaja, int ajankohta, int kesto) { 
        varaukset.add(new Varaus(varaaja, ajankohta, kesto)); 
    }

    public void tulosta() {
        IO.print(" ");
        IO.println(nimi);
        if (varaukset.isEmpty()) {
            IO.print("  ");
            IO.println("Ei varauksia.");
        }
        else {
            for (Varaus varaus : varaukset) {
                varaus.tulosta();
            }
        }
    }
}
// FILE_END
// FILE: Varaus.java
public class Varaus {
    private String varaaja;
    private int ajankohta;
    private int kesto;

    public Varaus(String varaaja, int ajankohta, int kesto) { 
        this.varaaja = varaaja;
        this.ajankohta = ajankohta;
        this.kesto = kesto;
    }

    public void tulosta() {
        IO.print("  ");
        IO.println("Klo " + ajankohta + "-" + (ajankohta + kesto) + ", varaaja " + varaaja);
    }
}
// FILE_END
// FILE: main.java
void main() {
    Rakennus agora = new Rakennus("Agora"); 
    agora.lisaaTila("Auditorio 1"); 
    agora.lisaaTila("AgFinland"); 
    agora.lisaaTila("AgFinland"); // Ei onnistu.

    agora.lisaaVaraus("AgFinland", "Maija", 8, 2); 
    agora.lisaaVaraus("AgFinland", "Matti", 10, 2); 
    agora.lisaaVaraus("Auditorio 5", "Maija", 13, 1); // Ei onnistu.

    IO.println();
    agora.tulosta();
}
// FILE_END
```

Voimme nyt käyttää `Rakennus`-luokkaa niin, että meidän ei tarvitse olla
tietoisia tilojen tai varausten toiminnasta. Vastaavasti `Rakennus` ei riipu
suoraan siitä, miten `Tila` tallentaa varausten tietoja.

Tässä vaiheessa meiltä puuttuu vielä osa olio-ohjelmoinnin tärkeimmistä 
työkaluista; perintä, polymorfismi ja rajapinnat. Tutustumme näihin seuraavassa
osassa.

## Tehtävät

<task>
  <task-title>Tehtävä 2.6: Ovi<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-6-ovi/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava6">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 2.7: Säästölipas<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-7-saastolipas/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava7">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 2.8: Sähköverkko<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-8-sahkoverkko/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava8">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title><i class="bi bi-stars jyu-gold"></i>Bonus: Tehtävä 2.9: Varaukset<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-9-varaukset/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava9">Tee tehtävä TIMissä</a></task-link>
</task>