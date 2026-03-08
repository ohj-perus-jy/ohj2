# Harjoitustyö, vaihe 1

> [!VAROITUS]
> Tämä osa julkaistaan 9. maaliskuuta 2026.
> {{#include ../ei-julkaistu.md}}

Tässä osassa aloitetaan oman harjoitustyön toteutus. Harjoitustyö toteutetaan
vaiheittain osissa 9-12, ja viimeistään osan 12 loppuun mennessä harjoitustyö
tulee palauttaa ja hyväksyttää tuntiopettajalla etä- tai lähiohjauksessa. 

Harjoitustyösi tulee täyttää kaikki [harjoitustyölle asetetut
vaatimukset](../harjoitustyo.md). Lue huolellisesti harjoitustyön vaatimukset
ennen aloittamista. 

Osissa 9-12 on annettu ohjeita, joiden tarkoituksena on auttaa sinua etenemään
harjoitustyössä. Vastaavasti osat 9-12 sisältävät tehtävät, joiden tarkoitus on
auttaa projektin edistämistä vaiheittain.
Kuten aiemminkin, tehtävistä on palautettava vähintään 50 %.

Harjoitustyötä ei kuitenkaan ole pakko toteuttaa näissä osissa
kuvattua vaiheustusta hyödyntäen.

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
Suosittelemme, että käytetät kurssin valmista JavaFX-pohjaa, jonka käyttöä on
esitelty [osassa
7.1](../osa7/01-javafx-perusteet.md#ensimmäinen-javafx-sovellus).

Vinkkejä:

- Valitse projektin poluksi (*Location*-asetus) sellainen, jonka pystyt helposti
  löytämään sinun tietokoneelta. Harjoitustyölle on hyvä tehdä myös oma
  erillinen tyhjä kansio, jotta harjoitustyön tiedostot eivät mene sekaisin
  muiden tiedostojen kanssa.
- Aseta projektillesi yksilöllinen tunniste (GroupId). Esimerkiksi voit käyttää
  muotoa `fi.jyu.ohj2.nimesi.aihe`, jossa `nimesi` on yliopiston tunnuksesi ja
  `aihe` on harjoitustyön aihe. 
- Voit halutessasi alustaa Git-varaston jo projektin luomisen yhteydessä
  valitsemalla *Create Git repository* -valintaruutu päälle.
  Tämä asetus käytännössä tarkoittaa, että IDEA suorittaa automaattisesti `git
  init` projektikansion luomisen jälkeen. Voit myös luoda varaston aina
  itse [osan 7.3](../osa7/03-versionhallinta.md) ohjeiden mukaan.

Kun saat projektin luotua, kokeile ajaa se vielä kerran ja varmistaa, että saat
edes yksinkertaisen käyttöliittymän käynnistettyä.

## Git-varaston alustaminen

Kun projekti on luotu, luo saman tien projektikansioon Git-varasto [osan
7.3](../osa7/03-versionhallinta.md) ohjeiden mukaan.
Älä kuitenkaan tee vielä heti ensimmäistä committia, vaan valmistele kansion sisältö.

Git-versiohallintaa käytettäiviin projekteihin on tapana sisällyttää
`.gitignore`- ja `README.md`-tiedostoja.
`.gitignore`-tiedoston merkitystä on esitelty hieman [osassa
7.3](../osa7/03-versionhallinta.md): tiedostossa listattuja tiedostoja ja
kansioita ei sisällytetä ikinä committeihin.
Varmista täten, että projektikansiossasi on `.gitignore`-tiedosto. Jos käytät
kurssin valmista JavaFX-pohjaa, sellainen tiedosto on valmiiksi sisällytetty
projektiin. 

`README.md`, eli ns. "Read me" -tiedosto, on tarkoitettu projektin esittämiseen
ja kehittämisen kannalta oleellisiin ohjeisiin.
Etävarastopalvelut yleensä näyttävät `README`-tiedoston sisällön projektin
etusivulla, joten tiedosto on myös hyvä paikka kertoa projektista yleisesti
ei-tekniselle peruskäyttäjälle.
Voit luoda `README.md`-tiedoston suoraan IDEAssa klikkaamalla projektiselaimessa
projektista hiiren toissijaisella painikkeella, valitsemalla **New** <i
class="bi bi-chevron-right"></i> **File** ja antamalla tiedostn nimeksi
`README.md`:

<video src="images/intellij-readme-md.mp4" controls></video>

`README.md`-tiedosto on tapana kirjoittaa käyttäen
[Markdown-merkintäkielellä](https://www.markdownguide.org/basic-syntax/).

Tässä vaiheessa README-tiedosto voi olla aika alkeellinen. Lisää tiedostoon
ainakin projektin nimi ja lyhyt kuvaus parilla virkkeellä.
Jos käytät valmista aihetta, voit kopioida projektin aiheen kuvauksen [harjoitustyön
ohjeesta](../harjoitustyo.md#harjoitustyön-aihe).

Kun saat `README` ja `.gitignore` -tiedostoja tehtyä, tee ensimmäinen commit.
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



