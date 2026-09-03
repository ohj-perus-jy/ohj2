# Versionhallinta

> [!TÄRKEÄÄ]
> 
> Tämä luku olettaa, että olet käyttänyt Git-versiohallintaa aikaisemman.
> Jos et ole aiemmin käyttänyt Gitiä tai kaipaat kertausta, lue aluksi
> Ohjelmointi 1 -kurssin materiaalin
> [Git-osio](https://ohjelmointi1.it.jyu.fi/git.html). Emme tässä vaiheessa
> tarvitse vielä etävarastoa, joten voit ohittaa GitLab-etävarastoa käsittelevän
> kohdan. 
>
> Vastaavasti Git-komentorivityökalun käyttö olettaa, että sinulla on kokemusta 
> komentorivityökalujen käytöstä. Mikäli kaipaat kertausta, tutustu
> Ohjelmointi 1 -kurssin komentorivimateriaaliin:
>
> - [OpenCS: Johdatus komentorivin käyttöön](https://opencs.it.jyu.fi/cli-intro/)
> - [Ohjelmointi 1: Pikakurssi komentorivin käyttöön](https://tim.jyu.fi/view/kurssit/tie/itkp102/ohjeet/tyokalut#pikakurssi-komentorivin-k%C3%A4ytt%C3%B6%C3%B6n)

Tässä vaiheessa on hyvä hetki aloittaa versionhallinta. Käytämme
Git-versionhallintaa, joka on laajasti käytetty työkalu ohjelmistokehityksessä.
Tämän osan jälkeen teet jokaisesta tutoriaalin tehtävästä oman Git-commitin, joka kuvaa
tehtävän aikana tehtyjä muutoksia. 

Gitin käyttämiseen on monenlaisia käyttöliittymiä &ndash; myös IDEAssa on
omansa. Käytämme tässä kuitenkin komentoriviä, koska se on suhteellisen
yleinen tapa käyttää Gitiä kaikissa ympäristöissä samalla tavalla. 

Aloitetaan versionhallinta luomalla Git-varasto projektille. Avaa komentorivi
ja siirry projektisi juurikansioon. Juurikansio on se kansio, jossa on
`src`-kansio ja `pom.xml`-tiedosto. Alusta sen jälkeen Git-varasto komennolla
`git init`:

<asciinema src="images/git-init.cast" rows="4" poster="npt:10"></asciinema>

Saat ilmoituksen, että tyhjä Git-varasto on luotu. Projektin polku `polku/omaan/todo/projektiin`
on tietenkin erilainen omalla koneellasi.

Ennen kuin teemme ensimmäisen commitin, meidän on kerrottava Gitille, mitä
tiedostoja tulisi lisätä mukaan. Aivan alkuun riittää, että lisätään kaikki
kansiossa olevat tiedostot mukaan käyttäen `git add .` -komentoa:

<asciinema src="images/git-add.cast" rows="2" poster="npt:10"></asciinema>

Tämä lisää kaikki nykyisessä kansiossa ja sen alikansioissa olevat tiedostot
tulevaan commitiin. Huomaa, että komento ei itsessään tulosta mitään.

Varmistetaan vielä, mitä tiedostoja lähtee committiin mukaan käyttäen `git
status` -komentoa:

<asciinema src="images/git-status.cast" rows="19" poster="npt:10"></asciinema>


Saat listan tiedostoista, joita Git seuraa ja tulee lisäämään seuraavaan
commitiin. Tarkastellaan lyhyesti sisältö.
Alkuun on aiemmista vaiheista tutut `pom.xml`, `.java`-lähdekoodit ja
`.fxml`-näkymätiedosto.
Puolestaan `.idea`-kansio sisältää IntelliJ IDEA:n kannalta oleellisia asetuksia.

Lisäksi mukana on `.gitignore`-tiedosto. Tämä tiedosto tuli valmiiksi
projektipohjan mukana. Tiedosto kertoo
Git-työkalulle, 
mitä tiedostoja **ei** haluta koskaan lisätä mukaan commitiin. Näin
varmistetaan, että esimerkiksi käännetyt `.class`-tiedostot tai IDEAn omat
asetustiedostot eivät päädy versionhallintaan. `.gitignore`-tiedostoa voi ja
kannattaa muokata tarpeen mukaan, jos halutaan jättää pois muita
tiedostoja versionhallinnasta.

Nyt voimme tehdä ensimmäisen commitin, joka tallentaa kansiossa olevan koodin
tilan Gitiin ikään kuin "ruutukaappauksena". 
Commitin yhteydessä kirjoitetaan kuvaava viesti, joka
kertoo, mitä muutoksia on tehty. Yleensä ensimmäiselle commitille kirjoitetaan
viesti, kuten "Initial commit" tai "Projektin aloitus". 
Luo uusi commit komennolla `git commit`:

<asciinema src="images/git-commit.cast" rows="14" poster="npt:10"></asciinema>

Komento listaa onnistumisen merkiksi kaikki tiedostot, joista tallennettiin
senhetkinen tila Gitiin.

Tästä eteenpäin jokaisen tehtävän yhteydessä tee uusi commit, jossa kuvaat
tehtävän aikana tekemiäsi muutoksia. Voit halutessasi tehdä useammankin
commitin, jos haluat. 

<task>
  <task-title num="7.3">Todo-sovellus, vaihe 3.<points>1 p.</points></task-title>
  <handout>

{{#include ../exercises/7-3-todo-3/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa7/tehtava3">Tee tehtävä TIMissä</a></task-link>
</task>