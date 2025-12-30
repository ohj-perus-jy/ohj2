/**
 * Leivänpaahdin on Keittiölaite, joka toimii verkkovirralla
 */
public class Leivanpaahdin extends Keittiolaite implements Verkkovirtalaite {

    @Override
    public void kytkeVirta() {
        // Leivänpaahtimen oma tapa reagoida virtaan:
        System.out.println("Leivänpaahdin: Vastukset alkavat hehkua punaisena.");
    }

    /**
     * Puhdista leivänpaahdin.
     */
    @Override
    public void puhdista() {
        System.out.println("Leivänpaahdin: Poistetaan murut ja pyyhitään kevyesti kostealla rätillä.");
    }
}