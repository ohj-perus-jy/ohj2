Tee oheisen luokkakaavion mukainen luokkarakenne. Lisää `Ajoneuvo`-luokkaan
`renkaidenMaara`-ominaisuus, joka määritellään muodostajassa. Lisää
`Ajoneuvo`-luokkaan metodi `vaihdaRenkaat()`, joka tulostaa konsoliin tekstin
"Renkaat vaihdettu". Ylikirjoita tämä metodi `Auto`, `Polkupyora`, ja
`KuormaAuto`-luokissa siten, että ne tulostavat sopivan tekstin kyseiselle
ajoneuvolle, esimerkiksi

```
Skoda (Auto): renkaita 4 vaihdettu.
Trek (Polkupyora): renkaita 2 vaihdettu.
Scania (KuormaAuto): renkaita 18 vaihdettu.
```

Vinkki: Saat tyypin nimen selville metodilla `this.getClass().getSimpleName()`.

Tee sitten pääohjelma, jossa 
 1. luot jokaisen ajoneuvoluokan olion,
 2. lisäät ne `List<Ajoneuvo>`-kokoelmaan ja 
 3. kutsut kunkin olion `vaihdaRenkaat()`-metodia, jotta saat yllä olevan
    kaltaisen tulosteen aikaiseksi. 

Luokkarakenteen tulee olla seuraava:

```plantuml
@startuml```
hide empty members
skinparam class {
    RoundCorner        0
    BorderColor        #888888
    BackgroundColor    transparent
}
skinparam arrowColor   #888888

class Ajoneuvo {
    - renkaidenMaara: int
    - merkki: String
    + Ajoneuvo(renkaidenMaara: int, merkki: String)    
    + vaihdaRenkaat(): void
}

class Auto
class Polkupyora
class KuormaAuto

Ajoneuvo <|-- Auto
Ajoneuvo <|-- Polkupyora
Auto <|-- KuormaAuto
@enduml 
```