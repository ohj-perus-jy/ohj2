Laajenna aiemmin tekemääsi verkkokaupan luokkahierarkiaa alla olevan UML-kaavion
mukaisesti. Saat kuvan suuremmaksi oikeaklikkaamalla (Windows) tai
Control-klikkaamalla (macOS) sitä ja valitsemalla "Avaa kuva uudessa
välilehdessä".

Tehtäväsivulla on valmiiksi annettuna pääohjelma, jota voit käyttää luokkiesi
testaamiseen. 

<details><summary>Avaa tästä ohjelman antama esimerkkituloste.</summary>

```
Kutsutaan perittyjä metodeja:
--- TUOTETIEDOT: Talvitakki Dulce & Käppänä ---
Hinta: 120.0 euroa
--- TUOTETIEDOT: Ruisleipä Reissurähjä ---
Hinta: 2.5 euroa
--- TUOTETIEDOT: HighPower ---
Hinta: 899.0 euroa

----------------------------

Kutsutaan omia metodeja:
Testi 1: Sovitetaan M-kokoista käyttäjää:
Sovitetaan vaatetta Talvitakki Dulce & Käppänä...
Voi ei. Sinä olet kokoa M, mutta tämä vaate on L.

Testi 2: Sovitetaan L-kokoista käyttäjää:
Sovitetaan vaatetta Talvitakki Dulce & Käppänä...
Mahtavaa! Koko L istuu sinulle täydellisesti.

Syödään Ruisleipä Reissurähjä.
Parasta ennen oli 20.12.2024, toivottavasti on hyvää.

Käynnistetään laite HighPower...
Virta päällä! Takuuta on jäljellä 24 kk.
--- TUOTETIEDOT: pHone ---
Hinta: 999.99 euroa
Käynnistetään laite pHone...
Virta päällä! Takuuta on jäljellä 24 kk.
Soitetaan numeroon 0401122330 (Orange 4G)
--- TUOTETIEDOT: Hernepussi ---
Hinta: 0.99 euroa
Sulatit pakastetta Hernepussi 10 minuuttia. Säilytyssuositus on -18 astetta C.
Syödään Hernepussi.
Parasta ennen oli 31.5.2026, toivottavasti on hyvää.
```
</details>

<br />

<details><summary>Tehtävän kuvaus sanallisessa muodossa</summary>

Tässä on kuvaus luokista ja niiden vaadituista ominaisuuksista (vastaavat kuin UML-kaaviossa):

 1. `Puhelin` (perii `Elektroniikka`)
    * Lisää attribuutit:
        * `private String kayttojarjestelma` (esim. "Android" tai "iOS")
        * `private boolean onko5G`
    * Lisää metodit:
        * `public void soita(String numero)`. Metodi tulostaa esimerkiksi:
          `Soitetaan numeroon 0401234567 (Appleroid, 4G)`
        * `public void tulostaPuhelimenTiedot()`. Metodin tulee kutsua ensin
          perittyä metodia (`tulostaPerustiedot();`), ja sitten tulostaa
          puhelimeen liittyvät lisätiedot (takuu, käyttöjärjestelmä ja 5G-tuki).

 2. `Pakaste` (perii `Ruoka`)
    * Lisää attribuutti:
        * `private int lampotilaSuositus` (esim. -18)
    * Lisää metodi:
        * `private void sulata(int minuutit)` (huomaa private-määre)
        * Kun metodia kutsutaan, se tulostaa esimerkiksi: `Sulatat pakastetta 10
          minuuttia. Säilytyssuositus: -18 C.`
    * Lisää metodi:
        * `public void sulataJaNauti(int minuutit)`
        * Metodi kutsuu ensin `sulata(minuutit)`-metodia ja sitten perittyä
          `syo()`-metodia.
</details>

<br />

```plantuml
@startuml
class Tuote {
    -String nimi
    -double hinta
    +Tuote(String nimi, double hinta)
    +void tulostaPerustiedot()
}
class Elektroniikka {
    -int takuuKuukaudet
    +Elektroniikka(String nimi, double hinta, int takuuKuukaudet)
    +void testaaLaite()
}
class Ruoka {
    -String parastaEnnen
    +Ruoka(String nimi, double hinta, String parastaEnnen)
    +void syo()
}
class Puhelin {
    -String kayttojarjestelma
    -boolean onko5G
    +Puhelin(String nimi, double hinta, int takuuKuukaudet, String kayttojarjestelma, boolean onko5G)
    +void soita(String numero)
    +void tulostaPerustiedot()
}
class Pakaste {
    -int lampotilaSuositus
    +Pakaste(String nimi, double hinta, String parastaEnnen, int lampotilaSuositus)
    -void sulata(int minuutit)
    +void sulataJaNauti(int minuutit)
}
Tuote <|-- Elektroniikka
Tuote <|-- Ruoka
Elektroniikka <|-- Puhelin
Ruoka <|-- Pakaste
@enduml
```
