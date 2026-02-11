
## Listaluvusta

> [!WIP]
> - Otetaan pohjaa seuraavista lähteistä
>    - <https://docs.oracle.com/javase/tutorial/collections/>
>    - <https://dev.java/learn/api/collections-framework/>
>    - <https://www.cs.helsinki.fi/u/ahslaaks/kkkk.pdf>

> [!Osaamistavoitteet]
>
> TODO: Pitäisikö olla sen sijaan ohjattu tehtävä?
> TAI: Voisi tehdä Full Stack Moocin tavoin ohjatusti ja sitten
>      tehtävänä on tehdä LinkedList tai HashMap.
> Vrt. myös [HY](https://java-programming.mooc.fi/part-12/2-arraylist-and-hashtable)
> 


> [!WIP]
> Tehdään esimerkkien kautta
> - Tehdään `Lista<T>`-luokka ja sille attribuutiksi taulukko
> - Katsotaan, mitkä ovat olennaisimmat listan toiminnan kannalta olevat metodit ja toteutetaan ne järjestyksessä
>     - `get(index)` -> suoraan
>     - `size()` -> suoraan
>     - `isEmpty()` -> tehtävänä
>     - `set(index, element)` -> suoraan
>     - `contains(object)` -> tehtävänä
>     - `indexOf(object)` -> tehtävänä
>     - `iterator()` -> suoraan tai tehtävänä



## Vanhaa tekstiä...

> [!WIP]
> Tehdään esimerkkien kautta
> - Toteutetaan järjestyksessä
>     - `add(e)` -> yllä olevan kuvauksen kautta
>     - `remove(e)` -> yllä olevan kuvauksen kautta
>     - `remove(index)` -> tehtävänä
>     - `size()`, `isEmpty()` ja muiden aiempien metodien päivitys -> tehtävänä

- Lopuksi huomioita
  - Toteutus ei vielä lopullinen, sillä `List`-rajapinta paljon laajempi

> [!WIP]
> Mahdollinen ajatus bonus- tai guru-tason tehtäväksi: toteuta itse tehtyyn listaan
> loput `Collection<T>`-rajapinnan pakolliset metodit, jotta itse tehtyä listaa voi käyttää kokoelmana.
>  - `contains`, `containsAll`, `equals`, `hashCode`, `isEmpty`, `iterator`, `size`, `toArray`

## Listan toteutuksia

- Yleisiä toteutuksia listalle
   - `ArrayList` - lista, jossa alkiot tallenetaan taulukkoon
      - kun taulukosta loppuu tila, luodaan uusi taulukko
      - kaikki operaatiot toteutettu taulukko-operaatioina
      - Erityishuomiot operaatioista
        - Uuden alkion lisääminen listan loppuun on keskimäärin O(1) mutta pahimmillaan O(n)
        - Lisääminen alkuun aina O(n), listan väliin keskimäärin O(n)
        - Alkion hakeminen indeksin perusteella O(1)
        - Plussaa: alkiot sijaitsevat tietokoneen muistissa aina lähekkäin, jolloin käyttöjärjestelmä pystyy optimoimaan muistin käyttöä
   - `LinkedList` - lista, jossa jokainen alkio sisältää arvon ja viitteen seuraavaan ja edelliseen alkioon
      - Alkiot muodostavat ikään kuin "ketjun", jota pitkin voi liikkua
      - Erityishuomiot operaatioista
        - Lisääminen loppuun ja alkuun on nopeaa O(1)
        - Poistaminen lopusta ja alusta on myös nopeaa O(1) -> soveltuu jonoksi, josta oma luku
   - Muuttumattomat listat `List.of`-metodilla


## Mitä rekursio tarkoittaa yleisellä tasolla

Rekursiivinen ongelmanratkaisu voidaan jakaa kahteen vaiheeseen:

1) Perustapaus:
- Jos ongelma on riittävän helppo, ratkaise se ja palauta vastaus.

2) Rekursiivinen tapaus:
- Muunna ongelmaa hiukan helpommaksi ja välitä se seuraavalle ratkaisijalle

(Hiukan erilainen sanoitus)
1. Voinko ratkaista tämän nyt?
2. Jos en, miten teen ongelmasta helpomman ja lähetän sen eteenpäin?

- Ongelman määrittely itseään pienempien aliongelmien avulla
- Rekursiivisen funktion rakenne
    - Funktion kutsuminen itseään
    - Parametrien muuttuminen kutsujen välillä

- Esimerkkitehtäviä:
   - Faktoriaali
   - Fibonacci
   - Puun tai listan läpikäynti

## Rekursio pinon avulla
Kutsupino (call stack)
- Miten funktiokutsut tallentuvat pinoon
- Paikallisten muuttujien elinkaari

Rekursion eteneminen pinossa
- Kutsuvaihe (push)
- Paluuvaihe (pop)

Rekursion ja iteratiivisen ratkaisun vertailu
- Rekursio vs. silmukat

Muistin käyttö

```java
void lahtolaskenta(int n) {
    if (n == 0) return;
    IO.println(n);
    lahtolaskenta(n - 1);
}

void main() {
    lahtolaskenta(5);
}
```

- Milloin rekursio pysähtyy
- Tyypilliset virheet (puuttuva tai väärä perustapaus)
    - Ääretön rekursio --> Liian suuret kutsusyvyydet
    - Virheellinen perustapaus

Induktiotapaus (rekursiivinen askel)
- Ongelman pienentäminen
- Oikean etenemissuunnan valinta

## Rekursiiviset tietorakenteet
"Itsensä sisältävää" tietorakennetta voidaan kutsua rekursiiviseksi tietorakenteeksi. Esimerkkejä tällaisista ovat linkitetty lista, puut ja graafit.

- Rekursiiviset algoritmit tietorakenteille
    - Haku
    - Läpikäynti (DFS, preorder, inorder, postorder)

### Hajota ja hallitse
Sopii erityisen hyvin, jos ongelma jakaantuu riippumattomiin aliongelmiin.
- Periaatteen idea
    - Ongelman jakaminen osiin
    - Osaongelmien yhdistäminen
- Rekursion rooli hajota ja hallitse -menetelmässä
- Esimerkkejä algoritmeista
    - Merge sort
    - Quick sort
    - Puolitushaku (engl. *binary search*)

## Pinon käyttö rekursiossa
Rekursiossa pinoa hallinnoi ohjelmointikieli. Iteratiivisessa ratkaisussa sinä itse huolehdit pinon käytöstä.

- Implisiittinen pino (kutsupino)
- Eksplisiittinen pino
    - Rekursion simulointi itse toteutetulla pinolla

## Dynaaminen ohjelmointi?
Dynaaminen ohjelmointi on sekä matemaattinen optimointimetodi ja algoritminen paradigma. 
- Yhteys rekursioon
    - Rekursiivinen määrittely + muistin käyttö
- Päällekkäiset aliongelmat
- Muistitekniikat
    - Memoisaatio
    - Taulukointi (bottom-up)
- Esimerkkejä
    - Fibonacci optimoituna
    - Kapsäkkiongelma (engl. *knapsack problem*) (koliket)

# Ahne algoritmi

Ahne algoritmi on mikä tahansa algoritmi, joka noudattaa heuristiikkaa, jossa jokaisessa tilanteessa valitaan lokaali optimi. Katsotaan seuraavaksi esimerkki ahneesta algoritmista eurovaluutalle

```java
void main() {
    int[] tulos = ahneMenetelma(new int[]{1,2,5,10,20,50}, 4);
    IO.println(Arrays.toString(tulos));
}

// Oletetaan, että yksiköt ovat jo nousevassa järjestyksessä
private int[] ahneMenetelma(int[] valuutat, int tavoite) {
    List<Integer> tulos = new ArrayList<>();
    int jaljella = tavoite;

    for (int i = valuutat.length - 1; i >= 0; i--) {
        int valuutta = valuutat[i];

        int maara = jaljella / valuutta; //Otetaan niin monta kuin mahdollista
        for (int j = 0; j < maara; j++) {
            tulos.add(valuutta);
        }
        jaljella -= maara * valuutta;
    }
    // Tavoite ei mahdollinen
    if(jaljella != 0) return new int[0];
    return tulos.stream().mapToInt(Integer::intValue).toArray();
}
```
Useimmat nykyiset rahayksiköt ovat tarkoituksella suunniteltu siten (kuten euro), että ahne algoritmi antaa optimaalisen tuloksen. Esimerkiksi, jos meillä olisi yksiköt `1,3,4` ahne algoritmi antaa tavoitteelle 6 tuloksen `4+1+1`, eikä globaalia optimia `3+3`:

```java
void main() {
    int[] tulos = ahneMenetelma(new int[]{1,3,4}, 6);
    IO.println(Arrays.toString(tulos));
}

//-private int[] ahneMenetelma(int[] valuutat, int tavoite) {
//-    List<Integer> tulos = new ArrayList<>();
//-    int jaljella = tavoite;

//-    for (int i = valuutat.length - 1; i >= 0; i--) {
//-        int valuutta = valuutat[i];

//-        int maara = jaljella / valuutta; //Otetaan niin monta kuin mahdollista
//-        for (int j = 0; j < maara; j++) {
//-            tulos.add(valuutta);
//-        }
//-        jaljella -= maara * valuutta;
//-    }
//-    // Tavoite ei mahdollinen
//-    if(jaljella != 0) return new int[0];
//-    return tulos.stream().mapToInt(Integer::intValue).toArray();
//-}
```
