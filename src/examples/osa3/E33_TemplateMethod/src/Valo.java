public class Valo extends Laite {
    private int kirkkaus = 0;

    public Valo(String nimi) {
        super(nimi);
    }

    @Override
    protected void valmistelePaivitys() {
        IO.println("Valmistellaan valoa päivitystä varten...");
        IO.println("Asetetaan valo kirkkauteen 0%...");
    }

    @Override
    public void vaihdaTilaa() {
        // Vaihda kirkkaus 0 -> 50 -> 100 -> 0 ...
        switch (kirkkaus) {
            case 0 -> kirkkaus = 50;
            case 50 -> kirkkaus = 100;
            case 100 -> kirkkaus = 0;
        }
    }

    @Override
    public void raportoiTila() {
        IO.println("Valon kirkkaus on " + kirkkaus + "%.");
    }
}