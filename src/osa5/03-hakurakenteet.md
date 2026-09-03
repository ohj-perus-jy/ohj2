# Hakurakenteet

> [!Osaamistavoitteet]
>
> - Tunnet Java-kielen yleisimmät valmiit tietorakenteet: `Map` ja sen toteutukset `HashMap`, `LinkedHashMap` ja `TreeMap`.
> - Osaat käyttää em. tietorakenteita.
> - Ymmärrät em. tietorakenteiden keskeisimmät operaatiot ja tunnistat niiden
>   aikavaativuudet.
> - Ymmärrät, miksi oliot tarvitsevat `hashCode`-metodin.

Kuvitellaan tilanne, jossa ylläpidämme laajaa opiskelijarekisteriä. Haluamme
tallentaa kunkin opiskelijan numeron ja nimen siten, että voimme 
opiskelijanumeron perusteella löytää helposti opiskelijan nimen. 

Jos käyttäisimme tähän listaa, joutuisimme tallentamaan tiedot joko 
eri listoihin tai luomaan erillisen olion, joka sisältää kaikki tiedot. Kun 
haluaisimme hakea tietyn henkilön tiedot, joutuisimme käymään listan alkioita 
läpi, kunnes oikea henkilö löytyy. Tämä ei ole hirveän tehokasta, jos 
opiskelijoita on hyvin suuri määrä. 

Hakurakenteet tarjoavat tähän ratkaisun mahdollistamalla suoran haun jonkin
tunnuksen perusteella parhaimmassa tapauksessa ilman koko listan läpikäymistä.
Tunnuksena voisi toimia esimerkiksi opiskelijan numero. Hakurakenne toimii kuin
sanakirja, josta voimme katsoa suoraan oikean kohdan sen sijaan, että lukisimme
koko kirjan kannesta kanteen löytääksemme tietyn sanan. Hakurakenteita
kutsutaankin useissa ohjelmointikielissä nimellä *sanakirja* (engl.
*dictionary*). Javassa ne tunnetaan nimellä *map*.

```java
//-void main() {
// Luodaan avain-arvo-pareja.
Map<String, String> opiskelijat = Map.of(
  "123", "Joni",
  "555", "Maija",
  "789", "Mikko"
);

// Voimme pyytää avaimen avulla opiskelijan tietoja suoraan käymättä
// koko tietorakennetta läpi.
IO.println("Opiskelija, jonka numero on 123: " + opiskelijat.get("123"));
//-}
```

Hakurakenteet ovat tietorakenteita, joihin tallennetaan tietoa
avain-arvo-pareina (engl. *key-value pair*), joista käytetään myös nimitystä
`Entry`. Siinä missä listassa yksilöllinen, kokonaislukutyyppinen indeksi toimii
"reittinä" sisältöön, hakurakenteessa reittinä toimii yksilöllinen, minkä
tahansa tyyppinen olio. Avaimet ovat aina uniikkeja; yksi avain voi esiintyä
hakurakenteessa vain kerran ja se osoittaa vain yhteen arvoon kerrallaan. Arvot
sen sijaan eivät ole uniikkeja. 

> [!HUOMAUTUS]
> Javassa sekä avaimet että arvot ovat aina olioita. Ne eivät 
> voi olla primitiivityyppejä, kuten `int` tai `double`, vaan tähän 
> tarkoitukseen on käytettävä vastaavia kääreluokkia, kuten `Integer` tai
> `Double`. 

## Map

`Map` on Javan kokoelmakehyksen toinen keskeinen rajapinta
`Collection`-rajapinnan rinnalla. `Map` määrittelee yleiset säännöt kaikille
hakurakenteille tarjoamalla tärkeimmät metodit avain-arvo-parien tallentamiseen
ja käsittelyyn. `Collection`-rajapinnan tapaan `Map`-rajapinta ei ota kantaa 
alkioiden järjestykseen tai sisältöön eikä edellytä sen toteuttavien luokkien
käyttävän mitään tiettyä tietorakennetta tiedon tallentamiseen.

Toisin kuin `Collection`, `Map` ei toteuta `Iterable`-rajapintaa, minkä 
vuoksi hakurakenteita ei voida iteroida esimerkiksi `for each` -silmukan avulla,
vaan alkioiden läpikäynti on tehtävä hieman hankalammin avainten tai arvojen 
kautta.

Tutustutaan nyt `Map`-rajapinnan tärkeimpiin metodeihin. Käytämme esimerkeissä
konkreettista `HashMap`-luokkaa, mutta kaikki esimerkeissä käytetyt metodit ovat
määritelty `Map`-rajapinnassa, joten ne toimivat kaikissa `Map`-toteutuksissa.

## Alkion lisääminen ja poistaminen

Alkioiden lisääminen onnistuu `put`- ja  `putIfAbsent`-metodeilla. Metodit
ottavat parametreina avaimen ja sitä vastaavan arvon. Jos avain on jo valmiiksi
tietorakenteessa, metodit palauttavat sitä vastaavan alkuperäisen arvon ennen
ylikirjoittamista. Jos avainta ei ole valmiiksi tietorakenteessa, metodit
palauttavat `null`.

```java
//-void main() {
Map<String, Integer> arvosanat = new HashMap<>();

// Lisää tai korvaa arvon.
arvosanat.put("Maija", 3);
arvosanat.put("Maija", 5); // Palauttaa 3 ja korvaa alkuperäisen.

// Lisää arvon vain, jos avainta ei ole vielä tietorakenteessa.
arvosanat.putIfAbsent("Joni", 1);
arvosanat.putIfAbsent("Joni", 0); // Palauttaa 1, mutta ei korvaa alkuperäistä.

IO.println(arvosanat);
//-}
```

Poistaminen onnistuu kokoelmien tapaan `remove`-metodilla, jolle annetaan
parametrina poistettava avain. Metodi palauttaa lisäämisen tapaan poistettavaa
avainta vastaavan arvon, jos sellainen tietorakenteessa on. Muussa tapauksessa
se palauttaa `null`.

```java
//-void main() {
Map<String, Integer> arvosanat = new HashMap<>();
arvosanat.put("Maija", 5);
arvosanat.put("Joni", 5);

// Poistaa avain-arvo-parin, jonka avain on "Joni".
arvosanat.remove("Joni");

IO.println(arvosanat);
//-}
```

## Arvon hakeminen avaimen avulla

Avainta vastaavan arvon hakemiseen voidaan käyttää `get` ja
`getOrDefault`-metodeja. Jos avainta ei löydy, `get` palauttaa `null`.
`getOrDefault`-metodille voi itse määrittää palautettavan oletusarvon.

```java
//-void main() {
Map<String, Integer> arvosanat = new HashMap<>();
arvosanat.put("Maija", 5);

// Arvo on 5.
IO.println("Maijan arvosana: " + arvosanat.get("Maija")); 

// Avainta ei ole, joten arvo on null.
IO.println("Jonin arvosana: " + arvosanat.get("Joni")); 

// Käytetään oletusarvoa 0.
IO.println("Jonin arvosana: " + arvosanat.getOrDefault("Joni", 0)); 
//-}
```

Voimme myös tarkistaa, sisältääkö tietorakenne tietyn avaimen tai arvon 
`containsKey` ja `containsValue` -metodeilla, jotka palauttavat totuusarvon 
`true` tai `false`.

```java
//-void main() {
Map<String, Integer> arvosanat = new HashMap<>();
arvosanat.put("Maija", 5);

IO.println(arvosanat.containsKey("Maija")); // true
IO.println(arvosanat.containsKey("Matti")); // false

IO.println(arvosanat.containsValue(5)); // true
IO.println(arvosanat.containsKey(0)); // false
//-}
```

## Alkioiden määrä

`Map`-rajapinta määrittelee `Collection`-rajapinnan tapaan myös `size` ja
`isEmpty` -metodit, joilla voimme tarkastella alkioiden lukumäärää tai sitä,
onko tietorakenne tyhjä.

```java
//-void main() {
Map<String, Integer> arvosanat = new HashMap<>();
arvosanat.put("Maija", 5);

IO.println("Alkioita: " + arvosanat.size()); // 1
IO.println("Tyhjä: " + arvosanat.isEmpty()); // false
//-}
```

## Alkioiden läpikäynti

`Map` ei toteuta `Iterable`-rajapintaa eikä ole siten suoraan iteroitavissa
`for each` -silmukalla, mutta se tarjoaa metodit `keySet`, `values` ja 
`entrySet`, jotka palauttavat avaimet, arvot tai näiden parit kokoelmina.

Huomaa, että `entrySet` palauttaa kokoelman `Map.Entry<K,V>`-tyypin olioista, 
jossa `K` ja `V` vastaavat tietorakenteen avaimen ja arvon tyyppejä.
`Map.Entry` on avain-arvo-pari, joka sisältää metodit `getKey` ja `getValue`. 

```java
//-void main() {
Map<String, Integer> arvosanat = new HashMap<>();
arvosanat.put("Maija", 3);
arvosanat.put("Matti", 4);

// Käydään läpi kaikki avaimet. Voimme avaimen perusteella hakea 
// myös sitä vastaavan arvon tulostettavaksi.
for (String avain : arvosanat.keySet()) {
  IO.println(avain + " : " + arvosanat.get(avain));
}

// Käydään läpi kaikki arvot. Arvon avulla emme pääse käsiksi 
// avaimeen, joten emme voi sitä tulostaa.
for (Integer arvo : arvosanat.values()) { 
  IO.println(arvo);
}

// Käydään läpi kaikki avain-arvo-parit.
for (Map.Entry<String, Integer> pari : arvosanat.entrySet()) { 
  IO.println(pari.getKey() + " : " + pari.getValue());
}
//-}
```

## Hajautustaulu

Ennen kuin tutustumme tarkemmin konkreettisiin Map-toteutuksiin, katsotaan ensin
yleisellä tasolla *hajautustaulun* (engl. *hash table*) toimintaperiaatetta.
Kyseessä on klassinen tietorakenteiden taustalla oleva logiikka, joka toimii
perustana useille Map-toteutuksille, kuten Javan `HashMap`- ja
`LinkedHashMap`-luokille.

Hajautustaulun toteutus perustuu taulukkoon, jota käytetään avain-arvo-parien
tallentamiseen. Menetelmän keskeinen idea on siinä, että tietoa ei tarvitse
etsiä selaamalla, vaan oikea sijainti lasketaan avaimen perusteella.

Kun tietorakenteeseen lisätään pari, sen paikka taulukossa määritetään
seuraavasti:

 1. Hajautusarvo: Avaimelle (key) lasketaan kokonaisluku hashCode-metodin avulla.
 2. Indeksi: Koska hajautusarvo voi olla valtava tai negatiivinen, se täytyy "leikata" taulukon kokoon sopivaksi.

Tämä tehdään tyypillisesti laskemalla hajautusarvon jakojäännös hajautustaulun
taustalla olevan taulukon koosta (kapasiteetti). Tästä luvusta otetaan
itseisarvo, joka on aina välillä [0..kapasiteetti-1].

```
indeksi = itseisarvo(hajautusarvo % kapasiteetti)
```

Koska mahdollisia hajautusarvoja on valtavasti, mutta taulukossa on vain
rajallinen määrä indeksejä, on mahdollista, että kaksi eri avainta päätyy samaan
indeksiin. Tätä kutsutaan törmäykseksi. Törmäysten hallintaan on kaksi
päästrategiaa: 

 1. Ketjutus (engl. Chaining): Tämä on muun muassa Javan `HashMap`-luokan
käyttämä tapa. Hajautustaulun jokainen indeksi on "ämpäri", joka sisältää
listan. Kaikki samaan indeksiin osuvat alkiot lisätään tähän listaan jonoon.

 2. Avoin hajautus (engl. Open Addressing): Indeksissä on tilaa vain yhdelle
    alkiolle. Jos paikka on varattu, etsitään seuraava vapaa paikka esimerkiksi
    siirtymällä taulukossa eteenpäin, kunnes tyhjä kohta löytyy.

Alkiota hakiessa lasketaan ensin indeksi samalla kaavalla kuin lisäyksessä.
Tämän jälkeiset vaiheet riippuvat strategiasta. Ketjutusmenetelmää käytettäessä
alkiota lähdetään etsimään indeksistä löytyvästä listasta. Avointa hajautusta
käytettäessä lähdetään käymään hajautustaulun taulukon indeksejä läpi, kunnes
etsitty avain (tai `null`-arvo) löytyy.

Törmäysten määrä vaikuttaa suoraan tietorakenteen suorituskykyyn. Hajautustaulun
lisäys-, poisto- ja hakuoperaatiot ovat hyvin nopeita. Niiden keskimääräinen
aikavaativuus on $O(1)$, sillä oikea indeksi saadaan suoraan yksinkertaisella
laskutoimituksella. Huonoimmassa tapauksessa kaikki alkiot päätyvät samaan
indeksiin, jolloin oikean alkion löytämiseksi joudutaan käymään koko
tietorakenne läpi, minkä vuoksi pahin tapaus on $O(n)$.

> [!HUOMAUTUS]
> Aikavaativuuksia käsitellään perusteellisemmin [Algoritmit 1
> -opintojaksolla](https://opinto-opas.jyu.fi/2025/fi/opintojakso/itka201/); tässä vain sivuamme niitä.
> Tämän opintojakson osalta riittää ymmärtää, että $O(1)$ tarkoittaa, että
> operaatio onnistuu vakioajassa, eli se ei riipu tietorakenteen koosta. $O(n)$
> tarkoittaa, että operaation vaatima aika kasvaa samassa suhteessa
> tietorakenteen kokoon. Jos esimerkiksi tietorakenteessa on 1000 alkiota,
> $O(n)$-operaatio vaatisi 1000 kertaa enemmän aikaa kuin $O(1)$-operaatio.

Jotta hajautustaulu pysyisi nopeana ($O(1)$), törmäykset on minimoitava. Tähän
vaikuttaa täyttöaste (engl. *load factor*). Jos taulukon kapasiteetti on liian
pieni suhteessa alkioiden määrään, taulukko tulee liian täyteen ja törmäykset
lisääntyvät. Kun täyttöaste ylittää tietyn rajan, hajautustaulu kasvatetaan --
yleensä tuplataan -- ja kaikki alkiot sijoitetaan uudelleen uuteen, isompaan
taulukkoon. Tämä operaatio on raskas, joten oikean alkukapasiteetin arviointi on
tärkeää.

Hajautustaulu toimii kuin varasto, jossa on monta säilytyslaatikkoa, joihin
voidaan laittaa kuinka monta esinettä tahansa. Kapasiteetti kuvastaa
säilytyslaatikoiden lukumäärää ja laatikot ovat hajautustaulun *indeksejä*.
Laatikot ovat tapa järjestellä esineitä niin, että löydämme haluamamme esineen
varastosta helpommin. Yksi laatikko voi olla vaatteita varten, toinen työkaluja,
ja kolmanteen laitetaan kaikki muut. Voimme yksinkertaistetusti ajatella, että
esimerkiksi kaikki työkalut saisivat hajautusfunktion tuloksena saman indeksin
ja päätyvät samaan laatikkoon. Etsiessämme vasaraa voimme heti katsoa työkalujen
laatikosta, mutta jos se sisältää suuren määrän esineitä, oikean työkalun
löytämiseen voi silti mennä aikaa.

## HashMap

`HashMap` on yleisimmin käytetty `Map`-rajapinnan toteuttava luokka.
`HashMap`-luokan toteutus perustuu edellä mainittuun hajautustauluun ja se
tarjoaa parhaan keskimääräisen suorituskyvyn perusoperaatioille. Alkioiden
hakeminen, lisääminen ja poistaminen avaimen perusteella onnistuu parhaimmillaan
vakioajassa $O(1)$. Kaikkien alkioiden läpikäyminen on kuitenkin
monimutkaisemman sisäisen tietorakenteen vuoksi hieman hitaampaa kuin listoissa.
`HashMap`-luokan suorituskykyerot tulevat paremmin esille, kun alkioita on hyvin
suuri määrä; jos alkioita on vähän, eroa esimerkiksi listaan ei juurikaan
huomaa.

`HashMap` ei takaa alkioiden järjestystä; alkioita läpi käydessä ne voivat olla 
missä järjestyksessä tahansa, ja järjestys voi muuttua, kun rakenteeseen 
lisätään uusia alkioita.

## LinkedHashMap

`LinkedHashMap` on `HashMap`-luokasta periytyvä luokka, joka ylläpitää 
sisäisesti hajautustaulun lisäksi linkitettyä listaa kaikista lisätyistä 
alkioista. Tämä mahdollistaa alkioiden **lisäysjärjestyksen** säilyttämisen, 
mutta lisätty tietorakenne vie hieman enemmän muistia.

```java
//-void main() {
Map<String, Integer> hashmap = new HashMap<>();
hashmap.put("Joni Virtanen", 20);
hashmap.put("Maija Meikäläinen", 10);
hashmap.put("Matti Korhonen", 5);

// Lisäysjärjestys ei säily.
for (String key : hashmap.keySet()) {
    IO.println(key + " : " + hashmap.get(key));
}

IO.println();

Map<String, Integer> linked = new LinkedHashMap<>();
linked.put("Joni Virtanen", 20);
linked.put("Maija Meikäläinen", 10);
linked.put("Matti Korhonen", 5);

// Lisäysjärjestys säilyy.
for (String key : linked.keySet()) {
    IO.println(key + " : " + linked.get(key));
}
//-}
```

`LinkedHashMap` sopii hyvin esimerkiksi verkkokaupan viimeksi katsottujen
tuotteiden tallentamiseen. Tuote voidaan hakea nopeasti avaimena toimivan
tuotetunnuksen perusteella, mutta samalla tuotteet säilyvät siinä järjestyksessä
kuin käyttäjä on niitä katsonut. Tämä tekee rakenteesta käytännöllisen silloin,
kun tarvitaan sekä nopeaa hakua että käyttäjälle näytettävää, luonnollista
järjestystä.

## TreeMap

`TreeMap` eroaa edellisistä siten, että se käyttää hajautustaulun sijaan
puurakennetta sisäisenä tietorakenteenaan. Se toteuttaa `SortedMap`- ja
`NavigableMap`-rajapinnat. `SortedMap` takaa, että avaimet ovat aina
**luonnollisessa järjestyksessä**, ja `NavigableMap` lisää tähän mahdollisuuden 
etsiä esimerkiksi lähintä avainta tietyn arvon ylä- tai alapuolelta. Muista
tässä osassa mainituista hakurakenteista poiketen `TreeMap` ei salli
`null`-arvoa avaimena, sillä sitä ei voitaisi vertailla muihin avaimiin
niiden järjestyksen selvittämiseksi.

`TreeMap` on puurakenteen vuoksi operaatioiltaan hitaampi kuin `HashMap`, mutta 
se mahdollistaa alkioiden järjestämisen avaimen perusteella. `TreeMap`-luokan 
operaatioiden aikavaativuus on $O(\log n)$.

```java
//-void main() {
Map<String, Integer> tree = new TreeMap<>();
tree.put("Olli", 100);
tree.put("Heikki", 200);
tree.put("Anna", 300);

// Tulostaa avaimen mukaisesti suuruusjärjestyksessä.
for (String key : tree.keySet()) {
    IO.println(key + " : " + tree.get(key));
}
//-}
```

`NavigableMap`-rajapinta tarjoaa myös useita metodeja, joilla voidaan hakea
avaimia tai pareja eri tavoin avainten järjestykseen perustuen. 

```java
//-void main() {
NavigableMap<String, Integer> tree = new TreeMap<>();
tree.put("B", 2);
tree.put("H", 3);
tree.put("A", 1);
tree.put("Q", 1);

// Tulostetaan pienin ja suurin avain.
IO.println("Pienin avain: " + tree.firstKey());
IO.println("Suurin avain: " + tree.lastKey()); 

// Tulostetaan annettua avainta lähin pienempi ja suurempi avain.
IO.println(tree.lowerKey("B")); 
IO.println(tree.higherKey("B"));

// Palauttaa koko tietorakenteen käänteisessä järjestyksessä.
IO.println(tree.descendingMap()); 
//-}
```

Lisäksi `TreeMap` mahdollistaa alipuiden muodostamisen `subMap`-metodilla.

```java
//-void main() {
NavigableMap<String, Integer> tree = new TreeMap<>();
tree.put("B", 2);
tree.put("H", 3);
tree.put("A", 1);

// Muodostetaan uusi hakurakenne alkioista, jotka ovat A-C välillä.
// Parametrien true-arvot kertovat, että myös A ja C otetaan mukaan.
Map<String, Integer> alipuu = tree.subMap("A", true, "C", true);
IO.println(alipuu);
//-}
```

Hyvä esimerkki `TreeMap`-rakenteen käyttökohteesta on aikaleimoihin perustuva
tapahtumien tallennus. Oletetaan, että järjestelmä kerää lokimerkintöjä, joissa
jokaisella tapahtumalla on tarkka aikaleima ja siihen liittyvä kuvaus. Tällöin
`TreeMap<LocalDateTime, Tapahtuma>` soveltuu rakenteeksi hyvin. Sen keskeinen
etu on avainten automaattinen järjestäminen: uudet tapahtumat sijoittuvat
suoraan oikeaan kohtaan, jolloin dataa voidaan käsitellä kronologisessa
järjestyksessä ilman erillistä lajittelua.

TreeMap mahdollistaa myös nopeat haut tietyltä aikaväliltä (subMap, headMap,
tailMap) sekä lähimmän arvon etsimisen. Esimerkiksi floorKey löytää annettua
hetkeä edeltävän (tai saman) aikaleiman, kun taas ceilingKey palauttaa seuraavan
(tai saman) aikaleiman. Kaikkien näiden hakumetodien aikavaativuus on $O(\log
n)$, mikä on huomattavasti tehokkaampaa kuin järjestämättömän tietorakenteen
läpikäynti.

`TreeMap` mahdollistaa myös tehokkaat aikavälihaut, jotka ovat tällaisessa
tilanteessa keskeisiä. Esimerkiksi voidaan hakea kaikki tapahtumat tietyn
ajanhetken jälkeen tai kahden aikaleiman väliltä käyttämällä `tailMap`, `headMap`
tai `subMap` -metodeja. Näiden operaatioiden aikavaativuus on $O(\log n)$, mikä tekee
niistä selvästi tehokkaampia kuin koko tietorakenteen läpikäynnin vaativat
ratkaisut. Lisäksi `TreeMap` tarjoaa metodeja, joilla voidaan löytää lähin
tapahtuma ennen tai jälkeen tietyn ajanhetken, mikä on tyypillinen tarve lokien
ja historiatietojen käsittelyssä.

Seuraavassa taulukossa verrataan TreeMap-rakennetta vaihtoehtoisiin
tietorakenteisiin aikajärjestystä vaativissa tilanteissa:

| Rakenne           | Etu                                                         | Haitta                                                                                             |
| :---------------- | :---------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| **HashMap**       | Yksittäisen avaimen haku on keskimäärin nopeampaa ($O(1)$). | Järjestys katoaa. Aikavälihaut vaatisivat kaikkien alkioiden läpikäynnin tai erillisen lajittelun. |
| **LinkedHashMap** | Säilyttää lisäysjärjestyksen.                               | Ei takaa aikajärjestystä, jos dataa ei syötetä kronologisesti.                                     |
| **PriorityQueue** | Nopea pääsy ääriarvoihin (min/max).                         | Ei tue tehokasta hakua mielivaltaisella avaimella tai aikavälillä.                                 |

Rakenteiden valinta riippuu siis tarpeesta: `HashMap` on yleensä paras, kun
tarvitaan mahdollisimman nopeaa avaimella hakua eikä järjestyksellä ole väliä.
`LinkedHashMap` sopii tilanteisiin, joissa lisäysjärjestys halutaan säilyttää.
`TreeMap` on näitä hitaampi, mutta oikea valinta silloin, kun tarvitaan
avainten jatkuvaa järjestystä sekä järjestykseen perustuvia hakuja.

---

<task>
  <task-title num="5.5">Sanat<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/5-5-sanat/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa5/tehtava5">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title num="5.6"><i class="bi bi-stars"></i>Varaukset<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/5-6-varaukset/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa5/tehtava6">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title num="5.7"><i class="bi bi-stars"></i>Hajautustaulu<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/5-7-hajautustaulu/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa5/tehtava7">Tee tehtävä TIMissä</a></task-link>
</task>
