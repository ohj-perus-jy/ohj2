import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Stream1 {
    static void main() {
        try {
            Files.lines(Paths.get("data.csv"))
                    .skip(1) // Ohitetaan otsikkorivi
                    .map(line -> line.split(",")) // Pilkotaan rivi sarakkeiksi
                    .forEach(parts -> {
                        String nimi = parts[0]; // Ensimmäinen sarake on nimi
                        int ika = Integer.parseInt(parts[1]); // Toinen sarake on ikä, parsitaan intiksi
                        IO.println("Nimi: " + nimi + ", Ikä: " + ika);
                    });
        } catch (IOException e) {
            IO.println("Tiedostoa ei löydy tai sitä ei voi lukea: " + e.getMessage());
        }
    }
}