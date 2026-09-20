# Ohjelmointi 2 (Jyväskylän yliopisto)

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

Tämä on Jyväskylän yliopiston Ohjelmointi 2 -kurssin oppimateriaali.
Materiaali on katseltavissa osoitteessa <https://ohjelmointi2.it.jyu.fi>. 

Tehtävien palauttaminen vaatii opintojaksolle
[ilmoittautumisen](https://opinto-opas.jyu.fi/2025/fi/opintojakso/tiep111/). 

## Materiaalin kehittäminen omalla koneella

Sivusto rakennetaan **[Zensicalilla](https://zensical.org)**. Materiaali on
kansiossa `src/`. Työkalut (muunnos, tyylit, skriptit, testit) ovat
git-submodule `zensical/tyokalut`, repo
[kirjatyokalut](https://github.com/ohj-perus-jy/kirjatyokalut), joka on yhteinen
Ohjelmointi 1:n ja Jypeli-ohjeiden kanssa.

```bash
git clone --recurse-submodules https://github.com/ohj-perus-jy/ohj2.git
cd ohj2
git config submodule.recurse true    # git pull ja git switch päivittävät jatkossa myös työkalut
```

Suositeltu tapa on käyttää mukana olevaa DevContaineria. Käynnistä
kehityspalvelin projektin juuresta:

```bash
./zensical/run.sh            # http://localhost:8001, seuraa src/:n muutoksia
./zensical/run.sh 8003       # eri portti
./zensical/run.sh build      # pelkkä rakennus zensical/site/-hakemistoon
./zensical/run.sh test       # testit (pytest + Playwright)
```

DevContainer hakee submodulen ja asentaa Zensicalin hakemistoon
`zensical/.venv` jo kontin luonnissa. Ilman DevContaineria saman tekee
ensimmäinen ajo (tarvittaessa myös `python3-venv`-paketin asennuksen, mihin
tarvitaan sudo); Python 3.11 tai uudempi riittää. Uuden tai muutetun
ASCII-kaavion (`bob`-koodilohko) piirtämiseen tarvitaan `svgbob_cli`, jonka
ajo asentaa itse cargolla (DevContainerissa Rust on valmiina).

**Muokattava sisältö on kansiossa `src/`.** `zensical/docs/` ja
`zensical/site/` ovat generoituja.

Haarat ja julkaisu: `main` on tuotanto (<https://ohjelmointi2.it.jyu.fi>),
`dev` on työhaara ja esikatselu osoitteessa
<https://ohjelmointi2.it.jyu.fi/dev/>. GitHub Actions julkaisee molemmat joka
työnnöllä. Muutokset viedään `dev` → `main` merge-committina.
Ulkoiset linkit tarkistetaan joka työnnössä ja maanantaisin (lychee,
`.github/workflows/links.yml`).

Lisää:

- [zensical/README.md](zensical/README.md): tämän kirjan asetukset
  (`kirja.toml`, `mkdocs.yml`, kaaviot) ja työkalujen päivittäminen
- [kirjatyokalut/README.md](https://github.com/ohj-perus-jy/kirjatyokalut#readme):
  rakenne, asetukset, työkalujen muuttaminen ja testit
- [zensical/KAYTTOONOTTO.md](zensical/KAYTTOONOTTO.md): mitä siirrossa
  mdBookista on vielä tekemättä

## Pikaohje kirjoittamiseen

Sivut kirjoitetaan Markdownilla samalla merkkauksella kuin mdBookin aikana;
työkalut muuntavat sen Zensicalille. Navigaatio on tiedostossa
`src/SUMMARY.md`.

Koodiesimerkit voivat sisältää useita tiedostoja. Käytä `// FILE: filename`- ja 
`// FILE_END`-merkintöjä erottaaksesi eri tiedostot.

```java
// FILE: main.java
public class Ohjelma {
    public static void main() {
        Kissa k = new Kissa("Snowball");
        IO.println(k.getAani());
    }
}
// FILE_END
// FILE: Kissa.java
public class Kissa {
    private String name;

    public Kissa(String name) {
        this.name = name;
    }

    public String getAani() {
        return "Miau!";
    }
}
// FILE_END
```

Koodin korostuksiin voit käyttää merkintöjä `// HIGHLIGHT_COLOR_BEGIN` ja 
`// HIGHLIGHT_COLOR_END`, jossa `COLOR` on jokin seuraavista: `GREEN`, `YELLOW`,
`RED`, `BLUE`.

```java
public class Kissa {
  private String name; 

  // HIGHLIGHT_GREEN_BEGIN
  public Kissa(String name) {
    this.name = name;
  }
// HIGHLIGHT_GREEN_END

// HIGHLIGHT_RED_BEGIN
  public String getAani() { 
// HIGHLIGHT_RED_END
// HIGHLIGHT_YELLOW_BEGIN
    return "Miau!";
// HIGHLIGHT_YELLOW_END
  } 
}
```  

![](src/images/highlight.png)

### Tehtävälohko

Tehtäviä varten on oma `task`-elementti, joka sisältää tehtävän otsikon,
tehtävänannon ja linkin TIM-tehtävään.

````md
<task>
  <task-title>Ydintehtävä: Tulostaminen <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/1-1-1-tulostaminen/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/itkp102/demot/demo1#tehtava_tulostaminen_header">Tee tehtävä TIMissa</a></task-link>
</task>
````

`include`-makro kannattaa kirjoittaa ihan vasempaan reunaan Markdown-ladonnan ongelmien ehkäisemiseksi. 

### Katso myös

- [Työkalujen tukema merkkaus](https://github.com/ohj-perus-jy/kirjatyokalut/blob/main/TAUSTA.md):
  alertit, välilehdet, piilorivit, kaaviot, terminaalinauhoitukset,
  vaiheittainen ohje, Testaa tietosi -visa
- [Zensicalin ohjeet](https://zensical.org/docs/)

## License

Ohjelmointi 2 oppimateriaali © 2025 by Denis Zhidkikh, Sami Sarsa, Antti-Jussi Lakanen, Rauli Ruokokoski, Karri Sormunen is licensed under
[Creative Commons Attribution-ShareAlike 4.0 International][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png

[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

