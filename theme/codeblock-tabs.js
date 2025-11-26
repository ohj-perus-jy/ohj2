(() => {

    const codeblocks = document.querySelectorAll("div.codeblock-tabs");

    for (const codeblock of codeblocks) {
        const tabButtons = codeblock.querySelectorAll(".codeblock-tabs-titles a");
        const tabPanels = codeblock.querySelectorAll(".codeblock-tabs-contents > section");

        for (const button of tabButtons) {
            button.addEventListener("click", (e) => {
                e.preventDefault();

                const fileNum = button.dataset.fileNum;

                for (const btn of tabButtons) {
                    if (btn.dataset.fileNum === fileNum) {
                        btn.setAttribute("aria-selected", "true");
                        btn.setAttribute("tabindex", "0");
                    }
                    else {
                        btn.setAttribute("aria-selected", "false");
                        btn.setAttribute("tabindex", "-1");
                    }
                }

                for (const panel of tabPanels) {
                    if (panel.dataset.fileNum === fileNum) {
                        panel.removeAttribute("hidden");
                        panel.setAttribute("aria-hidden", "false");
                    } else {
                        panel.setAttribute("hidden", "true");
                        panel.setAttribute("aria-hidden", "true");
                    }
                }
                
            });

        }

    }

})();