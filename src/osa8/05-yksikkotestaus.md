# Yksikkötestaus

Nyt sovellus sisältää jo useita kerroksia (malli, repository, viewmodel).
Ilman testejä regressioiden riski kasvaa nopeasti.

Tässä luvussa rakennetaan yksikkötestit erityisesti niihin osiin, jotka eivät
vaadi JavaFX-käyttöliittymän käynnistämistä.

## Mitä kannattaa testata?

`Model`

- oletusarvot (uusi tehtävä on tekemätön)
- kenttien asettaminen/getterit

`ViewModel`

- tyhjän tehtävän lisäys estetään
- tehtävä lisätään trimmatulla otsikolla
- poisto toimii valitulle tehtävälle

`Repository`

- tallennus ja lataus onnistuu
- puuttuva tiedosto käsitellään hallitusti

## JUnit 5 -esimerkki ViewModelille

```java
class TodoViewModelTest {

    @Test
    void lisaaTehtava_hylkaaTyhjan() {
        TodoViewModel vm = new TodoViewModel(new InMemoryRepository());

        vm.lisaaTehtava("   ");

        assertEquals(0, vm.getTehtavat().size());
    }

    @Test
    void lisaaTehtava_trimmaaTekstin() {
        TodoViewModel vm = new TodoViewModel(new InMemoryRepository());

        vm.lisaaTehtava("  Osta maitoa  ");

        assertEquals(1, vm.getTehtavat().size());
        assertEquals("Osta maitoa", vm.getTehtavat().getFirst().getOtsikko());
    }
}
```

## Repositoryn integraatiotyyppinen testi

Testaa tallennus/lataus kierroksena:

```java
@Test
void jsonRepository_roundtrip() throws IOException {
    Path temp = Files.createTempFile("todo", ".json");
    JsonTehtavaRepository repo = new JsonTehtavaRepository(temp);

    List<TehtavaDto> alku = List.of(
            new TehtavaDto("A", "kuvaus", false, "KESKI")
    );
    repo.tallenna(alku);
    List<TehtavaDto> luettu = repo.lataa();

    assertEquals(1, luettu.size());
    assertEquals("A", luettu.getFirst().otsikko());
}
```

## Testattavuuden perussääntö

Mitä vähemmän logiikkaa on controllerissa, sitä helpompi sovellus on testata.
Siksi tämä osa painottaa ViewModeliin siirrettyä logiikkaa.

## Ennen harjoitustyön vaihe 2 palautusta

Varmista vähintään:

- `mvn test` menee läpi
- tehtävän lisäys, poisto, muokkaus ja tallennus toimivat
- sovellus käynnistyy ilman vanhaa `tehtavat.json`-tiedostoa

<task>
  <task-title>Tehtävä 8.5: TODO-ohjelma, vaihe 11. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/8-5-todo-11/handout.md}}

  </handout>
</task>
