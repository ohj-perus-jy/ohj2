# Aliohjelmat

> [!Osaamistavoitteet]
>
> - Osaat määritellä aliohjelman 
> - Osaat käsitellään tietoa aliohjelmien avulla
> - Ymmärrät Javan perustietotyyppien ja viitetyyppien eron aliohjelmaa kutsuttaessa
> - Osaat dokumentoida aliohjelman

Aliohjelma on ohjelman osa, joka suorittaa tietyn tehtävän. Aliohjelmat
helpottavat ohjelman jäsentämistä, sillä niiden avulla ohjelma voidaan jakaa
pienempiin, hallittavampiin osiin. Aliohjelmat helpottavat myös
uudelleenkäyttöä, sillä samaa aliohjelmaa voidaan kutsua useita kertoja eri
kohdissa ohjelmaa ilman, että koodia tarvitsee kirjoittaa uudelleen. 

Aliohjelmia kutsutaan joskus myös funktioiksi, ja olio-ohjelmoinnin yhteydessä
myös metodeiksi. Nimeäminen riippuu kontekstista, mutta tässä yhteydessä
käytämme termiä aliohjelma.

Aliohjelma voi ottaa vastaan *syötteitä*, joita sanotaan *parametreiksi*.
Tehtävän suoritettuaan aliohjelma voi palauttaa tuloksen. Kutsutaan alla
`Keskiarvo`-aliohjelmaa, joka laskee kokonaislukujen joukon keskiarvon. Tässä
siis parametrina annetaan yksi kokonaislukutaulukko, ja aliohjelma palauttaa
keskiarvon `double`-tyyppisenä arvona.

```java
void main () {
    int[] luvut = {4, 8, 15, 16, 23, 42};
    double keskiarvo = keskiarvo(luvut);
    IO.println("Lukujen keskiarvo on: " + keskiarvo);
}

double keskiarvo(int[] luvut) {
    if (luvut.length == 0) {
        return 0; 
    }
    double summa = 0;
    for (int luku : luvut) {
        summa += luku;
    }
    return summa / luvut.length;
}
```

## Aliohjelman määrittely

Yllä oleva `keskiarvo`-aliohjelma koostuu monesta pienestä palasesta (1)
paluuarvo, (2) nimi, (3) parametrit ja (4) runko-osa. 

 * (1) Paluuarvon tyyppi (tässä `double`): Kertoo, minkä tyyppistä tietoa aliohjelma
   palauttaa. Jos aliohjelma ei palauta mitään, tyyppi on `void`. 
 * (2) Aliohjelman nimi (tässä `keskiarvo`): Kertoo millä nimellä sitä
   kutsutaan. 
 * (3) Parametrit (tässä `int[] luvut`): Sulkeiden sisään määritellään
   muuttujat, jotka ottavat vastaan aliohjelmalle annettavat syötteet.
   Parametreja voi olla nolla tai useampia, ja ne erotetaan toisistaan pilkulla.
   Jokaisella parametrilla on oma tyyppi ja nimi.

Kutsutaan näitä kolmea palasta yhdessä aliohjelman *esittelyriviksi*. [Luvussa
2](../osa2/index.md) tutustutaan myös olio-ohjelmointiin liittyviin määreisiin
(engl. *modifier*), joita esittelyriville voi lisätä.

> TODO: Siirto lukuun 2? Kertovat, että metodi on kaikkien käytettävissä ja toimii
> ilman olioita. Nämä osat vaihtelevat tai voivat jopa puuttua sen mukaan, missä
> kontekstissa aliohjelmaa käytetään. Ilman olioita toimivat aliohjelmat
> määritellään kuitenkin yleensä juuri näin.

Esittelyrivin jälkeen kirjoitetaan aaltosulkeiden sisään aliohjelman runko-osa.
Se sisältää varsinaisen koodin, joka suoritetaan, kun aliohjelmaa kutsutaan. 

Kuten kaikessa lähdekoodissa muutenkin, myös aliohjelmien ja parametrien nimien
tulee olla kuvaavia ja noudattaa Javan nimeämiskäytäntöjä sekä [tämän kurssin
tyyliohjetta](../tyyliohje.md).

## Paluuarvot ja datan käsittely

Aliohjelmaa voi ajatella *mustana laatikkona*: sinne syötetään raaka-ainetta
(parametrit), laatikon sisällä tapahtuu prosessointia, ja lopuksi ulos tulee
valmis tuote (paluuarvo). Avainsana `return` lopettaa metodin suorituksen
välittömästi ja palauttaa arvon kutsujalle. Arvon tyypin on vastattava metodin
määrittelyssä annettua tyyppiä.

Toisen tekemää aliohjelmaa käytettäessä emme välttämättä tiedä, mitä laatikon
sisällä tapahtuu, vaan luotamme siihen, että se toimii määritellyllä tavalla.
Tämä on tyypillistä ohjelmoinnissa, jossa käytämme valmiita kirjastoja ja
aliohjelmia. 

## Void-aliohjelma

Joskus metodia tarvitaan vain tekemään jokin toimenpide, kuten tulostamaan
tekstiä ruudulle, tai aiheuttamaan muu sivuvaikutus. Tällaisessa tapauksessa
aliohjelman ei tarvitse palauttaa arvoa. Tällöin paluuarvon tyypiksi merkitään
`void`.

## Parametrin välitys: alkeistietotyypit ja viitetyypit

On tärkeää ymmärtää, mitä itse asiassa annamme aliohjelmalle parametrina kun
kutsumme sitä. Javassa kaikki parametrit välitetään arvona (ns.
*pass-by-value*), mutta välitettävän arvon luonne riippuu parametrin tyypistä.

 * Jos parametrin tyyppi on alkeistietotyyppi (kuten `int`, `double`, `char`,
   `boolean`), aliohjelmalle annetaan *kopio alkuperäisestä arvosta*.
 * Jos parametrin tyyppi on viitetyyppi (kuten taulukko tai olio), aliohjelmalle
   annetaan *kopio viitteestä olioon*. 

Kun alkeistietotyyppi (ks. [Luku 1.2](02-muuttujat-ja-tietotyypit.md)) annetaan
parametrina metodille, kyseisen muuttujan arvo kopioidaan ja välitetään
kutsuttavalle aliohjelmalle. Jos aliohjelma muuttaa tätä kopiota, alkuperäinen
muuttuja ei muutu. Alla esimerkki, jossa annamme `int`-tyyppisen muuttujan
parametrina. 

```java
void yritaMuuttaa(int luku) {
    luku = 99; // Muutetaan vain kopiota
    System.out.println("Metodissa: " + luku);
}

void main(String[] args) {
    int x = 10;
    yritaMuuttaa(x);
    System.out.println("Mainissa: " + x); // Tulostaa edelleen 10
}
```

Javassa kaikki tyypit, mitkä eivät ole alkeistietotyyppejä, ovat
*viitetyyppejä*. Tässä vaiheessa opintoja tutuimpia viitetyyppejä ovat taulukot
(esim. `int[]`) ja `String`-oliot. Myös kaikki itse määritellyt oliot, joihin
tutustutaan Luvussa 3, ovat viitetyyppejä. 

Viitetyypin muuttuja ei sisällä itse dataa (kuten taulukon lukuja), vaan
viitteen olioon, joka sisältää datan. Voi ajatella, että muuttuja on
kaukosäädin, ja itse data on televisio. Ihan kuten televisiota ohjaillaan
kaukosäätimellä, viitetyyppisiä muuttujia käytetään olion sisältämän datan
käsittelyyn. 

Analogiamme hieman hajoaa tässä kohden, mutta viedään se silti loppuun, kun
kerran aloitimme: Kun viitetyyppi annetaan parametrina aliohjelmalle, kopioidaan
viite; siis kopio kaukosäätimestä, eikä alkuperäistä kaukosäädintä. Aliohjelma
saa kyllä käyttöönsä samanlaisen "kaukosäätimen", joka osoittaa samaan
"televisioon" kuin pääohjelman kaukosäädin. Jos aliohjelma sitten muokkaa olion
sisältöä (esim. taulukon alkioita) viitteen kautta, muutos näkyy myös
pääohjelmassa. Alla esimerkki tällaisesta tilanteesta, jossa annamme
`int[]`-tyyppisen taulukon parametrina, ja aliohjelma muokkaa taulukon alkioita.

```java
void nollaaTaulukko(int[] taulukko) {
    // Tämä muutos tapahtuu alkuperäiselle taulukolle!
    // Koska "taulukko"-muuttuja viittaa samaan olioon.
    for (int i = 0; i < taulukko.length; i++) {
        taulukko[i] = 0;
    }
}

void main(String[] args) {
    int[] luvut = {1, 2, 3};
    
    nollaaTaulukko(luvut);
    
    // Alkuperäinen taulukko on muuttunut
    System.out.println(luvut[0]); // Tulostaa 0
}
```

Oleellista on kuitenkin ymmärtää, että aliohjelman kutsussa annoimme
nimenomaisesti kopion viitteestä, emme alkuperäistä viitettä. Jos aliohjelma
yrittäisi muuttaa viitettä osoittamaan toiseen olioon, tämä muutos ei
vaikuttaisi alkuperäiseen viitteeseen pääohjelmassa. Alla esimerkki tästä
tilanteesta:

```java
void main(String[] args) {
    int[] luvut = {1, 2, 3};
    
    muutaViite(luvut);
    
    // Alkuperäinen taulukko ei ole muuttunut
    System.out.println(luvut[0]); // Tulostaa edelleen 1
}

void muutaViite(int[] taulukko) {
    // Tämä muutos ei vaikuta alkuperäiseen viitteeseen!
    taulukko = new int[] {9, 9, 9};
}
```

Joissain kielissä, kuten C++:ssa, on mahdollista välittää parametrina
alkuperäinen muuttuja viitteenä (ns. *pass-by-reference*). Javassa tällaista
mekanismia ei kuitenkaan ole, vaan kaikki parametrit välitetään arvona, kuten
yllä on selitetty.

## Aliohjelma ja sivuvaikutukset

Aliohjelmaa, joka muokkaa parametrina annettua oliota, sanotaan usein
aiheuttavan *sivuvaikutuksia*. Sivuvaikutukset voivat olla hyödyllisiä, mutta ne
voivat myös tehdä ohjelmasta vaikeammin ymmärrettävän. Siksi on erittäin tärkeää
olla tietoinen siitä, miten aliohjelmat käsittelevät parametreja.

## Kommentointi ja dokumentointi

Lähdekoodiin voi kirjoittaa tekstiä, joka ei ole varsinaista koodia, vaan
selittää sitä. Tällaista selitystekstiä on kahdentyyppisiä: (1) koodin sekaan
kirjoitettavia kommentteja (nimitetään näitä lyhyesti *kommenteiksi*) sekä (2)
dokumentaatiokommentteja. 

Kommenttien tarkoitus on palvella *kehityksen aikaista* tekemistä. Ne näkyvät
sisäisesti, eli ohjelmoijalle itselleen.  Dokumentaatiokommenttien tarkoitus on
palvella kaikkia, jotka *käyttävät* koodia. Ne näkyvät paitsi ohjelmoijalle
itselleen, myös niille, jotka hyödyntävät koodia esimerkiksi API:n (*application
programming interface*) kautta.

### Yhden rivin kommentointi

Yhden rivin kommentteja, jonka syntaksi on `//` voidaan käyttää esimerkiksi
merkitsemään TODO-kohtia koodissa:

```java
void main() {
    // TODO: Tarkista millaisia ongelmia tästä ratkaisusta voi tulla
    String syote = IO.readln();
    IO.println("Kirjoitit: " + syote);
}
```

Yleisesti hyvä periaate on, että ohjelmoija pyrkii kirjoittamaan sellaista
koodia, joka selittää itse itseään. Muuttujat, luokat, aliohjelmat ja muut
nimet, johon ohjelmoija pystyy vaikuttamaan, pyritään nimeämään mahdollisimman
kuvaavasti, jolloin yksittäisten rivien kommentointi ei välttämättä ole tarpeen.
Asiaa on kuvattu myös kurssin [tyylioppaassa](). TODO: Linkki.

Joskus yhden rivin kommenteilta ei voi välttyä, jos jotakin operaatiota ei voida
olettaa itsestäänselväksi tai muuttujan nimestä tulisi kohtuuttoman pitkä:

```java
void main() {
    int n = 9;
    // Pyöristää alaspäin lähimpään neljällä jaolliseen lukuun
    int pyoristetty = n & ~3; 
    IO.println(pyoristetty);
}
```

Nyt muuttujan `pyoristetty` tilalla voisi olla `pyoristaaAlaspainLahimpaanNeljallaJaolliseenLukuun`, joka ei sekään ole oikein
järkevä vaihtoehto.

### Monirivinen kommentti

Javassa monirivinen kommentti tulee `/*` ja  `*/` väliin. Tällaista suositellaan
käytettäväksi, kun jokin monimutkaisempi logiikka vaatii tarkempaa avaamista
ja/tai on järkevää selittää miksi juuri kyseinen ratkaisu on valittu. Tätä
kommenteissa olevaa tarkempaa avaamista ei kuitenkaan ole tarkoitus näyttää
koodin käyttäjille.

```java,noplayground
if (kayttaja.kayttaaVanhaa) {
    /* 
     * Vanhat käyttäjät (rekisteröityneet ennen vuotta 2022) käyttävät 
     * toistaiseksi vanhaa käyttöoikeusmallia.
     * Älä poista tarkistusta, ennen kuin kaikki tilit on siirretty.
     */
    return kaytaVanhojaKayttooikeuksia(kayttaja);
}
```

### Dokumentaatiokommentti

Dokumentaatiokommentti tarkoittaa sellaista kommenttia, josta voidaan
automaattisesti luoda erilaisia koodin käyttäjille tarkoitettuja
dokumentaatiomuotoja. Tällaisia dokumentaatiomuotoja voivat olla esimerkiksi
HTML-muotoiset API-dokumentaatiot, jotka kertovat miten koodia käytetään, tai
IDE:ssä näkyvät työkaluvihjeet aliohjelmien käytöstä.

Dokumentaatiokommenttien sijainti on ennen dokumentoitavaa koodia, kuten
aliohjelmaa tai luokkaa.

Javassa dokumentaatiokommentit kirjoitetaan erityisellä syntaksilla, joka eroaa
tavallisista kommenteista. Dokumentaatiokommentit alkavat `/**` ja päättyvät
`*/`, eli ovat syntaksiltaan hyvin lähellä monirivistä kommenttia.

```java
//- void main() {
//-   IO.println("summa(1, 2) ==> " + summa(1, 2));
//- }
//-
/**
 * Laskee kahden kokonaisluvun summan.
 * 
 * @param a Ensimmäinen luku
 * @param b Toinen luku
 * @return Lukujen summa
 */
int summa(int a , int b) {
    return a + b;
}
```

Aliohjelman dokumentaatiokommentin runko syntyy automaattisesti
IDEA-kehitysympäristössä, kun aliohjelman esittelyrivin yläpuolelle kirjoittaa
merkit `/**` ja painaa <kbd>Enter</kbd>. 

<video src="images/intellij-docstring.mp4" controls></video>

<details closed><summary><i class="bi bi-stars jyu-gold"></i> Bonus: miltä Javan dokumentaatio näyttää? </summary>

Oletetaan nyt, että tallennat yllä olevan tiedostoon `Summa.java` ja ajat sen
jälkeen komennon `javadoc Summa.java` Nyt voit avata luodun `index.html`
-tiedoston selaimessa, klikata selaimessa luokkaa `Summa` ja pääset
seuraavanlaiseen näkymään:

![Juuri tehdystä dokumentaatiosta kuva, joka voi näyttää tutulta jos on käynyt
tutkimassa Javan omaa dokumentaatiota ](images/summaDokumentaatio.png)

Näyttääkö tutulta? Vertaa esimerkiksi [Javan dokumentaatioon IO-luokasta](https://docs.oracle.com/javase/8/docs/api/java/lang/Object.html)

</details>

## Tehtävät



## T1.2
- Tehtävänäsi on Monty hallin ongelman simulointi neljällä ovella. Jos ongelma ei ole tuttu, 

Monty hallin ongelma neljällä ovella:
Kilpailijalla on edessään neljä ovea. Yhden oven takana on palkinto ja muiden ovien takana ei ole mitään. Kilpailija valitsee yhden ovista, jonka jälkeen juontaja paljastaa yhden ovista, jonka takana ei ole mitään. Kannattaako kilpailijan vaihtaa ovea suljettuun oveen, vai pitäytyä alkuperäisessä valinnassa?

Tehtävänäsi on simuloida molemmat vaihtoehdot:
1. Kilpailija pitäytyy alkuperäisessä valinnassaan
2. Kilpailija vaihtaa johonkin jäljellä olevista ovista, jotka eivät ole vielä auki ja joka ei ollut kilpailijan ensimmäinen valinta

ja valita vaihtoehdoista se, jolla voittaa todennäköisimmiten.

## T1.3
Komentorivipohjainen visa

(Pitä luoda kysymykset, oikeat vastaukset, tarkistaminen ja pisteytys)

<task>
<task-title>Tehtävä 1.4: Kokonaislukujen lukeminen käyttäjältä <points>1 p.</points> </task-title>
<handout>

{{#include ../exercises/1-4-kokonaislukujen-lukeminen/handout.md}}

</handout>
<task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa1/tehtava4">Tee tehtävä TIMissä</a></task-link>
</task>

## T1.5

Tulosta kaikki alkuluvut väliltä 1-n, missä n on käyttäjän syöttämä luku. (Kenties n voi olla korkeintaan 100?)

## T1.6
Laske matriisiin kahden muun matriisin summa, eli A + B = C

<task>
<task-title>Tehtävä 7: Salasanan vahvuuden tarkistaminen <points>1 p.</points> </task-title>
<handout>

{{#include ../exercises/1-7-salasanan-tarkistaja/handout.md}}

</handout>
<task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa1/tehtava7">Tee tehtävä TIMissä</a></task-link>
</task>

## T1.9
Laske kuinka monta esiintymää kutakin numeroa esiintyy luvussa.
Esimerkiksi 12223 --> 1 1kpl, 2 3 kpl ja 3 1 kpl

## T1.10
TODO: rajuruoho
Tulosta matriisissa olevat luvut spiraalimaisesti aloittaen vasemmasta yläkulmasta ja edeten kohti keskustaa. Esimerkiksi [[1 2 3] 
[4 5 6]
[7 8 9]]
palauttaa 123698745

## T1.11
Merkkijonon pakkaaminen: Tulosta merkki ja merkkien lukumäärä aaaabbbccd --> a4b3c2d1

<task>
<task-title>Tehtävä 10: Puuttuva luku <points>1 p.</points> </task-title>
<handout>

{{#include ../exercises/1-10-puuttuva-luku/handout.md}}

</handout>
<task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa1/tehtava10">Tee tehtävä TIMissä</a></task-link>
</task>

## T1.13
Pätevät sulkeet, eli tarkasta suljetaanko kaikki avatut sulut { --> false {} --> true, ({}) --> true jne.

## B2
TODO: rajuruoho
- Vakioaikainen haku taulukosta. Esimerkiksi, että kuinka monta päivää on kuukaudessa?

(Teoriatausta se, että laskennallista nopeutta voidaan lisätä käyttämällä enemmän muistia. Tähän esimerkiksi HashMap perustuu)

<task>
<task-title>Tehtävä B3: Sanakirja <points>1 p.</points> </task-title>
<handout>

{{#include ../exercises/1-B3-sanakirja/handout.md}}

</handout>
<task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa1/tehtavaB3">Tee tehtävä TIMissä</a></task-link>
</task>

## G1
TODO: rajuruoho
- Linkitetty lista käänteiseksi?

## G2

TODO: rajuruoho
- Neliömatriisin eli n x n, n $\in \mathbb{N}$ matriisin pyöräyttäminen 90-astetta. 
- In ([[1,2],[3,4]], oikealle) --> [[3,1],[4,2]]