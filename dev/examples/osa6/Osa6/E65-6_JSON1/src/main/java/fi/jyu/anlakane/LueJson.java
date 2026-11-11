package fi.jyu.anlakane;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.nio.file.Path;
import java.util.List;


public class LueJson {
    public static void main(String[] args) {
        ObjectMapper mapper = new ObjectMapper();
        Path polku = Path.of("", "henkilot.json");

        try {
            List<Henkilo> henkilot = mapper.readValue(
                    polku.toFile(),
                    new TypeReference<List<Henkilo>>() {}
            );

            henkilot.forEach(h ->
                    IO.println(h.nimi() + " (" + h.ika() + "), " + h.kaupunki())
            );
        } catch (IOException e) {
            IO.println("JSONin lukeminen epäonnistui: " + e.getMessage());
        }
    }
}