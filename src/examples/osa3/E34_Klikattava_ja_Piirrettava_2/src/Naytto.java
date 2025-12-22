import java.util.ArrayList;

/**
 * Naytto-luokka hallinnoi piirrettäviä komponentteja.
 */
public class Naytto {
    private ArrayList<Piirrettava> komponentit = new ArrayList<>();
    private Piirturi piirturi = new Piirturi();

    public void lisaaKomponentti(Piirrettava p) {
        komponentit.add(p);
    }

    public void poistaKomponentti(Piirrettava p) {
        komponentit.remove(p);
    }

    public void paivita() {
        piirturi.tyhjaa();
        for (Piirrettava p : komponentit) {
            p.piirra(piirturi);
        }
    }
}