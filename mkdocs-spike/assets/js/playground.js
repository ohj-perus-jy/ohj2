/* Java-playground, portattu tiedostosta theme/playground_ext.js.
 *
 * Ajopalvelin ja pyyntömuoto ovat ennallaan; vain DOM-osa on kirjoitettu
 * uusiksi mdBookin rakenteesta (pre > code.language-java) Materialin
 * rakenteeseen (div.highlight.java.playground > pre > code). */
(function () {
    "use strict";

    var EXECUTOR = "https://lakane.it.jyu.fi/executor/execute";
    var PLAYGROUND_LANGS = ["java", "javascript"];
    var DATA_URI_PATTERN = /@@@DATA_URI_BEGIN@@@(.+)@@@DATA_URI_END@@@/g;

    var PLAY = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">'
        + '<path fill="currentColor" d="M8 5.14v14l11-7-11-7Z"/></svg>';
    var UNDO = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">'
        + '<path fill="currentColor" d="M12.5 8c-2.65 0-5.05 1-6.9 2.6L2 7v9h9l-3.62-3.62A8.03 8.03 0 0 1 '
        + '12.5 10.5c3.54 0 6.55 2.31 7.6 5.5l2.37-.78A10.02 10.02 0 0 0 12.5 8Z"/></svg>';

    function language_of(block) {
        for (var i = 0; i < PLAYGROUND_LANGS.length; i += 1) {
            if (block.classList.contains(PLAYGROUND_LANGS[i])) {
                return PLAYGROUND_LANGS[i];
            }
        }
        return null;
    }

    /* Koodin teksti. Piilotetut //- rivit otetaan mukaan, kuten mdBookissakin:
       ne ovat osa ohjelmaa, ne on vain kätketty lukijalta. */
    function code_text(block) {
        if (block.aceEditor) {
            return block.aceEditor.getValue();
        }
        var code = block.querySelector("code");
        return code ? code.textContent : "";
    }

    function tab_set_of(block) {
        return block.closest(".tabbed-block") ? block.closest(".tabbed-set") : null;
    }

    /* Monitiedostoinen esimerkki: convert.py on jakanut // FILE: -lohkot
       Materialin välilehdiksi ja merkinnyt jokaisen data-file-attribuutilla. */
    function collect_files(block) {
        var set = tab_set_of(block);
        if (!set) {
            return null;
        }
        var blocks = set.querySelectorAll(".highlight[data-file]");
        if (blocks.length < 2) {
            return null;
        }
        var files = {};
        blocks.forEach(function (one) {
            files[one.dataset.file] = code_text(one);
        });
        return files;
    }

    function result_target(block) {
        var anchor = tab_set_of(block) || block;
        var next = anchor.nextElementSibling;
        if (next && next.classList.contains("playground-result")) {
            return next;
        }
        var pre = document.createElement("pre");
        pre.className = "playground-result";
        pre.appendChild(document.createElement("code"));
        anchor.parentNode.insertBefore(pre, anchor.nextSibling);
        return pre;
    }

    function fetch_with_timeout(url, options, timeout) {
        return Promise.race([
            fetch(url, options),
            new Promise(function (_, reject) {
                setTimeout(function () {
                    reject(new Error("timeout"));
                }, timeout || 6000);
            }),
        ]);
    }

    function run_code(block) {
        var target = result_target(block);
        var output = target.querySelector("code");
        target.querySelectorAll(".result-image").forEach(function (img) {
            img.remove();
        });

        var files = collect_files(block);
        var params = {
            language: language_of(block),
            code: files ? JSON.stringify(files) : code_text(block),
            multifile: Boolean(files),
        };

        output.textContent = "Suoritetaan...";
        target.classList.remove("playground-result--empty");

        fetch_with_timeout(EXECUTOR, {
            headers: { "Content-Type": "application/json" },
            method: "POST",
            mode: "cors",
            body: JSON.stringify(params),
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (response) {
                var result = response.errors || response.output || "";
                var dataUris = result.match(DATA_URI_PATTERN);
                if (dataUris) {
                    dataUris.forEach(function (dataUri) {
                        var img = document.createElement("img");
                        img.src = dataUri
                            .replace("@@@DATA_URI_BEGIN@@@", "")
                            .replace("@@@DATA_URI_END@@@", "");
                        img.className = "result-image";
                        target.appendChild(img);
                        result = result.replace(dataUri, "");
                    });
                }
                if (result.trim() === "") {
                    output.textContent = "Ei tulostetta";
                    target.classList.add("playground-result--empty");
                } else {
                    output.textContent = result;
                }
            })
            .catch(function (error) {
                output.textContent = "Playground Communication: " + error.message;
            });
    }

    function make_button(className, icon, title) {
        var button = document.createElement("button");
        button.className = className;
        button.innerHTML = icon;
        button.title = title;
        button.setAttribute("aria-label", title);
        return button;
    }

    function decorate(block) {
        if (block.dataset.playgroundReady === "1") {
            return;
        }
        block.dataset.playgroundReady = "1";

        var runButton = make_button("playground-button play-button", PLAY, "Aja koodi");
        runButton.addEventListener("click", function () {
            run_code(block);
        });
        block.appendChild(runButton);

        var code = block.querySelector("code");
        if (window.ace && block.classList.contains("editable") && code) {
            var editor = window.ace.edit(code);
            editor.getSession().setMode("ace/mode/java");
            editor.originalCode = editor.getValue();
            block.aceEditor = editor;
            editor.commands.addCommand({
                name: "run",
                bindKey: { win: "Ctrl-Enter", mac: "Ctrl-Enter" },
                exec: function () {
                    run_code(block);
                },
            });

            var undoButton = make_button("playground-button reset-button", UNDO, "Kumoa muutokset");
            undoButton.addEventListener("click", function () {
                editor.setValue(editor.originalCode);
                editor.clearSelection();
            });
            block.appendChild(undoButton);
        }
    }

    function run() {
        document.querySelectorAll(".highlight.playground").forEach(decorate);
    }

    if (typeof document$ !== "undefined") {
        document$.subscribe(run);
    } else {
        document.addEventListener("DOMContentLoaded", run);
    }
})();
