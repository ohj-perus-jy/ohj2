# Harjoitustyö, vaihe 2

> [!VAROITUS]
> Tämä osa julkaistaan 16. maaliskuuta 2026.
> {{#include ../ei-julkaistu.md}}

Jatketaan oman harjoitustyön tekemistä luomalla harjoitustyön käyttöliittymälle
interaktiivinen prototyyppi. Prototyypin ei vielä tarvitse sisältää varsinaista
toiminnallisuutta, mutta se antaa kuvan siitä, miltä sovellus tulee näyttämään.
Lisäksi se antaa käsityksen siitä, miten käyttäjä voi olla vuorovaikutuksessa
sovelluksen kanssa. 

## Näkymien luominen

Luo jokainen harjoitustyösi näkymä SceneBuilderissa. 

Lisää fx:id jokaiseen sellaiseen komponenttiin, johon todennäköisesti haluat
myöhemmin viitata koodissa. Älä unohda mahdollisia ohje- tai varoitustekstejä.
Aluksi ne voivat sisältää placeholder-tekstin. 

## Tapahtumankäsittelijät

Lisää tapahtumankäsittelijät jokaiseen komponenttiin, joihin haluat myöhemmin
lisätä toiminnallisuutta, kuten siirtymisiä muihin näkymiin, olioiden
lisäämistä, poistamista, jne. Tyypillisesti tällaiset komponentit ovat
painikkeita, alasvetovalikoita tai vastaavia. 

Tapahtumankäsittelijöille voi luoda pohjat myös SceneBuilderissa. Klikkaa
Code-kohtaa ja anna "On Action"-kohtaan tapahtumankäsittelijän nimi, esimerkiksi
`handleLoginButton`. 

## Komponenttien ja tapahtumankäsittelijöiden nimeäminen

Fx:id-tunnisteen loppuun on tapana on lisätä komponentin tyyppi. Tämä auttaa
koodin kirjoittamisessa, kun voit kirjoittaa vain *button* ja IDE osaa ehdottaa
oikeaa komponenttia.

| Komponentti | Lyhenne / Pääte | Esimerkki (fx:id)          |
| ----------- | --------------- | -------------------------- |
| Button      | btn tai Button  | `tallennaBtn`, `peruutaButton` |
| TextField   | txt tai Field   | `emailField`, `statusTxt`  |
| Label       | lbl tai Label   | `ilmoitusLabel`, `virheLbl`  |
| ComboBox    | combo           | `maaCombo`             |
| TableView   | table           | `kayttajaTable`, `tehtavaTable`                |
| CheckBox    | cb tai check    | `suodatusCheck`               |

Tapahtumankäsittelijöiden kohdalla on tapana käyttää `handle`- tai
`kasittele`-etuliitettä. Esimerkiksi `kasitteleUusiOstostapahtuma` voisi olla
tapahtumankäsittelijä, joka liittyy `uusiOstostapahtumaButton`-painikkeeseen.

## Kontrolleriluokkien nimeäminen

Näkymille kannattaa jo SceneBuilderissa antaa kontrolleriluokka, vaikka niitä ei
olisikaan vielä olemassa. Nimi syötetään kohtaan Controller <i class="bi
bi-arrow-right"></i> Controller class. Nimi tulee valita niin, että se on sama
kuin näkymän nimi, perään lisättynä "Controller"-sana. Esimerkiksi
`SyotaTehtava.fxml`-näkymälle sopisi `SyotaTehtavaController`-kontrolleriluokka.

> [!TÄRKEÄÄ]
> Kontrolleriluokan nimi tulee antaa nimi kokonaisuudessaan pakkauksen kanssa,
> esimerkiksi `fi.jyu.ohj2.anlakane.todo.SyotaTehtavaController`. Jos annat
> pelkän luokan nimen, kuten `SyotaTehtavaController`, IDE ei löydä luokkaa.

<task>
  <task-title>Tehtävä 10.1: Näkymät SceneBuilderissa. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/10-1-ht-5/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa10/tehtava1">Tee
    tehtävä TIMissä</a></task-link>
</task>

## Kontrolleri-luokkien luominen

Luo jokaiselle näkymälle oma kontrolleri-luokka. Vinkki: Saat SceneBuilderista
kontrolleriluokan pohjan, jonka voit copy-pasteta projektiisi. Klikkaa View <i
class="bi bi-arrow-right"></i> Show Sample Controller Skeleton. Täydennä siihen
tarvittavat tyypit `?`-merkkien kohdalle.

<task>
  <task-title>Tehtävä 10.2: Kontrollerit. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/10-2-ht-6/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa10/tehtava2">Tee
    tehtävä TIMissä</a></task-link>
</task>

## Siirtyminen näkymästä toiseen

Näkymien välillä pitää pystyä siirtymään. Kirjoita tapahtumankäsittelijöihin
tarvittava koodi, jotta voit siirtyä näkymästä toiseen. Myös kaikkien muiden
vuorovaikutteisten elementtien, kuten painikkeiden, pitää tehdä jotain,
esimerkiksi tulostaa konsoliin. Näin saat hyvän pohjan, johon voit myöhemmin
lisätä toiminnallisuutta. 

<task>
  <task-title>Tehtävä 10.3: Siirtyminen näkymästä toiseen. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/10-3-ht-7/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa10/tehtava3">Tee
    tehtävä TIMissä</a></task-link>
</task>


## Näyttäminen ohjaajalle

Kuten osassa 9, suosittelemme tässäkin vaiheessa näyttämään harjoitustyön
vaiheen ohjaajalle. 

<task>
  <task-title><i class="bi bi-stars jyu-gold"></i> Bonus: Tehtävä 10.4: Vaiheen
  näyttäminen ohjaajalle. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/10-4-ht-8/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa10/tehtava4">Tee
    tehtävä TIMissä</a></task-link>
</task>
