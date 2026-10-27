#!/usr/bin/env python3
"""Génère les images du README de profil (bannière + cartes de projets), en version claire et sombre.

Usage : python3 tools/build_assets.py   (depuis la racine du dépôt)
Les polices Geist sont intégrées dans chaque SVG : le rendu est le même partout, sans appel externe.
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "src"
OUT = ROOT / "assets"

# Couleurs officielles de GitHub (Primer) : thème clair et thème sombre par défaut
# Fond transparent : l'image prend la couleur de la page, quel que soit le thème GitHub
# (clair, sombre, « dimmed », contraste élevé). Bordures et textes lisibles sur tous les thèmes d'une même famille.
THEMES = {
    "dark": dict(card="none", line="#9198a1", line_op=".35", fg="#f0f6fc", fg2="#9198a1", fg3="#9198a1", accent="#4493f8", icon_bg="#9198a1", icon_op=".12", fire="#d29922", bg="#0d1117"),
    "light": dict(card="none", line="#59636e", line_op=".28", fg="#1f2328", fg2="#59636e", fg3="#59636e", accent="#0969da", icon_bg="#59636e", icon_op=".08", fire="#9a6700", bg="#ffffff"),
}
# Couleurs des langages telles que GitHub les affiche (linguist)
LANG = {"TypeScript": "#3178c6", "Rust": "#dea584", "Python": "#3572A5", "C#": "#178600", "C": "#555555"}

PROJECTS = [
    dict(id="musonic", name="Musonic", icon="musonic.svg",
         lines=["Your own music server, played like Spotify.", "Android, iOS, Android Auto, web and server."],
         langs=["TypeScript", "Rust"], link="musonic.doodz.dev"),
    dict(id="acouz", name="AcouZ", icon="acouz.svg",
         lines=["Hold a key, speak, release: your words", "appear in any Windows app."],
         langs=["Python"], link="acouz.doodz.dev"),
    dict(id="poni", name="PONI", icon="poni.png",
         lines=["Switch IP, mask and DNS in one click.", "Born one night in a hotel with bad Wi-Fi."],
         langs=["C#"], link="Windows · portable"),
    dict(id="esp32", name="ESP32 BACnet / Modbus", icon=None,
         lines=["A BACnet/IP ↔ Modbus TCP gateway", "for about 10 €, flashed from the browser."],
         langs=["C"], link="bacnet-modbus-esp32.doodz.dev"),
]


def b64(path):
    return base64.b64encode((SRC / path).read_bytes()).decode()


FONTS = (
    "<style>"
    ".s{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif}"
    ".m{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace}"
    "</style>"
)
LINK_ICON = "M7.775 3.275a.75.75 0 0 0 1.06 1.06l1.25-1.25a2 2 0 1 1 2.83 2.83l-2.5 2.5a2 2 0 0 1-2.83 0 .75.75 0 0 0-1.06 1.06 3.5 3.5 0 0 0 4.95 0l2.5-2.5a3.5 3.5 0 0 0-4.95-4.95l-1.25 1.25Zm-4.69 9.64a2 2 0 0 1 0-2.83l2.5-2.5a2 2 0 0 1 2.83 0 .75.75 0 0 0 1.06-1.06 3.5 3.5 0 0 0-4.95 0l-2.5 2.5a3.5 3.5 0 0 0 4.95 4.95l1.25-1.25a.75.75 0 0 0-1.06-1.06l-1.25 1.25a2 2 0 0 1-2.83 0Z"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def icon(p, c, x, y, size):
    """Icône du projet : SVG d'origine intégré, PNG en base64, ou puce dessinée pour l'ESP32."""
    if p["icon"] and p["icon"].endswith(".svg"):
        raw = (SRC / p["icon"]).read_text()
        raw = re.sub(r"<\?xml[^>]*>", "", raw)
        raw = re.sub(r'id="([^"]+)"', lambda m: f'id="{p["id"]}-{m.group(1)}"', raw)
        raw = re.sub(r"url\(#([^)]+)\)", lambda m: f'url(#{p["id"]}-{m.group(1)})', raw)
        raw = raw.replace("<svg ", f'<svg x="{x}" y="{y}" width="{size}" height="{size}" ', 1)
        return raw
    if p["icon"]:
        return (f'<clipPath id="{p["id"]}-clip"><rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * .22}"/></clipPath>'
                f'<image x="{x}" y="{y}" width="{size}" height="{size}" clip-path="url(#{p["id"]}-clip)" href="data:image/png;base64,{b64(p["icon"])}"/>')
    # Puce ESP32 dessinée : boîtier + broches, couleurs du thème
    pins = "".join(
        f'<rect x="{x + size * (.27 + i * .155)}" y="{y + size * .08}" width="{size * .06}" height="{size * .12}" rx="1.5" fill="{c["accent"]}"/>'
        f'<rect x="{x + size * (.27 + i * .155)}" y="{y + size * .8}" width="{size * .06}" height="{size * .12}" rx="1.5" fill="{c["accent"]}"/>'
        f'<rect x="{x + size * .08}" y="{y + size * (.27 + i * .155)}" width="{size * .12}" height="{size * .06}" rx="1.5" fill="{c["accent"]}"/>'
        f'<rect x="{x + size * .8}" y="{y + size * (.27 + i * .155)}" width="{size * .12}" height="{size * .06}" rx="1.5" fill="{c["accent"]}"/>'
        for i in range(4))
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * .22}" fill="{c["icon_bg"]}" fill-opacity="{c["icon_op"]}"/>{pins}'
            f'<rect x="{x + size * .22}" y="{y + size * .22}" width="{size * .56}" height="{size * .56}" rx="{size * .08}" fill="{c["fg"]}"/>'
            f'<text x="{x + size / 2}" y="{y + size * .56}" text-anchor="middle" class="m" font-size="{size * .15}" font-weight="600" fill="{c["bg"]}">ESP32</text>')


def card(p, theme):
    c = THEMES[theme]
    W, H = 620, 200
    lines = "".join(f'<text x="116" y="{92 + i * 24}" class="s" font-size="16" fill="{c["fg2"]}">{esc(t)}</text>' for i, t in enumerate(p["lines"]))
    langs, x = "", 28
    for name in p["langs"]:
        langs += f'<circle cx="{x + 6}" cy="{170}" r="6" fill="{LANG[name]}"/><text x="{x + 18}" y="175" class="s" font-size="14" fill="{c["fg2"]}">{esc(name)}</text>'
        x += 18 + len(name) * 8.2 + 22
    is_url = "." in p["link"] and " " not in p["link"]
    right = (f'<g transform="translate({W - 28 - len(p["link"]) * 7.9 - 22} 162)"><path d="{LINK_ICON}" fill="{c["fg2"]}"/></g>'
             f'<text x="{W - 28}" y="175" text-anchor="end" class="s" font-size="14" fill="{c["accent"]}">{esc(p["link"])}</text>') if is_url else \
            f'<text x="{W - 28}" y="175" text-anchor="end" class="s" font-size="14" fill="{c["fg2"]}">{esc(p["link"])}</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(p["name"])}: {esc(" ".join(p["lines"]))}">
{FONTS}
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{c["card"]}" stroke="{c["line"]}" stroke-opacity="{c["line_op"]}" stroke-width="2"/>
{icon(p, c, 28, 28, 68)}
<rect x="28" y="28" width="68" height="68" rx="15" fill="none" stroke="{c["line"]}" stroke-opacity="{c["line_op"]}" stroke-width="1.5"/>
<text x="116" y="60" class="s" font-size="22" font-weight="600" fill="{c["accent"]}">{esc(p["name"])}</text>
{lines}
{langs}
{right}
</svg>
'''


def banner(theme):
    c = THEMES[theme]
    W, H = 1280, 300
    # Petit dessin au trait, à droite : tente, feu, horizon. Une seule couleur, aucun effet.
    ax, ay = 1010, 92
    art = (f'<g fill="none" stroke="{c["fg2"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
           f'<path d="M{ax} {ay + 120} L{ax + 70} {ay + 10} L{ax + 140} {ay + 120}"/>'
           f'<path d="M{ax + 70} {ay + 10} L{ax + 70} {ay + 120}"/>'
           f'<path d="M{ax + 50} {ay + 120} L{ax + 70} {ay + 84} L{ax + 90} {ay + 120}"/>'
           f'<path d="M{ax + 196} {ay + 120} c-14 -10 -16 -26 -2 -44 c2 14 10 16 12 6 c8 12 8 28 -10 38z" stroke="{c["fire"]}"/>'
           f'<path d="M{ax + 176} {ay + 122} l40 -10 M{ax + 176} {ay + 112} l40 10"/>'
           f'</g><line x1="{ax - 40}" y1="{ay + 122}" x2="{W - 48}" y2="{ay + 122}" stroke="{c["line"]}" stroke-opacity="{c["line_op"]}" stroke-width="2"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Doodz. Automation technician by day. I build the tools I can't find elsewhere, sleep in the woods, and film it.">
{FONTS}
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{c["card"]}" stroke="{c["line"]}" stroke-opacity="{c["line_op"]}" stroke-width="2"/>
<clipPath id="av"><circle cx="130" cy="150" r="66"/></clipPath>
<circle cx="130" cy="150" r="68" fill="{c["line"]}" fill-opacity="{c["line_op"]}"/>
<image x="64" y="84" width="132" height="132" clip-path="url(#av)" href="data:image/jpeg;base64,{b64('avatar.png')}"/>
<text x="232" y="136" class="s" font-size="60" font-weight="600" letter-spacing="-1.5" fill="{c["fg"]}">Doodz</text>
<text x="232" y="180" class="s" font-size="22" fill="{c["fg2"]}">Automation technician by day. I build the tools</text>
<text x="232" y="210" class="s" font-size="22" fill="{c["fg2"]}">I can’t find elsewhere, sleep in the woods, <tspan fill="{c["accent"]}">and film it.</tspan></text>
<text x="232" y="252" class="m" font-size="14" fill="{c["fg3"]}">doodz.dev · France · probably future goat farmer</text>
{art}
</svg>
'''


def main():
    OUT.mkdir(exist_ok=True)
    for theme in THEMES:
        (OUT / f"banner-{theme}.svg").write_text(banner(theme))
        for p in PROJECTS:
            (OUT / f"card-{p['id']}-{theme}.svg").write_text(card(p, theme))
    print("assets générés :", ", ".join(sorted(f.name for f in OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
