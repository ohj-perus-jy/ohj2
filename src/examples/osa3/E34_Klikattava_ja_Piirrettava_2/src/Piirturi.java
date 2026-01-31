/**
 * Piirturi-luokka vastaa piirtoalueen piirtämisestä.
 */
public class Piirturi {
    /**
     * Piirrä teksti nätin suorakaiteen sisään
     *
     * @param teksti     Teksti
     * @param korostettu Onko teksti korostettuna vai ei
     */
    public void piirraPainike(String teksti, boolean korostettu) {
        if (!korostettu) {
            IO.println("[ " + teksti + " ]");
        } else {
            IO.println("[*" + teksti + "*]");
        }
    }

    /**
     * Piirrä pelkkä teksti
     *
     * @param teksti Teksti
     */
    public void piirraTeksti(String teksti) {
        IO.println(teksti);
    }


    /**
     * Tyhjää piirtoalue
     */
    public void tyhjaa() {
        IO.println("Tyhjennetään piirtoalue");
        // Jätetään tässä toteuttamatta        
    }
}