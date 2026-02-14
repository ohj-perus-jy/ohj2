# Tiedostojen käsittely

> [!VAROITUS]
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Osaat käsitellä tiedostoja Javan valmiiden rajapintojen kautta (Tiedostomuotojen käsittely "käsin" (CSV) ja kirjastolla (JSON))
> - Files API
> - Tietovirrat (Stream) ja sen oheisluokat (BufferedReader/Writer, Scanner)
> - Yksinkertaisen tiedoston lukeminen (CSV-tyylinen)
> - Jokin JSON-kirjasto ja JSON-tiedoston lukeminen: Gson, Jackson, org.json???

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

`Files`-luokka tarjoaa suoraviivaisen tavan lukea koko tiedosto kerralla
sellaisissa tilanteissa, joissa tiedoston koko on kohtuullinen. Voit esimerkiksi
lukea koko tiedoston muistiin rivilistana `Files.readAllLines()`-metodilla tai
merkkijonona `Files.readString()`-metodilla. Jos datan sisältää vaikkapa lukuja,
päivämääriä tai muuta erikoisempaa, tulee ne käsitellä erikseen. 

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

## Tiedoston käsittely Scanner-oliolla

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

        System.out.println("Lukuja: " + maara);
        System.out.println("Summa: " + summa);
        System.out.println("Keskiarvo: " + (maara == 0 ? 0 : summa / maara));
    }
}
```

## Tietovirrat (Stream) 

Kokoelmien ohella (ks. [osa 6.2](./02-kokoelmien-kasittely-stream-api.md)) myös
tiedostoja (ja muitakin ulkoisia resursseja) voidaan käsitellä virtoina
`Stream`-luokan avulla. Erityisen hyödyllisiä Streamit ovat silloin, kun
halutaan tehdä monimutkaisempia datan käsittelyä, joka vaatii useita peräkkäisiä
operaatioita, kuten muunnoksia (map), suodatuksia (filter) ja keräilyä (esim.
collect). Streamin avulla tämä onnistuu ketjutettujen metodikutsujen avulla,
joka tekee koodista joskus selkeämpää ja helpommin luettavaa. 

Luettaessa tiedostoa virtana tyypillinen aloitus on `Files.lines(polku)`, joka
antaa rivit "laiskasti", mikä tarkoittaa, että kaikkia rivejä ei lueta etukäteen
muistiin, vaan niitä luetaan sitä mukaa kun niitä tarvitaan. Tämä onkin
keskeinen ero `readAllLines`-metodiin: `Files.lines` sopii myös hyvin suurille
tiedostoille, koska se ei vaadi koko tiedoston lataamista muistiin.

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

## Tiedostojen käsittely BufferedReader- ja BufferedWriter-luokilla

Kun tarttee tehokkaasti lukea tavuja, niin se  ovi olla hyvä... Ehkä
bonustiedoksi? 

## CSV-tiedostojen käsittely

## JSON-tiedostojen käsittely Jackson-kirjastolla

JSON Jacsksonilla. Lue JSONia ja kirjoita JSONia. Tulostele jotain kivaa. Tästä tehtäviä. 

Ehkä? CSV -> Json voi muuntaa. Asenna riippuvuus Mavenilla. Sitten luetaan CSV-tiedosto, ja muunnetaan se JSON-muotoon.

