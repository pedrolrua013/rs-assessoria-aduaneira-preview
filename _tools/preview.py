#!/usr/bin/env python3
"""Gera uma cópia de pré-visualização com caminhos relativos (para abrir sem servidor ou publicar como artifact).
Uso: python3 _tools/preview.py <pasta_saida>"""
import os, re, sys, shutil, base64, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent.parent
out = pathlib.Path(sys.argv[1]).resolve()
if out.exists(): shutil.rmtree(out)
subprocess.run([sys.executable, str(ROOT / "_tools/build_pages.py")], env={**os.environ, "OUT": str(out)}, check=True, stdout=subprocess.DEVNULL)
font = base64.b64encode((ROOT / "assets/fonts/inter-display-600.woff").read_bytes()).decode()
css = (out / "assets/site.css").read_text()
css = css.replace("url(/assets/fonts/inter-display-600.woff)", f"url(data:font/woff;base64,{font})")
(out / "assets/site.css").write_text(css)
for f in out.rglob("*.html"):
    depth = len(f.relative_to(out).parts) - 1
    pre = "../" * depth or "./"
    s = f.read_text()
    def fix(m):
        attr, path = m.group(1), m.group(2)
        frag = ""
        if "#" in path: path, frag = path.split("#", 1); frag = "#" + frag
        if path == "": target = pre + "index.html"
        elif path.endswith("/"): target = pre + path + "index.html"
        else: target = pre + path
        return f'{attr}="{target}{frag}"'
    s = re.sub(r'(href|src)="/(?!/)([^"]*)"', fix, s)
    s = s.replace(f'href="{pre}index.html#', 'href="#') if depth == 0 else s
    s = re.sub(r'<link rel="preload"[^>]*>\n', "", s)
    f.write_text(s)
for junk in ["vercel.json", "robots.txt", "sitemap.xml"]:
    (out / junk).unlink(missing_ok=True)
print("preview ok:", out)
