# Tyyppiparametrit ja geneerisyys

> [!Osaamistavoitteet]
>
> - Osaat hyödyntää tyyppiparametreja toteuttaaksesi yleiskäyttöisiä eli geneerisiä luokkia ja metodeja

## Tyyppiparametrit 

- Näitä on käytetty mm. listoissa `List<Integer>`
- Mitä geneerisyydellä (generic programming / generics) tarkoitetaan?

- Viittaus edellisen osan polymorfismiasiaan
  - Polymorfismi olio-ohjelmoinnissa tarkoittaa tyypillisesti nimenomaan alityypitystä
- Tyyppiparametrit ja geneerisyys ovat myös polymorfismia, sillä periaate on sama:
  - Mahdollistaa, että yksi arvon tyyppi edustaa useita eri tyyppejä
    - Voi luoda luokkia, rajapintoja ja metodeita jotka hyödyntävät ulkopuolelta (muualta koodista) tulevia arvoja määrittämättä tarkkaa tyyppiä etukäteen.
  - Parametrinen polymorfismi

- Miksi tyyppiparametrit ja geneerisiä tyyppejä (tyyppiparametrisoituja luokkia tai rajapintoja), kun on jo polymorfismi alityypeillä?

- Tarkastellaan metodin parametrin yhteydessä hieman luokkaa `Object`, joka itsessään on "geneerinen", eli yleinen luokka — (kertauksena) kaikki Javan luokat perivät `Object`-luokan eli ovat tyyppiä `Object`.

```java
void main() {
    printWithType(new Object());
    printWithType("tekstiä");
    printWithType(1);
    printWithType(1.0);
}

void printWithType(Object value) {
    System.out.println("Arvo: " + value + ", Tyyppi: " + value.getClass().getSimpleName());
}
```

- Vastaava geneerinen metodi tyyppiparametrilla `T`:

```java
void main() {
    printWithType(new Object());
    printWithType("tekstiä");
    printWithType(1);
    printWithType(1.0);
}

<T> void printWithType(T value) {
    System.out.println("Arvo: " + value + ", Tyyppi: " + value.getClass().getSimpleName());
}
```

- `<T>` syntaksi tuttu esimerkiksi listoista: `List<String> = new ArrayList()<>`.

- Ylemmänkaltaisessa käyttötapauksessa ei vielä eroa.

- Katsotaan seuraavaksi seuraavaksi potentiaalista ongelmaa ohjelmakoodin toteutuksessa alityyppien avulla. Samalla tutustumme _rajoitettuihin_ tyyppiparametreihin.

- Pelkkä alityypitys mahdollistaa:

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    int suurempi = getLargest("1", "2")); // kääntäjälle ok
    System.out.println("Suurempi: " + getLargest("5", 4)); // kääntäjälle ok
}

Comparable getLargest(Comparable a, Comparable b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}
```

-> Ajonaikainen virhe, halutaan yleensä välttää sillä näissä on aina riski päätyä loppukäyttäjälle

- Tyyppiparametrien avulla (ja niiden järkevällä käytöllä) tämänkaltainen metodin väärinkäyttö havaitaan varmasti ajoissa

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    int suurempi = getLargest("1", "2")); // virhe havaitaan viimeistään kääntäessä
    System.out.println("Suurempi: " + getLargest(3, "5")); // virhe havaitaan viimeistään kääntäessä
}

<T extends Comparable> T getLargest(T a, T b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}

- Javan `Comparable` on _geneerinen luokka_ ja ottaa tyyppiparametrin, joten oikeampi käyttö olisi

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    int suurempi = getLargest("1", "2")); // virhe havaitaan viimeistään kääntäessä
    System.out.println("Suurempi: " + getLargest(3, "5")); // virhe havaitaan viimeistään kääntäessä
}

<T extends Comparable<T>> T getLargest(T a, T b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}

- Rajoitettuja tyyppiparametreja voi olla useampia, esim.

```java
void main() {
    printWithType(1);
    printWithType(1.0);
    printWithType(new Object());

    String suurempi = getLargest("1", "2")); // virhe havaitaan viimeistään kääntäessä
}

<T extends Comparable<T> & Number> T getLargest(T a, T b) {
    if (a.compareTo(b) >= 0) {
        return a;
    } else {
        return b;
    }
}

Tästä päästäänkiin geneerisiin luokkiin ja rajapintoihin.

- Klassinen esimerkki geneerisestä :

```java
class Pair<T> {
    private T first;
    private T second;

    public Pair(T first, T second) {
        this.first = first;
        this.second = second;
    }

    public T getFirst() {
        return first;
    }

    public T getSecond() {
        return second;
    }

    public void setFirst(T first) {
        this.first = first;
    }

    public void setSecond(T second) {
        this.second = second;
    }
}
```

Tyyppiparametreja voi olla useampi

```java
class Pair<T, U> {
    private T first;
    private U second;

    public Pair(T first, U second) {
        this.first = first;
        this.second = second;
    }

    public T getFirst() {
        return first;
    }

    public U getSecond() {
        return second;
    }

    public void setFirst(T first) {
        this.first = first;
    }

    public void setSecond(U second) {
        this.second = second;
    }
}
```


- Geneerisen metodin syntaksi (geneeriset esimerkit vasta ongelman havainnollistuksen jälkeen vai samassa?)
- Tyyppirajoitukset (tämä vasta myöhemmin vai Comparable-esimerkin kanssa?

- Tyyppiparametrit mahdollistavat eritasoista tyyppitarkastusta ja yleiskäyttöisen koodin kehittämistä kuin mitä pelkällä alityypityksellä on mahdollista

- Esimerkkejä milloin geneeriset tyypit ovat kivoja metodeissa
  - Identtinen overloadaus eri tyypeille
    - tässä myös miksi overloadaus on myös polymorfismia?

- Tehtäviä geneerisistä metodeista

- Esimerkkejä milloin geneeriset tyypit ovat kivoja luokissa
- Geneerisen luokan syntaksi

- Tehtäviä geneerisitä luokista

- Ekstramaininta: Javassa geneeriset tyypit muuten ohjelman kääntämisen aikana rajoituksen tyypiksi tai tyypiksi `Object`
- Ekstramaininta: (koska vain Java -asia): Geneerinen tyyppi ei voi olla primitiivi

- Ei unionityyppejä (kuten esimerkiksi Rustissa), täytyy tehdä luokka esim. StringOrInt

```java
class StringOrInt {
    private final Object value;

//    public StringOrInt(Object value) {  // ei näin -> ajonaikaiset virheet voidaan estää helposti kahdella konstruktorilla
//        if (!(value instanceof String) && !(value instanceof Integer)) {
//            throw new IllegalArgumentException("Value must be a String or an Integer");
//        }
//        this.value = value;
//    }

    public StringOrInt(String value) {
        this.value = value;
    }

    public StringOrInt(Integer value) {
        this.value = value;
    }

    public Object getValue() {
        return value;
    }

    public String getStringValue() {
        if (value instanceof String s) {
            return s;
        } else if (value instanceof Integer i) {
            return Integer.toString(i);
        } else {
            throw new IllegalStateException("Value is neither String nor Integer");
        }
    }

    public boolean isString() {
        return value instanceof String;
    }

    public boolean isInteger() {
        return value instanceof Integer;
    }

    public int getIntValue() {
        if (value instanceof Integer i) {
            return i;
        } else if (value instanceof String s) {
            try {
                return Integer.parseInt(s);
            } catch (NumberFormatException e) {
                throw new IllegalStateException("String value cannot be parsed to Integer");
            }
        } else {
            throw new IllegalStateException("Value is neither String nor Integer");
        }
    }
}
```

- Menee kikkailuksi, parempi tyytyä rajapintoihin ja abstrakteihin luokkiin
