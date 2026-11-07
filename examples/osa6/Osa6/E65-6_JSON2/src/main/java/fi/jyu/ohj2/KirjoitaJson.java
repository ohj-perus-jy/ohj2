package fi.jyu.ohj2;

import tools.jackson.databind.ObjectMapper;
import tools.jackson.core.JacksonException;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class KirjoitaJson {
    static void main() {
        ObjectMapper mapper = new ObjectMapper();

        List<Henkilo> henkilot = List.of(
                new Henkilo("Aino", 22, "Turku"),
                new Henkilo("Pekka", 41, "Oulu")
        );

        Path polku = Path.of("data", "henkilot-uusi.json");

        try {
            Files.createDirectories(polku.getParent());
            mapper.writeValue(polku.toFile(), henkilot);
            IO.println("Kirjoitettiin JSON: " + polku.toAbsolutePath());
        } catch (IOException e) {
            IO.println("Kansion luominen epäonnistui: " + e.getMessage());
        } catch (JacksonException je) {
            IO.println("JSON-prosessointi epäonnistui: " + je.getMessage());
        }
    }
}