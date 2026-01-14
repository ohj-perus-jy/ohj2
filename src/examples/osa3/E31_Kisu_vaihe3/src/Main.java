public class Main {
    public static void main() {
        Opiskelija opiskelija = new Opiskelija("Matti Opiskelija", "matti123");
        opiskelija.kirjaudu();
        opiskelija.ilmoittauduKurssille("Ohjelmointi 2");
        opiskelija.naytaKurssit();

        Opettaja opettaja = new Opettaja("Maija Opettaja", "maijaope");
        opettaja.kirjaudu();
        opettaja.lisaaKurssi("Ohjelmointi 1");
        opettaja.lisaaKurssi("Ohjelmointi 2");
        opettaja.naytaOpetettavatKurssit();

        Sihteeri sihteeri = new Sihteeri("Sari Sihteeri", "saris");
        sihteeri.kirjaudu();
        sihteeri.kirjaaOpintosuoritus("matti123", "Ohjelmoinnin perusteet");
    }
}