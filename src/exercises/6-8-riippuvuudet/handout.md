Tee uusi Maven-projekti. Luo `Main`-luokka ja `main`-metodi, johon kirjoitat seuraavan koodin:

```java,ignore
public class Riippuvuudet {

    static void main() {

        JSONObject json = new JSONObject();
        json.put("nimi", "Maija");
        json.put("ika", 25);

        IO.println(json.getString("nimi"));
        IO.println(json.getInt("ika"));
    }
}
```

Lisää `pom.xml`-tiedostoon riippuvuus `json`-nimiseen artefaktiin. Etsi tämä
riippuvuus Maven Centralista, ja kopioi sieltä XML-koodi `pom.xml`-tiedostoosi.
Lisää myös riippuvuuden vaatima `import`-lause luokan alkuun.