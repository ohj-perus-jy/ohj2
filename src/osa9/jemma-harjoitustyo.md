# Harjoitustyö

Tällä viikolla aloitetaan oman harjoitustyön toteutus. Harjoitustyö toteutetaan
vaiheittain osissa 9-12, ja viimeistään osan 12 loppuun mennessä harjoitustyö
tulee palauttaa ja hyväksyttää tuntiopettajalla etä- tai lähiohjauksessa. 

Harjoitustyösi tulee täyttää kaikki [harjoitustyölle asetetut
vaatimukset](../harjoitustyo.md). Lue huolellisesti harjoitustyön vaatimukset
ennen aloittamista. 

Osissa 9-12 on annettu ohjeita, joiden tarkoituksena on auttaa sinua etenemään
harjoitustyössä, mutta harjoitustyötä ei ole pakko toteuttaa näissä osissa
kuvattua vaiheustusta hyödyntäen. 





## Tehtävät

1. Suunnitelma

Kerro minkä aiheen valitset. Jos valitset oman aiheen, se tulee hyväksyttää
tuntiopettajalla. Teet samanlaisen vaatimusmäärittelyn kuin yllä, mutta
sovelluksesi tarpeisiin sopivaksi.

Kaikki tekevät: 

 - Käyttöliittymän suunnitelma wireframe.cc:llä, paintilla tai käsin piirrettynä.
 - Suunnitelmassa tulee kuvata:
   - mitä käyttäjä näkee näkymissä (päänäkymä, muokkausnäkymä, tms.)
   - mitä käyttäjä voi tehdä näkymissä
   - millä komponenteilla tärkeimmät toiminnot on tarkoitus toteuttaa

Jos teet oman aiheen: 

 - Mitä varten sovellus on
 - Toiminnot, mitä käyttäjä voi tehdä
 - Sovelluksen tietomalli

1. Tee JavaFX-projekti. 

2. Tee Git-varasto. Lisää projektiin .gitignore ja README.md. README voi
   toistaiseksi olla tyhjä tai sisältää vain projektisi nimen. Lähetä
   Git-varasto GitLabiin tai GitHubiin. Palauta TIMiin
   etävaraston URL-osoite. 

3. Toteuta tietomalli sovellukseen. Olennaisimmat attribuutit ja metodit tulee
   olla toteutettuina, mutta ei tarvitse vielä olla täydellisiä. Toimintoja ei
   tarvitse vielä toteuttaa; ei esim. tarvitse vielä tallentaa tiedostoon eikä
   lukea sovelluksessa.
   
<details><summary>Jos ehdit, aloita jo validointia ja aloita yksikkötestaus</summary>

Seuraavat asiat tehdään joka tapauksessa osassa 10, mutta tee ne nyt jos ehdit. 

 * toteuta malliluokille yksinkertainen validointi (`String onkoValidi()`),
   joka estää ilmeisen virheellisen datan, kuten tyhjän nimen tai
   negatiivisen summan. Esimerkki tästä voisi olla malliolion metodi `String
   onkoValidi()`, joka palauttaa tyhjän merkkijonon jos olio on validi, ja
   virheilmoituksen muuten.      

   Esimerkiksi `Tehtava`-olion `onkoValidi()`-metodi voisi olla seuraava: 
   
   ```java,ignore
   public String onkoValidi() {
       if (this.nimi == null || this.nimi.isBlank()) {
           return "Nimi ei saa olla tyhjä";
       }
       return "";
   }
   ```
   
   Jos luokassa on useita tarkistettavia kenttiä, `onkoValidi()`-metodi voisi
   tarkistaa kaikki kentät ja palauttaa kaikki virheilmoitukset yhdessä
   merkkijonossa.      
   
 * toteuta yksikkötestit, joissa hyödynnät `onkoValidi()`-metodia. 

</details>

5. Kokeile `Main`-luokassa, että malliluokkasi toimivat odotetulla tavalla.
   Olioita täytyy pystyä luomaan, poistamaan, muokkaamaan ja hakemaan --
   riippuen siitä, mitä sovelluksessasi on tarkoitus tehdä. Voit tehdä tästä
   aliohjelman, jota kutsut pääohjelmassa. Bonus: Kirjoita yksikkötestejä
   malliluokillesi.
