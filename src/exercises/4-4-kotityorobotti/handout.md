Tee `Robotti`, joka osaa suorittaa erilaisia kotitöitä, kuten imurointia ja
kukkien kastelua. 

Toteuta tehtävä oheisen UML-kaavion mukaisesti. Katkoviiva, jossa on avoin
nuolenkärki, tarkoittaa, että `Robotti`-luokka käyttää `Kayttoesine`-rajapintaa:
`Robotti`-luokka sisältää attribuutin, joka on tyyppiä `Kayttoesine`.

```mermaid
classDiagram
class Robotti {
    -Kayttoesine kayttoesine
    +Robotti()
    +vaihdaKayttoEsine(uusiEsine: Kayttoesine) void
    +teeTyota(kohde: String) void
}

class Kayttoesine {
    <<interface>>
    +kayta(kohde: String) boolean
}

class Imuri {
    -int roskanMaara
    -int KAPASITEETTI = 100
    +Imuri()
    +kayta(kohde: String) boolean
    +tyhjennaSailio() void
}

class Kastelukannu {
    -int vedenMaara
    -List~String~ kielletytKohteet
    +Kastelukannu()
    +kayta(kohde: String) boolean
    +taytaVesi() void
}

Robotti ..> Kayttoesine
Kayttoesine <|.. Imuri
Kayttoesine <|.. Kastelukannu
```

<details><summary>Kuvaus sanallisessa muodossa</summary>

Tässä on kuvaus luokista ja niiden vaadituista ominaisuuksista (vastaavat kuin UML-kaaviossa):

Robotilla on seuraavat metodit:

 * `void vaihdaKayttoesine(Kayttoesine esine)`: Vaihtaa robotin käyttämän esineen
   (esim. imuri tai kastelukannu).
 * `void teeTyota(String kohde)`: Suorittaa kotityön. Jos `kohde` on
   sillä listalla, jotka kyseiseltä käyttöesineeltä on kielletty (esim.
   `Kastelukannu`-oliolla ei saa kastella `"Tietokone"`-kohdetta), robotin tulee
   tulostaa virheilmoitus. Kielletyt käyttökohteet määritellään käyttöesineen
   attribuuttina merkkijonolistana. 
 * `Kastelukannu`-olio ei kastele jos vettä ei ole riittävästi. Sen voi täyttää
   `taytaVesi()`-metodilla. Kastelukannun vesimäärä on aluksi 50 yksikköä. Voit
   halutessasi tehdä uuden muodostajan, joka asettaa vesimäärän alkutilan
   toiseksi.
 * `Imuri`-olio ei imuroi jos roskasäiliö on täynnä. Sen voi tyhjentää
   `tyhjennaSailio()`-metodilla. Roskasäiliön kapasiteetti on 100 yksikköä. Voit
   halutessasi tehdä uuden muodostajan, joka asettaa roskasäiliön alkutilan
   toiseksi. 
 * Molemmat käyttöesineet palauttavat `kayta(String kohde)`-metodin avulla
   totuusarvon, joka kertoo onnistuiko työ.

</details>