/**
 * Pelkkää tekstiä esittävä piirrettävä komponentti.
 */
public class Teksti implements Piirrettava {
    private String sisalto;
    public Teksti(String sisalto)
    {
        this.sisalto = sisalto;
    }

    @Override
    public void piirra() {
        // Piirretään vain pelkkä tekstisisältö ilman kehyksiä
        IO.println(sisalto);
    }
}
