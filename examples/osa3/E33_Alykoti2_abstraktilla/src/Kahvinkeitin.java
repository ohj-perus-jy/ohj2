public class Kahvinkeitin extends Laite {

    private boolean kiehumassa = false;

    @Override
    public void vaihdaTilaa() {
        // Keitä kahvia tai kytke keitin pois päältä
        kiehumassa = !kiehumassa;
    }

    @Override
    public void raportoiTila() {
        String tila = kiehumassa ? "päällä" : "pois";
        IO.println("Kahvinkeittimen pannu on " + tila + ".");
    }
}