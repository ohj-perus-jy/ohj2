Vakoojat lähettävät viestejä toisilleen, mutta salausmenetelmä vaihtuu päivittäin, jotta vihollinen ei pääse perille logiikasta. Tarvitsemme rajapinnan, jonka avulla voimme vaihtaa salausalgoritmia lennosta.

1. Luo rajapinta `Salaaja`. Määrittele rajapintaan kaksi metodia

```java,ignore
String salaa(String viesti);
String pura(String salattuViesti);
```

2. Toteuta kolme erilaista luokkaa: `Kaantaja`, `Hakkeri` ja `SeuraavaKirjain`, jotka toteuttavat `Salaaja`-rajapinnan seuraavilla logiikoilla:

  * `Kaantaja` (Peilikuvakirjoitus). Logiikka: Kääntää sanan väärinpäin. Esimerkki: "Agentti" &rarr; "ittnegA". Vihje: Voit käyttää `StringBuilder`-luokan `reverse()`-komentoa tai silmukkaa, joka käy sanan läpi lopusta alkuun.

  * `Hakkeri` ("Leet-speak"). Logiikka: Korvaa tietyt kirjaimet numeroilla tai merkeillä. Esimerkki: "Agentti" -> "@g3ntt!"

```
Korvaa 'a' -> '@'
Korvaa 'e' -> '3'
Korvaa 'i' -> '!'
Korvaa 'o' -> '0'
```

  * `SeuraavaKirjain` (Caesar-siirros). Logiikka: Jokaista kirjainta siirretään aakkosissa yksi eteenpäin. Esimerkki: abc -> bcd. Vihje: Javassa `char` on luku. Voit tehdä `merkki + 1`. 
  
```
'a' -> 'b'
'b' -> 'c'
'k' -> 'l'
jne. 
```

Tässä harjoituksessa ei tarvitse huolehtia ö-kirjaimen pyörähtämisestä ympäri, ellei halua. Tehtävässä ei myöskään tarvitse huolehtia siitä, että salauksen ja purkamisen jälkeen saatu viesti ei välttämättä ole samanlainen kuin alkuperäinen viesti. Esimerkiksi jos `Hakkeri`-muuntajaa käytettäessä alkuperäisessä viestissä on oikeasti merkki `@`, pura-metodi antaa tulokseksi tuohon paikalle merkin `a`. Tämä ei haittaa tässä, mutta tietenkin oikeassa salauksessa pitäisi varmistaa, ettei tietoa katoa tai muutu vahingossa.
