# TIEP111 Ohjelmointi 2

Tämä on Jyväskylän yliopiston järjestämän **TIEP111 Ohjelmointi 2**
-opintojakson oppimateriaali. 

Voit palauttaa tehtäviä vain, jos olet ilmoittautunut opintojaksolle Sisu- tai
Ilpo-järjestelmässä. Oman etenemisesi tilanteen (harjoitustehtävien pisteet,
harjoitustyön hyväksyminen, tenttitulokset) näet
[TIM-järjestelmästä](https://tim.jyu.fi/view/kurssit/tie/tiep111/koti).

## Tietoja opintojaksosta

<!-- OPS:sta -->
<!-- Sisältö: Java-kieli, ohjelmansuunnittelun ja olio-ohjelmoinnin periaatteita, ohjelman testaaminen. Rekursio. -->
<!-- Oppia ymmärtämään oliopohjaisen ohjelmoinnin perusteet. Kyky tuottaa pieniä/keskikokoisia oliopohjaisia ohjelmia. Samoin tavoitteena on "testaus ensin" (TDD) ajatuksen sisäistäminen. Kyky suunnitella ja toteuttaa graafinen käyttöliittymä. -->

Opintojaksolla opit

 - oliopohjaisen ohjelmoinnin perusteita ja periaatteita,
 - tuottamaan pieniä ja keskisuuria oliopohjaisia ohjelmia,
 - graafisen käyttöliittymän suunnittelua ja kehittämistä,
 - ohjelman testaamista,
 - erilaisia ohjelmoijan työkaluja ja tekniikoita.

Tarkemmat tiedot löydät opintojakson
[Sisu-esitteestä](https://sisu.jyu.fi/student/courseunit/otm-4bc61fed-4013-4982-9158-48a4a198a4f2/brochure). 

## Uutiset

<details><summary>Kesän 2026 toteutus, DL-BONUS-takarajat</summary>

Kesätoteutus alkaa 1.6.2026. Ilmoittaudu Sisussa. 

DL-BONUS-pisteiden takarajat ovat seuraavat:

 * Osa 1: ma 8.6.2026 klo 11:59 (keskipäivä)
 * Osa 2: ma 15.6.2026 klo 11:59 (keskipäivä)
 * Osa 3: ma 22.6.2026 klo 11:59 (keskipäivä)
 * Osa 4: ma 29.6.2026 klo 11:59 (keskipäivä)
 * Osa 5: ma 6.7.2026 klo 11:59 (keskipäivä)
 * Osa 6: ma 13.7.2026 klo 11:59 (keskipäivä)

Harjoitustyön palautuksen takaraja pe 14.8.2026

Aikataulu on hieman tiukempi kuin kevään 2026 toteutuksessa.

</details>

<details><summary>1. tammikuuta 2026: Kurssimateriaalia uudistetaan keväällä 2026</summary>

Teemme kokonaisvaltaisen uudistuksen oppimateriaaliin sekä tehtäviin kevään 2026
aikana. Osa materiaalista julkaistaan kurssin edetessä. Uudistamisesta johtuen
sisällössä voi olla myös keskeneräisyyksiä ja virheitä. Pahoittelemme tästä
mahdollisesti aiheutuvaa haittaa. Pyydämme, että ilmoitat virheistä tai
parannusehdotuksista GitHubin kautta (katso tämän sivun alareuna) tai suoraan
opettajien sähköpostiin <ohj2-opet@jyu.onmicrosoft.com>.

</details>

## Ohjaukset ja tuki

Aikavälillä 6.7.-31.7. ohjausta on saatavana seuraavasti (huomaa muuttuneet ajat!):

| Tukikanava                                           | Aika                      | Paikka/Linkki                                                                                                                   |
| ---------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Lähiohjaus | Vain ajanvarauksella toistaiseksi | Agoralla luokat [Ag B212.1 Finland](https://navi.jyu.fi/space/m118988) ja [Ag B211.1 Sovjet](https://navi.jyu.fi/space/m118987) |
| Etäohjaus  | Vain ajanvarauksella toistaiseksi | [Ohjelmointi 2 Teams-kanva](#teams)                                                                                            |
| Sähköposti | Rajoitetusti kesäaikana           | ohj2-opet@jyu.onmicrosoft.com                                                                                                   |

Lisäksi ohjausta annetaan ajanvarauksella: 

| Ohjaaja | Ajanvarauslinkki                                                                                                 |
| ------- | ---------------------------------------------------------------------------------------------------------------- |
| Tatu    | [Varaa aika](https://outlook.office.com/book/AjanvarausTatuKauhanen@bookings.jyu.fi/?ismsaljsauthenabled)        |
| Karri   | [Varaa aika](https://book.ms/b/ks@bookings.jyu.fi)                                                               |

[Tenttipäivinä](tentti.md) ei kuitenkaan pidetä ohjauksia. 

Ohjaukset ovat yhteisiä TIEP111 Ohjelmointi 2, ITKP102 Ohjelmointi 1- ja
ITKA2004 Tietokannat ja tiedonhallinta -opintojaksojen kanssa. Ohjaajat auttavat
kaikkien kolmen kurssin opiskelijoita.

Varaamme oikeuden ohjausajankohtien muuttamiseen.

<!--
Ajalla 1.6.-21.6. ohjausta on saatavana seuraavasti

| Tukikanava                                           | Aika                      | Paikka/Linkki                                                                                                                   |
| ---------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Lähiohjaus                                           | tiistaista torstaihin klo 15-17| Agoralla luokat [Ag B212.1 Finland](https://navi.jyu.fi/space/m118988) ja [Ag B211.1 Sovjet](https://navi.jyu.fi/space/m118987) |
| Etäohjaus                                            | tiistaista torstaihin klo 15-17 | [Ohjelmointi 2 Teams-kanva](#teams)                                                                                            |
| Sähköposti | Rajoitetusti kesäaikana      | ohj2-opet@jyu.onmicrosoft.com                                                                                                   |
-->

<!-- 

Ajalla 24.4.-31.5. ohjausta on saatavana vain ajanvarauksella.

| Ohjaaja | Ajanvarauslinkki                                                                                                 |
| ------- | ---------------------------------------------------------------------------------------------------------------- |
| Tatu    | [Varaa aika](https://outlook.office.com/book/AjanvarausTatuKauhanen@bookings.jyu.fi/?ismsaljsauthenabled)        |
| Santtu  | [Varaa aika](https://bookings.cloud.microsoft/book/OhjAjanvarausSanttuSalo@bookings.jyu.fi/?ismsaljsauthenabled) |
| Karri   | [Varaa aika](https://book.ms/b/ks@bookings.jyu.fi)                                                               |
-->

<!-- 

Kevään 2026 on 12. tammikuuta &ndash; 24. huhtikuuta välisenä aikana tarjolla
lähiohjausta Agoralla, etäohjausta Teamsin kautta, sekä sähköpostitukea. 

Pääsiäistauon aikana (30.3.-6.4.) ei kuitenkaan ole ohjausta tarjolla.

Sisu vaatii ilmoittautumisen yhteydessä valitsemaan ohjausryhmän. Voit kuitenkin
täysin vapaasti käyttää kaikkia ohjausaikoja ja -kanavia riippumatta siitä,
mihin ohjausryhmään olet ilmoittautunut. 

--> 

<!-- 

Ohjausajat 7.4. alkaen:

| Tukikanava                                           | Aika                      | Paikka/Linkki                                                                                                                   |
| ---------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Lähiohjaus                                           | ke 10-18, to 10-18, pe 8-14 | Agoralla luokat [Ag B212.1 Finland](https://navi.jyu.fi/space/m118988) ja [Ag B211.1 Sovjet](https://navi.jyu.fi/space/m118987) |
| Etäohjaus                                            | ke 10-18, to 10-18, pe 8-14 | [Ohjelmointi 2 Teams-kanava](#teams)                                                                                            |
| Vastuuopettajien ja tuntiopettajien sähköpostiosoite | Jatkuva                   | ohj2-opet@jyu.onmicrosoft.com                                                                                                   |

(Ke klo 8-10 ja to 8-10 pudotettu pois 30.3. alkaen.)

<!-- Ohjausajat 12.1. alkaen: 

| Tukikanava                                           | Aika                      | Paikka/Linkki                                                                                                                   |
| ---------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Lähiohjaus                                           | ke 8-18, to 8-18, pe 8-14 | Agoralla luokat [Ag B212.1 Finland](https://navi.jyu.fi/space/m118988) ja [Ag B211.1 Sovjet](https://navi.jyu.fi/space/m118987) |
| Etäohjaus                                            | ke 8-18, to 8-18, pe 8-14 | [Ohjelmointi 2 Teams-kanva](#teams)                                                                                            |
| Vastuuopettajien ja tuntiopettajien sähköpostiosoite | Jatkuva                   | ohj2-opet@jyu.onmicrosoft.com                                                                                                   |

-->

<!--
| Tukikanava                                           | Aika                        | Paikka/Linkki                           |
| ---------------------------------------------------- | --------------------------- | --------------------------------------- |
| Etäohjaus                                            | ke 10-16, to 8-18, pe 10-16 | [Ohjelmointi 2 Teams-kanava](#teams-jy) |
| Vastuuopettajien ja tuntiopettajien sähköpostiosoite | Jatkuva                     | ohj2-opet@jyu.onmicrosoft.com           |

Ohjaukset ovat yhteisiä TIEP111 Ohjelmointi 2, ITKP102 Ohjelmointi 1- ja
ITKA2004 Tietokannat ja tiedonhallinta -opintojaksojen kanssa. Ohjaajat auttavat
kaikkien kolmen kurssin opiskelijoita.

Ohjausaikoja saatetaan lisätä tai poistaa kysynnän mukaan; kerro aikatoiveistasi
opettajille sähköpostitse. 

24.4. jälkeen ohjausta on saatavilla ajanvarauksella. Linkki ajanvaraukseen
tulee myöhemmin saataville. 
--> 

<details closed><summary>Haluatko ohjausaikoja näkyviin Sisun opintokalenteriin? (Avaa ohje klikkaamalla) </summary>

1. Kirjaudu Sisuun
2. Jos olet jo ilmoittautunut kurssille, klikkaa ylhäällä välilehteä
   *Opintokalenteri* tai klikkaa sitä hampurilaisvalikosta
3. Selaa oikealla oikea kurssi näkyville, eli tässä tapauksessa Ohjelmointi 2
4. Klikkaa oikealla olevaa oikealle osoittavaa väkästä Ohjelmointi 2 -kurssin
   kohdalla
5. Skrollaa alaspäin, kunnes tulee alaotsikko *Pääteohjaus*
6. Jos ei vielä näy, niin skrollaa alaspäin, kunnes näkyy *Muiden ryhmien
   tiedot* ja klikkaa sitä
7. Nyt voit skrollaamalla alaspäin haluamiesi pääteohjauksien kohdalta klikata
   nappulaa *Näytä tapahtumat kalenterissa*. 

   ![Näytä Sisu-tapahtumat kalenterissa](images/tapahtumat.jpg)

8. Nyt kyseisen ryhmän ohjausajat näkyvät sinulla automaattisesti. Tarvittaessa
   voit poistaa ryhmän tapahtumia viikkokohtaisesti Tapahtumakalenterista. 

</details>

## Ohjeet etäohjaukseen liittymiseksi {#teams}

<details><summary>Teams-kanavalle liittyminen: Jyväskylän yliopiston tutkinto-opiskelijat</summary>

1. Kirjaudu yliopiston tunnuksellasi Microsoft Teamsiin osoitteessa
    <https://teams.microsoft.com>. Käyttäjätunnus on muotoa
    `käyttäjätunnus@jyu.fi` (esim. `mameikal@jyu.fi`). Tunnuksen muoto
    `student.jyu.fi` ei käy. Tunnuksen toimiminen vaatii, että olet hyväksynyt
    Office 365 -palvelut OMA-palvelussa (<https://sso.jyu.fi>).

 2. Lataa Teams-sovellus (suositus) tai käytä nettiversiota. Saatavilla on myös
    mobiilisovellus. Jos selaimella liittymisessä on ongelmia, tarkista ensin
    tukeeko Microsoft sitä
    [täältä](https://learn.microsoft.com/en-us/microsoftteams/teams-client-web#prerequisites).

 3. Teams-sovelluksessa klikkaa *Teams* <i class="bi bi-chevron-right"></i> *Join or create team* <i class="bi bi-chevron-right"></i>
    *Join a team with a code*

 4. Syötä koodi `2po6c57` 

 5. Testaa kaverin kanssa, että puhelu ja ruudun jakaminen toimii. Sinun tulee
tarvittaessa sallia oikeudet käyttöjärjestelmäsi asetuksista. 

</details>

<details><summary>Teams-kanavalle liittyminen: Jyväskylän yliopiston Avoin yliopisto sekä erilliset opinto-oikeudet</summary>

Lähetä sähköpostilla alla oleva pyyntö osoitteeseen `ohj2-opet@jyu.onmicrosoft.com`.

```plain
Hei,

opiskelen Ohjelmointi 2 -kurssilla ei-tutkintoon johtavassa koulutuksessa.
Pyydän liittämään minut opintojakson Teams-ryhmään vieraana. 
Teamsissa käyttämäni sähköpostiosoite on: [oma sähköposti tähän].

Terveisin, [oma nimi]
```

Liitämme sinut viimeistään seuraavana arkipäivänä.

</details>

<details><summary>Etäohjauksiin osallistuminen ilman Teamsia</summary>

Jos et millään onnistu kirjautumaan Teamsiin tai et halua olla Teams-kanavalla,
voit pyytää etäohjausta Zoomin kautta seuraavasti: 

 1. Asenna Zoom sovellus koneellesi osoitteesta <https://zoom.us/download> (muut
    kuin tutkinto-opiskelijat) tai <https://jyufi.zoom.us>
    (tutkinto-opiskelijat; Valitse Download Client ihan alhaalta)
 2. Kirjaudu Zoomiin valitsemallasi tilillä, esim. Google-kirjautumista käyttäen
    (muut kuin tutkinto-opiskelijat) tai Single Sign-on / SSO -toiminnolla
    (tutkinto-opiskelijat; käytä company domainia `jyufi`)
 3. Aloita kokous New meeting toiminnolla
 4. Testaa Audio <i class="bi bi-chevron-right"></i> Test speaker & mikrofone toiminnolla että äänet pelittää
 5. Ota kokouslinkki talteen Participants <i class="bi bi-chevron-right"></i> Copy invite link
 6. Avaa ohjauspyyntölomake:
    [https://forms.gle/5QULUPBHjjqS4ndf6](https://forms.gle/5QULUPBHjjqS4ndf6)
 7. Täytä omat tietosi ja HUOM Pasteta lisätietokenttään kohdassa 5 kopioimasi
    linkki
 8. Odota, että ohjaaja tulee huoneeseesi. Saatat joutua hyväksymään hänen
    sisäänpääsyn (riippuu kokoushuoneesi asetuksista)

</details>

## Navigointi tässä materiaalissa

Tässä muutama pikavinkki tässä materiaalissa navigoimiseen.

 * Sisällysluettelon saat auki ja kiinni sivupalkki-kuvakkeesta <i class="bi
   bi-layout-sidebar"></i>.
 * Voit selata materiaalia eteen- ja taaksepäin nuolikuvakkeista sivun
   vasemmassa ja oikeassa laidassa (tai ihan sivun alalaidassa, jos käytät
   mobiililaitetta) <i class="bi bi-arrow-left-circle"></i> <i class="bi
   bi-arrow-right-circle"></i>.
 * Hakutoiminnon saat auki suurennuslasista oikeasta yläreunasta tai painamalla
   S-kirjainta näppäimistöltä <i class="bi bi-search"></i>.


## Palaute ja kehittäminen

Olemme erittäin kiitollisia kaikesta palautteesta, joka auttaa meitä kehittämään
opintojaksoa edelleen! Voit antaa palautetta ja kehitysehdotuksia opintojaksosta
kolmella tavalla:

 1. Jyväskylän yliopiston **tutkinto-opiskelijat** voivat antaa jatkuvaa palautetta
    opintojakson aikana Norppa-järjestelmässä. 

 2. **Kaikki opiskelijat** voivat ilmoittaa havaitsemistaan virheistä,
    epäselvyyksistä, tai muista ongelmista tässä oppimateriaalissa. Raportoi
    havaintosi GitHubissa klikkaamalla kunkin sivun alareunassa olevia linkkejä.
    Voit myös ilmoittaa puutteista suoraan opettajille sähköpostitse
    osoitteeseen `ohj2-opet@jyu.onmicrosoft.com`.
 
 3. Opintojakson lopuksi kaikki **Sisussa** (tai **Ilpo-portaalissa**)
    ilmoittautuneet (tutkinto, avoin, erilliset opinto-oikeudet, lukiolinjat)
    saavat henkilökohtaisen linkin kurssipalautekyselyyn, jossa voit antaa
    anonyymisti palautetta koko opintojaksosta.

## Tekijät ja lisenssi

Ohjelmointi 2 oppimateriaali © 2025 by Denis Zhidkikh, Sami Sarsa, Antti-Jussi
Lakanen, Rauli Ruokokoski, Karri Sormunen. 

Kiitos Jonne Itkoselle palautteesta ja parannusehdotuksista.

Materiaali on julkaistu CC-BY-SA-4.0-lisenssillä. Tarkemmat tiedot löydät
[materiaalin GitHub-sivulta](https://github.com/ohj-perus-jy/ohj2).
