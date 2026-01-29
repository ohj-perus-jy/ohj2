1. Tee abstrakti luokka `Viestikanava`. Sillä on attribuutti `String
vastaanottaja`, joka asetetaan konstruktorissa. Lisää abstrakti metodi
`lahetaSisaisesti(String viesti)`, joka ei palauta mitään. 

2. Tee myös metodi
`String getVastaanottaja()`, joka palauttaa vastaanottajan.

3. Tee konkreettinen metodi `laheta(String viesti)`, joka aluksi lopettaa metodin
(`return`), jos viesti on tyhjä tai `null`. Muuten metodi kutsuu abstraktia
metodia `lahetaSisaisesti(String viesti)`.

4. Peri `Viestikanava`-luokasta `Sahkoposti` ja `Tekstiviesti`. Molemmissa
luokissa ylikirjoita abstrakti metodi `lahetaSisaisesti(String viesti)`, joka
tulostaa konsoliin viestin muodossa "Lähetetään \<kanava\> \<osoite/numero\>:
\<viesti\>", esim. "Lähetetään sähköposti osoitteeseen antti-jussi@lakanen.com: Hei,
mikä on homma?" tai "Lähetetään tekstiviesti numeroon 0401234567: Tervetuloa
kurssille!".