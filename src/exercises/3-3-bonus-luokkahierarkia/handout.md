Laajenna luokkahierarkiaa edelleen. Lisää `SahkoAuto`-luokka, joka perii
`Tuote`-luokan. 

Lisää luokkaan 

 * attribuutit
     * vakio `TOIMINTASADE_MAX`, joka ilmaisee maksimietäisyyden kilometreinä, jonka
sähköauto voi kulkea yhdellä latauksella. 
     * `private double akunKunto` (prosentteina; väliltä 0-100)
 * metodit
     * `lataa()`, joka heikentää akun kuntoa 0.1%:lla jokaisella latauskerralla.
     * `tulostaAutonTiedot()`, joka tulostaa ensin tuotteen perustiedot (kutsu
       yliluokan metodia), ja sitten laskee ja tulostaa akun kunnon ja sen
       perusteella toimintasäteen.

