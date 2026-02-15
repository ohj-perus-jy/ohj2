import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Stream2 {
    static void main() {
        try {
            List<String> nimet = Files.lines(Paths.get("data.csv"))
                    .skip(1) // Ohitetaan otsikkorivi
                    .map(line -> line.split(",")) // Pilkotaan rivi sarakkeiksi
                    .filter(parts -> Integer.parseInt(parts[1]) >= 18) // Suodatetaan alle 18-vuotiaat
                    .map(parts -> parts[0]) // Otetaan vain nimi
                    .sorted() // Järjestetään nimet aakkosjärjestykseen
                    .toList(); // Kerätään tulokset listaksi

            nimet.forEach(IO::println); // Tulostetaan nimet
        } catch (IOException e) {
            IO.println("Tiedostoa ei löydy tai sitä ei voi lukea: " + e.getMessage());
        }
    }
}