# Ohjelmointi 2 (Jyväskylän yliopisto)

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

Tämä on Jyväskylän yliopiston Ohjelmointi 2 -kurssin oppimateriaali.
Materiaali on katseltavissa osoitteessa <https://ohjelmointi2.it.jyu.fi>. 

Tehtävien palauttaminen vaatii opintojaksolle
[ilmoittautumisen](https://opinto-opas.jyu.fi/2025/fi/opintojakso/tiep111/). 

## Materiaalin kehittäminen omalla koneella

- Asenna Rust ja Cargo (esim. rustup) TAI käytä mukana olevaa DevContaineria
- Aja ´update-mdbook.sh´ asentaakseen tarvittavat laajennokset

```bash
bash ./start.sh
```

tai

```bash
bash ./update-mdbook.sh
mdbook serve --hostname 0.0.0.0 --port 3000 --open
```

## Pikaohje mdBookin syntaksiin

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

