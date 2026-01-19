import java.util.ArrayList;

class Opettaja extends Henkilo {
    List<String> opetettavatKurssit;

    public Opettaja() {
        this.opetettavatKurssit = new ArrayList<>();
    }

    void naytaOpetettavatKurssit() {
        String kurssit = String.join(", ", opetettavatKurssit);
        IO.println(this.nimi + " opettaa kursseja: " + kurssit);
    }

    void lisaaKurssi(String kurssi) {
        opetettavatKurssit.add(kurssi);
    }
}