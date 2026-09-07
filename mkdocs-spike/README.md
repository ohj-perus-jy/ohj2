# Zensical-koeputki

Kokeilu siitä, voisiko Ohj2-materiaalin siirtää mdBookista **Zensicaliin**
(Material for MkDocsin tekijöiden uusi generaattori). Ei koske `../src`:ään
eikä `../book.toml`:iin — `bash ../start.sh` toimii koko ajan entiseen tapaan.

## Käynnistys

```bash
./mkdocs-spike/run.sh
```

Ensimmäisellä kerralla se asentaa itse tarvitsemansa (`python3-venv`, `pip`,
`zensical`) ja kysyy sudo-salasanaa apt:ta varten. Sen jälkeen sivusto on
osoitteessa <http://localhost:8001>. Portti 8001 on välitetty
devcontainerista; jos se ei aukea, avaa VS Coden **PORTS**-välilehti.

```bash
./mkdocs-spike/run.sh 8003     # eri portti
./mkdocs-spike/run.sh build    # pelkkä rakennus site/-hakemistoon
```

`zensical serve` seuraa muutoksia `docs/`:ssä. Kun muokkaat `../src`:ää,
aja `python3 convert.py` uudelleen.

## Periaate

Lähtötilanne on **Zensicalin oletusteema sellaisenaan**. Ei omaa CSS:ää, ei
omaa JavaScriptiä, ei template-ylikirjoituksia, ei Markdown-laajennuksia,
ei sisältömuunnoksia.

`convert.py` tekee tasan kaksi asiaa: kopioi `../src` → `docs/` ja kääntää
`SUMMARY.md`:n navigaatioksi. Kaikki mdBookin oma syntaksi jää siis sivuille
raakana näkyviin — se on tarkoitus. Näin listasta ei tule arvauksia vaan
havaintoja.

Aiempi, täysin viritetty versio on tallessa branchissa `spike/mkdocs`:
sieltä saa jokaisen palasen takaisin, kun se on ensin todettu tarpeelliseksi.

## Tarkistuslista

Käydään läpi yksi kerrallaan. Jokaiselle kolme kysymystä: mitä mdBook teki,
näyttääkö Zensical sen jo itse, ja tarvitaanko sitä oikeasti.

| # | mdBookin ominaisuus | Esiintymiä | Tila nyt |
|---|---|---|---|
| 1 | `{{#include tiedosto}}` | 194 | rikki — teksti näkyy raakana |
| 2 | `//-` piilorivit | 1094 | rikki — rivit näkyvät |
| 3 | ` ```java ` ajonappi (playground) | 231 | puuttuu |
| 4 | ` ```java,ignore` / `,noplayground` | 285 | puolittain — 253 lohkoa jää `language-text`iksi, ei Java-korostusta |
| 5 | `// FILE:` monitiedostolohkot | 192 | rikki — merkinnät näkyvät |
| 6 | `<task>` / `<points>` / `<handout>` | 507 | rikki — 501 tagia menee HTML:ään tyylittöminä |
| 7 | `> [!VINKKI]`-tyyliset alertit | 75 | rikki — näkyy lainauksena |
| 8 | `<details>`-lohkot | 88 | toimii (78 kpl HTML:ssä), mutta ilman animaatiota |
| 9 | `HIGHLIGHT_*_BEGIN/END` | 120 | rikki — merkinnät näkyvät |
| 10 | Lukujen numerointi navigaatiossa | koko nav | puuttuu |
| 11 | Osan etusivu = osan oma linkki navissa | 10 osaa | rikki — sivu toistuu ensimmäisenä lapsena |
| 12 | Otsikoiden numerointi sivun sisällä | — | ei ollut mdBookissakaan |
| 13 | Ääkköset ankkureissa (`#käyttö`) | — | riisutaan (`#kaytto`) |
| 14 | `.html`-päätteiset osoitteet (TIM) | — | puuttuu — nyt hakemistopolut |
| 15 | plantuml / bob / mermaid | 17 / 8 / 2 | rikki / rikki / puuttuu |
| 16 | `<asciinema>`-upotukset | 13 | rikki |
| 17 | Bootstrap-ikonit `<i class="bi ...">` | 136 | puuttuu — ei fonttia |
| 18 | JYU-paletti, kultainen korostus | 30 | puuttuu |
| 19 | Lisenssi + "Ehdota muutosta" alatunnisteessa | — | puuttuu |
| 20 | ACE-editori (`editable`-lohkot) | 2 | puuttuu |
| 21 | KaTeX | 0 | voi jättää pois |

Zensical antaa itse ilman mitään lisäystä: oikean reunan sisällysluettelon,
haun, edellinen/seuraava-linkit, kopioi koodi -napin ja responsiivisen
navigaation.

## Tehdyt kohdat

### Teemanvaihto (14 riviä `mkdocs.yml`:ään)

`book.toml`:ssa on `default-theme = "jyu-light"` ja
`preferred-dark-theme = "jyu-dark"` — kaksi teemaa, ei viittä. Sama tehdään
Materialin `palette`-lohkolla `media`-ehdolla, jolloin teema seuraa
käyttöjärjestelmää ja vaihdin ohittaa sen. Todennettu selaimella: kun
järjestelmä on vaalea, sivu avautuu `default`-teemalla ja vaihdin vie
`slate`en; kun järjestelmä on tumma, päinvastoin.

Havainto samalla: Materialin oletusväreillä koodilohkon ja sivun taustan
kontrasti on **1,09:1 molemmissa teemoissa** (vaalea 255,255,255 vs
245,245,245; tumma 11,12,15 vs 20,23,31). Sama ongelma josta aiemmin
huomautit — se on siis Materialin oletus, ei koeputken tekemä. Kuuluu
kohtaan 18.

## Mitattu ensimmäisestä ajosta

Rakennus kestää **16 s** (MkDocs + Material samasta sisällöstä: 31 s) ja
tuottaa **53 varoitusta**: 49 × "anchor does not exist", 4 × "page does not
exist". Kertyminen: `tyokalut.md` 20, `osa8/06-versionhallinnan-etakaytto.md`
9, `osa1/01-hei-java.md` 7. Suurin osa on mdBookin `#tab/...`-ankkureita ja
ääkkösellisiä ankkureita — nämä liittyvät listan kohtiin 13 ja 14.

Ilman mitään konfiguraatiota toimivat jo: Pygments-syntaksiväritys
(`language-java highlight`), oikean reunan sisällysluettelo, haku suomeksi,
kokoontaittuva navigaatio ja edellinen/seuraava-linkit.
