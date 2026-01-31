(function codeSnippets() {
    const PLAYGROUND_LANGS = ["java",  "javascript"];
    const DATA_URI_PATTERN = /@@@DATA_URI_BEGIN@@@(.+)@@@DATA_URI_END@@@/g;

    function get_playgrounds() {
        return PLAYGROUND_LANGS.flatMap(lang => Array.from(document.querySelectorAll(`pre:has(> .language-${lang}:not(.noplayground):not(.ignore))`)));
    }

    function get_language(code_area) {
        // Use stored language when editable blocks have had language-* stripped.
        const data_language = code_area.dataset.language;
        if (data_language) {
            return data_language;
        }
        const code_area_classes = [...code_area.classList.values()];
        const langClass = code_area_classes.find(cls => cls.startsWith('language-'));
        let language = null;
        if (langClass) {
            language = langClass.substring('language-'.length);
        }
        return language;
    }

    function fetch_with_timeout(url, options, timeout = 6000) {
        return Promise.race([
            fetch(url, options),
            new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), timeout)),
        ]);
    }

    const playgrounds = get_playgrounds();

    function get_codeblock_id(code_area) {
        const code_area_classes = [...code_area.classList.values()];
        const codeBlockIdClass = code_area_classes.find(cls => cls.startsWith('codeblock-id-'));
        let codeBlockId = null;
        if (codeBlockIdClass) {
            codeBlockId = codeBlockIdClass.substring('codeblock-id-'.length);
        }
        return codeBlockId;
    }

    function run_code(code_block) {
        let code_area = code_block.querySelector("code");
        const code_area_classes = [...code_area.classList.values()];
        
        const code_block_id = get_codeblock_id(code_area);
        

        let result_block_parent = code_block;

        if (code_block_id) {
            const codeblock_tabs = document.querySelector(`#${code_block_id}.codeblock-tabs`);

            const pre_block = codeblock_tabs.querySelector('pre.codeblock-result');
            if (pre_block) {
                result_block_parent = pre_block;
            } else { 
                const pre_block = document.createElement('pre');
                pre_block.className = 'codeblock-result';
                codeblock_tabs.appendChild(pre_block);
                result_block_parent = pre_block;    
            }
        }

        
        let result_block = result_block_parent.querySelector('.result');
        if (!result_block) {
            result_block = document.createElement('code');
            result_block.className = 'result hljs language-bash';

            result_block_parent.append(result_block);
        }
        result_block_parent.querySelectorAll('.result-image').forEach(img => img.remove());

        let text;
        let multifile = false;
        
        if (code_block_id) {
            const file_names = [...document.querySelectorAll(`#${code_block_id}.codeblock-tabs > .codeblock-tabs-titles a`).values()].map(el => el.textContent.trim());
            const code_blocks = [...document.querySelectorAll(`#${code_block_id}.codeblock-tabs > .codeblock-tabs-contents > section > pre`).values()].map(el => playground_text(el));

            const code_dict = Object.fromEntries(file_names.map((_, i) => [file_names[i], code_blocks[i]]));

            text = JSON.stringify(code_dict);
            multifile = true;
        } else {
            text = playground_text(code_block);
        }
        
        let language = get_language(code_area);

        for (const cls of code_area_classes) {
            if (cls.startsWith('feature-')) {
                language += `-${cls.substring('feature-'.length)}`;
            }
        }

        const params = {
            language: language,
            code: text,
            multifile: multifile,
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

                const dataUris = result.match(DATA_URI_PATTERN);
                if (dataUris) {
                    dataUris.forEach(dataUri => {
                        const uriContent = dataUri
                            .replace('@@@DATA_URI_BEGIN@@@', '')
                            .replace('@@@DATA_URI_END@@@', '');
                        const img = document.createElement('img');
                        img.src = uriContent;
                        img.className = 'result-image';
                        result_block.parentElement.appendChild(img);
                        result = result.replace(dataUri, '');
                    });
                }

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
                // Preserve original language before removing language-* classes for Ace.
                const langClass = [...block.classList.values()].find(cls => cls.startsWith('language-'));
                if (langClass) {
                    block.dataset.language = langClass.substring('language-'.length);
                }
                for (const lang of PLAYGROUND_LANGS) {
                    block.classList.remove(`language-${lang}`);
                }
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
