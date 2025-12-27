public class Rakennus {
    private String omistaja;
    private String väri;

    public Rakennus(String omistaja, String väri)
    {
        this.omistaja = omistaja;
        this.väri = väri;
    }

    public String getVäri() {
        return this.väri;
    }

    public String getOmistaja() {
        return this.omistaja;
    }

    // Olion metodi.
    public String kaunista() {
        // Välitetään omistava olio tulosta-metodille.
        return Kaunistaja.MuotoileKauniisti(this);
    }

    // Staattinen metodi, joka ottaa vastaan Rakennus-olion.
    public static void tulosta(Rakennus rakennus) {
        IO.println(rakennus.omistaja + " " + rakennus.väri);
    }
}
