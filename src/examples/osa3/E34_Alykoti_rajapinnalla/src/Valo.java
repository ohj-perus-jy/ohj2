public class Valo extends Laite implements Saadettava {
    private int kirkkaus = 0;

    protected Valo(String nimi) {
        super(nimi);
    }

    @Override
    public void asetaArvo(int arvo) {
        if (arvo < 0) arvo = 0;
        if (arvo > 100) arvo = 100;
        this.kirkkaus = arvo;
    }

    @Override
    public void vaihdaTilaa() {
        // Yksinkertainen päälle-pois
        if (kirkkaus == 100) kirkkaus = 0;
        else kirkkaus = 100;
    }

    @Override
    public void raportoiTila() {
        IO.println("Valon kirkkaus on " + kirkkaus + "%.");
    }
}