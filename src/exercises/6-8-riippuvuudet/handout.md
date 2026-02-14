Tee uusi Maven-projekti. Aseta pakkauksen nimeksi `fi.jyu.omatunnus` (laita
`omatunnus`-kohdalle JY-käyttäjätunnus tai jokin muu keksimäsi käyttäjänimi).
Anna pääluokan nimeksi `Riippuvuudet`. 

```java,ignore
void main() {
    JSONObject json = new JSONObject();
    json.put("nimi", "Maija");
    json.put("ika", 25);
    IO.println(json.getString("nimi"));
    IO.println(json.getInt("ika"));
}
```

Lisää nyt `pom.xml`-tiedostoon riippuvuus `json`-nimiseen artefaktiin. Etsi tämä
kirjasto Maven Centralista, ja kopioi sieltä XML-koodi `pom.xml`-tiedostoosi.
Lisää myös riippuvuuden vaatima `import`-lause luokan alkuun.