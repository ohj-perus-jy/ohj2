public class Kaunistaja {
    public static String MuotoileKauniisti(Rakennus rakennus) {
        return "Ihana rakennus, jonka omistaa "
                + rakennus.getOmistaja()
                + ", on väriltään "
                + rakennus.getVäri().toLowerCase() + ".";
    }
}
