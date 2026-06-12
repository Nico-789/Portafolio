import json
import shutil
from html import escape
from pathlib import Path
from string import Template

ICON_BY_SKILL = {
    "python": "python",
    "javascript": "javascript",
    "sql": "postgresql",
    "java": "openjdk",
    "fastapi": "fastapi",
    "flask": "flask",
    "react": "react",
    ".net": "dotnet",
    "android studio": "androidstudio",
    "docker": "docker",
    "git": "git",
    "postman": "postman",
    "mongodb": "mongodb",
    "power bi": "powerbi",
}


def build_skill_badge(item):
    key = (item or "").strip().lower()
    slug = ICON_BY_SKILL.get(key)
    icon_html = ""
    if slug:
        icon_html = f'<img class="pill-icon" src="https://cdn.simpleicons.org/{slug}" alt="" aria-hidden="true">'
    return f'<span class="pill">{icon_html}<span>{item}</span></span>'

BASE_DIR = Path(__file__).resolve().parent
CONTENT_PATH = BASE_DIR / "content.json"
TEMPLATE_PATH = BASE_DIR / "template.html"
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "public"
OUTPUT_ASSETS_DIR = OUTPUT_DIR / "assets"


def build_tags(tags):
    if not tags:
        return ""
    items = "".join([f"<span class=\"tag\">{tag}</span>" for tag in tags])
    return f"<div class=\"tags\">{items}</div>"


def build_links(links):
    if not links:
        return ""
    items = []
    for link in links:
        label = link.get("label", "Link")
        url = link.get("url", "#")
        items.append(f"<a class=\"project-link\" href=\"{url}\" target=\"_blank\" rel=\"noreferrer\">{label}</a>")
    return f"<div class=\"project-links\">{''.join(items)}</div>"


def build_projects(projects):
    cards = []
    for project in projects:
        title = project.get("title", "Project")
        summary = project.get("summary", "")
        impact = project.get("impact", "")
        tags_html = build_tags(project.get("tags", []))
        links_html = build_links(project.get("links", []))
        cards.append(
            """
            <article class="card">
                <div class="card-header">
                    <h3>{title}</h3>
                    <p class="summary">{summary}</p>
                </div>
                <p class="impact">{impact}</p>
                {tags_html}
                {links_html}
            </article>
            """.format(
                title=title,
                summary=summary,
                impact=impact,
                tags_html=tags_html,
                links_html=links_html,
            )
        )
    return "".join(cards)


def build_certifications(certifications):
    items = []
    for cert in certifications:
        name = cert.get("name", "Certification")
        issuer = cert.get("issuer", "")
        year = cert.get("year", "")
        image = (cert.get("image", "") or "").strip()

        if image:
            media_html = (
                f'<div class="cert-media"><img src="{image}" alt="Certificacion {name}" loading="lazy" '
                f'onerror="this.closest(\'.cert-media\').classList.add(\'cert-media-placeholder\'); this.remove();">'
                f'<span>Imagen pendiente</span></div>'
            )
        else:
            media_html = '<div class="cert-media cert-media-placeholder" aria-hidden="true"><span>Imagen pendiente</span></div>'

        items.append(
            f'<li>{media_html}<div class="cert-body"><strong>{name}</strong><span>{issuer}</span><span>{year}</span></div></li>'
        )
    return "".join(items)


def build_skills(skills):
    groups = []
    for group in skills:
        category = group.get("category", "Skills")
        items = group.get("items", [])
        badges = "".join([build_skill_badge(item) for item in items])
        groups.append(
            """
            <div class="skill-group">
                <h4>{category}</h4>
                <div class="pills">{badges}</div>
            </div>
            """.format(category=category, badges=badges)
        )
    return "".join(groups)


def build_interests(interests):
    if not interests:
        return ""
    cleaned = [escape(str(interest).strip()) for interest in interests if str(interest).strip()]
    items = "".join([f"<li>{interest}</li>" for interest in cleaned])
    return items


def build_languages(languages):
    if not languages:
        return ""
    items = []
    for lang in languages:
        name = lang.get("name", "")
        level = lang.get("level", "")
        items.append(f"<li><span>{name}</span><span>{level}</span></li>")
    return "".join(items)


def build_contact(email, phone):
    email = (email or "").strip()
    phone = (phone or "").strip()

    if email:
        return email, f"mailto:{email}"

    if phone:
        normalized = phone.replace(" ", "")
        return phone, f"tel:{normalized}"

    return "", "#"


def main():
    data = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    template = Template(TEMPLATE_PATH.read_text(encoding="utf-8"))

    email = data.get("email", "")
    phone = data.get("phone", "")
    contact_value, contact_href = build_contact(email, phone)

    mapping = {
        "name": data.get("name", "Your Name"),
        "role": data.get("role", "Your Role"),
        "tagline": data.get("tagline", ""),
        "location": data.get("location", ""),
        "email": email,
        "phone": phone,
        "contact_value": contact_value,
        "contact_href": contact_href,
        "linkedin": data.get("linkedin", ""),
        "github": data.get("github", ""),
        "about": data.get("about", ""),
        "cta_text": data.get("cta_text", "Let's talk"),
        "projects_html": build_projects(data.get("projects", [])),
        "certifications_html": build_certifications(data.get("certifications", [])),
        "skills_html": build_skills(data.get("skills", [])),
        "interests_html": build_interests(data.get("interests", [])),
        "languages_html": build_languages(data.get("languages", [])),
        "year": data.get("year", "2026"),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    html = template.safe_substitute(mapping)
    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")

    if ASSETS_DIR.exists():
        shutil.copytree(ASSETS_DIR, OUTPUT_ASSETS_DIR, dirs_exist_ok=True)

    print("Generated public/index.html")


if __name__ == "__main__":
    main()
