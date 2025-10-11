const PLAYGROUND_LANG = "java";


function get_playgrounds() {
    return Array.from(document.querySelectorAll(`pre:has(> .language-${PLAYGROUND_LANG}:not(.noplayground))`));
}

(function codeSnippets() {
    function fetch_with_timeout(url, options, timeout = 6000) {
        return Promise.race([
            fetch(url, options),
            new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), timeout)),
        ]);
    }

    const playgrounds = get_playgrounds();
    if (playgrounds.length > 0) {
        fetch_with_timeout('https://play.rust-lang.org/meta/crates', {
            headers: {
                'Content-Type': 'application/json',
            },
            method: 'POST',
            mode: 'cors',
        })
            .then(response => response.json())
            .then(response => {
            // get list of crates available in the rust playground
                const playground_crates = response.crates.map(item => item['id']);
                playgrounds.forEach(block => handle_crate_list_update(block, playground_crates));
            });
    }

    function handle_crate_list_update(playground_block, playground_crates) {
        // update the play buttons after receiving the response
        update_play_button(playground_block, playground_crates);

        // and install on change listener to dynamically update ACE editors
        if (window.ace) {
            const code_block = playground_block.querySelector('code');
            if (code_block.classList.contains('editable')) {
                const editor = window.ace.edit(code_block);
                editor.addEventListener('change', () => {
                    update_play_button(playground_block, playground_crates);
                });
                // add Ctrl-Enter command to execute rust code
                editor.commands.addCommand({
                    name: 'run',
                    bindKey: {
                        win: 'Ctrl-Enter',
                        mac: 'Ctrl-Enter',
                    },
                    exec: _editor => run_rust_code(playground_block),
                });
            }
        }
    }

    // updates the visibility of play button based on `no_run` class and
    // used crates vs ones available on https://play.rust-lang.org
    function update_play_button(pre_block, playground_crates) {
        const play_button = pre_block.querySelector('.play-button');

        // skip if code is `no_run`
        if (pre_block.querySelector('code').classList.contains('no_run')) {
            play_button.classList.add('hidden');
            return;
        }

        // get list of `extern crate`'s from snippet
        const txt = playground_text(pre_block);
        const re = /extern\s+crate\s+([a-zA-Z_0-9]+)\s*;/g;
        const snippet_crates = [];
        let item;
        // eslint-disable-next-line no-cond-assign
        while (item = re.exec(txt)) {
            snippet_crates.push(item[1]);
        }

        // check if all used crates are available on play.rust-lang.org
        const all_available = snippet_crates.every(function(elem) {
            return playground_crates.indexOf(elem) > -1;
        });

        if (all_available) {
            play_button.classList.remove('hidden');
        } else {
            play_button.classList.add('hidden');
        }
    }

    function run_rust_code(code_block) {
        let result_block = code_block.querySelector('.result');
        if (!result_block) {
            result_block = document.createElement('code');
            result_block.className = 'result hljs language-bash';

            code_block.append(result_block);
        }

        const text = playground_text(code_block);
        const classes = code_block.querySelector('code').classList;
        let edition = '2015';
        classes.forEach(className => {
            if (className.startsWith('edition')) {
                edition = className.slice(7);
            }
        });
        const params = {
            version: 'stable',
            optimize: '0',
            code: text,
            edition: edition,
        };

        if (text.indexOf('#![feature') !== -1) {
            params.version = 'nightly';
        }

        result_block.innerText = 'Running...';

        fetch_with_timeout('https://play.rust-lang.org/evaluate.json', {
            headers: {
                'Content-Type': 'application/json',
            },
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify(params),
        })
            .then(response => response.json())
            .then(response => {
                if (response.result.trim() === '') {
                    result_block.innerText = 'No output';
                    result_block.classList.add('result-no-output');
                } else {
                    result_block.innerText = response.result;
                    result_block.classList.remove('result-no-output');
                }
            })
            .catch(error => result_block.innerText = 'Playground Communication: ' + error.message);
    }

    const code_nodes = Array
        .from(document.querySelectorAll('code'))
        // Don't highlight `inline code` blocks in headers.
        .filter(function(node) {
            return !node.parentElement.classList.contains('header');
        });

    if (window.ace) {
        // language-LANG class needs to be removed for editable
        // blocks or highlightjs will capture events
        code_nodes
            .filter(function(node) {
                return node.classList.contains('editable');
            })
            .forEach(function(block) {
                block.classList.remove(`language-${PLAYGROUND_LANG}`);
            });
    }

    // Process playground code blocks
    playgrounds.forEach(function(pre_block) {
        // Add play button
        let buttons = pre_block.querySelector('.buttons');
        if (!buttons) {
            buttons = document.createElement('div');
            buttons.className = 'buttons';
            pre_block.insertBefore(buttons, pre_block.firstChild);
        }

        const runCodeButton = document.createElement('button');
        runCodeButton.className = 'fa fa-play play-button';
        runCodeButton.hidden = true;
        runCodeButton.title = 'Run this code';
        runCodeButton.setAttribute('aria-label', runCodeButton.title);

        buttons.insertBefore(runCodeButton, buttons.firstChild);
        runCodeButton.addEventListener('click', () => {
            run_rust_code(pre_block);
        });


        const code_block = pre_block.querySelector('code');
        if (window.ace && code_block.classList.contains('editable')) {
            const editor = window.ace.edit(code_block);
            editor.getSession().setMode("ace/mode/java");

            const undoChangesButton = document.createElement('button');
            undoChangesButton.className = 'fa fa-history reset-button';
            undoChangesButton.title = 'Undo changes';
            undoChangesButton.setAttribute('aria-label', undoChangesButton.title);

            buttons.insertBefore(undoChangesButton, buttons.firstChild);

            undoChangesButton.addEventListener('click', function() {
                const editor = window.ace.edit(code_block);
                editor.setValue(editor.originalCode);
                editor.clearSelection();
            });
        }
    });
})();