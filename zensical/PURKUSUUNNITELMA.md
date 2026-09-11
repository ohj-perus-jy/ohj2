# Purkusuunnitelma: mitä `convert.py`:stä jää, kun mdBook poistuu

Tämä tiedosto olettaa, että koeputki voittaa: `../src` siirtyy Zensicalin
lähdepuuksi ja mdBook (`../book.toml`, `../theme/`, `../start.sh`) poistetaan.
Se vastaa yhteen kysymykseen — mitkä `convert.py`:n vaiheista lakkaavat silloin
olemasta, mitkä vasta lähdettä muokkaamalla ja mitkä eivät koskaan.

Tila ja käyttöohjeet ovat [README.md](README.md):ssä, tehtyjen ratkaisujen
perustelut [PERUSTELUT.md](PERUSTELUT.md):ssä. Vaihenumerot viittaavat
`convert.py`:n alkukommenttiin, kohtanumerot README.md:n tarkistuslistaan.
Esiintymäluvut ovat `python3 convert.py`:n raportista (10.9.2026).

**Tämä on päättelyä nykyisestä koodista, ei mitattua eikä kokeiltua.**
Toisin kuin PERUSTELUT.md, jossa jokaisen kohdan takana on todennus, tässä ei
ole vielä ajettu mitään. Luvut ovat mitattuja, päätelmät eivät.

## Lähtökohta: mdBookin poistuminen ei vie syntaksia mukanaan

Ensimmäinen houkutus on ajatella, että kun mdBook poistuu, mdBookin syntaksin
kääntäminen poistuu sen mukana. Näin ei ole. Syntaksi on `../src`:ssä ja jää
sinne, kunnes joku kirjoittaa sen uusiksi. Sivulla lukee `> [!VINKKI]`
riippumatta siitä, onko `book.toml` olemassa.

mdBookin poistuminen vie mukanaan vain **rajoitteen**: koeputken sääntö "ei
koske `../src`:ään" on olemassa siksi, että `bash ../start.sh` pitää toimia
koko ajan. Kun sitä vaatimusta ei ole, lähdettä saa muokata — mutta se on
tehtävä erikseen, eikä joka kohdassa kannata.

Siksi vaiheet jakautuvat kolmeen.

## Taustaksi: vaihtoehdot A, B ja C

Alla viitataan kahdesti PERUSTELUT.md:n vaihtoehtoihin. Tässä ne lyhyesti,
jotta sitä lukua ei tarvitse etsiä.

Ratkaistava ongelma oli tämä: `zensical serve` seuraa `docs/`-hakemistoa,
jonka `convert.py` kirjoittaa — ei lähdepuuta `../src`. Kesken kirjoittamista
tehty muutos ei siis näy selaimessa ennen kuin muunnos on ajettu uudelleen.
Kolme tapaa päästä siitä eroon:

**A. Lähde pysyy mdBookin syntaksina, `convert.py` jää ja sen ympärille
tehdään vahti.** Käännösaskel on olemassa muttei näy käsityönä: `run.sh`
käynnistää `convert.py --watch`:n palvelimen rinnalle, ja tallennus riittää.
**Tämä on nykytila.** Ratkaiseva mittaus oli, että koko kierros tallennuksesta
selaimen päivittymiseen on 2,3 s — vaihtoehdot olisivat olleet perusteltuja
vain, jos luku olisi ollut kymmeniä sekunteja.

**B. Käännetään kerran ja `docs/` committoidaan uudeksi lähdepuuksi.**
Muunnoksia ei silloin ole lainkaan. Hylättiin, koska hinta on kohtuuton juuri
niissä kohdissa, jotka koeputkessa on tehty: kirjoittaisit käsin
`` ```{ .java data-hidden="1 3" data-hl-green="2" } `` ja laskisit rivinumerot
itse — ja numeroisit ne uudelleen joka kerta kun lisäät rivin lohkon alkuun.
Merkintä `// HIGHLIGHT_GREEN_BEGIN` on olemassa juuri siksi, ettei numeroita
tarvitse kirjoittaa.

**C. Sivukohtaiset muunnokset siirretään Python-Markdown-laajennukseksi.**
Merkinnät käännettäisiin silloin sivua renderöitäessä eikä ennalta: ei
erillistä komentoa, ei `docs/`-kopiota, ja `serve` seuraisi suoraan lähdettä.
Kirjoittaja kirjoittaa edelleen `// HIGHLIGHT_GREEN_BEGIN`, ja rivinumerot
lasketaan joka renderöinnillä uudelleen — eli C säilyttää sen, minkä B menettää.

### Miten C tehtäisiin

Tie on tarkistettu Zensicalin koodista. **Yleistä plugin-rajapintaa ei ole:**
`config.py` tuntee vain kovakoodatun listan MkDocs-liitännäisiä, eikä MkDocsin
`hooks:`-avainta tueta lainkaan. Mutta `markdown_extensions` menee sellaisenaan
Python-Markdownille (`zensical/markdown/render.py`), joten oma laajennus
latautuu nimellä:

```yaml
markdown_extensions:
  - ohj2.highlights
```

Laajennuksen on oltava `.venv`:stä importattavissa. Muunnokset olisivat
esikäsittelijöitä (`Preprocessor`), koska ne katsovat raakoja rivejä ennen
jäsennystä — samaa työtä kuin `mark_highlights` ja `hide_lines` tekevät nyt.

C:tä ei ole tehty, koska nopeussyy raukesi mittauksissa. Ainoa jäljellä oleva
syy on `docs_dir: src`, joka säilyttäisi sivujen sisäiset linkit, kuvapolut,
`edit_uri`:n ja Gitin historian koskemattomina. Se on myös se, mihin alla oleva
luku *Seuraus* päätyy: mdBookin poistuttua C on paljon halvempi kuin nyt.

## 1. Poistuu heti, pelkästään mdBookin lähdöstä

Nämä eivät ole syntaksin kääntämistä vaan kiertoteitä sen ympäri, ettei
lähdettä saa koskea tai ettei mdBook osaa jotain.

**`drop_sections`** (vaihe 2, kohta 1) — 1 osio. Etusivun "Navigointi tässä
materiaalissa" kuvaa mdBookin käyttöliittymää. Poista osio `src/index.md`:stä,
niin muunnos, `DROP_SECTIONS`, `HEADING_RE` ja niiden testit menevät mukana.

**`NEST_UNDER`** — 2 sivua. mdBookin `SUMMARY.md` ei salli etulinkkien
sisäkkäisyyttä, Zensical sallii. Siirrä `tenttiohjeet.md` `tentti/`-hakemistoon
lähteessä, ja mukana lähtevät `nest_moves`, `sync_docs`:n siirtologiikka **ja**
`build_extra`:n koko `edit_source`-polkukartta — jälkimmäinen on olemassa vain
siksi, että siirretyn sivun muokkauslinkki löytäisi takaisin.

**`build_nav`** — koko navigaatio. `SUMMARY.md`:tä ei enää ole, joten
`nav.yml` kirjoitetaan käsin ja otetaan versionhallintaan.

Yksi asia ei poistu tämän mukana: **lukujen numerointi** (kohta 10). Numerot
eivät ole lähteessä, vaan mdBook laskee ne sijainnista, ja Materialissa ei ole
vastinetta. Joko numerot kirjoitetaan `nav.yml`:n otsikoihin käsin ja
ylläpidetään käsin, tai `nav.yml` pysyy numeroimattomana järjestyslistana ja
12 riviä koodia laskee ne. Tämä on ainoa kohta, jossa käsin kirjoitettu
navigaatio on aidosti huonompi kuin generoitu.

## 2. Poistuu kertaluontoisella lähteen uudelleenkirjoituksella

Nämä yhdeksän ovat puhdasta syntaksin kääntämistä: yhdestä merkinnästä
toiseen, ilman että mitään lasketaan. Ne voi ajaa lähteeseen kerran ja
committoida — se on **vaihtoehto B** rajattuna vain niihin
kohtiin, joissa se ei maksa mitään.

| Kohta | Muunnos               | Esiintymiä              | Lähteeseen kirjoitettaisiin           |
| ----- | --------------------- | ----------------------- | ------------------------------------- |
| 4     | `convert_fences`      | 392 aitaa               | `{ .java .ignore }`                   |
| 7     | `convert_alerts`      | 75 lohkoa               | `!!! tip "Vinkki"`                    |
| 8     | `convert_details`     | 143 tagia + 6 summarya  | `<details markdown="1">`              |
| 13    | `convert_anchors`     | 6 linkkiä + 1 otsikko   | `#kaytto` ja `## Otsikko {#tunnus}`   |
| —     | `drop_breaks`         | 10 riviä                | ei mitään, rivit vain pois            |
| 25    | `convert_divs`        | 9 tagia                 | `<div class="ht-reqs" markdown="1">`  |
| 17    | `convert_icons`       | 58 nuolta, 22 kuvaketta | `›` ja `:material-menu:`              |
| 17    | `convert_bonus_marks` | 30 merkkiä              | ks. alla                              |
| 23    | `convert_tabs`        | 9 joukkoa               | `=== "Windows"`                       |

Kolme tarkennusta:

**`convert_fences` ei poistu kokonaan, vaan halkeaa.** Attribuuttien
kääntäminen (`java,ignore` → `{ .java .ignore }`) on kertatyötä, mutta saman
funktion sisällä laskettavat piilorivit (142 lohkoa, `hide_lines`) ja
korostukset (79 lohkoa, `mark_highlights`) eivät ole — ne kuuluvat kohtaan 3.

**`convert_anchors` halkeaa kahtia: toinen puoli käy lähteeseen heti, toinen
vasta vaihdon jälkeen.**

Välilyönnin lisääminen otsikon tunnuksen eteen (1 otsikko) käy `../src`:ään
milloin tahansa: mdBook hyväksyy molemmat muodot. Mitattu sen omasta
käännöksestä — `osa4/01-rajapinta.md`:n välilyönnitön `{#alykoti-saadettava}`
antaa `id="alykoti-saadettava"` aivan kuten `tyokalut.md`:n välilyönnillinen
`{#jdk}` antaa `id="jdk"`.

Ääkkösten riisuminen (6 linkkiä) **ei** käy ennen vaihtoa. Riisuttua ankkuria
ei voi kirjoittaa lähteeseen, koska mdBook säilyttää ääkköset otsikon tunnuksessa
(`book/osa7/01-javafx-perusteet.html`: `id="ensimmäinen-javafx-sovellus"`):
`#ensimmainen-javafx-sovellus` osoittaisi siellä tyhjään. Ainoa muoto, jonka
molemmat generaattorit ymmärtävät samalla tavalla, on **otsikon oma
ascii-tunnus** — kuuden linkin lisäksi neljä kohdeotsikkoa saisi `{#tunnus}`:n:

| Kohdeotsikko                                                                       | Otsikon tunnukseksi                       |
| ----------------------------------------------------------------------------------- | ----------------------------------------- |
| `osa1/01-hei-java.md:73` "Opas: Java-ohjelmien kääntäminen ja ajaminen"              | `{#opas-kaantaminen-ja-ajaminen}`         |
| `osa4/02-vertailurajapinta.md:1` "Comparable-rajapinta ja luonnollinen järjestys"    | `{#comparable-ja-luonnollinen-jarjestys}` |
| `osa7/01-javafx-perusteet.md` "Ensimmäinen JavaFX-sovellus"                          | `{#ensimmainen-javafx-sovellus}`          |
| `osa7/01-javafx-perusteet.md` "JavaFX-sovelluksen käynnistys ja ydinluokat"          | `{#javafx-kaynnistys-ja-ydinluokat}`      |

Tunnus muuttaa mdBookin nykyisiä osoitteita: ulkopuolinen linkki vanhaan
ääkköselliseen ankkuriin (TIM, kirjanmerkit) lakkaa toimimasta. Kohdan 14
päätöksen (11.9.2026, [KAYTTOONOTTO.md](KAYTTOONOTTO.md)) jälkeen se ei ole
enää erillinen hinta, koska vanhat osoitteet menevät vaihdossa rikki joka
tapauksessa. `.html`-polku antaa 404:n, eikä ankkurikaan osuisi, vaikka sivu
löytyisi: Zensical riisuu ääkköset otsikon tunnuksesta
(`site/osa7/01-javafx-perusteet/index.html`:
`id="ensimmainen-javafx-sovellus"`). Tunnus vain aikaistaisi rikkoutumisen.

Tunnuksia ei myöskään tarvita. KAYTTOONOTTO.md:n järjestyksessä purku
tehdään vaihdon jälkeen, kun mdBookia ei enää ole. Silloin `convert_anchors`
ajetaan lähteeseen kuten muutkin muunnokset: kuusi linkkiä riisuttuun muotoon
ja yksi välilyönti, ja Zensical tuottaa vastaavat tunnukset itse. Ankkurit
ovat silloin samat kuin nykyisessä `docs/`:ssä, joka kääntyy varoituksetta.
Yllä oleva versio (kuusi linkkiä ja neljä tunnusta) on tarpeen vain, jos
ankkurit korjataan `main`issa ennen vaihtoa, eikä siihen ole syytä:
`convert_anchors` puretaan joka tapauksessa vasta vaihdon jälkeen.

**Ikonilyhenne toimii ilman konfiguraatiota.** Zensicalin emoji-indeksi
(`zensical/extensions/emoji.py`, `_load_twemoji_index`) indeksoi jokaisen SVG:n
teeman `templates/.icons/`-hakemistosta nimellä `:material-menu:`, eli
`ICON_MAP`:n arvot ovat suoraan kirjoitettavissa lähteeseen ja koko `icons/`-
hakemisto sekä sitä vahtiva testi jäävät pois. Bonusmerkki on poikkeus: se ei
ole teeman ikoni vaan oma polku, joten se vaatii joko inline-SVG:n lähteeseen
tai `custom_icons`-hakemiston ja `attr_list`-luokan kullan säilyttämiseksi.

## 3. Jää, vaikka mdBookia ei olisi koskaan ollutkaan

### Merkinnät, joissa lähteen syntaksi on parempi kuin kohde

Näissä uudelleenkirjoitus olisi tappio, koska merkintä on olemassa juuri siksi,
ettei kirjoittajan tarvitse laskea:

- **`hide_lines` (142 lohkoa) ja `mark_highlights` (79 lohkoa)** — muuten
  kirjoittaisit `data-hidden="1 3"` käsin ja numeroisit rivit uudelleen joka
  kerta kun lisäät rivin lohkon alkuun. Tämä on se argumentti, jolla
  vaihtoehto B kokonaisuudessaan hylättiin.
- **`convert_files`** — 73 lohkoa, 194 tiedostoa. `// FILE:` on yksi rivi;
  välilehtijoukko on kehys jokaisen tiedoston ympärillä.
- **`convert_tasks`** — 169 korttia. Sama asia isommassa mittakaavassa.
- **`convert_includes`** — 190 makroa. Ainoa neljästä, jolle on valmis
  vastine: `pymdownx.snippets` (`--8<--`) ei ole Zensicalin oletuslistalla,
  mutta `markdown_extensions` menee sellaisenaan Python-Markdownille. Tämä
  kannattaa tarkistaa erikseen — rivivalinnat (`take_lines`) on katettava.

### Kirjan tason työ, jota Zensical ei tee

- **`build_print_page`** (kohta 24) — tulostussivua ei ole olemassa ilman
  tätä, eikä MkDocsin tulostusliitännäisiä voi ottaa avuksi.
- **`convert_plantuml` (21 kaaviota), `convert_svgbob` (12) ja
  `prune_diagrams`** — piirtäminen ei ole teeman ominaisuus.
- **Vaihe 3 (assetit)** niin kauan kuin ne ovat `docs_dir`:n ulkopuolella.

## Seuraus: vaihtoehto C:n hinta romahtaa

Vaiheet **1 ja 5** — kopiointi ja jäänteiden poisto — eivät poistu millään
yllä olevalla. Ne kuolevat vain, jos `docs_dir: src`, mikä on README.md:n
jäljellä oleva avoin kysymys, ja se taas edellyttää että jäljelle jäävät
sivukohtaiset muunnokset siirtyvät renderöintiin Python-Markdown-laajennuksena
(**vaihtoehto C**).

Tässä on koko juttu. PERUSTELUT.md toteaa vaihtoehto C:stä, ettei kaikkea voi
siirtää, ja luettelee neljä kirjan tason estettä: navigaatio, tulostussivun
runko, PlantUML-kuvien haku ja `NEST_UNDER`-siirrot. Kun mdBook poistuu, tuosta
listasta jää jäljelle **yksi ja puoli**:

- Navigaatio poistuu kohdan 1 mukana.
- `NEST_UNDER` poistuu kohdan 1 mukana.
- PlantUML ei ollutkaan kirjan tason työtä: `convert_plantuml` ja
  `convert_svgbob` ottavat parametrikseen yhden sivun tekstin. Vain
  `prune_diagrams` on koko puun asia, ja se on kertaluontoinen siivous.
- Tulostussivun runko jää. Se tarvitsee koko `nav`-lohkon.

Eli vaihtoehto C ei tarkoita mdBookin jälkeen enää sitä, että käännösaskel
jäisi puolitiehen. Se tarkoittaa laajennusta plus muutamaa kymmentä riviä,
jotka ajetaan vain rakenteen muuttuessa — ei jokaisen tallennuksen jälkeen.
Silloin vahtia (`--watch`) ei tarvita, koska `zensical serve` seuraa suoraan
lähdepuuta.

## Vaiheiden kohtalo yhtenä taulukkona

| Vaihe                              | Kohtalo                                                           |
| ---------------------------------- | ----------------------------------------------------------------- |
| 1. `sync_docs`                     | vasta `docs_dir: src`:n myötä, joka edellyttää vaihtoehto C:tä    |
| 2. sivun 14 muunnosta              | 1 heti, 8 uudelleenkirjoituksella, 5 jää (ks. yllä)               |
| 3. assetit                         | jää, ellei niitä siirretä `docs_dir`:n sisään                     |
| 4. `build_nav`                     | poistuu heti                                                      |
| 4. `build_extra` `edit_source`     | poistuu heti (`NEST_UNDER`:n mukana)                              |
| 4. `build_extra` `tab_labels`      | poistuu välilehtien uudelleenkirjoituksen mukana                  |
| 4. `build_print_page`              | jää                                                               |
| 5. jäänteiden poisto               | vaiheen 1 mukana                                                  |
| 5. `prune_diagrams`                | jää                                                               |
| vahti (`--watch`)                  | vaiheen 1 mukana: ilman `docs/`-kopiota ei ole mitään vahdittavaa |

## Järjestys

Kohta 1 ensin: se on pieni, ja se poistaa kolme asiaa kolmesta eri tiedostosta
kerralla. Kohta 2 sen jälkeen yhtenä committina per muunnos, jotta lähteen
diff pysyy luettavana. Vasta sitten kannattaa punnita vaihtoehto C, koska
vasta silloin tietää, kuinka pieni jäljelle jäävä joukko oikeasti on.

Ja jos vaihtoehto C jää tekemättä, mikään yllä olevasta ei mene hukkaan:
`convert.py` on silloin kolmanneksen lyhyempi ja tekee vain sitä, mitä Zensical
ei osaa.
