class Henkilo {
    private String nimi;

    /**
     * Yksilöllinen käyttäjätunniste
     */
    private String kayttajatunnus;

    /**
     * Onko henkilö kirjautunut järjestelmään.
     */
    private boolean kirjautunut;

    public Henkilo(String nimi, String kayttajatunnus)
    {
        this.nimi = nimi;
        this.kayttajatunnus = kayttajatunnus;
        this.kirjautunut = false;
    }

    public String getNimi()
    {
        return nimi;
    }

    protected void kirjaudu() {
        IO.println("Kirjautuminen onnistui käyttäjätunnuksella: " + kayttajatunnus);
        kirjautunut = true;
    }

    protected void kirjauduUlos() {
        IO.println(kayttajatunnus + " kirjautui ulos.");
        kirjautunut = false;
    }
}