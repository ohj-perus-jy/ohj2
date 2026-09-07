# MkDocs-koeputki

Selvittää, kannattaisiko Ohj2 siirtää mdBookista Material for MkDocsiin. Tämä
hakemisto on itsenäinen: se **lukee** `../src`:ää mutta ei muuta sitä, eikä
koske `../book.toml`:iin tai `../theme/`:een. Nykyinen `bash ../start.sh` toimii
koko ajan.

## Ajaminen

```bash
./run.sh          # muunna ja tarjoile http://localhost:8001
./run.sh build    # muunna ja rakenna site/
```

Ensiasennus (devcontainerista puuttuu `python3-venv`):

```bash
sudo apt-get install -y python3-venv python3-pip
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

## Rakenne

| Tiedosto | Tehtävä |
|---|---|
| `convert.py` | Muuntaa `../src` → `docs/`. Ainoa totuus; `docs/` on kertakäyttöinen |
| `mkdocs.yml` | Material-konfiguraatio. `nav` tulee generoidusta `nav.yml`:stä |
| `extensions/custom_blocks.py` | Rekisteröi `<task>`/`<handout>` lohkoelementeiksi |
| `assets/js/hidelines.js` | `//-` piilorivien silmäikoni |
| `assets/js/playground.js` | Java-ajonappi, portattu `../theme/playground_ext.js`:stä |
| `assets/js/nav-numbers.js` | Lihavoi lukunumerot sivupalkissa |
| `assets/css/admonitions.css` | Generoitu `../theme/alerts-style.css`:stä |

## Mitä koeputki osoitti

**Toimii suoraan, ilman omaa koodia**

- Oikean reunan "Tällä sivulla" -sisällysluettelo (`toc.follow`) — alkuperäinen kysymys
- Omat suomenkieliset alert-tyypit. `mkdocs-callouts` muuntaa sisällön
  `> [!Osaamistavoitteet]` -syntaksin admonitioiksi, joten **`src/`:ään ei kosketa
  lainkaan**. Kaikki 13 tyyppiä (myös `tärkeää` ääkkösineen) värit ja SVG-ikonit
  siirtyivät suoraan
- Sisältövälilehdet, `<details>`, mermaid, koodin kopiointinappi, suomenkielinen haku
- Buildi 190 sivusta noin 28 s

**Rakennettiin itse, toimii**

- **Piilorivit (1094 kpl).** `convert.py` riisuu `//-` etuliitteen ja tallentaa
  rivinumerot `data-boring`-attribuuttiin; `pymdownx.highlight`in `line_spans`
  antaa jokaiselle riville oman spanin, jolloin JS piilottaa juuri oikeat rivit.
  Vaati ~45 riviä JS:ää ja ~45 riviä CSS:ää — selvästi vähemmän kuin pelättiin,
  eikä Python-hookia tarvittu lainkaan
- **Java-ajonappi (231 lohkoa).** Ajopalvelin ja pyyntömuoto säilyivät
  muuttumattomina; vain DOM-osa kirjoitettiin uusiksi. `// FILE:`-monitiedosto-
  esimerkit (192 markkeria) muunnetaan Materialin välilehdiksi ja ajonappi kerää
  niistä tiedostot — sama toiminnallisuus kuin `mdbook-codeblock-tabs`illa, ilman
  omaa preprocessoria

**Lukujen numerointi**

`convert.py` numeroi navigaation samoin kuin mdBook: vain SUMMARYn listakohdat
(`- [Luku](...)`) saavat numeron, juoksevasti ja `---`-erottimien yli, jolloin
etu- ja jälkisivut (Työkalut, Luennot, Eteneminen) jäävät numeroimatta.
Ylätaso `1.`–`13.`, alataso `6.1.`–`6.6.`. `mkdocs-section-index` tekee osan
etusivusta osan oman linkin, joten se ei toistu lapsena. `nav-numbers.js`
lihavoi numeron, koska se on osa nav-otsikkoa eikä sitä voi valita CSS:llä.

**Löydös: `<task>` vaatii pienen laajennuksen**

Python-Markdown käärii tuntemattomat tagit `<p>`:n sisään, jolloin
`<task>`-korttien rakenne rikkoutuu. `markdown="1"` ei yksin auta. Ratkaisu on
`extensions/custom_blocks.py` (14 riviä), joka lisää tagit
`md.block_level_elements`-listaan. Sen jälkeen `../theme/tasks.css` toimii
lähes sellaisenaan — tarvittiin yksi lisäsääntö (`task > task-title > p
{ display: contents }`), koska Python-Markdown käärii otsikon sisällön `<p>`:hen.

## Vielä auki

- Silmäikonin ja ajonapin **vuorovaikutus** on testattu vain HTML-tasolla;
  selaimessa katsominen on seuraava askel
- Kopiointinappi: kopioiko Material `display: none` -rivit mukaan? mdBook kopioi
- `bob` (11) ja `plantuml` (17) jätettiin koskematta — renderöityvät nyt
  tavallisina koodilohkoina
- `HIGHLIGHT_*_BEGIN/END` -rivikorostukset (120) portaamatta
- `<asciinema>` (13) portaamatta
- Buildin varoitukset: muutama rikkinäinen sisäinen linkki, jotka ovat olemassa
  jo nyt (esim. `osa3/03-abstraktit-luokat.md` puuttuu)
