/* Koesivun osa1/vaiheet.md kohtaukset (tests/test_walkthrough.py). */

(window.jyuWalkScenes ??= []).push((ui) => {
  const session = [
    { cwd: "~", cmd: "cd koe" },
    { cwd: "~/koe", branch: "main", cmd: "git status", out: ["On branch main", ["green", "\tnew file:   a.txt"]] },
  ];

  return {
    selain: () => ui.browser({
      title: "Koe",
      url: "https://example.invalid/",
      typeUrl: true,
      body: '<p class="koe-teksti" data-type>Hei</p>'
        + '<p><span class="jw-btn koe-nappi" data-click data-on="jw-on" data-ring>OK</span></p>',
    }),

    komento: () => ui.gitBash({ session, from: 0, to: 2 }),

    piilotus: () => ui.window({
      title: "Ikkuna",
      body: '<div class="koe-ikkuna" data-show data-order="1" data-hide="5">Ikkuna</div>'
        + '<div class="koe-lopuksi" data-show data-order="9">Valmis</div>'
        + '<div style="height:40px;overflow:hidden"><div class="koe-vieritys" data-scroll="40" data-order="7">'
        + "<div style=\"height:40px\">Yksi</div><div style=\"height:40px\">Kaksi</div></div></div>",
    }),

    /* Yksittäinen animaatio (<animation>) samalla sivulla. */
    animaatio: () => ui.window({
      title: "Animaatio",
      body: '<p class="koe-anim-teksti" data-type>Moi</p>'
        + '<p><span class="jw-btn koe-anim-nappi" data-click data-on="jw-on" data-ring>OK</span></p>',
    }),
  };
});
