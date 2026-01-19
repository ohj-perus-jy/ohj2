import java.util.ArrayList;

class Opiskelija extends Henkilo {
    List<String> kaynnissaOlevatKurssit;

    public Opiskelija() {
        this.kaynnissaOlevatKurssit = new ArrayList<>();
    }

    void naytaOpintoOhjelma() {
        String kurssit = String.join(", ", kaynnissaOlevatKurssit);
        IO.println(this.nimi + " opiskelee kursseilla: " + kurssit);
    }

    void ilmoittauduKurssille(String kurssi) {
        IO.println(this.nimi + " ilmoittautui kurssille: " + kurssi);
        kaynnissaOlevatKurssit.add(kurssi);
    }
}
