void main()
{
    Lista<String> nimet = new Lista<>(10);
    Object o = nimet;
    Lista<Integer> luvut = (Lista<Integer>) o; // unchecked cast
    luvut.add(42);
    String s = nimet.get(0);
}