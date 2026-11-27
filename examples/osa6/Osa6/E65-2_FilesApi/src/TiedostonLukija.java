import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class TiedostonLukija {

    public static void main(String[] args) {
        try {
            List<String> lines = Files.readAllLines(Paths.get("data.csv"));
            // Ohitetaan otsikkorivi
            for (int i = 1; i < lines.size(); i++) {
                String line = lines.get(i); // Esim. "Maija,25"
                String[] parts = line.split(","); // Pilkotaan rivi sarakkeiksi
                String nimi = parts[0]; // Ensimmäinen sarake on nimi
                int ika = Integer.parseInt(parts[1]); // Toinen sarake on ikä, parsitaan intiksi
                IO.println("Nimi: " + nimi + ", Ikä: " + ika);
            }
        } catch (IOException e) {
            IO.println("Tiedostoa ei löydy tai sitä ei voi lukea: " + e.getMessage());
        } finally {
            // Ei tarvitse erikseen sulkea mitään, koska Files API hoitaa sen puolestamme
        }
    }
}