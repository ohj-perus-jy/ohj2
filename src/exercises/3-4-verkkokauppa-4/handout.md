Tulostimme aiemmissa tehtävissä olion tietoja luomalla omia metodeita, kuten `tulostaPuhelimenTiedot(int kuukausiaKulunut)`, joka ei kuitenkaan pidemmän päälle ole kovin järkevää. Olemme nyt tutustuneet `toString()` metodiin, joka on Javan standardin mukaista, jonka jälkeen esimerkiksi aiemmin luodun puhelimen tulostuksen voisi hoitaa näin: `IO.println(puhelin)`

Korvaa tai lisää luokkiin `Tuote`, `Elektroniikka` ja `Puhelin` metodi `toString()`, jossa kutsut ensimmäisenä yliluokan `toString()` metodia ja lisää merkkijonoon luokan omista attribuuteista tietoja.

Tehtäväsivulla on valmiiksi annettuna pääohjelma, jota voit käyttää luokkiesi
testaamiseen.

<details><summary>Avaa tästä, mitä ohjelma voisi esimerkiksi tulostaa.</summary>

```
Tietokone HighPower: 899.0 €
Takuuta laitteessa alunperin: 24 kk

Aifoun42: 888.0 €
Takuuta laitteessa alunperin: 37 kk
Käyttöjärjestelmä: AiOS
Yhteystyyppi: 5G

----------------------------

--- UUSI KAUPAN TUOTE ---
Light Bulb: 67000.0 €
Takuuta laitteessa alunperin: 73 kk
Akun kunto: 100.00
Toimintasäde: 404.00 km

--- KÄYTTÖÖNOTTO JA LATAUS ---
Ladataan autoa Light Bulb...
Ladataan autoa Light Bulb...
Ladataan autoa Light Bulb...
Ladataan autoa Light Bulb...
Ladataan autoa Light Bulb...

--- TILANNE LATAUSTEN JÄLKEEN ---
Light Bulb: 67000.0 €
Takuuta laitteessa alunperin: 73 kk
Akun kunto: 99.50
Toimintasäde: 401.98 km
```
</details>

<br />

Laajenna luokkahierarkiaa edelleen. Lisää `SahkoAuto`-luokka, joka perii
`Elektroniikka`-luokan. 

Lisää luokkaan 

 * attribuutit
     * vakio `TOIMINTASADE_MAX`, joka ilmaisee maksimietäisyyden kilometreinä, jonka
sähköauto voi kulkea yhdellä latauksella. 
     * `private double akunKunto` (prosentteina; väliltä 0-100)
 * metodit
     * `lataa()`, joka heikentää akun kuntoa 0.1%:lla jokaisella latauskerralla.
     * `toString()`, joka kutsuu ensin yliluokan metodia
       `toSTring()`, jonka jälkeen tulostaa akun kunnon prosentteina ja sitten
       toimintasäteen kilometreinä, jonka laskemiseen hyödynnetään kaavaa: (akunkunto / 100 * TOIMINTASADE_MAX).
--- 