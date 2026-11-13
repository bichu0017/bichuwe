const menuButton = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");
document.querySelectorAll('a[href^="/admin-dashboard/"]').forEach((link) => {
  if (window.location.port === "5500") {
    link.href = `${window.location.protocol}//${window.location.hostname}:8000${link.getAttribute("href")}`;
  }
});
const navItems = [...document.querySelectorAll(".nav-link")];
const sections = navItems
  .map((item) => document.querySelector(item.getAttribute("href")))
  .filter(Boolean);

menuButton.addEventListener("click", () => {
  const isExpanded = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!isExpanded));
  menuButton.setAttribute("aria-label", isExpanded ? "Open navigation" : "Close navigation");
  navLinks.classList.toggle("is-open", !isExpanded);
});

navItems.forEach((item) => {
  item.addEventListener("click", () => {
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Open navigation");
    navLinks.classList.remove("is-open");
  });
});

if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));

  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        navItems.forEach((item) => item.classList.toggle("active", item.getAttribute("href") === `#${entry.target.id}`));
      }
    });
  }, { rootMargin: "-30% 0px -60% 0px" });
  sections.forEach((section) => sectionObserver.observe(section));
} else {
  document.querySelectorAll(".reveal").forEach((element) => element.classList.add("is-visible"));
}

document.querySelector("#current-year").textContent = new Date().getFullYear();

const setText = (selector, value) => {
  const element = document.querySelector(selector);
  if (element && value) element.textContent = value;
};

const getResults = async (endpoint) => {
  const response = await fetch(endpoint);
  if (!response.ok) throw new Error(`${endpoint} returned ${response.status}`);
  const payload = await response.json();
  return Array.isArray(payload) ? payload : payload.results ?? [];
};

const loadPortfolioContent = async () => {
  document.querySelectorAll(".social-links a").forEach((link) => { link.hidden = true; });
  try {
    const profiles = await getResults("/api/profile/");
    const profile = profiles[0];
    if (profile) {
      const heading = document.querySelector("#hero-title");
      const accentPeriod = document.createElement("span");
      accentPeriod.className = "accent-period";
      accentPeriod.textContent = ".";
      heading.replaceChildren(document.createTextNode(`Hi, I’m ${profile.full_name}`), accentPeriod);
      setText(".hero-role", profile.professional_title);
      setText(".hero-description", profile.introduction);
      setText(".about-body p", profile.biography);
      const emailLink = document.querySelector(".contact-email");
      if (profile.email && emailLink) {
        emailLink.href = `mailto:${profile.email}`;
        emailLink.textContent = profile.email;
        emailLink.hidden = false;
      }
      const location = document.querySelector(".contact-location");
      if (profile.location && location) {
        location.textContent = profile.location;
        location.hidden = false;
      }
      const phoneLink = document.querySelector(".contact-phone");
      if (profile.phone && phoneLink) {
        phoneLink.href = `tel:${profile.phone}`;
        phoneLink.textContent = profile.phone;
        phoneLink.hidden = false;
      }
      document.querySelector(".contact-placeholder").hidden = Boolean(profile.email || profile.location || profile.phone);
      for (const [network, url] of Object.entries({
        linkedin: profile.linkedin_url,
        github: profile.github_url,
        instagram: profile.instagram_url,
      })) {
        const link = document.querySelector(`[data-social="${network}"]`);
        if (link && url) {
          link.href = url;
          link.hidden = false;
        }
      }
      const profileImages = [
        profile.profile_image,
        profile.profile_image_2,
        profile.profile_image_3,
      ].filter(Boolean);
      if (profileImages.length) {
        const image = document.querySelector(".hero-photo");
        image.alt = `Portrait of ${profile.full_name}`;
        const controls = document.querySelector(".photo-controls");
        image.src = profileImages[0];

        if (profileImages.length > 1) {
          let activeIndex = 0;
          let transitionTimeout;
          const buttons = profileImages.map((_, index) => {
            const button = document.createElement("button");
            button.className = "photo-control";
            button.type = "button";
            button.setAttribute("aria-label", `Show profile photo ${index + 1}`);
            button.setAttribute("aria-pressed", String(index === activeIndex));
            button.addEventListener("click", () => showPhoto(index));
            controls.append(button);
            return button;
          });
          controls.hidden = false;

          function showPhoto(index) {
            if (index === activeIndex) return;
            activeIndex = index;
            buttons.forEach((button, buttonIndex) => {
              button.setAttribute("aria-pressed", String(buttonIndex === activeIndex));
            });
            image.classList.add("is-transitioning");
            window.clearTimeout(transitionTimeout);
            transitionTimeout = window.setTimeout(() => {
              image.src = profileImages[activeIndex];
              image.classList.remove("is-transitioning");
            }, 220);
          }

          if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            window.setInterval(() => showPhoto((activeIndex + 1) % profileImages.length), 3000);
          }
        }
      }
    }

    const [skills, projects] = await Promise.all([
      getResults("/api/skills/"),
      getResults("/api/projects/"),
    ]);
    if (skills.length) renderSkills(skills);
    if (projects.length) renderProjects(projects);
  } catch (error) {
    console.error("Could not load portfolio content from the API.", error);
  }

  await loadFileResources();
};

const loadFileResources = async () => {
  try {
    const [resumes, certificates] = await Promise.all([
      getResults("/api/resume/"),
      getResults("/api/certifications/"),
    ]);
    renderResume(resumes[0]);
    renderCertificates(certificates);
  } catch (error) {
    console.error("Could not load resume and certificate files.", error);
    document.querySelector("#resume-list").innerHTML = "<p class=\"empty-files\">Resume files could not be loaded. Please try again later.</p>";
    document.querySelector("#certificate-list").innerHTML = "<p class=\"empty-files\">Certificates could not be loaded. Please try again later.</p>";
  }
};

const renderResume = (resume) => {
  const container = document.querySelector("#resume-list");
  if (!resume) return;
  const fileName = document.createElement("span");
  fileName.className = "file-icon";
  fileName.textContent = "CV";
  fileName.setAttribute("aria-hidden", "true");
  const details = document.createElement("div");
  const title = document.createElement("h3");
  title.textContent = resume.description || "Bichu Biju — Resume";
  const date = document.createElement("p");
  date.textContent = `Updated ${new Date(resume.uploaded_at).toLocaleDateString()}`;
  details.append(title, date);
  const download = document.createElement("a");
  download.className = "button button-primary";
  download.href = resume.download_url;
  download.textContent = "Download resume";
  download.setAttribute("download", "");
  container.replaceChildren(fileName, details, download);
};

const renderCertificates = (certificates) => {
  const container = document.querySelector("#certificate-list");
  if (!certificates.length) return;
  container.replaceChildren();
  certificates.forEach((certificate) => {
    const card = document.createElement("article");
    card.className = "certificate-card";
    if (certificate.certificate_image) {
      const imageLink = document.createElement("a");
      imageLink.className = "certificate-image-link";
      imageLink.href = certificate.certificate_image;
      imageLink.target = "_blank";
      imageLink.rel = "noreferrer";
      imageLink.setAttribute("aria-label", `View certificate: ${certificate.title}`);
      const image = document.createElement("img");
      image.src = certificate.certificate_image;
      image.alt = `Certificate: ${certificate.title}`;
      image.loading = "lazy";
      imageLink.append(image);
      card.append(imageLink);
    }
    const details = document.createElement("div");
    details.className = "certificate-details";
    const title = document.createElement("h3");
    title.textContent = certificate.title;
    const organization = document.createElement("p");
    organization.className = "certificate-organization";
    organization.textContent = certificate.organization;
    details.append(title, organization);
    if (certificate.description) {
      const description = document.createElement("p");
      description.textContent = certificate.description;
      details.append(description);
    }
    if (certificate.issue_date) {
      const date = document.createElement("p");
      date.className = "certificate-date";
      date.textContent = new Date(certificate.issue_date).toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
      });
      details.append(date);
    }
    if (certificate.credential_url) {
      const credential = document.createElement("a");
      credential.className = "text-link";
      credential.href = certificate.credential_url;
      credential.target = "_blank";
      credential.rel = "noreferrer";
      credential.textContent = "View credential ↗";
      details.append(credential);
    }
    if (certificate.certificate_file) {
      const fileLink = document.createElement("a");
      fileLink.className = "text-link";
      fileLink.href = certificate.certificate_file;
      fileLink.target = "_blank";
      fileLink.rel = "noreferrer";
      fileLink.textContent = "Open certificate file ↗";
      details.append(fileLink);
    }
    card.append(details);
    container.append(card);
  });
};

const renderSkills = (skills) => {
  const container = document.querySelector(".skills-grid");
  const grouped = skills.reduce((groups, skill) => {
    const group = groups.get(skill.category) ?? [];
    group.push(skill);
    groups.set(skill.category, group);
    return groups;
  }, new Map());
  container.replaceChildren();
  [...grouped.entries()].forEach(([category, items], index) => {
    const card = document.createElement("article");
    card.className = "skill-group reveal is-visible";
    const number = document.createElement("span");
    number.className = "skill-number";
    number.textContent = String(index + 1).padStart(2, "0");
    const title = document.createElement("h3");
    title.textContent = category;
    const tags = document.createElement("div");
    tags.className = "skill-items";
    items.forEach((skill) => {
      const tag = document.createElement("span");
      tag.textContent = skill.name;
      tags.append(tag);
    });
    card.append(number, title, tags);
    container.append(card);
  });
};

const renderProjects = (projects) => {
  const container = document.querySelector("#project-grid");
  container.replaceChildren();
  projects.forEach((project) => {
    const card = document.createElement("article");
    card.className = "project-card reveal is-visible";
    const art = document.createElement("div");
    art.className = "project-art art-neural";
    if (project.thumbnail) {
      art.style.backgroundImage = `linear-gradient(#173c3d33,#173c3d33), url("${project.thumbnail}")`;
      art.style.backgroundSize = "cover";
      art.style.backgroundPosition = "center";
    } else {
      art.setAttribute("aria-hidden", "true");
    }
    const label = document.createElement("span");
    label.className = "art-label";
    label.textContent = project.category;
    art.append(label);
    const info = document.createElement("div");
    info.className = "project-info";
    const type = document.createElement("span");
    type.className = "project-type";
    type.textContent = project.featured ? "FEATURED PROJECT" : "PROJECT";
    const title = document.createElement("h3");
    title.textContent = project.title;
    const description = document.createElement("p");
    description.textContent = project.description;
    const tags = document.createElement("div");
    tags.className = "tag-list";
    (project.technologies ?? []).forEach((technology) => {
      const tag = document.createElement("span");
      tag.textContent = technology;
      tags.append(tag);
    });
    info.append(type, title, description, tags);
    for (const [url, labelText] of [[project.github_url, "GitHub"], [project.live_demo_url, "Live demo"]]) {
      if (!url) continue;
      const link = document.createElement("a");
      link.className = "text-link";
      link.href = url;
      link.target = "_blank";
      link.rel = "noreferrer";
      link.textContent = labelText;
      info.append(link);
    }
    card.append(art, info);
    container.append(card);
  });
};

loadPortfolioContent();

document.querySelector("#contact-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  if (!form.reportValidity()) return;

  const status = document.querySelector("#form-status");
  const submitButton = form.querySelector('button[type="submit"]');
  submitButton.disabled = true;
  status.textContent = "Sending your message…";
  try {
    const csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]').value;
    const response = await fetch("/api/contact/", {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken },
      body: new FormData(form),
    });
    if (!response.ok) {
      const details = await response.json();
      throw new Error(details.detail ?? "The message could not be sent.");
    }
    form.reset();
    status.textContent = "Thanks — your message has been sent.";
  } catch (error) {
    console.error("Contact form submission failed.", error);
    status.textContent = "Sorry, your message could not be sent. Please email me directly.";
  } finally {
    submitButton.disabled = false;
  }
});
