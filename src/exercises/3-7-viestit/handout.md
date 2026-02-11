Tee abstrakti luokka `Viesti`, jolla on attribuutti `String viesti`, joka
asetetaan konstruktorissa. Aseta `viesti`-attribuutin näkyvyys mahdollisimman
rajoitetuksi. Luokalla on myös abstrakti metodi `void laheta()`.

Peri `Viesti`-luokasta luokat `Sahkoposti` ja `Tekstiviesti`. Molemmissa luokissa on
konstruktori, joka kutsuu yliluokan konstruktoria. Toteuta molempiin luokkiin
`laheta()`-metodit. `Sahkoposti`-luokan `laheta()`-metodi tulostaa muodossa
"Lähetetään sähköposti: \<viesti\>" ja `Tekstiviesti`-luokan `laheta()`-metodi
tulostaa muodossa `"Lähetetään tekstiviesti: \<viesti\>"