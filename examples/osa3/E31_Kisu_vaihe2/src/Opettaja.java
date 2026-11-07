import java.util.ArrayList;
import java.util.List;

class Opettaja extends Henkilo {
    private List<String> opetettavatKurssit;

    public Opettaja(String nimi) {
        super(nimi);
        this.opetettavatKurssit = new ArrayList<>();
    }

    void lisaaKurssi(String kurssi) {
        opetettavatKurssit.add(kurssi);
    }

    void naytaOpetettavatKurssit() {
        String kurssit = String.join(", ", opetettavatKurssit);
        IO.println(this.getNimi() + " opettaa kursseja: " + kurssit);
    }
}