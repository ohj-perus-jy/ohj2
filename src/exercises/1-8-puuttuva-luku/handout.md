Tee funktio `int puuttuvaLuku(int[] taulukko)`.
Funktiolle annetaan parametriksi taulukko, joka sisältää
luvut 1-N satunnaisessa järjestyksessä, mutta yksi luvuista puuttuu.
Funktion on palautettava luku, joka puuttuu.
Funktio ei saa aiheuttaa sivuvaikutuksia.

Esimerkiksi:

- `puuttuvaLuku(new int[] { 1, 6, 3, 4, 5 })` palauttaa `2`
- `puuttuvaLuku(new int[] { 8, 2, 4, 1, 3, 5, 6 })` palauttaa `7`
- `puuttuvaLuku(new int[] { })` palauttaa `1`
- `puuttuvaLuku(new int[] { 2 })` palauttaa `1`

Voit käyttää alla olevaa apufunktiota satunnaisen taulukon luomiseksi:

```java,ignore
int[] annaSyote(int maxLuku) {
    Random r = new Random();
    List<Integer> luvut = new ArrayList<>(IntStream.range(1, r.nextInt(2, maxLuku + 1)).boxed().toList());
    Collections.shuffle(luvut);
    luvut.remove(r.nextInt(luvut.size()));
    return luvut.stream().mapToInt(Integer::intValue).toArray();
}
```

Voit käyttää aliohjelmaa seuraavasti:

```java,ignore
// Tekee taulukon luvuista 1-10, mutta yksi luku puuttuu
int[] syote = annaSyote(10); 
// Selvitetään, mikä luvuista puuttuu
int puuttuva = puuttuvaLuku(syote);
```
