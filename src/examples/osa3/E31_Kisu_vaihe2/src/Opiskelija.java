import java.util.ArrayList;
class Opiskelija extends Henkilo {
    List<String> kaynnissaOlevatKurssit;

    public Opiskelija(String nimi)
    {
        super(nimi);
        kaynnissaOlevatKurssit = new ArrayList<>();
    }

    void ilmoittauduKurssille(String kurssi) {
        kaynnissaOlevatKurssit.add(kurssi);
    }

    public void naytaKurssit(){
        String kaikkiKurssit = String.join(", ", kaynnissaOlevatKurssit);
        IO.println(this.getNimi() + " opiskelee kursseilla: " + kaikkiKurssit);
    }
}