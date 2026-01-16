
Rajapinnasta löytyy oletusmetodit `comparing` sekä `thenComparing`, joiden
avulla voidaan määrittää järjestämisen ehdot. Sekä `comparing`, että
`thenComparing` ottavat argumenttina funktion, jonka palauttama arvoa käytetään
vertailuun.

Alla esimerkki, jossa määritellään korttien järjestys ensin sarjan nimen ja
sitten aakkosjärjestyksen mukaan käyttäen `Comparator`-rajapintaa ja luokan
getter-metodeja.

```java
// FILE: main.java
void main() {
    List<Kerailykortti> kortit = Arrays.asList(
        new Kerailykortti("Loistava Lohikäärme", "Eläimet", 3),
        new Kerailykortti("Vauhdikas Vespajetti", "Ajoneuvot", 1),
        new Kerailykortti("Aloittelijan Ameeba", "Eläimet", 1),
        new Kerailykortti("Mieletön Merihevonen", "Eläimet", 2),
        new Kerailykortti("Nopea Nopsa", "Ajoneuvot", 2)
    );
    IO.println("Ennen järjestämistä:");
    kortit.forEach(IO::println);

    //HIGHLIGHT_GREEN_BEGIN
    Collections.sort(
            kortit,
            Comparator.comparing(Kerailykortti::getSarja)
                    .thenComparing(Kerailykortti::getNimi)
    );
    //HIGHLIGHT_GREEN_END

    IO.println("\nJälkeen järjestämisen nimen mukaan:");
    kortit.forEach(IO::println);
}
// FILE_END
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private String sarja;
    private int tunnistenumero;

    public Kerailykortti(String nimi, String sarja, int tunnistenumero) {
        this.nimi = nimi;
        this.sarja = sarja;
        this.tunnistenumero = tunnistenumero;
    }

    // HIGHLIGHT_GREEN_BEGIN
    public String getNimi() {
        return nimi;
    }

    public String getSarja() {
        return sarja;
    }
    // HIGHLIGHT_GREEN_END

    @Override
    public String toString() {
        return "Kortti: " + nimi + " (Sarja: " + sarja + ", #" + tunnistenumero + ")";
    }
}
// FILE_END
```

Huomaa kaksi merkittävää asiaa. Järjestysmedotille `Collections.sort` annetaan
erikseen `Comparator`-olio toisena argumenttina. Toinen merkittävä seikka on,
että `Kerailykortti`-luokkaan on lisätty getter-metodit `getNimi` ja `getSarja`,
jotta `Comparator`-rajapinnan lambda-lausekkeet voivat käyttää näitä kenttiä
vertailuun.

_Comparator_ ei näe luokan yksityisiä kenttiä suoraan, joten getter-metodit ovat
välttämättömiä. Tässä on yksi syy miksi getterit ovat hyödyllisiä, vaikka luokan
sisällä ei olisikaan tarvetta muuttaa kenttien arvoja.

Vielä yksi asia `Comparator`:sta. Aiemmin käyttämämme
`Collections.sort`-metodille hieman lyhyempänä vaihtoehtona voimme käyttää
`List`-rajapinnan tarjoamaa
[`sort(Comparator)`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/List.html#sort(java.util.Comparator))-metodia
listaolioille.

```java
// FILE: main.java
void main() {
    List<Kerailykortti> kortit = Arrays.asList(
        new Kerailykortti("Loistava Lohikäärme", "Eläimet", 3),
        new Kerailykortti("Vauhdikas Vespajetti", "Ajoneuvot", 1),
        new Kerailykortti("Aloittelijan Ameeba", "Eläimet", 1),
        new Kerailykortti("Mieletön Merihevonen", "Eläimet", 2),
        new Kerailykortti("Nopea Nopsa", "Ajoneuvot", 2)
    );
    IO.println("Ennen järjestämistä:");
    kortit.forEach(IO::println);

    //HIGHLIGHT_GREEN_BEGIN
    kortit.sort(Comparator.comparing(Kerailykortti::getSarja)
            .thenComparing(Kerailykortti::getNimi));
    //HIGHLIGHT_GREEN_END

    IO.println("\nJälkeen järjestämisen nimen mukaan:");
    kortit.forEach(IO::println);
}
// FILE_END
// FILE: Kerailykortti.java
class Kerailykortti {
    private String nimi;
    private String sarja;
    private int tunnistenumero;

    public Kerailykortti(String nimi, String sarja, int tunnistenumero) {
        this.nimi = nimi;
        this.sarja = sarja;
        this.tunnistenumero = tunnistenumero;
    }

    public String getNimi() {
        return nimi;
    }

    public String getSarja() {
        return sarja;
    }

    @Override
    public String toString() {
        return "Kortti: " + nimi + " (Sarja: " + sarja + ", #" + tunnistenumero + ")";
    }
}
// FILE_END
```

Olennainen ero `Collections.sort`:iin verrattuna on, että `List.sort`:lle täytyy
antaa `Comparator` parametrina.