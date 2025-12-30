public class Main {
    public static void main(String[] args) {
        Laite[] laitteet = {
                new Valo(),
                new Turvakamera(),
                new Kahvinkeitin()
        };

        for (Laite laite : laitteet) {
            laite.vaihdaTilaa();
            laite.raportoiTila();
        }
    }
}