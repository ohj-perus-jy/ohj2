/**
 * Laatikon näköinen klikkattava painike,
 * jossa on tekstiä.
 */
public class Painike implements Piirrettava, Klikattava {

    private String sisalto;
    private boolean korostettu;

    public Painike(String sisalto)
    {
        this.sisalto = sisalto;
        this.korostettu = false;
    }

    /**
     * Piirretään painike Piirturi-olion avulla.
     */
    @Override
    public void piirra(Piirturi piirturi) {
        piirturi.piirraPainike(sisalto, korostettu);
    }

    /**
     * Käsitellään klikkaustapahtuma
     */
    @Override
    public void klikattu() {
        IO.println("(Klikattiin painiketta, jossa lukee \"" + sisalto + "\")");
    }

    /**
     * Asetetaan korostustila. Jos tila muuttuu, piirretään komponentti uudestaan.
     */
    @Override
    public void asetaKorostus(boolean korostus) {
        this.korostettu = korostus;
    }
}
