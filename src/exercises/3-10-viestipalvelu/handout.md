Tee `Viestipalvelu`-luokka, jolle voi lisätä erilaisia `Viestikanava`-olioita
`lisaaKanava(Viestikanava kanava)`-metodilla. Lisää myös metodi
`lahetaKaikille(String viesti)`, joka lähettää viestejä kaikilla kanavilla
kerralla.

Pari valinnaista lisähaastetta (ei pisteitä; nämä ovat kuitenkin
mallivastauksessa mukana):
 
 1. Muuta `Viestikanava`-luokkaa siten, että se ottaa listan vastaanottajia, ei
   vain yhtä. Tämän seurauksena pitää muuttaa myös `lahetaSisaisesti`-metodeja.
 2. Laita `Tekstiviesti`-luokkaan merkkiraja (esim. 80 merkkiä). Jos viesti on tätä
   pidempi, niin viesti tulee pilkkoa merkkirajan mukaisiin pätkiin. 
