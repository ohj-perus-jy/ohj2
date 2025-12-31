public class Suorakulmio extends Muoto {
    double leveys;
    double korkeus;

    public Suorakulmio(double leveys, double korkeus)
    {
        this.leveys = leveys;
        this.korkeus = korkeus;
    }

    @Override
    public double laskeAla() {
        return leveys * korkeus;
    }
}
