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

- [x] Mergeä `fix/rikkinaiset-linkit` → `main`. Tehty: PR #118 (`027178f`).
      Sama patch on koeputkessa (`927c27f`), joten merge ei konfliktoi.
- [x] Päätä `src/SUMMARY.md`:n Tyyliopas-rivi. Ratkesi `main`issa: rivi
      poistettiin (`45b8cf4`) ja `src/tyyliopas.md` poistettiin (`9ac482b`).
      Koeputken kopio tiedostosta on sama kuin poistettu, joten `main` → `dev`
      vain poistaa sen. Tarkistettu 2026-09-11:
      `git merge-tree --write-tree origin/main origin/spike/zensical` → 0.
- [x] `.gitignore` ja `.devcontainer/devcontainer.json` (portti 8001) ovat
      pelkkiä lisäyksiä. Vietiin `main`iin suoraan ilman PR:ää (`2c05e5a`,
      2026-09-11).

Lisäksi yksi sisältökorjaus, joka toimii myös mdBookissa:

- [x] Korjaa `src/osa1/01-hei-java.md`:n muokattava esimerkki
      (` ```java,editable `) sellaiseksi, ettei se vaadi käyttäjän syötettä.
      ACE-editori on siirretty myöhemmäksi (README, kohta 20), eikä ajonappi
      välitä ohjelmalle syötettä kummassakaan sivustossa, joten
      `IO.readln` ei saa ajossa mitään. Päätetty 2026-09-11: lohko on
      ` ```java,noplayground ` (pelkkä `editable`-määreen poisto ei riittäisi,
      koska tavallinen `java`-lohko saa ajonapin molemmissa sivustoissa) ja
      lukijaa ohjataan kokeilemaan omassa kehitysympäristössä. `main`issa
      `44f2366`. Jäljellä on yksi `editable`-lohko:
      `src/extra/luetelma-ja-hahmonsovitus.md`, joka ei lue syötettä.

Työvälinehuomio: devcontainerissa ei ole `gh`-komentoa, joten PR:t avataan
selaimessa.

## Vaihe 1 — `dev`-haara

Tehty 2026-09-11. `dev` alkaa koeputken viimeisestä commitista (`e08a991`),
`main` mergetty siihen (`a163085`, ei konflikteja), `merge-tree` → 0.
`spike/zensical` poistettu GitHubista ja paikallisesti; historia on `dev`:ssä.

```bash
git switch -c dev spike/zensical
git merge main
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

- [x] Kirjoita `.github/workflows/pages.yml` uusiksi (PR #119, 2026-09-11):
  - laukaisin: push `main`iin ja `dev`:iin
  - job `mdbook`: nykyinen kontti, `checkout` refillä `main`, `mdbook build`
    → artefakti. `dev`-pushissa ajetaan lisäksi erillinen job
    `mdbook-dev-check`, joka rakentaa `dev`:n mdBookilla pelkkänä
    tarkistuksena: se todistaa, ettei `dev` riko mdBookia. Se ei estä
    julkaisua, mutta värjää ajon punaiseksi.
  - job `zensical`: `ubuntu-latest` + `actions/setup-python`, `checkout`
    refillä `dev`, `pip install -r zensical/requirements.txt`,
    `python3 convert.py && zensical build` → artefakti
  - job `deploy`: `_site/` + `_site/dev/`, `upload-pages-artifact`,
    `deploy-pages`
- [x] Vie `pages.yml` **ensin `main`iin**, sitten `main` → `dev`. Tiedoston on
      oltava sama molemmissa: `main`-push ajaa `main`in version, ja vanha
      versio pyyhkisi `/dev/`:n. Tehty 2026-09-11: PR #119 → `main`
      (`df7a022`), sitten `main` → `dev` (`1c48281`).
- [x] Settings → Environments → `github-pages` → Deployment branches: lisää
      `dev`. Oletuksena vain oletushaara saa julkaista. Tehty 2026-09-11.
- [x] Lukitse versio `zensical/requirements.txt`:ssä: `zensical==0.0.60`.
      README kuvaa juuri 0.0.60:n käytöstä, eikä CI saa päivittää sitä
      huomaamatta. Tehty `dev`:ssä 2026-09-11.
- [x] Todennettu 2026-09-11:
  - push `dev`:iin → `/dev/` päivittyy ja juuri on yhä mdBook. Ajo
    34566904249: kaikki neljä jobia vihreitä; `/dev/osa1/04-aliohjelmat/`
    sai tyyliopas-korjauksen, juuren `04-aliohjelmat.html` vastaa 200 ja
    lataa `book.js`:n.
  - push `main`iin → molemmat säilyvät. Ajot 34566774107 (#119) ja
    34566813874 (#120) julkaisivat juuren ja `/dev/`:n.
  - `/dev/`-alipolussa: kaikki 23 css/js-tiedostoa vastaavat 200, polut ovat
    suhteellisia (`../../assets/`), kuvat ja `.cast`-tiedostot löytyvät.
    Headless-selaimella `/dev/osa1/01-hei-java/`: ajonappi tulostaa
    "Hei, maailma!", 7 asciinema-elementtiä saavat soittimen, ei
    JS-virheitä.
  - TIM:n linkki (`tim.jyu.fi/view/kurssit/tie/tiep111/koti`) vastaa 200.

Sivuvaikutus, joka löytyi `dev`:n buildista: `main` poisti `src/tyyliopas.md`:n
mutta `src/osa1/04-aliohjelmat.md` linkitti siihen kahdesti. Korjattu PR:llä
#120 `main`iin (linkit pois, teksti jää) ja mergetty `dev`:iin.

CI ei tarvitse `svgbob_cli`:tä eikä PlantUML-palvelinta, koska `cache/svgbob/`
ja `assets/plantuml/` ovat versionhallinnassa. Uusi tai muutettu kaavio: aja
`python3 convert.py` paikallisesti ja committoi molemmat hakemistot. Muuten
bob-kaavio jää CI:ssä koodilohkoksi.

## Vaihe 3 — `dev` pysyy mergettävänä

Voimassa 2026-09-11 alkaen vaihtoon asti. Nämä eivät ole kertaluontoisia
tehtäviä vaan sääntöjä; ruksi tarkoittaa "noudatetaan".

- [ ] `main` → `dev` vähintään viikoittain ja aina ennen isompaa työtä. Ei
      rebasea, koska `dev` on julkaistu ja jaettu.
- [ ] Zensicalin työ pysyy `zensical/`-hakemistossa.
- [ ] `src/`:hen vain muutoksia, jotka toimivat myös mdBookissa. Ne ensin
      `main`iin omana PR:nä (kuten linkkikorjaukset), sitten `main` → `dev`.
- [ ] mdBookin tiedostoihin ei kosketa `dev`:ssä: `book.toml`, `theme/`,
      `highlight/`, `mermaid/`, `start.sh`. `pages.yml` muuttuu vain `main`in
      kautta.

## Vaihe 4 — Portti

Kaikkien neljän on oltava totta ennen vaihetta 5. Tarkistetaan uudestaan
juuri ennen vaihtoa; alla tilanne 2026-09-11 (`dev` = `1c48281`):

- [x] `git merge-tree --write-tree origin/main origin/dev` palauttaa 0
- [x] CI:n mdBook-tarkistus on vihreä `dev`:llä (`mdbook-dev-check`, ajo
      34566904249)
- [x] `./zensical/run.sh test` menee läpi (198 passed)
- [x] `ohjelmointi2.it.jyu.fi/` ja `ohjelmointi2.it.jyu.fi/dev/` toimivat

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
