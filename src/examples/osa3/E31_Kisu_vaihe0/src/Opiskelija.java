import java.util.ArrayList;

class Opiskelija {
    String nimi;
    ArrayList<String> kaynnissaOlevatKurssit;

    public Opiskelija() {
        this.kaynnissaOlevatKurssit = new ArrayList<>();
    }

    void setNimi(String nimi) {
        this.nimi = nimi;
    }

    String getNimi() {
        return this.nimi;
    }

    void naytaOpintoOhjelma() {
        String kurssit = String.join(", ", kaynnissaOlevatKurssit);
        IO.println(nimi + " opiskelee kursseilla: " + kurssit);
    }

    void ilmoittauduKurssille(String kurssi) {
        IO.println(this.nimi + " ilmoittautui kurssille: " + kurssi);
        kaynnissaOlevatKurssit.add(kurssi);
    }
}
