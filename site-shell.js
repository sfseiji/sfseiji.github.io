async function loadSharedFragment(targetId, filePath, replacements = {}) {
  const target = document.getElementById(targetId);
  if (!target) return;

  const response = await fetch(filePath, { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Failed to load ${filePath}: ${response.status}`);
  }

  let html = await response.text();

  Object.entries(replacements).forEach(([key, value]) => {
    const pattern = new RegExp(`{{${key}}}`, "g");
    html = html.replace(pattern, value);
  });

  target.innerHTML = html;
}

function initNavToggle() {
  const toggle = document.querySelector('#site-header .nav-toggle');
  const links = document.querySelector('#site-header .nav-links');
  if (!toggle || !links) return;
  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  // close the menu after a navigation tap
  links.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => links.classList.remove('open')));
}

function setActiveNav() {
  const currentPage = document.body.dataset.page;
  if (!currentPage) return;

  document.querySelectorAll('#site-header .nav-link[data-page]').forEach(link => {
    if (link.dataset.page === currentPage) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });
}

async function setFooterMeta() {
  const yearEl = document.getElementById('footer-year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  const updatedTextEl = document.getElementById('last-updated-text');
  const updatedWrapEl = document.getElementById('footer-updated-wrap');
  if (!updatedTextEl || !updatedWrapEl) return;

  // Pull the last-commit date once per session and cache it.
  const CACHE_KEY = "sfseiji_last_commit";
  const REPO = "sfseiji/sfseiji.github.io";
  const formatDate = (iso) => {
    const d = new Date(iso);
    return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
  };

  try {
    let cached = sessionStorage.getItem(CACHE_KEY);
    if (cached) {
      updatedTextEl.textContent = formatDate(cached);
      return;
    }
    const res = await fetch(`https://api.github.com/repos/${REPO}/commits?per_page=1`, { cache: "no-cache" });
    if (!res.ok) throw new Error(`status ${res.status}`);
    const data = await res.json();
    const iso = data?.[0]?.commit?.author?.date;
    if (!iso) throw new Error("missing commit date");
    sessionStorage.setItem(CACHE_KEY, iso);
    updatedTextEl.textContent = formatDate(iso);
  } catch (e) {
    // Fall back to per-page data-updated, then hide if neither is available.
    const fallback = (document.body.dataset.updated || "").trim();
    if (fallback) {
      updatedTextEl.textContent = fallback;
    } else {
      updatedWrapEl.style.display = "none";
    }
  }
}

async function initSiteShell() {
  const root = document.body.dataset.root || ".";
  const replacements = { ROOT: root };

  try {
    await loadSharedFragment("site-header", `${root}/includes/header.html`, replacements);
    await loadSharedFragment("site-footer", `${root}/includes/footer.html`, replacements);
    setActiveNav();
    initNavToggle();
    setFooterMeta();
  } catch (error) {
    console.error("Error loading shared site shell:", error);
  }
}

document.addEventListener("DOMContentLoaded", initSiteShell);