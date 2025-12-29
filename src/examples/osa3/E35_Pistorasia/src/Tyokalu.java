public abstract class Tyokalu {
    /**
     * Laitteen käyttötunnit
     */
    private int kayttotunnit = 0;

    /**
     * Käytä laitetta
     * @param tunnit Montako tuntia laitetta käytetään.
     */
    public void kayta(int tunnit)
    {
        this.kayttotunnit = tunnit;
    }

    /**
     * Huolla laitetta
     * @return Onnistuiko huolto
     */
    public abstract boolean huolla();
}
