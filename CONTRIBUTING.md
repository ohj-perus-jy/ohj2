# Kontribuutioehdotus

## Aseta autentikointi
- SSH vs. PAT?
    - Voi käyttää molempia, mutta suositellaan turvallisuussyistä SSH:ta
- Tarkemmat ohjeet SSH:n käyttöönottoon: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

## Kloonaa repositorio
- **SSH:ta käytettäessä:**
    - git clone git@github.com:ohj-perus-jy/ohj2.git
        - Osoite löytyy projektin juuresta oikealla ylhäällä olevasta "code" painikkeesta ja sieltä kohdasta SSH
- CLI ohjeistus?

## Konttisysteemi devausta varten
- Asenna Rust (mukana tulee myös automaattisesti Cargo)
- Asenna mdbook
- Asenna mdbookkiin mermaid tuki: https://github.com/badboy/mdbook-mermaid
- Mene komentorivillä projektin juureen ja aja komento: mdbook serve --hostname 0.0.0.0 --port 3000 --open

## Tee branch
- git switch -c [branchin nimi]
    - Luo uuden branchin [branchin nimi] ja vaihtaa siihen
- Voit katsella lisää osoitteesta: https://git-scm.com/docs/git-switch

## Puske branch etävarastoon
- git push -u origin [branchin nimi]

## Tee muutoksia branchiin

## Tee pull request
#### Halutaanko hyödyntää tuota issuen automaattista linkkausta vai miten PR ja issuet keskustelevat keskenään?
git commit -m "[haluamasi teksti] #[issuen numero]"
1. Puske halutut muutokset branchiin
2. Githubin kautta tai:
    1. Tähän ohjeet CLI versioon

## Puske muutoksia branchiin ehdotuksien mukaisesti
