# Osallistuminen ja kehittäminen

Tervetuloa mukaan kehittämään Ohjelmointi 2 -kurssin materiaalia! Kaikki
korjaukset ovat tervetulleita, kirjoitusvirheistä laajempiin
sisältömuutoksiin.

## Lisenssi

Tähän repoon tehdyt muutokset julkaistaan [CC BY-SA 4.0](LICENSE)
-lisenssillä. Lähettämällä muutoksia hyväksyt, että muutoksesi julkaistaan
CC BY-SA 4.0 -lisenssin ehdoilla.

Lisenssi ei koske issueita.

## Miten voit auttaa?

1. **Ilmoita ongelmasta.** Sivun alareunan *Ilmoita ongelma* -linkki avaa
   [issue-lomakkeen](https://github.com/ohj-perus-jy/ohj2/issues/new/choose),
   jossa sivun nimi on jo valmiina.
2. **Korjaa pieni virhe selaimessa.** Sivun alareunan *Muokkaa*-linkki avaa
   sivun lähdetiedoston GitHubin editorissa. Jos sinulla ei ole
   kirjoitusoikeutta repoon, GitHub tekee sinulle oman kopion (forkin) ja
   ehdottaa muutosta pull requestina.
   [Ohje tiedostojen muokkaamiseen GitHubissa](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files).
3. **Tee laajempia muutoksia omalla koneella.** Uusia lukuja, esimerkkejä tai
   kuvia varten kannattaa pystyttää kehitysympäristö. Näet silloin sivut
   sellaisina kuin ne julkaistaan.

## Kehitysympäristö

Sivusto rakennetaan **[Zensicalilla](https://zensical.org)**. Työkalut
(muunnos, tyylit, skriptit, testit) ovat git-submodule `zensical/tyokalut`,
repo [kirjatyokalut](https://github.com/ohj-perus-jy/kirjatyokalut).

Kloonaa repo submoduleineen. Jos sinulla ei ole kirjoitusoikeutta, forkkaa
repo ensin ja kloonaa oma forkkisi.

```bash
git clone --recurse-submodules https://github.com/ohj-perus-jy/ohj2.git
cd ohj2
git config submodule.recurse true    # git pull ja git switch päivittävät jatkossa myös työkalut
```

Windowsissa avaa WSL, ja kloonaa WSL:n levylle, älä Windowsin kansioon (`C:\…`), koska
asennus on sieltä hidasta. Avaa WSL-pääte (`wsl`), kloonaa
kotihakemistoosi ja avaa kansio VS Codessa komennolla `code ohj2`.

Suositeltu tapa on käyttää mukana olevaa DevContaineria. Se hakee submodulen ja
asentaa Zensicalin hakemistoon `zensical/.venv` jo kontin luonnissa. Jos et
halua käyttää DevContaineria, ensimmäinen käynnistys (ks. alla) asentaa
tarvittavat työkalut ja riippuvuudet. 

Käynnistä kehityspalvelin projektin juuresta:

```bash
./zensical/run.sh            # http://localhost:8001, seuraa src/:n muutoksia
./zensical/run.sh 8003       # eri portti
./zensical/run.sh build      # pelkkä rakennus zensical/site/-hakemistoon
./zensical/run.sh test       # testit (pytest + Playwright)
```

**Muokattava sisältö on kansiossa `src/`.** Älä muokkaa tiedostoja kansioissa
`zensical/docs/` ja `zensical/site/`.

## Kirjoittaminen

Sivut kirjoitetaan Markdownilla mdBookin merkkauksella; työkalut muuntavat
sen Zensicalille. Navigaatio on tiedostossa `src/SUMMARY.md`. Sivun osoite
tulee tiedoston polusta, eikä vanhoille osoitteille ole ohjauksia: sivun
siirto tai uudelleennimeäminen rikkoo TIMin linkit, joten päivitä ne samalla.

Kaikki työkalujen tukema merkkaus on kirjatyökalujen
[Ominaisuudet-taulukossa](https://github.com/ohj-perus-jy/kirjatyokalut#ominaisuudet):
alertit, välilehdet, piilorivit, korostetut rivit (`// HIGHLIGHT_GREEN_BEGIN`),
monitiedostoiset koodiesimerkit (`// FILE: Kissa.java`), kaaviot,
vaiheittainen ohje, Testaa tietosi -visa ja muut. Teeman omat ominaisuudet
ovat [Zensicalin ohjeissa](https://zensical.org/docs/).

### Tehtävälohko

Tehtävällä on oma `task`-elementti, joka sisältää tehtävän otsikon,
tehtävänannon ja linkin TIM-tehtävään.

````md
<task>
<task-title num="1.1">Oma ohjelma Javalla<points>1 p.</points></task-title>
<handout>

{{#include ../exercises/1-1-eka-ohjelma/handout.md}}

</handout>
<task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa1/tehtava1">Tee tehtävä TIMissä</a></task-link>
</task>
````

Kirjoita `include`-makro ihan vasempaan reunaan, jotta Markdown-ladonta ei
tulkitse sitä koodilohkoksi.

### Kirjoitusasu

- Valikkopolut kirjoitetaan kursiivilla ja kohdat erotetaan ›-merkillä:
  *File* › *New* › *Project*.
- Lukuvälit kirjoitetaan pitkällä viivalla: 1–3, ei 1-3.
- Listan kohtaan kuuluva jatkokappale, kuva, koodilohko tai `<details>`
  sisennetään neljällä välilyönnillä. Muuten numeroitu lista alkaa alusta.
- Kaavoja ei renderöidä. Eksponentti kirjoitetaan `2<sup>31</sup>` ja
  kertomerkki `·`.

## Haarat ja julkaisu

- `main` on tuotanto (<https://ohjelmointi2.it.jyu.fi>).
- `dev` on ylläpitäjien työhaara, ja sen esikatselu on osoitteessa
  <https://ohjelmointi2.it.jyu.fi/dev/>.

GitHub Actions julkaisee molemmat joka työnnöllä. Ulkoiset linkit
tarkistetaan joka työnnössä, pull requestissa ja maanantaisin (lychee,
`.github/workflows/links.yml`).

Ylläpitäjille: isot tai keskeneräiset muutokset (uudet luvut, rakenne)
tehdään `dev`iin ja viedään `dev` → `main`. Pienet korjaukset,
työkalupäivitykset ja pull requestit menevät suoraan `main`iin. Kun `main`
muuttuu, yhdistä `main` → `dev`. Haarat yhdistetään aina merge-commitilla,
ei rebasella eikä squashilla. `pages.yml`:n on oltava sama molemmissa
haaroissa, koska kummankin työntö julkaisee molemmat sivustot.

## Pull request

Tee pull request `main`-haaraan.

1. Luo uusi haara:

    ```bash
    git switch -c korjaus-aihe
    ```

2. Muokkaa `src/`-kansion tiedostoja ja tarkista tulos kehityspalvelimella.
3. Commitoi ja pushaa. Jos muutos liittyy issueen, mainitse se viestissä
   (esim. `Korjattu kirjoitusvirhe, #123`).

    ```bash
    git add src/
    git commit -m "Kuvaava viesti muutoksesta"
    git push -u origin korjaus-aihe
    ```

4. Avaa GitHubissa pull request `main`-haaraan. Ylläpitäjät tarkistavat
   ehdotuksesi ja antavat tarvittaessa palautetta.

## Lisää

- [zensical/README.md](zensical/README.md): tämän kirjan asetukset
  (`kirja.toml`, `mkdocs.yml`, kaaviot, ääneenluku) ja työkalujen päivittäminen
- [kirjatyokalut/README.md](https://github.com/ohj-perus-jy/kirjatyokalut#readme):
  rakenne, asetukset, työkalujen muuttaminen ja testit
- [TODO.md](TODO.md): avoimet tehtävät

Kiitos avustasi materiaalin parantamisessa!
