public class Main {
    public static void main(String[] args) {
        Teksti otsikko = new Teksti("Haluatko aloittaa rajapintojen opiskelun?");
        otsikko.piirra();

        Painike okPainike = new Painike("OK!");
        okPainike.piirra();

        // Simuloidaan hiiren vieminen painikkeen päälle
        // Korostamisen jälkeen piirretään painike uudestaan
        okPainike.asetaKorostus(true);
        okPainike.piirra();

        // Simuloidaan klikkaus
        okPainike.klikattu();
    }
}