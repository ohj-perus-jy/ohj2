Tee `Robotti`, joka osaa suorittaa erilaisia kotitöitä, kuten imurointia ja
kukkien kastelua. 

Toteuta tehtävä oheisen UML-kaavion mukaisesti. Katkoviiva, jossa on musta
nuoli, tarkoittaa, että `Robotti`-luokka käyttää `KayttoEsine`-rajapintaa:
`Robotti`-luokka sisältää attribuutin, joka on tyyppiä `KayttoEsine`.

```plantuml
@startuml
class Robotti {
    -KayttoEsine kayttoEsine
    +Robotti()
    +void vaihdaKayttoEsine(KayttoEsine esine)
    +void teeTyota(String kohde)
}

interface KayttoEsine {
    +boolean kayta(String kohde)
}

class Imuri {
    -roskanMaara : int
    -KAPASITEETTI : int = 100
    +Imuri()
    +boolean kayta(String kohde)
    +void tyhjennaSailio()
}

class KasteluKannu {
    -vedenMaara : int
    -kielletytKohteet : List<String>
    +KasteluKannu()
    +boolean kayta(String kohde)
    +void taytaVesi()
}

Robotti ..> KayttoEsine
Imuri ..|> KayttoEsine
KasteluKannu ..|> KayttoEsine
@enduml
```

<details><summary>Kuvaus sanallisessa muodossa</summary>

Tässä on kuvaus luokista ja niiden vaadituista ominaisuuksista (vastaavat kuin UML-kaaviossa):

Robotilla on seuraavat metodit:

 * `void vaihdaKayttoEsine(KayttoEsine esine)`: Vaihtaa robotin käyttämän esineen
   (esim. imuri tai kastelukannu).
 * `void teeTyota(String kohde)`: Suorittaa kotityön. Jos `kohde` on
   sillä listalla, jotka kyseiseltä käyttöesineeltä on kielletty (esim.
   `KasteluKannu`-oliolla ei saa kastella `"Tietokone"`-kohdetta), robotin tulee
   tulostaa virheilmoitus. Kielletyt käyttökohteet määritellään käyttöesineen
   attribuuttina merkkijonolistana. 

</details>