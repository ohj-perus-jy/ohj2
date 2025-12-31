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

    @Override
    public void piirra() {
        // Piirretään suorakulmio ja teksti
        if (!korostettu) {
            IO.println("[ " + sisalto + " ]");
        } else {
            IO.println("[*" + sisalto + "*]");
        }
    }

    @Override
    /**
     * Käsitellään klikkaustapahtuma
     */
    public void klikattu() {
        IO.println("(Klikattiin painiketta, jossa lukee \"" + sisalto + "\")");
    }

    @Override
    /**
     * Asetetaan korostustila.
     */
    public void asetaKorostus(boolean korostus) {
        this.korostettu = korostus;
    }
}
