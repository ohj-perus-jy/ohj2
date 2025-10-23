# Object ja muita hyödyllisiä rajapintoja Javassa

> [!Osaamistavoitteet]
>
> - Ymmärtää, että kaikki Javan luokat perivät `Object`-luokasta
> - Tuntee hyödylliset ylikirjoitettavat metodit `Object`-luokassa: `equals`, `toString`, (ehkä `hashCode`?)
> - Tuntee hyödyllisiä Java-kielen rajapintoja
>    - Vertailurajapintoja (Comparable<T>) -> mahdollistaa Javan järjestämismetodien käytön (Arrays.sort jne.)
>    - Cloneable -> mahdollistaa olion todellisen kopioinnin (vrt. viite)
>    - `Iterable<T>`-rajapinta ja for-each-silmukka
>    - Bonus: Vertailuluokka (Comparator<T>) -> mahdollistaa määrittää useita erilaisia vertailutapoja samalle luokalle
