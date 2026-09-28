#!/usr/bin/env python3
"""Génère cv.pdf — un CV d'une page, fond = l'image fournie par Adam
(tools/assets/cv-bg.webp, son propre montage Photoshop : quasi noir, halo
bleu au coin haut-gauche), utilisée telle quelle. Structure du CV inspirée
de celui de Bastien Okonski (deux colonnes, pitch en intro, compétences
groupées, expériences datées, projets avec tags et liens) mais avec les
vraies données d'Adam.

Contenu et coordonnées : à jour manuellement ici, pas encore piloté par
l'admin (data.json) — voir CONTEXTE.md si ça change.

    pip3 install --user reportlab pillow
    python3 tools/generate_cv.py

Écrit cv.pdf. Le bouton "CV" du site (cv.pdf, avec `download`) le sert
déjà sur toutes les pages — rien d'autre à brancher.
"""
import os, io, re
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit, ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cv.pdf")

# Police cursive du site (adam/style.css : --font-script, "Homemade Apple"),
# pour que la bio du CV soit dans la même main que celle de la page d'accueil.
pdfmetrics.registerFont(TTFont("HomemadeApple", os.path.join(ROOT, "tools", "fonts", "HomemadeApple-Regular.ttf")))

W, H = A4  # 595 x 842 pt

# ---- palette du site (adam/style.css : --accent-strong, --accent-sky, --text-dim) ----
ACCENT = (91/255, 99/255, 255/255)    # #5b63ff (accentStrong)
ACCENT_SKY = (163/255, 174/255, 255/255)  # #a3aeff
WHITE = (1, 1, 1)
TEXT_DIM = (0.72, 0.74, 0.85)
TEXT_FAINT = (0.55, 0.57, 0.7)
LINE = (0.25, 0.28, 0.45)

MARGIN = 42
COL_GAP = 24
COL_W = (W - 2 * MARGIN - COL_GAP) / 2
LX = MARGIN
RX = MARGIN + COL_W + COL_GAP

c = canvas.Canvas(OUT, pagesize=A4)


# Fond exact fourni par Adam (capture de son propre montage Photoshop) —
# pas une recomposition : l'image telle quelle, juste mise a l'echelle A4.
BG_IMAGE_PATH = os.path.join(ROOT, "tools", "assets", "cv-bg.webp")


def make_background(w_pt, h_pt, scale=3):
    img = Image.open(BG_IMAGE_PATH).convert("RGB")
    iw, ih = img.size
    target_ratio = w_pt / h_pt
    img_ratio = iw / ih
    # recadrage "cover" (au cas ou le ratio ne collerait pas exactement)
    if abs(img_ratio - target_ratio) > 0.005:
        if img_ratio > target_ratio:
            new_w = int(ih * target_ratio)
            x0 = (iw - new_w) // 2
            img = img.crop((x0, 0, x0 + new_w, ih))
        else:
            new_h = int(iw / target_ratio)
            y0 = (ih - new_h) // 2
            img = img.crop((0, y0, iw, y0 + new_h))
    return img.resize((int(w_pt * scale), int(h_pt * scale)), Image.LANCZOS)


# ---- fond ----
bg_buf = io.BytesIO()
make_background(W, H).save(bg_buf, format="PNG")
bg_buf.seek(0)
c.drawImage(ImageReader(bg_buf), 0, 0, width=W, height=H)


def wrap(text, font, size, max_w):
    return simpleSplit(text, font, size, max_w)


# ---- en-tête (juste le nom et le rôle — pas de 3e ligne, déjà redit en Formations) ----
y = H - 56
c.setFillColorRGB(*WHITE)
c.setFont("Helvetica-Bold", 27)
c.drawString(LX, y, "Adam Karroum")

c.setFillColorRGB(*ACCENT_SKY)
c.setFont("Helvetica-Bold", 10.5)
c.drawString(LX, y - 20, "Communication · Audiovisuel")

# bloc contact, aligné à droite
contact = [
    "adam.karroum@student.isfsc.be",
    "0486 53 37 15",
    "Bruxelles, Belgique",
]
c.setFont("Helvetica", 10)
cy = y
for i, line in enumerate(contact):
    c.setFillColorRGB(*(WHITE if i == 0 else TEXT_DIM))
    c.drawRightString(W - MARGIN, cy, line)
    cy -= 14


# Memes traces SVG que la rangee d'icones du site (script.js, SOCIAL_ICONS) —
# un vrai glyphe vectoriel plutot qu'une forme approximee a la main, pour que
# CV/lettre/site soient visuellement la meme identite.
ACCENT_SKY_HEX = "#%02x%02x%02x" % tuple(round(v * 255) for v in ACCENT_SKY)
SOCIAL_SVG = {
    "linkedin": '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none">'
                '<path d="M4.98 3.5a2.5 2.5 0 11-.02 5 2.5 2.5 0 01.02-5zM3 8.98h4v12.02H3V8.98zm7 0h3.8v1.64h.05c.53-.98 1.83-2.02 3.77-2.02 4.03 0 4.78 2.53 4.78 5.82v6.58h-4v-5.84c0-1.39-.03-3.18-1.98-3.18-1.98 0-2.29 1.5-2.29 3.08v5.94h-4V8.98z" fill="{color}"/></svg>',
    "instagram": '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none">'
                 '<rect x="3" y="3" width="18" height="18" rx="5" stroke="{color}" stroke-width="1.6"/>'
                 '<circle cx="12" cy="12" r="4" stroke="{color}" stroke-width="1.6"/>'
                 '<circle cx="17.2" cy="6.8" r="1.1" fill="{color}"/></svg>',
}


def social_icon(x, cy, size, url, platform):
    markup = SOCIAL_SVG[platform].format(s=size, color=ACCENT_SKY_HEX)
    drawing = svg2rlg(io.BytesIO(markup.encode("utf-8")))
    renderPDF.draw(drawing, c, x, cy - size / 2)
    c.linkURL(url, (x, cy - size / 2, x + size, cy + size / 2), relative=0)


# Icônes réseaux : plus bas sur la page (voir bloc après l'encart "Jobs
# étudiants"), pas dans l'en-tête.

# ---- pitch (bordure gauche façon citation ; police cursive du site, comme
# la bio de la page d'accueil) ----
y -= 80
pitch = ("Depuis petit, je suis passionné par la création de contenu et l'influence sur le web. "
         "Autodidacte, j'ai développé des compétences en graphisme, montage vidéo et mixage audio.")
lines = wrap(pitch, "HomemadeApple", 10.5, W - 2 * MARGIN)
c.setFont("HomemadeApple", 10.5)
c.setFillColorRGB(*TEXT_DIM)
ty = y
for line in lines:
    c.drawString(LX, ty, line)
    ty -= 16

y = ty - 26


def section_title(x, y, title):
    c.setFillColorRGB(*ACCENT_SKY)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x, y, title.upper())
    c.setStrokeColorRGB(*LINE)
    c.setLineWidth(0.6)
    c.line(x, y - 7, x + COL_W, y - 7)
    return y - 24


def entry(x, y, date, title, place, desc_lines, link=None, gap_after=22):
    c.setFillColorRGB(*TEXT_FAINT)
    c.setFont("Helvetica", 8.5)
    c.drawString(x, y, date)
    y -= 13
    c.setFillColorRGB(*WHITE)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x, y, title)
    y -= 14
    if place:
        c.setFillColorRGB(*ACCENT_SKY)
        c.setFont("Helvetica", 9.5)
        c.drawString(x, y, place)
        if link:
            c.setFillColorRGB(*ACCENT)
            c.setFont("Helvetica-Bold", 8.5)
            voir = "Voir »"
            voir_w = c.stringWidth(voir, "Helvetica-Bold", 8.5)
            c.drawRightString(x + COL_W, y, voir)
            c.linkURL(link, (x + COL_W - voir_w, y - 2, x + COL_W, y + 9), relative=0)
        y -= 14
    if desc_lines:
        c.setFillColorRGB(*TEXT_DIM)
        c.setFont("Helvetica", 9)
        for dl in desc_lines:
            for wrapped in wrap(dl, "Helvetica", 9, COL_W):
                c.drawString(x, y, wrapped)
                y -= 12.5
    return y - gap_after


def skill_group(x, y, title, items):
    c.setFillColorRGB(*WHITE)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x, y, title)
    y -= 13.5
    c.setFillColorRGB(*TEXT_DIM)
    c.setFont("Helvetica", 9.5)
    for wrapped in wrap(items, "Helvetica", 9.5, COL_W):
        c.drawString(x, y, wrapped)
        y -= 12
    return y - 13


def project(x, y, title, desc, tags, link_label=None):
    c.setFillColorRGB(*WHITE)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x, y, title)
    y -= 13.5
    if desc:
        c.setFillColorRGB(*TEXT_DIM)
        c.setFont("Helvetica", 9.5)
        for wrapped in wrap(desc, "Helvetica", 9.5, COL_W):
            c.drawString(x, y, wrapped)
            y -= 12.5
    if tags or link_label:
        c.setFillColorRGB(*ACCENT_SKY)
        c.setFont("Helvetica", 8.5)
        c.drawString(x, y, " · ".join(tags))
        if link_label:
            c.setFillColorRGB(*ACCENT)
            c.setFont("Helvetica-Bold", 8.5)
            c.drawRightString(x + COL_W, y, link_label)
        y -= 13
    return y - 13


def insert_card(x, top_y, title, items):
    """Encart en pointillés, sans fond, coins droits — pour un groupe d'xp à
    part des expériences « com » — ex. jobs étudiants."""
    pad = 14
    item_h = 32
    h = pad * 2 + 18 + len(items) * item_h

    c.saveState()
    c.setDash(3, 3)
    c.setStrokeColorRGB(140/255, 160/255, 255/255)
    c.setStrokeAlpha(0.5)
    c.setLineWidth(0.8)
    c.rect(x, top_y - h, COL_W, h, fill=0, stroke=1)
    c.restoreState()

    ty = top_y - pad - 9
    c.setFillColorRGB(*ACCENT_SKY)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x + pad, ty, title.upper())
    ty -= item_h
    for date, jtitle, place in items:
        c.setFillColorRGB(*TEXT_FAINT)
        c.setFont("Helvetica", 8)
        c.drawString(x + pad, ty + 16, date)
        c.setFillColorRGB(*WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + pad, ty + 3, jtitle)
        c.setFillColorRGB(*ACCENT_SKY)
        c.setFont("Helvetica", 9)
        c.drawRightString(x + COL_W - pad, ty + 3, place)
        ty -= item_h
    return top_y - h


# ============ COLONNE GAUCHE : Expériences (com) puis Formations ============
ly = y
ly = section_title(LX, ly, "Expériences")

ly = entry(LX, ly, "2024 — Aujourd'hui", "Responsable communication & digital", "Union Oasis Forest",
           ["Stratégie social media et identité visuelle du club (+1 200 % de vues, +1 400 % "
            "d'interactions sur Instagram, saison 2025-26).",
            "Conception du site web et d'un outil d'administration sur mesure ; structuration "
            "de l'ASBL (Google Workspace for Nonprofits)."],
           link="https://adam.nocturnz.xyz/groupe.html?id=union-oasis-forest")
ly = entry(LX, ly, "2025 (3 mois)", "Stage — Production & communication", "Média En Esprit (Chloé Levy)",
           ["Tournage et gestion de plateau (concert, théâtre), montage long format et formats "
            "courts, direction artistique (miniatures, logo), dans les locaux de RMB Slice."],
           link="https://adam.nocturnz.xyz/groupe.html?id=en-esprit")

ly = section_title(LX, ly, "Formations")
ly = entry(LX, ly, "2023 — Aujourd'hui", "Bachelier en Communication",
           "ISFSC (HE ICHEC – ECAM – ISFSC)", [])
ly = entry(LX, ly, "2022 — 2023", "Informatique de gestion",
           "Haute École Léonard de Vinci", [])
ly = entry(LX, ly, "2017 — 2022", "CESS général — option sciences économiques",
           "Athénée Joseph Bracops", [])

# ---- encart jobs étudiants (hors expériences liées à la com) : plus de
# place en bas de cette colonne qu'à droite, une fois les compétences ajoutées.
# Meme ecart que celui laisse par entry() au-dessus de "FORMATIONS" (son
# gap_after de 22pt) : pas de correction manuelle supplementaire ici.
jobs_card_top = ly
ly = insert_card(LX, ly, "Jobs étudiants", [
    ("2022 — Aujourd'hui", "Hôte d'accueil", "Basic-Fit"),
    ("2025 — 2026", "Technicien de surface", "Hôpital Erasme (ISS)"),
])
jobs_card_bottom = ly

# ============ COLONNE DROITE : Compétences, Soft skills, Projets ============
ry = y
ry = section_title(RX, ry, "Compétences")
ry = skill_group(RX, ry, "Montage vidéo", "Premiere Pro, After Effects, DaVinci Resolve, CapCut")
ry = skill_group(RX, ry, "Design graphique", "Photoshop, InDesign, Illustrator, Lightroom")
ry = skill_group(RX, ry, "Outils (Administratif)", "Meta Business Suite, Google Workspace, Notion")
ry = skill_group(RX, ry, "Langues", "Français, Anglais B1")

ry = section_title(RX, ry, "Soft skills")
c.setFillColorRGB(*TEXT_DIM)
c.setFont("Helvetica", 9.5)
for wrapped in wrap("Créativité · Autonomie · Stratégie RS · Montage",
                     "Helvetica", 9.5, COL_W):
    c.drawString(RX, ry, wrapped)
    ry -= 12.5
ry -= 13

ry = section_title(RX, ry, "Projets mis en avant")
ry = project(RX, ry, "Projet 360° : DEI-Belgique",
             "Campagne de sensibilisation aux VEO pour la DEI-Belgique.",
             ["Vidéo 360°", "Stratégie créative"], "Voir »")
ry = project(RX, ry, "Nocturnz — Portfolio en ligne",
             "Service qui permet à chacun d'avoir son portfolio en ligne, sans abonnement "
             "et sans une ligne de code : moteur, panneau d'édition visuel, sous-domaine "
             "personnalisé.",
             ["HTML/CSS/JS", "Cloudflare Workers"], "Voir »")

c.setFillColorRGB(*ACCENT)
c.setFont("Helvetica-Bold", 9)
voir_plus = "Voir plus →"
c.drawString(RX, ry, voir_plus)
voir_plus_w = c.stringWidth(voir_plus, "Helvetica-Bold", 9)
c.linkURL("https://adam.nocturnz.xyz/projets.html",
          (RX, ry - 2, RX + voir_plus_w, ry + 9), relative=0)
ry -= 13

# ---- icônes réseaux : grandes, au niveau de l'encart "Jobs étudiants"
# (colonne de gauche), centrées sous la colonne de droite
icon_size = 30
icon_gap = 22
socials = [
    ("linkedin", "https://www.linkedin.com/in/adamxbc/"),
    ("instagram", "https://www.instagram.com/_adamdrk"),
]
icons_w = len(socials) * icon_size + (len(socials) - 1) * icon_gap
icon_x0 = RX + COL_W / 2 - icons_w / 2
icon_cy = (jobs_card_top + jobs_card_bottom) / 2
for i, (platform, url) in enumerate(socials):
    social_icon(icon_x0 + i * (icon_size + icon_gap), icon_cy, icon_size, url, platform)

c.save()
print("Écrit :", OUT, "—", os.path.getsize(OUT) // 1024, "Ko")
