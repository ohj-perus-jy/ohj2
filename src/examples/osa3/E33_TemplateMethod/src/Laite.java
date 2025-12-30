public abstract class Laite {
    private String nimi;
    private boolean kytketty;

    protected Laite(String nimi) {
        this.nimi = nimi;
    }

    public final void suoritaPaivitys() {
        kytkePaalle();
        valmistelePaivitys(); // Abstrakti askel, jonka aliluokka toteuttaa
        paivitys();
        kytkePois();
    }

    protected abstract void valmistelePaivitys();

    private void paivitys() {
        IO.println("Haetaan uusin päivitys verkosta...");
        IO.println("Laite päivitetään...");
    }

    public void kytkePaalle() {
        if (!kytketty) {
            kytketty = true;
            System.out.println(nimi + " käynnistyy.");
        }
    }

    public void kytkePois() {
        if (kytketty) {
            kytketty = false;
            System.out.println(nimi + " sammuu.");
        }
    }


    public abstract void vaihdaTilaa();
    public abstract void raportoiTila();
}