(() => {
    const tabButtons = document.querySelectorAll(".accordion-tabs a[data-accordion-target]");

    function setActiveTab(tabId, clickedElement = null) {
        let clickedElementPosition = null;

        if (clickedElement) {
            // Get element's position within the viewport
            const rect = clickedElement.getBoundingClientRect();
            clickedElementPosition = rect.top;
        }

        const targetContentsOpen = document.querySelectorAll(`.accordion-contents section[data-accordion-group="${tabId}"]`);
        const targetContentsClosed = document.querySelectorAll(`.accordion-contents section[data-accordion-group]:not([data-accordion-group="${tabId}"])`);

        const buttonsOpen = document.querySelectorAll(`.accordion-tabs a[data-accordion-target="${tabId}"]`);
        const buttonsClosed = document.querySelectorAll(`.accordion-tabs a[data-accordion-target]:not([data-accordion-target="${tabId}"])`);

        for (const content of targetContentsOpen) {
            // set aria-hidden to false and remove hidden attribute
            content.setAttribute("aria-hidden", "false");
            content.removeAttribute("hidden");
        }

        for (const button of buttonsOpen) {
            // set aria-selected to true
            // set tabindex to 0
            button.setAttribute("aria-selected", "true");
            button.setAttribute("tabindex", "0");
        }


        for (const content of targetContentsClosed) {
            // set aria-hidden to true and add hidden attribute
            content.setAttribute("aria-hidden", "true");
            content.setAttribute("hidden", "true");
        }

        for (const button of buttonsClosed) {
            // set aria-selected to false
            // set tabindex to -1
            button.setAttribute("aria-selected", "false");
            button.setAttribute("tabindex", "-1");
        }

        const url = new URL(window.location);
        url.searchParams.set("tabs", tabId);
        window.history.replaceState({}, "", url);

        // Scroll so that the clicked element is at the same position as before
        // This prevents jumping when the content above changes height
        if (clickedElementPosition !== null) {
            window.requestAnimationFrame(() => {
                const rect = clickedElement.getBoundingClientRect();
                const newClickedElementPosition = rect.top;
                const positionDifference = newClickedElementPosition - clickedElementPosition;
                window.scrollBy(0, positionDifference);
            });
        }
    }


    const urlParams = new URLSearchParams(window.location.search);
    const tabIdFromUrl = urlParams.get("tabs");
    if (tabIdFromUrl) {
        setActiveTab(tabIdFromUrl);
    }

    for (const button of tabButtons) {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const targetId = button.dataset.accordionTarget;
            setActiveTab(targetId, e.target);
        });
    }

})();