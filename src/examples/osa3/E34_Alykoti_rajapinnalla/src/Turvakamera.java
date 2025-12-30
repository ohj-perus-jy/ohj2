public class Turvakamera extends Laite {
    private boolean tallennusPaalla = false;

    public Turvakamera(String nimi)
    {
        super(nimi);
    }

    @Override
    public void vaihdaTilaa() {
        // Kytke tallennus päälle/pois
        tallennusPaalla = !tallennusPaalla;
    }
    @Override
    public void raportoiTila() {
        String tila = tallennusPaalla ? "päällä" : "pois";
        System.out.println("Turvakameran tallennus on " + tila + ".");
    }
}