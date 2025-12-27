/**
 * Sirkkeli on Työkalu, joka toimii verkkovirralla
 */
public class Sirkkeli extends Tyokalu implements Verkkovirtalaite {

    @Override
    public void kytkeVirta() {
        // Sirkkelin oma tapa reagoida virtaan:
        System.out.println("Sirkkeli: Moottori alkaa pyörittää terää 4000 rpm.");

        // Kutsutaan tässä myös yliluokan kayta()-metodia, jolloin
        // käyttötunnit lisääntyvät.
        super.kayta(1);
    }

    /**
     * Huolletaan sirkkeli.
     * @return Onnistuiko huolto.
     */
    @Override
    public boolean huolla() {
        System.out.println("Huolletaan sirkkeliä... Teroitetaan terää ja säädetään kierrosnopeutta.");
        return true;
    }
}