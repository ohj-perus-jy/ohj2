Lisää `Auto`-luokalle vakio `TOIMINTASADE_MAX`, joka ilmaisee maksimietäisyyden kilometreinä, jonka auto voi kulkea yhdellä latauksella tai tankkauksella. Lisää `Auto`-luokkaan metodi `tankkaaKayttovoimaa()`, joka lisää ajoneuvolle käyttövoimaa (bensiiniä tai sähköä). 

Lisää sitten `Sahkoauto`-luokkaan attribuutti `akunKunto` (prosentteina; väliltä 0-100) sekä `toimintasade` (kilometreinä). Kun autoa ladataan, akun kunto heikkenee (ja siten toimintasäde) 0.1%:lla jokaisella latauskerralla. Niinpä `toimintasade` tulee laskea akun kunnon perusteella `akunKunto` / 100 * `TOIMINTASADE_MAX`.
