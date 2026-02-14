# Kokoelmien käsittely: Stream API

> [!VAROITUS]
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Ainakin map, filter, reduce
> - lambda-lausekkeiden käyttö Stream API:ssa
> - `Stream`, `IntStream`, ero iteraattoreihin


Olemme toistaiseksi käyttäneet silmukoita datan käsittelyyn.
Jos haluaisimme esimerkiksi laskea listan jokaisen parillisen alkion summan,
kirjoittaisimme sen tavallisesti näin:

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

Tällaista ohjelmointitapaa kutsutaan *imperatiiviseksi*, eli kirjoitamme
koodiin, mitä tietokoneen pitäisi tehdä vaihe vaiheelta 
päästäkseen haluttuun lopputulokseen.

Etenkin datan prosessoinnissa on useimmin helpommin käsitellä data
*deklaratiivisesti* eli kirjoittamalla, millaisen lopputuloksen halutaan.
Javan Stream API tarjoaa deklaratiivisen tavan käsitellä kokoelmia ja
tietovirtoja lambdalausekkeiden avulla. 
Sen avulla yllä oleva silmukka voidaan korvata yhdellä rivillä:

```java
//-void main() {
List<Integer> numeroita = List.of(508, 18, 17, -148, 67, 42, -41);
int summa = numeroita.stream().filter(i -> i % 2 == 0).mapToInt(i -> i.intValue()).sum();
IO.println("Summa: " + summa);
//-}
```

## Striimien perustoiminta

Tarkastellaan yllä olevaa esimerkkiä tarkemmin.
Huomaamme ensin, että yksi rivi koostuu kolmesta metodikutsusta:

```java,ignore
numeroita                       // Käsiteltävä lista
  .stream()                     // 1.
  .filter(i -> i % 2 == 0)      // 2.
  .mapToInt(i -> i.intValue())  // 3.
  .sum();                       // 4.
```

Tarkastellaan jokainen vaihe kerrallaan.

**1. Kokoelman muuntaminen striimiksi**

Aivan alkuun muunnamme numerolistan `Steam<T>`-tyyppiseksi olioksi eli
striimiksi ([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/Stream.html)).
Striimin voi ajatella ikään kuin koneena, joka
ottaa kokoelman ja tuottaa yhden alkion kerrallaan *tietovirtana*:

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

Striimin `filter()` on metodi, joka
suorittaa parametrina annetun lambdalausekkeen jokaiselle alkiolle.
Jos lauseke palauttaa alkiolle `true`, alkio jatkaa eteenpäin tietovirrassa.
Jos taas lauseke palauttaa `false`, alkio poistetaan tietovirrasta.

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

**3. Käsittelijäfunktio `map`**

Striimien tärkein työkalu ovat erilaiset *käsittelijät*, jotka ovat yksittäisiä
alkioita käsiteltäviä funktioita. 
Käsittelijäfunktio alkaavat yleensä nimellä `map`, kuten `mapToInt()`.
Käsittelijät ottavat yhden alkion kerrallaan ja voivat tuottaa
yhden tai useamman uuden alkion tietovirtaan.
Voit ajatella käsittelijät ikään kuin koneina, jotka ottavat sisään alkioita
tietovirrasta ja tuottaavat tietovirtaan uusia alkioita.

Esimerkiksi `mapToInt()` on käsittelijä, joka ottaa alkion, korvaa alkion
kokonaisluvulla annetun lambdalausekkeen avulla ja tuottaa tietovirtaan
tuotetun kokonaisluvun alkuperäisen alkion sijaan:

```bob
\   42   /
 \  67  /
  \-148/                tietovirta -->
   \  /                                            
+---\/---+             +--------+             +--------------+      int
|        |    .---.    |        |    .---.    |              |     .---.  
| Stream |---( -148)---| filter |---( 18  )---|   mapToInt   |----( 508 )----->
|        |    `---'    |"i%2==0"|    `---'    |"i.intValue()"|     `---' 
+--------+             +--------+             +--------------+    
```

Tässä tapauksessa `i.intValue()` muuttaa `Integer`-tyyppisen käärijäluokan 
olion tavalliseksi `int`-tyyppiseksi kokonaisluvuksi.
Tämä muunnos tarvitaan, koska yleinen `Stream<T>` on geneerinen luokka,
ja Javassa geneeristen luokkien tyyppiparametrina ei voi olla perustietotyyppi.

Samalla `mapToInt` muuttaa striimin `IntStream`-tyyppiseksi striimiksi
([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/stream/IntStream.html)).
`IntStream` sopii erityisesti kokonaislukujen käsittelyyn paremmin, sillä se
sisältää kokonaislukujen kanssa yhteensopivia kerääjiä.

**4. Kerjääjäfunktio**

Striimien lopuksi kutsutaan yleensä jokin *kerääjäfunktio*, joka
ottaa vastaan striimin lopussa olevat alkiot ja palauttaa ne ohjelmalle.
Kerääjäfunktiot voidaan ajatella koneina, jotka ottavat vastaan
tietovirran loppuun tulevia alkioita ja "pakkaavat" alkiot ohjelmoijalle
sopivaan muotoon.

Tässä esimerkissä käytämme `sum()`-kerääjää, joka ottaa kokonaisluvut
ja palauttaa niiden summan:

```bob
\   42   /
 \  67  /
  \-148/                tietovirta -->
   \  /                                            
+---\/---+   +--------+   +--------------+      \+------+   
|        |   |        |   |              |    508\      |  
| Stream |---| filter |---|   mapToInt   |--- 18  \ sum |---> 420
|        |   |"i%2==0"|   |"i.intValue()"|  "-148"/     | 
+--------+   +--------+   +--------------+    42 /+-----+ 
                                                /
```

## Striimien käyttäminen

Striimit tarjoavat vaihtoehtoisen tavan käsitellä kokoelmia ja dataa.
Kaikki, mitä on mahdollista tehdä striimeillä on myös mahdollista
kirjoittaa tavallisina silmukkoina.
Huomaamme kuitenkin, että yhdistämällä Stream API -funktioita voidaan saada
hyvin ytimekkäitä ratkaisua sellaisiin ongelmiin, joiden ratkaisu olisi
vaatinut useita rivejä koodia.

### Striimien luominen


Yleisin striimien käyttötapa on kokoelmien käsittely; kaikilla kokoelmilla
on `steam()`-metodi, joka palauttaa kokoelmaa käsittelevän striimin.

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

Stream-olioita voidaan kuitenkin luoda hyvin monipuolisesti, eikä se rajoitu
vain kokoelmiin.
Esimerkiksi taulukoista voidaan luoda striimi `Arrays.stream`-metodilla:

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
striimiluokat `IntStream`, `DoubleStream`, `LongStream`, jne. 
Nämä erikoisluokat tarjoavat muun muassa erilaisia tilastofunktioita, kuten
`max`, `min`, `average` ja `sum`.
Kokoelmien tapauksessa perustietotyypit kääritään kuitenkin aina käärijäluokkaan,
jolloin striimit ovat muotoa `Stream<Integer>`, `Stream<Double>`,
`Stream<Long>`. `Stream`-luokka tarjoaa aiemmin mainitut `mapToString`,
`mapToDouble` ja vastaavia metodeja, jolla striimin voi muuttaa
perustietotyyppiversioon.

On myös mahdollista luoda striimejä, jotka tuottavat äärettömästi arvoja.
`Stream.generate` kutsuu jatkuvasti parametrina annettua funktiota ja tuottaa
sen arvoja tietovirtaan. Äärettömien striimien tapauksessa on käytettävä
alkioita rajoittavia metodeja, kuten `limit`, joka päästää läpi vain annetun
määrän ensimmäistä alkiota:

```java
//-void main() {
Stream<String> risuaitoja = Stream.generate(() -> "#");
List<String> kymmenenRisuaitaa = risuaitoja.limit(10).toList();
IO.println(kymmenenRisuaitaa);
//-}
```

### Striimin välioperaatiot

Kaikki striimin metodit, jotka palauttavat uuden `Stream`-oliot ovat
ns. *välioperaatioita*. Esimerkiksi yllä mainittu suodatus ja käsittely ovat
välioperaatioita, jotka muokkaavat tietovirrassa liikkuvia alkioita.

Oletetaan, että teemme kaupan ostos- ja varastohallintajärjestelmää.
Käyttäjät voivat ostaa erilaisia tuotteita eri päivämäärinä. 
Haluamme laskea erilaisia tilastoja kaupan hallinnolle.

Käyttäjien ostoksia mallinetaan ostotapahtumina, jotka sisältävät yhteenvetona
ostotapahtuman hinnan ja ostopäivämäärän:


```java
public class Ostotapahtuma {
  private double hinta;
  private LocalDate pvm;
}
```

Haluaisimme selvittää ostosten keskimääräistä hintaa syyskuun aikana.

Sen sijaan, että kirjoittaisimme silmukan ja `if`-ehtoja, voimme käyttää
striimeja ja välioperaatoita. Ensiksi, haluamme keskittyä vain syyskuun
osototapahtumiin. Tätä varten voimme käyttää `filter()`-metodia, joka suodattaa
striimistä alkioita annetun `boolean`-funktion perusteella:

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
ostotapahtuma on `Ostotapahtuma`-tyyppinen.
Voimme käyttää striimin `map`-metodia, joka muuntaa jokaisen alkion arvon
toiseksi annetun muunnosfunktion perusteella.
Meidän muunnosfunktiossa riittää hakea `Ostotapahtuma`-olion
`hinta`-attribuutti, jolloin näin saadaan striimin luvuista:

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
liukuluku. Jotta keskiarvon laskenta olisi helpompaa, muunnetaan 
`Double`-alkiot perustyyppiinsä `mapToDouble()`-metodilla:

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

`DoubleStream` sisältää valmiiksi `average()`-metodin, joka kerää
ja palauttaa striimissä olevien alkioiden keskiarvon:

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

Huomaa, että `average()` on striimiä lopettava funktio ja että se palauttaa
`OptionalDouble`-tyyppisen arvon tavallisen `double`-arvon sijaan. Palaamme
tähän hetken päästä alempana.

### Striimien lopetusoperaatiot

Kaikki striimin metodit, jotka palauttavat jotain muuta kuin
uuden striimit ovat *lopetusoperaatioita*. 
Lopetusoperaatiot yleensä käyvät läpi striimissa kaikki alkiot ja tuottavat
arvon tai sivuvaikutuksen. 

Yleisin hyödyllinen lopetusoperaatio on striimin alkioiden kerääminen
kokoelmaksi. Esimerkiksi `toList()`-metodi kerää striimin alkiot listaksi
ja `toArray()`-metodi taulukoksi:

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

Huomaa, että lopetusoperaation jälkeen striimi yleensä lasketaan
käytetyksi, eikä jo käytettyä striimiä voi enää yleensä käyttää sen jälkeen.
Jo käytetyn striimin uudelleenkäyttäminen aiheuttaa yleensä virheen:

```java,ignore
//-void main() {
List<Integer> arvosanoja = List.of(1, 4, 5, -1, 0, 15, 2, 4, 5);

Stream<Integer> arvosanojaStream = arvosanoja.stream()
                                       .filter(i -> 1 <= i && i <= 5)
                                       .sorted();
// toList() lopettaa striimin
List<Integer> arvosanojaLista = arvosanojaStream.toList();

// VIRHE: yritetään käyttää jo käytettyä striimia
long arvosanatLkm = arvosanojaStream.count();
//-}
```

```
java.lang.IllegalStateException: stream has already been operated upon or closed
```

Kuten kokoelmissa, myös striimeissä on `forEach()`-metodi, jonka avulla
voi suorittaa mielivaltaista koodia jokaiselle alkiolle:

```java
//-void main() {
IntStream.range(0, 10)      // Striimi kokonaisluvuista 0-9
  .filter(i -> i % 2 == 1)  // Otetaan vain parittomat kokonaisluvut
  .forEach(IO::println);    // Suoritetaan IO.println jokaiselle luvulle
//-}
```

Striimit sisältävät myös muutaman apufunktion yleisempiin ongelmiin.
`min()` ja `max()` -metodit keräävät striimin alkiot ja palauttavat
alkioista suurimman. Kummatkin metodit ottavat parametrina `Comparator`-vertailijafunktion.

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
palauta arvoja suoraan, vaan `Optional<T>`-olion ([JavaDoc](https://docs.oracle.com/en/java/javase/25/docs//api/java.base/java/util/Optional.html)).
Nimensä mukaan tällainen olio kuvastaa arvon mahdollista puuttumista.
Esimerkiksi, jos striimissä ei ole yhtään alkiota tai jos lopetusfunktio
ei voi muuten laskea arvoa, se palauttaa `Optional.empty`-arvon kuvastamaan
laskennan epäonnistumista:

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
etsimiseen kokoelmista; `findFirst()`-metodi palauttaa ensimmäisen alkion,
joka pääsee "tietovirtaan loppuun" asti.
Esimerkiksi, jos haluaisimme löytää varastosovelluksesta ostotapahtuman,
joka oli tehty syyskuussa ja ylittänyt hinnaltaan 100 €:

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
kuinka monta alkiota striimissä on.
Lisäksi perustietotyyppeille tarkoitetuissa striimeissä `IntStream`,
`DoubleStream` ja `LongStream` löytyy muun muassa seuraavia tilastometodeja:

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