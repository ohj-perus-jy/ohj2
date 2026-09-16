/* Liittää assets/css/search.css:n hakuikkunan shadow-juureen, johon sivun
 * tyylit eivät ulotu. Tiedosto on jo ladattu sivulle (extra_css), joten
 * selain ei hae sitä uudestaan. bundle.js luo juuren ennen tätä skriptiä;
 * MutationObserver on varalla. */

(() => {
  "use strict";

  const link = document.querySelector(
    'link[rel="stylesheet"][href*="assets/css/search.css"]');
  if (!link || !document.querySelector(".md-search")) return;

  const attach = () => {
    const host = [...document.body.children].find((el) => el.shadowRoot);
    if (!host) return false;
    if (!host.shadowRoot.querySelector('link[href*="assets/css/search.css"]'))
      host.shadowRoot.append(link.cloneNode());
    return true;
  };

  if (attach()) return;
  const observer = new MutationObserver(() => {
    if (attach()) observer.disconnect();
  });
  observer.observe(document.body, { childList: true });
})();
