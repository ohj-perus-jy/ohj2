import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;


public class TiedostonLukija {
    static void main() {
        try {
            Scanner scanner = new Scanner(new File("data.csv"));
            // Ohitetaan otsikkorivi
            if (scanner.hasNextLine()) {
                scanner.nextLine();
            }
            // Luetaan rivejä, kunnes tiedoston loppu saavutetaan
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine(); // Esim. "Maija,25"
                String[] parts = line.split(","); // Pilkotaan rivi sarakkeiksi
                String nimi = parts[0]; // Ensimmäinen sarake on nimi
                int ika = Integer.parseInt(parts[1]); // Toinen sarake on ikä, parsitaan intiksi
                IO.println("Nimi: " + nimi + ", Ikä: " + ika);
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            IO.println("Tiedostoa ei löydy: " + e.getMessage());
        }
    }
}