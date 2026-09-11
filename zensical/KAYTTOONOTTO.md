# Käyttöönotto: työjärjestys

Zensical tuotantoon ilman, että mdBook-sivusto tai `main` hajoaa välissä.
Mitä `convert.py`:stä puretaan vaihdon jälkeen:
[PURKUSUUNNITELMA.md](PURKUSUUNNITELMA.md).

## Säännöt

1. Zensical elää `dev`-haarassa. Jokainen push `dev`:iin julkaisee sen
   GitHub Pagesiin.
2. `dev` on koko ajan mergettävissä `main`iin ilman isoja konflikteja.
3. PURKUSUUNNITELMA.md:n operaatiot tehdään vasta, kun sääntö 2 on totta
   (vaihe 4).

## Vaihe 0 — `main`iin ensin se, mikä ei ole Zensicalia

Koeputki muuttaa `zensical/`-hakemiston ulkopuolella kolmea asiaa. Ne ensin
pois tieltä.

- [ ] Mergeä `fix/rikkinaiset-linkit` → `main`. Sama patch on koeputkessa
      (`927c27f`), joten merge ei konfliktoi.
- [ ] Päätä `src/SUMMARY.md`:n Tyyliopas-rivi. Koeputki poisti sen sivumennen
      (`f3e51c0`), ja merge poistaisi sen myös mdBookista. Joko oma PR
      `main`iin tai rivi takaisin `dev`:iin.
- [ ] `.gitignore` ja `.devcontainer/devcontainer.json` (portti 8001) ovat
      pelkkiä lisäyksiä. Ne voivat mennä `main`iin sellaisenaan.

Lisäksi yksi sisältökorjaus, joka toimii myös mdBookissa:

- [ ] Korjaa `src/osa1/01-hei-java.md`:n muokattava esimerkki
      (` ```java,editable `) sellaiseksi, ettei se vaadi käyttäjän syötettä.
      ACE-editori on siirretty myöhemmäksi (README, kohta 20), eikä ajonappi
      välitä ohjelmalle syötettä kummassakaan sivustossa, joten
      `IO.readln` ei saa ajossa mitään.

## Vaihe 1 — `dev`-haara

```bash
git switch -c dev spike/zensical
git merge main            # main on 3 committia edellä
git push -u origin dev
git merge-tree --write-tree origin/main origin/dev   # paluuarvo 0 = ei konflikteja
```

## Vaihe 2 — Julkaisu Pagesiin

**Ongelma:** repossa on vain yksi Pages-sivusto. `pages.yml` julkaisee sinne
mdBookin jokaisesta `main`-pushista, ja erillinen `dev`-julkaisu korvaisi koko
sivuston.

**Ratkaisu:** yksi työnkulku, joka rakentaa molemmat samaan artefaktiin.

Sivusto on omassa domainissaan (Settings → Pages), ja
`ohj-perus-jy.github.io/ohj2/` ohjaa sinne. Siksi artefaktin juuri on domainin
juuri.

| Osoite                         | Sisältö                      |
| ------------------------------ | ---------------------------- |
| `ohjelmointi2.it.jyu.fi/`      | mdBook `main`ista, kuten nyt |
| `ohjelmointi2.it.jyu.fi/dev/`  | Zensical `dev`:stä           |

- [ ] Kirjoita `.github/workflows/pages.yml` uusiksi:
  - laukaisin: push `main`iin ja `dev`:iin
  - job `mdbook`: nykyinen kontti, `checkout` refillä `main`, `mdbook build`
    → artefakti. `dev`-pushissa rakennetaan lisäksi `dev` pelkkänä
    tarkistuksena: se todistaa, ettei `dev` riko mdBookia.
  - job `zensical`: `ubuntu-latest` + `actions/setup-python`, `checkout`
    refillä `dev`, `pip install -r zensical/requirements.txt`,
    `python3 convert.py && zensical build` → artefakti
  - job `deploy`: `_site/` + `_site/dev/`, `upload-pages-artifact`,
    `deploy-pages`
- [ ] Vie `pages.yml` **ensin `main`iin**, sitten `main` → `dev`. Tiedoston on
      oltava sama molemmissa: `main`-push ajaa `main`in version, ja vanha
      versio pyyhkisi `/dev/`:n.
- [ ] Settings → Environments → `github-pages` → Deployment branches: lisää
      `dev`. Oletuksena vain oletushaara saa julkaista.
- [ ] Lukitse versio `zensical/requirements.txt`:ssä: `zensical==0.0.60`.
      README kuvaa juuri 0.0.60:n käytöstä, eikä CI saa päivittää sitä
      huomaamatta.
- [ ] Todenna:
  - push `dev`:iin → `/dev/` päivittyy ja juuri on yhä mdBook
  - push `main`iin → molemmat säilyvät
  - `/dev/`-alipolussa: tyylit, ajonappi, tulostus ja asciinema toimivat
    (paikallisesti sivusto on juuressa, joten tätä ei ole vielä nähty)
  - TIM:n linkki aukeaa

CI ei tarvitse `svgbob_cli`:tä eikä PlantUML-palvelinta, koska `cache/svgbob/`
ja `assets/plantuml/` ovat versionhallinnassa. Uusi tai muutettu kaavio: aja
`python3 convert.py` paikallisesti ja committoi molemmat hakemistot. Muuten
bob-kaavio jää CI:ssä koodilohkoksi.

## Vaihe 3 — `dev` pysyy mergettävänä

Voimassa vaihtoon asti.

- [ ] `main` → `dev` vähintään viikoittain ja aina ennen isompaa työtä. Ei
      rebasea, koska `dev` on julkaistu ja jaettu.
- [ ] Zensicalin työ pysyy `zensical/`-hakemistossa.
- [ ] `src/`:hen vain muutoksia, jotka toimivat myös mdBookissa. Ne ensin
      `main`iin omana PR:nä (kuten linkkikorjaukset), sitten `main` → `dev`.
- [ ] mdBookin tiedostoihin ei kosketa `dev`:ssä: `book.toml`, `theme/`,
      `highlight/`, `mermaid/`, `start.sh`. `pages.yml` muuttuu vain `main`in
      kautta.

## Vaihe 4 — Portti

Kaikkien neljän on oltava totta ennen vaihetta 5:

- [ ] `git merge-tree --write-tree origin/main origin/dev` palauttaa 0
- [ ] CI:n mdBook-tarkistus on vihreä `dev`:llä
- [ ] `./zensical/run.sh test` menee läpi
- [ ] `ohjelmointi2.it.jyu.fi/` ja `ohjelmointi2.it.jyu.fi/dev/` toimivat

## Vaihe 5 — Vaihto ja purku

Purku kirjoittaa `src/`:n Zensicalin muotoon, jolloin mdBook lakkaa
toimimasta. Siksi vaihto tehdään ensin.

**Kohta 14 (`.html`-osoitteet):** päätetty 2026-09-11, että vanhat osoitteet
saavat mennä rikki. Zensical tekee sivuista hakemistoja
(`osa2/02-luokka-ja-olio/`), joten mdBookin `osa2/02-luokka-ja-olio.html`
antaa vaihdon jälkeen 404:n. Rikki menevät TIMin omat linkit kirjaan ja
kirjanmerkit.

**Vaihto:**

- [ ] PR `dev` → `main`
- [ ] `pages.yml`: Zensical `main`ista juureen ja `dev`:stä `/dev/`:iin
      (esikatselu). mdBook-job pois.
- [ ] Samassa PR:ssä `src/exercises/*/handout.md`:n viisi `.html`-linkkiä
      hakemistomuotoon. Aiemmin muutos rikkoisi ne mdBookissa.
- [ ] Poista mdBook: `book.toml`, `theme/`, `highlight/`, `mermaid/`,
      `start.sh`, mdBook-kohdat `.vscode/tasks.json`:sta ja
      `.vscode/launch.json`:sta sekä devcontainerin portti 36742. Päivitä
      mdBook-maininnat `README.md`:stä, `CONTRIBUTING.md`:stä ja
      `.cursorrules`:sta.
- [ ] Vaiheen 3 mdBook-säännöt raukeavat. `main` → `dev` -sääntö jää voimaan.

**Purku** (järjestys PURKUSUUNNITELMA.md:stä):

- [ ] Kohta 1: `drop_sections`, `NEST_UNDER` ja `build_nav`, jolloin `nav.yml`
      menee versionhallintaan.
- [ ] Kohta 2: yksi commit per muunnos (`fences`, `alerts`, `details`,
      `anchors`, `drop_breaks`, `divs`, `icons`, `bonus_marks`, `tabs`).
      Jokaisessa: aja muunnos `src/`:hen, poista funktio ja sen testit, aja
      `run.sh test`.
- [ ] Jos muunnoscommit konfliktoi, älä ratkaise sitä käsin. Tee commit
      uudelleen tuoreen `main`in päälle ajamalla sama muunnos.
- [ ] Vasta sitten punnitse vaihtoehto C.
