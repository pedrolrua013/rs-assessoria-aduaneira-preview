"""Gera as thumbnails (SVG 1200x675) dos artigos do blog na identidade da RS."""
import pathlib, random

W, H = 1200, 675

def bg(theme, seed):
    r = random.Random(seed)
    if theme == "dark":
        base = '<rect width="1200" height="675" fill="#0C0D10"/>'
        glow = f'<circle cx="{r.randint(700,1000)}" cy="{r.randint(150,350)}" r="520" fill="url(#g)"/>'
        grid = "rgba(255,255,255,.05)"
    elif theme == "red":
        base = '<rect width="1200" height="675" fill="url(#rg)"/>'
        glow = '<circle cx="1050" cy="-60" r="420" fill="none" stroke="rgba(255,255,255,.18)"/><circle cx="1050" cy="-60" r="300" fill="none" stroke="rgba(255,255,255,.12)"/>'
        grid = "rgba(255,255,255,.07)"
    else:
        base = '<rect width="1200" height="675" fill="#F4F2EE"/>'
        glow = f'<circle cx="{r.randint(750,1000)}" cy="{r.randint(200,400)}" r="460" fill="url(#gl)"/>'
        grid = "rgba(23,23,26,.06)"
    lines = "".join(f'<path d="M{x} 0V675" stroke="{grid}"/>' for x in range(0, 1201, 60)) + "".join(f'<path d="M0 {y}H1200" stroke="{grid}"/>' for y in range(15, 676, 60))
    defs = '''<defs>
<radialGradient id="g"><stop offset="0" stop-color="#C8151B" stop-opacity=".45"/><stop offset="1" stop-color="#C8151B" stop-opacity="0"/></radialGradient>
<radialGradient id="gl"><stop offset="0" stop-color="#C8151B" stop-opacity=".16"/><stop offset="1" stop-color="#C8151B" stop-opacity="0"/></radialGradient>
<linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8E0D11"/><stop offset=".6" stop-color="#C8151B"/><stop offset="1" stop-color="#E0262C"/></linearGradient>
<linearGradient id="paper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#ECE9E3"/></linearGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="28" stdDeviation="28" flood-color="#000" flood-opacity=".35"/></filter>
<filter id="shl" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="24" stdDeviation="24" flood-color="#5a0a0d" flood-opacity=".18"/></filter>
</defs>'''
    return defs + base + glow + f'<g>{lines}</g>'

def stamp():
    s = bg("light", 1)
    s += '<g filter="url(#shl)" transform="translate(560 120) rotate(-6)"><rect width="400" height="500" rx="18" fill="url(#paper)" stroke="rgba(0,0,0,.06)"/>'
    s += "".join(f'<rect x="44" y="{70+i*44}" width="{300 - (i%3)*60}" height="12" rx="6" fill="#D9D5CE"/>' for i in range(8))
    s += '<rect x="44" y="40" width="160" height="16" rx="8" fill="#17171A"/></g>'
    s += '<g transform="translate(860 470) rotate(-14)"><circle r="120" fill="none" stroke="#C8151B" stroke-width="10"/><circle r="94" fill="none" stroke="#C8151B" stroke-width="3"/><text y="14" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="44" fill="#C8151B" letter-spacing="4">LIBERADO</text></g>'
    s += '<g transform="translate(140 200)"><rect width="250" height="250" rx="40" fill="#0C0D10"/><path d="M80 140l40 40 80-90" fill="none" stroke="#FF5A5F" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/></g>'
    return s

def cycle():
    s = bg("dark", 2)
    s += '<g transform="translate(600 338)" fill="none" stroke-linecap="round">'
    s += '<path d="M-260 0A260 260 0 0 1 220 -140" stroke="#FF5A5F" stroke-width="14"/><path d="M200 -170l30 34-44 8" stroke="#FF5A5F" stroke-width="14" stroke-linejoin="round"/>'
    s += '<path d="M260 0A260 260 0 0 1 -220 140" stroke="rgba(255,255,255,.75)" stroke-width="14"/><path d="M-200 170l-30-34 44-8" stroke="rgba(255,255,255,.75)" stroke-width="14" stroke-linejoin="round"/></g>'
    s += '<g filter="url(#sh)" transform="translate(470 250)"><path d="M0 60l130-50 130 50-130 50z" fill="#E0262C"/><path d="M0 60v110l130 50V110z" fill="#B11116"/><path d="M260 60v110l-130 50V110z" fill="#8E0D11"/>'
    s += "".join(f'<path d="M{20+i*22} {72+i*8}v95" stroke="rgba(0,0,0,.25)" stroke-width="3"/>' for i in range(5)) + '</g>'
    s += '<text x="90" y="590" font-family="Arial,Helvetica,sans-serif" font-size="30" font-weight="700" fill="rgba(255,255,255,.35)" letter-spacing="6">II · IPI · PIS · COFINS</text>'
    return s

def seed():
    s = bg("red", 3)
    s += '<g filter="url(#sh)">'
    for i, (x, y, rot, sc) in enumerate([(380, 360, -20, 1.4), (620, 300, 15, 1.9), (860, 390, 40, 1.3), (500, 520, -50, .9), (760, 540, 60, 1)]):
        s += f'<g transform="translate({x} {y}) rotate({rot}) scale({sc})"><path d="M0 -90C55 -50 70 20 0 90C-70 20 -55 -50 0 -90z" fill="#fff"/><path d="M0 -60V70" stroke="#E7C9CA" stroke-width="6" stroke-linecap="round"/></g>'
    s += '</g><g transform="translate(620 135)" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"><path d="M0 120V0"/><path d="M0 40C0 0-40-20-90-20 -90 30-50 50 0 40z" fill="rgba(255,255,255,.9)" stroke="none"/><path d="M0 20C0-20 40-40 90-40 90 10 50 30 0 20z" fill="rgba(255,255,255,.75)" stroke="none"/></g>'
    return s

def ship():
    s = bg("dark", 4)
    s += '<path d="M0 520C200 490 400 550 600 520S1000 490 1200 520V675H0z" fill="rgba(255,255,255,.04)"/><path d="M0 560C200 530 400 590 600 560S1000 530 1200 560" stroke="rgba(255,255,255,.12)" fill="none" stroke-width="3"/>'
    s += '<g filter="url(#sh)" transform="translate(260 250)"><path d="M0 230h700l-80 90H70z" fill="#E0262C"/>'
    cols = ["#B11116", "#F4F2EE", "#6F7078", "#C8151B", "#F4F2EE", "#3A3B40"]
    for row in range(3):
        for c in range(7):
            col = cols[(row * 3 + c) % len(cols)]
            s += f'<rect x="{90 + c*78}" y="{150 - row*62}" width="72" height="56" rx="4" fill="{col}"/>'
    s += '<rect x="600" y="40" width="70" height="190" rx="6" fill="#F4F2EE"/><rect x="612" y="60" width="46" height="18" rx="4" fill="#17171A"/></g>'
    s += '<g transform="translate(860 90)"><rect width="230" height="150" rx="16" fill="#fff"/>' + "".join(f'<rect x="{24+i*10}" y="30" width="{4 if i%3 else 7}" height="70" fill="#17171A"/>' for i in range(18)) + '<text x="24" y="128" font-family="Arial,Helvetica,sans-serif" font-size="22" font-weight="700" fill="#C8151B">DU-E</text></g>'
    return s

def code():
    s = bg("light", 5)
    s += '<g filter="url(#shl)">'
    parts = ["8201", ".", "10", ".", "00"]
    x = 170
    for p in parts:
        if p == ".":
            s += f'<circle cx="{x+14}" cy="410" r="10" fill="#17171A"/>'; x += 40; continue
        w = 70 * len(p) + 40
        s += f'<rect x="{x}" y="260" width="{w}" height="190" rx="28" fill="{"#0C0D10" if p=="8201" else "#fff"}"/>'
        s += f'<text x="{x+w/2}" y="392" text-anchor="middle" font-family="Courier New,monospace" font-weight="700" font-size="120" fill="{"#fff" if p=="8201" else "#C8151B"}">{p}</text>'
        x += w + 20
    s += '</g><g transform="translate(900 120)" fill="none" stroke="#C8151B" stroke-width="18" stroke-linecap="round"><circle cx="60" cy="60" r="60"/><path d="M105 105l60 60"/></g>'
    s += '<text x="170" y="540" font-family="Arial,Helvetica,sans-serif" font-size="30" font-weight="700" fill="rgba(23,23,26,.35)" letter-spacing="6">SH · NCM · MERCOSUL</text>'
    return s

KINDS = {"stamp": stamp, "cycle": cycle, "seed": seed, "ship": ship, "code": code}

def build(posts, out_dir):
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    for p in posts:
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{KINDS[p["thumb"]]()}</svg>'
        (out / f'{p["slug"]}.svg').write_text(svg)
