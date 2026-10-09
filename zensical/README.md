# Zensical

Ohjelmointi 2 -materiaalin sivusto rakennetaan **Zensicalilla** (Material for
MkDocsin tekijöiden generaattori). Lähdepuu on `../src`.

Työkalut (`convert.py`, `puhe.py`, tyylit, skriptit, teeman mallit, testit)
ovat git-submodule [`tyokalut/`](https://github.com/ohj-perus-jy/kirjatyokalut),
yhteinen ohj1:n ja Jypeli-ohjeiden kanssa:

- ominaisuudet, käyttö, asetukset, työkalujen muuttaminen ja testit:
  [tyokalut/README.md](tyokalut/README.md)
- ratkaisujen perustelut: [tyokalut/PERUSTELUT.md](tyokalut/PERUSTELUT.md)
- mistä ominaisuudet tulivat (koeputken README tarkistuslistoineen; tämän
  tiedoston aiempi sisältö on gitin historiassa):
  [tyokalut/TAUSTA.md](tyokalut/TAUSTA.md)
- merkkauksen siirto mdBookin syntaksista Zensicalin omaan (mikä on tehty ja
  mikä jää) ja avoimet kysymykset:
  [tyokalut/YHTENAISTYS.md](tyokalut/YHTENAISTYS.md)

Mitä ohj2:ssa on vielä tekemättä: [../TODO.md](../TODO.md).

## Käynnistys

```bash
./zensical/run.sh              # http://localhost:8001, vahtii ../src:ää
./zensical/run.sh 8003         # eri portti
./zensical/run.sh build        # pelkkä rakennus site/-hakemistoon
./zensical/run.sh test         # testit: koekirja ja tämä kirja
./zensical/run.sh puhe         # ääneenluvun leikkeet (kirja.toml: [puhe]);
                               # --teksti ei tee ääniä
```

Ääneenluku on kokeiluna yhdellä sivulla (`osa1/02-muuttujat-ja-tietotyypit.md`).
Leikkeiden tekeminen tarvitsee Azure Speech -avaimen (`AZURE_SPEECH_KEY`,
`AZURE_SPEECH_REGION`); käännös ja julkaisu eivät tarvitse. Leikkeet ovat
erillisessä repossa [ohj2-puhe](https://github.com/ohj-perus-jy/ohj2-puhe),
jonka `puhe` kloonaa kansioon `zensical/puhe/` ja johon se pushaa uudet
leikkeet; julkaisu hakee sen samaan kansioon.

Kloonin tai haaran vaihdon jälkeen submodule haetaan komennolla
`git submodule update --init` (`run.sh` tekee sen itse, jos hakemisto on
tyhjä). `git pull` ja `git switch` eivät päivitä submodulea;
`git config submodule.recurse true` korjaa sen tässä kloonissa. `run.sh`
huomauttaa, jos `tyokalut/` on eri versiossa kuin haara odottaa.

**Muokattava puu on `../src`, ei `docs/`.**

## Tämän kirjan omat tiedostot

- `kirja.toml`: kirjan asetukset työkaluille: ääneen luettavat sivut ja
  äänivarasto (`[puhe]`) sekä testien sallima puuttuva kuva
  (`[testit] rikkinaiset_kuvat`).
- `mkdocs.yml`: `site_name`, `site_url`, `copyright` ja `repo_url`.
  Sivustovalikkoa (`extra.sites`) ei ole, joten kurssin nimi on pelkkä linkki
  etusivulle. Teema, tyylit ja skriptit tulevat työkalujen
  `mkdocs-pohja.yml`:stä generoidun `nav.yml`:n kautta.
- `cache/mermaid/`: mermaid-kaaviot (luokkakaaviot ym.), jotka `convert.py`
  piirtää beautiful-mermaidilla (Node-paketti `tyokalut/mermaid/`, jonka
  `convert.py` asentaa npm:llä; devcontainerin kuvassa Node on valmiina).
- `cache/svgbob/`: bob-kaaviot (svgbob_cli 0.7.6, jonka `convert.py` asentaa
  cargolla; devcontainerin kuvassa Rust on valmiina).

  Kaaviot ovat versionhallinnassa, ja tiedoston nimi on kaavion lähteen sha1.
  Uusi tai muutettu kaavio piirretään paikallisesti
  (`./zensical/run.sh build`), ja syntynyt tiedosto committoidaan (samoin
  vanhan poisto). Julkaisu ei asenna svgbobia, ja sen `convert.py --strict`
  kaatuu, jos kaavio puuttuu eikä sitä saada.
- `run.sh`: kääre, joka kutsuu `tyokalut/run.sh`:ta.

## Työkalujen päivittäminen

```bash
git -C zensical/tyokalut pull origin main
git add zensical/tyokalut && git commit -m "Työkalut: ..."
```

Jokainen haara kiinnittää oman työkaluversionsa. `.github/workflows/pages.yml`
kääntää samalla ajolla `main`in ja `dev`in, joten rakennetta koskeva muutos
viedään molempiin samalla työnnöllä: osoitin päivitetään `main`iin ja
yhdistetään `main` → `dev` merge-commitilla (ks. ../CONTRIBUTING.md).
