# TODO

Siirto mdBookista Zensicaliin on tehty: tuotannossa ja mdBook poistettu
2026-09-20. Vaiheet ja päätökset ovat gitin historiassa
(`git log -p -- zensical/KAYTTOONOTTO.md`). Haarat ja työtavat:
[CONTRIBUTING.md](CONTRIBUTING.md). Merkkauksen siirto mdBookin syntaksista
Zensicalin omaan ja työkalujen avoimet asiat: `zensical/tyokalut/YHTENAISTYS.md`.

## Aineisto

- [ ] `osa1/index.md`, *Materiaalin käytöstä* (r. 11–16): yläpalkin kuvaus on
      mdBookin. Teemanappi on kaksiasentoinen (vaalea, tumma), eikä
      kirjasinvalikkoa mainita. Tarkista samalla sisällysluettelon rivi.
- [ ] `osa8/01-malli-ja-observable-rajapinta.md` (r. 96 ja 182): piilorivin
      kommentti "jotta mdbookissa voidaan matkia" näkyy silmänapilla.
      Esimerkiksi "jotta esimerkin voi ajaa kirjassa".
- [ ] `src/mdbook-plantuml-img/` (17 SVG) on mdBookin PlantUML-liitännäisen
      tuloste. Mikään ei viittaa siihen, mutta se julkaistaan. Kaaviot ovat
      nyt `zensical/cache/plantuml/`:ssa. Poista.

## Julkaisu

- [ ] 117 tiedostoa `SUMMARY.md`:n ulkopuolelta julkaistaan sivuina ja
      näkyvät haussa, mm. 103 tehtävänantoa, luonnokset (`*/jemma*.md`,
      `osa5/huomiot.md`) ja `takarajat.md`. mdBook ei julkaissut niitä.
      Rajaa `kirja.toml`:n `ei_sivuja`-listalla, jos TIM ei linkitä niihin.
- [ ] `kirja.toml`: `[testit] rikkinaiset_kuvat` on vanhentunut. Kuva siirtyi
      `osa4/images/`:iin 2026-09-11 (`05cea84`), ja osoite vastaa 200. Poista
      osio ja aja `./zensical/run.sh test`.
- [ ] *Settings* › *Pages* › *Enforce HTTPS* on pois: `http://`-osoite vastaa
      200 ilman ohjausta, vaikka varmenne on voimassa. Sama ohj1:ssä ja
      jypelidocsissa.

## Linkit

- [ ] TIMin linkit kirjaan hakemistomuotoon (`tentti.html` → `tentti/`,
      `tenttiohjeet.html` → `tentti/tenttiohjeet/`). Korjaamatta:
      `tehtavat/templates/preambles/preamble`, `tehtavat/osa1/tehtava3`
      (`suorittaminen.html#eettiset-ohjeet`) ja 14 menneen tentin dokumenttia
      kansiossa `tentti/`. Kansio ei ole julkinen: tarkista kirjautuneena.

## Kehitysympäristö

- [ ] Devcontainerin kuva `ohj-mdbook-tooling` →
      `mcr.microsoft.com/devcontainers/python:3.11-bookworm` ja feature
      `ghcr.io/devcontainers/features/rust:1` (svgbob_cli), kuten
      jypelidocsissa. Kuvan repon arkistointi: ohj1:n TODO.md.

## Merkkaus

- [ ] Lähde Zensicalin merkintätapaan YHTENAISTYS.md:n taulukon mukaan.
      Ei odota mitään; tehty on `[siirrot]` (`NEST_UNDER`) ja
      `DROP_SECTIONS` 2026-09-21.
