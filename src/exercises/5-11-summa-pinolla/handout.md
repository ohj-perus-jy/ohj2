Laske lukujen 1 + 2 + ... + n summa **ilman rekursiota** käyttäen omaa pinoa.

Lähtökohtana on rekursiivinen määritelmä:

```java,ignore
int summa(int n) {
    if (n == 0) return 0;
    return n + summa(n - 1);
}
```

Kirjoita metodi `summaIteratiivisesti(int n)`, joka palauttaa saman tuloksen.
Mallinna rekursiota pinon avulla: talleta pinoon luvut, jotka "odottavat"
paluuvaiheessa. Käytä pinon toteutukseen `ArrayDeque`-toteutusta. Et tarvitse
tässä vielä `Kehys`-olion kaltaista rakennetta.
