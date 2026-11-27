import java.util.ArrayList;

class Opiskelija extends Henkilo {
    private List<String> kaynnissaOlevatKurssit = new ArrayList<>();
    private int opintopisteet;
    private boolean opintoOikeusVoimassa;

    public Opiskelija(String nimi, String kayttajatunnus) {
        super(nimi, kayttajatunnus);
        this.kaynnissaOlevatKurssit = new ArrayList<>();
        this.opintoOikeusVoimassa = false;
        this.opintopisteet = 0;
    }

    void aktivoiOpintoOikeus() {
        this.opintoOikeusVoimassa = true;
    }

    void ilmoittauduKurssille(String kurssi) {
        this.kaynnissaOlevatKurssit.add(kurssi);
    }

    public void naytaKurssit() {
        String kaikkiKurssit = String.join(", ", this.kaynnissaOlevatKurssit);
        IO.println(this.getNimi() + " opiskelee kursseilla: " + kaikkiKurssit);
    }
}