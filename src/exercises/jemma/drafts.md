## Monty Hall
- Tehtävänäsi on Monty hallin ongelman simulointi neljällä ovella. Jos ongelma ei ole tuttu, 

Monty hallin ongelma neljällä ovella:
Kilpailijalla on edessään neljä ovea. Yhden oven takana on palkinto ja muiden ovien takana ei ole mitään. Kilpailija valitsee yhden ovista, jonka jälkeen juontaja paljastaa yhden ovista, jonka takana ei ole mitään. Kannattaako kilpailijan vaihtaa ovea suljettuun oveen, vai pitäytyä alkuperäisessä valinnassa?

Tehtävänäsi on simuloida molemmat vaihtoehdot:
1. Kilpailija pitäytyy alkuperäisessä valinnassaan
2. Kilpailija vaihtaa johonkin jäljellä olevista ovista, jotka eivät ole vielä auki ja joka ei ollut kilpailijan ensimmäinen valinta

ja valita vaihtoehdoista se, jolla voittaa todennäköisimmiten.

## Komentorivipohjainen visa

(Pitä luoda kysymykset, oikeat vastaukset, tarkistaminen ja pisteytys)

## Matriisin spiraalitulostus
Tulosta matriisissa olevat luvut spiraalimaisesti aloittaen vasemmasta
yläkulmasta ja edeten kohti keskustaa. Esimerkiksi 
[
    [1 2 3] 
    [4 5 6]
    [7 8 9]
    ]
palauttaa 123698745

## Pätevät sullkeet
Pätevät sulkeet, eli tarkasta suljetaanko kaikki avatut sulut { --> false {} --> true, ({}) --> true jne.

## Vakioaikainen haku
- Vakioaikainen haku taulukosta. Esimerkiksi, että kuinka monta päivää on kuukaudessa?

(Teoriatausta se, että laskennallista nopeutta voidaan lisätä käyttämällä enemmän muistia. Tähän esimerkiksi HashMap perustuu)

## Käänteinen linkitetty lista?
- Linkitetty lista käänteiseksi?

## Matriisin pyöräytys 90-astetta
Esimerkkinä vaikkapa kuvan käsittely.

Voisiko olla viikolla 7?

- Neliömatriisin eli n x n, n $\in \mathbb{N}$ matriisin pyöräyttäminen 90-astetta. 
- In ([[1,2],[3,4]], oikealle) --> [[3,1],[4,2]]

## Sanakirjahyökkäys
TODO: Tehtävä muotoiltava niin, että opiskelija oikeasti ymmärtää mitä
pyydetään. 

salasana = TunnettuSalasana

while(true) {
    i = 0
    j = i
    for (i...)
      for (j...)
         generoitu = lista[i] + lista[j]
         if ... return
}

Pieni taulukko sanoja

kissa
koira
pertti
omena
ohjelmointi

Valitse oma salasana näistä kahdesta.

Omistamasi ulkoisen kovalevyn salasana on päässyt unohtumaan. Muistat, että
salasana koostuu kahdesta
[tästä](https://raw.githubusercontent.com/rajuruoho/nykysuomensanalista/main/src/nykysuomensanalista2024.txt)
listasta valitusta yhteenliitetystä sanasta ilman välimerkkejä. Muodosta funktio
`salasana`, joka ottaa parametrina listan merkkijonoja ja joka palauttaa
salasanan `String` -tyyppisenä.
