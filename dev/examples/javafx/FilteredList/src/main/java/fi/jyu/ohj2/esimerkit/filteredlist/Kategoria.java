package fi.jyu.ohj2.esimerkit.filteredlist;

import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

public class Kategoria {

    private final StringProperty nimi = new SimpleStringProperty();

    public Kategoria() {
        // Tarvitaan Jacksonille
    }

    public Kategoria(String nimi) {
        this.nimi.set(nimi);
    }

    // Nimi
    public void setNimi(String nimi) {
        this.nimi.set(nimi);
    }

    public String getNimi() {
        return nimi.get();
    }

    public StringProperty nimiProperty() {
        return nimi;
    }

    public String toString() {
        return getNimi();
    }
}
