public class Kahvinkeitin extends Laite {

    private boolean kiehumassa = false;

    public Kahvinkeitin(String nimi)
    {
        super(nimi);
    }

    @Override
    protected void valmistelePaivitys() {
        IO.println("Valmistellaan keitintä päivitystä varten...");
        IO.println("Keskeytä kiehuminen...");
    }

    @Override
    public void vaihdaTilaa() {
        // Keitä kahvia tai kytke keitin pois päältä
        kiehumassa = !kiehumassa;
    }
    @Override
    public void raportoiTila() {
        String tila = kiehumassa ? "päällä" : "pois";
        System.out.println("Kahvinkeittimen pannu on " + tila + ".");
    }
}