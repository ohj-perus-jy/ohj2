# Ohjausrakenteet

> [!Osaamistavoitteet]
>
> - Kerrataan lyhyesti rakenteisen ohjelmoinnin perusteet
> - Ehtolauseet (`if`, `switch`)
> - Toistolauseet (`for`, `while`, `do-while`), ja listatyyppiset tietorakenteet
> - Tiedostat, että Javassa merkkijonot verrataan `equals`-aliohjelmalla eikä `==`

TODO: Pitäisikö tässä sanoa jotain muuta rakenteisesta ohjelmoinnista, kuin luvussa 1.2?

## Ehtolauseet

### If
If-lauseet toimivat samalla tavalla Javassa kuin muissakin kielissä, eli 
```java.ignore
if (ehto) {
    tee jotain
} else if (ehto2) {
    tee jotain muuta
} else {
    oletustoiminto
}
```

### Ehdollinen operaattori 
Syntaksi ehdolliselle ? operaattorille (engl. *ternary operator*) on: ehto ? tosi : epätosi. Sopii erityisesti tapauksiin, joissa vaihtoehtoja on kaksi. 

Koodiesimerkki:
```java,editable
void main () {
    int luku1 = 1;
    int luku2 = 2;
    int suurempi = (luku1 > luku2) ? luku1 : luku2;

    IO.println("Suurempi luvuista on: " + suurempi);
}, joka nostaa luettavuutta enti
```

### switch-lause
switch/case-syntaksi auttaa parantamaan koodin luettavuutta ja switch saattaa olla nopeampi ajaa Javassa (hyppytaulukoiden) ansiosta, jos (casena(keissinä, tapauksena?)) käytetään primitiivisiä tyyppejä tai enumeja. Java 25:sen mukana tuli nuolisyntaksi, joka nostaa luettavuutta entisestään. (Pitäisikö selittää syntaksista enemmänkin?). Tästä seuraavaksi esimerkki:

```java,editable
void main () {
    int kuukausi = 13;
    int vuosi = 2000;

    IO.println(
        switch(kuukausi) {
            case 1, 3, 5, 7, 8, 10, 12 -> 31;
            case 4, 6, 9, 11 -> 30;
            case 2 -> (vuosi % 4 == 0 && (vuosi % 100 != 0 || vuosi % 400 == 0)) ? 29 : 28; 
            default -> -1;
        }
    );

}
```

## Silmukat
Javasta löytyy 4 eri silmukkaa For, While, Do-While ja For-Each

### For
Sopii erityisesti silloin, kun tiedät etukäteen kuinka monta operaatiota tulee suorittaa.

```java
//-void main () {
int[] luvut = {1,2,3,4};
int summa = 0;
for (int i = 0; i < luvut.length: i += 2) {
    luvut[i]++;
}
IO.println(summa);
//-}

Seuraavissa esimerkeissä silmukoita koskien `luvut` ja `summa` pysyvät samanlaisina kuin yllä olevassa esimerkissä.

### For-Each
For-Each silmukka sopii erityisen hyvin, kun halutaan käydä läpi kaikki joukon alkiot (mikä olisi hyvä tapa ilmaista tämä? Kertoisi mistä on todella kyse?)

```java
void main () {
    //-int[] luvut = {1,2,3,4};
    //-int summa = 0;

    for (int luku : luvut) {
        summa += luku;
    }
    IO.println(summa);
}
```

### While
While silmukka on erityisen hyvä silloin, kun et etukäteen tiedä kuinka monta kertaaa silmukka suoritetaan. 

```java
void main () {
    //-int[] luvut = {1,2,3,4};
    //-int summa = 0;
    int i = 0;

    while(i < luvut.length){
        summa += luvut[i];
        i++;
    }

    IO.println(summa);
}
```

### Do-While
Toimintaperiaatteeltaan samanlainen kuin while-silmukka, mutta suoritetaan ainakin kerran. Syntaksista kannattaa huomata, että while avainsanan sisältävän rivin loppuun tuolee puolipiste `;`

```java
void main () {
    //-int[] luvut = {1,2,3,4};
    //-int summa = 0;
    //-int i = 0;
    do {
        summa += luvut[i];
        i++;
    } while (i < luvut.length);

    IO.println(summa);
}
```

## Listat
TODO:
(Kuinka tarkkaan metodeja tulisi käydä läpi? Vai mieluummin tekisi jonkin tehtävän, jossa joutuu kahlaamaan dokumentaatiota, että löytää sopivat metodit?)d

Huomaa ainakin nämä erot Javan ja C# välillä listoja käytettäessä:

| C#                     | Java                              |
| ---------------------- | --------------------------------- |
| list[indeksi]          | list.get(indeksi)                 |
| list.Count             | list.size()                       |
| list.RemoveAt(indeksi) | list.remove(indeksi)              |

Lisäksi Javassa metodille `.add()` on kaksi toteutusta, joista `.add(lisättava)` lisää listan loppuun ja `.add(indeksi, lisättävä)` lisää tiettyyn indeksiin taulukossa siirtäen loput alkiot yhden oikealle. Myös `.remove()` metodille on kaksi optiota, joista `.remove(indeksi)` poistaa tietyssä indeksissä olevan alkion ja `.remove(poistettavaAlkio)` poistaa tietyn alkion listasta, jos alkio löytyy (Pitäisikö kuitenkin puhua poistettavista olioista?). 

```java
import java.util.*;

void main () {
    List<String> mjonoLista = new ArrayList<>();
    mjonoLista.add("eka");
    mjonoLista.add(0, "toka");
    mjonoLista.add("kolmas");

    //Kaksi esimerkkiä kuinka luoda listaan heti sisältöä
    List<String> toinen = new ArrayList<>(List.of("koira", "kissa", "kala"));
    List<String> varit = Arrays.asList("punainen", "sininen", "keltainen");

    //For-Each on hyvä listojen tulostamiseen
    for(String mjono : mjonoLista) {
            IO.println(mjono);
    }

    for(String mjono : toinen) {
        IO.println(mjono);
    }

        for(String mjono : varit) {
        IO.println(mjono);
    }

}
```

Muista metodeista voi lukea dokumentaatiosta: https://docs.oracle.com/javase/8/docs/api/java/util/List.html

## Merkkijonojen vertailu
Javassa merkkijonojen sisältöjen vertailu tapahtuu String-luokan metodilla `.equals()`. (Sisäisesti `==` Java vertaa, että viittaavatko molemmat samaan objektiin)

```java
void main () {
    String mjono1 = "eka";
    String mjono2 = "eka";
    IO.println(mjono1.equals(mjono2));
}
```