(() => {

    function updateIndicator(codeblock) {
        const titles = codeblock.querySelector(".codeblock-tabs-titles");
        const active = titles.querySelector('a[aria-selected="true"]');
        let indicator = titles.querySelector(".codeblock-tabs-indicator");

        if (!indicator) {
            indicator = document.createElement("div");
            indicator.className = "codeblock-tabs-indicator";
            titles.appendChild(indicator);
        }

        if (active) {
            const li = active.closest("li");
            const marginTop = parseFloat(getComputedStyle(li).marginTop) || 0;
            indicator.style.left = li.offsetLeft + "px";
            indicator.style.top = (li.offsetTop - marginTop) + "px";
            indicator.style.width = li.offsetWidth + "px";
        }
    }

    const codeblocks = document.querySelectorAll("div.codeblock-tabs");

    for (const codeblock of codeblocks) {
        const tabButtons = codeblock.querySelectorAll(".codeblock-tabs-titles a");
        const tabPanels = codeblock.querySelectorAll(".codeblock-tabs-contents > section");

        // Set initial indicator position without animation
        const indicator = document.createElement("div");
        indicator.className = "codeblock-tabs-indicator";
        indicator.style.transition = "none";
        codeblock.querySelector(".codeblock-tabs-titles").appendChild(indicator);
        updateIndicator(codeblock);
        // Re-enable transition after initial placement
        requestAnimationFrame(() => {
            indicator.style.transition = "";
        });

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

                updateIndicator(codeblock);
            });

        }

    }

})();