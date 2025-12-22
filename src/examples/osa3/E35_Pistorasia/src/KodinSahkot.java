public class KodinSahkot {

    public static void main(String[] args) {

        // 1. Luodaan infrastruktuuri: Pistorasia
        // Tässä kohtaa Pistorasia-olio syntyy tietokoneen muistiin.
        Pistorasia keittionPistoke = new Pistorasia();

        // 2. Luodaan laitteet
        // Huomaa: Muuttujan tyyppi voi olla joko rajapinta (Verkkovirtalaite)
        // tai luokka itse (Leivanpaahdin). Molemmat toimivat.
        Verkkovirtalaite paahdin = new Leivanpaahdin();
        Verkkovirtalaite sirkkeli = new Sirkkeli();

        // 3. Käytetään laitteita pistorasian kautta
        System.out.println("--- Aamu keittiössä ---");

        // Kytketään paahdin seinään
        keittionPistoke.kytkeLaite(paahdin);
        // TULOSTUS: "Pistorasia antaa sähköä" -> "Leivänpaahdin: Vastukset alkavat hehkua..."

        System.out.println("\n--- Remontti alkaa ---");

        // Otetaan paahdin pois ja kytketään sirkkeli SAMAAN pistorasiaan
        keittionPistoke.kytkeLaite(sirkkeli);
        // TULOSTUS: "Pistorasia antaa sähköä" -> "Sirkkeli: Moottori alkaa pyörittää..."

        // sirkkeli.kayta(); // Ei onnistu!
        // Huomaa, että emme tässä voi kutsua kayta()-metodia,
        // vaan kytkeminen pistorasiaan hoitaa myös käyttämisen, ts.
        // käyttötuntien kasvattamisen.
    }
}