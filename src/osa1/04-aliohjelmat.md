# Aliohjelmat

> [!VAROITUS]
> Tämä osio julkaistaan 12. tammikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Osaat määritellä aliohjelman 
> - Osaat käsitellä tietoa aliohjelmien avulla
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
`keskiarvo`-aliohjelmaa, joka laskee kokonaislukujen joukon keskiarvon. Tässä
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

Esittelyrivin jälkeen kirjoitetaan aaltosulkeiden sisään aliohjelman runko-osa.
Se sisältää varsinaisen koodin, joka suoritetaan, kun aliohjelmaa kutsutaan. 

Kuten kaikessa lähdekoodissa muutenkin, myös aliohjelmien ja parametrien nimien
tulee olla kuvaavia ja noudattaa Javan nimeämiskäytäntöjä sekä [tämän kurssin
tyyliohjetta](../tyyliohje.md).

## Paluuarvot ja datan käsittely

Aliohjelmaa voi ajatella *mustana laatikkona*: sinne syötetään raaka-ainetta
(parametrit), laatikon sisällä tapahtuu prosessointia, ja lopuksi ulos tulee
valmis tuote (paluuarvo). Avainsana `return` lopettaa aliohjelman suorituksen
välittömästi ja palauttaa arvon kutsujalle. Arvon tyypin on vastattava aliohjelman
määrittelyssä annettua tyyppiä.

Toisen tekemää aliohjelmaa käytettäessä emme välttämättä tiedä, mitä laatikon
sisällä tapahtuu, vaan luotamme siihen, että se toimii määritellyllä tavalla.
Tämä on tyypillistä ohjelmoinnissa, jossa käytämme valmiita kirjastoja ja
aliohjelmia. 

## Void-aliohjelma

Joskus aliohjelmaa tarvitaan vain tekemään jokin toimenpide, kuten tulostamaan
tekstiä ruudulle, tai aiheuttamaan muu sivuvaikutus. Tällaisessa tapauksessa
aliohjelman ei tarvitse palauttaa arvoa. Tällöin paluuarvon tyypiksi merkitään
`void`.

## Parametrin välitys: alkeistietotyypit ja viitetyypit

On tärkeää ymmärtää, mitä itse asiassa annamme aliohjelmalle parametrina kun
kutsumme sitä. Javassa kaikki parametrit välitetään arvona (ns.
*pass-by-value*), mutta välitettävän arvon luonne riippuu parametrin tyypistä.

 * Jos parametrin tyyppi on alkeistietotyyppi (kuten `int`, `double`, `char`,
   `boolean`), aliohjelmalle annetaan *kopio alkuperäisestä arvosta*.
 * Jos parametrin tyyppi on viitetyyppi (kuten taulukko), aliohjelmalle
   annetaan *kopio viitteestä alkuperäiseen dataan*. 

Kun alkeistietotyyppi (ks. [Luku
1.2](02-muuttujat-ja-tietotyypit.md#alkeistietotyypit)) annetaan
parametrina, kyseisen muuttujan arvo kopioidaan ja välitetään
kutsuttavalle aliohjelmalle. Jos aliohjelma muuttaa tätä kopiota, alkuperäinen
muuttuja ei muutu. Alla esimerkki, jossa annamme `int`-tyyppisen muuttujan
parametrina. 

```java
void yritaMuuttaa(int luku) {
    luku = 99; // Muutetaan vain kopiota
    IO.println("Metodissa: " + luku);
}

void main() {
    int x = 10;
    yritaMuuttaa(x);
    IO.println("Mainissa: " + x); // Tulostaa edelleen 10
}
```

Kun viitetyyppi (ks. [Luku
1.2](02-muuttujat-ja-tietotyypit.md#viitetietotyypit)) annetaan parametrina
aliohjelmalle, kopioidaan
viite eikä alkuperäistä dataa. Aliohjelma
saa siis käyttöönsä kopion viitteestä, joka osoittaa samaan
dataan kuin pääohjelman muuttuja. Jos aliohjelma sitten muokkaa muuttujan 
osoittamaa dataa (esim. taulukon alkioita), muutos näkyy myös
pääohjelmassa.

Voit ajatella viitteen ikään kuin "kaukosäätimenä", jolla
ohjataan "televisiota" eli dataa. Vaikka aliohjelmalle
viedään kopio "kaukosäätimestä", voi sillä ohjata samaa "televisiota".

Alla esimerkki tällaisesta tilanteesta, jossa annamme
`int[]`-tyyppisen taulukon parametrina, ja aliohjelma muokkaa taulukon alkioita.

```java
void nollaaTaulukko(int[] taulukko) {
    // Tämä muutos tapahtuu alkuperäiselle taulukolle!
    // Koska "taulukko"-muuttuja viittaa samaan taulukkoon.
    for (int i = 0; i < taulukko.length; i++) {
        taulukko[i] = 0;
    }
}

void main(String[] args) {
    int[] luvut = {1, 2, 3};
    
    nollaaTaulukko(luvut);
    
    // Alkuperäinen taulukko on muuttunut
    IO.println(luvut[0]); // Tulostaa 0
}
```

Oleellista on kuitenkin ymmärtää, että aliohjelman kutsussa annoimme
nimenomaisesti kopion viitteestä, emme alkuperäistä viitettä. Jos aliohjelma
yrittäisi muuttaa viitettä osoittamaan muuhun dataan (esim. toiseen taulukkoon), 
tämä muutos ei vaikuttaisi alkuperäiseen viitteeseen pääohjelmassa. Alla
esimerkki tästä 
tilanteesta:

```java
void main(String[] args) {
    int[] luvut = {1, 2, 3};
    
    muutaViite(luvut);
    
    // Alkuperäinen taulukko ei ole muuttunut
    IO.println(luvut[0]); // Tulostaa edelleen 1
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

Aliohjelmaa, joka muokkaa parametrina annettua dataa, sanotaan usein
aiheuttavan *sivuvaikutuksia*. 
Esimerkiksi, jos alla oleva aliohjelma `kaanna` kääntää parametrina annetun
taulukon alkiot käänteiseen järjestykseen:

```java
void kaanna(int[] taulu) {
    // Toteutus piilotettu tilan säästämiseksi
//-    for (int i = 0; i < taulu.length / 2; i++) {
//-        int tmp = taulu[i];
//-        taulu[i] = taulu[taulu.length - 1 - i];
//-        taulu[taulu.length - 1 - i] = tmp;
//-    }
}

void main() {
    int[] taulukko = {1, 2, 3, 4, 5};
    IO.println("taulukko = " + Arrays.toString(taulukko));
    kaanna(taulukko);
    IO.println("taulukko = " + Arrays.toString(taulukko));
}
```

Huomaa, että `kaanna` ei palauta mitään, mutta sen *sivuvaikutuksena*
on, että parametrina annettu taulukko kääntyy.
Yllä oleva aliohjelma voitaisiin toteuttaa myös ilman sivuvaikutuksia
muuttamalla palautusarvoa:

```java
int[] kaanna(int[] taulu) {
    // Toteutus piilotettu tilan säästämiseksi
//-    int[] tulos = new int[taulu.length];
//-    for (int i = 0; i < taulu.length; i++) {
//-        tulos[i] = taulu[taulu.length - 1 - i];
//-    }
//-    return tulos;
}

void main() {
    int[] taulukko = {1, 2, 3, 4, 5};
    IO.println("taulukko = " + Arrays.toString(taulukko));
    int[] kaannetty = kaanna(taulukko);
    IO.println("kaannetty = " + Arrays.toString(kaannetty));
}
```

Sivuvaikutukset voivat olla hyödyllisiä muun muassa muistin käytön optimoinnin
kannalta, mutta ne voivat myös tehdä ohjelmasta
vaikeammin ymmärrettävän. Yllä olevassa esimerkissä 
aliohjelman `void kaanna(int[] taulu)` sivuvaikutus ei ole ilmiselvää
ellei katso aliohjelman lähdekoodia. Sivuvaikutuksilla voikin esimerkiksi 
tiedostamatta tuhota tai muokata dataa.
Siksi on erittäin tärkeää
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
jälkeen komennon `javadoc Summa.java`. Nyt voit avata luodun `index.html`
-tiedoston selaimessa, klikata selaimessa luokkaa `Summa` ja pääset
seuraavanlaiseen näkymään:

![Juuri tehdystä dokumentaatiosta kuva, joka voi näyttää tutulta jos on käynyt
tutkimassa Javan omaa dokumentaatiota ](images/summaDokumentaatio.png)

Näyttääkö tutulta? Vertaa esimerkiksi [Javan dokumentaatioon IO-luokasta](https://docs.oracle.com/javase/8/docs/api/java/lang/Object.html)

</details>
