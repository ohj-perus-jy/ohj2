# Kokoelmien käsittely: Stream API

> [!VAROITUS]
> Tämä osio julkaistaan 16. helmikuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Ainakin map, filter, reduce
> - lambda-lausekkeiden käyttö Stream API:ssa
> - `Stream`, `IntStream`, ero iteraattoreihin


Olemme toistaiseksi käyttäneet silmukoita datan käsittelyyn.
Jos haluaisimme esimerkiksi laskea listan alkioiden summan,
kirjoittaisimme sen tavallisesti näin:

```java
//-void main() {
List<Integer> numeroita = List.of(409, 18, 17, -92, 67, 42, -41);
int summa = 0;
for (int numero : numeroita) {
    summa += numero;
}
IO.println("Summa: " + summa);
//-}
```

Tällaista ohjelmointitapaa kutsutaan *imperatiiviseksi*, eli kirjoitamme
koodiin, mitä tietokoneen pitäisi tehdä vaihe vaiheelta 
päästäkseen haluttuun lopputulokseen.

Etenkin datan prosessoinnissa on useimmin helpommin käsitellä data
*deklaratiivisesti* eli kirjoittamalla, millaisen lopputuloksen halutaan.
Javan Stream API tarjoaa deklaratiivisen tavan käsitellä kokoelmia ja
tietovirtoja lambdalausekkeiden avulla. 
Sen avulla yllä oleva silmukka voidaan korvata yhdellä rivillä:

```java
//-void main() {
List<Integer> numeroita = List.of(409, 18, 17, -92, 67, 42, -41);
int summa = numeroita.stream().mapToInt(i -> i.intValue()).sum();
IO.println("Summa: " + summa);
//-}
```

## Perusajatus Stream API takana

Tarkastellaan yllä olevaa esimerkkiä tarkemmin.
Huomaamme ensin, että yksi rivi koostuu kolmesta metodikutsusta:

```java,ignore
numeroita                       // Käsiteltävä lista
  .stream()                     // 1.
  .mapToInt(i -> i.intValue())  // 2.
  .sum();                       // 3.
```

Tarkastellaan jokainen vaihe kerrallaan.

**1. Kokoelman muuntaminen striimiksi**

Aivan alkuun muunnamme numerolistan `Steam`-olioksi eli striimiksi.
Striimin voi ajatella ikään kuin koneena, joka
ottaa kokoelman ja tuottaa yhden alkion kerrallaan *tietovirtana*:

```bob
\   42   /
 \  67  /
  \ -92/
   \17/           tietovirta -->
+---\/---+         
|        |      .---.       .---.  
| Stream |-----( 18  )-----( 409 )----->
|        |      `---'       `---' 
+--------+
```


**2. Käsittelijä, joka muuntaa `Integer`-alkiot `int`-alkiloiksi**

Striimien tärkein työkalu ovat erilaiset *käsittelijät*, jotka ovat yksittäisiä
alkioita käsiteltäviä funktioita.
Käsittelijät ottavat yhden alkion kerrallaan ja voivat tuottaa
yhden tai useamman uuden alkion tietovirtaan.
Voit ajatella käsittelijät ikään kuin koneina, jotka ottavat sisään alkioita
tietovirrasta ja tuottaavat tietovirtaan uusia alkioita.

Esimerkiksi `mapToInt` on käsittelijä, joka ottaa alkion, korvaa alkion
kokonaisluvulla annetun lambdalausekkeen avulla ja tuottaa tietovirtaan
tuotetun kokonaisluvun alkuperäisen alkion sijaan:

```bob
\   42   /
 \  67  /
  \ -92/
   \17/           tietovirta -->
+---\/---+         
|        |      .---.       .---.  
| Stream |-----( 18  )-----( 409 )----->
|        |      `---'       `---' 
+--------+
```