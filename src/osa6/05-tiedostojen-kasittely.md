# Tiedostojen käsittely

> [!VAROITUS]
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Osaat lukea ja kirjoittaa tekstitiedostoja Javan `Files`-luokan avulla.
> - Osaat käyttää `Scanner`-luokkaa tiedon lukemiseen ja parsimiseen tiedostosta.
> - Osaat käsitellä tiedostoja riveittäin hyödyntäen Stream-rajapintaa.
> - Tunnet JSON-tiedostomuodon perusteet.
> - Osaat käyttää Jackson-kirjastoa JSON-datan lukemiseen ja kirjoittamiseen.
> - Ymmärrät, miten Javan `record`-tietueet soveltuvat datan mallintamiseen.

Tiedoston käsittelyssä on aina sama peruskaari: avaat resurssin, luet tai
kirjoitat dataa tietyssä muodossa, ja suljet resurssin. Java tarjoaa tähän
useita valmiita vaihtoehtoja. Valinta riippuu siitä, luetko luetko dataa vain
riveittäin vai tarvitsetko rivien pilkkomista ja parsimista arvoiksi (esim.
luvut), haluatko käsitellä suurta tiedostoa suorituskykyisesti, ja missä
muodossa data on.

## Oman tiedoston lisääminen projektiin

Oletetaan, että meillä on oheisen kaltainen tekstitiedosto. 

```csv
nimi,ika
Maija,25
Matti,30
```

Tiedosto sisältää henkilöiden tietoja. Ensimmäisellä rivillä on sarakkeiden
nimet, ja seuraavilla riveillä on tietoja henkilöistä. Tiedot on erotettu
toisistaan pilkuilla. Tällaista tiedostomuotoa kutsutaan CSV-tiedostoksi (engl.
*comma-separated values*), ja se on varsin yleinen tapa tallentaa
taulukkomuotoista dataa tekstitiedostoon.

Tallennetaan tällainen tiedosto nimellä `data.csv` projektin juurikansioon.
Jotta IDEA osaa ohjelman ajon aikana käyttää tätä tiedostoa, määritellään, että
ohjelman työskentelykansio on projektin juurikansio. Tämän voi tehdä Run <i
class="bi bi-chevron-right"></i> Edit Configurations. Valitse vasemmalta luokka,
johon `main`-metodi on kirjoitettu. Oikealla "Working directory" -kohdassa
varmista, että kansioksi on määritetty projektin lähdekoodin juurihakemisto,
joka päättyy yleensä `src` tai `src/main/java`.

Nyt voimme käyttää `data.csv`-tiedostoa ohjelmassamme.

## Tiedoston käsittely Files API:lla

`Files`-luokka (tai oikeammin sanottuna `java.nio.file`-paketin API) tarjoaa
suoraviivaisen tavan lukea koko tiedosto kerralla sellaisissa tilanteissa,
joissa tiedoston koko on kohtuullinen. Voit esimerkiksi lukea koko tiedoston
muistiin rivilistana `Files.readAllLines()`-metodilla tai merkkijonona
`Files.readString()`-metodilla. Jos datan sisältää vaikkapa lukuja, päivämääriä
tai muuta erikoisempaa, tulee ne käsitellä erikseen. 

Tehdään yllä oleva esimerkki käyttäen `Files`-luokan `readAllLines()`-metodia.
Tämä metodi lukee koko tiedoston muistiin listana merkkijonoja, joissa jokainen
merkkijono vastaa yhtä riviä tiedostossa. Tämän jälkeen voimme käydä listan läpi
ja pilkkoa jokaisen rivin sarakkeiksi.

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class TiedostonLukija {

    public static void main(String[] args) {
        try {
            List<String> lines = Files.readAllLines(Paths.get("data.csv"));
            for (int i = 1; i < lines.size(); i++) {
                String line = lines.get(i); 
                String[] parts = line.split(","); 
                String nimi = parts[0]; 
                int ika = Integer.parseInt(parts[1]); 
                IO.println("Nimi: " + nimi + ", Ikä: " + ika);
            }
        } catch (IOException e) {
            IO.println("Tiedostoa ei löydy tai sitä ei voi lukea: " + e.getMessage());
        } finally {
            // Ei tarvitse erikseen sulkea mitään, koska Files API hoitaa sen puolestamme
        }
    }
}
```

Samalla idealla &ndash; eli kokonainen tiedosto kerrallaan &ndash; voit myös
kirjoittaa tiedostoon. Kun koko sisältö on yhtenä merkkijonona, voit käyttää
`Files.writeString()`-metodia. Ennen kirjoittamista tulee varmistaa, että
 kansio, johon tiedosto kirjoitetaan, pitää olla olemassa. Tämä voidaan tehdä
seuraavasti:

```java,ignore
Path polku = Path.of("data", "tulos.txt"); // Polku-olio, joka sisältää tiedon kansiosta ja tiedostosta
Files.createDirectories(polku.getParent()); // Varmistetaan, että data-kansio on olemassa
``` 

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class KirjoitaTiedostoWriteString {
    public static void main(String[] args) {
        Path polku = Path.of("data", "tulos.txt");

        try {
            Files.createDirectories(polku.getParent()); // varmistetaan, että data-kansio on olemassa

            String sisalto = "Hei!\nTämä on uusi tiedosto.\n";
            Files.writeString(polku, sisalto, StandardCharsets.UTF_8);

            IO.println("Kirjoitettiin: " + polku.toAbsolutePath());
        } catch (IOException e) {
            IO.println("Kirjoittaminen epäonnistui: " + e.getMessage());
        }
    }
}
```

Kun data on riveinä, esimerkiksi listana, on usein luontevaa kirjoittaa se
riveittäin käyttäen `Files.write()`-metodia. 

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class KirjoitaTiedostoRiveina {
    public static void main(String[] args) {
        Path polku = Path.of("data", "data.csv");

        List<String> rivit = List.of(
                "nimi,ika",
                "Maija,25",
                "Matti,30"
        );

        try {
            Files.createDirectories(polku.getParent());
            Files.write(polku, rivit, StandardCharsets.UTF_8);

            IO.println("Kirjoitettiin: " + polku.toAbsolutePath());
        } catch (IOException e) {
            IO.println("Kirjoittaminen epäonnistui: " + e.getMessage());
        }
    }
}
```

On myös mahdollista lisätä tekstiä olemassa olevan tiedoston loppuun. Se vaatii
parin lisäargumentin antamista. Alla lyhyt esimerkki `Files.write()`-metodin
käytöstä, jossa teksti lisätään olemassa olevan tiedoston loppuun.

```java,ignore
// ...
Path polku = Path.of("data", "tulos.txt");
String rivi = "Uusi rivi, joka lisätään tiedoston loppuun.\n";
Files.writeString(
        polku,
        rivi,
        StandardCharsets.UTF_8, // Käytetään UTF-8-koodausta
        StandardOpenOption.CREATE, // Luo tiedosto, jos sitä ei ole
        StandardOpenOption.APPEND // Lisää tekstiä olemassa olevan tiedoston loppuun
);
// ...
```

## Lukeminen Scanner-oliolla

Scanner sopii tilanteisiin, joissa haluat lukea tekstiä ikään kuin palasissa:
esimerkiksi kokonainen rivi kerrallaan, seuraavaan välilyöntiin asti tai jopa
seuraavan luvun. Voit ajatella, että Scanner-olio on kuin lukupää, "kursori",
joka etenee sitä mukaa kun kutsut kursoria eteenpäin liikuttavia metodeja, kuten
`nextLine()` tai `next()`. Kun tiedostossa ei ole enää luettavaa, saat
`hasNext()`-metodilta paluuarvon `false`. 

Scanner osaa myös lukea lukuja ja muita primitiivityyppejä suoraan (`nextInt()`,
`nextDouble()`, jne.), mikä vähentää käsin parsimista. 

Alla olevassa mallikoodissa luetaan tiedosto `Scanner`-oliolla. Ensin luodaan
Tiedoston lukeminen tapahtuu siis rivi kerrallaan, ja jokainen rivi pilkotaan
sarakkeiksi.

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;


public class TiedostonLukija {

    public static void main(String[] args) {
        try {
            Scanner scanner = new Scanner(new File("data.csv"));
            // Ohitetaan otsikkorivi
            if (scanner.hasNextLine()) {
                scanner.nextLine();
            }
            // Luetaan rivejä, kunnes tiedoston loppu saavutetaan
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine(); // Esim. "Maija,25"
                String[] parts = line.split(","); // Pilkotaan rivi sarakkeiksi
                String nimi = parts[0]; // Ensimmäinen sarake on nimi
                int ika = Integer.parseInt(parts[1]); // Toinen sarake on ikä, parsitaan intiksi
                IO.println("Nimi: " + nimi + ", Ikä: " + ika);
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            IO.println("Tiedostoa ei löydy: " + e.getMessage());
        } finally {
            // Suljetaan scanner
            scanner.close();
        }
    }
}
```

Aina käsiteltävä aineisto ei ole näin "nättiä". Tiedostossa voi olla lukuja,
joiden erottimina voi olla vaikkapa välilyönti, pilkku, puolipiste tai
rivinvaihto. 

Oletetaan tiedosto `mittaukset.txt`:

```
12  8,  5
-3; 10  7
virhe  2  1.5  3
```

Haluat lukea kaikki numerot riippumatta siitä, millä tavalla ne on eroteltu.
Tämä on vaikeampi tehdä siististi rivi kerrallaan `Files`-luokan avulla, mutta
`Scanner`-olion avulla asia hoituu kätevämmin. `Scanner`-olion
`useDelimiter()`-metodilla voit määritellä, mitkä merkit toimivat erottimina.
Esimerkiksi `useDelimiter("[\\s,;]+")` määrittelee, että välilyönti, pilkku ja
puolipiste ovat erottimia. Kaikki ennen erotinmerkkiä olevat merkit muodostavat
niin sanotun *tokenin*, joka voidaan lukea `next()`-metodilla.


```java
import java.io.File;
import java.io.IOException;
import java.util.Locale;
import java.util.Scanner;

public class LueNumerotScannerilla {
    public static void main(String[] args) throws IOException {

        double summa = 0.0;
        int maara = 0;

        Scanner sc = new Scanner(new File("mittaukset.txt"));
        try {
            sc.useLocale(Locale.US); // desimaalierottimena piste "."
            sc.useDelimiter("[\\s,;]+"); // erottimina välilyönti, rivinvaihto, pilkku tai puolipiste

            while (sc.hasNext()) { // onko vielä luettavia tokeneja
                if (sc.hasNextDouble()) { // onko seuraava palanen kelvollinen luku
                    summa += sc.nextDouble(); // lue luku ja lisää summaan
                    maara++;
                } else {
                    sc.next(); // ohita token, joka ei ole kelvollinen luku
                }
            }
        } finally {
            sc.close();
        }

        IO.println("Lukuja: " + maara);
        IO.println("Summa: " + summa);
        IO.println("Keskiarvo: " + (maara == 0 ? 0 : summa / maara));
    }
}
```

Scanner-oliolla ei voi kirjoittaa tiedostoon, se on vain lukutyökalu.

## Tietovirrat (Stream) 

Kokoelmien ohella (ks. [osa 6.2](./02-kokoelmien-kasittely-stream-api.md)) mmyös
tiedostoja (ja muitakin ulkoisia resursseja) voidaan käsitellä Stream-rajapinnan
avulla. Streamit ovat hyödyllisiä silloin, kun dataan halutaan tehdä useita
peräkkäisiä operaatioita, kuten muunnoksia (map), suodatuksia (filter) ja
keräilyä (esim. toList, collect). Tällöin käsittely kuvataan ketjuna, joka
kertoo selkeästi mitä datalle tehdään vaihe vaiheelta.

Luettaessa tiedostoa virtana tyypillinen aloitus on Files.lines(polku). Se
tuottaa rivit laiskasti: rivejä ei lueta etukäteen kokonaan muistiin, vaan niitä
luetaan sitä mukaa kuin streamiä kulutetaan. Tämä on keskeinen ero
readAllLines-metodiin: Files.lines sopii myös suurille tiedostoille, koska se ei
vaadi koko tiedoston lataamista muistiin. Koska tiedostoa luetaan taustalla,
stream täytyy sulkea.

Tehdään aluksi yksinkertainen esimerkki, jossa toistetaan aiempi kuvio, mutta
nyt käytetään `Files.lines`-metodia ja Stream-käsittelyä. Käytämme aiemmin
opittua `map`-operaatiota muuntamaan jokaisen rivin taulukkomuotoon. Käytämme
kerääjäfunktiona `forEach`-metodia, joka suorittaa annetun lambda-lausekkeen
jokaiselle riville. Tässä parsimme rivit samalla tavalla kuin aiemmissa
esimerkeissä, ja lopuksi tulostamme nimet ja iät.

```java,ignore
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class TiedostonLukijaStream {
    static void main() {
        try {
            Files.lines(Paths.get("data.csv"))
                    .skip(1) // Ohitetaan otsikkorivi
                    .map(line -> line.split(",")) // Pilkotaan rivi sarakkeiksi
                    .forEach(parts -> {
                        String nimi = parts[0]; // Ensimmäinen sarake on nimi
                        int ika = Integer.parseInt(parts[1]); // Toinen sarake on ikä, parsitaan intiksi
                        IO.println("Nimi: " + nimi + ", Ikä: " + ika);
                    });
        } catch (IOException e) {
            IO.println("Tiedostoa ei löydy tai sitä ei voi lukea: " + e.getMessage());
        }
    }
}
``` 

Jatketaan esimerkkiä hieman. Suodatetaan sellaiset henkilöt pois, joiden ikä on
alle 18 vuotta, ja lopuksi tulostetaan nimet aakkosjärjestyksessä.

```java,ignore
//-import java.io.IOException;
//-import java.nio.file.Files;
//-import java.nio.file.Paths;
//-import java.util.List;
//-
//-public class TiedostonLukijaStream {
//-    static void main() {
//-        try {
List<String> nimet = Files.lines(Paths.get("data.csv"))
        .skip(1) // Ohitetaan otsikkorivi
        .map(line -> line.split(",")) // Pilkotaan rivi sarakkeiksi
// HIGHLIGHT_GREEN_BEGIN
        .filter(parts -> Integer.parseInt(parts[1]) >= 18) // Suodatetaan alle 18-vuotiaat
        .map(parts -> parts[0]) // Otetaan vain nimi
        .sorted() // Järjestetään nimet aakkosjärjestykseen
        .toList(); // Kerätään tulokset listaksi
nimet.forEach(IO::println); // Tulostetaan nimet
// HIGHLIGHT_GREEN_END
//-        } catch (IOException e) {
//-            IO.println("Tiedostoa ei löydy tai sitä ei voi lukea: " + e.getMessage());
//-        }
//-    }
//-}
```

Virtapohjaisessa käsittely on varsin näppärää, kun käsittely on suhteellisen
yksinkertaista ja lineaarisesti etenevää. Virtapohjainen käsittely voi kuitenkin
merkittävästi hankaloittaa esimerkiksi debuggaamista, joka on hyvä tiedostaa. 

<details><summary><i class="bi bi-stars jyu-gold"></i> Valinnaista lisätietoa: Stream-käsittelyn haasteista tarkemmin</summary>

 * kertakäyttöisyys: Stream-olion voi käyttää vain kerran, minkä jälkeen se on
   suljettava. Jos haluat käsitellä samaa dataa uudestaan,
   sinun täytyy luoda uusi Stream-olio.
 * debuggaaminen: Ketjutus piilottaa välitulokset. Jos jokin map/filter-vaihe
   heittää poikkeuksen, pinoloki kertoo kyllä missä lambdassa oltiin, mutta
   "mikä rivi" ja "millä välituloksella" ei näy ilman erillisiä tulostuksia tai
   erillisen
   [`peek()`](https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html#peek-java.util.function.Consumer-)-metodin
   kutsumista. Lambda-lausekkeita ei voi askeltaa yhtä suoraviivaisesti kuin
   perinteistä `for`-silmukkaa. 
 * virheiden käsittely: lambda-lausekkeiden sisällä tapahtuvat tarkistamattomat
   poikkeukset (esim. `NumberFormatException` `Integer.parseInt()`-kutsussa) on
   käsiteltävä erikseen, koska lambda-lausekkeet eivät salli tarkistamattomien
   poikkeusten heittämistä suoraan. Tämä voi tehdä virheiden käsittelystä hieman
   monimutkaisempaa verrattuna perinteiseen silmukkaan.
 * laiskuus voi yllättää: Stream ei tee mitään ennen keräysoperaatiota
   (`forEach`, `toList`, `collect`, `count`, …). Tämä voi aiheuttaa yllätyksiä, kuten
   että koodi näyttää lukevan tiedoston, mutta mitään ei tapahdu, jos
   keräysvaihe puuttuu. Myöskään poikkeukset eivät synny siinä kohdassa,
   missä tiedosto avataan, vaan vasta keräysvaiheessa.

</details>

## BufferedReader ja BufferedWriter

[BufferedReader](https://docs.oracle.com/javase/8/docs/api/java/io/BufferedReader.html)
ja
[BufferedWriter](https://docs.oracle.com/javase/8/docs/api/java/io/BufferedWriter.html)
ovat "perinteisiä" työkalut tekstitiedostojen käsittelyyn silloin, kun haluat
lukea ja kirjoittaa rivi kerrallaan ja hallita käsittelysilmukkaa tarkasti. Ne
puskuroivat I/O:ta, eli eivät tee järjestelmäkutsua jokaisesta yksittäisestä
merkistä, vaan lukevat ja kirjoittavat suuremmissa paloissa. Tämä parantaa
suorituskykyä erityisesti suurilla tiedostoilla ja tekee käsittelystä
ennustettavaa. Jätämme näiden opiskelun omatoimiseksi, valinnaiseksi
harjoitukseksi.

## JSON-muotoinen tiedosto

JSON (JavaScript Object Notation) on suosittu tiedonvaihtomuoto, joka on paljon
käytetty erityisesti web-kehityksessä. JSON-tiedostot ovat avain-arvo-pareja
sisältäviä tekstitiedostoja, jotka voivat sisältää monimutkaisia
tietorakenteita, kuten taulukkoja ja olioita.

JSON voi sisältää seuraavan tyyppisiä arvoja:

 * merkkijono (`"Maija"`)
 * luku (`25`)
 * totuusarvo (`true` / `false`)
 * tyhjä arvo (`null`)
 * taulukko (`[...]`)
 * olio (`{...}`)

Esimerkiksi tiedosto `henkilot.json` voi näyttää tältä:

```json
[
  {
    "nimi": "Maija",
    "ika": 25,
    "kaupunki": "Jyväskylä"
  },
  {
    "nimi": "Matti",
    "ika": 30,
    "kaupunki": "Tampere"
  }
]
```

CSV:hen verrattuna JSONin etu on se, että kentät voivat olla sisäkkäisiä, eli
vaikkapa "kaupunki" voisi olla olio, jossa on "aikaisemmat_kaupungit" ja
"nykyinen_kaupunki". Näin ollen rivit eivät ole sidottuja yhteen
taulukkomalliin. Haittapuolena rakenne on usein hieman raskaampi lukea
silmämääräisesti verrattuna CSV:hen. Lisäksi niissä on hieman enemmän syntaksia,
mikä tekee niistä hieman monimutkaisempia käsitellä "käsin" ilman erillistä
kirjastoa.

## JSON-tiedostojen käsittely Jackson-kirjastolla

JSONin käsittely onnistuu toki käsin merkkijonoja pilkkomalla, mutta käytännössä
tämä on virhealtista. Siksi JSONia kannattaa käsitellä siihen tarkoitetulla
kirjastolla. Yksi yleisimmistä Java-kirjastoista on **Jackson**.

Lisää `pom.xml`-tiedostoon Jackson-riippuvuus:

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.17.2</version>
</dependency>
```

Riippuvuuden lisäämisen jälkeen virkistä Maven-projektisi. Alla oleva esimerkki
lukee tiedoston `henkilot.json` listaksi `Henkilo`-olioita. Selitämme koodin
tarkemmin seuraavaksi.


```java
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public class LueJson {
    public static void main(String[] args) {
        ObjectMapper mapper = new ObjectMapper();
        Path polku = Path.of("data", "henkilot.json");

        try {
            List<Henkilo> henkilot = mapper.readValue(
                    polku.toFile(),
                    new TypeReference<List<Henkilo>>() {}
            );

            henkilot.forEach(h ->
                    IO.println(h.nimi() + " (" + h.ika() + "), " + h.kaupunki())
            );
        } catch (IOException e) {
            IO.println("JSONin lukeminen epäonnistui: " + e.getMessage());
        }
    }
}
```

**JSONin lukeminen tiedostosta:** Lukeminen aloitetaan luomalla
`ObjectMapper`-olio, joka on Jackson-kirjaston keskeinen työkalu JSONin
muuntamiseen Java-olioiksi ja päinvastoin. Tämän jälkeen käytetään
`readValue()`-metodia, joka ottaa JSON-tiedoston ja kertoo, minkä tyyppiseksi
JSONin pitäisi muuntaa. 

Jotta muunnos olisi mahdollinen, meidän täytyy mallintaa JSON-tieto
Java-olioiksi. Tehdään Java-luokka `Henkilo`, jossa on kentät `nimi`, `ika` ja
`kaupunki`, eli saman nimiset kentät kuin JSON-tiedostossa. Tehdään myös niitä
vastaavat getterit ja setterit, sekä tyhjä konstruktori &ndash; tämän kaltainen
luokka on Jackson-kirjaston vaatimus, jotta se osaa luoda olioita JSONista. Alla
esimerkki. 

```java,ignore
public class Henkilo {
    private String nimi;
    private int ika;
    private String kaupunki;

    public Henkilo() {
    }

    public void setNimi(String nimi) {
        this.nimi = nimi;
    }

    public String getNimi() {
        return nimi;
    }

    public int getIka() {
        return ika;
    }

    public void setIka(int ika) {
        this.ika = ika;
    }

    public void setKaupunki(String kaupunki) {
        this.kaupunki = kaupunki;
    }

    public String getKaupunki() {
        return kaupunki;
    }
}
```

Koska on mahdollista, että JSON-tiedoston lukeminen epäonnistuu (esim. tiedosto
ei löydy, JSON on virheellistä tai tyyppimuunnos epäonnistuu), tulee mahdolliset
`IOException`-poikkeukset käsitellä käyttäen `try-catch`-rakennetta.

**JSONin kirjoittaminen tiedostoon** on aavistuksen lukemista helpompaa.
Kirjoittaminen tapahtuu `writeValue()`-metodilla, joka ottaa tiedoston ja
tallennettavan olion, ja muuntaa sen JSON-muotoon. Tiedoston kirjoittaminen voi
epäonnistua, joten sekin tulee käsitellä `try-catch`-rakenteella.

Seuraava esimerkki kirjoittaa listan
henkilöitä tiedostoon `henkilot-uusi.json`:

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class KirjoitaJson {
    public static void main(String[] args) {
        ObjectMapper mapper = new ObjectMapper()
                .enable(SerializationFeature.INDENT_OUTPUT); // kauniimpi sisennys

        List<Henkilo> henkilot = List.of(
                new Henkilo("Aino", 22, "Turku"),
                new Henkilo("Pekka", 41, "Oulu")
        );

        Path polku = Path.of("data", "henkilot-uusi.json");

        try {
            Files.createDirectories(polku.getParent());
            mapper.writeValue(polku.toFile(), henkilot);
            IO.println("Kirjoitettiin JSON: " + polku.toAbsolutePath());
        } catch (IOException e) {
            IO.println("JSONin kirjoittaminen epäonnistui: " + e.getMessage());
        }
    }
}
```

## Record-luokka JSONin mallintamiseen

Esitellään tässä kohtaa lyhyesti Javan *record*-käsite. Javan record on
erityinen luokka, joka on suunniteltu pienten, suoraviivaisten datarakenteiden
kuten JSONin kaltaisen rakenteisen datan mallintamiseen. Kun määrittelet
recordin, Java muodostaa automaattisesti joitain rutiineja sinulle valmiiksi
taustalla. Saat valmiina: 

 * automaattisen konstruktorin, joka ottaa kaikki kentät argumentteina,
 * kenttiä vastaavat "getterit", joiden nimet ovat suoraan kenttien nimet, esim.
`nimi()` eikä `getNimi()`,
 * `equals()`- ja `hashCode()`-toteutukset,
 * selkeän `toString()`-tulostuksen.

Record-olion *komponentit* (eli attribuutit) ovat käytännössä final-kenttiä,
mikä tarkoittaa, että recordit ovat pääosin muuttumattomia olioita. 

Näin recordit ovat luonnollinen pari JSON-kirjastoille: JSON-olio vastaa usein
suoraan yhtä "datakimppua", jonka voi mallintaa recordilla ilman ylimääräistä
koodia. Siinä missä perinteinen luokka kirjoitetaan usein niin, että
määritellään kentät, konstruktorit ja getterit erikseen, recordissa sama asia
ilmaistaan tiiviisti yhdellä rivillä. 

On hyvä huomata, että recordiin saa kyllä kirjoittaa metodeja ja tarkistuksia,
mutta perusajatus on pitää se pienenä ja keskittyä datan esittämiseen. Jos
luokkaan alkaa kertyä paljon muuttuvaa tilaa tai monimutkaista
toiminnallisuutta, tavallinen luokka on yleensä parempi valinta.

Määritellään datalle nyt tietotyyppi käyttäen record-rakennetta:

```java
public record Henkilo(String nimi, int ika, String kaupunki) {}
```

Tällä tavalla pitkähkö `Henkilo`-luokka saadaan korvattua yhdellä rivillä. Tässä
tapauksessa record-luokka on toiminnallisuudeltaan täysin samanlainen kuin
aiemmin määritetty perinteinen luokka.

## Tehtävät

<task>
  <task-title>Tehtävä 6.9: Sanat. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/6-9-sanat/handout.md}}

  </handout>

  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa6/tehtava9">Tee tehtävä TIMissä</a></task-link>

</task>



<task>
  <task-title>Tehtävä 6.10: Lue henkilöt JSON-tiedostosta. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/6-10-json-1/handout.md}}

  </handout>

  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa6/tehtava10">Tee tehtävä TIMissä</a></task-link>

</task>

<task>
  <task-title><i class="bi bi-stars jyu-gold"></i> Bonus: Tehtävä 6.11: CSV -> JSON. <points>1 p.</points> </task-title>

  <handout>

{{#include ../exercises/6-11-csv-json/handout.md}}

  </handout>

  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa6/tehtava11">Tee tehtävä TIMissä</a></task-link>

</task>
