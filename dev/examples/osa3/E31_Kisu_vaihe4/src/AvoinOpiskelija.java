/**
 * Avoimen yliopiston opiskelija
 */
public class AvoinOpiskelija extends Opiskelija {
    /**
     * Maksamattomien maksujen määrä
     */
    private double maksujaMaksamatta;

    /**
     * Avoimen yliopiston opiskelija
     *
     * @param nimi           Nimi
     * @param kayttajatunnus Käyttäjätunnus
     */
    public AvoinOpiskelija(String nimi, String kayttajatunnus) {
        super(nimi, kayttajatunnus);
        maksujaMaksamatta = 0;
    }

    /**
     * Osta opinto-oikeus kurssille.
     *
     * @param kurssi Ostettava kurssi
     * @param hinta  Kurssin hinta
     * @return Maksamattomien maksujen määrä
     */
    public double ostaOpintoOikeus(String kurssi, double hinta) {
        maksujaMaksamatta += hinta;
        return maksujaMaksamatta;
    }

    /**
     * Suorita opintomaksun maksu
     *
     * @param eur Suoritettu maksun määrä
     * @return Onko kaikki maksut maksettu
     */
    public boolean maksa(double eur) {
        maksujaMaksamatta -= eur;
        if (maksujaMaksamatta == 0) {
            IO.println("Maksut maksettu!");
            return true;
        }
        if (maksujaMaksamatta < 0) {
            IO.println("Maksut maksettu!");
            IO.println("Olet maksanut ylimääräistä " + Math.abs(maksujaMaksamatta) + " EUR.");
            return true;
        }

        IO.println("Maksuja maksamatta vielä: " + maksujaMaksamatta + " EUR.");
        return false;
    }
}
