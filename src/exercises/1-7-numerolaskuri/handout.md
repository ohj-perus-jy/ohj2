Tee ohjelma, joka kysyy käyttäjältä syötteen ja tulostaa,
kuinka monta kertaa kukin numero (0–9) esiintyy syötteessä.

Esimerkiksi, jos käyttäjä antaa syötteenä `12223`, ohjelma tulostaa:

```
1: 1 kpl
2: 3 kpl
3: 1 kpl
```

Vastaavasti, jos syötteenä annetaan `10002244412`, ohjelma tulostaa.

```
0: 3 kpl
1: 2 kpl
2: 3 kpl
4: 3 kpl
```

Tulostamisen jälkeen ohjelma kysyy käyttäjältä uuden syötteen.
Jos käyttäjä antaa tyhjän syötteen, ohjelman suoritus päättyy.

<details>
<summary>Vinkki</summary>

Yksittäisen merkin saa muunnettua kokonaisluvuksi 
yhdistämällä
[`Character.toString`](https://docs.oracle.com/en/java/javase/25/docs/api//java.base/java/lang/Character.html#toString())
ja
[`Integer.parse`](https://docs.oracle.com/en/java/javase/25/docs/api//java.base/java/lang/Integer.html#parseInt(java.lang.String)):

```java,ignore
int numeroLukuna = Integer.parseInt(Character.toString(a));
```

Huomaa, että `Integer.parseInt` olettaa, että annettu merkkijono on 
todellakin numero; jos se sisältää jotain muuta kuin numeroa, 
funktio heittää virheen.
Voit tarkistaa, että onko yksittäinen merkki numero käyttämällä
`Character.isDigit`-funktiota.

</details>
