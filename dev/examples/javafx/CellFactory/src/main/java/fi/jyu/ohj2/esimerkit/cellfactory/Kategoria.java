package fi.jyu.ohj2.esimerkit.cellfactory;

import javafx.beans.property.SimpleBooleanProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;
import javafx.beans.property.BooleanProperty;

public class Kategoria {

    private final StringProperty nimi = new SimpleStringProperty();
    private final BooleanProperty poistettu = new SimpleBooleanProperty();

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

    // Poistettu
    public void setPoistettu(boolean poistettu) {
        this.poistettu.set(poistettu);
    }

    public boolean isPoistettu() {
        return poistettu.get();
    }

    public BooleanProperty poistettuProperty() {
        return poistettu;
    }
}
