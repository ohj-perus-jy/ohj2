import java.util.ArrayList;
import java.util.List;

class Opiskelija extends Henkilo {
    private List<String> kaynnissaOlevatKurssit = new ArrayList<>();
    int opintopisteet = 0;

    public Opiskelija(String nimi, String kayttajatunnus) {
        super(nimi, kayttajatunnus);
        kaynnissaOlevatKurssit = new ArrayList<>();
        opintopisteet = 0;
    }

    void ilmoittauduKurssille(String kurssi) {
        kaynnissaOlevatKurssit.add(kurssi);
    }

    public void naytaKurssit() {
        String kaikkiKurssit = String.join(", ", kaynnissaOlevatKurssit);
        IO.println(this.getNimi() + " opiskelee kursseilla: " + kaikkiKurssit);
    }
}