# Tehtävien lisääminen

## Tehtäväkansion perusrakenne

Tehtävät laitetaan `exercises` -kansion alle omin kansiona. 
Yksittäisen tehtävän tiedostot ja kansiot:

```
exercises/
└── <chnum>-<partnum>-<order>-<task_id>
    ├── exercise-details.yml
    ├── handout.md
    ├── starter
    │   └── Tehtava.cs
    ├── solution
    │   └── Tehtava.cs
    └── test
        └── <testitiedostoja>
```

Muuttujat ja niiden selitykset

- `<chnum>`: Osan numero, johon tehtävä kuuluu
- `<partnum>`: Alaosan numero, johon tehtävä kuuluu
- `<order>`: Tehtävän suhteellinen järjestys alaosan sisällä
- `<task_id>`: Uniikki tehtävän tunnus

Esimerkiksi `5-1-1-positiiviset_ja_negatiiviset`.

`<task_id>` ei saa sisältää välilyöntejä eikä muita erikoismerkkejä. 

## Tehtävän rakenteen määrittely: `exercise-details.yml`

Jokaisessa tehtävässä on oltava `exercise-details.yml` -tiedosto.

Alla esimerkki tiedostosta ja kaikista tuetuista attribuuteista:

**Koodaustehtävä**

```yml
# Pakollinen kenttä: Tehtävän tyyppi. Skeeman mukaan tämän on oltava "code".
exercise_type: code

# Pakollinen kenttä: Tehtävän nimi.
# Tämä on nimi, joka näytetään opiskelijoille.
title: "Hei Maailma -esimerkki"

# Pakollinen kenttä: Tehtävän maksimipisteet.
points: 1

# Pakollinen kenttä: Koodaustehtävän tarkistin.
# Tämä määrittelee käytetyn ohjelmointikielen ja ajoympäristön.
# Yleisiä arvoja: "csharp", "java", "jypeli", "python"
type: csharp

# Vapaaehtoinen kenttä: Arviointiasetukset.
# Määrittelee, miten tehtävästä saa pisteitä.
grading:
  # Vapaaehtoinen kenttä: Pisteet odotetusta tulosteesta.
  # Kuinka monta pistettä annetaan, jos ohjelman tuloste vastaa
  # test/expected_output.txt -tiedostoa.
  # "auto" tarkoittaa 1 pistettä, jos tiedosto on olemassa, muuten 0.
  # Voi olla myös kiinteä luku (esim. 0.5).
  expected_output: auto

  # Vapaaehtoinen kenttä: Pisteet ohjelman tulosteesta.
  # Jos true, pisteet yritetään lukea ohjelman tulosteesta (etsitään "RANDOMCHECK: ...").
  # Oletusarvo on false.
  read_from_program: false

  # Vapaaehtoinen kenttä: Itsearviointi.
  # Jos true, opiskelija voi asettaa pisteet itse.
  # Oletusarvo on false.
  self_grading: false

  # Vapaaehtoinen kenttä: Yksikkötestit.
  # Voi olla kiinteä pistemäärä (esim. 1.0) tai asetusobjekti.
  unit_test:
    # Kuinka monta pistettä yksikkötesteistä voi saada.
    points: 1.5
    # Kuka testit määrittelee.
    # "teacher": Opettajan määrittelemät testit ("Aja opettajan testit").
    # "student": Opiskelijan määrittelemät testit ("Aja omat testit").
    source: teacher

# Vapaaehtoinen kenttä: Näytetäänkö koodi tiivistettynä.
# Jos true, "Näytä koko koodi" -painikkeella piilotettu koodi näytetään aina.
# Oletusarvo on false.
view_collapsed_code: true
```

**Monivalintatehtäväsarja**

**TODO**


## Alkukoodi ja mallivastaus

Opiskelijalle näkyvät alkukoodit laitetaan kansioon `starter`.
Vastaavasti mallivastaus laitetaan kansioon `solution`.

Hyödyllisiä huomioita:

- Jos kansioissa on useita tiedostoja, lisätään ne kaikki mukaan alkukoodiin ja mallivastauksiin.
- Jos tehtävässä on oma arvostelukoodi (`test/run`-kansio), testauskoodi liitetään mukaan alkukoodin mukaan
  Silloin voi olla tarve arvostelukoodin pääohjelma käyttäjän ohjelman sijaan. Tällaisissa tapauksissa alkukoodin pääohjelma voi
  lisätä `NORUNBEGIN`/`NORUNEND` -lohkoon, jolloin koodi näytetään käyttäjälle mutta ei sisällytetä mukaan ajoon.
  Esimerkiksi:

  ```csharp
  public class Ohjelma
  {
        // NORUNBEGIN
        public static void Main()
        {
            Console.WriteLine(Summa(1, 2));
        }
        // NORUNEND

        // BYCODEBEGIN
        // Toteuta Summa-aliohjelma tähän
        // BYCODEEND
  }
  ```

  Tällöin Aja-painiketta painaessa palvelimella ajetaan seuraava koodi:

  ```csharp
  public class Ohjelma
  {
        // Toteuta Summa-aliohjelma tähän
  }
  ```

  Tämän avulla testaajakoodi voi määrittää oman Main-aliohjelman, jota voidaan ajaa.

## Testit ja arviointi

`test`-kansioon voi lisätä koodin testaamiseen ja arviointiin liittyviä tiedostoja.

Tällä hetkellä tuetut tiedostot ja kansiot:

- `expected_output.txt` - Ohjelman odotettu tuloste
- `run` - Kansio, jonka sisällä olevat kooditiedostot liitetään osaksi alkukoodia. Hyödyllinen `grading.read_from_program` -asetuksen kanssa.