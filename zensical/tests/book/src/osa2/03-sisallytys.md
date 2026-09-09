# Sisällytys

Sisällytykset (README.md kohta 1) ratkaistaan ennen muita muunnoksia, joten
sivulle päätyy tiedoston sisältö eikä makro. Kolme muotoa, samat kuin
oikeassa materiaalissa.

Koko tiedosto:

{{#include ./ohje.md}}

Yksi rivi taulukon soluun:

| Kohta | Teksti                   |
| ----- | ------------------------ |
| 1     | {{#include ./ohje.md:1}} |

Koodiaidan sisällä `// FILE:` -merkinnän jäljessä: monitiedostolohko näkee
vasta sisällytetyn tekstin ja jakaa sen välilehdiksi.

```java,ignore
// FILE: Esimerkki.java
{{#include ./Esimerkki.java}}
```
