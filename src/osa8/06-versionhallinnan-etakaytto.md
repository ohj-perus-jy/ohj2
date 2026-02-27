# Versionhallinnan etäkäyttö (Git)

Tähän asti olet käyttänyt Gittiä todennäköisesti vain paikallisesti omalla
koneellasi: olet tehnyt _commit_-komentoja ja luonut tallennuspisteitä. Jotta
koodisi on turvassa kiintolevyn rikkoutumiselta ja jotta voisit jakaa sitä
muille (esimerkiksi harjoitustyön ohjaajalle), koodi pitää viedä
**etävarastoon** (remote repository).

Tässä luvussa siirrämme paikallisen projektin GitHubiin, GitLabiin tai muuhun
valitsemaasi palveluun.

## 1. Etävaraston luominen palvelussa

1. Kirjaudu sisään valitsemaasi palveluun (esim. GitHub).
2. Etsi painike **New repository** (Uusi varasto).
3. Anna varastolle nimi (esim. `todo-sovellus`).
4. Valitse näkyvyydeksi tyypillisesti **Private** (yksityinen), jos kyseessä on
   keskeneräinen harjoitustyö, jota ei haluta jakaa julkisesti nettiin.
5. **Älä** täppää valintoja "Add a README file" tai "Add .gitignore", sillä
   meillä on jo lokaalisti olemassa oleva projekti.

Kun olet painanut "Create repository", palvelu näyttää sinulle varaston
verkko-osoitteen, joka näyttää esimerkiksi tältä:
`https://github.com/kayttajatunnus/todo-sovellus.git`

## 2. Etävaraston yhdistäminen lokaaliin projektiin

Avaa Git Bash (tai Mac/Linuxin terminaali) projektisi juuressa (siellä missä on
`.git`-kansio ja `pom.xml`).

Kerro paikalliselle Gitillesi, että tällä projektilla on nyt olemassa "koti"
internetissä:

```bash
git remote add origin https://github.com/kayttajatunnus/todo-sovellus.git
```

(Korvaa URL tietysti oman varastosi osoitteella!) Sana `origin` on
Git-maailmassa vakiintunut nimitys projektin pääasialliselle etävarastolle.

## 3. Koodin lähettäminen (Push)

Nyt voimme "työntää" koodin verkkoon:

```bash
git push -u origin main
```

Tämä komento tekee kaksi asiaa:

1. `push` lähettää lokaalit commitit etävarastoon.
2. `-u origin main` (upstream) linkittää paikallisen `main`-haarasi varaston
   `main`-haaraan. Jatkossa riittää, että kirjoitat vain `git push`.

_Huom:_ Jos lokaali haarasi on vielä myöhemmin nimetty vanhanaikaisesti
`master`, komento on `git push -u origin master`. Voit tarkistaa nykyisen
haarasi nimen komennolla `git branch`.

### Tunnistautuminen

Kun teet pusheja ensimmäistä kertaa, palvelu kysyy tunnuksiasi. Nykyään pelkkä
salasanan syöttäminen terminaaliin ei yleensä toimi turvallisuussyistä. Sinun
pitää joko:

1. Käyttää selaimen kautta aukeavaa tunnistautumisikkunaa (GitHub tekee tämän
   usein automaattisesti moderneissa Git-asennuksissa).
2. Luoda palvelun asetuksista **Personal Access Token** (PAT) ja laittaa se
   salasanan tilalle terminaaliin.
3. Ottaa käyttöön **SSH-avaimet** (suositeltu edistyneemmille).

## Jatkossa

Kun etävarasto on kerran määritelty ja ensimmäinen push on tehty, jatkossa
työnkulku on yksinkertainen:

1. Tee muutoksia koodiin.
2. `git add .`
3. `git commit -m "Lisätty muokkausikkuna"`
4. `git push`

Koodisi on nyt turvassa ja valmiina eteenpäin jaettavaksi!
