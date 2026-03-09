# Harjoitustyö, vaihe 1

> [!VAROITUS]
> Tämä osa julkaistaan 9. maaliskuuta 2026.
> {{#include ../ei-julkaistu.md}}

Tässä osassa aloitetaan oman harjoitustyön toteutus. Harjoitustyö toteutetaan
vaiheittain osissa 9-12, ja viimeistään osan 12 loppuun mennessä harjoitustyö
tulee palauttaa ja hyväksyttää tuntiopettajalla etä- tai lähiohjauksessa. Lue
huolellisesti [harjoitustyön vaatimukset](../harjoitustyo.md) ennen
aloittamista. 

Osissa 9-12 on annettu ohjeita, joiden tarkoituksena on auttaa sinua etenemään
harjoitustyössä. Vastaavasti osat 9-12 sisältävät tehtäviä, joiden tarkoitus on
auttaa projektin edistämistä vaiheittain. Kuten aiemminkin, tehtävistä on
palautettava vähintään 50 %.

Suosittelemme toteuttamaan harjoitustyön näissä osissa kuvattua vaiheistusta
hyödyntäen.

## Harjoitustyön aihe

Aloita ensin valitsemalla harjoitustyön aihe ja tutustumalla harjoitustyön
vaatimuksiin. Löydät valmiita aiheita [harjoitustyön
ohjesivulta](../harjoitustyo.md).

Kun olet valinnut aiheen, ilmoita se alla olevan tehtävän kautta.

<task>
  <task-title>Tehtävä 9.1: Harjoitustyö, aiheen valinta. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/9-1-ht-1/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa9/tehtava1">Tee
    tehtävä TIMissä</a></task-link>
</task>

## Projektin alustaminen

Kun olet valinnut aiheen, voit luoda valmiiksi uuden JavaFX-projektin.
Suosittelemme, että käytät kurssin valmista JavaFX-pohjaa, jonka käyttöä on
esitelty [osassa
7.1](../osa7/01-javafx-perusteet.md#ensimmäinen-javafx-sovellus).

Vinkkejä:

- Tee aluksi harjoitustyölle oma erillinen tyhjä kansio paikasta, jonka pystyt
  helposti löytämään tietokoneeltasi. 
- Kun luot projektia IDEAssa, valitse projektin poluksi (*Location*-asetus)
  juuri tuo äsken tekemäsi kansio. tietokoneelta. 
- Aseta projektillesi yksilöllinen tunniste (GroupId). Voit käyttää muotoa
  `fi.jyu.ohj2.nimesi.aihe`, jossa `nimesi` on yliopiston tunnuksesi ja `aihe`
  on harjoitustyön aihe. 

Kun saat projektin luotua, kokeile ajaa se ja varmista, että saat sovelluksen
käynnistettyä.

## Git-varaston alustaminen

Kun projekti on luotu, luo saman tien projektikansioon Git-varasto
komentoriviltä komennolla `git init`. Älä kuitenkaan tee vielä heti ensimmäistä
commitia, vaan valmistellaan ensin hieman kansion sisältöä.

Git-versiohallintaa käyttäviin projekteihin on tapana sisällyttää `.gitignore`-
ja `README.md`-tiedostot. `.gitignore`-tiedoston merkitystä on esitelty hieman
[osassa 7.3](../osa7/03-versionhallinta.md): tähän tiedostoon listattuja
tiedostoja ja kansioita ei sisällytetä commiteihin ilman erityistä pakotusta.
Esimerkkejä tällaisista ovat esimerkiksi IDEAn luomat `out`- ja
`target`-kansiot, joissa on käännettyä koodia. Erityisen tärkeää on muistaa
lisätä `.gitignore`-tiedostoon mahdolliset salaisuuksia sisältävät tiedostot,
kuten henkilötietoja, salasanoja tai API-avaimia sisältävät tiedostot, jotta ne
eivät päädy vahingossa etävarastoon. 

Varmista, että projektikansiossasi on `.gitignore`-tiedosto. Jos käytät kurssin
valmista JavaFX-pohjaa, sellainen tiedosto on valmiiksi sisällytetty projektiin. 

Huomaa kirjoitusasu: tiedoston nimi on `.gitignore`, alussa piste ja kaikki
pienellä. Vastaavasti `README.md`-tiedoston nimi on kaikki isoilla kirjaimilla,
eikä siinä ole alussa pistettä.

`README.md`, eli ns. "Lue minut"-tiedosto, on tarkoitettu projektin esittämiseen
ja toisaalta kehittämisen kannalta oleellisiin ohjeisiin. Etävarastopalvelut
yleensä näyttävät tämän tiedoston heti projektin etusivulla, joten tiedosto on
myös hyvä paikka kertoa projektista yleisesti ei-tekniselle peruskäyttäjälle.
Voit luoda `README.md`-tiedoston suoraan IDEAssa klikkaamalla projektiselaimessa
projektista hiiren toissijaisella painikkeella, valitsemalla **New** <i
class="bi bi-chevron-right"></i> **File** ja antamalla tiedoston nimeksi
`README.md`:

<video src="images/intellij-readme-md.mp4" controls></video>

`README.md`-tiedosto on tapana kirjoittaa käyttäen
[Markdown-merkintäkieltä](https://www.markdownguide.org/basic-syntax/).

Tässä vaiheessa README-tiedosto voi olla aika alkeellinen. Lisää tiedostoon
ainakin projektin nimi ja lyhyt kuvaus parilla virkkeellä.
Jos käytät valmista aihetta, voit kopioida projektin aiheen kuvauksen [harjoitustyön
ohjeesta](../harjoitustyo.md#harjoitustyön-aihe).

Kun saat `README` ja `.gitignore` -tiedostot tehtyä, tee ensimmäinen commit.
Luo lopuksi uusi etävarasto ja lataa nykyinen varastosi sinne [osan
8.6](../osa8/06-versionhallinnan-etakaytto.md) ohjeiden perusteella.


<task>
  <task-title>Tehtävä 9.2: Harjoitustyö, Git-etävarasto. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/9-2-ht-2/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa9/tehtava2">Tee
    tehtävä TIMissä</a></task-link>
</task>

## Tietomallin toteuttaminen

Ennen kuin menet syvemmin käyttöliittymään, on syytä ensin pohtia sovelluksen
tietomallia ja sen toimintaa. 
Aloita kehitystyö toteuttamalla tietomallin kannalta
oleelliset luokat projektiin. Valmiissa aiheessa luokat, niiden attribuutit ja
luokkien väliset suhteet on esitetty UML-kaaviona.

Vinkkejä:

- Tee tietomallin attribuutit käyttäen JavaFX `Property`-tyyppejä valmiiksi.
  Tämä helpottaa näkymän ja tietomallin kytkemistä yhteen myöhemmin.
- Laita tietomalliin liittyvät luokat valmiiksi `model`-alipakkaukseen erillään
  muista luokista.
- Mieti jo hieman, mitä julkisia metodeja luokan on hyvää tarjota muille
  luokille. Vaikka get- ja set-metodeja tarvitaan tietomallin tallentamiseksi
  JSON-muotoon, voit jo alustavasti miettiä, mitä metodeja luokka voisi tarjota
  parantakseen
  [kapselointia](../osa2/03-kapselointi.md#kapselointi-ja-koheesio).
  Esimerkiksi osan 7-8 mallisovelluksessa ohjainluokka ei ikinä lisää
  `Tehtava`-oliota tehtäväkokoelman `tehtavat`-listaan itse, vaan tehtävän
  lisäys on tehtäväkokoelman vastuulla `lisaaTehtava`-metodin kautta.

  Älä kuitenkaan jää miettimään luokkien toimintaa liian kauan; kaikkia
  tapauksia ei voi vaan ennustaa. Voit tehdä apumetodeja lisää myöhemmin, kun
  toteutat ohjainluokkia.
- Voit testata tietomallin luokkien välistä yhteistoimintaa kokeilemalla käyttää
  tietomallin luokkia vaikkapa ohjelman `main`-pääohjelmassa.
  Et tarvitse tähän vielä käyttöliittymää, vaan voit luoda ja käyttää olioita
  suoraan pääohjelmassa.
  Varmista, että pystyt tietomallin luokkien ja niiden metodien avulla
  tekemään sovelluksen ja harjoitustyön vaatimusten kannalta olennaisimmat
  toiminnot, kuten tiedon lisäyksen, hakemisen, muokkauksen ja poiston.
  Debuggerin avulla voit varmistaa, että tietomallin tila on oikea.

  Halutessasi voit jopa kirjoittaa yksikkötestejä, jossa testaat tietomallin
  perustoiminnallisuuksia. Voit ottaa mallia [osan
  8.5](../osa8/05-yksikkotestaus.md#todo-ohjelman-testaaminen) ohjeesta, jossa
  Todo-sovelluksen tietomallin metodeja ja niiden toimivuutta testattiin.
- Sinun ei tarvitse vielä miettiä tallentamista tai lataamista tässä
  vaiheessa.

Kun sinulla on alustava versio tietomallista toteutettuna Javassa eikä koodi
sisällä virheitä, on hyvä hetki tallentaa muutokset Gitiin. Tee muutoksista uusi
commit (`git add` + `git commit`) ja puske ne etävarastoon talteen (`git push`).

## Käyttöliittymän alustava suunnitelma

Kun sinulla on käsitys sovelluksen tietomallista ja vaatimuksista, on hyvä hetki
alkaa pohtia käyttöliittymän alustavaa asettelua ja toimintaa.

Tee omaan projektiin uusi kansio `suunnitelma` (IDEA: klikkaa projektiselaimessa
projektin nimestä hiiren toissijaisella painikkeella ja valitse **New** <i
class="bi bi-chevron-right"></i> **Directory**). Tee uuteen kansioon samalla
Markdown-tiedosto nimeltään `kayttoliittyma.md`.
Kirjaa tiedostoon ylös alustavia tietoja sovelluksen käyttöliittymän
tarvittavista näkymistä.

<details>
<summary>Voit käyttää seuraavaa mallirunkoa käyttöliittymän suunnitelmatiedostolle</summary>

```md
# Käyttöliittymän suunnitelma

## Näkymä 1

![Näkymän karkea ulkoasu kuvana (wireframe.cc, DrawIO, Paint tai paperilla piirretty)](nakyma1.jpg)

**Olennaiset toiminnot**

- Mitä käyttäjä näkee käyttöliittymässä
- Miten tähän näkymään pääsee 
  (sovelluksen avaus, painikkeen klikkaus, jne.)
- Mitä käyttäjä voi tehdä käyttöliittymässä: 
  mitä voi klikata, mitä jokainen painike tekee

**Olennaiset komponentit**

- Mitä JavaFX-komponentteja saatat tarvita käyttöliittymän toteuttamiseen
- Tämä on pääosin paikka, johon voit kirjata linkkejä JavaFX-luokkiin 
  ja kirjastoihin, jotta niitä on helpompaa löytää käyttösuunnitelmaa tehtäessä
- Tämä osa ei ole pakollinen, vaan tarkoitettu helpottamaan dokumentaation hakemista myöhemmin

## Näkymä 2

![Näkymän karkea ulkoasu kuvana (wireframe.cc, DrawIO, Paint tai paperilla piirretty)](nakyma2.jpg)

**Olennaiset toiminnot**

- Mitä käyttäjä näkee käyttöliittymässä
- Miten tähän näkymään pääsee 
  (sovelluksen avaus, painikkeen klikkaus, jne.)
- Mitä käyttäjä voi tehdä käyttöliittymässä: 
  mitä voi klikata, mitä jokainen painike tekee

**Olennaiset komponentit**

- Mitä JavaFX-komponentteja saatat tarvita käyttöliittymän toteuttamiseen
- Tämä on pääosin paikka, johon voit kirjata linkkejä JavaFX-luokkiin 
  ja kirjastoihin, jotta niitä on helpompaa löytää käyttösuunnitelmaa tehtäessä
- Tämä osa ei ole pakollinen, vaan tarkoitettu helpottamaan dokumentaation hakemista myöhemmin
```

</details>

Piirrä alustavat karkeat kuvat jokaisesta näkymästä. Voit piirtää näkymät
käyttäen esimerkiksi verkossa olevia kaaviosovelluksia, kuten
[wireframe.cc](https://wireframe.cc/), [DrawIO](https://app.diagrams.net)
tai [Figma](https://www.figma.com/).
Voit piirtää karkeat kuvat myös piirtosovelluksella tai vaikkapa
piirtämällä kuvat paperille ja skannaamalla ne.
Pääasia on, että tässä vaiheessa käyttöliittymän tarkan ulkoasun ei tarvitse
olla mietitty loppuun, vaan keskityt ensisijaisesti eri komponenttien väliseen
karkeaan asetteluun. 

Voit halutessasi tehdä näkymät heti valmiiksi SceneBuilderilla. Siinä
tapauksessa ota näkymistä kuvakaappaus. 
Älä kuitenkaan käytä liikaa aikaa näkymien tekemiseen tässä vaiheessa;
suunnitelman tarkoituksena on saada karkea idea käyttöliittymän näkymistä.

Tallenna kuvat `suunnitelma`-kansioon ja mainitse ne
`kayttoliittyma.md`-tiedostoon. Löydät ohjeita kuvien upottamiseen
Markdown-tiedostoihin
[verkosta](https://www.markdownguide.org/basic-syntax/#images-1).

Kuvaa suunnitelmassa, mitä näkymässä näytetään ja millä eri tavoin käyttäjä voi
vuorovaikuttaa käyttöliittymän kanssa. 
Näin voit varmistaa jo tässä vaiheessa, että muistat ottaa huomioon kaikki 
vaaditut tietomallin lisäys-, luku-, muokkaus- ja poistotoiminnot.

Kun käyttöliittymän näkymien suunnitelma on valmis, tee muutoksista commit ja
puske muutokset etävarastoon.


<task>
  <task-title>Tehtävä 9.3: Käyttöliittymäsuunnitelma. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/9-3-ht-3/handout.md}}

</handout>
    <task-link><a
    href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa9/tehtava3">Tee
    tehtävä TIMissä</a></task-link>
</task>