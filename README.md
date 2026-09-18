# Ohjelmointi 2 (Jyväskylän yliopisto)

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

Tämä on Jyväskylän yliopiston Ohjelmointi 2 -kurssin oppimateriaali.
Materiaali on katseltavissa osoitteessa <https://ohjelmointi2.it.jyu.fi>. 

Tehtävien palauttaminen vaatii opintojaksolle
[ilmoittautumisen](https://opinto-opas.jyu.fi/2025/fi/opintojakso/tiep111/). 

## Materiaalin kehittäminen omalla koneella

- Käytä mukana olevaa DevContaineria. Se käyttää valmista mdBook-työkalukuvaa,
  joka sisältää tarvittavat laajennokset.
- Käynnistä esikatselu DevContainerin sisällä:

```bash
bash ./start.sh
```

- Jos et halua käyttää DevContaineria (esimerkiksi nopeita muokkauksia tai et halua
  ladata isoa DevContainer-kuvaa),
  voit sen sijaan käyttää pelkästään mdbook-työkalua ja sen laajennoksia
  sisältävän Docker-kuvaa. Esimerkiksi materiaalin koko rakentaminen yhdellä komennolla:

  ```bash
  docker run --rm -v .:/workspace \
    ghcr.io/ohj-perus-jy/ohj-mdbook-tooling:runner-latest \
    build
  ```

  Vastaavasti materiaalin avaaminen paikallisesti:

  ```bash
  docker run --rm -it -v .:/workspace -p 3000:3000 \
    ghcr.io/ohj-perus-jy/ohj-mdbook-tooling:runner-latest \
    serve --hostname 0.0.0.0 --port 3000
  ```

### mdBook-työkalukuvan päivittäminen

DevContainer käyttää valmista GHCR-kuvaa
`ghcr.io/ohj-perus-jy/ohj-mdbook-tooling:devcontainer-latest`. Jos mdBook-työkaluja tai
esikäsittelijöitä pitää päivittää, tee muutokset repossa
`ohj-perus-jy/ohj-mdbook-tooling` ja pushaa ne `main`-haaraan. Tämän seurauksena
rakentaminen ja julkaisu tapahtuvat automaattisesti.

Huomaa, että `:devcontainer-latest` on liikkuva tagi: jo käynnissä oleva DevContainer ei päivity
automaattisesti. Päivitetty kuva otetaan käyttöön ajamalla esimerkiksi:

```bash
docker pull ghcr.io/ohj-perus-jy/ohj-mdbook-tooling:devcontainer-latest
```

tai VS Codessa komennolla `Dev Containers: Rebuild and Reopen in Container`.

## Zensical-esikatselu (`dev`-haara)

`main` julkaistaan vielä mdBookilla. `dev`-haarasta rakennetaan samasta
`src/`-puusta **[Zensical](https://zensical.org)**-sivusto esikatseluun
osoitteeseen <https://ohjelmointi2.it.jyu.fi/dev/>; vaihdon työjärjestys on
tiedostossa [zensical/KAYTTOONOTTO.md](zensical/KAYTTOONOTTO.md).

Zensicalin työkalut (muunnos, tyylit, skriptit, testit) ovat git-submodule
`zensical/tyokalut`, repo
[kirjatyokalut](https://github.com/ohj-perus-jy/kirjatyokalut), joka on yhteinen
Ohjelmointi 1:n ja Jypeli-ohjeiden kanssa:

```bash
git submodule update --init           # kloonin tai haaran vaihdon jälkeen
git config submodule.recurse true     # git pull ja git switch päivittävät jatkossa myös työkalut

./zensical/run.sh            # http://localhost:8001, seuraa src/:n muutoksia
./zensical/run.sh build      # pelkkä rakennus zensical/site/-hakemistoon
./zensical/run.sh test       # testit (pytest + Playwright)
```

`run.sh` hakee submodulen ja asentaa Zensicalin ensimmäisellä ajolla. Lisää:
[zensical/README.md](zensical/README.md) ja
[kirjatyokalut/README.md](https://github.com/ohj-perus-jy/kirjatyokalut#readme).

## Pikaohje kirjoittamiseen

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

- [mdBook-ohjeet](https://rust-lang.github.io/mdBook/index.html)
- [KaTeX-ohjeet](https://katex.org/docs/supported)

## License

Ohjelmointi 2 oppimateriaali © 2025 by Denis Zhidkikh, Sami Sarsa, Antti-Jussi Lakanen, Rauli Ruokokoski, Karri Sormunen is licensed under
[Creative Commons Attribution-ShareAlike 4.0 International][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png

[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

