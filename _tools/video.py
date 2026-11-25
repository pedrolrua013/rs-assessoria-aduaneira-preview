#!/usr/bin/env python3
"""Prepara um vídeo para ser controlado pelo scroll (hero ou faixas take-N).

Uso:
  python3 _tools/video.py ORIGEM.mp4 hero        -> assets/video/hero.mp4, hero-m.mp4, posters
  python3 _tools/video.py ORIGEM.mp4 take-2      -> assets/video/take-2.mp4, take-2-m.mp4, poster
  Opcional: --x 0.73  (centro horizontal do recorte vertical do mobile, 0 a 1)

Cada frame vira keyframe (-g 1), sem áudio: é o que deixa o vídeo andar e voltar
com o scroll sem travar. Precisa de ffmpeg.
"""
import subprocess, sys, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/video"

def run(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    src, name = args[0], args[1]
    x = float(args[args.index("--x") + 1]) if "--x" in args else 0.5
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", src], capture_output=True, text=True, check=True).stdout)["streams"][0]
    W, H = info["width"], info["height"]
    cw = int(H * 9 / 16) // 2 * 2
    cx = max(0, min(W - cw, int(W * x - cw / 2)))
    crop = f"crop={cw}:{H}:{cx}:0,scale=540:960"
    enc = ["-an", "-c:v", "libx264", "-preset", "veryfast", "-g", "1", "-movflags", "+faststart", "-pix_fmt", "yuv420p"]
    run("-i", src, "-vf", "scale=1280:-2", "-crf", "30", *enc, str(OUT / f"{name}.mp4"))
    run("-i", src, "-vf", crop, "-crf", "31", *enc, str(OUT / f"{name}-m.mp4"))
    run("-i", src, "-vf", "select=eq(n\\,0),scale=1600:-2", "-frames:v", "1", "-c:v", "libwebp", "-quality", "72", str(OUT / f"{name}-poster.webp"))
    run("-i", src, "-vf", f"select=eq(n\\,0),{crop}", "-frames:v", "1", "-c:v", "libwebp", "-quality", "72", str(OUT / f"{name}-poster-m.webp"))
    for f in sorted(OUT.glob(f"{name}*")):
        print(f"{f.relative_to(ROOT)}  {f.stat().st_size/1e6:.1f} MB")

if __name__ == "__main__":
    main()
