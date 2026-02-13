Toteuta kokonaislukuja sisältävän binääripuun solmujen summan laskenta **ilman
rekursiota** käyttäen omaa pinoa. Käytä oheista `Solmu`-luokkaa.

```java,ignore
public class Solmu {
    int arvo;
    Solmu vasen;
    Solmu oikea;

    Solmu(int arvo) {
        this.arvo = arvo;
    }
}
```

Lähtökohtana on rekursiivinen määritelmä:

```java,ignore
int summa(Solmu juuri) {
    if (juuri == null) return 0;
    return juuri.arvo + summa(juuri.vasen) + summa(juuri.oikea);
}
```

Mallinna rekursiota pinon avulla: jokainen pinon alkio vastaa rekursiivisen
kutsun tilaa. Tätä varten tarvitset `Kehys`-luokan (esim. `Solmu` ja `kayty`),
jolla ylläpidetään tilatietoa. Pinoa ei tarvitse toteuttaa, vaan voit käyttää
`ArrayDeque`-toteutusta, kuten materiaalissakin. 

Esimerkkipääohjelma on mukana TIM-tehtävässä. 
