(function codeSnippets() {
    const PLAYGROUND_LANG = "java";

    function get_playgrounds() {
        return Array.from(document.querySelectorAll(`pre:has(> .language-${PLAYGROUND_LANG}:not(.noplayground))`));
    }

    function fetch_with_timeout(url, options, timeout = 6000) {
        return Promise.race([
            fetch(url, options),
            new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), timeout)),
        ]);
    }

    const playgrounds = get_playgrounds();

    function run_code(code_block) {
        let result_block = code_block.querySelector('.result');
        if (!result_block) {
            result_block = document.createElement('code');
            result_block.className = 'result hljs language-bash';

            code_block.append(result_block);
        }

        const text = playground_text(code_block);

        console.log(text);

        const params = {
            language: "java",
            code: text,
        };

        result_block.innerText = 'Running...';

        fetch_with_timeout('https://tim03.it.jyu.fi/executor/execute', {
            headers: {
                'Content-Type': 'application/json',
            },
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify(params),
        })
            .then(response => response.json())
            .then(response => {
                let result = response.errors || response.output || '';
                if (result.trim() === '') {
                    result_block.innerText = 'No output';
                    result_block.classList.add('result-no-output');
                } else {
                    result_block.innerText = result;
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
            run_code(pre_block);
        });
        

        const code_block = pre_block.querySelector('code');

        if (window.ace && code_block.classList.contains('editable')) {
            const editor = window.ace.edit(code_block);
            editor.getSession().setMode("ace/mode/java");

            // editor.addEventListener('change', () => {
            //     update_play_button(playground_block, playground_crates);
            // });
            // add Ctrl-Enter command to execute rust code

            let no_run = pre_block.querySelector('code').classList.contains('no_run');
            if (no_run) {
                runCodeButton.classList.add('hidden');
            } else {
                editor.commands.addCommand({
                    name: 'run',
                    bindKey: {
                        win: 'Ctrl-Enter',
                        mac: 'Ctrl-Enter',
                    },
                    exec: _editor => run_code(pre_block),
                });
            }
            

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