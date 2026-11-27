package fi.jyu.ohj2.esimerkit.cellfactory;

import javafx.beans.property.ObjectProperty;
import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

public class Tehtava {

    private final StringProperty otsikko = new SimpleStringProperty();
    private final ObjectProperty<Kategoria> kategoria = new SimpleObjectProperty<>();

    public Tehtava() {
        // Tarvitaan Jacksonille
    }

    public Tehtava(String otsikko, Kategoria kategoria) {
        this.otsikko.set(otsikko);
        this.kategoria.set(kategoria);
    }

    // Otsikko
    public void setOtsikko(String otsikko) {
        this.otsikko.set(otsikko);
    }

    public String getOtsikko() {
        return otsikko.get();
    }

    public StringProperty otsikkoProperty() {
        return otsikko;
    }

    // Kategoria
    public void setKategoria(Kategoria kategoria) {
        this.kategoria.set(kategoria);
    }

    public Kategoria getKategoria() {
        return kategoria.get();
    }

    public ObjectProperty<Kategoria> kategoriaProperty() {
        return kategoria;
    }
}
