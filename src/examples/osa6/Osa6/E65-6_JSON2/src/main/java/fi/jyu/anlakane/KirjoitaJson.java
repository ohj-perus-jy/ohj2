package fi.jyu.anlakane;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class KirjoitaJson {
    public static void main(String[] args) {
        ObjectMapper mapper = new ObjectMapper()
                .enable(SerializationFeature.INDENT_OUTPUT); // kauniimpi sisennys

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
            IO.println("JSONin kirjoittaminen epäonnistui: " + e.getMessage());
        }
    }
}