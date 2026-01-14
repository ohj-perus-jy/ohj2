# Luokka ja olio

> [!Osaamistavoitteet]
>
> - Luokka ja olio
> - Konstruktori, metodi, attribuutti
> - Luokan rakenne ja suhde olioon (konstruktori, attribuutti, metodi, this-viite, "luokka blueprintina oliolle")
> - Osaat määritellä ja hyödyntää omia luokkia Javalla

## Luokka

Ensimmäinen askel olio-ohjelmointiin on luokan määritteleminen
`class`-avainsanaa käyttäen. Luokkaa voi ajatella kaavana tai muottina, jonka
pohjalta olioita luodaan. Luokka kertoo, mitä tietoja olio sisältää
(attribuutit) ja mitä se voi tehdä (metodit). Luokassa määriteltyjä
attribuutteja ja metodeja kutsutaan myös *luokan jäseniksi* (engl. *class
member*).

Tehdään pieni ajatusharjoitus: mietitään hetki talonrakennusta. Arkkitehdin
piirtämän yhden rakennuspiirustuksen pohjalta voidaan rakentaa monta rakennusta.
Ne olisivat rakenteeltaan samanlaisia, sillä ne ovat saman kaavan mukaan tehty,
mutta jokaisella rakennuksella olisi kuitenkin oma tila; eri omistaja, väri,
sisustus, ja niin edelleen. Rakennuspiirustusta voi (ainakin etäisesti) ajatella
olio-ohjelmoinnin luokkana, kun taas rakennukset ovat sen pohjalta tehtyjä
olioita. Luokan nimi kertoo, *mikä* olio on, joten jos tekisimme luokan
rakennuksille, sen nimeksi sopisi `Rakennus`.

Huomaa, että Javassa on tapana aloittaa luokkien nimet aina isolla kirjaimella.

Määritellään aluksi tyhjä luokka `Rakennus`, jota lähdemme täydentämään.

```java,ignore
class Rakennus {
    // Luokan sisällä määritellään rakenne, jota luokasta 
    // tehdyt oliot vastaavat.
}
```

Luokasta luodaan ilmentymiä eli *olioita* käyttämällä avainsanaa `new`. Tämä
varaa muistista oliolle sopivan tilan, valitsee ja suorittaa sopivan
muodostajan, ja palauttaa viitteen juuri luotuun olioon. Sijoitamme tämän
viitteen muuttujaan, jotta pääsemme olioon sitä kautta käsiksi. Luokan nimi on
muuttujan tyyppi ja siten kertoo kääntäjälle, _millainen_ olio muistisijainnissa
täytyy olla.

```java,ignore
void main() {
    // Lauseke 'new Rakennus()' luo olion ja palauttaa viitteen siihen. 
    // Sijoitamme tämän viitteen muuttujaan 'rakennus'.
    Rakennus rakennus = new Rakennus();
}
```

> [!HUOMAUTUS]
> Viitemuuttuja ja olio ovat kaksi eri asiaa.
> Viitemuuttuja on kuin nuoli, joka voi osoittaa olioon. Viitemuuttujan ei kuitenkaan ole
> pakko viitata mihinkään, jolloin sen arvo on `null`. Olio on vastaavasti
> mahdollista luoda ilman siihen viittaavaa muuttujaa, mutta jos olioon
> osoittavia viitteitä ei ole, siihen ei päästä käsiksi ja se merkitään automaattisesti roskaksi. Useampi
> viitemuuttuja voi viitata samaan olioon, mutta viitemuuttuja voi osoittaa vain
> yhteen olioon kerrallaan. 

## Attribuutit

Attribuutti on luokan sisällä määritelty muuttuja, joka edustaa olion
ominaisuutta, piirrettä tai tilaa. Siinä missä luokka määrittelee, mitä tietoja
olioilla voi olla, attribuutit tallentavat kunkin yksittäisen olion
konkreettiset arvot. Kuten muuttujat yleensä, attribuutit voivat olla
alkeistietotyyppejä tai viitteitä. Niiden nimeämisessä käytetään myös samoja
käytänteitä.  

Lisätään nyt muutama attribuutti `Rakennus`-luokkaamme.

```java,ignore
public class Rakennus {
    // Nämä muuttujat ovat olion attribuutteja. Jokaisella rakennuksella
    // on omistaja ja väri, mutta ne eivät välttämättä ole kaikilla 
    // olioilla arvoiltaan samat.
    private String omistaja;

    // Attribuutille voidaan asettaa oletusarvo. Tässä värin oletusarvo on 
    // sininen, jolloin kaikilla tämän luokan pohjalta tehdyillä olioilla
    // on aluksi tämä arvo, ellei sitä muuteta.
    private String väri = "sininen";
}
```

Attribuutit poikkeavat esimerkiksi aliohjelmien paikallisista muuttujista siten,
että niiden näkyvyyttä voidaan hallita erilaisten näkyvyysmääreiden avulla.
Aliohjelman paikalliset muuttujat ovat olemassa ja nähtävillä vain aliohjelman
sisällä sen suorituksen ajan, mutta attribuutit ovat olemassa koko olion eliniän
ajan ja ne *voidaan* asettaa näkyväksi myös olion ulkopuolelta, joskin tämä on
yleisesti ottaen huono idea. Palaamme näkyvyysmääreisiin myöhemmin tässä osassa.

Luokasta tehdyt oliot sisältävät aina luokassa määritellyt attribuutit.
Attribuutille voidaan luokassa antaa oletusarvo, jolloin luokasta luodut oliot
saavat sen myös oman attribuuttinsa alkuarvoksi. Jos attribuutilla ei ole
oletusarvoa, sen arvo voidaan määrittää olion luomisen yhteydessä, myöhemmin
metodien avulla, tai jopa jättää määrittämättä.

> [!HUOMAUTUS]
> Luokassa olevien aliohjelmien sisällä esitellyt muuttujat eivät ole
> attribuutteja, vaan aliohjelman *paikallisia* eli *lokaaleja* muuttujia. Vain
> suoraan luokan alla olevat muuttujat ovat attribuutteja. Lokaalien muuttujien
> sisältämä tieto katoaa aliohjelman suorituksen lopussa, eli ne eivät ole osa
> olion tilaa. Paikallisella muuttujalla voi olla sama nimi kuin attribuutilla,
> jolloin se peittää attribuutin. Tätä kutsutaan varjostamiseksi (engl.
> *shadowing*). Jos attribuutilla ja paikallisella muuttujalla on sama nimi,
> käytetään lausekkeissa ensisijaisesti lokaalia muuttujaa. Tässäkin tilanteessa 
> olion metodeista voi yhä päästä käsiksi sen attribuuttiin 
> käyttämällä `this`-viitettä, johon palaamme hyvin pian.

```java,ignore
public class Rakennus {
    // Olion attribuutti, jolla on oletusarvo.
    private String väri = "sininen";

    public void tulosta()
    {
        // Tämä lokaali muuttuja peittää saman nimen omaavan attribuutin 
        // aliohjelman sisällä.
        String väri = "punainen"; 

        // Tulostaa "punainen". Tunniste 'väri' viittaa ensisijaisesti 
        // lokaaliin muuttujaan, jos sellainen on näkyvissä.
        IO.println(väri); 

        // Tulostaa "sininen". Voimme viitata olion metodin sisältä sen 
        // attribuuttiin 'this'-viitteen avulla.
        IO.println(this.väri); 
    }
}
```

## Metodit

Luokassa määriteltyjä aliohjelmia kutsutaan *metodeiksi*. Siinä missä
attribuuttia voisi kuvailla niin, että se muodostaa olion sisäisen tilan,
metodia voisi kuvailla olion kyvyksi tehdä jotain. Javassa erikoista on se, 
että kaikki aliohjelmat ovat itse asiassa aina *jonkin* luokan sisällä ja siten 
metodeja.

Metodien määrittely ei syntaksiltaan eroa muista aliohjelmista, ja niiden
nimeämisessä käytetään myös samanlaisia käytänteitä. Metodeja
voidaan myös kuormittaa. Metodien näkyvyyttä luokan ulkopuolelle voidaan hallita
attribuuttien tapaan näkyvyysmääreiden avulla.

Kuten yleensä aliohjelmia tehdessä, metodin tulisi suorittaa tehtävä, jota sen 
nimi kuvastaa. Liian suuret tehtävät on hyvä jakaa pienempiin osiin eli 
useammaksi metodiksi.

Voidaksemme kutsua olion metodia, meillä täytyy olla olio ja siihen viite.
Lisätään nyt `Rakennus`-luokkaamme pari yksinkertaista metodia olion tilan
käsittelyyn ja kutsutaan näitä. Tällaisia metodeja kutsutaan usein
saantimetodeiksi.

```java
// FILE: Rakennus.java
public class Rakennus {
    private String omistaja;
    private String väri;

    // Olion metodi, joka ottaa vastaan merkkijonon ja sijoittaa 
    // sen 'väri'-attribuuttiin.
    public void setVäri(String väri) {
        // Parametrilla ja attribuutilla on sama nimi, joten käytämme 
        // this-viitettä.
        this.väri = väri;
    }

    // Olion metodi, joka palauttaa 'väri'-attribuutin arvon kutsujalle.
    public String getVäri() {
        return this.väri;
    }
}
// FILE_END
// FILE: main.java
void main() {
    // Luodaan kaksi rakennusta.
    Rakennus rakennus1 = new Rakennus();
    Rakennus rakennus2 = new Rakennus();

    // Käytetään olioiden metodeja muuttamaan niiden tilaa.
    rakennus1.setVäri("vihreä");
    rakennus2.setVäri("valkoinen");

    // Tulostetaan olioiden värit saantimetodien avulla.
    IO.println(rakennus1.getVäri()); // Tulostaa "vihreä"
    IO.println(rakennus2.getVäri()); // Tulostaa "valkoinen"

    // Huom! Emme voi kutsua olion metodia ilman oliota. Jos yritämme 
    // kutsua olion metodia luokan kautta seuraavasti, se aiheuttaa virheen.
    // Rakennus.setVäri("sininen");
}
// FILE_END
```

Voisimme lisätä myös vastaavat metodit luokan toista attribuuttia varten.
Keskustelemme myöhemmin tässä osassa siitä, miten olion tilaa voidaan käsitellä
hieman järkevämmin, mutta tässä vaiheessa tällaiset yksinkertaiset `get` ja
`set` -metodit riittävät.

## This-viite

Avainsana `this` viittaa olioon itseensä. Se toimii viitteenä "tähän olioon",
jonka kontekstissa koodia suoritetaan. 

Käytimme tämän osan alun esimerkeissä `this`-viitettä lukeaksemme olion
attribuutteja näin: 

```java,ignore
public class Rakennus {
    private String väri;

    // ...

    public String getVäri() {
        return this.väri;
    }
}
```

Tämä viite on automaattisesti käytettävissä aina, kun kutsutaan jonkin olion
metodia. Metodikutsun yhteydessä `this` asetetaan osoittamaan metodin
suorituksen sisällä siihen olioon, jonka metodia kutsuttiin, eikä sitä voi
muuttaa. Viitteen kautta metodi pääsee käsiksi oikean olion tilaan sekä sen
muihin metodeihin. Olion metodien sisällä `this`-viitettä käytetään
implisiittisesti, jos samalla näkyvyysalueella ei ole konfliktia tunnisteissa -
esimerkiksi attribuutin kanssa samaa nimeä käyttävää lokaalia muuttujaa. Meidän
ei siis tarvitse kirjoittaa aina attribuutin tai metodikutsun eteen `this`,
sillä kääntäjä osaa päätellä sen itse, jos konfliktia ei ole. Joissain
ohjelmointikielissä tällaista viitettä kutsutaan myös nimellä `self`.

Katsotaan muutamaa esimerkkiä `this`-viitteen käytöstä.

```java
// FILE: Rakennus.java
public class Rakennus {
    private String omistaja;
    private String väri;

    public void setVäri(String väri) {
        // Käytämme tässä this-viitettä, sillä attribuutilla ja parametrilla 
        // on sama nimi. Lokaalia muuttujaa käytettäisiin muuten ensisijaisesti.
        this.väri = väri; 
    }

    public String getVäri() {
        // Tässä this on vapaaehtoinen. Samalla näkyvyysalueella ei ole muita 
        // "väri" nimisiä muuttujia, joten sekaannusta ei tapahdu.
        // this-viitteen käyttö on kuitenkin täysin sallittua.
        return this.väri;
    }
}
// FILE_END
// FILE: main.java
void main() {
    Rakennus talo = new Rakennus();

    // Kutsumme 'talo' viitteen kautta löytyvän olion setVäri-metodia, joten 
    // tämän metodikutsun suorituksessa 'this' viittaa samaan olioon kuin 
    // pääohjelman 'talo'.
    talo.setVäri("harmaa");

    IO.println(talo.getVäri());
}
// FILE_END
```

Metodien sisällä voimme käyttää `this`-viitettä kuin muitakin viitemuuttujia.
Voimme esimerkiksi välittää sen toiselle aliohjelmalle parametrina. Tämä ei ole
tarpeen olion omia metodeja kutsuessa, mutta voimme näin välittää viitteen 
olioon myös luokan ulkopuolisille aliohjelmille.

```java
// FILE: Rakennus.java
public class Rakennus {
    private String omistaja;
    private String väri;

    public String getOmistaja() {
        return omistaja;
    }

    public void setOmistaja(String omistaja) {
        this.omistaja = omistaja;
    }

    public String getVäri() {
        return väri;
    }

    public void setVäri(String väri) {
        this.väri = väri;
    }

    // Olion metodi.
    public String kaunista() {
        // Välitetään omistava olio toisen luokan metodille.
        return Kaunistaja.MuotoileKauniisti(this);
    }
}
// FILE_END
// FILE: Kaunistaja.java
public class Kaunistaja {
    public static String MuotoileKauniisti(Rakennus rakennus) {
        return "Ihana rakennus, jonka omistaa "
                + rakennus.getOmistaja()
                + ", on väriltään "
                + rakennus.getVäri().toLowerCase() + ".";
    }
}

// FILE_END
// FILE: main.java
void main() {
    Rakennus talo = new Rakennus();
    talo.setOmistaja("Maija Opettaja");
    talo.setVäri("Keltainen");
    IO.println(talo.kaunista());
}
// FILE_END
```

## Muodostaja eli konstruktori

Muodostaja eli konstruktori on luokan erikoismetodi, jota käytetään uuden olion 
luomisen yhteydessä sen tilan alustamiseen. Muodostajan nimi on aina sama kuin 
luokan nimi ja se kirjoitetaan isolla alkukirjaimella, mikä poikkeaa muiden 
metodien nimeämistyylistä. Muodostajalle ei määritetä paluuarvon tyyppiä, vaan 
muodostaja palauttaa aina viitteen muodostettuun olioon.

Luokassa täytyy olla ainakin yksi muodostaja. Olemme kuitenkin tähän asti
luoneet olioita määrittelemättä luokkaan muodostajaa. Tämä onnistuu
Javassa, sillä jos luokkaan *ei* ole tehty yhtään muodostajaa, kääntäjä luo
automaattisesti parametrittoman muodostajan. Automaattisesti luotu parametriton
muodostaja on toteutukseltaan tyhjä siinä mielessä, että se ei sisällä yhtään
lausetta. Parametritonta muodostajaa ei luoda automaattisesti, jos
määrittelemme luokkaan yhdenkin muodostajan itse.

Muodostajan nimi on aina sama kuin luokan, joten teemme siis muodostajia 
lisätessämme metodin kuormitusta erilaisilla parametreilla. Kääntäjä valitsee 
oikean muodostajan automaattisesti olion luomisen yhteydessä annettujen 
argumenttien perusteella. 

Käytimme aikaisemmassa esimerkissä `Rakennus`-luokkaa määrittelemättä
muodostajaa. Otetaan metodit hetkeksi pois selkeyden vuoksi ja katsotaan, mitä
olioita luodessa tapahtuu. 

```java,ignore
// FILE: Rakennus.java
public class Rakennus {
    private String omistaja;
    private String väri;
}
// FILE_END
// FILE: main.java
void main() {
    // Emme määritelleet luokkaan yhtään muodostajaa itse, joten
    // olio luodaan oletusmuodostajaa käyttäen.
    Rakennus rakennus = new Rakennus();
}
// FILE_END
```

Tässä tapauksessa olio muodostetaan automaattista oletusmuodostajaa käyttäen,
sillä yhtään muodostajaa ei ole määritelty. Voimme tehdä vastaavan muodostajan
itsekin seuraavasti. 

```java,ignore
// FILE: Rakennus.java
public class Rakennus {
    private String omistaja;
    private String väri;

    // Parametriton muodostaja, joka vastaa oletusmuodostajaa.
    public Rakennus() {
        // Voisimme täällä alustaa olion tilan jollain tavalla, 
        // asettamalla attribuuteille alkuarvot.
    }
}
// FILE_END
// FILE: main.java
void main() {
    // Olio luodaan itse määrittelemäämme parametritonta muodostajaa käyttäen.
    Rakennus rakennus = new Rakennus();
}
// FILE_END
```

Olemme tähän asti muodostaneet olioita ilman kunnollista alustusta. Tämä ei ole
hyvä käytäntö, joten korjataan tilanne seuraavaksi.

Rakennukset ovat heti luomisen jälkeen tilassa, jossa niillä ei ole omistajaa 
tai väriä. Tällä hetkellä vasta luodun olion attribuuttien arvot ovat `null`.
Oliosta ja sen tarkoituksesta riippuen tällaiset arvot *voivat* olla sallittuja,
mutta jos rakennus on olemassa, sillä täytynee olla jokin omistaja ja väri.

Olisi parempi, että olio olisi heti luonnin jälkeen käyttökelpoinen. Voisimme
luoda olion suoraan oikeaan tilaan määrittelemällä muodostajan, joka ottaa olion
tilan alustamiseen tarvittavat tiedot vastaan parametreina ja alustaa
attribuutit oikein.

Lisätään nyt `Rakennus`-luokalle toinen muodostaja, joka ottaa omistajan ja
värin vastaan parametreina ja alustaa näillä olion attribuutit. Näin meidän ei
tarvitse asettaa attribuutteja erikseen olion luomisen jälkeen. Voimme nyt myös 
poistaa parametrittoman muodostajan, jotta sitä ei voi enää käyttää
luomaan olioita, joilla on virheellinen alkutila.

```java,ignore
// FILE: Rakennus.java
public class Rakennus {
    private String omistaja;
    private String väri;

    public Rakennus(String omistaja, String väri) {
        // Alustetaan olion tila parametreilla. Huomaa tässä this-viitteen 
        // käyttö, sillä parametrien ja attribuuttien nimet ovat samat.
        this.omistaja = omistaja;
        this.väri = väri;
    }
}
// FILE_END
// FILE: main.java
void main() {
    // Oliolle annetaan kaksi merkkijonoa argumentteina. Nämä vastaavat 
    // määrittelemäämme parametrillista muodostajaa, joten sitä käytetään 
    // olion muodostamiseen.
    Rakennus rakennus1 = new Rakennus("JYU", "valkoinen");

    // Tämä ei onnistuisi, sillä emme ole määritelleet muodostajaa, jossa on 
    // vain yksi parametri.
    // Rakennus rakennus2 = new Rakennus("JYU");

    // Tämäkään ei onnistuisi, sillä parametritonta muodostajaa ei enää ole 
    // eikä sellaista enää luoda automaattisesti.
    // Rakennus rakennus3 = new Rakennus();
}
// FILE_END
```

Lisätään vielä lopuksi hieman erikoisempi muodostaja, joka ottaa vastaan toisen
saman luokan olion ja kopioi sen tilan muodostettavalle oliolle. Tällaisesta
muodostajasta puhuttaessa käytetään usein nimitystä *copy constructor*. 

```java,ignore
// FILE: Rakennus.java
public class Rakennus {
    private String omistaja;
    private String väri;

    public Rakennus(String omistaja, String väri) {
        this.omistaja = omistaja;
        this.väri = väri;
    }

    // Muodostaja, joka ottaa vastaan toisen saman luokan olion ja 
    // kopioi sen arvot muodostettavalle oliolle.
    public Rakennus(Rakennus kopioitava) {
        this.omistaja = kopioitava.omistaja;
        this.väri = kopioitava.väri;
    }
}
// FILE_END
// FILE: main.java
void main() {
    Rakennus rakennus1 = new Rakennus("JYU", "valkoinen");

    // Antamalla argumenttina toisen Rakennus-tyyppisen olion käytämme uutta 
    // muodostaa, joka kopioi olion arvot. Molemmilla rakennuksilla on nyt 
    // sama omistaja ja väri.
    Rakennus rakennus2 = new Rakennus(rakennus1);
}
// FILE_END
```

Voimme lisäksi käyttää muodostajassa `this`-avainsanaa kuin metodia, jos
haluamme siirtää muodostamisen toiselle saman luokan muodostajalle. Voimme usein
välttää näin turhaa toistoa.

Muutetaan luokkaa nyt niin, että parametriton muodostaja käyttää parametrillista 
muodostajaa antamaan attribuuteille alkuarvot.

```java,ignore
// FILE: Rakennus.java
public class Rakennus {
    private String omistaja;
    private String väri;

    public Rakennus(String omistaja, String väri) {
        this.omistaja = omistaja;
        this.väri = väri;
    }

    public Rakennus(Rakennus kopioitava) {
        // Siirrämme muodostamisen yllä olevalle muodostajalle sitä 
        // vastaavilla parametreilla
        this(kopioitava.omistaja, kopioitava.väri);
    }
}
// FILE_END
```

<task>
  <task-title>Tehtävä 2.1: Luokkia ja olioita, osa 1<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-1-luokkia-ja-olioita1/handout.md}}
  
  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava1">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 2.2: Oma luokka<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-2-oma-luokka/handout.md}}
  
  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava2">Tee tehtävä TIMissä</a></task-link>
</task>


## Static

Staattisuuden käsite on usein alussa hieman hankala ymmärtää. Kannattaa aluksi 
lukea kertauksena Ohjelmointi 1 -kurssin
[materiaaleista](https://tim.jyu.fi/view/kurssit/tie/ohj1/materiaali/staattiset)
staattisuutta koskeva osa. Luokan jäsenten osalta staattisuus toimii samalla
tavalla myös Javassa. Käytämme tässä Javassa yleensä käytettyjä termejä,
mutta mainittakoon, että nimityskäytännöt vaihtelevat hieman
ohjelmointikielestä riippuen.

Tavallisia, ei-staattisia attribuutteja ja metodeja kutsutaan *olion* 
attribuuteiksi (engl. *instance attribute*) ja -metodeiksi 
(engl. *instance method*). Nimensä mukaisesti olion attribuutit ja metodit 
liittyvät olioon; jokaisella oliolla on tällaisille attribuuteille oma arvo ja 
metodit kiinnittyvät olioon, jolle ne kuuluvat, minkä vuoksi ne pääsevät olion 
tilaan käsiksi.

Luokan jäsenet voidaan määritellä kuuluvaksi olion sijaan **luokalle** 
`static`-määritettä käyttämällä. Tällaisia attribuutteja ja metodeja kutsutaan 
*luokan* attribuuteiksi (engl. *class attribute*) ja -metodeiksi 
(engl. *class method*). Sana `static` voi olla hieman harhaanjohtava;
*staattisuus* ei tässä tarkoita, että nämä luokan jäsenet ovat pysyviä tai 
muuttumattomia.

Luokan attribuutti ei ole osa minkään olion tilaa ja sillä on vain yksi arvo, 
joka on jaettu kaikkien luokan olioiden kesken. Jos yksi olio muuttaa oman 
luokkansa attribuutin arvoa, muutos näkyy kaikissa saman luokan olioissa. 

Samalla tavalla voimme ajatella myös luokan metodien olevan jaettu kaikkien 
luokan olioiden kesken; ne eivät liity mihinkään olioon, eivätkä siten pääse 
minkään olion tilaan suoraan käsiksi. Oliot voivat kutsua oman luokkansa
(staattista) metodia, mutta se ei silti mahdollista olion tilan käsittelyä tämän
metodin sisältä. Koska staattiset metodit eivät liity mihinkään olioon, niiden 
sisällä ei myöskään voi käyttää `this`-viitettä.

Voidaksemme kutsua **olion metodia**, meillä täytyy olla olio ja siihen viite.
Staattista **luokan metodia** sen sijaan voimme kutsua suoraan luokan kautta
ilman olion luomista. Staattista metodia *on mahdollista* kutsua myös
olioviitteen kautta, mutta tämäkään ei mahdollista olion tilan tarkastelua
metodin sisältä. 

Tehdään aluksi luokka, jossa ei ole staattisia jäseniä.

```java
// FILE: Henkilo.java
public class Henkilo {
    private String etunimi;
    private String sukunimi;

    public Henkilo(String etunimi, String sukunimi) {
        this.etunimi = etunimi;
        this.sukunimi = sukunimi;
    }

    public String annaNimi() {
        return etunimi + " " + sukunimi;
    }
}
// FILE_END
// FILE: main.java
void main() {
    // Emme voi kutsua olion metodia suoraan luokan kautta ilman oliota.
    // Henkilo.annaNimi();

    Henkilo h1 = new Henkilo("Anna", "Korhonen");
    IO.println(h1.annaNimi());
}
// FILE_END
```

Koska `annaNimi` on *olion* metodi, meidän täytyy ensin luoda olio. Emme voi
kutsua tätä metodia *staattisesti* luokan kautta, eikä siinä olisi oikeastaan
järkeä.

Lisätään nyt *luokan* attribuutti `luokanNimi` ja -metodi
`annaLuokanNimi`, joka yksinkertaisesti palauttaa staattisen attribuutin arvon. 

> [!HUOMAUTUS]
> Vastaava staattinen metodi itse asiassa on jo olemassa nimellä `getClass`,
> vaikka emme sellaista itse määrittelekään. Tällaisia valmiita metodeja on
> kaikissa luomissamme luokissa valmiiksi. Palaamme tähän osassa 3.

```java
// FILE: Henkilo.java
public class Henkilo {
    private String etunimi;
    private String sukunimi;
    private static String luokanNimi = "Henkilo";

    public Henkilo(String etunimi, String sukunimi) {
        this.etunimi = etunimi;
        this.sukunimi = sukunimi;
    }

    public String annaNimi() {
        return etunimi + " " + sukunimi;
    }

    public static String annaLuokanNimi() {
        return luokanNimi;
    }
}
// FILE_END
// FILE: main.java
void main() {
    // Emme voi kutsua olion metodia suoraan luokan kautta ilman oliota.
    // Henkilo.annaNimi();

    Henkilo h1 = new Henkilo("Anna", "Korhonen");
    IO.println(h1.annaNimi());

    // Staattista metodia sen sijaan voi kutsua luokan kautta:
    IO.println(Henkilo.annaLuokanNimi());

    // Staattista metodia voi kutsua myös olion kautta, mutta selkeyden vuoksi 
    // on parempi käyttää luokkaa.
    // IO.println(h1.annaLuokanNimi());
}
// FILE_END
```

Nyt meillä on *luokan* metodi `annaLuokanNimi`, jota voimme kutsua ilman oliota.
Voisimme kutsua tätä luokan metodia myös olion kautta, mutta se ei ole tarpeen
ja kääntäjä varoittaakin siitä.

> [!HUOMAUTUS]
> Tekstin tulostamiseen käyttämämme `IO.println()` on itse asiassa
> [IO-luokan](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/io/IO.html)
> staattinen metodi. Sen käyttäminen on helpompaa, kun meidän ei tarvitse joka
> kerta luoda IO-oliota ja kutsua sen `println`-metodia.

<task>
  <task-title>Tehtävä 2.3: Static<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-3-static/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava3">Tee tehtävä TIMissä</a></task-link>
</task>

## Olion elinkaari

Ohjelman ajon aikana luokasta luodaan ilmentymä eli olio. 
Jotta olioon voidaan päästä käsiksi, luodaan sitä varten viitemuuttuja.
Javan kääntäjä tarkistaa käännöksen yhteydessä, että muuttuja on yhteensopiva
luodun olion kanssa, ja asettaa viitteen osoittamaan luotuun olioon.

Olion luonnin yhteydessä Java varaa sille sopivan tilan virtuaalikoneensa 
kekomuistista. Kun olioon ei enää ole yhtään viitettä olemassa, se tuhoutuu. 
Javassa ohjelmoijan ei tarvitse itse pitää huolta muistin varaamisesta tai
vapauttamisesta. Tuhoutuneiden olioiden varaama muisti vapautetaan lopulta Javan
automaattisen roskienkeräyksen toimesta.

Käydään vielä olion koko elinkaari läpi esimerkkien avulla. Tarvitsemme olioiden
luomista varten ensimmäiseksi luokan. Käytetään esimerkkinä taas 
`Henkilo`-luokkaa, mutta lisätään nyt muutama hyvin yksinkertainen metodi olion 
tilan muuttamiseen.

```java
// FILE: Henkilo.java
class Henkilo {
    private String etunimi;
    private String sukunimi;

    public Henkilo(String etunimi, String sukunimi) {
        this.etunimi = etunimi;
        this.sukunimi = sukunimi;
    }

    public String annaNimi() {
        return etunimi + " " + sukunimi;
    }

    public void asetaEtunimi(String etunimi) {
        this.etunimi = etunimi;
    }

    public void asetaSukunimi(String sukunimi) {
        this.sukunimi = sukunimi;
    }
}
// FILE_END
// FILE: main.java
void main() {
    // Voimme luoda viitemuuttujan ilman että se viittaa mihinkään 
    // olioon. Oliota ei tässä luoda.
    Henkilo h0;

    // Tässä luodaan olio ja sijoitetaan sen viite h0-muuttujaan. 
    // Kääntäjä valitsee käytettäväksi parametrittoman muodostajan, 
    // sillä muodostajalle ei anneta argumentteja.
    h0 = new Henkilo("Mikko", "Mäkinen");

    // Tässä luodaan olio, mutta viitettä ei sijoiteta mihinkään. 
    // Emme pääse tähän olioon enää käsiksi ja se merkitään tuhottavaksi.
    new Henkilo("Mikko", "Mäkinen");

    // Yleensä on suoraviivaisempaa esitellä viitemuuttuja ja 
    // luoda siihen sijoitettava olio yhdessä.
    Henkilo h1 = new Henkilo("Mikko", "Mäkinen");
    IO.println("h1: " + h1.annaNimi());

    // Voimme käyttää parametrillista muodostajaa antamalla muodostajalle 
    // parametreja vastaavat arvot.
    Henkilo h2 = new Henkilo("Anna", "Korhonen");
    IO.println("h2: " + h2.annaNimi());

    // Viitemuuttujat voivat osoittaa samaan olioon. Oliota ei kopioida.
    Henkilo h3 = h2;
    IO.println("h3: " + h3.annaNimi());
}
// FILE_END
```

Pääohjelmassa luodaan nyt olio eri muodostajia käyttäen ja katsotaan samalla
viitteiden toimintaa.

Kun olemme luoneet olioita, voimme tarkastella ja muokata niiden tilaa ohjelman
suorituksen aikana.

```java
// FILE: main.java
void main() {
    Henkilo h1 = new Henkilo("Joni", "Mäkinen");
    IO.println(h1.annaNimi());
    h1.asetaSukunimi("Korhonen");
    IO.println(h1.annaNimi());
}
// FILE_END
// FILE: Henkilo.java
class Henkilo {
    private String etunimi;
    private String sukunimi;

    public Henkilo(String etunimi, String sukunimi) {
        this.etunimi = etunimi;
        this.sukunimi = sukunimi;
    }

    public String annaNimi() {
        return etunimi + " " + sukunimi;
    }

    public void asetaEtunimi(String etunimi) {
        this.etunimi = etunimi;
    }

    public void asetaSukunimi(String sukunimi) {
        this.sukunimi = sukunimi;
    }
}
// FILE_END
```

Tarkastellaan lopuksi olioiden elinkaaren loppua, eli niiden tuhoutumista. Kun
olioon ei enää ole yhtään viitettä, se merkitään "roskaksi", jonka Javan
automaattinen roskienkeräys (engl. *garbage collection*) voi aikanaan poistaa
muistista vapauttaen sitä varten varten varatun tilan.

```java
// FILE: main.java
void main() {
    // Luomme taas kaksi oliota.
    Henkilo h1 = new Henkilo("Joni", "Mäkinen");
    Henkilo h2 = new Henkilo("Anna", "Korhonen");

    // Muuttuja h1 on tällä hetkellä ainoa viite ensimmäiseen olioon.
    // Jos sijoitamme h1-muuttujaan jonkin muun viitten tai asetamme sen arvoksi
    // null, olio merkitään tuhottavaksi, sillä siihen ei ole enää viitteitä.
    h1 = null;

    // Aliohjelman päättyessä kaikki sen sisällä luodut lokaalit 
    // muuttujat (h1 ja h2) tuhoutuvat. Tässä tapauksessa olioihin ei ole 
    // enää muita viitteitä, joten nekin tuhoutuvat.
}
// FILE_END
// FILE: Henkilo.java
class Henkilo {
    private String etunimi;
    private String sukunimi;

    public Henkilo(String etunimi, String sukunimi) {
        this.etunimi = etunimi;
        this.sukunimi = sukunimi;
    }

    public String annaNimi() {
        return etunimi + " " + sukunimi;
    }

    public void asetaEtunimi(String etunimi) {
        this.etunimi = etunimi;
    }

    public void asetaSukunimi(String sukunimi) {
        this.sukunimi = sukunimi;
    }
}
// FILE_END
```

Emme tällä kurssilla perehdy kovin syvällisesti Javan automaattiseen
roskienkeräykseen tai muistin hallintaan. Tämän kurssin kannalta riittää, että
tiedämme milloin olio muuttuu roskaksi ja tuhoutuu. Jos haluat tutustua
aiheeseen hieman tarkemmin, voit aloittaa lukemalla täältä
[täältä](https://www.geeksforgeeks.org/java/jvm-heap-area/) lisää kekomuistista
ja sen varaamisesta sekä
[täältä](https://www.geeksforgeeks.org/java/garbage-collection-in-java/) Javan
roskienkeräyksestä suhteellisen helposti lähestyttävässä muodossa.

## Tehtävät

<task>
  <task-title>Tehtävä 2.4: Luokkia ja olioita, osa 2<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-4-luokkia-ja-olioita2/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava4">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 2.5: Kirjasto<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-5-kirjasto/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava5">Tee tehtävä TIMissä</a></task-link>
</task>