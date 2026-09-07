# MkDocs-koeputki

Selvittää, kannattaisiko Ohj2 siirtää mdBookista Material for MkDocsiin. Tämä
hakemisto on itsenäinen: se **lukee** `../src`:ää mutta ei muuta sitä, eikä
koske `../book.toml`:iin tai `../theme/`:een. Nykyinen `bash ../start.sh` toimii
koko ajan.

## Ajaminen

```bash
bash mkdocs-spike/setup.sh    # kertaluontoinen asennus (~2 min)
./mkdocs-spike/run.sh         # muunna ja tarjoile http://localhost:8001
./mkdocs-spike/run.sh build   # muunna ja rakenna site/
```

### Toisella koneella (Windows + VS Code + Docker)

1. Hae branch: `git fetch && git switch spike/mkdocs`
2. Avaa kansio VS Codessa ja valitse **Reopen in Container**. Ensimmäisellä
   kerralla image latautuu, mikä vie hetken.
3. Kontin terminaalissa: `bash mkdocs-spike/setup.sh`
4. `./mkdocs-spike/run.sh` — VS Code välittää portin 8001 automaattisesti,
   ja terminaaliin tulee klikattava linkki.

Nykyinen mdBook pyörii rinnalla omassa portissaan (`bash start.sh`), joten
molempia voi katsoa yhtä aikaa.

Skriptit ovat LF-päätteisiä (`.gitattributes: *.sh text eol=lf`), joten ne
toimivat Windowsiltakin haettuna. Jos haluat myös ACE-editorin niihin kahteen
`editable`-lohkoon, aja ensin `mdbook build` — `convert.py` kopioi ACE:n
`book/`-hakemistosta jos sellainen on olemassa.

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
