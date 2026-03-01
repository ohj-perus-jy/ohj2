# Tyyppiparametrit ja geneerisyys

> [!Osaamistavoitteet]
>
> - Osaat hyödyntää tyyppiparametreja toteuttaaksesi yleiskäyttöisiä eli
>   geneerisiä luokkia ja metodeja

Olet oppinut aiemmissa ohjelmointiopinnoissasi, että parametrit mahdollistavat
toiston vähentämisen yleistämällä ohjelman toimintaa erilaisille arvoille.
Parametrien idea on erottaa laskennan logiikka itse arvoista. Kun kirjoitamme
metodin, laskenta määritellään vain kerran. Esimerkiksi, jos haluaisimme *ilman
parametreja* selvittää, missä indeksissä etsimämme luku ilmaantuu ensimmäistä
kertaa, voisimme kirjoittaa koodin näin.

```java
//-void main() {
int[] taulukko1 = {2, 3, 4};
// Etsitään luku 3
for (int i = 0; i < taulukko1.length; i++) {
    if (taulukko1[i] == 3) {
        IO.println("Luku 3 on ekan kerran indeksissä " + i);
        break;
    }
}

int[] taulukko2 = {-20, 10, 2, 1};
// Etsitään luku 2
for (int i = 0; i < taulukko2.length; i++) {
    if (taulukko2[i] == 2) {
        IO.println("Luku 2 on ekan kerran indeksissä " + i);
        break;
    }
}
//-}
```

Tämä toimii, mutta koodia on kopioitu turhaan. Tehdään nyt funktio, joka ottaa
taulukon *parametrina*.

```java
int etsiIndeksi(int[] taulukko, int etsittava) {
    for (int i = 0; i < taulukko.length; i++)
        if (taulukko[i] == etsittava) return i;
    return -1;
}

void main() {
    IO.println("Luku 3 on indeksissä " + etsiIndeksi(new int[] {2, 3, 4}, 3));
    IO.println("Luku 2 on indeksissä " + etsiIndeksi(new int[] {-20, 10, 2, 1}, 2));
}
```

Tätä voi ajatella parametrien käyttönä arvojen tasolla: metodi on yleinen, mutta
sille annettavat arvot vaihtelevat.

Huomaamme kuitenkin nopeasti, että sama `etsiIndeksi`-funktio ei kuitenkaan
toimi muille lukutyypeille, kuten `long` tai `float`, eikä myöskään kokonaan
muunlaisille tyypeille, kuten `String`. Näitä varten täytyisi tehdä erilliset
funktiot.

```java
int etsiIndeksiLong(long[] taulukko, long etsittava) {
    for (int i = 0; i < taulukko.length; i++)
        if (taulukko[i] == etsittava) return i;
    return -1;
}

int etsiIndeksiFloat(float[] taulukko, float etsittava) {
    for (int i = 0; i < taulukko.length; i++)
        if (taulukko[i] == etsittava) return i;
    return -1;
}

int etsiIndeksiString(String[] taulukko, String etsittava) {
    for (int i = 0; i < taulukko.length; i++)
        if (taulukko[i].equals(etsittava)) return i;
    return -1;
}

void main() {
    long[] longTaulukko = {-10L, 5L, 1L};
    float[] floatTaulukko = {-10.0f, 2.0f};
    String[] stringTaulukko = {"Koira", "Kissa", "Lintu"};
    IO.println("Luku -10 on indeksissä " + etsiIndeksiLong(longTaulukko, -10L));
    IO.println("Luku 2.0 on indeksissä " + etsiIndeksiFloat(floatTaulukko, 2.0f));
    IO.println("Merkkijono \"Kissa\" on indeksissä " + etsiIndeksiString(stringTaulukko, "Kissa"));
}
```
Koska Java on staattisesti tyypitetty kieli, emme voi kirjoittaa yhtä ja samaa
metodia, joka toimisi automaattisesti kaikille näille. Ilman tällaista ratkaisua
päätyisimme helposti tilanteeseen, jossa meillä on joukko lähes identtisiä
metodeja: `etsiIndeksiInt`, `etsiIndeksiDouble`, `etsiIndeksiString` ja niin
edelleen. Koodi on käytännössä sama, vain tyypit vaihtuvat. 

Oikeastaan `etsiIndeksi`-funktion perusajatus on aina sama:

```java,ignore
int etsiIndeksi(TYYPPI[] taulukko, TYYPPI etsittava) {
    for (int i = 0; i < taulukko.length; i++)
        if (taulukko[i] == etsittava) return i;
    return -1;
}
```

Javassa tämän tapaisen koodin kirjoittaminen on mahdollista *tyyppiparametrien*
avulla.

## Tyyppiparametrit 

Tyyppiparametri on parametri, jonka arvona on tietotyyppi. Tyyppiparametrin
tarkoitus on vähentää toistoa tapauksissa, jossa sama koodi toimii eri
tyyppisille arvoille luopumatta staattisen tyypityksen antamista hyödyistä.
Lisäksi tyyppiparametrit mahdollistavat ylimääräisten tyyppimuunnosten
välttämistä jossain tapauksissa.

Tyypiparametri tai -parametrit voidaan määrittää metodille tavallisten
parametrien lisäksi. Erikoisuutena on, että tyyppiparametreja voidaan myös
määrittää luokille. Yhdessä metodien ja luokkien tyyppiparametrit
mahdollistavat *geneeristä ohjelmointia*, eli tyypistä riippumattomien
algoritmien ja tietorakenteiden ohjelmointia. 

## Geneerinen metodi

Metodia, joka määrittelee tyyppiparametrin, kutsutaan *geneeriseksi metodiksi*.
Geneerisessä metodissa tietotyyppiä ei ole lukittu metodia määriteltäessä
tiettyyn tyyppiin etukäteen, vaan tyyppi ilmaistaan symbolilla, joka
täsmennetään vasta metodia kutsuttaessa. Metodin tyyppiparametri laitetaan
kulmasulkeiden väliin ennen metodin palautustyyppiä. Yleinen käytäntö on käyttää
yksikirjaimisia, isoja kirjaimia. Tavallisin näistä on `T`, joka tulee sanasta
Type.

```java
// aliohjelma "tulosta", jolla on yksi tyyppiparametri T 
// ja yksi tavallinen parametri "arvo"
<T> void tulosta(T arvo) {
    IO.println("Moikka, olen '" + arvo + "' ja olen luokan '" + arvo.getClass() + "' olio!");
}

void main() {
    tulosta(1.0);
    tulosta(1);
    tulosta("kissa");
}
```

Geneerinen metodi voi olla staattinen, ei-staattinen tai konstruktori.
Tyyppiparametri voi esiintyä metodin palautustyypissä, parametreissa tai
molemmissa.

Tyyppiparametreja voi olla yksi tai useampia. Ne määritellään pilkulla
eroteltuina kulmasulkeiden sisällä, ja jokainen niistä voi edustaa toisistaan
riippumatonta tyyppiä. Esimerkiksi alla olevassa metodissa on kaksi
tyyppiparametria, `T1` ja `T2`, jotka voivat edustaa mitä tahansa kahta
erilaista tietotyyppiä.

```java
<T1, T2> String yhdista(T1 arvo1, T2 arvo2) {
    return arvo1.toString() + ", " + arvo2.toString();
}

void main() {
    IO.println(yhdista(1, 2)); // T1 = Integer, T2 = Integer
    IO.println(yhdista(true, 1.0)); // T1 = Boolean, T2 = Double
}
```

Tyyppiparametrien nimeämisen osalta yleistynyt käytäntö tällä hetkellä lienee,
että nimi on yleensä yksi suuraakkonen, joka on johdettu tyyppiparametrin
merkityksestä, kuten `T` (**T**ype), `E` (**E**lement), `K` (**K**ey), `N`
(**N**umber), `V` (**V**alue). Jossain tapauksissa tyyppiparametrien nimeen
lisätään myös numero, kuten `T1`, `T2`, `T3`, jne.

Huomaa, että yllä olevissa esimerkeissä tyyppiparametri määritellään, mutta
tyyppiparametreille ei anneta arvoa kutsuttaessa. Tämä voitaisiin kyllä tehdä;
esimerkiksi yllä oleva `tulosta`-aliohjelman kutsulle voidaan määrittää
tarkasti tyyppiparametrin tyyppi.

```java
//-<T> void tulosta(T arvo) {
//-    IO.println("Moikka, olen '" + arvo + "' ja olen luokan '" + arvo.getClass() + "' olio!");
//-}
//-
void main() {
    this.<Double>tulosta(1.0); // sama kuin tulosta(1.0)
    this.<String>tulosta("kissa"); // tulosta("String")
}
```

Tyyppiparametrin arvoa ei yleensä määritetä kutsussa, sillä kääntäjä osaa
yleensä päätellä tyyppiparametrin arvon automaattisesti. Esimerkiksi
`tulosta(1.0)`-kutsussa lausekkeen `1.0` tyyppi on `double`, joten kääntäjä
päättelee tyyppiparametrin `T` olevan (`Double`). On kuitenkin hyvä pitää
mielessä, että tyypiparametrille kyllä annetaan taustalla arvo, vaikka sitä ei
itse kirjoittaisikaan näkyville. 

Katsotaan, miten aiempi etsimisongelma ratkeaa geneerisen metodin avulla. 

```java
<T> int etsiIndeksi(T[] taulukko, T etsittava) {
    for (int i = 0; i < taulukko.length; i++)
        if (taulukko[i].equals(etsittava)) return i;
    return -1;
}

void main() {
    Integer[] kokonaisluvut = {2, 3, 4};
    Double[] liukuluvut = {-10.0, 2.0, 0.0, 5.5};
    String[] elaimet = {"koira", "kissa", "gepardi", "kissa", "gepardi"};

    IO.println(etsiIndeksi(kokonaisluvut, 3));
    IO.println(etsiIndeksi(liukuluvut, 5.4));
    IO.println(etsiIndeksi(elaimet, "gepardi"));
}
```

Huomaa, että jouduimme tekemään erityisesti pari muutosta:

Ensinnäkin, vertailu tapahtuu nyt kirjoittamalla
`taulukko[i].equals(etsittava)`. Tämä johtuu siitä, että tyyppiparametri `T` voi
edustaa mitä tahansa viitetietotyyppiä, ja viitetietotyyppisten arvojen
vertailua ei voi tehdä `==`-operaattorilla.

Toiseksi, `main`-pääohjelmassa tulee käyttää perustietotyyppien `int`, `double`
ja `long` sijaan käärijäluokkia `Integer`, `Double` ja `Long`. Tämä johtuu
siitä, että Javassa vain viitetietotyyppejä voidaan käyttää tyyppiparametreina.
Rajoite puolestaan johtuu Javan tavasta toteuttaa viitetietotyyppejä.
Mainittakoon, että Java-kieltä kehitetään jatkuvasti, ja on hyvin mahdollista,
että lähitulevaisuudessa tämä rajoite jää pois.

<details><summary><i class="bi bi-stars jyu-gold"></i>Valinnaista lisätietoa: Miksi tyyppiparametrit eivät voi olla perustietotyyppejä?</summary>

Java käyttää mekanismia nimeltä *type erasure*, jonka voisi vapaasti suomentaa
"tyyppien poistamiseksi". Tämä tarkoittaa, että käännettäessä Java-koodi
tavukoodiksi tyyppiparametrit poistetaan ja korvataan niiden ylärajalla.
Ylärajalla tarkoitetaan sitä tyyppiä, jota geneerinen parametri varmasti
edustaa. Jos tyyppiparametrille on asetettu rajoitus, kuten `<T extends
Number>`, yläraja on tällöin `Number`. Käännöksen jälkeen kaikki `T`:hen
viittaava koodi käsitellään ikään kuin tyyppi olisi `Number`. Jos taas
tyyppiparametrille ei ole asetettu rajoitusta, sen yläraja on automaattisesti
`Object`. Esimerkiksi tyyppiparametri `T` käsitellään käännöksen jälkeen ikään
kuin se olisi `Object`.

Käytännössä tämä tarkoittaa, että geneerisyys ei ole Javan ajonaikainen
ominaisuus, vaan käännösaikainen tarkistusmekanismi. Tyyppitiedot poistetaan,
jotta geneerinen koodi olisi yhteensopivaa vanhemman, ei-geneerisen Java-koodin
kanssa.

Koska primitiivityypit eivät peri `Object`-luokkaa, ne eivät voi toimia
tyyppiparametreina. Siksi geneerisissä rakenteissa on aina käytettävä
käärijäluokkia (`Integer`, `Double`, `Boolean`).

Sama rajoitus näkyy myös taulukoiden kanssa: Java ei salli geneeristen
taulukoiden luomista. Esimerkiksi lause new T[10] ei ole sallittu, koska
tyyppiparametri ei ole ajonaikana tiedossa type erasure -mekanismin vuoksi.
Käytännössä tämä tarkoittaa, että geneerisen koodin yhteydessä käytetään lähes
aina kokoelmia (kuten ArrayList<T>) taulukoiden sijaan.
</details>

## Geneerinen luokka ja geneerinen rajapinta

Geneerisyys ei rajoitu vain metodeihin. Tyyppiparametrien todellinen hyöty
tapana tuottaa yleistyvää koodia tulee esiin erityisesti silloin, kun
tyyppiparametreja määritellään luokille tai rajapinnoille. Olemmekin jo
käyttäneet kurssilla tyyppiparametreja valmiissa luokissa, kuten `ArrayList<T>`.
lista itsessään on yleinen, mutta sen sisältämä tyyppi täsmennetään.

> [!TODO]
> DZ: Joku yksinkertainen esimerkki? Vaikkapa Osassa 1 oleva salasanatehtävä,
> mutta se palauttaisi `Tulos(boolean oikein, String virhe)`. Se refaktoroidaan
> luokaksi `Pari<T, U>`.

Geneerinen luokka on erityisen perusteltu silloin, kun luokka säilyttää jonkin
tyyppisiä arvoja ja useat metodit liittyvät samaan tyyppiparametriin.
Esimerkiksi `Pari<T, U>` voisi olla tällainen: luokan tarkoitus on säilyttää
kahta arvoa, ja on olennaista, että niiden tyypit säilyvät koko elinkaaren
ajan. 

```java,ignore
public class Pari<T, U> {
    private T eka;
    private U toka;

    public Pari(T eka, U toka) {
      this.eka = eka;
      this.toka = toka;
    }

    public T getEka() {
      return eka;
    }

    public U getToka() {
      return toka;
    }

    public void setEka(T eka) {
      this.eka = eka;
    }

    public void setToka(U toka) {
      this.toka = toka;
    }
}
```

Tämän luokan avulla voimme luoda ilmentymiä, joiden arvot voivat olla mitä
tahansa tyyppejä, ilman, että meidän tarvitsee kirjoittaa erillisiä luokkia
jokaista käyttötarkoitusta varten. Alla esimerkki

```java
//- public class Pari<T, U> {
//-     private T eka;
//-     private U toka;
//- 
//-     public Pari(T eka, U toka) {
//-       this.eka = eka;
//-       this.toka = toka;
//-     }
//- 
//-     public T getEka() {
//-       return eka;
//-     }
//- 
//-     public U getToka() {
//-       return toka;
//-     }
//- 
//-     public void setEka(T eka) {
//-       this.eka = eka;
//-     }
//- 
//-     public void setToka(U toka) {
//-       this.toka = toka;
//-     }
//- }
void main() {
    Pari<String, Integer> nimiJaIka = new Pari<>("Matti", 30);
    IO.println("Nimi: " + nimiJaIka.getEka() + ", Ikä: " + nimiJaIka.getToka());

    Pari<Double, Double> koordinaatit = new Pari<>(60.192059, 24.945831);
    IO.println("Leveysaste: " + koordinaatit.getEka() + ", Pituusaste: " + koordinaatit.getToka());
}
```

Jos saman toteuttaisi `Object`-tyyppisillä attribuuteilla ja yrittäisi "paikata"
sen geneerisillä metodeilla, tyyppiturvallisuus katoaa helposti ja mukaan tulee
pakollisia tyyppimuunnoksia, mistä taas seuraa mahdollisia ajonaikaisia
virheitä. 

```java,ignore
public class Pari {
    private final Object eka;
    private final Object toka;

    public Pari(Object eka, Object toka) {
        this.eka = eka;
        this.toka = toka;
    }

    public <T> T getEka() {
        return (T) eka; // tyyppimuunnos, ei käännösaikaista varmistusta
    }
}
```

Yllä olevassa esimerkissä *mukamas* geneerinen metodi ei oikeasti tee luokasta
tyyppiturvallista, koska luokan tila on edelleen `Object`-tasolla ja
tyyppimuunnos tapahtuu vasta ajon aikana. Geneerisen luokan idea on nimenomaan
se, että tyyppi kiinnittyy luokan kenttiin ja niiden käyttöön käännösaikaisesti.

On tärkeää huomata, että geneerisen metodin ja geneerisen luokan valinta ei
riipu siitä, onko metodi staattinen, vaan siitä, kuuluuko tyyppi luokan pysyvään
rakenteeseen vai vain yksittäiseen toimintaan. Metodi luokan sisällä voi
edelleen olla geneerinen, kunhan se käyttää omaa, eri nimistä tyyppiparametria
eikä sekoitu luokan tyyppiparametriin.

<details><summary><i class="bi bi-stars jyu-gold"></i>Valinnaista lisätietoa: 
Java ei voi kaikissa tilanteissa päätellä tyyppiä yksikäsitteisesti
</summary>

Edellä mainittiin, että Java pystyy usein päättelemään geneerisen metodin
tyyppiparametrin automaattisesti. Tätä ominaisuutta kutsutaan nimellä *type
inference*. Käytännössä kääntäjä tarkastelee metodikutsun argumentteja ja niiden
tyyppejä ja päättelee niiden perusteella, mikä tyyppiparametri täyttää metodin
määrittelyn vaatimukset.

Esimerkiksi kutsussa `etsiIndeksi(kokonaisluvut, 3)` kääntäjä näkee, että taulukon
tyyppi on `Integer[]` ja etsittävä arvo on `Integer`. Näiden perusteella se
päättelee, että tyyppiparametrin `T` on oltava `Integer`, eikä kutsussa tarvitse
kirjoittaa sitä erikseen.

Java sallii myös eksplisiittisen geneerisen metodikutsun, jossa tyyppiparametri
annetaan itse:

`Etsija.<Integer>etsiIndeksi(kokonaisluvut, 3);`

Vaikka useimmissa käytännön tilanteissa kääntäjän automaattinen päättely on
kuitenkin riittävä, voi olla tilanteita, joissa kääntäjä ei pysty päättelemään
tyyppiä yksiselitteisesti tai kun halutaan tehdä tyyppi eksplisiittiseksi
luettavuuden tai virheiden paikantamisen vuoksi.

Yksi tällainen tapaus syntyy, kun argumenteilla on eri, mutta yhteensopivia
tyyppejä, eikä ole selvää, mikä niistä pitäisi valita tyyppiparametriksi.

```java
static <T> T valitse(T a, T b) {
    return a;
}

// valitse(1, 1.0);        // KÄÄNNÖSVIRHE: tyyppiä T ei voida päätellä
Number n = <Number>valitse(1, 1.0); // OK: tyyppi annetaan eksplisiittisesti
```

Tässä tapauksessa argumentit ovat eri tyyppiä (`Integer` ja `Double`). Molemmat
perivät `Number`-luokan, mutta kääntäjä ei voi itse päättää, mikä näistä (tai
niiden yhteinen yläluokka) olisi oikea valinta tyyppiparametrille. Antamalla
tyyppiparametrin eksplisiittisesti kerromme kääntäjälle, että haluamme käyttää
metodia `Number`-tyyppisenä.
</details>

## Geneerisyys ja polymorfismi

Geneerisyys ja polymorfismi (tarkemmin alityyppipolymorfismi) ovat kaksi eri
mekanismia, jotka täydentävät toisiaan. Vaikka molemmat lisäävät koodin
joustavuutta, ne ratkaisevat eri ongelmia ja toimivat eri vaiheissa ohjelman
suoritusta.

 1. Polymorfismi (alityypitys): Ajonaikainen mekanismi, johon tutustuimme
    [osassa 3](../osa3/02-polymorfismi.md). Sen tehtävä on mahdollistaa
    olioiden käsittely niiden yliluokan tai rajapinnan kautta, jolloin oikea
    toiminnallisuus (metodin toteutus) valitaan vasta ohjelman ajon aikana.
 2. Geneerisyys (parametrinen polymorfismi): Käännösaikainen mekanismi. Sen
    tehtävä on varmistaa tyyppiturvallisuus ja vähentää toistoa sallimalla saman
    koodin toimia eri tyypeillä ilman että tyyppitieto katoaa.
 3. Pelkkä polymorfismi (ei tyyppiturvaa) Ennen geneerisyyttä (Java 1.4 ja
aiemmat) kokoelmat perustuivat pelkkään polymorfismiin ja `Object`-luokkaan.

```java
// "Raaka" lista (raw type) - ei suositella enää
List lista = new ArrayList();
lista.add("teksti");
lista.add(123); // Sallittu, koska Integer on Object

for (Object o : lista) {
    // toString() kutsuu kunkin olion omaa toteutusta
    IO.println(o.toString());
}
```

Tässä polymorfismi sinänsä toimii, mutta koodi ei ole tyyppiturvallista.
Kääntäjä ei voi estää meitä lisäämästä listaan vääriä tyyppejä, mikä johtaa
virheisiin usein vasta, kun yritämme muuntaa (cast) oliota takaisin
alkuperäiseen tyyppiinsä.

Geneerisyys tuo koodiin rajoitteet, jotka kääntäjä tarkistaa.

```java
List<String> sanat = new ArrayList<>();
sanat.add("kissa");
sanat.add("koira");
// sanat.add(123); // KÄÄNNÖSVIRHE!
```

Tässä geneerisyys estää virheellisen käytön jo ennen kuin ohjelmaa edes ajetaan.
Tässä esimerkissä emme varsinaisesti hyödynnä polymorfismia omien luokkien
suhteen, vaan luotamme kääntäjän tiukkaan valvontaan siitä, että lista sisältää
vain merkkijonoja.

Tehokkainta on yhdistää molemmat: geneerisyys rajaa sallitut tyypit tiettyyn
perheeseen (esim. `Number`), ja polymorfismi hoitaa kyseisen perheen jäsenten
yksilöllisen toiminnan.

```java
// Listalle kelpaa mikä tahansa luku (Integer, Double, Long...)
List<Number> luvut = new ArrayList<>();
luvut.add(1);   // Integer on Number
luvut.add(2.5); // Double on Number

for (Number n : luvut) {
    // Geneerisyys takaa, että 'n' on vähintään Number.
    // Polymorfismi (Number-luokan toteutus) hoitaa arvot.
    IO.println(n.doubleValue());
}
```

## Tyyppirajoitukset

Tyyppiparametreille voidaan asettaa rajoituksia, jotka määrittelevät, millainen
tyyppi parametrina voidaan antaa. Tämä tehdään käyttämällä `extends`-avainsanaa
tyyppiparametrin määrittelyn yhteydessä. Rajoitukset voivat olla luokkia tai
rajapintoja, ja ne määrittelevät ylärajan tyypille, jota tyyppiparametri voi
edustaa. Huomaa, että `extends`-avainsanaa käytetään tässä yhteydessä sekä
luokista että rajapinnoista, vaikka rajapinnat eivät perikään luokkia.

```java
// Tyyppiparametri T voi olla vain Number-luokan alityyppi
<T extends Number> void tulostaLuku(T luku) {
    IO.println("Numero: " + luku.doubleValue());
}

void main() {
    tulostaLuku(10);      // OK: Integer on Number
    tulostaLuku(3.14);    // OK: Double on Number
    // tulostaLuku("kissa"); // KÄÄNNÖSVIRHE: String ei ole Number
}
```

Rajoituksia voidaan asettaa useita käyttämällä `&`-operaattoria, jolloin tyyppiparametrin
on täytettävä useita ehtoja. Alla on esimerkki metodista, jossa tyyppiparametrin tulee olla
sekä `Number`-luokan että `Comparable`-rajapinnan alityyyppi.

```java
// Tyyppiparametri T voi olla vain luokka, joka on sekä Number että Comparable
<T extends Number & Comparable<T>> void vertaile(T a, T b) {
    if (a.compareTo(b) < 0) {
        IO.println(a + " on pienempi kuin " + b);
    } else if (a.compareTo(b) > 0) {
        IO.println(a + " on suurempi kuin " + b);
    } else {
        IO.println(a + " on yhtä suuri kuin " + b);
    }
}

void main() {
    vertaile(10, 20);      // OK: Integer on Number ja Comparable
    vertaile(3.14, 2.71);  // OK: Double on Number ja Comparable
    // vertaile("kissa", "koira"); // KÄÄNNÖSVIRHE: String ei ole Number
}
```

Tyyppirajoituksia voidaan tehdä myös käyttäen niin sanottuja jokerimerkkiä
(`?`), joka edustaa tuntematonta tyyppiä. Jokerimerkin avulla on mahdollista
muun muassa määritellä niin sanottuja ala- ja ylärajoituksia geneerisille
tyypeille. Jokerimerkkiä käytetään usein geneerisissä kokoelmissa, kun halutaan
ilmaista, että kokoelmasta voi lukea tai siihen voi kirjoittaa tietyn tyyppisiä
alkioita, mutta tarkkaa tyyppiä ei tiedetä etukäteen. Alla esimerkkejä. 

```java,ignore
// Metodi, joka ottaa listan, joka voi sisältää mitä tahansa Number-luokan alityyppejä.
// Listasta voi lukea Number-tyyppisiä arvoja, mutta ei voi lisätä mitään, koska
// emme tiedä tarkkaa tyyppiä.
void tulostaLuvut(List<? extends Number> luvut) {
    for (Number n : luvut) {
        IO.println(n); // Huomaa, että emme tiedä tarkkaa tyyppiä, mutta tiedämme että se on Number
    }
    // luvut.add(10); // KÄÄNNÖSVIRHE: emme voi lisätä, koska emme tiedä tarkkaa tyyppiä
}

/* Ottaa listan, jonka alkioiden tyyppi on Number tai jokin sen ylityyppi 
 * (esim. Object), joten listaan on turvallista lisätä Number-arvoja, ja siten myös Integer, Double jne. 
 */
void lisaaLukuja(List<? super Number> lista) {
    lista.add(10);      // OK: Integer on Number
    lista.add(3.14);    // OK: Double on Number
    // lista.add("kissa"); // KÄÄNNÖSVIRHE: String ei ole Number    
    // Integer eka = lista.getFirst(); // KÄÄNNÖSVIRHE: emme tiedä tarkkaa tyyppiä, joten emme voi olettaa että se on Integer
}
```

Emme käsittele jokerimerkkiä tässä osiossa tarkemmin, mutta voit tutustua
niihin omatoimisesti [Javan
dokumentaatiosta](https://docs.oracle.com/javase/tutorial/java/generics/wildcards.html). 

## Geneeristen tyyppien invarianssi

Vaikka `Integer` on `Number`-luokan alityyppi, `List<Integer>` ei ole
`List<Number>`-luokan alityyppi. Ne ovat täysin erillisiä tyyppejä, eikä niillä
ole perintäsuhdetta. Tätä kutsutaan invarianssiksi, eli muuttumattomuudeksi
tyyppisuhteissa. Geneeriset tyypit ovat oletuksena invariantteja
turvallisuussyistä. Alla on lyhyt esimerkki, joka havainnollistaa tätä
periaatetta.

```java
List<Integer> kokonaisluvut = new ArrayList<>();
kokonaisluvut.add(1);

// Jos geneerisyys EI olisi invarianttia, voisimme tehdä näin:
List<Number> luvut = kokonaisluvut; // (Tämä on se kohta, minkä Java estää)

// Nyt luvut ja kokonaisluvut viittaavat samaan listaan muistissa.
// Koska luvut on tyyppiä List<Number>, voimme lisätä sinne liukuluvun:
luvut.add(3.14); 

// MUTTA 'kokonaisluvut' luulee edelleen sisältävänsä vain Integer-lukuja!
Integer i = kokonaisluvut.get(1); // PAM! Ajonaikainen virhe (ClassCastException)
```

Jos voisimme kohdella kokonaislukulistaa yleisenä numerolistana, voisimme
vahingossa ujuttaa sinne desimaalilukuja. Sitten kun alkuperäinen koodi yrittää
lukea listaa kokonaislukuina, ohjelma kaatuisi. Tämä on erityisen hämmentävää
siksi, että Javan taulukot toimivat eri tavalla. Taulukot ovat *kovariantteja*,
eli `Integer[]`-taulukkoa voidaan käsitellä `Number[]`-taulukkona, mutta tällöin
tyyppiturvallisuus tarkistetaan vasta ajonaikaisesti: jos taulukkoon yritetään
tallentaa väärän tyyppinen alkio (esim. Double), Java heittää
`ArrayStoreException`-poikkeuksen.

```java
// Tämä on sallittua Javassa:
Integer[] kokonaisluvut = {1, 2};
Number[] luvut = kokonaisluvut; // OK taulukoilla!

// Mutta tämä aiheuttaa virheen vasta ohjelmaa ajettaessa:
luvut[0] = 3.14; // ArrayStoreException!
``` 

Taulukoiden kanssa Java hyväksyy riskin ja heittää virheen vasta, kun ohjelma on
käynnissä. Geneerisyyden (listat yms.) yksi tärkeimmistä tavoitteista oli
korjata tämä ongelma ja siirtää virhe käännösaikaan.

Jos haluamme hyödyntää polymorfismia geneeristen kokoelmien välillä, meidän on
käytettävä jokerimerkkejä. Esimerkiksi, jos haluamme
käsitellä`List<Integer>`-listaa kuten `List<Number>`-listaa, voimme käyttää
`List<? extends Number>`-tyyppiä.

```java
// Nyt tämä on sallittua, mutta lista on "read-only" turvallisuussyistä
List<? extends Number> luvut = kokonaisluvut;

for (Number n : luvut) {
    IO.println(n); // Toimii
}
```

<task>
  <task-title>Tehtävä 4.8: Etsi suurin. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-8-etsi-suurin/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa4/tehtava8">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 4.9: Kontti. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-9-kontti/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa4/tehtava9">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title><i class="bi bi-stars jyu-gold"></i> Bonus: Tehtävä 4.10: Iso kontti. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-10-iso-kontti/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa4/tehtava10">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title><i class="bi bi-stars jyu-gold"></i> Bonus: Tehtävä 4.11:
  Tyyppirajoitukset, osa 1. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-11-tyyppirajoitukset-1/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa4/tehtava11">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title><i class="bi bi-stars jyu-gold"></i> Bonus: Tehtävä 4.12: Tyyppirajoitukset, osa 2. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/4-12-tyyppirajoitukset-2/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa4/tehtava12">Tee tehtävä TIMissä</a></task-link>
</task>
