# Osallistuminen ja kehittäminen (Contributing)

Tervetuloa mukaan kehittämään Ohjelmointi 2 -kurssimateriaalia! Arvostamme suuresti kaikkia parannusehdotuksia, olivat ne sitten pieniä kirjoitusvirheiden korjauksia tai laajempia sisältömuutoksia.

## Lisenssi

Huomioithan, että tähän repoon tehdyt muutokset julkaistaan 
[CC BY-SA 4.0](LICENSE) -lisenssillä. 
Lähettämällä muutoksia tämän repon sisältöön hyväksyt, että muutoksesi
julkaistaan CC BY-SA 4.0 -lisenssin ehdoilla.

Lisenssi ei koske tähän repoon lähetettyjä issue-kortteja.

## Miten voit auttaa?

Voit osallistua monella tavalla:

1.  **Ilmoita ongelmasta:** Jos huomaat virheen mutta et ehdi korjata sitä itse, [luo uusi Issue](https://github.com/ohj-perus-jy/ohj2/issues/new).
2.  **Pienet korjaukset:** Kirjoitusvirheet ja pienet selkeytykset on helpointa tehdä suoraan selaimessa GitHubin web-käyttöliittymän kautta.
    - [Ohje tiedostojen muokkaamiseen GitHubissa](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)
3.  **Laajemmat muutokset:** Jos haluat lisätä uusia esimerkkejä tai lukuja, suosittelemme pystyttämään paikallisen kehitysympäristön.

---

## Kehitysympäristön pystyttäminen

Jos haluat tehdä laajempia muutoksia ja nähdä ne livenä omalla koneellasi, toimi seuraavasti:

### 1. Autentikointi ja kloonaus
Suosittelemme [SSH-avaimen](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) käyttöä autentikointiin.

```bash
git clone --recurse-submodules git@github.com:ohj-perus-jy/ohj2.git
cd ohj2
git config submodule.recurse true    # git pull ja git switch päivittävät jatkossa myös työkalut
```

### 2. Työkalujen asennus
Materiaali on toteutettu **[Zensicalilla](https://zensical.org)**. Työkalut
ovat git-submodule `zensical/tyokalut`. Suositeltu tapa on käyttää mukana
olevaa DevContaineria: se hakee submodulen ja asentaa Zensicalin jo kontin
luonnissa.

Jos et käytä DevContaineria, tarvitset Python 3.11:n tai uudemman. Ensimmäinen
`./zensical/run.sh` asentaa loput hakemistoon `zensical/.venv` (tarvittaessa
myös `python3-venv`-paketin, mihin tarvitaan sudo).

### 3. Paikallinen esikatselu
Käynnistä kehityspalvelin projektin juuresta:
```bash
./zensical/run.sh
```
Materiaali on osoitteessa <http://localhost:8001>, ja näkymä päivittyy automaattisesti, kun tallennat muutoksia.

Voit testata pelkän käännöksen ilman kehityspalvelinta ajamalla:

```bash
./zensical/run.sh build
```

---

## Työnkulku (Workflow)

Kun haluat ehdottaa muutoksia, noudata tätä prosessia:

1.  **Luo uusi branch:**
    ```bash
    git switch -c korjaus-aihe
    ```
2.  **Tee muutokset:** Muokkaa `src`-kansion markdown-tiedostoja. Noudata projektin tyyliopasta ja olemassa olevia käytänteitä.
3.  **Commit & Push:**
    Pyri kirjoittamaan selkeitä commit-viestejä. Jos muutoksesi liittyy avoimeen issueen, voit linkittää sen viestissä (esim. `Korjattu typo #123`).
    ```bash
    git add .
    git commit -m "Kuvaava viesti muutoksesta"
    git push -u origin korjaus-aihe
    ```
4.  **Tee Pull Request (PR):**
    Avaa GitHubissa projektin sivu ja luo uusi Pull Request branchistasi. Ohjaajat tarkistavat ehdotuksesi ja antavat tarvittaessa palautetta.

Kiitos avustasi materiaalin parantamisessa!
