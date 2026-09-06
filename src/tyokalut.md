# Työkaluohjeet

**Ohjelmointi 2** -opintojaksolla käytämme seuraavia työkaluja:

- **[Java Development Kit (JDK)](#jdk)** - *ohjelmistokehityspaketti*, joka sisältää
  muun muassa Java-kääntäjän sekä virtuaalikoneen Java-ohjelmien ajamista
  varten. 

- **[Git](#git)** - *versiohallintaohjelma* (engl. Version Control Software, VCS), joka
  mahdollistaa koodin versioinnin ja yhteistyön koodaajien välillä.

- **[IntelliJ IDEA](#idea)** - *integroitu kehitysympäristö* (engl. Integrated
  Development Environment, IDE), jolla voi kehittää ja debugata muun muassa
  Java-ohjelmia. IntelliJ IDEA on maksuton: JetBrains lopetti erillisen
  Community Edition -version vuoden 2025 lopussa, ja nykyinen yhtenäinen
  IntelliJ IDEA on ilmainen ilman erillistä aktivointia tai kirjautumista.

- **[SceneBuilder](#scenebuilder)** - aputyökalu JavaFX-käyttöliittymien luomiseksi.

- **[ComTest](#comtest)** - työkalu *dokumentaatiotestien* kirjoittamiselle ja ajamiselle.


Yllä olevat ohjelmat löytyvät valmiiksi asennettuna [Agoran
mikroluokissa](https://navi.jyu.fi/space/m118987) (Alban puoleinen pääty,
ensimmäinen ja toinen kerros). Jos sinulla on oma tietokone, suosittelemme
vahvasti, että asennat ohjelmat myös siihen. Erityisesti harjoitustyön tekeminen
on helpompaa, kun kaikki tarvittavat ohjelmat on myös omalla tietokoneella.

> [!TÄRKEÄÄ]
>
> Tämän sivun ohjeet vaativat komentorivin käyttöä. Voit tarvittaessa kerrata komentorivin perusteita seuraavista linkeistä:
>
> - [OpenCS: Johdatus komentorivin käyttöön](https://opencs.it.jyu.fi/cli-intro/)
> - [Ohjelmointi 1: Pikakurssi komentorivin käyttöön](https://tim.jyu.fi/view/kurssit/tie/itkp102/ohjeet/tyokalut#pikakurssi-komentorivin-k%C3%A4ytt%C3%B6%C3%B6n)


Kurssilla virallisesti tuettuja käyttöjärjestelmiä ovat Windows, macOS ja Linux.
Työkalujen asentaminen ChromeOS:ään saattaa olla mahdollista, mutta emme valitettavasti voi tarjota tukea kyseiseen käyttöjärjestelmään. 
Tästä syystä emme suosittele ChromeOS:n käyttöä.

Valitse käyttöjärjestelmäsi alta:

### [Windows](#tab/win)

Alla olevat ohjeet on testattu seuraavilla käyttöjärjestelmillä:

- Windows 11
- Windows 10 (käyttöjärjestelmän version on oltava vähintään 1809)

> [!HUOMAUTUS]
>
> Microsoftin tuki Windows 10:lle päättyi 14.10.2025, eikä käyttöjärjestelmä saa
> enää tietoturvapäivityksiä. Suosittelemme päivittämään Windows 11:een.

Näet käyttöjärjestelmän version suorittamalla seuraava komento PowerShell-komentorivillä:

```bash
winver
```

***

### [macOS](#tab/macos)

Alla olevat ohjeet on testattu seuraavilla käyttöjärjestelmillä:

- macOS 15 Sequoia

Ohjeiden pitäisi toimia myös uudemmissa macOS-versioissa (macOS 26 Tahoe).

***

### [Linux](#tab/linux)

Alla olevat ohjeet on testattu seuraavilla käyttöjärjestelmillä:

- Arch Linux (`6.17.7-arch1-1`)
- CachyOS Linux (`6.18.2-2-cachyos`)
- Linux Mint 22.2 (`6.14.0-37-generic`)

***

### [Valitse](#tab/default)

Valitse käyttöjärjestelmäsi yllä olevista vaihtoehdoista.

***

## Esivalmistelut

### [Windows](#tab/win)

Jos Windows Updatessa on saatavilla käyttöjärjestelmäpäivityksiä, asenna ne.

Varmista sen jälkeen, että tietokoneellasi on `winget`-pakkaushallintaohjelma asennettuna:

1. Avaa PowerShell-komentorivi (*Haku-ikoni* <i class="bi bi-chevron-right"></i> *Kirjoita PowerShell* <i class="bi bi-chevron-right"></i> *Windows PowerShell*).
2. Anna seuraava komento:

    ```bash
    winget -v
    ```

    Tuloksena pitäisi tulostua `winget`-työkalun versio. Jos sen sijaan saat virheen, jossa
    lukee *'winget' is not recognized as the name of a cmdlet, function, script file, or operable program*,
    tarkoittaa tämä, että sinulla todennäköisesti ei ole `winget`-työkalua asennettuna.
    Jos käyttöjärjestelmän päivitys ei auta, kokeile seuraavia ratkaisuja:
    
    - Tarkista, että käyttöjärjestelmäsi on ajan tasalla (katso yhteensopivat käyttöjärjestelmäversiot ylempänä).
    - Kokeile ladata ja asentaa `winget`-käsin: [Lataa asennusohjelma](https://github.com/microsoft/winget-cli/releases/latest/download/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle)
      Asennuksen jälkeen sulje ja käynnistä PowerShell uudelleen.

***

### [macOS](#tab/macos)

Varmista ensin, että tietokoneesi on ajan tasalla.

Varmista sen jälkeen, että tietokoneellasi on Homebrew-pakkaushallintaohjelma asennettuna:

1. Avaa Pääte tai Terminal (*Launchpad* <i class="bi bi-chevron-right"></i> *Pääte/Terminal*)
2. Anna seuraava komento:

    ```bash
    brew --version
    ```

Jos saat virheen `command not found: brew`,
sinun tulee asentaa Homebrew alla olevilla ohjeilla:

<details>
<summary>Homebrew-työkalun asennusohjeet (Avaa klikkaamalla)</summary>

1. Avaa Pääte tai Terminal (*Launchpad* <i class="bi bi-chevron-right"></i> *Pääte/Terminal*)
2. Asenna ensin macOS:n kehitystyökalut suorittamalla alla oleva komento:

    ```bash
    xcode-select --install
    ```
    
    Saatat nyt saada seuraavanlaisen ilmoituksen:
    *Komento "xcode-select" vaatii komentorivikehitystyökalut. Haluatko asentaa työkalut nyt?*
    (Englanniksi: *The 'xcode-select' command requires the command line developer tools. Would you like to install the tools now?*)
    
    Jos tällainen ilmoitus ilmestyy, valitse *Asenna*/*Install* ja odota työkalujen asentumista.
    Hyväksy tarvittaessa käyttöehdot.
    Kun asennus on valmis, saat *Ohjelmisto asennettiin*/*The software was installed* -dialogin.
    Klikkaa silloin *Valmis*.
    
    Jos saat virheen, jossa lukee `command line tools are already installed`, sinulla
    on jo tarvittavat työkalut asennettuna ja voit jatkaa seuraavaan vaiheeseen.  
3. Asenna Homebrew-ohjelmahallintatyökalu seuraavalla komennolla:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
    
    *Anna työkalun latautua rauhassa.*
    
    Kirjoita macOS-käyttäjäsi salasana, kun *Password*-kenttä ilmestyy.
    *Huomaa, että salasanan kirjoittaminen ei tuota mitään näkyvää tulostetta komentoriville,
    ei edes `*`-merkkejä.* Paina Enter-painiketta, kun olet kirjoittanut salasanan.
    
    Ennen asennusta Homebrew vielä tulostaa varmistusdialogin, jonka lopussa lukee
    
    ```
    Press RETURN/ENTER to continue or any other key to abort:
    ```
    
    Paina siinä tapauksessa Enter-näppäintä ja odota ohjelman asentumista.
4. Kopioi ja suorita seuraavat komennot (huom: kopioi kaikki neljä riviä kerralla)

    ```bash
    BREW_PREFIX=$( [[ $(uname -m) == arm64 ]] && echo /opt/homebrew || echo /usr/local )
    echo >> ~/.zprofile
    echo "eval \"\$(${BREW_PREFIX}/bin/brew shellenv)\"" >> ~/.zprofile
    eval "$(${BREW_PREFIX}/bin/brew shellenv)"
    ```
5. Testaa, että Homebrew toimii suorittamalla komento:

    ```bash
    brew --version
    ```
    
    Jos asennus suoritettiin onnistuneesti, näet seuraavanlaisen tulosteen:
    
    ```
    Homebrew X.X.X
    ```
    
    Versionumero `X.X.X` voi olla mikä tahansa; olennaista on, että tuloste ilmestyy näkyviin.
</details>

***

### [Linux](#tab/linux)

Alla olevissa ohjeissa oletetaan, että sinulla on kokemusta ohjelmien asentamisesta
käyttämälläsi Linux-jakelulla.
Linux-ohjeet toimivat täten ohjenuorana; käytä tarvittaessa omaa harkintaa.

Ota huomioon seuraavat asiat seuratessa ohjeita:

- Vaikka osa työkaluista löytyy jakelujen omasta pakkaustenhallinnasta, kaikkia
   graafisia ohjelmia (erityisesti IntelliJ IDEA ja SceneBuilder) ei ole yleensä
   julkaistu jakelukohtaisissa repoissa.
   *Suosittelemme* käyttämään jakelusta riippumatonta pakkaustenhallintaa, 
   kuten [Snap](https://snapcraft.io/docs/installing-snapd) tai [Flatpak](https://flatpak.org/).
   
   Tällä sivulla olevat ohjeet käyttävät ensisijaisesti Snapia tai jakelukohtaisia
   pakkauksia, jos niitä on. Linux Mint-jakelulle saat Snapin asennettua [jakelun ohjetta](https://linuxmint-user-guide.readthedocs.io/en/latest/snap.html#how-to-install-the-snap-store-in-linux-mint-20) seuraamalla.

- Kun olet asentanut tarvittavat esipakkaukset, käynnistä uusi tyhjä pääte.

***

### [Valitse](#tab/default)

Valitse käyttöjärjestelmäsi yllä olevista vaihtoehdoista.

***

## Git {#git}

### [Windows](#tab/win)

Tarkista ensin, onko sinulla jo Git asennettuna.

1. Avaa PowerShell-komentorivi.
2. Kokeile, onko Git jo valmiiksi asennettu suorittamalla komento:

    ```bash
    git --version
    ```

    
Jos näet git-työkalun version (esim. `git version X.XX.XX`, jossa `X.XX.XX` on työkalun tarkka versio),
**voit ohittaa Git-työkalun asennusohjeen kokonaan.**

Jos saat tuloksena virheen, että komentoa ei löydy, jatka alla olevilla ohjeilla.

<details>
<summary>Git-työkalun asennusohjeet (Avaa klikkaamalla)</summary>

1. Avaa PowerShell-komentorivi.
2. Asenna Git for Windows suorittamalla alla oleva komento:

    ```bash
    winget install -e --id=Git.Git --custom '/COMPONENTS="ext,ext\shellhere,ext\guihere"'
    ```
    
    Odota komennon suorittamista loppuun ja anna tarvittaessa asennusoikeus.
    Jos näet komentorivillä kysymyksen, kuten:
    
    ```
    Do you agree to all the source agreements terms?
    [Y] Yes [N] No:
    ```
    
    Paina komentorivillä `y`-näppäintä ja sen jälkeen `Enter`-näppäintä.
    
    Tarkista lopuksi, että komentorivillä olevassa tulosteessa on teksti `Successfully installed`.
    
3. Sulje kaikki auki olevat komentorivit ja avaa uusi PowerShell-komentorivi
4. Testaa, että `git`-komento on asennettu suorittamalla komento:

    ```bash
    git --version
    ```
    
    Jos asennus onnistui, näet seuraavanlaisen tulosteen:
    
    ```
    git version X.XX.XX
    ```
    
    Tekstin `X.XX.XX` tilalla näkyy git-työkalun tarkka versio.

5. Testaa, vielä, että Git Bash on asennettu. Mene *Haku-ikoni* <i class="bi bi-chevron-right"></i> Kirjoita *Git Bash* <i class="bi bi-chevron-right"></i> Valitse *Git Bash*.

    Jos kaikki toimii, pitäisi avautua Git Bash -komentorivi:

    ![](images/git-bash-windows.png)

</details>

***

### [macOS](#tab/macos)

Tarkista ensin, onko sinulla jo Git asennettuna.

1. Avaa Pääte.
2. Kokeile, onko Git jo valmiiksi asennettu suorittamalla komento:

    ```bash
    git --version
    ```

    
Jos saat tuloksena virheen, että komentoa ei löydy, jatka alla olevilla ohjeilla.

<details>
<summary>Git-työkalun asennusohjeet (Avaa klikkaamalla)</summary>

1. Avaa Pääte.
2. Git-työkalun pitäisi olla jo valmiiksi asennettu jos teit Valmistelu-vaiheessa olevat asiat. Tarkista, että Git toimii suorittamalla seuraava komento:

    ```bash
    git --version
    ```
    
    Jos asennus onnistui, näet seuraavanlaisen tulosteen:
    
    ```
    git version X.XX.XX
    ```
    
    Tekstin `X.XX.XX` tilalla näkyy git-työkalun tarkka versio.

</details>

***

### [Linux](#tab/linux)

Tarkista ensin, onko sinulla jo Git asennettuna.

1. Avaa jakelusi pääteohjelma.
2. Kokeile, onko Git jo valmiiksi asennettu suorittamalla komento:

    ```bash
    git --version
    ```

    
Jos näet git-työkalun version (esim. `git version X.XX.XX`, jossa `X.XX.XX` on työkalun tarkka versio),
**voit ohittaa Git-työkalun asennusohjeen kokonaan.**

Jos taas näet virheen, että komentoa ei löydy, jatka alla olevilla ohjeilla.

<details>
<summary>Git-työkalun asennusohjeet (Avaa klikkaamalla)</summary>

1. Avaa jakelusi pääteohjelma.
2. Asenna Git-pakkaus: `git`. Pakkauksen nimi on yleensä sama
   kaikissa yleisillä jakeluissa (Ubuntu, Debian, Fedora, Arch, jne.)
3. Asennuksen jälkeen sulje ja avaa pääte uudelleen
4. Testaa, että `git`-komento on asennettu suorittamalla komento:

    ```bash
    git --version
    ```
    
    Jos asennus onnistui, näet seuraavanlaisen tulosteen:
    
    ```
    git version X.XX.XX
    ```
    
    Tekstin `X.XX.XX` tilalla näkyy git-työkalun tarkka versio.

</details>

***

### [Valitse](#tab/default)

Valitse käyttöjärjestelmäsi yllä olevista vaihtoehdoista.

***

## IntelliJ IDEA {#idea}

### [Windows](#tab/win)

1. Avaa PowerShell-komentorivi.
2. Asenna IntelliJ IDEA suorittamalla alla oleva komento:

    ```bash
    winget install --interactive -e --id=JetBrains.IntelliJIDEA
    ```

    Ohjelman lataamisen jälkeen avautuu asennusohjelma.
    Etene asennusohjelmassa eteenpäin *Next*-painikkeella.
    Kohdassa *Installation Options* valitse seuraavat ruksit päälle:
    
    - Add "Open Folder as Project"
    - Create Associations: .java, .gradle, .kt
    
    Etene asennusohjelmassa ja anna ohjelman asentua. 
3. Kun pääset asennusohjelman loppuun, valitse *Run IntelliJ IDEA* ja paina *Finish*.
   Testaa, että ohjelma toimii.

    Ensimmäisellä kerralla käynnistys saattaa kestää, sillä järjestelmä tarkistaa sovelluksen.
    Hyväksy mahdolliset IDEAn käyttöehdot.

4. Jos sinulla on jo jokin muu kehitysympäristö asennettuna (JetBrains Rider tai Visual Studio Code),
   IDEA saattaa kysyä, haluatko tuoda (engl. *import*) asetuksia niistä. Voit 
   halutessasi tuoda asetukset, voit tehdä asetukset myös myöhemmin ja painaa *Skip Import*.

5. Kun asennus on valmis, sinulla pitäisi näkyä *Welcome to IntelliJ IDEA* -ikkuna.

6. Kytke lopuksi IDEAn tekoälyavustukset pois päältä kohdan [IDEAn
   tekoälyavustusten kytkeminen pois päältä](#idea-ai) ohjeiden mukaisesti.

Valmis!

***

### [macOS](#tab/macos)

1. Avaa Pääte.
2. Asenna IntelliJ IDEA suorittamalla alla oleva komento:

    ```bash
    brew install --cask intellij-idea
    ```

    Anna asennuksen suoriutua loppuun asti. Sinulta saatetaan pyytää
    macOS-käyttäjän salasanaa `Password:`-kentässä. Kirjoita silloin
    salasana paikalle ja paina <kbd>Enter</kbd>.

3. Tarkista, että IntelliJ IDEA toimii. Avaa Launchpad ja käynnistä sieltä *IntelliJ IDEA*.

    Ensimmäisellä kerralla käynnistys saattaa kestää, sillä järjestelmä tarkistaa sovelluksen.
    Järjestelmä saattaa myös kysyä, *IntelliJ IDEA on internetistä ladattu appi. Avataanko se?*.
    Siinä tapauksessa voi valita *Avaa*.
    
    Hyväksy mahdolliset IDEAn käyttöehdot.

4. Jos sinulla on muu kehitysympäristö asennettuna (JetBrains Rider tai Visual
   Studio Code), IntelliJ IDEA saattaa kysyä, haluatko tuoda (engl. *import*)
   asetuksia niistä. Paina *Skip Import*. IDEAan asetetaan erilliset asetukset
   myöhemmin.

5. Kun asennus on valmis, sinulla pitäisi näkyä *Welcome to IntelliJ IDEA* -ikkuna.

6. Kytke lopuksi IDEAn tekoälyavustukset pois päältä kohdan [IDEAn
   tekoälyavustusten kytkeminen pois päältä](#idea-ai) ohjeiden mukaisesti.

Valmis!

***

### [Linux](#tab/linux)

1. Avaa jakelusi pääteohjelma.
2. Asenna IntelliJ IDEA. Asennustapa vaihtelee jakelun mukaan:

    - Arch: Asenna [`intellij-idea-community-edition`](https://archlinux.org/packages/extra/x86_64/intellij-idea-community-edition/)-pakkaus.
      Pakkauksen nimessä on yhä vanha *Community Edition* -nimi, mutta se sisältää
      nykyisen yhtenäisen IntelliJ IDEAn.

      ```bash
      sudo pacman -S intellij-idea-community-edition
      ```

    - Muut jakelut: Suosittelemme asentamaan [IDEA-snapin](https://snapcraft.io/intellij-idea) käyttäen `snap`-pakkaustenhallintaa:

        ```bash
        sudo snap install intellij-idea --classic
        ```
        
        Vaihtoehtoisesti voit asentaa IntelliJ:n käsin seuraamalla [virallisia asennusohjeita](https://www.jetbrains.com/help/idea/installation-guide.html#standalone_linux)

3. Tarkista, että IntelliJ IDEA toimii. Käynnistä JetBrains IntelliJ IDEA (joko sovellusvalikosta tai `idea`-komennolla).
    
    Hyväksy mahdolliset IDEAn käyttöehdot.

4. Jos sinulla on muu kehitysympäristö asennettuna (JetBrains Rider tai Visual
   Studio Code), IntelliJ IDEA saattaa kysyä, haluatko tuoda (engl. *import*)
   asetuksia niistä. Paina *Skip Import*. IDEAan asetetaan erilliset asetukset
   myöhemmin.

5. Kun asennus on valmis, sinulla pitäisi näkyä *Welcome to IntelliJ IDEA* -ikkuna.

6. Kytke lopuksi IDEAn tekoälyavustukset pois päältä kohdan [IDEAn
   tekoälyavustusten kytkeminen pois päältä](#idea-ai) ohjeiden mukaisesti.

Valmis!

***

### [Valitse](#tab/default)

Valitse käyttöjärjestelmäsi yllä olevista vaihtoehdoista.

***

## IDEAn tekoälyavustusten kytkeminen pois päältä {#idea-ai}

IDEAssa on parikin erilaista tekoälypohjaista täydennysominaisuutta: *AI
Assistant* ja *Inline Completion*. Näiden avulla ympäristö yrittää täydentää
kirjoitettua koodia.

Voit kytkeä nämä ominaisuudet pois päältä seuraavasti.

1. AI Assistantin kytkeminen pois
   - Settings <i class="bi bi-chevron-right"></i> Plugins
   - Valitse Installed-välilehti
   - Etsi *JetBrains AI Assistant* ja poista plugin käytöstä (Disable) tai poista se kokonaan (Uninstall)
2. Inline Completion -täydennyksen kytkeminen pois
   - Avaa IntelliJ IDEA *Welcome to IntelliJ IDEA* -näkymään
   - Klikkaa vasemmassa alalaidassa olevaa rattaan kuvaketta <i class="bi bi-chevron-right"></i> Settings
   - Mene asetuksissa kohtaan Editor <i class="bi bi-chevron-right"></i> General
     <i class="bi bi-chevron-right"></i> Code Completion <i class="bi bi-chevron-right"></i> Inline
   - Ota ruksi **pois** kohdasta *Enable inline completion using language models*
   - Tallenna asetukset *OK*-painikkeella
   - Voit halutessasi poistaa myös *Full Line Code Completion* -pluginin
     käytöstä kohdassa Settings <i class="bi bi-chevron-right"></i> Plugins

## Java Development Kit (JDK) {#jdk}


> 1. Avaa IntelliJ IDEA ja odota, kunnes pääset *Welcome to IntelliJ IDEA* -näkymään.
>
> 
> 2. Klikkaa ikkunan keskellä tai ylälaidassa olevaa *New Project* -painiketta:
> 
>     ![](images/intellij-welcome.jpg)
> 
> 3. Avautuneesta ikkunasta klikkaa *JDK*-alasvetolaatikkoa ja valitse *Download JDK...* -painike:
> 
>     ![](images/intellij-jdk.jpg)
> 
> 4. Aseta avautuneessa ikkunassa asetukset seuraavasti:
> 
>     - **Version:** 25
>     - **Vendor:** Oracle OpenJDK
>     
>     *Älä muuta Location-kohdassa olevaa polkua!*
> 
>     Paina lopuksi **Select**-painiketta.
> 
>     ![](images/intellij-jdk-download.jpg)
> 
> 5. Jätä muut projektin asetukset sellaiseksi kuin ne ovat. Paina oikeassa alalaidassa olevaa **Create**-painiketta ja anna projektin latautua.
> 
>     Tämä avaa IntelliJ IDEA -kehitysympäristön käyttöliittymän.
> 
>     JDK:n lataamisessa voi mennä aikaa. Odota rauhassa, kunnes kaikki virheet ja punaiset tekstit häviää.
> 
> 6. Kun projekti on latautunut eikä virheitä näy, kokeile ajaa projekti painamalla oikeassa ylälaidassa olevaa *Play*-painiketta:
> 
>     ![](images/intellij-play.jpg)
> 
> 7. Odota, kunnes ohjelma kääntyy. Jos kaikki toimii, ikkunan alapuolelle pitäisi ilmestyä konsoli-ikkuna, jossa näet seuraavan tekstin:
> 
> 
>     ```text
>     Hello and welcome!
>     i = 1
>     i = 2
>     i = 3
>     i = 4
>     i = 5
>     ```
> 
> 8. Voit nyt sulkea IntelliJ IDEA:n.


## SceneBuilder {#scenebuilder}

### [Windows](#tab/win)

1. Avaa PowerShell-komentorivi.
2. Asenna SceneBuilder suorittamalla alla oleva komento:

    ```bash
    winget install -e --id=Gluon.SceneBuilder
    ```
    
    Odota komennon suorittamista loppuun ja anna tarvittaessa asennusoikeus.
    Jos näet komentorivillä kysymyksen, kuten:
    
    ```
    Do you agree to all the source agreements terms?
    [Y] Yes [N] No:
    ```
    
    Paina komentorivillä `y`-näppäintä ja sen jälkeen `Enter`-näppäintä.
    
    Tarkista lopuksi, että komentorivillä olevassa tulosteessa on teksti `Successfully installed`.


3. Testaa, että SceneBuilder toimii. Mene *Haku-ikoni* <i class="bi bi-chevron-right"></i> Kirjoita *SceneBuilder* <i class="bi bi-chevron-right"></i> Valitse *SceneBuilder*.
   
    Varmista, että ohjelma käynnistyy.

4. Sulje ohjelma.

Valmis!

***

### [macOS](#tab/macos)

1. Avaa Pääte.
2. Asenna SceneBuilder suorittamalla alla oleva komento:

    ```bash
    brew install --cask scenebuilder
    ```

    Anna asennuksen suoriutua loppuun asti. Sinulta saatetaan pyytää
    macOS-käyttäjän salasanaa `Password:`-kentässä. Kirjoita silloin
    salasana paikalle ja paina <kbd>Enter</kbd>.

3. Tarkista, että SceneBuilder toimii. Avaa Launchpad ja käynnistä sieltä *SceneBuilder*.

    Tämän pitäisi käynnistää SceneBuilder-ohjelma.

4. Sulje SceneBuilder.

Valmis!

***

### [Linux](#tab/linux)

1. Avaa jakelusi pääteohjelma.
2. Asenna SceneBuilder. Asennustapa vaihtelee jakelun mukaan:

    - Arch: Asenna [`javafx-scenebuilder`](https://aur.archlinux.org/packages/javafx-scenebuilder)-pakkaus AUR:sta.
      Voit asentaa sen käsin tai käyttämällä [yay](https://github.com/Jguer/yay)-työkalua:
      
      ```bash
      yay -S javafx-scenebuilder
      ```

    - Flatpak: Asenna työkalu komennolla 
    
        ```bash
        flatpak install flathub com.gluonhq.SceneBuilder
        ```
      
    - Muut jakelut: Suosittelemme lataamaan virallisen `.rpm`- tai
      `.deb`-asennustiedoston [SceneBuilderin
      sivuilta](https://gluonhq.com/products/scene-builder/#download).
      
        `.deb`-tiedoston asennus (Debian, Ubuntu, Linux Mint) onnistuu esimerkiksi `dpkg`-komennolla:

        ```
        sudo dpkg -i tiedosto.deb
        ```

        vastaavasti `.rpm`-tiedoston asennus (Fedora, CentOS) onnistuu `rpm`-komennolla:
    
        ```bash
        sudo rpm -i tiedosto.rpm
        ```

3. Tarkista, että SceneBuilder toimii. Käynnistä SceneBuilder (joko sovellusvalikosta tai `scenebuilder`-komennolla).
    
    Sulje ohjelma.

Valmis!

***

### [Valitse](#tab/default)

Valitse käyttöjärjestelmäsi yllä olevista vaihtoehdoista.

***


## ComTest {#comtest}

> 1. Avaa IntelliJ IDEA ja odota, kunnes pääset *Welcome to IntelliJ IDEA* -näkymään.
>
>    **Jos sinulle avautui jokin vanha projekti**, klikkaa yläpalkista tai hampurilaisvalikosta *File* <i class="bi bi-chevron-right"></i> *Close project*. Tämä vie sinut takaisin *Welcome to IntelliJ IDEA* -näkymään.
>
> 2. Klikkaa ikkunan vasemmassa alalaidassa olevaa rattaan kuvaketta <i class="bi bi-chevron-right"></i> *Settings*.
>
> 3. Valitse vasemmalla puolella olevista asetusnäkymistä *Plugins*
>
> 4. Valitse *Marketplace*-välilehti ja hae hakusanalla `ComTest`
>
> 5. Valitse Comtest Runner -pluginin kohdalta *Install*
>
>       ![](images/rider-install-comtest.gif)
>
>       *Kuvakaappaus on JetBrains Riderista, mutta vaiheet ovat IntelliJ IDEAssa samat.*
>
> 6. Paina *OK*
>
> 7. Sulje IntelliJ IDEA


## Mitä seuraavaksi?

Onneksi olkoon! Sinulla on seuraavaksi kaikki tarvittavat kurssityökalut. Voit jatkaa tästä varsinaisiin materiaaleihin.

## Yleiset ongelmat ja ratkaisut

<details>
<summary>Saan IDEAssa Java-projektia ajaessa virheen <code>error: illegal character: '\ufeff'</code> </summary>

Virhe voi mahdollisesti johtua siitä, että toit Rider-työkalun asetukset
IDEAan. Riderin asetukset eivät ole täysin yhteensopivia Javan kehityksen kanssa
eikä IDEA osaa korjata ongelmaa.

Tee seuraavasti:

1. Avaa IntelliJ IDEA ja odota, kunnes pääset *Welcome to IntelliJ IDEA* -näkymään.
  
   **Jos sinulle avautui jokin vanha projekti**, klikkaa yläpalkista tai hampurilaisvalikosta *File* <i class="bi bi-chevron-right"></i> *Close project*. Tämä vie sinut takaisin *Welcome to IntelliJ IDEA* -näkymään.

2. Klikkaa ikkunan vasemmassa alalaidassa olevaa rattaan kuvaketta <i class="bi bi-chevron-right"></i> *Settings*.

3. Valitse vasemmalla puolella olevista asetusnäkymistä *Editor* <i class="bi
   bi-chevron-right"></i> *File Encodings*

4. Aseta *Create UTF-8 files* -asetuksen arvoksi **with no BOM**.

5. Paina *OK*.

6. Tee *uusi* projekti ja kokeile ajaa yksinkertainen ohjelma.

</details>

<details>
<summary>Internal error: com.intellij.platform.ide.bootstrap... Process "C:\...idea64.exe" is still running and does not respond</summary>

Tämä virhe voi johtua siitä, että Rider on jostain syystä jumittunut taustaprosessina
käyttöjärjestelmässä. 

 1. Sulje IntelliJ IDEA kokonaan.
 2. Avaa Rider.
 3. Sulje Rider.
 4. Käynnistä IntelliJ IDEA uudelleen.

</details>
