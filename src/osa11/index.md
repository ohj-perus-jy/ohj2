# Harjoitustyö, vaihe 3

Aikaisempien osien perusteella sinulla pitäisi olla sovelluksen runko valmiina.
Tässä vaiheessa toteutetaan harjoitustyön toiminnallisuudet, eli kytketään
tietomalli käyttöliittymään. 

Tässä vaiheessa kunkin tehtävän kohdalle palautetaan kyseiseen tehtävään
liittyvä URL-osoite, joka sisältää niin sanotun *commit hashin*. Tällä tavalla
ohjaaja pääsee tarvittaessa tarkastelemaan juuri tiettyyn vaiheeseen liittyvää
koodia.

## Commit hash

Commit hash on Gitin muodostama yksilöllinen tunniste yksittäiselle commitille.
Se näyttää yleensä pitkältä merkkijonolta, kuten `a1b2c3d4...`, ja sen avulla
voidaan viitata täsmällisesti juuri tiettyyn projektin tilaan.

Commitin tarkoitus on tallentaa yksi versio projektista versionhallintaan.
Commit hash taas kertoo, *mikä* näistä tallennetuista versioista on kyseessä.
Kun tehtävän palautuksessa annetaan commit hash, ohjaaja voi avata juuri sen
hetken koodin, jossa tehtävä on ollut valmiina.

Commit hash ei edusta vain yksittäistä tiedostoa tai muutosta, vaan
commit-oliota, joka sisältää metatietoa yhdestä commitista: Näitä ovat
esimerkiksi viesti ("message"), tekijä ("author"), viittaus projektin
hakemistorakenteeseen ("tree") sekä viittaus edelliseen commitiin ("parent"). 

GitLab- ja GitHub-palveluissa on mahdollisuus tarkastella committeja siten, että
hash-arvo on suoraan URL-osoitteessa.

**Commit hash -osoitteen esimerkki GitLabissa**

 1. Kirjaudu GitLabiin ja avaa projektisi.
 2. Klikkaa vasemmalta Code <i class="bi bi-chevron-right"></i> Commits.
 3. Näet listan commiteista. Valitse se commit, joka liittyy tehtävän palautukseen. Klikkaa sitä.
 4. Osoiterivillä näkyy URL-osoite, joka sisältää commit hash -arvon. Kopioi tämä URL-osoite ja liitä se tehtävän palautukseen.

**Commit hash -osoitteen esimerkki GitHubissa**

 1. Kirjaudu GitHubiin ja avaa projektisi.
 2. Klikkaa vihreän Code-kuvakkeen alta **NNN Commits**, jossa NNN on committien määrä.
 3. Näet listan commiteista. Valitse se commit, joka liittyy tehtävän palautukseen. Klikkaa sitä.
 4. Osoiterivillä näkyy URL-osoite, joka sisältää commit hash -arvon. Kopioi tämä URL-osoite ja liitä se tehtävän palautukseen.

## Tehtävät

Kuhunkin tehtävään palautetaan URL-osoite, joka vie commitiin etävarastossasi.
Jos olet tehnyt omaa työtäsi hieman eri rytmissä kuin tässä vaiheistuksessa on
esitetty, palauta URL-osoite siihen commitiin joka parhaiten edustaa kyseisen
tehtävän vaatimuksia.

<task>
  <task-title num="11.1">Tiedon lisääminen.<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/11-1-ht-9/handout.md}}

</handout>
    <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa11/tehtava1">Tee tehtävä TIMissä</a></task-link>

</task>

<task>
    <task-title num="11.2">Poistaminen.<points>1 p.</points></task-title>
<handout>

{{#include ../exercises/11-2-ht-10/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa11/tehtava2">Tee
    tehtävä TIMissä</a></task-link>
</task>

<task>
    <task-title num="11.3">Tallentaminen ja lukeminen tiedostosta.<points>1 p.</points></task-title>

<handout>

{{#include ../exercises/11-3-ht-11/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa11/tehtava3">Tee
    tehtävä TIMissä</a></task-link>
</task>

<task>
    <task-title num="11.4">Tiedon muokkaaminen.<points>1 p.</points></task-title>
<handout>

{{#include ../exercises/11-4-ht-12/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa11/tehtava4">Tee
    tehtävä TIMissä</a></task-link>
</task>

<task>
<task-title num="11.5">Validointi.<points>1 p.</points></task-title>
<handout>

{{#include ../exercises/11-5-ht-13/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa11/tehtava5">Tee
    tehtävä TIMissä</a></task-link>
</task>

<task>
    <task-title num="11.6">Yksikkötestit.<points>1 p.</points></task-title>
    <handout>

{{#include ../exercises/11-6-ht-14/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa11/tehtava6">Tee
    tehtävä TIMissä</a></task-link>
</task>

<task>
    <task-title num="11.7">README-tiedosto.<points>1 p.</points></task-title>
<handout>

{{#include ../exercises/11-7-ht-15/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa11/tehtava7">Tee
    tehtävä TIMissä</a></task-link>
</task>

<task>
    <task-title num="11.8"><i class="bi bi-stars"></i>Bonus: Näytä vaihe ohjaajalle.<points>1 p.</points></task-title>

<handout>

{{#include ../exercises/11-8-ht-16/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa11/tehtava8">Tee
    tehtävä TIMissä</a></task-link>
</task>
