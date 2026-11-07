/**
 * Pelkkää tekstiä esittävä piirrettävä komponentti.
 */
public class Teksti implements Piirrettava {
    private String sisalto;

    public Teksti(String sisalto) {
        this.sisalto = sisalto;
    }

    /**
     * Piirrä komponentti
     *
     * @param piirturi Piirturi
     */
    @Override
    public void piirra(Piirturi piirturi) {
        piirturi.piirraTeksti(sisalto);
    }
}
