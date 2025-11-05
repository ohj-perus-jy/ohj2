# Ohjausrakenteet

> [!Osaamistavoitteet]
>
> - Kerrataan lyhyesti rakenteisen ohjelmoinnin perusteet
> - Ehtolauseet (`if`, `switch`)
> - Toistolauseet (`for`, `while`, `do-while`), ja listatyyppiset tietorakenteet
> - Tiedostat, että Javassa merkkijonot verrataan `equals`-aliohjelmalla eikä `==`

## Ehtolauseet


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
Javasta löytyy 4 eri silmukkaa for, while, do-while ja foreach

## Listat

## Merkkijonojen vertailu