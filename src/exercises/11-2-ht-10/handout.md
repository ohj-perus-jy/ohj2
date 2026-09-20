Toteuta tiedon poistaminen. Poistamisessa tulee huomioida ja käsitellä myös muut
mahdolliset oliot, jotka viittaavat poistettuun olioon. Esimerkiksi, jos poistat
Kategoria-olion
[Kulujenseuranta-sovelluksessa](https://ohjelmointi2.it.jyu.fi/harjoitustyo/#aihe),
pitää poistaa (asettaa null-arvioon tai Optional.empty()-arvoon) kategoria
kaikilta niiltä Tapahtuma-olioilta, jotka siihen viittaavat. Poistamisessa on
myös hyvä olla varmistusdialogi esimerkiksi [Alert-luokan
avulla](https://code.makery.ch/blog/javafx-dialogs-official/), jotta vahingossa
tapahtuneet klikkaukset eivät tuhoa dataa.
