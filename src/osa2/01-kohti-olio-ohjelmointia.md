# Kohti olio-ohjelmointia

> [!Osaamistavoitteet]
>
> - Otat askeleen proseduraalisen ohjelmoinnin *data ja funktio*
>   -ajattelumallista kohti olio-ohjelmoinnin *tila ja metodi* -ajattelumallia.
> - Ymmärrät olion käsitteen; tieto ja toiminnallisuus yhdessä paketissa.
> - Ymmärrät, miten käsitteiden mallintaminen olioina voi helpottaa ohjelman
>   rakentamista.

Tähän mennessä olemme tehneet enimmäkseen ohjelmia, joissa dataa tallennetaan
ohjelman muuttujiin ja käsitellään funktioiden avulla. Tällaista
ohjelmointityyliä kutsutaan *proseduraaliseksi ohjelmoinniksi*. Tutustumme tällä
kurssilla toiseen ohjelmointityyliin: *olio-ohjelmointiin*. 

Olio-ohjelmointi on hyvin laaja aihe, ja käymme tällä kurssilla läpi
olio-ohjelmoinnin teoriaa valikoidusti erityisesti tämän opintojakson tarpeita
ajatellen. Syvemmin teoriaan perehdytään esimerkiksi opintojaksolla 
[TIEA1130 Oliosuuntautunut suunnittelu ja ohjelmointi](https://opinto-opas.jyu.fi/2025/fi/opintojakso/tiea1130/). 

## Perusidea

Olio-ohjelmoinnissa ideana on luoda olioiksi kutsuttuja rakenteita, jotka
sisältävät datan sekä toiminnallisuudet sen muokkaamiseen. Oliot voivat olla
samanlaisia, mutta jokaisella oliolla on oma *tila*, joka voi muuttua ohjelman
suorituksen aikana. Olion tila tallentuu sen omiin muuttujiin eli
*attribuutteihin*. 

Oliolla voi olla myös omia aliohjelmia, joita kutsutaan *metodeiksi*. Metodi on
oliolle kuuluva aliohjelma, joka voi tarkastella ja muuttaa sen omistavan olion
tilaa. Ennen olion luontia täytyy ensin määrittää *luokka* eli *class*, jossa
kuvaillaan olion rakenne.

Olioiden tehtävä on olla vastuussa oman vastuualueensa toiminnallisuuksista. 
Olioiden välinen yhteistoiminta ja kommunikointi metodikutsujen kautta on 
olio-ohjelmoinnissa keskeisessä osassa. Joissain ohjelmointikielissä tätä 
saatetaan kutsutaan viestinvälitykseksi.

Minimaalinen, olioita hyödyntävä ohjelma voisi näyttää esimeriksi tältä:

```java
class Kissa {
    private String nimi;

    public String getNimi() {
        return nimi;
    }

    public void setNimi(String uusiNimi) {
        this.nimi = uusiNimi;
    }
}

void main() {
    Kissa kissa1 = new Kissa();
    kissa1.setNimi("Miuku");

    Kissa kissa2 = new Kissa();
    kissa2.setNimi("Katti");

    IO.println(kissa1.getNimi());
    IO.println(kissa2.getNimi());
}
```

Esimerkissä määritellään ensin `Kissa`-luokka ja luodaan sitten pääohjelmassa
sen pohjalta olioita, jotka sisältävät attribuuttina merkkijonon `nimi` sekä
kaksi metodia. Olion nimeä voidaan muuttaa kutsumalla sen `setNimi`-metodia ja
se voidaan pyytää vastaavasti `getNimi`-metodilla. Molemmilla olioilla on oma
tilansa - eli oma nimi. Yhden olion tila ei vaikuta toisen olion tilaan. 

Tästä yksinkertaisesta esimerkistä näemme, kuinka data voidaan ryhmitellä
olioiden sisälle. Tässä tapauksessa olion ainoa attribuutti `nimi` on suoraan
käsiteltävissä metodien kautta. Käytännössä tällainen suora manipulointi on
harvinaista tuotantokoodissa, mutta palaamme tähän myöhemmin.

Yhtä muuttujaa varten tuskin kannattaa tehdä eri olioita, mutta
olio-ohjelmoinnin hyödyt tulevat nopeasti esille, kun tallennettavan tiedon
määrä lisääntyy. Mietitään esimerkiksi tilannetta, jossa haluaisimme tallentaa
tietoa kilpailussa mukana olevista kilpailijoista. Kilpailijoita voi olla useita
ja jokaisesta pitäisi tallentaa ainakin nimi, kilpailijanumero ja pisteet.
Olioiden avulla voimme pitää yhden kilpailijan tiedot ja niiden muokkaamiseen
liittyvät toiminnallisuudet saman rakenteen sisällä, mikä helpottaa näiden
tietojen käsittelyä. 

```java
class Kilpailija {
    private String nimi;
    private int numero;
    private int pisteet;

    public Kilpailija(String nimi, int numero, int pisteet) {
        this.nimi = nimi;
        this.numero = numero;
        this.pisteet = pisteet;
    }

    // ...

    public void tulostaTiedot() {
        IO.println(String.format("%d: %s, %d pistettä", numero, nimi, pisteet));
    }
}

void main() {
    Kilpailija[] kilpailijat = {
        new Kilpailija("A", 2, 20),
        new Kilpailija("B", 4, 15),
        new Kilpailija("C", 6, 10)
    };

    for (Kilpailija kilpailija : kilpailijat) {
        kilpailija.tulostaTiedot();
    }
}
```

Vastaavan ohjelman tekeminen ilman olio-ohjelmointia vaatii vähän aivojumppaa.
Yksi tapa olisi käyttää kolmea erillistä taulukkoa: Yksi sisältäisi nimet,
toinen numerot ja kolmas pisteet. Tällöin täytyy kuitenkin huolehtia, että
kilpailijan tiedot löytyvät aina samoista indekseistä kaikissa taulukoissa, mikä
on käytännössä hankalaa ja altistaa virheille. Olioiden avulla tiedot ja
toiminnallisuudet voidaan paketoida selkeämmin yhteen. 

Yhteen kuuluvan tiedon ja toiminnallisuuden järjestely saman rakenteen sisälle
tekee ohjelman koodista helpommin ymmärrettävää ja laajennettavaa, mutta se ei
toki ole olio-ohjelmoinnin ainoa etu; voimme myös piilottaa osan luokan
toteutusyksityiskohdista vain luokan sisäiseen käyttöön, jolloin luokkaa
käyttävä ohjelmoija saa käyttöönsä vain tarkkaan määritetyn julkisen rajapinnan
eikä hänen tarvitse miettiä luokan sisäistä toimintaa. Tutustumme 3. osassa myös
polymorfismiin, perintään ja rajapintoihin, jolloin olio-ohjelmoinnin hyödyt
tulevat todella esille. 

## Pääohjelma Javassa

Java on erityisesti olio-ohjelmointiin suuntautunut ohjelmointikieli, jossa myös
pääohjelman on historiallisesti täytynyt olla luokan sisällä. Javan uudemmissa
versioissa tähän on tullut muutoksia; yksinkertaisen ohjelman kirjoittamista on
pyritty helpottamaan niin, että pääohjelma ei tarvitsisi ympärilleen luokkaa.
Näistä muutoksista voi lukea lisää [Java 21:n
dokumentaatiosta](https://openjdk.org/jeps/445) sekä vuoden 2025 syksyllä
julkaistun [Java 25:n dokumentaatiosta](https://openjdk.org/jeps/512). 

Nykyään riittää näissä materiaaleissa käytetty suoraviivaisempi pääohjelma:

```java
void main() {
    IO.println("Hei maailma!");
}
```

Aiemmin minimaalinen Java-ohjelma saattoi näyttää tältä:

```java
public class HeiMaailma {
    public static void main(String[] args) {
        IO.println("Hei maailma!");
    }
}
```

Vanhemman tyylin esimerkissä on muutama uusi käsite, joihin tutustumme tässä
osassa tarkemmin. Ohjelmassa määritetään ensiksi `class`-avainsanaa käyttäen
luokka, jonka nimeksi on esimerkissä annettu `HeiMaailma`. Pääohjelma `main`
sijoitetaan tämän luokan sisälle. Vanhassa tyylissä pääohjelmassa täytyy olla
`static`-määrite, jota katsomme tarkemmin pian.

Koska suoraviivaisempi pääohjelma on verrattain uusi ominaisuus, valtaosa 
verkosta ja kirjoista löytyvistä esimerkeistä käyttää yhä alkuperäistä tyyliä, 
eli luokan sisään upotettua pääohjelmaa. Tämä on hyvä tiedostaa tietoa etsiessä.
