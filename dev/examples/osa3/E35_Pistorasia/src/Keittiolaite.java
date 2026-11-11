/**
 * Keittiölaite
 */
public abstract class Keittiolaite {
    /**
     * Sisältääkö laite lämmitysvastuksia.
     */
    boolean lammittava;

    /**
     * Kaikki keittiölaitteet pitää voida pestä.
     */
    public abstract void puhdista();
}
