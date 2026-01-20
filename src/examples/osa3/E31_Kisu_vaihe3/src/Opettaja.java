import java.util.ArrayList;
class Opettaja extends Henkilo {
    private String tehtavanimike;
    List<String> opetettavatKurssit = new ArrayList<>();

    public Opettaja(String nimi, String kayttajatunnus)
    {
        super(nimi, kayttajatunnus);
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