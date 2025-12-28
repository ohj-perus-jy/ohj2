/*
 * Sidebar TOC normalization:
 * - Collapse all chapters on load
 * - Expand only the chapter that contains the current page
 * - Mark readiness to avoid flashing content during load
 */
(function sidebarToc() {
    const scrollboxSelector = "mdbook-sidebar-scrollbox";
    let tocReady = false;

    // Normalize paths so `/foo/` and `/foo/index.html` are treated as the same page.
    function normalizePath(pathname) {
        let normalized = pathname.replace(/\/+$/, "");
        if (normalized.endsWith("/index.html")) {
            normalized = normalized.slice(0, -"/index.html".length);
        }
        return normalized;
    }

    // Match the current page against sidebar links and return the active <a>.
    function resolveActiveLink(root) {
        const currentUrl = new URL(window.location.href);
        const currentPath = normalizePath(currentUrl.pathname);
        const links = Array.from(root.querySelectorAll("a[href]"));

        for (const link of links) {
            if (!link.href) {
                continue;
            }

            const linkUrl = new URL(link.href, currentUrl);
            const linkPath = normalizePath(linkUrl.pathname);
            if (linkPath === currentPath) {
                return link;
            }
        }

        return root.querySelector("a.active");
    }

    // Return the top-level chapter <li> associated with an active link.
    function getChapterItemForLink(root, activeLink) {
        const linkLi = activeLink.closest("li");
        if (!linkLi) {
            return null;
        }

        if (linkLi.parentElement === root) {
            const nextLi = linkLi.nextElementSibling;
            if (nextLi && nextLi.querySelector("ol.section")) {
                return linkLi;
            }
        }

        const sectionOl = linkLi.closest("ol.section");
        if (!sectionOl) {
            return null;
        }

        const sectionContainer = sectionOl.closest("li");
        if (!sectionContainer) {
            return null;
        }

        const chapterItem = sectionContainer.previousElementSibling;
        if (chapterItem && chapterItem.classList.contains("chapter-item")) {
            return chapterItem;
        }

        return null;
    }

    // Return the subchapter <ol> paired with a chapter item, if present.
    function getSectionForChapterItem(chapterItem) {
        const nextLi = chapterItem.nextElementSibling;
        if (!nextLi) {
            return null;
        }
        return nextLi.querySelector("ol.section");
    }

    // Set an explicit max-height to animate open/close without layout jumps.
    function updateSectionHeight(chapterItem) {
        const section = getSectionForChapterItem(chapterItem);
        if (!section) {
            return;
        }

        if (chapterItem.classList.contains("expanded")) {
            section.style.maxHeight = `${section.scrollHeight}px`;
        } else {
            section.style.maxHeight = "0px";
        }
    }

    // Sync max-height for all sections (used after initial expansion).
    function updateAllSectionHeights(root) {
        const chapterItems = Array.from(root.querySelectorAll("li.chapter-item"));
        chapterItems.forEach((chapterItem) => updateSectionHeight(chapterItem));
    }

    // Add toggle buttons next to chapters that have subchapters.
    function ensureChapterToggles(root) {
        const chapterItems = Array.from(root.querySelectorAll("li.chapter-item"));

        chapterItems.forEach((chapterItem) => {
            const nextLi = chapterItem.nextElementSibling;
            if (!nextLi || !nextLi.querySelector("ol.section")) {
                return;
            }

            if (chapterItem.querySelector("button.toc-toggle")) {
                return;
            }

            const toggle = document.createElement("button");
            toggle.type = "button";
            toggle.className = "toc-toggle";
            toggle.setAttribute("aria-label", "Toggle subchapters");
            toggle.addEventListener("click", (event) => {
                event.preventDefault();
                event.stopPropagation();
                chapterItem.classList.toggle("expanded");
                updateSectionHeight(chapterItem);
            });

            chapterItem.appendChild(toggle);
        });
    }

    // Expand only the chapter that owns the active link.
    function expandActivePath(root) {
        const activeLink = resolveActiveLink(root);
        if (!activeLink) {
            return null;
        }

        root.querySelectorAll("a.active").forEach((link) => {
            link.classList.remove("active");
        });
        activeLink.classList.add("active");

        const chapterItem = getChapterItemForLink(root, activeLink);
        if (!chapterItem) {
            return null;
        }

        chapterItem.classList.add("expanded");
        return chapterItem;
    }

    // Normalize the TOC and signal readiness to CSS.
    function normalizeSidebarToc() {
        const scrollbox = document.querySelector(scrollboxSelector);
        if (!scrollbox) {
            return;
        }

        const root = scrollbox.querySelector("ol.chapter");
        if (!root) {
            return;
        }

        if (!tocReady) {
            document.documentElement.classList.remove("toc-ready");
        }

        ensureChapterToggles(root);

        root.querySelectorAll("li.expanded").forEach((item) => {
            item.classList.remove("expanded");
        });

        expandActivePath(root);

        if (!tocReady) {
            document.documentElement.classList.add("toc-initial");
            requestAnimationFrame(() => {
                document.documentElement.classList.add("toc-ready");
                updateAllSectionHeights(root);
                tocReady = true;
                setTimeout(() => {
                    document.documentElement.classList.remove("toc-initial");
                }, 900);
            });
        } else {
            updateAllSectionHeights(root);
        }
    }

    // Observe the sidebar content and normalize once it is populated.
    function init() {
        const scrollbox = document.querySelector(scrollboxSelector);
        if (!scrollbox) {
            return;
        }

        const observer = new MutationObserver(() => normalizeSidebarToc());
        observer.observe(scrollbox, { childList: true, subtree: true });
        normalizeSidebarToc();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
