"""Builds the site: copies the App Store screenshots (en/de) as JPGs, fills the gallery in index.html
and writes privacy.html and support.html with the shared navigation and footer.
Run from the site folder: python3 src/build.py
"""
import glob
import os
import re
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.expanduser("~/Developer/kleiner reparirer")
SHOTS = os.path.join(GAME, "marketing", "appstore")

os.chdir(SITE)
os.makedirs("img/shots", exist_ok=True)
names = []
for lang in ["en", "de"]:
    for f in sorted(glob.glob(os.path.join(SHOTS, lang, "[0-9][0-9].png"))):
        n = os.path.basename(f)[:2]
        im = Image.open(f).convert("RGB").resize((1400, 1050), Image.LANCZOS)
        im.save(f"img/shots/{lang}_{n}.jpg", quality=84, optimize=True)
        if lang == "en":
            names.append(n)
if names:
    Image.open(f"img/shots/en_01.jpg").resize((1200, 900)).crop((0, 135, 1200, 765)).save("img/og.jpg", quality=85)

index = open("index.html", encoding="utf-8").read()
gallery = "\n".join(
    f'      <img data-l="en" class="shot" src="img/shots/en_{n}.jpg" alt="" loading="lazy" width="1400" height="1050">'
    f'<img data-l="de" class="shot" src="img/shots/de_{n}.jpg" alt="" loading="lazy" width="1400" height="1050">'
    for n in names[1:])
index = re.sub(r"(<div class=\"gallery\">).*?(\n    </div>)", lambda m: m.group(1) + "\n" + gallery + m.group(2), index, flags=re.S)
open("index.html", "w", encoding="utf-8").write(index)

head = index[:index.index("<title>")]
nav = re.search(r"<nav class=\"wrap\">.*?</nav>", index, re.S).group(0)
footer = re.search(r"<!--FOOTER-->.*?<!--/FOOTER-->", index, re.S).group(0)


def page(name, title, body):
    html = f"{head}<title>{title} – Kleiner Reparierer</title>\n</head>\n<body>{nav}\n\n<main class=\"wrap doc\">\n{body}\n</main>\n{footer}\n</body>\n</html>\n"
    open(name, "w", encoding="utf-8").write(html)


page("privacy.html", "Privacy", open("src/privacy.html", encoding="utf-8").read())
page("support.html", "Support", open("src/support.html", encoding="utf-8").read())
print(len(names), "screenshots, pages written")
