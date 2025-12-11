# Kohti olio-ohjelmointia

> [!Osaamistavoitteet]
>
> - Eteneminen "data+funktio"-ajatuksesta (Ohj1) kohti "tila+metodi"-ajatusta (Ohj2)
> - Proseduraalisesta ohjelmoinnista ("data+funktio") olio-ohjelmointiin ("tila+metodi+viestit")
> - Ymmärrät luokkien ja olioiden roolin olio-ohjelmoinnissa (Tieto ja toiminnallisuus yhdessä paketissa)

Hahmotelma:

Perusasiat lyhyesti:
- mitä olio-ohjelmointi on? Mikä on olio?
- mitä olio-ohjelmoinnilla voi saavuttaa?
- olion tila ja metodit (vrt. proseduraalinen ohjelmonti)
Esimerkki: yksinkertainen esimerkki; luokka ja oliot
Esimerkki: proseduraalinen ohjelma verrattuna olio-ohjelmointia hyödyntävään ohjelmaan

## Olio-ohjelmointi

Tähän mennessä olemme tehneet enimmäkseen proseduraalisia ohjelmia, joissa dataa tallennetaan ohjelman muuttujiin ja käsitellään funktioiden avulla. Tutustumme tällä kurssilla myös toiseen ohjelmointiparadigmaan; olio-ohjelmointiin. Olio-ohjelmoinnissa ideana on luoda olioiksi kutsuttuja objekteja, jotka sisältävät datan sekä toiminnallisuudet sen muokkaamiseen. Oliot voivat olla samanlaisia, mutta jokaisella oliolla on oma *tila*, joka voi muuttua ohjelman suorituksen aikana. Olion tila tallentuu sen omiin muuttujiin eli *attribuutteihin*. Oliolla voi olla myös omia aliohjelmia, joita kutsutaan *metodeiksi*. Metodi on oliolle kuuluva aliohjelma, joka voi tarkastella ja muuttaa sen omistavan olion tilaa. Ennen olion luontia täytyy ensin määrittää *luokka* eli *class*, jossa kuvaillaan olion rakenne.

Minimaalinen, olioita hyödyntävä ohjelma voisi näyttää esimeriksi tältä:

```java
public class Kissa {
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

Esimerkissä määritellään ensin `Kissa`-luokka ja luodaan sitten pääohjelmassa sen pohjalta olioita, jotka sisältävät attribuuttina merkkijonon `nimi` sekä kaksi metodia. Olion nimeä voidaan muuttaa kutsumalla sen `setNimi`-metodia ja se voidaan pyytää vastaavasti `getNimi`-metodilla. Molemmilla olioilla on oma tilansa - eli oma nimi. Yhden olion tila ei vaikuta toisen olion tilaan.

Tästä yksinkertaisesta esimerkistä näemme, kuinka data voidaan ryhmitellä olioiden sisälle. Tässä tapauksessa olion ainoa attribuutti `nimi` on suoraan käsiteltävissä metodien kautta, mutta olioilla voi toki olla myös attribuutteja, joiden ei ole tarkoituskaan olla muiden nähtävissä tai saatavissa.

Kuinka voimme käyttää olioita hyödyksi ohjelmoinnissa? Mietitään esimerkiksi tilannetta, jossa haluaisimme tallentaa tietoa kilpailussa mukana olevista kilpailijoista. Kilpailijoita voi olla useita ja jokaisesta pitäisi tallentaa ainakin nimi, kilpailijanumero ja pisteet. Olioiden avulla voimme pitää yhden kilpailijan tiedot ja niiden muokkaamiseen liittyvät toiminnallisuudet saman rakenteen sisällä, mikä helpottaa näiden tietojen käsittelyä. Mieti hetki, kuinka tekisit alla olevan kaltaisen ohjelman ilman olio-ohjelmointia.

```java
public class Kilpailija {
    private String nimi;
    private int numero;
    private int pisteet;

    public Kilpailija(String nimi, int numero, int pisteet) {
        this.nimi = nimi;
        this.numero = numero;
        this.pisteet = pisteet;
    }

    // ...

    @Override
    public String toString() {
        return String.format("%d: %s, %d pistettä", numero, nimi, pisteet);
    }
}

void main() {
    Kilpailija[] kilpailijat = {
        new Kilpailija("A", 2, 20),
        new Kilpailija("B", 4, 15),
        new Kilpailija("C", 6, 10)
    };

    for (Kilpailija kilpailija : kilpailijat) {
        IO.println(kilpailija.toString());
    }
}
```

Jotkin esimerkeissä esiintyvät rakenteet ja käsitteet voivat tässä vaiheessa tuntua vielä vierailta. Lähdemme tutustumaan näihin tarkemmin heti osassa 2.2.

Olio-ohjelmointi on hyvin laaja aihe, jonka teoriaan perehdytään syvällisemmin esimerkiksi opintojaksolla [TIEA1130 Oliosuuntautunut suunnittelu ja ohjelmointi](https://opinto-opas.jyu.fi/2025/fi/opintojakso/tiea1130/). Käymme tällä kurssilla läpi olio-ohjelmoinnin teoriaa valikoidusti erityisesti tämän opintojakson tarpeita ajatellen. 

Jos haluat tutustua olio-ohjelmointiin syvällisemmin, suosittelemme lämpimästi tutustumaan aiheeseen liittyvään kirjallisuuteen.

TODO: Linkki kurssiin, linkkejä vapaaehtoiseen luettavaan, SOLID, ym?

TODO: Jos puhutaan olio-ohjelmoinnin oikeista hyödyistä, motivaationa voisi lyhyesti mainita polymorfismin, perinnän ym, ja että näihin tutustutaan tarkemmin seuraavassa osassa.

TODO: Yhteen kuuluvan tiedon ja toiminnallisuuden järjestely saman rakenteen sisälle voi tehdä koodista helpommin ymmärrettävää ja siten hallittavaa, mutta se ei toki ole olio-ohjelmoinnin ainoa etu. Tutustumme seuraavassa osassa polymorfismiin, perintään ja rajapintoihin. Käyttämällä näitä ominaisuuksia voidaan vähentää toistoa ... 

## Pääohjelma Javassa

Java on erityisesti olio-ohjelmointiin suuntautunut ohjelmointikieli, jossa myös pääohjelman on historiallisesti täytynyt olla luokan sisällä. Javan uudemmissa versioissa tähän on tullut muutoksia; yksinkertaisen ohjelman kirjoittamista on pyritty helpottamaan niin, että pääohjelma ei tarvitsisi ympärilleen luokkaa. Näistä muutoksista voi lukea lisää [Java 21:n dokumentaatiosta](https://openjdk.org/jeps/445) sekä vuoden 2025 syksyllä julkaistun [Java 25:n dokumentaatiosta](https://openjdk.org/jeps/512).

Aikaisemmin minimaalinen Java-ohjelma saattoi näyttää tältä:

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hei maailma!");
    }
}
```

Nykyään riittää myös näissä materiaaleissa käytetty suoraviivaisempi pääohjelma:

```java
void main() {
    System.out.println("Hei maailma!");
}
```

Koska ominaisuus on verrattain uusi, valtaosa verkosta ja kirjoista löytyvistä esimerkeistä käyttää yhä alkuperäistä tyyliä, eli luokan sisään upotettua pääohjelmaa. Tämä on hyvä tiedostaa tietoa etsiessä.
