# Harjoitustyö, vaihe 1: osa 2

Tämä sivu kokoaa ne vaiheen 1 vaatimukset, jotka vastaavat suunnilleen osan 8
Todo-sovellusta. Tavoitteena on, että työ ei ole vain toimiva käyttöliittymä,
vaan myös rakenteeltaan järkevästi suunniteltu sovellus, jossa malli,
käyttöliittymä ja tallennus on erotettu toisistaan.

## Tietomalli ja käyttöliittymän kytkentä

- Sovelluksen dataa ei mallinneta käyttöliittymäkomponenteilla, vaan omilla
  malliluokilla.
- Sovelluksessa käytetään JavaFX:n havaittavia rakenteita silloin, kun ne
  liittyvät käyttöliittymän ja datan kytkemiseen. Käytännössä tämä tarkoittaa
  vähintään sitä, että keskeinen tietokokoelma on `ObservableList` tai vastaava
  havaittava rakenne.
- Datan esittämiseen käytetään tarkoituksenmukaista komponenttia. Jos työssä on
  useita samantyyppisiä olioita, `TableView` on yleensä luonteva ratkaisu.
- Käyttäjä voi valita yksittäisen olion käyttöliittymästä ja poistaa sen.

## Arkkitehtuuri ja vastuunjako

- Sovelluksen rakenteen tulee noudattaa vähintään karkeasti samaa ajatusta kuin
  malliharjoitustyössä: data, käyttöliittymä ja niitä yhteen kytkevä logiikka on
  erotettu toisistaan.
- Käyttöliittymäluokka tai kontrolleri ei saa sisältää kaikkea sovelluksen dataa
  ja tallennuslogiikkaa itsessään.
- Tiedon lataus ja tallennus on erotettu omaksi vastuukseen pois
  käyttöliittymälogiikasta.

## Muokkausnäkymä tai sen suunnitelma

- Sovelluksessa on oltava ajatus siitä, miten yksittäisen olion tarkempia tietoja
  voidaan muokata.
- Tämä voi olla erillinen näkymä, dialogi tai muu perusteltu ratkaisu.
- Osiin 7 ja 8 perustuvan malliharjoitustyön hengessä oliolla on hyvä olla
  vähintään yksi tai kaksi lisätietoa pelkän nimen tai otsikon lisäksi.
- Jos et vielä toteuta varsinaista muokkausnäkymää valmiiksi, suunnitelman tulee
  olla mukana palautuksessa.

## Komponenttien ja luokkien vastuut

- Palautuksessa on mukana lyhyt kuvaus komponenttien ja luokkien vastuista.
- Kuvauksesta tulee käydä ilmi ainakin:
  - mikä luokka tai luokat muodostavat sovelluksen mallin
  - mikä luokka vastaa käyttöliittymän ohjaamisesta
  - missä tiedon tallennus ja lataus hoidetaan
  - miten käyttöliittymä ja malli keskustelevat keskenään

## Testaus ja versionhallinta

- Sovelluksen keskeiselle mallille tai bisneslogiikalle on kirjoitettu ainakin
  joitakin yksikkötestejä.
- Työlle on tehty julkinen Git-etävarasto GitLabiin tai GitHubiin.

## Tavoitetaso

Jos oma sovelluksesi on tässä vaiheessa suunnilleen samalla tasolla kuin osien
7 ja 8 Todo-sovellus ilman bonuksia, olet oikealla tasolla. Vaiheen 1 lopussa
työssäsi pitäisi näkyä sekä toimiva perussovellus että uskottava rakenne sen
jatkokehitykselle.
