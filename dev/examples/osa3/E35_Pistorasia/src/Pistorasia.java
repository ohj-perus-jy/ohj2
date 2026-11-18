public class Pistorasia {

    // Pistorasiaan voi kytkeä MINKÄ TAHANSA (yhden) verkkovirtalaitteen.
    // Pistorasiaa ei kiinnosta, onko se sirkkeli vai paahdin.
    public void kytkeLaite(Verkkovirtalaite laite) {
        IO.println("--- Pistorasia antaa sähköä ---");

        // Pistorasia kutsuu sopimuksen mukaista metodia.
        // Tässä tapahtuu polymorfismi: oikea laite reagoi oikealla tavalla.
        laite.kytkeVirta();
    }
}