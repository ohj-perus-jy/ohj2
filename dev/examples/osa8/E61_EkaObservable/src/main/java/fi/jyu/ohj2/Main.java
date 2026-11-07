package fi.jyu.ohj2;

import javafx.collections.FXCollections;
import javafx.collections.ListChangeListener;
import javafx.collections.ObservableList;

public class Main {
    static void main() {
        // 1. Luodaan ObservableList tavallisen ArrayListin sijaan
        ObservableList<String> nimet = FXCollections.observableArrayList();

        // 2. Rekisteröidään kuuntelija, joka reagoi heti kun listan sisältö muuttuu
        nimet.addListener((ListChangeListener<String>)change -> {
            while (change.next()) { // Käydään läpi kaikki tapahtuneet muutokset
                if (change.wasAdded()) {
                    IO.println("Listalle lisättiin: " + change.getAddedSubList());
                }
            }
        });

        // 3. Muutetaan dataa
        nimet.add("Ada");
        nimet.add("Linus");

    }
}
