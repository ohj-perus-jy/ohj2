public class TutkintoOpiskelija extends Opiskelija {

    private String tutkintoOhjelma;

    public TutkintoOpiskelija(String nimi, String kayttajatunnus, String tutkintoOhjelma)
    {
        super(nimi, kayttajatunnus);
        this.tutkintoOhjelma = tutkintoOhjelma;
    }

    public String getTutkintoOhjelma()
    {
        return tutkintoOhjelma;
    }

}
