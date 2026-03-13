# Osa 10

> [!VAROITUS]
> Tämä osa julkaistaan 16. maaliskuuta 2026.
> {{#include ../ei-julkaistu.md}}

> [!Osaamistavoitteet]
>
> - Testaaminen (JUnit, olio-ohjelmien testaaminen)
> - SOLID-periaatteet
> - Koodihaju, refaktorointi
> - Harjoitustyön vaihe 2 palautus TIMiin
> - Harjoitustyösi täyttää vaiheen 4 vaatimukset, jotka on kuvattu harjoitustyön ohjeessa


Jatketaan oman harjoitustyön tekemistä. 

## Käyttöliittymän interaktiivinen prototyyppi

Tässä kohdassa luodaan harjoitustyön käyttöliittymälle interaktiivinen
prototyyppi. Prototyyppi ei vielä sisällä toiminnallisuutta, mutta näyttää miltä
sovellus tulee näyttämään. Se antaa myös yleiskuvan siitä miten käyttäjät voivat
olla vuorovaikutuksessa sovelluksen kanssa. 

## Näkymien luominen

Luo jokainen harjoitustyösi näkymä. 

 1. Aloita luomalla nämä näkymät SceneBuilderissa. 
 2. Lisää fx:id jokaiseen sellaiseen komponenttiin, johon todennäköisesti haluat
myöhemmin viitata koodissa. Älä unohda mahdollisia ohje- tai varoitustekstejä.
Aluksi ne voivat sisältää jonkin placeholder-tekstin. 
 3. Lisää tapahtumankäsittelijät komponentteihin, joihin haluat myöhemmin
lisätä toiminnallisuutta. Tyypillisesti nämä ovat painikkeita, alasvetovalikoita
tai muita vuorovaikutteisia elementtejä.


## Komponenttien ja tapahtumankäsittelijöiden nimeäminen SceneBuilderissa

Fx:id-tunnisteen loppuun on tapana on lisätä komponentin tyyppi. Tämä auttaa
koodin kirjoittamisessa, kun voit kirjoittaa vain *button* ja IDE osaa ehdottaa
oikeaa komponenttia.

| Komponentti | Lyhenne / Pääte | Esimerkki (fx:id)      |
| ----------- | --------------- | ---------------------- |
| Button      | btn tai Button  | loginBtn, cancelButton |
| TextField   | txt tai Field   | emailField, searchTxt  |
| Label       | lbl tai Label   | statusLabel, errorLbl  |
| ComboBox    | combo           | countryCombo           |
| TableView   | table           | userTable              |
| CheckBox    | cb tai check    | termsCheck             |


<task>
  <task-title>Tehtävä 10.1: Näkymät SceneBuilderissa. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/10-1-ht-5/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa10/tehtava1">Tee
    tehtävä TIMissä</a></task-link>
</task>

## Siirtyminen näkymästä toiseen

Näkymien välillä pitää pystyä siirtymään. Kirjoita tapahtumankäsittelijöihin
tarvittava koodi, jotta voit siirtyä näkymästä toiseen. Näin saat hyvän pohjan,
johon voit myöhemmin lisätä toiminnallisuutta.


<task>
  <task-title>Tehtävä 10.2: Siirtyminen näkymästä toiseen. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/10-2-ht-7/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa10/tehtava2">Tee
    tehtävä TIMissä</a></task-link>
</task>


<task>
  <task-title><i class="bi bi-stars jyu-gold"></i> Bonus: Tehtävä 10.3: Vaiheen
  näyttäminen ohjaajalle. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/10-3-ht-6/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa10/tehtava3">Tee
    tehtävä TIMissä</a></task-link>
</task>
