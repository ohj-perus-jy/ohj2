# Luokka ja olio

> [!Osaamistavoitteet]
>
> - Ymmärrät luokan ja olion suhteen, ja miten luokka toimii mallina olioiden luomisessa.
> - Osaat määritellä oman luokan ja sen jäsenet, eli attribuutit, metodit ja konstruktorit.
> - Ymmärrät olioiden elinkaaren ja osaat käyttää olioita ohjelman osina.
> - Ymmärrät, miten `this`-viite toimii olion metodeissa.
> - Tiedät, mitä `static`-määrite merkitsee luokan jäsenten osalta.

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
> Viitemuuttuja ja olio ovat kaksi eri asiaa. Viitemuuttuja on kuin nuoli, joka
> voi osoittaa olioon. Viitemuuttujan ei kuitenkaan ole pakko viitata mihinkään,
> jolloin sen arvo on `null`. Olio on vastaavasti mahdollista luoda ilman siihen
> viittaavaa muuttujaa, mutta jos olioon osoittavia viitteitä ei ole, siihen ei
> päästä käsiksi ja se merkitään automaattisesti roskaksi. Useampi viitemuuttuja
> voi viitata samaan olioon, mutta viitemuuttuja voi osoittaa vain yhteen olioon
> kerrallaan. 

## Attribuutit

Attribuutti on luokan sisällä, aliohjelmien ulkopuolella määritelty muuttuja,
joka edustaa olion ominaisuutta, piirrettä tai tilaa. Luokasta tehdyt oliot
sisältävät aina luokassa määritellyt attribuutit. Siinä missä luokka
määrittelee, mitä tietoja olioilla voi olla, attribuutit tallentavat kunkin
yksittäisen olion konkreettiset arvot. Kuten muuttujat yleensä, attribuutit
voivat olla alkeistietotyyppejä tai viitteitä. Niiden nimeämisessä käytetään
myös samoja käytänteitä. Huomaa, että metodien sisällä esitellyt muuttujat eivät
ole attribuutteja; ne ovat metodin *paikallisia* eli *lokaaleja* muuttujia.
Lokaalit muuttujat eivät ole osa olion tilaa.

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

Attribuutit poikkeavat paikallisista muuttujista siten, että niiden näkyvyyttä
voidaan hallita näkyvyysmääreiden avulla. Paikalliset muuttujat ovat olemassa ja
nähtävillä vain aliohjelman sisällä sen suorituksen ajan, mutta attribuutit ovat
olemassa koko olion eliniän ajan ja näkyvät kaikille muille jäsenille luokan
sisällä. Ne *voidaan* asettaa näkyväksi myös olion ulkopuolelta, joskin tämä on
yleisesti ottaen huono idea. Palaamme näkyvyysmääreisiin myöhemmin tässä osassa.

> [!HUOMAUTUS]
> Paikallisella muuttujalla voi olla sama nimi kuin attribuutilla, jolloin se
> peittää attribuutin. Tätä kutsutaan varjostamiseksi (engl. *shadowing*). Jos
> attribuutilla ja paikallisella muuttujalla on sama nimi, käytetään
> lausekkeissa ensisijaisesti lokaalia muuttujaa. Tässäkin tilanteessa olion
> metodeista voi yhä päästä käsiksi sen attribuuttiin käyttämällä
> `this`-viitettä, johon palaamme hyvin pian.

Attribuutille voidaan luokassa antaa oletusarvo, jolloin luokasta luodut oliot
saavat sen myös oman attribuuttinsa alkuarvoksi. Jos attribuutilla ei ole
oletusarvoa, sen arvo voidaan määrittää olion luomisen yhteydessä, myöhemmin
metodien avulla, tai jopa jättää määrittämättä.

```java,ignore
public class Rakennus {
    // Olion attribuutti, jolla on oletusarvo.
    private String väri = "sininen";

    public void tulosta() {
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
että kaikki aliohjelmat ovat itse asiassa aina *jonkin* luokan sisällä. Ehkä
tästä syystä Java-kielessä tupataan kutsumaan kaikkia aliohjelmia metodeiksi.

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
hieman järkevämmin, mutta tässä vaiheessa tällaiset yksinkertaiset `get`- ja
`set`-metodit riittävät.

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
muuttaa. Viitteen kautta metodi pääsee käsiksi oikean olion tilaan sekä
metodeihin. Olion metodien sisällä `this`-viite on pakko kirjoittaa vain, jos
näkyvyysalueella on samanniminen jäsen, kuten lokaali muuttuja. Meidän ei siis
tarvitse kirjoittaa aina attribuutin tai metodikutsun eteen `this`, sillä
kääntäjä osaa päätellä sen itse, jos konfliktia ei ole. Joissain
ohjelmointikielissä tällaista viitettä kutsutaan myös nimellä `self`.

Katsotaan muutama esimerkki `this`-viitteen käytöstä.

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

Lisätään nyt `Rakennus`-luokalle muodostaja, joka ottaa omistajan ja värin
vastaan parametreina ja alustaa näiden avulla olion attribuutit. Näin meidän ei
tarvitse asettaa attribuutteja erikseen olion luomisen jälkeen pääohjelmassa.
Voimme nyt myös poistaa parametrittoman muodostajan, jotta sitä ei voi enää
käyttää luomaan olioita, joilla on virheellinen alkutila.

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
// FILE_END
```

Pari huomiota: Emme voi luoda rakennusta yhdellä parametrilla, esimerkiksi
`Rakennus rakennus2 = new Rakennus("JYU");`, sillä määrittelemämme muodostaja
tarvitsee kaksi parametria. Emme voi myöskään luoda rakennusta ilman
parametreja, esimerkiksi `Rakennus rakennus3 = new Rakennus();`, koska
oletusmuodostajaa ei enää ole. 

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
  <task-title>Tehtävä 2.1: Kello<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-1-kello/handout.md}}
  
  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava1">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 2.2: Ajastin<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-2-ajastin/handout.md}}
  
  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava2">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 2.3: Oma luokka<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-3-oma-luokka/handout.md}}
  
  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava3">Tee tehtävä TIMissä</a></task-link>
</task>


## Static

Luokan jäsenet voidaan määritellä kuuluvaksi olion sijaan **luokalle**
`static`-määritettä käyttämällä. Tällaisia attribuutteja ja metodeja kutsutaan
luokan attribuuteiksi (engl. *class attribute*) ja luokan metodeiksi (engl.
*class method*). 

Sana `static` voi olla hieman harhaanjohtava; *staattisuus* ei tässä tarkoita,
että nämä luokan jäsenet ovat pysyviä tai muuttumattomia. Käytämme kuitenkin
tässä materiaalissa sanaa staattinen kuvaamaan luokan jäseniä. 

Siinä missä attribuutit ja metodit liittyvät olioon -- olion attribuutit ja
metodit pääsevät olion tilaan käsiksi -- luokan attribuutti ei ole osa minkään
olion tilaa ja sillä on vain yksi arvo, joka on jaettu kaikkien luokan olioiden
kesken. Jos yksi olio muuttaa oman luokkansa attribuutin arvoa, muutos näkyy
kaikissa saman luokan olioissa. 

Samalla tavalla voimme ajatella myös luokan metodien olevan jaettu kaikkien
luokan olioiden kesken; ne eivät liity mihinkään olioon, eivätkä siten pääse
minkään olion tilaan suoraan käsiksi. Oliot voivat kutsua oman luokkansa
metodia, siis staattista metodia, mutta tämä kutsu ei mahdollista olion tilan
käsittelyä. Koska staattiset metodit eivät liity mihinkään olioon, niiden
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
kutsua tätä metodia *staattisesti* luokan kautta, esimerkiksi
`Henkilo.annaNimi()`.

Lisätään nyt *luokan* attribuutti `taysiIkaisyydenRaja`, joka kuvastaa kaikkien
henkilöiden täysi-ikäisyyden rajaa. Lisätään luokkaan myös metodi
`onkoTaysiIkainen`, joka tarkistaa, onko annettu ikä täysi-ikäinen. Huomaa, että
kyseinen metodi ei liity mihinkään olioon, vaan se tarkistaa vain annetun iän. 

```java
// FILE: Henkilo.java
public class Henkilo {
    private String etunimi;
    private String sukunimi;
    private static int taysiIkaisyydenRaja = 18;

    public Henkilo(String etunimi, String sukunimi) {
        this.etunimi = etunimi;
        this.sukunimi = sukunimi;
    }

    public String annaNimi() {
        return etunimi + " " + sukunimi;
    }

    public static boolean onkoTaysiIkainen(int ika) {
        return ika >= taysiIkaisyydenRaja;
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
    IO.println(Henkilo.onkoTaysiIkainen(20)); // Tulostaa 'true'
    IO.println(Henkilo.onkoTaysiIkainen(15)); // Tulostaa 'false'

    // Staattista metodia voi kutsua myös olion kautta, mutta selkeyden vuoksi 
    // on parempi käyttää luokkaa.
    // IO.println(h1.onkoTaysiIkainen(20)); // Tämä toimii, mutta ei ole suositeltavaa.
}
// FILE_END
```

Nyt meillä on *luokan* metodi `onkoTaysiIkainen`, jota voimme kutsua ilman oliota.
Voisimme kutsua tätä luokan metodia myös olion kautta, mutta se ei ole tarpeen
ja kääntäjä varoittaakin siitä.

Staattinen jäsen on hyödyllinen, kun haluamme määritellä jonkin toiminnallisuuden,
joka ei liity mihinkään yksittäiseen olioon, mutta liittyy luokkaan yleisesti.

Staattiseen jäseneen pääsee käsiksi myös olion metodin sisältä. Voimme
esimerkiksi tarkistaa, onko henkilö täysi-ikäinen.

```java,ignore
// Olion metodi voi myös käyttää staattista muuttujaa
public boolean onkoHenkiloItseTaysiIkainen() {
    return this.ika >= taysiIkaisyydenRaja;
}
```

Selkeyden vuoksi on hyvä käyttää luokan nimeä, kun viitataan staattiseen jäseneen
luokan sisälläkin, esimerkiksi `Henkilo.taysiIkaisyydenRaja`. Tämä auttaa erottamaan
staattiset jäsenet olion jäsenistä.

Yllä oleva esimerkki on sikäli varoittava, että täysi-ikäisyyden rajaa pystyy
muuttamaan mistä tahansa koodista, joka pääsee käsiksi `Henkilo`-luokkaan.
Tällaisen "globaalin" tilan käyttäminen koodissa on yleensä erittäin huono idea. 

Yksi esimerkki staattisesta metodista, jota käytämme usein, on `IO.println()`.
Tämä on
[IO-luokan](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/io/IO.html)
staattinen metodi. Sen käyttäminen on helpompaa, kun meidän ei tarvitse joka
kerta luoda IO-oliota ja kutsua sen `println`-metodia.

<task>
  <task-title>Tehtävä 2.4: Static<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-4-static/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava4">Tee tehtävä TIMissä</a></task-link>
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
  <task-title>Tehtävä 2.5: Puhelin<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-5-puhelin/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava5">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 2.6: Kirjasto<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/2-6-kirjasto/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa2/tehtava6">Tee tehtävä TIMissä</a></task-link>
</task>
