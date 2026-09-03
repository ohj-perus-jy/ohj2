(() => {
    // Method lists in task handouts are written as
    //   * `metodi(String a)`: kuvaus
    // Give the signature its own line and drop the leading colon, but only for
    // lists where every item follows the pattern.
    const SEPARATOR = /^\s*:\s*/;

    const firstNode = (li) => {
        for (const node of li.childNodes) {
            const blank = node.nodeType === Node.TEXT_NODE && !node.textContent.trim();
            if (!blank) return node;
        }
        return null;
    };

    const descriptionOf = (code) => {
        let node = code.nextSibling;
        while (node && node.nodeType === Node.TEXT_NODE && !node.textContent.trim()) {
            node = node.nextSibling;
        }
        return node;
    };

    // Returns a function that strips the separator, or null if the item does
    // not start with `code`: text.
    const stripper = (li) => {
        const signature = firstNode(li);
        if (!signature || signature.nodeName !== "CODE") return null;

        const description = descriptionOf(signature);
        if (!description || description.nodeType !== Node.TEXT_NODE) return null;
        if (!SEPARATOR.test(description.textContent)) return null;

        return () => {
            description.textContent = description.textContent.replace(SEPARATOR, "");
        };
    };

    for (const list of document.querySelectorAll("task handout ul")) {
        const items = [...list.children].filter((child) => child.nodeName === "LI");
        if (items.length === 0) continue;

        const strippers = items.map(stripper);
        if (strippers.some((strip) => strip === null)) continue;

        strippers.forEach((strip) => strip());
        list.classList.add("sig-list");
    }
})();
