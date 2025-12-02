# Rajapinnat

> [!Osaamistavoitteet]
>
> - Ymmärtää rajapinnan (interface) rooli ja käyttää sitä vaihtokohdissa (strategiat, palvelut).
> - Rajapinnat ("Kissa osaa Puhua, Kävellä, Hyppiä...")
> - abstrakti luokka vs. rajapinta (rajapintametodin oletustoteutus)
> - Ymmärrät, että luokka voi toteuttaa monta rajapintaa, mutta periä vain yhdestä luokasta
> - Testaaminen rajapintaa vasten, ei toteutusta vasten.
> - "Moniperintä" rajapintojen avulla
> - Käytetään perintää ja rajapintoja olioiden yhteistyössä

## Perintä ja rajapinnat olioiden yhteistyössä

Perinnällä ja rajapinnoilla on mahdollista tehdä joskus sama asia

Otetaan esimerkki, jossa käytämme perintää ja rajapintoja yhdessä. 

Kuvitellaan, että rakennamme järjestelmää, joka hallinnoi erilaisia ajoneuvoja, kuten autoja, polkupyöriä ja kuorma-autoja. Haluamme, että kaikki ajoneuvot voivat vaihtaa renkaita, mutta tapa, jolla tämä tehdään, voi vaihdella ajoneuvotyypin mukaan.