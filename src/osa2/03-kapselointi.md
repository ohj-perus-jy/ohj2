# Kapselointi

> [!Osaamistavoitteet]
>
> - Ymmärrät kapseloinnin ja sen hyödyt (Decoupling/Coupling)
> - Toteutetaan olioiden yhteistyö pienessä olioverkossa. Pidetään kytkentä löyhänä, eli olioiden välinen riippuvuus on vain rajapinnan (metodien) varassa, ei sisäisen toteutuksen varassa.
> - julkisuusmääreet `public` ja `private`, getterit ja setterit, metodi pääasiallisena tapana olioille "viestiä"
> - Kutsuja ei tiedä (eikä voi riippua siitä) miten olion tila on toteutettu. Toteutustaa voi muuttaa ilman että kutsujan tarvitsee muuttaa koodiaan.
