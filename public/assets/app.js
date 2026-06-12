document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("fade-in");
  const header = document.querySelector(".site-header");

  const onScroll = () => {
    if (!header) {
      return;
    }
    header.classList.toggle("scrolled", window.scrollY > 8);
  };

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const links = document.querySelectorAll("a[href^='#']");
  links.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const targetId = link.getAttribute("href").slice(1);
      const target = document.getElementById(targetId);
      if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  const skillPills = Array.from(document.querySelectorAll("#skills .pill"));
  const closeAllPills = (exceptPill) => {
    skillPills.forEach((pill) => {
      if (pill !== exceptPill) {
        pill.classList.remove("is-open");
        pill.setAttribute("aria-pressed", "false");
      }
    });
  };

  skillPills.forEach((pill) => {
    pill.setAttribute("role", "button");
    pill.setAttribute("tabindex", "0");
    pill.setAttribute("aria-pressed", "false");

    const togglePill = () => {
      const isOpen = !pill.classList.contains("is-open");
      closeAllPills(pill);
      pill.classList.toggle("is-open", isOpen);
      pill.setAttribute("aria-pressed", isOpen ? "true" : "false");
    };

    pill.addEventListener("click", togglePill);
    pill.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        togglePill();
      }
    });
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest("#skills .pill")) {
      closeAllPills();
    }
  });
});
