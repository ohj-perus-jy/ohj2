public class Ympyra extends Muoto {

    double sade;

    public Ympyra(double r) {
        this.sade = r;
    }

    @Override
    public double laskeAla() {
        return Math.PI * sade * sade;
    }
}
