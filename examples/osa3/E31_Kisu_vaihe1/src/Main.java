void main() {
    Opiskelija opiskelija = new Opiskelija();
    opiskelija.setNimi("Olli Opiskelija");
    opiskelija.ilmoittauduKurssille("Ohjelmointi 2");

    Opettaja opettaja = new Opettaja();
    opettaja.setNimi("Maija Opettaja");
    opettaja.lisaaKurssi("Ohjelmointi 1");
    opettaja.lisaaKurssi("Ohjelmointi 2");
    opettaja.naytaOpetettavatKurssit();
}