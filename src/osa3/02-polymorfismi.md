# Polymorfismi

> [!Osaamistavoitteet]
>
> - Polymorfismi (dynaaminen sidonta, rajapinnat ja abstraktit luokat voivat olla muuttujan tai parametrin tyyppeinä)
> - Tunnistaa polymorfismin merkitys olioiden yhteistyössä. Olio, joka käyttää ylätason tyyppiä (rajapinta, abstrakti luokka) voi toimia erilaisten aliluokkien kanssa.
> - Kutsuttava metodi päätetään ajon aikana olion todellisen tyypin perusteella, ei muuttujan tyypin perusteella.
> - Osaat hyödyntää rajapintoja ja abstrakteja luokkia luokkienvälisen riippuvuuden välttämiseksi 

![Bändi](images/band.png)

Kuvitellaan tilanne, jossa ohjelmassa on erilaisia soittimia: `Kitara`, `Piano` ja `Rumpusetti`. Haluamme, että soittimia voi soittaa. Yksi mahdollisuus olisi kirjoittaa jokaiselle soittimelle oma metodi soittamista varten, kuten:

```java,noplayground
Kitara kitara = new Kitara();
kitara.soitaKitaraa();
Piano piano = new Piano();
piano.soitaPianoa();
Rumpusetti rumpusetti = new Rumpusetti();
rumpusetti.soitaRumpuja();
```

Jos tavoitteena on kuitenkin vain saada soitin soimaan, tämä lähestymistapa ei ole laajennettavissa: jokaisen uuden soittimen lisääminen vaatisi muutoksia moniin paikkoihin.

Sen sijaan usein haluamme pystyä käsittelemään soittimia (ja olioita yleisemminkin) yhtenäisenä joukkona ja kutsumaan vain yhtä metodia – kuten `soita()` – oli kyseessä mikä soitin tahansa. Tätä varten tarvitsemme polymorfismia.

*Polymorfismi* viittaa olio-ohjelmoinnissa kykyyn käsitellä erilaisia olioita yhtenäisellä tavalla. Kun metodia kutsutaan, päätös siitä, mikä metodi tosiasiallisesti suoritetaan, tehdään ajon aikana olion todellisen tyypin perusteella. Polymorfismi mahdollistaa joustavan koodin kirjoittamisen, jossa uusia olioita voidaan lisätä ilman, että olemassa olevaa koodia tarvitsee muuttaa.



Polymorfismi jaetaan yleensä kahteen päätyyppiin: (1) käännösaikaiseen polymorfismiin, jota kutsutaan myös *dynaamiseksi sidonnaksi* (engl. *dynamic binding*) ja (2) ajon aikaiseen polymorfismiin. Käännösaikaisella polymorfismilla tarkoitetaan Javassa aliohjelman kuormitusta (engl. *method overloading*). Asiaa on käsitelty Ohjelmointi 1 -kurssilla, emmekä sitä tässä käsittele tarkemmin, mutta lyhyesti: aliohjelman kuormitus tarkoittaa sitä, että aliohjelmalla voi olla useita samannimisiä toteutuksia, jotka eroavat toisistaan parametrien lukumäärän, parametrien tyyppien tai aliohjelman paluuarvon perusteella. Lue lisää Ohjelmointi 1 -kurssin materiaalista. (TODO: Linkki)

## is-a-suhde

Perintäsuhteesta käytetään englanninkielistä termiä *is-a*-suhde. Voimmekin sanoa, että `Opiskelija` *on* `Henkilo`, `Opettaja` *on* `Henkilo` ja `Sihteeri` *on* `Henkilo` -- nimen omaan näin päin. Edelleen, myös `TutkintoOpiskelija` *on* `Henkilo`, koska se perii `Opiskelija`-luokan, joka puolestaan perii `Henkilo`-luokan. 

Polymorfismin ansiosta voimme käsitellä `Opiskelija`, `Opettaja` ja `Sihteeri`-olioita koodissamme `Henkilo`-luokan olioina, kun ei ole tarpeen tietää tarkasti, minkä aliluokan olioita käsittelemme. Tämä on hyödyllistä esimerkiksi silloin, kun haluamme käsitellä henkilöitä yhtenä ryhmänä. 

Lisätään kaikki tekemämme oliot `Henkilo`-taulukkoon:

```java,noplayground
Opiskelija opiskelija = new Opiskelija();
Opettaja opettaja = new Opettaja();
Sihteeri sihteeri = new Sihteeri();

Henkilo[] henkilot = {opiskelija, opettaja, sihteeri};
```

Jotta esimerkkimme olisi vähän mielekkäämpi, lisätään vielä `Henkilo`-luokkaan metodit `kirjaudu()` ja `kirjauduUlos()`. Nyt siis kaikki henkilöt perivät nämä metodit.

```java,noplayground
class Henkilo {
    // HIGHLIGHT_GREEN_BEGIN
    private boolean kirjautunut;
    // HIGHLIGHT_GREEN_END

    public Henkilo(String nimi) {
        // ...
        // HIGHLIGHT_GREEN_BEGIN
        this.kirjautunut = false;
        // HIGHLIGHT_GREEN_END
        // ..
    }

    // HIGHLIGHT_GREEN_BEGIN
    void kirjaudu() {
        this.kirjautunut = true;
        IO.println(this.getNimi() + " kirjautui sisään.");
    }
    void kirjauduUlos() {
        this.kirjautunut = false;
        IO.println(this.getNimi() + " kirjautui ulos.");
    }
    // HIGHLIGHT_GREEN_END
}
```

Voimme nyt kutsua vaikkapa `kirjauduUlos()`-metodia kaikille `henkilot`-taulukon olioille ilman, että meidän tarvitsee tietää tarkasti, minkä tyyppisiä olioita taulukossa on:

```java,noplayground
for (Henkilo henkilo : henkilot) {
    henkilo.kirjauduUlos();
}
```

Huomionarvoista on *is-a*-suhteen suunta; `Opettaja` ei ole `Sihteeri`, vaikkakin molemmat perivät `Henkilo`-luokan. 

## Korvaaminen ja polymorfismi

Edellisessä esimerkissä kaikki aliluokan edustajat perivät yliluokan metodit sellaisenaan, jolloin niitä ei tarvitse määritellä uudelleen aliluokassa. Perityn luokan metodeja voidaan kuitenkin myös *korvata* (engl. *override*) aliluokassa, mikä tarkoittaa, että aliluokka voi määritellä oman version peritystä metodista. Juuri tämä mahdollistaa polymorfismin, ja sen, että voimme muuttaa perityn metodin käyttäytymistä aliluokassa. 

## Esimerkki 1

Lisätään yllä olevaan `Opiskelija`-esimerkkimme attribuutti `boolean opintoOikeusVoimassa`, joka ilmaisee, onko opiskelijalla voimassa oleva opinto-oikeus. Jos opinto-oikeus ei ole voimassa, opiskelija ei voi kirjautua järjestelmään. Korvataan `kirjaudu()`-metodi `Opiskelija`-luokassa tarkistamaan tämä ehto ennen kirjautumista.

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

Muissa `Henkilo`-luokan aliluokissa, kuten `Opettaja` ja `Sihteeri`, `kirjaudu()`-metodi toimii edelleen alkuperäisellä tavalla, koska niitä ei ole korvattu.

Metodin korvaamiseen liittyy pari sääntöä: 

 * Korvaaminen koskee aina hierarkiassa *lähintä* yliluokan metodia. 
 * Kun aliluokan olion metodia kutsutaan, kutsu viittaa aina hierarkiassa lähimpään korvattuun versioon.

Alla oleva koodi havainnollistaa korvaamista ja kutsujen välittymistä luokkahierarkiassa.

```java
// FILE: main.java
public class KokeillaanKorvaamista {  
  public static void main(String args[]) {  
    C c = new C();  
    c.hei();    // Kutsuu A-luokan hei()-metodia
    c.moikka(); // Kutsuu B-luokan moikka()-metodia
    c.huhhuh(); // Kutsuu C-luokan huhhuh()-metodia
  }  
}  
// FILE_END
// FILE: A.java
class A {  
    public void hei() { IO.println("A-olio sanoo hei."); }  
    public void moikka() { IO.println("A-olio sanoo moikka."); }  
    public void huhhuh() { IO.println("A-olio sanoo huh huh!!."); }  
}  
// FILE_END
// FILE: B.java
class B extends A {  
    public void moikka() { IO.println("B-olio huutaa moikka!"); }  
    public void huhhuh() { IO.println("B-olio huutaa huh huh!!"); }  
}  
// FILE_END
// FILE: C.java
class C extends B {  
    public void huhhuh() { IO.println("C-olio huhuilee...."); }  
}  
// FILE_END
```

## Esimerkki 2

Tarkastellaan `Muoto`-luokkaa, jolla on metodi `laskeAla()`. 

```java
public class Muoto {
    public double laskeAla() {
        return 0.0;
    }
}
```

Huomaamme, että `laskeAla()`-metodin toteutus on vähän hassu. Tämä johtuu siitä, että ei ole oikeastaan mitään ns. yleistä muotoa, vaan `Muoto`-luokan edustajan tulee aina olla jokin konkreettinen muoto, kuten suorakulmio tai ympyrä, joilla on omat tavat laskea pinta-ala. Palaamme tähän dilemmaan osassa [3.3 Abstraktit luokat](03-abstraktit-luokat.md).

Tehdään nyt aliluokat `Suorakulmio` ja `Ympyra`. Koska näiden muotojen pinta-alat ovat luonnollisesti keskenään erilaisia, tulee kummallakin olla oma toteutus `laskeAla()`-metodille.

```java,ignore
// FILE: Suorakulmio.java
public class Suorakulmio extends Muoto {
    private double leveys;
    private double korkeus;

    public Suorakulmio(double leveys, double korkeus) {
        this.leveys = leveys;
        this.korkeus = korkeus;
    }

    @Override
    public double laskeAla() {
        return leveys * korkeus;
    }
}
// FILE_END
// FILE: Ympyra.java
public class Ympyra extends Muoto {
    private double sade;

    public Ympyra(double sade) {
        this.sade = sade;
    }

    @Override
    public double laskeAla() {
        return Math.PI * sade * sade;
    }
}
// FILE_END
```

Nyt voimme kirjoittaa koodia, joka käsittelee `Muoto`-olioita ilman, että tarvitsee tietää, onko kyseessä `Suorakulmio` vai `Ympyra`. 

```java
// FILE: main.java
public class Main {
    public static void main()
    {
        Muoto muoto1 = new Ympyra(5);
        Muoto muoto2 = new Suorakulmio(5, 7);

        IO.println(muoto1.laskeAla());
        IO.println(muoto2.laskeAla());
    }
}
// FILE_END
// FILE: Muoto.java
public class Muoto {
    public double laskeAla() {
        return 0.0;
    }
}
// FILE_END
// FILE: Suorakulmio.java
public class Suorakulmio extends Muoto {
    private double leveys;
    private double korkeus;

    public Suorakulmio(double leveys, double korkeus) {
        this.leveys = leveys;
        this.korkeus = korkeus;
    }

    @Override
    public double laskeAla() {
        return leveys * korkeus;
    }
}
// FILE_END
// FILE: Ympyra.java
public class Ympyra extends Muoto {
    private double sade;

    public Ympyra(double sade) {
        this.sade = sade;
    }

    @Override
    public double laskeAla() {
        return Math.PI * sade * sade;
    }
}
// FILE_END
```

## Miksi polymorfismia tarvitaan?

Polymorfismi mahdollistaa monin tavoin joustavan ja laajennettavan koodin kirjoittamisen. Olio-ohjelmoinnissa polymorfismia tarvitaan erityisesti siksi, että sen avulla voimme tarjota yhtenäisen tavan käsitellä keskenään hyvinkin erilaisia olioita.

Kun useat luokat perivät saman yliluokan (tai toteuttavat saman rajapinnan; paneudumme rajapintoihin luvussa [3.3 Rajapinnat]()), ne voidaan käsitellä yhden yhteisen tyypin kautta. Tämä mahdollistaa sen, että ohjelma voi käsitellä joukkoa erilaisia olioita kuten:

 * kaikkia soittimia (`Soitin`), kuten kitarat, pianot ja rummut
 * kaikkia ajoneuvoja (`Ajoneuvo`), vaikka ne olisivatkin erilaisia, kuten autoja, polkupyöriä ja lentokoneita
 * kaikkia eläimiä (`Elain`), kuten koiria, kissoja ja lintuja
 * kaikkia graafiseen käyttöliittymään piirrettäviä komponentteja (`Piirrettava`), kuten painikkeita, tekstikenttiä ja kuvia
 * kaikkia maksutapoja (`Maksutapa`), kuten luottokortti, PayPal ja käteinen

## Huomautus instanceof-operaattorista

TODO: Samilla oli tähän oma branch. Alla oleva teksti on vanhaa, ja poistunee sellaisenaan. 

Javassa on mahdollista tarkistaa, onko olio tietyn luokan ilmentymä käyttämällä `instanceof`-operaattoria. Esimerkiksi:

On kuitenkin niin, että `instanceof`-operaattorin käyttö tarkoittaa varsin usein sitä, ettei perintää ja polymorfismia ole hyödynnetty optimaalisella tavalla, jonka seurauksena koodiin tulee runsaasti ehtolauseita, jotka tarkistavat olion tyypin ja suorittavat sen perusteella erilaisia toimintoja. Tällöin menetetään olio-ohjelmoinnin keskeinen etu, eli se, että olioiden erilaiset toteutukset voidaan piilottaa niiden käyttäjiltä. Käytännössä ainoa, missä kyseistä operaattoria tarvitsee, on, jos käsitellään `Object`-olioita jonkin hyvin matalan tason yleisluokan kautta. 

## Tehtävät

<task>
  <task-title>Tehtävä 3.4: Korvaaminen, osa 1. <points>1 p.</points> </task-title>
  <handout>

  {{#include ../exercises/3-4-korvaaminen/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa3/tehtava4">Tee tehtävä TIMissä</a></task-link>
</task>

.
