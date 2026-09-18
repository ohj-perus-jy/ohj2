"""Vaiheittaisen ohjeen äänet pilvipalvelun puhesynteesillä (Azure Speech).

    ./run.sh puhe ../src/git-ht-ohje.md            # puuttuvat ja vanhentuneet
    ./run.sh puhe ../src/git-ht-ohje.md --teksti   # luettavat tekstit, ei ääniä

Sivun <walkthrough scenes="..." audio="kansio"> kertoo kansion (lähteen
sivun hakemistosta). Jokaisesta vaiheesta tulee sinne <kohtaus>.mp3, ja
puhe.json muistaa, millä äänellä ja mistä tekstistä (tiiviste) kukin on tehty.
Ääni tehdään vain uudelle tai muuttuneelle vaiheelle, joten tekstin
korjaamisen jälkeinen ajo on halpa. Luettava teksti on convert.py:n
walkthrough_speech: sama, josta käännös tarkistaa, onko ääni ajan tasalla,
ja jättää vanhentuneen äänen pois.

Avain ja alue ympäristömuuttujista AZURE_SPEECH_KEY ja AZURE_SPEECH_REGION
(Azure-portaalissa Speech-resurssin Keys and Endpoint -sivulta). Avainta ei
tallenneta mihinkään.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from html import escape
from pathlib import Path

import convert

VOICE = "fi-FI-HarriNeural"

# Puhe on kapeakaistaista: 48 kbit/s mono on noin 6 kt sekunnissa.
FORMAT = "audio-24khz-48kbitrate-mono-mp3"


def ssml(text: str, voice: str = VOICE) -> str:
    """Luettava teksti SSML:ksi: jokainen rivi omana kappaleenaan (tauko)."""
    paragraphs = "".join(f"<p>{escape(line, quote=False)}</p>"
                         for line in text.split("\n") if line)
    return ('<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"'
            f' xml:lang="fi-FI"><voice name="{escape(voice)}">{paragraphs}</voice></speak>')


def azure(document: str) -> bytes:
    """SSML-dokumentti Azure Speechin REST-rajapinnalla MP3:ksi."""
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        raise SystemExit("aseta ympäristömuuttujat AZURE_SPEECH_KEY ja AZURE_SPEECH_REGION "
                         "(Azure-portaali: Speech-resurssi, Keys and Endpoint)")
    request = urllib.request.Request(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1",
        data=document.encode("utf-8"),
        headers={
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": FORMAT,
            "User-Agent": "ohj2-puhe",
        })
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def refresh(page: Path, synthesize: Callable[[str], bytes] = azure, voice: str = VOICE,
            log: Callable[[str], None] = print) -> list[str]:
    """Tee sivun puuttuvat ja vanhentuneet äänet. -> tehtyjen vaiheiden kohtaukset.

    Luettelo kirjoitetaan jokaisen äänen jälkeen, jotta keskeytynyt ajo ei tee
    valmiita uudelleen. Poistuneiden vaiheiden äänet poistetaan. Äänen vaihto
    tekee kaikki uudelleen.
    """
    audio, speech = convert.walkthrough_speech(page.read_text(encoding="utf-8"))
    if audio is None:
        raise SystemExit(f"{page}: <walkthrough>-tagissa ei ole audio-attribuuttia")
    folder = page.parent / audio
    manifest = folder / convert.SPEECH_MANIFEST
    try:
        previous = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        previous = {}
    made = previous.get("steps", {}) if previous.get("voice") == voice else {}
    current = {scene: digest for scene, digest in made.items() if scene in speech}
    folder.mkdir(parents=True, exist_ok=True)

    def save() -> None:
        manifest.write_text(json.dumps({"voice": voice, "steps": dict(sorted(current.items()))},
                                       ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    done: list[str] = []
    for scene, text in speech.items():
        digest = convert.speech_hash(text)
        file = folder / f"{scene}.mp3"
        if current.get(scene) == digest and file.is_file():
            continue
        log(f"{scene}: {len(text)} merkkiä")
        file.write_bytes(synthesize(ssml(text, voice)))
        current[scene] = digest
        done.append(scene)
        save()
    for file in folder.glob("*.mp3"):
        if file.stem not in speech:
            file.unlink()
            log(f"{file.stem}: vaihe poistunut, ääni poistettu")
    save()
    return done


def main() -> int:
    parser = argparse.ArgumentParser(description="Vaiheittaisen ohjeen äänet (Azure Speech)")
    parser.add_argument("page", type=Path, help="lähteen sivu, esim. ../src/git-ht-ohje.md")
    parser.add_argument("--teksti", action="store_true",
                        help="näytä vaiheiden luettavat tekstit tekemättä ääniä")
    parser.add_argument("--voice", default=VOICE, help=f"Azuren ääni (oletus {VOICE})")
    args = parser.parse_args()
    if args.teksti:
        _, speech = convert.walkthrough_speech(args.page.read_text(encoding="utf-8"))
        for scene, text in speech.items():
            print(f"[{scene}]\n{text}\n")
        return 0
    try:
        done = refresh(args.page, voice=args.voice)
    except urllib.error.HTTPError as error:
        print(f"puhepalvelu vastasi {error.code}: {error.read().decode(errors='replace')}",
              file=sys.stderr)
        return 1
    print(f"tehty {len(done)} ääntä" if done else "äänet ovat ajan tasalla")
    return 0


if __name__ == "__main__":
    sys.exit(main())
