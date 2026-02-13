# Joukko- ja jonorakenteet

> [!Osaamistavoitteet]
>
> - Tunnet Java-kielen yleisimmät valmiit tietorakenteet: `Set`, `Queue`, `Deque` ja niiden toteutukset `HashSet` ja `ArrayDeque`.
> - Osaat käyttää ym. tietorakenteita.
> - Ymmärrät ym. tietorakenteiden keskeisimmät operaatiot ja niiden aikakompleksisuudet. 
> - Ymmärrät, miksi oliot tarvitsevat `hashCode`-metodin.

## Joukkorakenteet

Joukot ovat kokoelmia, joiden kaikki alkiot ovat uniikkeja. Jos joukkoon
yritetään lisätä jonkin alkion duplikaatti, sen tila ei muutu millään tavalla.
Tämä ominaisuus tekee joukoista hyödyllisiä tietorakenteita, kun haluamme
varmistaa, että samaa tietoa ei löydy tietorakenteesta montaa kertaa.

Voisimme käyttää joukkoa esimerkiksi sähköpostilistan vastaanottajien
sähköpostiosoitteiden tallentamiseen. Tämä takaa, että yksi sähköpostiosoite voi
esiintyä vastaanottajien listassa korkeintaan yhden kerran, jolloin yhteen
sähköpostiosoitteeseen ei lähetetä koskaan saman viestin kopioita. 
Tietorakennetta käytetään usein myös matemaattisten joukkojen ja niiden 
operaatioiden mallintamiseen.

## Set

Javan kokoelmakehys sisältää rajapinnan `Set`, joka määrittelee perussäännöt
kaikille joukkorakenteille. `Set` periytyy `Collection`-rajapinnasta, joten
kaikki joukot toteuttavat myös sen lupaamat toiminnallisuudet. Voimme tämän
vuoksi esimerkiksi iteroida joukkoja helposti listojen tavoin.

Javassa yleisimmin käytetty joukon toteutus on `HashSet`, joka perustuu nimensä
mukaisesti hajautustauluun. Sisäisesti `HashSet`-käyttää alkioiden 
tallentamiseen `HashMap`-tietorakennetta, johon se tallentaa joukon alkiot 
avaimina. Hajautustaulutoteutuksen vuoksi erityisesti alkion lisääminen,
poistaminen ja hakeminen tietorakenteesta onnistuvat nopeasti vakioajassa. 
Hajautustaulu on kuitenkin tavallista taulukkoa monimutkaisempi tietorakenne, joten 
tietorakenteen läpikäyminen on taulukkoon perustuvaa `ArrayList`-luokkaa hieman
hitaampaa, mikä voi olla huomattavissa alkioiden määrän kasvaessa hyvin suureksi.

`Collection` ja `Map` -rajapintojen tapaan `Set`-rajapinta tai sen toteuttava 
luokka `HashSet` eivät takaa alkioiden olevan missään tietyssä järjestyksessä,
mutta tätä tarkoitusta varten on olemassa myös järjestyksen säilyttäviä
joukkorakenteita.

Katsotaan nyt, kuinka `HashSet`-tietorakenteen käyttö onnistuu `Set`-rajapinnan
kautta.

### Alkion lisääminen ja poistaminen

Alkioiden lisääminen ja poistaminen `HashSet`-rakenteeseen onnistuu kokoelmista
tuttuun tapaan. Lisääminen tapahtuu `add`-metodilla ja poistaminen taas tehdään 
`remove`-metodilla. Molemmat metodit palauttavat totuusarvon `true`, jos joukko
*muuttui* operaation seurauksena, eli jos operaatio oikeasti lisää tai poistaa
alkion.

Alkion lisääminen ja poistaminen tapahtuvat `HashSet`-tietorakenteessa 
hajautustaulun vuoksi keskimäärin vakioajassa *O(1)*.

```java
//-void main() {
Set<String> nimet = new HashSet<>();

// Alkioiden lisääminen.
nimet.add("Matti");
nimet.add("Maija");

// Lisääminen palauttaa false, koska alkio on jo joukossa.
IO.println(nimet.add("Matti"));

// Alkion poistaminen.
IO.println(nimet.remove("Maija"));
IO.println(nimet.remove("Maija")); // Palauttaa false, koska alkiota ei ole.
//-}
```

### Alkion etsiminen

Tietyn alkion löytäminen joukosta onnistuu helposti `contains`-metodilla, joka
palauttaa totuusarvon sen perusteella löytyykö alkio joukosta. 

`HashSet`-tietorakenteen ei hajautustaulun vuoksi tarvitse käydä koko
tietorakennetta läpi, joten etsiminen on myös keskimäärin vakioaikainen 
operaatio.

```java
//-void main() {
Set<String> nimet = new HashSet<>();
nimet.add("Matti");
nimet.add("Maija");

if (nimet.contains("Matti")) {
    IO.println("Matti löytyi joukosta!");
}
//-}
```

### Alkioiden määrä ja läpikäyminen

`Set` periytyy `Collection`-rajapinnasta, joten voimme käyttää kokoelmista
tuttuja metodeja `size` ja `isEmpty` alkioiden lukumäärän tarkastelemiseen. 
`Iterable`-rajapinnan ansiosta voimme myös iteroida joukkoja helpommin 
`for each` -silmukan avulla. 

Kaikkien alkioiden läpikäynnin aikavaativuus on myös joukoilla *O(n)*

```java
//-void main() {
Set<String> nimet = new HashSet<>();
nimet.add("Matti");
nimet.add("Maija");

for (String nimi : nimet) {
    IO.println(nimi);
}

IO.println();
IO.println("Joukossa on " + nimet.size() + " alkiota.");
IO.println("Onko tyhjä: " + nimet.isEmpty());
//-}
```

## Alkioiden järjestys

`HashSet` ei säilytä alkioiden järjestystä millään tavalla, mutta
hakurakenteiden tapaan myös joukoille on olemassa tietorakenteita, jotka
säilyttävät joko alkioiden lisäysjärjestyksen tai niiden luonnollisen
järjestyksen.

`LinkedHashSet` periytyy `HashSet`-luokasta ja ylläpitää `LinkedHashMap`-luokan
tapaan sisäistä linkitettyä listaa, joka säilyttää alkiot niiden
lisäysjärjestyksessä. `LinkedHashSet`-rakenteen perusoperaatiot ovat edelleen 
keskimääräiseltä aikavaativuudeltaan *O(1)*, mutta tietorakenne vaatii hieman 
enemmän muistia linkitetyn listan ylläpitämisen vuoksi.

```java
//-void main() {
LinkedHashSet<String> linked = new LinkedHashSet<>();
linked.add("Joni Virtanen");
linked.add("Maija Meikäläinen");
linked.add("Matti Korhonen");

// LinkedHashSet säilyttää alkioiden lisäysjärjestyksen.
IO.println(linked);
//-}
```

`TreeSet` toteuttaa `SortedSet`- ja `NavigableSet`-rajapinnat ja säilyttää
alkiot vastaavasti `TreeMap`-luokan tapaan niiden luonnollisessa järjestyksessä.
Se ei periydy `HashSet`-tietorakenteesta, sillä se käyttää alkioiden 
tallentamiseen hajautustaulun sijaan tasapainotettua puuta, jonka
perusoperaatiota ovat hieman hitaampia. Alkioiden lisääminen, poistaminen ja
hakeminen ovat aikavaativuudeltaan keskimäärin *O(log n)*.

```java
//-void main() {
TreeSet<String> tree = new TreeSet<>();
tree.add("Joni Virtanen");
tree.add("Maija Meikäläinen");
tree.add("Matti Korhonen");

// TreeSet lajittelee alkiot automaattisesti luonnolliseen järjestykseen.
IO.println(tree);
//-}
```

`SortedSet` ja `NavigableSet` -rajapinnat tarjoavat omat hyödylliset metodinsa 
järjestetyn joukon hallinnoimiseen. Toiminnot ovat hyvin samankaltaisia 
hakurakenteiden `SortedMap` ja `NavigableMap` -rajapintojen kanssa.

```java
//-void main() {
NavigableSet<Integer> tree = new TreeSet<>();
tree.add(1);
tree.add(2);
tree.add(5);
tree.add(4);
tree.add(3);

// Alkiot ovat suuruusjärjestyksessä.
IO.println(tree);

// Tulostetaan pienin ja suurin alkio.
IO.println("Pienin alkio: " + tree.first()); // 1
IO.println("Suurin alkio: " + tree.last());  // 5

// Tulostetaan annettua lukua lähin pienemi ja suurempi alkio.
IO.println(tree.lower(3)); // 2
IO.println(tree.higher(3)); // 4

// Palauttaa koko tietorakenteen käänteisessä järjestyksessä.
IO.println(tree.descendingSet()); 
//-}
```

`NavigableSet` mahdollistaa myös alijoukkojen muodostamisen `subSet`-metodilla.

```java
//-void main() {
NavigableSet<Integer> tree = new TreeSet<>();
tree.add(1);
tree.add(2);
tree.add(5);
tree.add(4);
tree.add(3);

// Muodostetaan uusi joukko alkioista, jotka ovat 3-5 välillä.
// Parametrien true-arvot kertovat, että myös 3 ja 5 otetaan mukaan joukkoon.
Set<Integer> alijoukko = tree.subSet(3, true, 5, true);
IO.println(alijoukko);
//-}
```

## Jonot ja pinot

Jonot ja pinot ovat listojen kaltaisia lineaarisia tietorakenteita. Nämä 
tietorakenteet ovat hyödyllisiä tilanteissa, joissa haluamme tarkastella 
erityisesti tietorakenteen alussa ja lopussa sijaitsevia alkioita. Jonot ja
pinot ovat käytännössä listoja, joissa alkioiden lisäys-, poisto- ja
hakuoperaatiot rajoittuvat tietorakenteen päätyihin, mutta näiden 
tietorakenteiden *käsitteet* ovat erittäin hyödyllisiä tietojenkäsittelyssä ja
niitä käytetäänkin tietojärjestelmissä hyvin usein.

Jonon lisäksi on myös olemassa kaksipäinen jono, joka yhdistää jonon ja pinon 
toiminnallisuudet ja sallii siten lisäys- ja poisto-operaatiot tietorakenteen
molempiin päätyihin. Javassa kaksipäinen jono sisältää myös monia
muita hyödyllisiä toiminnallisuuksia ja sitä itse asiassa käytetään Javassa sekä
jonon että pinon toteuttamiseen.

## Pino

Pino eli *stack* on tietorakenne, joka toimii *viimeisenä sisään, ensimmäisenä ulos* (engl.
*last in, first out*) -periaatteen mukaisesti. Alkioita voidaan lisätä vain 
pinon alkuun ja poistaminen kohdistuu aina ensimmäiseen alkioon.

Esimerkiksi tekstinkäsittelyohjelman *kumoa*-toiminto toimii kuin pino.
Tekstiin tehdyt muutokset lisätään aina pinon päällimmäiseksi ja
kumoamistoiminnon seurauksena ohjelma ottaa viimeisimmän muutoksen pinon päältä
ja kumoaa sen.

> [!HUOMAUTUS]
> Poikkeuksellisesti Java **ei** tarjoa `Stack`-rajapintaa pinon
> toteuttamista varten. Javan historiasta johtuen `Stack` on luokka, 
> jonka käyttöä ei enää suositella. Pinon toteuttamiseen käytetään nykyään 
> kaksipäistä jonoa, eli `Deque`-rajapinnan toteuttavaa `ArrayDeque`-luokkaa.

Pinon perusoperaatiot ovat `push`, `pop` ja `peek`. Javan `Deque` sisältää nämä 
metodit, joten käytämme niitä.

```java
//-void main() {
Deque<String> pino = new ArrayDeque<>();

// Lisää alkioita pinoon. Ei palauta mitään.
pino.push("A");
pino.push("B"); 
pino.push("C");

// Huomaa, että viimeisimpänä lisätty alkio tulostuu ensimmäisenä.
IO.println(pino);

// Palauttaa alkion "C", mutta ei poista sitä pinosta.
// Palauttaa null, jos pinossa ei ole yhtään alkiota.
IO.println(pino.peek());

// Palauttaa alkion "C" ja poistaa sen pinosta.
// Palauttaa null, jos pinossa ei ole yhtään alkiota.
IO.println(pino.pop());

IO.println(pino);
//-}
```

## Jono

Jono eli *queue* toimii *ensimmäisenä sisään, ensimmäisenä ulos* 
(engl. *first in, first out*) -periaatteen mukaisesti. Ensimmäisenä lisätty
alkio otetaan myös ensimmäiseksi pois.

Jonot toimivat kuten nimen perusteella voisi odottaa. Verkkoreitittimet ovat 
yksi hyvä esimerkki jonorakenteen käytöstä; ne tallentavat lähetettävät 
paketit jonoon, josta ne lähetetään eteenpäin samassa järjestyksessä, kuin ne 
lisättiin.

Javan `Queue`-rajapinta määrittelee jonorakenteiden yleiset toiminnallisuudet. 
Se laajentaa `Collection`-rajapintaa ja sisältää metodit, joilla alkioita
voidaan lisätä jonon loppuun ja poistaa tai tarkastella sen alusta.

`Queue`-rajapinta sisältää näistä kolmesta perustoiminnosta kahdet eri versiot,
jotka käsittelevät virheet eri tavalla. Metodit `add`, `remove` ja `element` 
aiheuttavat virhetilanteissa ohjelman pysäyttävän poikkeuksen, kun taas `offer`,
`poll` ja `peek` palauttavat näissä tilanteissa eri arvon. Käsittelemme 
poikkeuksia myöhemmin tällä kurssilla, joten tässä vaiheessa voimme keskittyä 
käyttämään `offer`, `poll` ja `peek` -metodeja, jotka toimivat ihan yhtä hyvin.

`ArrayDeque`-luokka toteuttaa `Queue`-rajapinnan, joten se sisältää kaikki sen
tarvitsemat metodit. Käytämme siis sitä toteuttamaan jonon.

```java
//-void main() {
Queue<String> jono = new ArrayDeque<>();

// Lisätään alkioita jonon loppuun. 
// 'offer' palauttaa true, jos alkion lisääminen onnistuu ja false, jos ei.
jono.offer("A");
jono.offer("B");

IO.println(jono); // [A, B]

// Katsotaan ensimmäistä alkiota poistamatta sitä jonosta.
// 'peek' palauttaa null, jos jonossa ei ole alkioita.
IO.println(jono.peek()); // "A"

// Poistetaan alkioita jonon alusta. Palauttaa alkion.
// 'poll' palauttaa null, jos jonossa ei ole alkioita.
IO.println(jono.poll()); // "A"
IO.println(jono.poll()); // "B"
IO.println(jono.poll()); // null
//-}
```

## Kaksipäinen jono

Kaksipäinen jono tunnetaan nimellä *deque*, joka on lyhenne tietorakenteen
englanninkielisestä nimestä *double ended queue*. Voisimme käyttää tätä
tietorakennetta mallintamaan esimerkiksi jonoa, jonka alkuun voisi joissain
tapauksissa lisätä alkion esimerkiksi sen tärkeyden mukaan.

`Deque`-rajapinta määrittelee kaikki kaksipäisten jonojen tarvitsemat
toiminnallisuudet. Käytännössä tämä tarkoittaa sitä, että se lupaa kaikki
jonon ja pinon tarvitsemat metodit sekä muutamia muita hyödyllisiä
toiminnallisuuksia, kuten mahdollisuuden alkioiden läpikäymiseen käänteisessä
järjestyksessä. Huomaa, että `Deque` sisältää tässä kohdassa mainittujen
metodien lisäksi myös pinon ja jonon yhteydessä mainitut metodit.

`Deque`-rajapinnan yleisimmin käytetty toteutusluokka on `ArrayDeque`, joka
nimensä mukaisesti käyttää taulukkoa sisäisenä tietorakenteenaan.
`Deque`-toteuttaa `Collection`-rajapinnan, joten kaikki kokoelmista tutut
metodit, kuten `size`, `isEmpty` ja `contains` ovat myös käytettävissä.

### Alkion lisääminen ja poistaminen

Myös `Deque` määrittelee kaksi eri tapaa lisätä ja poistaa alkioita: metodit, 
jotka heittävät poikkeuksen epäonnistuessaan, ja metodit, jotka palauttavat
näissä tilanteissa `null` tai `false`. 

Alkioita voidaan lisätä alkuun metodeilla `addFirst` ja `offerFirst` tai 
loppuun metodeilla `addLast` ja `offerLast`. Käytetään toistaiseksi
`offerFirst` ja `offerLast`-metodeja, sillä ne eivät aiheuta poikkeuksia 
epäonnistuessaan. 

```java
//-void main() {
Deque<Integer> luvut = new ArrayDeque<>();

// 'offerFirst' lisää alkion jonon alkuun, 'offerLast' lisää alkion jonon loppuun.
// Molemmat palauttavat false, jos lisääminen epäonnistuu.
luvut.offerFirst(2);
IO.println(luvut); // [2]
luvut.offerLast(3);
IO.println(luvut); // [2, 3]
luvut.offerFirst(1);
IO.println(luvut); // [1, 2, 3]
//-}
```

Poistaminen onnistuu vastaavasti kummastakin päästä. Metodit `removeFirst` ja
`removeLast` poistavat alkion tai heittävät poikkeuksen, jos jono on tyhjä.
Sen sijaan `pollFirst` ja `pollLast` palauttavat `null`-arvon, jos
poistettavaa ei löydy, joten voimme toistaiseksi käyttää ensisijaisesti näitä.

Lisäksi voimme kurkata alkioita poistamatta niitä
käyttämällä `peekFirst` tai `peekLast` -metodeja.

```java
//-void main() {
Deque<Integer> luvut = new ArrayDeque<>();
luvut.offerFirst(3);
luvut.offerFirst(2);
luvut.offerFirst(1);

IO.println(luvut); // Tulostaa [1, 2, 3]

// Kurkistetaan ensin ensimmäistä ja viimeistä arvoa.
IO.println(luvut.peekFirst()); // Tulostaa 1
IO.println(luvut.peekLast()); // Tulostaa 3

// Poistetaan ensimmäinen ja viimeinen arvo. Poistaminen palauttaa alkion, 
// jos poistaminen onnistuu. Muussa tapauksessa null.
luvut.pollFirst();
luvut.pollLast();

IO.println(luvut); // Tulostaa [2]
//-}
```

Sekä lisääminen että poistaminen molemmista päistä tapahtuu vakioajassa *O(1)*, 
sillä `ArrayDeque` on toteutettu kehämäisenä taulukkona, jossa pään ja hännän 
sijaintia seurataan indekseillä. Taulukon alkioita ei siis tarvitse lisäyksen
tai poiston yhteydessä käydä läpi tai siirrellä.

`ArrayDeque` tarjoaa myös `Collection`-rajapinnan metodin `remove`, jolla 
voidaan poistaa parametrina annettu alkio mistä tahansa kohdasta. Se toimii 
samalla tavalla kuin listasta poistaminen; käymällä koko listan läpi alkiota 
etsiessään.

### Alkioiden läpikäyminen

`ArrayDeque` toteuttaa `Iterable`-rajapinnan, joten voimme iteroida sen 
`for each` -silmukalla. Lisäksi sen metodi `descendingIterator` palauttaa
iteraattorin, jonka avulla tietorakenne voidaan käydä läpi käänteisessä
järjestyksessä. Alkioiden läpikäynnin aikavaativuus on *O(n)*, mikä on sama 
kuin tavallisella listalla.

```java
//-void main() {
Deque<Integer> luvut = new ArrayDeque<>();
luvut.offerFirst(3);
luvut.offerFirst(2);
luvut.offerFirst(1);

// Tavallinen läpikäynti.
for (Integer luku : luvut) {
    IO.println(luku);
}

// Käänteinen läpikäynti.
Iterator<Integer> it = luvut.descendingIterator();
while (it.hasNext()) {
    IO.println(it.next());
}
//-}
```

## Prioriteettijono

Prioriteettijono eli *priority queue* on jonon erikoistapaus, jonka toteutus 
on Javassa `PriorityQueue`-luokka. Tavallinen jono säilyttää alkiot niiden
lisäysjärjestyksessä, mutta prioriteettijono pitää huolen, että luonnollisessa
järjestyksessä *pienin* alkio tulee aina ensimmäisenä, kun pyydämme siltä
ensimmäistä alkiota.

```java
//-void main() {
PriorityQueue<Integer> luvut = new PriorityQueue<>();
luvut.offer(2);
luvut.offer(3);
luvut.offer(1);
luvut.offer(5);
luvut.offer(4);

// Huomaa, että tulostaessa tietorakenteen kaikki alkiot ne
// eivät ole luonnollisessa järjestyksessä.
IO.println(luvut);

// Prioriteettijono antaa aina "tärkeimmän" eli pienimmän alkion, kun
// piidämme siltä seuraavaa alkiota.
IO.println(luvut.poll()); // 1
IO.println(luvut.poll()); // 2
IO.println(luvut.poll()); // 3
IO.println(luvut.poll()); // 4
IO.println(luvut.poll()); // 5
//-}
```

`PriorityQueue`-luokan operaatioiden aikavaativuus poikkeaa perusjonoista, koska 
rakenne perustuu sisäisesti kekoon (engl. *heap*). Alkion lisäämisen ja 
poistamisen aikavaativuus on *O(log n)*. Pienimmän alkion pyytäminen on 
kuitenkin erittäin nopeaa ja tapahtuu vakioajassa *O(1)*.

---

<task>
  <task-title>Tehtävä 5.8: Joukot<points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/5-8-joukot/handout.md}} 

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa5/tehtava8">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title>Tehtävä 5.9: Tehtävälista<points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/5-9-tehtavalista/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa5/tehtava9">Tee tehtävä TIMissä</a></task-link>
</task>

<task>
  <task-title><i class="bi bi-stars jyu-gold"></i> Bonus: Tehtävä 5.10: Sulut<points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/5-10-sulut/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa5/tehtava10">Tee tehtävä TIMissä</a></task-link>
</task>
