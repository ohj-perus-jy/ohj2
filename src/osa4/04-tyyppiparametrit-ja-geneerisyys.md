# Tyyppiparametrit ja geneerisyys

> [!VAROITUS]
> Tämä osio julkaistaan 2. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}
 
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

Jos saman toteuttaisi `Object`-tyyppisillä attribuuteilla ja yrittäisi ”paikata”
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
    Luvussa 3. Sen tehtävä on mahdollistaa olioiden käsittely niiden yliluokan
    tai rajapinnan kautta, jolloin oikea toiminnallisuus (metodin toteutus)
    valitaan vasta ohjelman ajon aikana.
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

## Geneeristen tyyppien invarianssi

Vaikka `Integer` on `Number`-luokan alityyppi, `List<Integer>` ei ole
`List<Number>`-luokan alityyppi. Ne ovat täysin erillisiä tyyppejä, eikä niillä
ole perintäsuhdetta. Tätä kutsutaan invarianssiksi, eli muuttumattomuudeksi
tyyppisuhteissa. Geneeriset tyypit ovat oletuksena invariantteja
turvallisuussyistä:

```java
// OLETETAAN, että tämä olisi sallittua (Javassa tämä on virhe!):
List<Integer> kokonaisluvut = new ArrayList<>();
kokonaisluvut.add(1);

// Jos geneerisyys EI olisi invarianttia, voisimme tehdä näin:
List<Number> luvut = kokonaisluvut; // (Tämä on se kohta, minkä Java estää)

// Nyt 'luvut' ja 'kokonaisluvut' viittaavat samaan listaan muistissa.
// Koska 'luvut' on tyyppiä List<Number>, voimme lisätä sinne liukuluvun:
luvut.add(3.14); 

// MUTTA 'kokonaisluvut' luulee edelleen sisältävänsä vain Integer-lukuja!
Integer i = kokonaisluvut.get(1); // PAM! Ajonaikainen virhe (ClassCastException)
```

Jos voisimme kohdella kokonaislukulistaa yleisenä numerolistana, voisimme
vahingossa ujuttaa sinne desimaalilukuja. Sitten kun alkuperäinen koodi yrittää
lukea listaa kokonaislukuina, ohjelma kaatuisi. Tämä on erityisen hämmentävää
siksi, että Javan taulukot (arrays) toimivat eri tavalla. Taulukot ovat
kovariantteja.

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
käytettävä jokerimerkkejä (wildcards):

```java
// Nyt tämä on sallittua, mutta lista on "read-only" turvallisuussyistä
List<? extends Number> luvut = kokonaisluvut;

for (Number n : luvut) {
    IO.println(n); // Toimii
}
```

## Tyypiparametrit ja polymorfismi

- Näitä on käytetty mm. listoissa `List<Integer>`
- Mitä geneerisyydellä (generic programming / generics) tarkoitetaan?

- Viittaus edellisen osan polymorfismiasiaan
  - Polymorfismi olio-ohjelmoinnissa tarkoittaa tyypillisesti nimenomaan alityypitystä
- Tyyppiparametrit ja geneerisyys ovat myös polymorfismia, sillä periaate on sama:
  - Mahdollistaa, että yksi arvon tyyppi edustaa useita eri tyyppejä
    - Voi luoda luokkia, rajapintoja ja metodeita jotka hyödyntävät ulkopuolelta (muualta koodista) tulevia arvoja määrittämättä tarkkaa tyyppiä etukäteen.
  - Parametrinen polymorfismi

- Miksi tyyppiparametrit ja geneerisiä tyyppejä (tyyppiparametrisoituja luokkia tai rajapintoja), kun on jo polymorfismi alityypeillä?

- Tarkastellaan metodin parametrin yhteydessä hieman luokkaa `Object`, joka itsessään on "geneerinen", eli yleinen luokka — (kertauksena) kaikki Javan luokat perivät `Object`-luokan eli ovat tyyppiä `Object`.

```java
void main() {
    printWithType(new Object());
    printWithType("tekstiä");
    printWithType(1);
    printWithType(1.0);
}

void printWithType(Object value) {
    System.out.println("Arvo: " + value + ", Tyyppi: " + value.getClass().getSimpleName());
}
```

- Vastaava geneerinen metodi tyyppiparametrilla `T`:

```java
void main() {
    printWithType(new Object());
    printWithType("tekstiä");
    printWithType(1);
    printWithType(1.0);
}

<T> void printWithType(T value) {
    System.out.println("Arvo: " + value + ", Tyyppi: " + value.getClass().getSimpleName());
}
```

- `<T>` syntaksi tuttu esimerkiksi listoista: `List<String> = new ArrayList()<>`.

- Ylemmänkaltaisessa käyttötapauksessa ei vielä eroa.

- Katsotaan seuraavaksi seuraavaksi potentiaalista ongelmaa ohjelmakoodin toteutuksessa alityyppien avulla. Samalla tutustumme _rajoitettuihin_ tyyppiparametreihin.

- Pelkkä alityypitys mahdollistaa:

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    int suurempi = getLargest("1", "2")); // kääntäjälle ok
    System.out.println("Suurempi: " + getLargest("5", 4)); // kääntäjälle ok
}

Comparable getLargest(Comparable a, Comparable b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}
```

- Jos Stream API käyty, heitto [sorted()](https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html#sorted--)-metodiin, jolle kelpaa mikä tahansa tyyppi `olio.stream().sorted().toList()` -> vasta ajonaikainen eikä käännöksenaikainen virhe

-> Ajonaikainen virhe, halutaan yleensä välttää sillä näissä on aina riski päätyä loppukäyttäjälle

- Tyyppiparametrien avulla (ja niiden järkevällä käytöllä) tämänkaltainen metodin väärinkäyttö havaitaan varmasti ajoissa

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    int suurempi = getLargest("1", "2")); // virhe havaitaan viimeistään kääntäessä
    System.out.println("Suurempi: " + getLargest(3, "5")); // virhe havaitaan viimeistään kääntäessä
}

<T extends Comparable> T getLargest(T a, T b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}

- Javan `Comparable` on _geneerinen luokka_ ja ottaa tyyppiparametrin, joten oikeampi käyttö olisi

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    int suurempi = getLargest("1", "2")); // virhe havaitaan viimeistään kääntäessä
    System.out.println("Suurempi: " + getLargest(3, "5")); // virhe havaitaan viimeistään kääntäessä
}

<T extends Comparable<T>> T getLargest(T a, T b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}

- Rajoitettuja tyyppiparametreja voi olla useampia, esim.

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    String suurempi = getLargest("1", "2")); // virhe havaitaan viimeistään kääntäessä
}

<T extends Comparable<T> & Number> T getLargest(T a, T b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}

Tästä päästäänkiin geneerisiin luokkiin ja rajapintoihin.

- Klassinen esimerkki geneerisestä :

```java
class Pair<T> {
    private T first;
    private T second;

    public Pair(T first, T second) {
        this.first = first;
        this.second = second;
    }

    public T getFirst() {
        return first;
    }

    public T getSecond() {
        return second;
    }

    public void setFirst(T first) {
        this.first = first;
    }

    public void setSecond(T second) {
        this.second = second;
    }
}
```

Tyyppiparametreja voi olla useampi

```java
class Pair<T, U> {
    private T first;
    private U second;

    public Pair(T first, U second) {
        this.first = first;
        this.second = second;
    }

    public T getFirst() {
        return first;
    }

    public U getSecond() {
        return second;
    }

    public void setFirst(T first) {
        this.first = first;
    }

    public void setSecond(U second) {
        this.second = second;
    }
}
```


- Geneerisen metodin syntaksi (geneeriset esimerkit vasta ongelman havainnollistuksen jälkeen vai samassa?)
- Tyyppirajoitukset (tämä vasta myöhemmin vai Comparable-esimerkin kanssa?

- Tyyppiparametrit mahdollistavat eritasoista tyyppitarkastusta ja yleiskäyttöisen koodin kehittämistä kuin mitä pelkällä alityypityksellä on mahdollista

- Esimerkkejä milloin geneeriset tyypit ovat kivoja metodeissa
  - Identtinen overloadaus eri tyypeille
    - tässä myös miksi overloadaus on myös polymorfismia?

- Tehtäviä geneerisistä metodeista

- Esimerkkejä milloin geneeriset tyypit ovat kivoja luokissa
- Geneerisen luokan syntaksi

- Tehtäviä geneerisistä luokista

- Ekstrana: jokerimerkki `?` tyyppiparametreissa
  - rajoitetut jokerimerkit
    - `extends` ja `super`
  - `?` sama kuin `? extends Object`
  - Tutkitaan mitä `Collections.sort`

- Ekstramaininta: Javassa geneeriset tyypit muuten ohjelman kääntämisen aikana rajoituksen tyypiksi tai tyypiksi `Object`
- Ekstramaininta: (koska vain Java -asia): Geneerinen tyyppi ei voi olla primitiivi

- Ei unionityyppejä (kuten esimerkiksi Rustissa), täytyy tehdä luokka esim. StringOrInt

```java
class StringOrInt {
    private final Object value;

//    public StringOrInt(Object value) {  // ei näin -> ajonaikaiset virheet voidaan estää helposti kahdella konstruktorilla
//        if (!(value instanceof String) && !(value instanceof Integer)) {
//            throw new IllegalArgumentException("Value must be a String or an Integer");
//        }
//        this.value = value;
//    }

    public StringOrInt(String value) {
        this.value = value;
    }

    public StringOrInt(Integer value) {
        this.value = value;
    }

    public Object getValue() {
        return value;
    }

    public String getStringValue() {
        if (value instanceof String s) {
            return s;
        } else if (value instanceof Integer i) {
            return Integer.toString(i);
        } else {
            throw new IllegalStateException("Value is neither String nor Integer");
        }
    }

    public boolean isString() {
        return value instanceof String;
    }

    public boolean isInteger() {
        return value instanceof Integer;
    }

    public int getIntValue() {
        if (value instanceof Integer i) {
            return i;
        } else if (value instanceof String s) {
            try {
                return Integer.parseInt(s);
            } catch (NumberFormatException e) {
                throw new IllegalStateException("String value cannot be parsed to Integer");
            }
        } else {
            throw new IllegalStateException("Value is neither String nor Integer");
        }
    }
}
```

- Menee kikkailuksi, parempi tyytyä rajapintoihin ja abstrakteihin luokkiin
