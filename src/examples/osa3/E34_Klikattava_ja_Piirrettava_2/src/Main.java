public class Main {
    public static void main() {
        Naytto naytto = new Naytto();
        Teksti otsikko = new Teksti("Haluatko aloittaa rajapintojen opiskelun?");
        Painike okPainike = new Painike("OK!");

        naytto.lisaaKomponentti(otsikko);
        naytto.lisaaKomponentti(okPainike);

        // Piirretään kaikki komponentit
        naytto.paivita();

        // Simuloidaan hiiren vieminen painikkeen päälle
        okPainike.asetaKorostus(true);
        // Päivitetään komponentit. Huomaa, että
        // tämä piirtää aivan kaikki komponentit uudelleen.
        naytto.paivita();

        // Simuloidaan klikkaus
        okPainike.klikattu();
    }
}