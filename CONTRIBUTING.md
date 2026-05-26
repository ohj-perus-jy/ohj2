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
git clone git@github.com:ohj-perus-jy/ohj2.git
cd ohj2
```

### 2. Työkalujen asennus
Materiaali on toteutettu **mdBookilla**. Suositeltu tapa on käyttää mukana
olevaa DevContaineria, joka sisältää mdBookin ja tarvittavat laajennokset
valmiiksi asennettuina.

Jos et käytä DevContaineria, tarvitset [Rust & Cargon](https://www.rust-lang.org/tools/install)
ja voit asentaa mdBook-työkalut fallback-skriptillä:

```bash
bash ./update-mdbook.sh
```

### 3. Paikallinen esikatselu
Käynnistä kehityspalvelin projektin juuresta:
```bash
bash ./start.sh
```
Tämä avaa materiaalin selaimeesi (oletuksena localhost:3000) ja päivittää näkymän automaattisesti, kun tallennat muutoksia.

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
