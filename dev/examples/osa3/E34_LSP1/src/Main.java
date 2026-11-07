void main() {
    Soitin[] soittimet = {
            new Kitara(),
            new Piano(),
            new HarjoitusPiano()
    };

    Konsertti konsertti = new Konsertti();
    konsertti.soitaKaikkiaSoittimia(soittimet);
}