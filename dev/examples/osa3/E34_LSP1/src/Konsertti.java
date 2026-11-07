public class Konsertti {
    public void soitaKaikkiaSoittimia(Soitin[] soittimet) {
        for (Soitin soitin : soittimet) {
            soitin.soita();
        }
    }
}