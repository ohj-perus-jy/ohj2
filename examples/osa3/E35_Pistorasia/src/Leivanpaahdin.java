/**
 * Leivänpaahdin on Keittiölaite, joka toimii verkkovirralla
 */
public class Leivanpaahdin extends Keittiolaite implements Verkkovirtalaite {

    @Override
    public void kytkeVirta() {
        // Leivänpaahtimen oma tapa reagoida virtaan:
        IO.println("Leivänpaahdin: Vastukset alkavat hehkua punaisena.");
    }

    /**
     * Puhdista leivänpaahdin.
     */
    @Override
    public void puhdista() {
        IO.println("Leivänpaahdin: Poistetaan murut ja pyyhitään kevyesti kostealla rätillä.");
    }
}