# Komponenttien asettelu

Sovelluksemme on toiminnallisesti valmis, mutta sen ulkoasussa on vielä muutama
puute:

- Ikkunan oletuskoko on liian suuri.
- Ikkunan koon kasvattaminen jättää tyhjää tilaa väärään paikkaan.
- Komponenttien asettelu kaipaa hienosäätöä: valintaruudut ovat liian lähekkäin,
  nimiöt on keskitetty oudosti ja painikkeet ovat kaukana syöttökentistä.

Parannetaan sovelluksen ulkoasua ja tutustutaan `VBox`-säiliön lähisukulaiseen
`HBox`.

Avaa sovelluksen `main.fxml`-tiedosto SceneBuilderissa. Valitse heti yläpalkista
**View** <i class="bi bi-chevron-right"></i> **Show Outlines** tai paina
<kbd>Ctrl</kbd>+<kbd>E</kbd> (macOS: <kbd>Cmd</kbd>+<kbd>E</kbd>). Toiminto
muuttaa komponentit näyttämään laatikoilta, mikä helpottaa koon ja paikan
hahmottamista:

<img src="images/scenebuilder-outline.png">

Tämän osan jälkeen voit palata takaisin perusnäkymään valitsemalla **View** <i
class="bi bi-chevron-right"></i> **Hide Outlines**.

## Ikkunan ja komponenttien koko

Korjataan aluksi ikkunan koko. Valitse vasemman puolen Hierarchy-paneelista koko
sovelluksen sisältävä `VBox`-elementti ja avaa oikealta Layout-paneeli:

<video src="images/scenebuilder-layout-panel.mp4" controls></video>

Layout-paneeli sisältää komponentin kokoon liittyvät asetukset. JavaFX:ssä
jokaisella komponentilla on kolmenlaista korkeutta ja leveyttä:

- **Oletuskoko** (`Pref Width` ja `Pref Height`): komponentin oletuskoko, kun
  sovellusnäkymä ladataan. Koko voi kuitenkin muuttua riippuen komponentin
  luonteesta ja sitä ympäröivistä tai sisältämistä komponenteista.
- **Pienin koko** (`Min Width` ja `Min Height`): Pienin sallittu koko, johon
  komponentti voi kutistua.
- **Suurin koko** (`Max Width` ja `Max Height`): Suurin sallittu koko, johon
  komponentti voi kasvaa.

Voit antaa ominaisuuksille arvoksi desimaaliluvun tai käyttää seuraavia
erikoisarvoja:

- `USE_COMPUTED_SIZE`: JavaFX laskee komponentille parhaan koon sen sisällön
  perusteella.
- `USE_PREF_SIZE`: JavaFX käyttää oletuskokoa (`Pref`). Hyödyllinen koon
  rajoittamiseen.

Näitä huomioon ottaen asetetaan koko näkymän `VBox`:lle seuraavat arvot:

- Min Width: `USE_PREF_SIZE`
- Min Height: `USE_PREF_SIZE`
- Pref Width: `400`
- Pref Height: `400`
- Max Width: `USE_COMPUTED_SIZE`
- Max Height: `USE_COMPUTED_SIZE`

Toisin sanoen: alusta näkymä kokoon 400x400, äläkä salli sen pienentämistä
tästä, mutta anna sen kasvaa vapaasti. Huomaat muutoksen heti SceneBuilderissa:

<img src="images/scenebuilder-vbox-resize.png">

Tallenna FXML-tiedosto ja käynnistä sovellus. Ikkunan oletuskoko on nyt 400x400:

<img src="images/todo-app-pref-size.png" width="300">

Ikkunaa voi kuitenkin edelleen pienentää alle 400x400, koska muokkasimme vain
näkymän rajoja, emme koko ikkunan (`Stage`). Korjataan tämä asettamalla ikkunan
minimikoko `App`-luokan `start()`-metodissa. Samalla muokataan sovelluksen
otsikko siistimmäksi:

```java,ignore
public void start(Stage stage) throws IOException {
    FXMLLoader loader = new FXMLLoader(getClass().getResource("main.fxml"));
    Scene scene = new Scene(loader.load());

    stage.setScene(scene);
    // HIGHLIGHT_GREEN_BEGIN
    stage.setMinHeight(400);
    stage.setMinWidth(400);
    // HIGHLIGHT_GREEN_END
    // HIGHLIGHT_YELLOW_BEGIN
    stage.setTitle("TODO-sovellus");
    // HIGHLIGHT_YELLOW_END
    stage.show();
}
```

Nyt kun käynnistät sovelluksen, huomaat, että ikkunan kokoa ei voi pienentää
alle 400x400:

<video src="images/todo-app-size-limit.mp4" controls width="400"></video>

## `VBox`-säiliön komponenttien väli

`VBox`-komponentti sisältää Spacing-asetuksen, joka määrittää komponentin
sisällä olevien komponenttien välisen tyhjän tilan.

Huomaamme, että näkymän `VBox`-säiliössä välistys on 20, joka on hiukan liian
suuri. Korjataan tämä vaihtamalla asetuksen arvoksi `10`:

<img src="images/scenebuilder-vbox-spacing.png">

Korjataan samalla se, että tehtävien `VBox`-säiliöissä
`CheckBox`-valintaruutujen välissä ei ole yhtään tyhjää tilaa. Aseta tehtyjen ja
tekemättömien tehtävien `VBox`-komponenteille Spacing-arvoksi `5`. Tallenna
FXML-tiedosto ja aja sovellus. Huomaat, että nyt valintaruutujen välissä on
hieman tyhjää tilaa:

<img src="images/scenebuilder-checkbox-spacing.png" width="300">

## Komponenttien kasvaminen `VBox`-säiliön kasvaessa

Ikkunan koon muuttaminen paljastaa uuden ongelman: tehtyjen ja tekemättömien
listat eivät kasva ikkunan mukana. Alla oleva video havainnollistaa tilanteen:

<video src="images/todo-app-vbox-no-resize.mp4" controls width="300"></video>

Oletuksena `VBox` pitää sisällään olevien komponenttien korkeuden
muuttumattomana. Voimme kuitenkin määrittää erikseen, miten kunkin komponentin
tulisi käyttäytyä, kun säiliöön syntyy tyhjää tilaa. Tässä tapauksessa haluamme,
että listat täyttävät vapaan tilan, mutta muut komponentit (nimiöt, kentät,
painikkeet) pysyvät samankokoisina.

Valitse SceneBuilderissa tekemättömien tehtävien `VBox` ja avaa Layout-paneeli:

<img src="images/scenebuilder-vbox-constraints.png">

Kun komponentti on jonkin `VBox`-säiliön sisällä, komponentille on mahdollista
asettaa ns. Vgrow-asetus. Asetus määrittää, miten komponentin korkeuden tulee
käyttäytyä, jos komponenttia sisältävän `VBox` korkeus kasvaa. Mahdolliset
asetukset ovat:

- `NEVER`: Korkeus pysyy samana.
- `ALWAYS`: Täyttää aina tyhjän tilan. Jos usealla komponentilla on tämä asetus,
  ne jakavat tilan keskenään.
- `SOMETIMES`: Kasvaa vain, jos mitään muuta komponenttia ei voi kasvattaa.

Aseta tekemättömien tehtävien säiliölle Vgrow-asetuksen arvoksi `ALWAYS`. Tee
sama myös tehtyjen tehtävien säiliölle, jolloin kummatkin säiliöt kasvavat
samassa suhteessa.

Tallenna ja kokeile: nyt listat täyttävät ikkunan pystysuunnassa, ja muut
komponentit säilyttävät kokonsa.

## Painikkeen asettaminen syöttökentän tasolle

Tällä hetkellä syöttökenttä näyttää olevan hieman irrallinen painikkeesta.
Sovelluksissa on yleisempää, että suoraan kenttään liittyvät painikkeet
laitetaan syöttökentän kanssa samalle riville.

Koska `VBox` asettaa komponentit aina allekkain, tarvitsemme sen vaakasuoraa
vastinetta: **`HBox`** (**H**orizontal **Box**). Nimensä mukaisesti `HBox` on
säiliökomponentti, jonka sisällä olevat alkiot sijoitetaan vaakasuorassa
suunnassa vasemmalta oikealle.

Lisää `HBox`-komponentti tehtyjen tehtävien alle ja raahaa syöttökenttä ja
painike sen sisään:

<video src="images/scenebuilder-hbox-add.mp4" controls></video>

Aseta `HBox`-komponentille seuraavat asetukset:

- Spacing: `10` (syöttökentän ja painikkeen välille lisätään tyhjää tilaa)
- Pref Width ja Pref Height: `USE_COMPUTED_SIZE` (säiliön koko mukautuu
  syöttökentään ja painikkeeseen)
- Vgrow: `NEVER` (säiliön korkeus ei ikinä muutu vaikka sitä sisältävä `VBox`
  kasvaisi)

Valitse lopuksi `TextField`-syöttökenttä ja aseta sen **Hgrow**-asetukseksi
`ALWAYS`. Tämä vastaa `VBox`:n Vgrow-asetusta, mutta toimii vaakasuunnassa:
syöttökenttä täyttää nyt kaiken vapaan tilan leveyssuunnassa.

## Nimiöiden tasaaminen vasemmalle

Tehdään aivan viimeinen loppusilaus: sovelluksissa on yleistä, että nimiöt ovat
tasattu vasempaan reunaan. Korjataan vielä tasaus, jotta sovelluksen ulkoasu on
käyttäjälle "tutumpi".

Valitse koko näkymän päällimmäinen `VBox` ja aseta Properties-paneelissa
**Alignment**-asetukseksi `CENTER_LEFT`:

<img src="images/scenebuilder-alignment.png">

Tallenna ja käynnistä sovellus. Varmista, että kaikki toimii ja komponentit
mukautuvat hyvin ikkunan kokoon.

<video src="images/todo-app-final-product.mp4" controls></video>



<task>
  <task-title>Tehtävä 7.6: TODO-ohjelma, vaihe 6. <points>1 p.</points> </task-title>
  <handout>

{{#include ../exercises/7-6-todo-6/handout.md}}

  </handout>
  <task-link><a href="https://tim.jyu.fi/view/kurssit/tie/tiep111/tehtavat/osa7/tehtava6">Tee tehtävä TIMissä</a></task-link>
</task>




<!-- 

Komponetin kokoon vaikuttavat neljä pääominaisuutta: leveys (*width*), korkeus
(*height*), marginaali eli komponentin ympärillä oleva tila (*marginal*)
ja välistys eli komponentin sisäreunan ympärillä oleva tila (*padding*).
Visuaalisesti nämä ominaisuudet voidaan esittää seuraavasti:

```bob
+-------------------------------+
|            width              |
|     |<----------------- |     |
|                               |
|  -  +-------------------+     |
|h ^  |     padding       |     |
|e |  |   +----------+    |     |
|i |  |   |   {c}    |    |     |
|g |  |   | "Sisältö"|    |     |
|h |  |   +----------+    |     |
|t v  |       {p}         |     |
|  -  +-------------------+     |
|             {m}               |
|           margin              |
+-------------------------------+

Legend:
m = {
    fill: #af8255;
}
p = {
    fill: #b7c37f;
}
c = {
    fill: #87b0bc;
}
```

-->