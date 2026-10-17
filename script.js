document.documentElement.classList.add("js");

const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#primary-nav");
const navLinks = [...document.querySelectorAll('.site-nav a[href^="#"]')];

function closeMenu(returnFocus = false) {
  menuButton?.setAttribute("aria-expanded", "false");
  navigation?.classList.remove("is-open");
  if (returnFocus) menuButton?.focus();
}

menuButton?.addEventListener("click", () => {
  const open = menuButton.getAttribute("aria-expanded") !== "true";
  menuButton.setAttribute("aria-expanded", String(open));
  navigation?.classList.toggle("is-open", open);
});
navigation?.addEventListener("click", (event) => {
  if (event.target.closest("a")) closeMenu();
});
document.addEventListener("keydown", (event) => {
  if (
    event.key === "Escape" &&
    menuButton?.getAttribute("aria-expanded") === "true"
  )
    closeMenu(true);
});
document.addEventListener("click", (event) => {
  if (!event.target.closest(".header-inner")) closeMenu();
});
window.matchMedia("(min-width: 721px)").addEventListener("change", (event) => {
  if (event.matches) closeMenu();
});

// A small, keyboard-accessible explanation of the architecture illustration.
const stageTabs = [...document.querySelectorAll("[data-stage]")];
function selectStage(tab) {
  const stage = tab.dataset.stage;
  stageTabs.forEach((item) => {
    const active = item === tab;
    item.setAttribute("aria-selected", String(active));
    item.tabIndex = active ? 0 : -1;
    document.getElementById(item.getAttribute("aria-controls")).hidden =
      !active;
  });
  document.querySelectorAll("[data-layer]").forEach((layer) => {
    layer.classList.toggle("is-selected", layer.dataset.layer === stage);
  });
}
stageTabs.forEach((tab, index) => {
  tab.addEventListener("click", () => selectStage(tab));
  tab.addEventListener("keydown", (event) => {
    let next;
    if (event.key === "ArrowRight") next = (index + 1) % stageTabs.length;
    if (event.key === "ArrowLeft")
      next = (index - 1 + stageTabs.length) % stageTabs.length;
    if (event.key === "Home") next = 0;
    if (event.key === "End") next = stageTabs.length - 1;
    if (next === undefined) return;
    event.preventDefault();
    selectStage(stageTabs[next]);
    stageTabs[next].focus();
  });
});

// Progressive enhancement: the page is readable if JavaScript is unavailable.
if ("IntersectionObserver" in window) {
  const reveal = document.querySelectorAll("[data-reveal]");
  document.documentElement.classList.add("reveal-ready");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.06 },
  );
  reveal.forEach((element) => observer.observe(element));

  const sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const id = entry.target.id;
        navLinks.forEach((link) => {
          const active = link.getAttribute("href") === `#${id}`;
          link.classList.toggle("is-active", active);
          if (active) link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        });
      });
    },
    { rootMargin: "-15% 0px -60% 0px", threshold: 0 },
  );
  document
    .querySelectorAll("section[id]")
    .forEach((section) => sectionObserver.observe(section));
}

const footerYear = document.querySelector("#footer-year");
if (footerYear) footerYear.textContent = `© ${new Date().getFullYear()}`;
