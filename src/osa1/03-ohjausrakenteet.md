# Ohjausrakenteet

> [!Osaamistavoitteet]
>
> - Kerrataan lyhyesti rakenteisen ohjelmoinnin perusteet
> - Ehtolauseet (`if`, `switch`)
> - Toistolauseet (`for`, `while`, `do-while`), ja listatyyppiset tietorakenteet
> - Tiedostat, että Javassa merkkijonot verrataan `equals`-aliohjelmalla eikä `==`

## Ehtolauseet

### If
If-lauseet toimivat samalla tavalla Javassa kuin muissakin kielissä, eli 
```java.ignore
if (ehto) {
    tee jotain
} else if (ehto2) {
    tee jotain muuta
} else {

}
```

```java
void main () {
    bool =
}
```

### Switch


### Ehdollinen operaattori 

Syntaksi ? operaattorille (engl. *ternary operator*) on: ehto ? tosi : epätosi

Koodiesimerkki:
```java,editable
void main () {
    int luku1 = 1;
    int luku2 = 2;
    int suurempi = (luku1 > luku2) ? luku1 : luku2;

    IO.println("Suurempi luvuista on: " + suurempi);
}
```

## Silmukat
Javasta löytyy 4 eri silmukkaa For, While, Do-While ja For-Each

### For
Sopii erityisesti silloin, kun tiedät etukäteen kuinka monta operaatiota tulee suorittaa.

```java
void main () {
    int[] luvut = {1,2,3,4};
    int summa = 0;

    for (int i = 0; i < luvut.length: i += 2) {
        luvut[i]++;
    }
    IO.println(summa);
}
```

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
Kuinka tarkkaan metodeja tulisi käydä läpi? Vai mieluummin tekisi jonkin tehtävän, jossa joutuu kahlaamaan dokumentaatiota, että löytää sopivat metodit?

Huomaa ainakin nämä erot Javan ja C# välillä listoja käytettäessä:

| C#        | Java                              |
| --------- | --------------------------------- |
| public    | näkyvyysmodifikaattori — julkinen |
| static    | staattinen — kuuluu luokalle      |
| void      | ei palauta arvoa                  |

```java
import java.util.*;

void main () {
    List<String> mjonoLista = new ArrayList<>();
    mjonoLista.add("eka");
    mjonoLista.add("toka");
    mjonoLista.add("kolmas");
    IO.println(mjonoLista.size());
    IO.println(mjonoLista.indexOf("kolmas"));

    List<String> toinen = new ArrayList<>(List.of("koira", "kissa", "kala"));
    List<String> varit = Arrays.asList("punainen", "sininen", "keltainen");
    toinen.add("kissakala");

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

## Merkkijonojen vertailu
Javassa merkkijonojen sisältöjen vertailu tapahtuu String-luokan metodilla `.equals()`. (Sisäisesti `==` Java vertaa, että viittaavatko molemmat samaan objektiin)

```java
void main () {
    String mjono1 = "eka";
    String mjono2 = "eka";
    IO.println(mjono1.equals(mjono2));
}
```