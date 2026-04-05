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

function setFooterMeta() {
  const yearEl = document.getElementById('footer-year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  const updatedTextEl = document.getElementById('last-updated-text');
  const updatedWrapEl = document.getElementById('footer-updated-wrap');
  const updatedValue = document.body.dataset.updated || "";

  if (updatedTextEl && updatedWrapEl) {
    if (updatedValue.trim() !== "") {
      updatedTextEl.textContent = updatedValue;
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
    setFooterMeta();
  } catch (error) {
    console.error("Error loading shared site shell:", error);
  }
}

document.addEventListener("DOMContentLoaded", initSiteShell);