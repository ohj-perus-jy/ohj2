# TableView

## Tyhjän rivin klikkaaminen

Oletuksena TableView-komponentti *ei* poista valintaa, jos käyttäjä klikkaa tyhjää riviä. Tämä on usein epäintuitiivista.

Tyhjän rivin klikkaaminen saadaan koodissa kiinni esimerkiksi asettamalla
riveille `setOnMouseClicked`-kuuntelija, joka tarkistaa, onko klikattu rivi `null` ja poistaa valinnan, jos näin on.

```java,ignore
tableView.setRowFactory(tv -> {
    TableRow<MyData> rivi = new TableRow<>();
    rivi.setOnMouseClicked(tapahtuma -> {
        if (rivi.isEmpty()) {
            tableView.getSelectionModel().clearSelection();
        }
    });
    return rivi;
});
```