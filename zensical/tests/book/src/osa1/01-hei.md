# Hei, maailma

Sivun sisäinen ankkuri: [alas](#lopuksi). Kuva alihakemistosta:

![Koekuva](../images/kuva.png)

## Monta tiedostoa yhdessä lohkossa

```java,ignore
//FILE: Main.java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hei, maailma!");
    }
}
// FILE_END
// FILE: Valo.java
public class Valo {
}
```

## Ajettava ohjelma

```java
// HIGHLIGHT_GREEN_BEGIN
//-void main() {
IO.println("Hei, maailma!");
// HIGHLIGHT_GREEN_END
//-}
```

## Ohjelma ilman ajonappia

```java,noplayground
IO.println("Tätä ei voi ajaa.");
```

## Monta tiedostoa ajettavana

```java
// FILE: Main.java
// HIGHLIGHT_RED_BEGIN
public class Main { }
// HIGHLIGHT_RED_END
// FILE: Valo.java
//HIGHLIGHT_YELLOW_BEGIN
public class Valo { }
//HIGHLIGHT_YELLOW_END
```

## Käyttöjärjestelmävälilehdet

### [Windows](#tab/win)

Windows-ohje.

***

### [macOS](#tab/mac)

macOS-ohje.

***

### [Valitse](#tab/default)

Tämä lohko jää pois: Zensicalissa yksi välilehti on aina valittuna.

***

## Lopuksi

Luvun viimeinen kappale.
