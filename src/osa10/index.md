# Harjoitustyö, vaihe 2

> [!VAROITUS]
> Tämä osa julkaistaan 16. maaliskuuta 2026.
> {{#include ../ei-julkaistu.md}}

Jatketaan oman harjoitustyön tekemistä. 

## Käyttöliittymän interaktiivinen prototyyppi

Tässä kohdassa luodaan harjoitustyön käyttöliittymälle interaktiivinen
prototyyppi. Prototyyppi ei vielä sisällä toiminnallisuutta, mutta näyttää miltä
sovellus tulee näyttämään. Se antaa myös yleiskuvan siitä miten käyttäjät voivat
olla vuorovaikutuksessa sovelluksen kanssa. 

## Näkymien luominen

Luo jokainen harjoitustyösi näkymä. 

Aloita luomalla nämä näkymät SceneBuilderissa. 

Lisää fx:id jokaiseen sellaiseen komponenttiin, johon todennäköisesti haluat
myöhemmin viitata koodissa. Älä unohda mahdollisia ohje- tai varoitustekstejä.
Aluksi ne voivat sisältää jonkin placeholder-tekstin. 

## Tapahtumankäsittelijät

Lisää tapahtumankäsittelijät komponentteihin, joihin haluat myöhemmin lisätä
toiminnallisuutta. Tyypillisesti nämä ovat painikkeita, alasvetovalikoita tai
muita vuorovaikutteisia elementtejä.

Tapahtumankäsittelijöille voi luoda pohjan myös SceneBuilderissa. Klikkaa
Code-kohtaa ja anna "On Action"-kohtaan tapahtumankäsittelijän nimi, esimerkiksi
`handleLoginButton`. 

## Komponenttien ja tapahtumankäsittelijöiden nimeäminen SceneBuilderissa

Fx:id-tunnisteen loppuun on tapana on lisätä komponentin tyyppi. Tämä auttaa
koodin kirjoittamisessa, kun voit kirjoittaa vain *button* ja IDE osaa ehdottaa
oikeaa komponenttia.

| Komponentti | Lyhenne / Pääte | Esimerkki (fx:id)          |
| ----------- | --------------- | -------------------------- |
| Button      | btn tai Button  | `loginBtn`, `cancelButton` |
| TextField   | txt tai Field   | `emailField`, `searchTxt`  |
| Label       | lbl tai Label   | `statusLabel`, `errorLbl`  |
| ComboBox    | combo           | `countryCombo`             |
| TableView   | table           | `userTable`                |
| CheckBox    | cb tai check    | `termsCheck`               |

Tapahtumankäsittelijöiden kohdalla tapana on käyttää `handle`- tai
`kasittele`-etuliitettä. Esimerkiksi `kasitteleUusiOstostapahtuma` voisi olla
tapahtumankäsittelijä, joka liittyy `uusiOstostapahtumaButton`-painikkeeseen.

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
tarvittava koodi, jotta voit siirtyä näkymästä toiseen. Myös kaikkien muiden
vuorovaikutteisten elementtien, kuten painikkeiden, pitää tehdä jotain,
esimerkiksi tulostaa konsoliin. Näin saat hyvän pohjan, johon voit myöhemmin
lisätä toiminnallisuutta. 

<task>
  <task-title>Tehtävä 10.2: Siirtyminen näkymästä toiseen. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/10-2-ht-6/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa10/tehtava2">Tee
    tehtävä TIMissä</a></task-link>
</task>


## Näyttäminen ohjaajalle

Kuten osassa 9, suosittelemme tässäkin vaiheessa näyttämään harjoitustyön
vaiheen ohjaajalle. 

<task>
  <task-title><i class="bi bi-stars jyu-gold"></i> Bonus: Tehtävä 10.3: Vaiheen
  näyttäminen ohjaajalle. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/10-3-ht-7/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa10/tehtava3">Tee
    tehtävä TIMissä</a></task-link>
</task>
