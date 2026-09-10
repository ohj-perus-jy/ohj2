# Zensical-koeputki

Kokeilu siitä, voisiko Ohj2-materiaalin siirtää mdBookista **Zensicaliin**
(Material for MkDocsin tekijöiden uusi generaattori). Ei koske `../src`:ään
eikä `../book.toml`:iin — `bash ../start.sh` toimii koko ajan entiseen tapaan.

**Tila: tarkistuslistan 25 kohdasta 18 on tehty**, kaksi ei tarvita ja viisi on
auki. Jokaisen ratkaisun perustelut, vaihtoehdot ja todennus ovat omassa
tiedostossaan: [PERUSTELUT.md](PERUSTELUT.md). Mitä `convert.py`:stä poistuu,
jos koeputki voittaa ja mdBook puretaan:
[PURKUSUUNNITELMA.md](PURKUSUUNNITELMA.md).

## Käynnistys

```bash
./zensical/run.sh
```

Ensimmäisellä kerralla se asentaa itse tarvitsemansa (`python3-venv`, `pip`,
`zensical`) ja kysyy sudo-salasanaa apt:ta varten. Sen jälkeen sivusto on
osoitteessa <http://localhost:8001>. Portti 8001 on välitetty
devcontainerista; jos se ei aukea, avaa VS Coden **PORTS**-välilehti.

```bash
./zensical/run.sh 8003     # eri portti
./zensical/run.sh build    # pelkkä rakennus site/-hakemistoon
```

**Muokattava puu on `../src`, ei `docs/`.** `docs/` on kertakäyttöinen kopio,
jonka `convert.py` kirjoittaa yli; sinne tehty muutos katoaa seuraavassa
ajossa.

`run.sh` käynnistää palvelimen rinnalle vahdin (`convert.py --watch`), joka
ajaa muunnoksen aina kun `../src` tai `assets/` muuttuu. Tallennus siis
riittää, eikä palvelinta tarvitse käynnistää uudelleen. Mitattuna selaimessa
oikealla sivulla: **1,1-1,4 s** tallennuksesta, viisi tallennusta peräkkäin.

| Vaihe                                            | Aika  |
| ------------------------------------------------ | ----- |
| vahti huomaa tallennuksen ja odottaa sen loppuun  | 0,6 s |
| `convert.py`                                      | 0,3 s |
| palvelimen käännös ja selaimen uudelleenlataus    | 0,4 s |

Vahti loppuu palvelimen mukana. Kertamuunnoksen voi yhä ajaa itse:
`python3 convert.py`.

`convert.py` kirjoittaa vain sen, mikä oikeasti muuttui: yhden sivun muutos on
yksi kirjoitus `docs/`:iin, ja muuttumaton ajo ei kirjoita mitään. Se ei ole
nopeusoptimointi vaan ehto sille, että muutos näkyy selaimessa lainkaan —
`zensical serve` ilmoittaa jokaisesta muuttuneesta tiedostosta selaimelle
erikseen, ja koko puun uudelleenkirjoitus hukutti oikean ilmoituksen satojen
turhien sekaan.

Muunnoksia ajetaan yksi kerrallaan (tiedostolukko `.convert.lock`). Kaksi
yhtä aikaa ajavaa muunnosta — esimerkiksi kaksi auki olevaa `run.sh`:ta —
sekoittaisi `docs/`:n keskenään; mitattuna se poisti kymmenen
versionhallinnassa ollutta `cache/svgbob/`-tiedostoa.

Vahti kysyy tiedostojen muokkausajat 0,3 s välein (600 tiedostoa, 6 ms) eikä
käytä inotifyä. Syy on ympäristössä: inotify ei saa tapahtumia lainkaan, jos
repo on Windowsin levyllä 9p-liitoksen takana, ja siellä vahti olisi hiljaa
rikki. Devcontainerin volume on ext4, joten kumpikin tapa toimisi täällä.

`convert.py` ei tyhjennä `docs/`:ia, koska `zensical serve` (0.0.60) kaatuu tai
unohtaa `docs/assets/`:n staattiset tiedostot, jos sen seuraama hakemisto
katoaa kesken rakennuksen; perustelu on `convert.py`:n `sync_docs`-funktiossa.
Jos tyylit silti katoavat — sivu näyttää paljaalta oletusteemalta ilman
virheilmoitusta — syy näkyy näin:

```bash
curl -s localhost:8001/assets/css/layout.css | head -1
```

Palvelin vastaa puuttuvaan tiedostoon etusivun HTML:llä (`<!doctype html>`,
tilakoodi 200), ei 404:llä. Silloin käynnistä palvelin uudelleen.

## Testit

```bash
./zensical/run.sh test                        # kaikki, 183 testiä
./zensical/run.sh test tests/test_convert.py  # pelkät muunnokset, 0,2 s
./zensical/run.sh test --nobuild              # käytä olemassa olevaa site/:ä
```

Ensimmäisellä kerralla asentuvat `pytest`, `playwright`, sen chromium ja
selaimen systeemikirjastot (`playwright install-deps`, vaatii sudon); sivuston
rakentamiseen riittää yhä pelkkä `zensical`.

Mitään ei jäljitellä: testit ajavat `convert.py`:n ja `zensical build`in
oikeasti ja avaavat sivun oikeassa selaimessa. Kerroksia on kolme, koska
rikkoutumisia on kolmea lajia:

| Tiedosto                | Mitä                                                          | Kesto      |
| ----------------------- | ------------------------------------------------------------- | ---------- |
| `tests/test_convert.py` | `convert.py`:n muunnokset yksin: ei käännöstä eikä selainta   | 0,2 s      |
| `tests/test_print.py`   | tulostussivun kokoaminen selaimessa, koekirjalla              | 6 s        |
| `tests/test_playground.py` | ajonapit koekirjalla, suorituspalvelin korvattuna          | 16 s       |
| `tests/test_hidelines.py` | piilorivit ja silmänappi koekirjalla                       | 2 s        |
| `tests/test_highlights.py` | korostetut rivit koekirjalla                              | 2 s        |
| `tests/test_change.py`  | koekirjan materiaalia muutetaan: näkyykö muutos tulosteessa   | 25 s       |
| `tests/test_book.py`    | sama oikealla materiaalilla, 72 lukua                          | 10 s       |

Koekirja (`tests/book/src`), testeihin kirjatut tunnetut poikkeukset ja
selaimen systeemikirjastot: [PERUSTELUT.md](PERUSTELUT.md).

## Tarkistuslista

| #  | mdBookin ominaisuus                          | Esiintymiä                | Tila nyt                                                                                                           |
| -- | -------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1  | `{{#include tiedosto}}`                      | 194                       | **tehty** — `convert_includes`; 4 makroa jää näkyviin, kohde puuttuu aineistosta                                   |
| 2  | `//-` piilorivit                             | 1103                      | **tehty** — `hide_lines` + `assets/js/hidelines.js`; rivit piiloon ja silmänappi, ajoon ne menevät yhä               |
| 3  | ` ```java ` ajonappi (playground)            | 231                       | **tehty** — `assets/js/playground.js`; sama palvelin ja sama pyyntö kuin mdBookissa, monitiedostolohkot mukaan lukien |
| 4  | ` ```java,ignore` / `,noplayground`          | 289                       | **tehty** — attribuutit luokiksi (`{ .java .ignore }`), korostus palasi                                            |
| 5  | `// FILE:` monitiedostolohkot                | 73 lohkoa / 194 tiedostoa | **tehty** — `pymdownx.tabbed`, tiedosto per välilehti                                                              |
| 6  | `<task>` / `<points>` / `<handout>`          | 507                       | **tehty** — `convert_tasks` + `assets/css/tasks.css`; riippuva numerointi laatikon sijaan                          |
| 7  | `> [!VINKKI]`-tyyliset alertit               | 75                        | **tehty** — `convert_alerts`; `admonition` on jo Zensicalin oletuslistalla, `mkdocs.yml` ennallaan                 |
| 8  | `<details>`-lohkot                           | 88 + 6 `<summary>`        | **tehty** — `convert_details`; `markdown="1"` avaustagiin ja `markdown="block"` monirivisiin yhteenvetoihin       |
| 9  | `HIGHLIGHT_*_BEGIN/END`                      | 120                       | **tehty** — `mark_highlights` + `assets/js/highlights.js`; värit kirkkautta muuttamatta, ks. kohta 9              |
| 10 | Lukujen numerointi navigaatiossa             | koko nav                  | **tehty** — `convert.py`, 12 riviä                                                                                 |
| 11 | Osan etusivu = osan oma linkki navissa       | 13 osaa                   | **tehty** — `navigation.indexes`                                                                                   |
| 12 | Otsikoiden numerointi sivun sisällä          | —                         | ei ollut mdBookissakaan                                                                                            |
| 13 | Ääkköset ankkureissa (`#käyttö`)             | —                         | riisutaan (`#kaytto`)                                                                                              |
| 14 | `.html`-päätteiset osoitteet (TIM)           | —                         | puuttuu — nyt hakemistopolut                                                                                       |
| 15 | plantuml / bob / mermaid                     | 17 / 11 / 2               | **tehty** — `convert_plantuml` (kuviksi), `convert_svgbob` (upotetuksi SVG:ksi); mermaid toimi jo itsestään        |
| 16 | `<asciinema>`-upotukset                      | 13                        | rikki                                                                                                              |
| 17 | Ikonit `<i class="bi ...">` ja `<i class="fa ...">` | 150                | **tehty** — 66 bonusmerkkiä `convert_bonus_marks`, 58 valikkopolun nuolta merkkinä ja 22 kuvaketta teeman glyfeinä `convert_icons`; 4 poistui navigointiosion mukana |
| 18 | JYU-paletti, kultainen korostus              | 30                        | puuttuu                                                                                                            |
| 19 | Lisenssi + "Ehdota muutosta" alatunnisteessa | —                         | **tehty** — tekijät, lisenssi ja muokkauslinkki; "Ilmoita ongelmasta" puuttuu                                      |
| 20 | ACE-editori (`editable`-lohkot)              | 2                         | puuttuu — `.editable` säilyy nyt luokkana; ajonappi ajaa lohkon sellaisenaan, ks. kohdat 3 ja 4                     |
| 21 | KaTeX                                        | 0                         | voi jättää pois                                                                                                    |
| 22 | Edellinen/seuraava sivun alareunassa         | joka sivu                 | **tehty** — `navigation.footer`                                                                                    |
| 23 | `### [Windows](#tab/win)`-välilehdet         | 33 lohkoa / 9 joukkoa     | **tehty** — `pymdownx.tabbed` + `content.tabs.link`                                                                |
| 24 | Tulostuspainike: koko kirja yhdeksi PDF:ksi  | joka sivu                 | **tehty** — `assets/js/print.js`, `print.css`, runko `convert.py`:stä, yläpalkin malli                             |
| 25 | `<div class="ht-reqs">` vaatimuslohkot       | 9                         | **tehty** — `convert_divs` + `assets/css/requirements.css`; numerointi 1.1, 1.2, ... CSS-laskurista               |

Zensical antaa itse ilman mitään lisäystä: oikean reunan sisällysluettelon,
haun ja responsiivisen navigaation.

## Mitä puuttuu

Tarkistuslistalta viisi kohtaa:

- **16 `<asciinema>`-upotukset** (13 kpl) — rikki, tagi jää sivulle näkyviin.
- **18 JYU-paletti, kultainen korostus** (30 kohtaa) — puuttuu kokonaan.
  Tehtäväkorttien bonusliuska käyttää toistaiseksi omaa tummennettua sävyään,
  koska kirjan `#C29A5B` on valkoista vasten vain 2,4:1.
- **20 ACE-editori** (2 `editable`-lohkoa) — lohko näkyy tavallisena koodina.
  Sen mukana `fa-history`-kuvake osoittaa "Peruuta muutokset" -nappiin, jota
  sivustolla ei ole.
- **14 `.html`-päätteiset osoitteet** — TIM:n linkit osoittavat mdBookin
  muotoon, Zensicalissa sivut ovat hakemistopolkuja.
- **13 ääkköset ankkureissa** — Zensical riisuu ne (`#käyttö` -> `#kaytto`).
  Tästä jää yksi kuollut linkki tulostussivulle; se on kirjattu testiin.

Pienempiä:

- Alatunnisteen "Ilmoita ongelmasta" -linkki (kohta 19).
- Kopioi koodi -nappi: teemalla on siihen valmis `content.code.copy`, se on
  vain ottamatta käyttöön (1 rivi `mkdocs.yml`:ään).
- Neljä `{{#include}}`-makroa jää sivuille näkyviin: kohde puuttuu
  aineistosta.
- Etusivun ja osan 1 ohjeteksteissä on kaksi mdBook-aikaista väitettä:
  teemanapin "vaalea, tumma, automaattinen" (Zensicalissa nappi on
  kaksiasentoinen) ja se, kumpi glyfi napissa milloinkin on. Kuvakkeet on
  korjattu, virkkeet eivät.

## Avoimet kysymykset

- **Sivuston hakemistorakenne.** `docs_dir: src` säilyttäisi sivujen sisäiset
  linkit, kuvapolut, `edit_uri`:n ja Gitin historian koskemattomina. Se on nyt
  ainoa jäljellä oleva syy siirtää sivukohtaiset muunnokset renderöintiin
  (PERUSTELUT.md: vaihtoehto C), koska nopeussyy raukesi mittauksissa.
  Mitä siirrettävää jää jäljelle mdBookin poistuttua, ks.
  [PURKUSUUNNITELMA.md](PURKUSUUNNITELMA.md).

## Ratkaistut kysymykset

- **Jääkö `convert.py` pysyväksi osaksi työnkulkua?** Jää, ja sen ympärille
  tehtiin vahti (`--watch`). Ratkaiseva luku oli, kauanko tallennuksesta kuluu
  selaimen päivittymiseen: mitattuna `zensical serve` kääntää vain muuttuneen
  sivun ja tarjoilee sen **0,2–0,6 s** kuluttua, ja koko kierros `../src`:stä
  selaimeen on **2,3 s**. Vaihtoehto oli perusteltu vain, jos luku olisi ollut
  kymmeniä sekunteja. Perustelut ja hylätyt vaihtoehdot: PERUSTELUT.md.

## Periaate

Lähtötilanne on Zensicalin oletusteema sellaisenaan: jokainen lisätty rivi
pitää pystyä perustelemaan jollakin mdBookin ominaisuudella, jota oikeasti
tarvitaan. Perustelut ovat [PERUSTELUT.md](PERUSTELUT.md):ssä ja tiedostojen
omissa alkukommenteissa. Aiempi, täysin viritetty versio on tallessa branchissa
`spike/mkdocs`.
