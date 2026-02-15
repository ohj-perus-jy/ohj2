# Listarakenteet

`List`-rajapinta kuvaa kokoelmaa, jossa alkiot ovat tietyssä järjestyksessä ja
niihin voidaan viitata indeksin avulla. Tämä vastaa monella tapaa taulukkoa,
mutta tarjoaa huomattavasti joustavamman rajapinnan. Sivuhuomautus: Oikeampaa
olisi sanoa, että kyseessä on `List<E>`-rajapinta, jossa `E` on listan alkioiden
(*element*) tyyppi, mutta tässä yhteydessä jätämme geneerisyyden mainitsematta,
jotta kirjoitusasu pysyy yksinkertaisena. 

Kuvitellaan, että ohjelma tallentaa opiskelijoiden nimet siinä järjestyksessä
kuin he ovat ilmoittautuneet kurssille. Tässä tilanteessa järjestyksellä on
merkitystä, ja sama nimi voi esiintyä useammin kuin kerran, koska kahdella eri
henkilöllä voi olla sama nimi. 

```java
//-void main() {
List<String> opiskelijat = new ArrayList<>();
opiskelijat.add("Aino");
opiskelijat.add("Ville");
opiskelijat.add("Aino");

IO.println(opiskelijat.get(1)); // Ville
//-}
```

Listan käyttäminen tuntuu luontevalta, koska ajattelet tietoa nimenomaan jonona:
ensimmäinen, toinen, kolmas. `ArrayList` on tässä yleisin valinta, koska se
mahdollistaa nopean pääsyn alkioihin indeksin avulla. Tässä vaiheessa kurssia
voit ajatella, että `List` tarkoittaa käytännössä `ArrayList`‑luokkaa, ellei ole
erityistä syytä käyttää muuta toteutusta.

Listan alkioiden suhteellinen järjestys säilyy, vaikka välistä poistetaan
alkioita. Kun yksi alkio poistetaan, sitä seuraavat alkiot siirtyvät
automaattisesti yhden askeleen eteenpäin.

```java
//-void main() {
List<String> opiskelijat = new ArrayList<>();
opiskelijat.add("Aino");
opiskelijat.add("Ville");
opiskelijat.add("Aino");
opiskelijat.remove("Ville");
IO.println(opiskelijat);
//-}
```

Jokaisella alkiolla on listassa aina tietty paikka eli indeksi, ja tämän vuoksi
lista käydään läpi aina samassa järjestyksessä. Tämä tekee listasta sopivan
tilanteisiin, joissa järjestyksellä on merkitystä, järjestystä halutaan muokata
tai säilyttää, tai sama alkio saa esiintyä useita kertoja.

## Oma listarakenne

Seuraavaksi rakennetaan itse yksinkertainen dynaaminen listarakenne taulukon
päälle. Tämän tarkoituksena on havainnollistaa, miten `ArrayList` toimii
sisäisesti perusperiaatteiden tasolla. Toteutus ei ole täydellinen eikä kata
koko `List`‑rajapintaa, mutta riittää ymmärtämään keskeiset ideat.

Aloitetaan luomalla oma luokka `Lista<T>`, joka sisältää taulukon alkioiden
tallentamista varten. Alla oleva koodi on annettu valmiiksi.

```java,ignore
public class Lista<T> {
  private T[] alkiot;
  private int koko;

  @SuppressWarnings("unchecked")
    public Lista(int kapasiteetti) {
      this.alkiot = (T[]) new Object[kapasiteetti];
    this.koko = 0;
  }
}
```

Tämän seurauksena `alkiot`-taulukko alustuu niin, että se sisältää
`kapasiteetti`-parametrin verran `null`-arvoja. 

Tässä välissä on tarpeen selittää, miksi `@SuppressWarnings("unchecked")`
tarvitaan. Javassa ei voi suoraan luoda geneeristä `T`-tyyppistä taulukkoa.
Tyyppiparametri `T` on olemassa vain käännösaikana. Ajonaikaisesti Java ei
tiedä, mikä `T` oikeasti on. Tätä kutsutaan tyyppien häviämiseksi (type
erasure). Taulukot sen sijaan ovat ajonaikaisesti tyyppitietoisia; kun luot
taulukon, JVM tietää tarkasti, minkä tyyppisiä alkioita siihen saa tallentaa.
Tästä syntyy ristiriita: Java ei pysty luomaan taulukkoa tyypistä `T`, koska
`T`:n todellinen tyyppi ei ole ajonaikaisesti tiedossa. Siksi tämä ei ole
sallittua:

```java,ignore
new T[10]; // käännösvirhe 
```

Ainoa tapa kiertää rajoitus on luoda taulukko yleisimmästä mahdollisesta
viitetyypistä eli `Object`:sta ja pakottaa se tyyppimuunnoksella geneeriseksi.

```java,ignore
(T[]) new Object[kapasiteetti];
```

Kääntäjä tietää, että tämä muunnos ei ole täysin turvallinen. Se ei pysty
varmistamaan, että taulukkoon ei koskaan päädy väärän tyyppisiä alkioita. Varoituksen ohittava annotaatio
`@SuppressWarnings("unchecked")` ei tee koodista turvallisempaa eikä
vaarallisempaa. Se ainoastaan kertoo kääntäjälle, että tiedostat tämän
rajoituksen ja hyväksyt sen. Ilman annotaatiota ohjelma toimii täsmälleen
samalla tavalla, mutta kääntäjä tulostaa varoituksen.

<details><summary><i class="bi bi-stars jyu-gold"></i> Valinnaista lisätietoa: Missä tilanteessa tyyppimuunnos voisi aiheuttaa ongelmia?</summary>

Oletetaan, että luot `Lista<String>`-olion. Tällöin `T` on `String`. Sisäisesti
taustalla luotu taulukko alkioiden säilyttämistä varten on kuitenkin `Object[]`.
Niin kauan kuin listaa käytetään oikein, ongelmaa ei synny. Mutta Java sallii
tämän: 

```java,ignore
Lista<String> nimet = new Lista<>(10); // Lista, jossa T on String, pituus 10
Object o = nimet;
Lista<Integer> luvut = (Lista<Integer>) o; // unchecked cast
```

Kääntäjä varoittaa, mutta sallii koodin. Nyt molemmat viitteet osoittavat samaan
listaan.

Seuraavaksi lisätään listaan alkioita käyttäen `luvut`-viitettä:

```java,ignore
luvut.add(42); // oletetaan että add-metodi on toteutettu
```

Tämä onnistuu ajonaikaisesti, koska taulukko on oikeasti `Object[]` ja `Integer` on
`Object`. JVM ei havaitse mitään virhettä tässä vaiheessa. Ongelmia syntyy, kun
yrität hakea alkiota listasta:

```java,ignore
String s = nimet.get(0); // ClassCastException
```

Tässä vaiheessa JVM yrittää muuntaa alkion `String`-tyyppiseksi, koska lista on
`Lista<String>`. Koska alkio on kuitenkin `Integer`, syntyy `ClassCastException`.
Tämä on se tarkka syy, miksi kääntäjä varoittaa unchecked-muunnoksesta. Se ei
pysty todistamaan, että listan sisäinen tyyppisopimus säilyy ehjänä kaikissa
tilanteissa. On tärkeää huomata, että ongelma ei johdu listan käytöstä sinänsä,
vaan siitä, että geneerisen luokan tyyppitietoa kierretään eksplisiittisellä
tyyppimuunnoksella. Valmiit Javan kokoelmat ovat samassa tilanteessa, mutta
niiden rajapinnat ja toteutukset on suunniteltu niin, että tällaisia rikkomuksia
ei käytännössä tapahdu normaalissa käytössä.

</details>

## Listan perustoiminnot

Ensimmäisenä toteutetaan metodi `add(element)`, joka lisää alkion listan
loppuun. Emme vielä murehdi sitä, mitä tapahtuu, jos taulukko on täynnä. Jos taulukossa
on tilaa, lisääminen on yksinkertaista: asetetaan alkio taulukon seuraavaan vapaaseen
kohtaan ja kasvatetaan kokoa yhdellä. Jos taulukko on täynnä, palataan vain
`return`-lauseella tekemättä mitään -- korjataan tämä myöhemmin.

Koska emme voi vielä lukea alkioita listasta, emme voi ohjelmallisesti tarkistaa,
että lisäys onnistui. Voimme kuitenkin käyttää debuggeria. Kutsutaan 
`add`-metodia pääohjelmasta ja asetetaan sen jälkeen keskeytyskohta.

```java,ignore
void main() {
  Lista<String> lista = new Lista<>(10);
  lista.add("Aino");
  lista.add("Ville");
  lista.add("Matti");
  // Aseta keskeytyskohta loppusulun kohdalle
}
```

Käynnistä IDEAn debuggeri, ja tarkista `lista`-olion `alkiot`-taulukko. Sen pitäisi sisältää
lisätyt nimet alusta alkaen. IDEA ei näytä `null`-arvoja taulukon lopussa
oletuksena. Jos haluat, saat ne esille klikkaamalla `alkiot`-taulukon kohdalla
hiiren oikeaa painiketta, valitse "Customize data view", ja poista valinta
kohdasta "Hide null elements". 

<task>
  <task-title>Tehtävä 5.1: Listaan lisääminen. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/5-1-lista-1/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa5/tehtava1">Tee tehtävä TIMissä</a></task-link>
</task>

Tehdään seuraavaksi metodi `get(int index)`, joka palauttaa listan tietyn indeksin
alkion, sekä metodi `set(int index, T element)`, joka asettaa tietyn alkion tiettyyn
indeksiin. 

```java,ignore
public T get(int index) {
  if (index < 0 || index >= koko) {
    throw new IndexOutOfBoundsException("Indeksi " + index + " ei ole välillä 0.." + (koko - 1));
  }
  return alkiot[index];
}

public void set(int index, T element) {
  if (index < 0 || index >= koko) {
    throw new IndexOutOfBoundsException("Indeksi " + index + " ei ole välillä 0.." + (koko - 1));
  }
  alkiot[index] = element;
}
``` 

Käsittelemme poikkeuksia tarkemmin vasta myöhemmin, mutta tässä yhteydessä on
tarpeen mainita, mitä `throw new...`-rivi tarkoittaa. Listan indeksit alkavat
nollasta ja jatkuvat aina `koko - 1`:een asti. Jos yrität hakea alkiota
indeksillä, joka on pienempi kuin nolla tai suurempi tai yhtä suuri kuin `koko`,
kyseinen indeksi on listan ulkopuolella. Tämä on yleinen käytäntö Javan
kokoelmissa, ja varmasti sinulle myös tuttu aivan ohjelmoinnin alkeista asti.
Nyt pääsemme itse heittämään kyseisen poikkeuksen!


## Dynaamisuus

Vaikka Javassa `List`-rajapinta ei periaatteessa vaadi dynaamisuutta, eli
alkioiden lisäämistä ja poistamista, niin käytännössä listojen odotetaan tukevan
sitä. Tämä tarkoittaa, että listan koko voi muuttua ajon aikana. Tämä on
merkittävä ero taulukkoon verrattuna, jossa koko on kiinteä. 

Listan dynaamisuuden toteuttaminen taulukon päälle vaatii hieman lisälogiikkaa.
Jos taulukossa on tilaa, ts. koko on pienempi kuin taulukon pituus, niin uuden
alkion lisääminen on helppoa: asetetaan alkio taulukon seuraavaan vapaaseen
kohtaan ja kasvatetaan kokoa yhdellä. Jos taulukko on täynnä, yleinen käytäntö
on, että luodaan uusi, yleensä kaksinkertainen, taulukko, kopioidaan vanhan
taulukon alkiot uuteen taulukkoon, ja sitten lisätään uusi alkio uuteen
taulukkoon. Tämä prosessi varmistaa, että lista voi kasvaa tarpeen mukaan.

<task>
  <task-title>Tehtävä 5.2: Dynaaminen lista, osa 1. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/5-2-dynaaminen-lista-1/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa5/tehtava2">Tee tehtävä TIMissä</a></task-link>
</task>

Alkioiden poistaminen listasta on hieman monimutkaisempaa, koska poistettu alkio
jätetään tyhjäksi paikaksi taulukkoon. Yksi vaihtoehto olisi jättää kohta
`null`-arvoksi. Tämä aiheuttaisi kuitenkin ongelmia, alkioiden järjestys ja
indeksi eivät enää täsmäisi. 

Toinen vaihtoehto olisi kopioida kaikki alkiot paitsi poistettu uuteen
taulukkoon. Tämä olisi melko tehotonta, koska jokainen poisto vaatisi koko
taulukon kopioimisen.

Yleensä poistaminen toteutetaan siten, että poistettua alkiota seuraavat alkiot
siirretään yhden askeleen taaksepäin. Näin lista pysyy ehyenä, eikä uutta
taulukkoa tarvita. 

<task>
  <task-title>Tehtävä 5.3: Dynaaminen lista, osa 2. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/5-3-dynaaminen-lista-2/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa5/tehtava3">Tee tehtävä TIMissä</a></task-link>
</task>

Poistaminen voi tapahtua myös alkion yhtäsuuruuden perusteella. Tällöin
etsitään ensimmäinen alkio, joka on yhtä suuri kuin annettu alkio, ja poistetaan
se.

Jotta `remove(T element)`-metodi toimisi oikein, on tärkeää käyttää
`equals`-metodia yhtäsuuruuden tarkistamiseen. Tämä varmistaa, että vertailu
toimii oikein myös silloin, kun listassa on geneerisiä tyyppejä. Toteutetaan
tämä metodi seuraavaksi. Olemme tähän asti laittaneet listan alkioiksi lähinnä
lukuja ja merkkijonoja, mutta käyttäessämme geneeristä `T`-tyyppiä, metodi
toimii kaikilla olioilla, jotka toteuttavat `equals`-metodin. 

## Equals-metodi

Otetaan tässä yhteydessä pieni tangentti `equals`- ja `hashCode`-metodeista,
koska niiden oikea käyttö on olennaista kokoelmien kanssa työskennellessä.
Aloitetaan `equals`-metodista. 

Javassa `==`-operaattori toimii luotettavana sisällön vertailuna vain
primitiivityyppien kanssa. Tämä on tietysti aivan hyvä tapa vertailla vaikkapa
lukuja tai `String`-merkkijonoja. Olioviitteiden osalta `==`-operaattori
vertailee viitteitä. Esimerkiksi `Integer a = new Integer(42);` ja `Integer b =
new Integer(42);` eivät ole `a == b`, vaikka niiden sisällöt ovatkin samat.

`equals`-metodin tarkoitus on vertailla olioiden *sisältöä* eli sitä, ovatko ne
samat sovelluksen näkökulmasta.

Kaikki luokat perivät `equals`-metodin luokasta `Object`. Oletustoteutus
`Object.equals` käyttäytyy kuten `==`, eli se vertailee viitteitä. Siksi
sisältövertailu vaatii usein oman `equals`-toteutuksen.

`equals`-metodilla on selkeä sopimus, jota pitää noudattaa:
- Refleksiivisyys: `x.equals(x)` on aina `true`.
- Symmetrisyys: jos `x.equals(y)` on `true`, niin `y.equals(x)` on `true`.
- Transitiivisuus: jos `x.equals(y)` ja `y.equals(z)`, niin `x.equals(z)`.
- Johdonmukaisuus: useat kutsut samalla datalla antavat saman tuloksen.
- `x.equals(null)` on aina `false`.

Tyypillinen `equals`-toteutus etenee seuraavasti:
1. Jos viitteet ovat samat, palauta `true`.
2. Jos toinen on `null` tai tyyppi ei täsmää, palauta `false`.
3. Muunna tyyppi ja vertaile niitä kenttiä, jotka määrittelevät "saman".

Esimerkki luokasta, joka vertailee henkilön nimeä ja opiskelijanumeroa. Vain
siinä tilanteessa että molemmat kentät ovat yhtä suuret, olioiden katsotaan
olevan yhtä suuret.

```java
public class Opiskelija {
  private String nimi;
  private String opiskelijanumero;

  public Opiskelija(String nimi, String opiskelijanumero) {
    this.nimi = nimi;
    this.opiskelijanumero = opiskelijanumero;
  }

  @Override
  public boolean equals(Object toinen) {
    if (this == toinen) {
      return true;
    }
    if (toinen == null || getClass() != toinen.getClass()) {
      return false;
    }
    // Tämä tyyppimuunnos on nyt turvallinen
    Opiskelija toinenOpiskelija = (Opiskelija) toinen;
    return this.opiskelijanumero.equals(toinenOpiskelija.opiskelijanumero)
        && this.nimi.equals(toinenOpiskelija.nimi);
  }
}
```

Jos opiskelijanumero tai nimi voi olla `null`, käytä `Objects.equals(a, b)`,
joka toimii *null-turvallisesti*. 

```java
import java.util.Objects;

@Override
public boolean equals(Object toinen) {
  
  // ...
  
  Opiskelija toinenOpiskelija = (Opiskelija) toinen;
  return Objects.equals(this.opiskelijanumero, toinenOpiskelija.opiskelijanumero)
      && Objects.equals(this.nimi, toinenOpiskelija.nimi);
}
```

## HashCode-metodi

Kun luokka toteuttaa `equals`-metodin, on ehdottoman tärkeää toteuttaa myös
`hashCode`-metodi. Nämä kaksi kulkevat käsi kädessä, ja toisen unohtaminen
johtaa vaikeasti jäljitettäviin virheisiin. Jotta ymmärrämme miksi, on
sukellettava hetkeksi hajautustaulujen (kuten `HashSet` ja `HashMap`)
toimintaperiaatteeseen.

**Miten hajautus toimii?** Kuvittele kirjasto, jossa on tuhansia kirjoja. Jos haluat
löytää tietyn kirjan, et käy jokaista kirjaa läpi yksi kerrallaan alusta loppuun
(kuten lista tekisi). Sen sijaan katsot kirjastojärjestelmästä hyllyluokan
(esim. 800–899). Javassa `hashCode` toimii kuten tämä hyllyluokka:

 1. Lokerointi: `hashCode`-metodi tiivistää olion tiedot yhdeksi
    kokonaisluvuksi, jota kutsutaan *hajautusarvoksi*. Kokoelma käyttää tätä
lukua päättääkseen, mihin lokeroon olio tallennetaan.
 2. Nopeus: Kun etsit oliota kokoelmasta, Java laskee etsittävän olion
hajautusarvon ja hyppää suoraan oikeaan lokeroon.
 3. Tarkistus: Lopuksi Java käy läpi vain kyseisessä lokerossa olevat oliot
käyttäen `equals`-metodia varmistaakseen, onko etsitty olio todella siellä.

Javan kokoelmat luottavat sokeasti siihen, että jos `equals` sanoo, että kaksi
oliota ovat samat, niiden hajautusarvojen on oltava samat. 

 * Pakollinen suunta: `x.equals(y) == true` $\rightarrow$ `x.hashCode() == y.hashCode()`.

 * Ei-pakollinen suunta: Vaikka hajautusarvot olisivat samat, oliot voivat olla
eri sisältöisiä, jolloin syntyy niin sanottu *törmäys*. Tämä tarkoittaa, että ne
vain päätyvät samaan lokeroon, mutta `equals` erottelee ne kuitenkin toisistaan.

**Toteutus:** Helpoin ja turvallisin tapa toteuttaa `hashCode` on käyttää Javan
valmista apumetodia `Objects.hash`. On erittäin tärkeää, että `hashCode`-arvon
laskennassa käytetään tismalleen samoja kenttiä kuin `equals`-metodissa. Jos
`equals` vertailee nimeä ja opiskelijanumeroa, `hashCode` ei voi jättää toista
pois.

```java,ignore
@Override
public int hashCode() {
    // Luodaan tunnusluku (hash) samoista kentistä kuin equals-vertailussa
    return Objects.hash(nimi, opiskelijanumero);
}
```

<details><summary><i class="bi bi-stars jyu-gold"></i>Valinnaista lisätietoa: Älä muuta avaimia!</summary>

Hajauttavien rakenteiden kanssa on yksi vaaranpaikka: olioiden muuttaminen.

Jos lisäät olion `HashSet`-kokoelmaan ja sen jälkeen muutat olion kenttiä (esim.
opiskelijanumeroa), olion laskennallinen `hashCode` muuttuu. Olio on kuitenkin
edelleen alkuperäisen hajautusarvon mukaisessa lokerossa. Kun yrität etsiä sitä
uudella arvolla, Java katsoo uuteen lokeroon eikä löydä mitään.

Nyrkkisääntö: Jos käytät oliota `HashMap`-avaimena tai `HashSet`-jäsenenä, pyri
pitämään kyseinen olio muuttumattomana.

Vinkki: Jos käytät Javan uudempia record-tietueita, sinun ei tarvitse huolehtia
tästä. Java generoi automaattisesti oikeaoppiset `equals`- ja
`hashCode`-metodit, jotka ottavat huomioon kaikki tietueen kentät.

</details>

Vaikka juuri oman dynaamisen listan rakentelussa sinun ei tarvitsekaan itse
toteuttaa `equals`- tai `hashCode`-metodeja, on jatkon kannalta tärkeää ymmärtää
näiden metodien merkitys kokoelmien, kuten `HashSet` ja `HashMap`, taustalla. 

## Poistaminen alkion perusteella

Kuten edellä opimme, poistaminen alkion perusteella edellyttää, että listan
alkioiden tyypillä on toimiva `equals`-metodi. Tämän jälkeen poistaminen voidaan
tehdä luotettavasti käymällä lista läpi ja vertaamalla jokaista alkiota
haluttuun alkioon `equals`-metodilla. 

Jos listassa voi olla useita samanlaisia alkioita, tämä toteutus poistaa vain
ensimmäisen; muiden poistaminen vaatii uuden läpikäynnin.

<task>
  <task-title>Tehtävä 5.4: Dynaaminen lista, osa 3. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/5-4-dynaaminen-lista-3/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa5/tehtava4">Tee tehtävä TIMissä</a></task-link>
</task>
