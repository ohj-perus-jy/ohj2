# Kokoelmien käsittely: Stream API

> [!VAROITUS] 
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Ymmärrät deklaratiivisen ja imperatiivisen ohjelmoinnin eron kokoelmien
>   käsittelyssä
> - Tunnet Stream API:n keskeiset käsitteet (väli- ja lopetusoperaatiot)
> - Osaat käyttää striimejä kokoelmien suodattamiseen, muuntamiseen ja
>   lajitteluun
> - Osaat hyödyntää `Optional`-tyyppiä mahdollisesti puuttuvien arvojen
>   käsittelyssä
> - Tunnet perustietotyypeille tarkoitetut striimit, kuten `IntStream` ja
>   `DoubleStream`


Olemme toistaiseksi käyttäneet silmukoita kokoelmien käsittelyyn. Jos haluamme
esimerkiksi laskea listasta jokaisen parillisen alkion summan, kirjoitamme
ratkaisun tavallisesti näin:

```java
//-void main() {
List<Integer> numeroita = List.of(508, 18, 17, -148, 67, 42, -41);
int summa = 0;
for (int numero : numeroita) {
    if (numero % 2 == 0) {
      summa += numero;
    }
}
IO.println("Summa: " + summa);
//-}
```

Tätä ohjelmointitapaa kutsutaan *imperatiiviseksi*. Siinä kirjoitamme vaihe
vaiheelta, *mitä tietokoneen pitäisi tehdä* päästäkseen haluttuun
lopputulokseen.

Datan prosessoinnissa on kuitenkin usein selkeämpää kuvata, *millaisen*
lopputuloksen haluamme, sen sijaan että kertoisimme tarkat suoritusvaiheet. Tätä
kutsutaan *deklaratiiviseksi* ohjelmoinniksi. Javan Stream API tarjoaa tähän
työkalut hyödyntämällä lambdalausekkeita. Sen avulla voimme korvata yllä olevan
silmukan yhdellä rivillä:

```java
//-void main() {
List<Integer> numeroita = List.of(508, 18, 17, -148, 67, 42, -41);
int summa = numeroita.stream().filter(i -> i % 2 == 0).mapToInt(Integer::intValue).sum();
IO.println("Summa: " + summa);
//-}
```

## Striimien perustoiminta

Tarkastellaan yllä olevaa esimerkkiä tarkemmin. Huomaamme, että rivi koostuu
neljästä eri osasta:

```java,ignore
numeroita                       //    Käsiteltävä kokoelma
  .stream()                     // 1. Muunto striimiksi
  .filter(i -> i % 2 == 0)      // 2. Suodatus
  .mapToInt(Integer::intValue)  // 3. Muunnos perustietotyypiksi
  .sum();                       // 4. Arvon laskeminen
```

Käydään jokainen vaihe läpi.

**1. Kokoelman muuntaminen striimiksi**

Kaikilla Javan kokoelmilla on `stream()`-metodi, joka palauttaa
`Stream<T>`-tyyppisen olion eli striimin
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html)).
Striimiä voi ajatella liukuhihnana tai koneena, joka ottaa kokoelman ja tuottaa
siitä yhden alkion kerrallaan *tietovirtana*:

```bob
\   42   /
 \  67  /
  \-148/
   \17/           tietovirta -->
+---\/---+         
|        |      .---.       .---.  
| Stream |-----( 18  )-----( 508 )----->
|        |      `---'       `---' 
+--------+
```

**2. Suodatinfunktio `filter`**

Striimin `filter()` on metodi, joka suorittaa parametrina annetun
lambdalausekkeen jokaiselle alkiolle. Jos lauseke palauttaa alkiolle `true`,
alkio jatkaa eteenpäin tietovirrassa. Jos taas lauseke palauttaa `false`, alkio
poistetaan tietovirrasta.

Toisin sanoen, `filter()` on eräänlainen *suodatin*, joka lambdalausekkeen
perusteella joko antaa alkion mennä läpi tai suodattaa sen pois:

```bob
\   42   /
 \  67  /
  \-148/                tietovirta -->
   \  /                                            
+---\/---+             +--------+          
|        |    .---.    |        |      .---.       .---.  
| Stream |---( -148)---| filter |-----( 18  )-----( 508 )----->
|        |    `---'    |"i%2==0"|      `---'       `---' 
+--------+             +--------+ true -> eteenpäin
                  false    :     
                    |      :     
                    V      v     
                  pois   .---.   
                        ( 17  ) 
                         `---' 
```

**3. Muunnosfunktio `map`**

Striimien tärkeimpiä työkaluja ovat erilaiset *muunnokset* eli kuvaukset. Nämä
metodit alkavat yleensä sanalla `map`. Ne ottavat yhden alkion kerrallaan ja
muuttavat sen joksikin muuksi.

Esimerkiksi `mapToInt()` on muunnos, joka ottaa alkion ja muuttaa sen
`int`-tyyppiseksi luvuksi annetun funktion avulla. Tässä käytämme
`Integer::intValue` -funktioviitettä, joka muuttaa `Integer`-olion tavalliseksi
kokonaisluvuksi.

```bob
\   42   /
 \  67  /
  \-148/                tietovirta -->
   \  /                                            
+---\/---+             +--------+             +-------------------+      int
|        |    .---.    |        |    .---.    |                   |     .---.  
| Stream |---( -148)---| filter |---( 18  )---|   mapToInt        |----( 508 )----->
|        |    `---'    |"i%2==0"|    `---'    |"Integer::intValue"|     `---' 
+--------+             +--------+             +-------------------+    
```

Tarvitsemme tämän vaiheen siksi, että yleinen `Stream<T>` on geneerinen, ja
Javassa geneeristen tyyppien sisällä ei voi olla perustietotyyppejä (kuten
`int`). Kutsumalla `mapToInt()` striimi muuttuu `IntStream`-tyyppiseksi
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/IntStream.html)).
`IntStream` on optimoitu juuri numeroiden käsittelyyn ja se tarjoaa valmiita
tilastollisia metodeja, kuten `sum()`.

**4. Arvon laskeminen**

Striimin päätteeksi kutsumme aina jotain lopetusfunktiota. Se ottaa vastaan
tietovirran lopussa olevat alkiot ja palauttaa ne ohjelmalle halutussa muodossa
(esim. summana tai listana).

Tässä esimerkissä käytimme `sum()`-metodia, joka laskee luvut yhteen ja
palauttaa lopputuloksen yhtenä lukuna:

```bob
\   42   /
 \  67  /
  \-148/                tietovirta -->
   \  /                                            
+---\/---+   +--------+   +-------------------+      \+------+   
|        |   |        |   |                   |    508\      |  
| Stream |---| filter |---|   mapToInt        |--- 18  \ sum |---> 420
|        |   |"i%2==0"|   |"Integer::intValue"|  "-148"/     | 
+--------+   +--------+   +-------------------+    42 /+-----+ 
                                                     /
```

## Striimien käyttäminen

Kaikki, mitä on mahdollista tehdä striimeillä, voitaisiin kirjoittaa myös
tavallisina silmukoina. Kuitenkin yhdistämällä eri Stream API -funktioita saamme
usein hyvin ytimekkäitä ratkaisuja ongelmiin, jotka muuten vaatisivat useita
rivejä imperatiivista koodia.

### Striimien luominen

Yleisin tapa on luoda striimi suoraan kokoelmasta. Kaikilla Javan
`Collection`-rajapinnan toteuttavilla luokilla on `stream()`-metodi:

```java
//-void main() {
List<String> hedelmia = List.of("omena", "päärynä", "appelsiini");
Map<String, Integer> asukaslukuja = Map.of(
  "Helsinki", 695526,
  "Tampere", 263526,
  "Jyväskylä", 149967
);
Set<String> automerkkeja = Set.of("BMW", "Audi", "Hyundai", "Volvo");

Stream<String> hedelmiaStream = hedelmia.stream();
Stream<Map.Entry<String, Integer>> asukaslukujaStream = asukaslukuja.entrySet().stream();
Stream<String> automerkkejaStream = automerkkeja.stream();
//-
//-IO.println("Hedelmiä, jossa ei ole p-kirjainta: " + hedelmiaStream.filter(h -> !h.contains("p")).toList());
//-IO.println("Kaupunki, jossa on eniten asukkaita: " + asukaslukujaStream.max(Comparator.comparing(Map.Entry::getValue)).get().getKey());
//-IO.println("Automerkkien nimet yhdistettynä: " + automerkkejaStream.reduce("", (p, n) -> p + n));
//-}
```

Myös taulukoista voidaan luoda striimi `Arrays.stream`-metodilla:

```java
//-void main() {
int[] arvosanoja = {5, 1, 2, 3, 4, 5, 2, 5, 5, 4};
String[] opettajat = {"Denis", "Antti-Jussi", "Sami", "Karri"};

IntStream arvosanojaStream = Arrays.stream(arvosanoja);
Stream<String> opettajatStream = Arrays.stream(opettajat);
//-
//-IO.println("Arvosanojen keskiarvo: " + arvosanojaStream.average().getAsDouble());
//-IO.println("Opettaja, jolla on pisin etunimi: " + opettajatStream.max(Comparator.comparing(String::length)).get());
//-}
```

Mainittakoon tässä vaiheessa, että perustietotyypeille on olemassa omat
striimiluokat `IntStream`, `DoubleStream`, `LongStream`, jne. Nämä erikoisluokat
tarjoavat muun muassa erilaisia tilastofunktioita, kuten `max`, `min`, `average`
ja `sum`. Kokoelmien tapauksessa perustietotyypit kääritään kuitenkin aina
käärijäluokkaan, jolloin striimit ovat muotoa `Stream<Integer>`,
`Stream<Double>`, `Stream<Long>`. `Stream`-luokka tarjoaa aiemmin mainitut
`mapToInt`, `mapToDouble` ja vastaavia metodeja, jolla striimin voi muuttaa
perustietotyyppiversioon.

Voimme myös luoda striimejä, jotka tuottavat äärettömästi arvoja. Esimerkiksi
`Stream.generate` kutsuu annettua funktiota toistuvasti. Tällöin on käytettävä
alkioita rajoittavia metodeja, kuten `limit`, joka pysäyttää tietovirran halutun
määrän jälkeen:

```java
//-void main() {
Stream<String> risuaitoja = Stream.generate(() -> "#");
List<String> kymmenenRisuaitaa = risuaitoja.limit(10).toList();
IO.println(kymmenenRisuaitaa);
//-}
```

### Striimin välioperaatiot

Kaikki striimin metodit, jotka palauttavat uuden `Stream`-olion, ovat ns.
*välioperaatioita* (engl. *intermediate operations*). Niitä käytetään
tietovirrassa liikkuvien alkioiden muokkaamiseen ja suodattamiseen.

Kuvitellaan, että ylläpidämme kaupan ostostietoja. Haluamme selvittää syyskuun
ostosten keskihinnan.

```java,ignore
public class Ostotapahtuma {
  private double hinta;
  private LocalDate pvm;
}
```

Sen sijaan, että kirjoittaisimme silmukan ja `if`-ehtoja, rakennetaan haluttua
tulosta antavan striimin vaihe vaiheelta. Aloitetaan ensin ottamalla mukaan vain
syyskuun mukaan. Voimme käyttää `filter()`-metodia, joka suodattaa striimistä
alkioita annetun `boolean`-funktion perusteella:

```java
// FILE: main.java
void main() {
  List<Ostotapahtuma> ostotapahtumat = List.of(
    new Ostotapahtuma(100.0, LocalDate.of(2025, Month.JANUARY, 2)),
    new Ostotapahtuma(21.5, LocalDate.of(2025, Month.JULY, 3)),
    new Ostotapahtuma(12.0, LocalDate.of(2025, Month.SEPTEMBER, 1)),
    new Ostotapahtuma(5.25, LocalDate.of(2025, Month.SEPTEMBER, 12)),
    new Ostotapahtuma(245.0, LocalDate.of(2025, Month.SEPTEMBER, 21)),
    new Ostotapahtuma(342.0, LocalDate.of(2025, Month.OCTOBER, 2))
  );

  Stream<Ostotapahtuma> vainSyyskuu = 
          ostotapahtumat.stream()
                        .filter(o -> o.getPvm().getMonth() == Month.SEPTEMBER);

  vainSyyskuu.forEach(IO::println);
}
// FILE_END
// FILE: Ostotapahtuma.java
import java.time.LocalDate;

public class Ostotapahtuma {
  private double hinta;
  private LocalDate pvm;
//-
//-  public Ostotapahtuma(double hinta, LocalDate pvm) {
//-    this.hinta = hinta;
//-    this.pvm = pvm;
//-  }
//-
//-  public LocalDate getPvm() {
//-    return pvm;
//-  }
//-
//-  public double getHinta() {
//-    return hinta;
//-  }
//-
//-  @Override
//-  public String toString() {
//-    return pvm.toString() + ", " + hinta + " €";
//-  }
}
// FILE_END
```

Nyt kun meillä on vain syyskuun ostokset suodatettu mukaan, haluamme laskea
niiden keskiarvohinnan. Keskiarvo voidaan laskea vain luvuista, kun taas
ostotapahtuma on `Ostotapahtuma`-tyyppinen. Voimme käyttää striimin
`map`-metodia, joka muuntaa jokaisen alkion arvon toiseksi annetun
muunnosfunktion perusteella. Meidän muunnosfunktiossa riittää hakea
`Ostotapahtuma`-olion `hinta`-attribuutti, jolloin näin saadaan striimin
luvuista:

```java
// FILE: main.java
//-void main() {
//-  List<Ostotapahtuma> ostotapahtumat = List.of(
//-    new Ostotapahtuma(100.0, LocalDate.of(2025, Month.JANUARY, 2)),
//-    new Ostotapahtuma(21.5, LocalDate.of(2025, Month.JULY, 3)),
//-    new Ostotapahtuma(12.0, LocalDate.of(2025, Month.SEPTEMBER, 1)),
//-    new Ostotapahtuma(5.25, LocalDate.of(2025, Month.SEPTEMBER, 12)),
//-    new Ostotapahtuma(245.0, LocalDate.of(2025, Month.SEPTEMBER, 21)),
//-    new Ostotapahtuma(342.0, LocalDate.of(2025, Month.OCTOBER, 2))
//-  );
//-
  Stream<Double> syyskuunHinnat = 
          ostotapahtumat.stream()
                        .filter(o -> o.getPvm().getMonth() == Month.SEPTEMBER)
// HIGHLIGHT_GREEN_BEGIN
                        .map(o -> o.getHinta());
// HIGHLIGHT_GREEN_END

  syyskuunHinnat.forEach(IO::println);
//-}
// FILE_END
// FILE: Ostotapahtuma.java
import java.time.LocalDate;

public class Ostotapahtuma {
  private double hinta;
  private LocalDate pvm;
//-
//-  public Ostotapahtuma(double hinta, LocalDate pvm) {
//-    this.hinta = hinta;
//-    this.pvm = pvm;
//-  }
//-
//-  public LocalDate getPvm() {
//-    return pvm;
//-  }
//-
//-  public double getHinta() {
//-    return hinta;
//-  }
//-
//-  @Override
//-  public String toString() {
//-    return pvm.toString() + ", " + hinta + " €";
//-  }
}
// FILE_END
```

Huomaa, että tuloksena on `Stream<Double>`, eli käärijäluokkaan tallennettu
liukuluku. Jotta keskiarvon laskenta olisi helpompaa, muunnetaan `Double`-alkiot
perustyyppiinsä `mapToDouble()`-metodilla:

```java
// FILE: main.java
//-void main() {
//-  List<Ostotapahtuma> ostotapahtumat = List.of(
//-    new Ostotapahtuma(100.0, LocalDate.of(2025, Month.JANUARY, 2)),
//-    new Ostotapahtuma(21.5, LocalDate.of(2025, Month.JULY, 3)),
//-    new Ostotapahtuma(12.0, LocalDate.of(2025, Month.SEPTEMBER, 1)),
//-    new Ostotapahtuma(5.25, LocalDate.of(2025, Month.SEPTEMBER, 12)),
//-    new Ostotapahtuma(245.0, LocalDate.of(2025, Month.SEPTEMBER, 21)),
//-    new Ostotapahtuma(342.0, LocalDate.of(2025, Month.OCTOBER, 2))
//-  );
//-
// HIGHLIGHT_YELLOW_BEGIN
  DoubleStream syyskuunHinnat = 
// HIGHLIGHT_YELLOW_END
          ostotapahtumat.stream()
                        .filter(o -> o.getPvm().getMonth() == Month.SEPTEMBER)
                        .map(o -> o.getHinta())
// HIGHLIGHT_GREEN_BEGIN
                        .mapToDouble(d -> d.doubleValue());
// HIGHLIGHT_GREEN_END

  syyskuunHinnat.forEach(IO::println);
//-}
// FILE_END
// FILE: Ostotapahtuma.java
import java.time.LocalDate;

public class Ostotapahtuma {
  private double hinta;
  private LocalDate pvm;
//-
//-  public Ostotapahtuma(double hinta, LocalDate pvm) {
//-    this.hinta = hinta;
//-    this.pvm = pvm;
//-  }
//-
//-  public LocalDate getPvm() {
//-    return pvm;
//-  }
//-
//-  public double getHinta() {
//-    return hinta;
//-  }
//-
//-  @Override
//-  public String toString() {
//-    return pvm.toString() + ", " + hinta + " €";
//-  }
}
// FILE_END
```

`DoubleStream` sisältää valmiiksi `average()`-metodin, joka kerää ja palauttaa
striimissä olevien alkioiden keskiarvon:

```java
// FILE: main.java
//-void main() {
//-  List<Ostotapahtuma> ostotapahtumat = List.of(
//-    new Ostotapahtuma(100.0, LocalDate.of(2025, Month.JANUARY, 2)),
//-    new Ostotapahtuma(21.5, LocalDate.of(2025, Month.JULY, 3)),
//-    new Ostotapahtuma(12.0, LocalDate.of(2025, Month.SEPTEMBER, 1)),
//-    new Ostotapahtuma(5.25, LocalDate.of(2025, Month.SEPTEMBER, 12)),
//-    new Ostotapahtuma(245.0, LocalDate.of(2025, Month.SEPTEMBER, 21)),
//-    new Ostotapahtuma(342.0, LocalDate.of(2025, Month.OCTOBER, 2))
//-  );
//-
  OptionalDouble syyskuunKeskiarvo = 
          ostotapahtumat.stream()
                        .filter(o -> o.getPvm().getMonth() == Month.SEPTEMBER)
                        .map(o -> o.getHinta())
                        .mapToDouble(d -> d.doubleValue())
// HIGHLIGHT_GREEN_BEGIN
                        .average();
// HIGHLIGHT_GREEN_END

  IO.println(syyskuunKeskiarvo);
//-}
// FILE_END
// FILE: Ostotapahtuma.java
import java.time.LocalDate;

public class Ostotapahtuma {
  private double hinta;
  private LocalDate pvm;
//-
//-  public Ostotapahtuma(double hinta, LocalDate pvm) {
//-    this.hinta = hinta;
//-    this.pvm = pvm;
//-  }
//-
//-  public LocalDate getPvm() {
//-    return pvm;
//-  }
//-
//-  public double getHinta() {
//-    return hinta;
//-  }
//-
//-  @Override
//-  public String toString() {
//-    return pvm.toString() + ", " + hinta + " €";
//-  }
}
// FILE_END
```

Huomaa, että `average()` ei palauta suoraan `double`-arvoa, vaan
`OptionalDouble`-olion. Tämä johtuu siitä, että jos striimi on tyhjä
(esimerkiksi yhtään syyskuun ostosta ei löytyisi), keskiarvoa ei voida laskea.
Palaamme tähän hetken päästä alempana.

### Striimien lopetusoperaatiot

Kaikki striimin metodit, jotka palauttavat jotain muuta kuin uuden striimin ovat
*lopetusoperaatioita* (engl. *terminal operations*). Lopetusoperaatiot yleensä
käyvät läpi striimissä kaikki alkiot ja tuottavat arvon tai sivuvaikutuksen. 

Yleisin hyödyllinen lopetusoperaatio on striimin alkioiden kerääminen
kokoelmaksi. Esimerkiksi `toList()`-metodi kerää striimin alkiot listaksi ja
`toArray()`-metodi taulukoksi:

```java
//-void main() {
List<Integer> arvosanoja = List.of(1, 4, 5, -1, 0, 15, 2, 4, 5);

List<Integer> oikeitaArvosanoja = arvosanoja.stream()
                                    .filter(i -> 1 <= i && i <= 5)
                                    .sorted()
                                    .toList();

int[] oikeitaArvosanojaTaulu = arvosanoja.stream()
                                    .filter(i -> 1 <= i && i <= 5)
                                    .mapToInt(i -> i.intValue())
                                    .sorted()
                                    .toArray();

IO.println(oikeitaArvosanoja);
IO.println(Arrays.toString(oikeitaArvosanojaTaulu));
//-}
```

Huomaa, että lopetusoperaation jälkeen striimi yleensä lasketaan käytetyksi,
eikä jo käytettyä striimiä voi enää yleensä käyttää sen jälkeen. Jo käytetyn
striimin uudelleenkäyttäminen aiheuttaa yleensä virheen:

```java,ignore
//-void main() {
List<Integer> arvosanoja = List.of(1, 4, 5, -1, 0, 15, 2, 4, 5);

Stream<Integer> arvosanojaStream = arvosanoja.stream()
                                       .filter(i -> 1 <= i && i <= 5)
                                       .sorted();
// toList() lopettaa striimin
List<Integer> arvosanojaLista = arvosanojaStream.toList();

// VIRHE: yritetään käyttää jo käytettyä striimiä
long arvosanatLkm = arvosanojaStream.count();
//-}
```

```
java.lang.IllegalStateException: stream has already been operated upon or closed
```

Kuten kokoelmissa, myös striimeissä on `forEach()`-metodi, jonka avulla voi
suorittaa mielivaltaista koodia jokaiselle alkiolle:

```java
//-void main() {
IntStream.range(0, 10)      // Striimi kokonaisluvuista 0-9
  .filter(i -> i % 2 == 1)  // Otetaan vain parittomat kokonaisluvut
  .forEach(IO::println);    // Suoritetaan IO.println jokaiselle luvulle
//-}
```

Striimit sisältävät myös muutaman apufunktion yleisempiin ongelmiin. `min()` ja
`max()` -metodit keräävät striimin alkiot ja palauttavat alkioista suurimman.
Kummatkin metodit ottavat parametrina `Comparator`-vertailijafunktion.

```java
//-void main() {
List<String> opet = List.of("Denis", "Antti-Jussi", "Sami", "Karri");

Optional<String> pisinNimi = opet.stream().max(Comparator.comparing(String::length));
Optional<String> lyhinNimi = opet.stream().min(Comparator.comparing(String::length));

IO.println("Pisin: " + pisinNimi);
IO.println("Lyhin: " + lyhinNimi);
//-}
```

Huomaa, että `max()`, `min()` ja monet muut striimin lopetusfunktiot eivät
palauta arvoja suoraan, vaan `Optional<T>`-olion
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs//api/java.base/java/util/Optional.html)).
Nimensä mukaan tällainen olio kuvastaa arvon mahdollista puuttumista.
Esimerkiksi, jos striimissä ei ole yhtään alkiota tai jos lopetusfunktio ei voi
muuten laskea arvoa, se palauttaa `Optional.empty`-arvon kuvastamaan laskennan
epäonnistumista:

```java
//-void main() {
List<String> opet = List.of("Denis", "Antti-Jussi", "Sami", "Karri");

Optional<String> pisinNimi = opet.stream()
                    .filter(s -> s.startsWith("V"))
                    .max(Comparator.comparing(String::length));

IO.println("Pisin: " + pisinNimi);
//-}
```

Ennen kuin palautettua arvoa voi käyttää, tulee ensin tarkistaa, sisältääkö
`Optional<T>`-olio tuloksen. Tämä onnistuu esimerkiksi `isPresent()`-metodilla.
Kun tiedetään, että arvo on olemassa, se voidaan hakea `get()`-metodilla:

```java
//-void main() {
List<String> opet = List.of("Denis", "Antti-Jussi", "Sami", "Karri");

Optional<String> pisinNimi = opet.stream().max(Comparator.comparing(String::length));

if (pisinNimi.isPresent()) {
  String nimi = pisinNimi.get();

  IO.println("Pisin: " + nimi);
} else {
  IO.println("Annetuilla ehdoilla ei löytynyt yhtään nimeä");
}
//-}
```

Mainittakoon, että `Optional<T>`-tyyppi sisältää joukon muita apufunktioita,
joilla voi välttyä ylimääräisiltä `if`-rakenteilta.

Palataan vielä hetkeksi striimeihin. Striimit soveltuvat kätevästi arvojen
etsimiseen kokoelmista; `findFirst()`-metodi palauttaa ensimmäisen alkion, joka
pääsee "tietovirran loppuun" asti. Esimerkiksi, jos haluaisimme löytää
varastosovelluksesta ostotapahtuman, joka oli tehty syyskuussa ja ylittänyt
hinnaltaan 100 €:

```java
// FILE: main.java
//-void main() {
List<Ostotapahtuma> ostotapahtumat = List.of(
  new Ostotapahtuma(100.0, LocalDate.of(2025, Month.JANUARY, 2)),
  new Ostotapahtuma(21.5, LocalDate.of(2025, Month.JULY, 3)),
  new Ostotapahtuma(12.0, LocalDate.of(2025, Month.SEPTEMBER, 1)),
  new Ostotapahtuma(5.25, LocalDate.of(2025, Month.SEPTEMBER, 12)),
  new Ostotapahtuma(245.0, LocalDate.of(2025, Month.SEPTEMBER, 21)),
  new Ostotapahtuma(342.0, LocalDate.of(2025, Month.OCTOBER, 2))
);
 
Optional<Ostotapahtuma> tapahtuma = 
                  ostotapahtumat.stream()
                      .filter(o -> o.getPvm().getMonth() == Month.SEPTEMBER)
                      .filter(o -> o.getHinta() > 100.0)
                      .findFirst();

if (tapahtuma.isPresent()) {
  IO.println(tapahtuma.get());
} else {
  IO.println("Tapahtumaa ei löytynyt");
}

//-}
// FILE_END
// FILE: Ostotapahtuma.java
import java.time.LocalDate;

public class Ostotapahtuma {
  private double hinta;
  private LocalDate pvm;
//-
//-  public Ostotapahtuma(double hinta, LocalDate pvm) {
//-    this.hinta = hinta;
//-    this.pvm = pvm;
//-  }
//-
//-  public LocalDate getPvm() {
//-    return pvm;
//-  }
//-
//-  public double getHinta() {
//-    return hinta;
//-  }
//-
//-  @Override
//-  public String toString() {
//-    return pvm.toString() + ", " + hinta + " €";
//-  }
}
// FILE_END
```

Lopuksi, striimeillä on myös joitain tilastoihin liittyviä operaatioita.
Esimerkiksi aiemmin koodissa mainittu `count()`-metodi palauttaa kokonaislukuna,
kuinka monta alkiota striimissä on. Lisäksi perustietotyypeille tarkoitetuissa
striimeissä `IntStream`, `DoubleStream` ja `LongStream` löytyy muun muassa
seuraavia tilastometodeja:

- `sum()` - summaa luvut yhteen
- `min()`/`max()` - etsii pienimmän/suurimman luvun
- `average()` - laskee lukujen keskiarvon
- `summaryStatistics()` - laskee kerrallaan summan, suurimman, pienimmän luvut
  ja keskiarvon


```java
//-void main() {
IntStream lukuja = new Random().ints(20, 0, 100);
IO.println(lukuja.summaryStatistics());
//-}
```

<task>
  <task-title>Tehtävä 6.3: Musiikkilista <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/6-3-musiikkilista/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa6/tehtava3">Tee tehtävä TIMissa</a></task-link>
</task>

<task>
  <task-title>Tehtävä 6.4: Keskiarvo raja-arvoilla <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/6-4-sademaara/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa6/tehtava4">Tee tehtävä TIMissa</a></task-link>
</task>