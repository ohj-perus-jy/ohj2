import java.io.File;
import java.io.IOException;
import java.util.Locale;
import java.util.Scanner;

public class LueNumerotScannerilla {
    public static void main(String[] args) throws IOException {

        double summa = 0.0;
        int maara = 0;

        Scanner sc = new Scanner(new File("mittaukset.txt"));
        try {
            sc.useLocale(Locale.US); // desimaalipiste "."
            sc.useDelimiter("[\\s,;]+"); // välilyönti, rivinvaihto, pilkku tai puolipiste

            while (sc.hasNext()) {
                if (sc.hasNextDouble()) {
                    summa += sc.nextDouble();
                    maara++;
                } else {
                    sc.next(); // ohita token (esim. "virhe")
                }
            }
        } finally {
            sc.close();
        }

        System.out.println("Lukuja: " + maara);
        System.out.println("Summa: " + summa);
        System.out.println("Keskiarvo: " + (maara == 0 ? 0 : summa / maara));
    }
}