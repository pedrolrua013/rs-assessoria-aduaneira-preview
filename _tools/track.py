#!/usr/bin/env python3
"""Rastreia a lateral do contêiner quadro a quadro num vídeo de câmera parada.

Uso: python3 _tools/track.py VIDEO.mp4 assets/video/crate-a.json [--red] [--debug pasta]
--red: rastreia pela cor (contêiner vermelho), sem precisar de fundo limpo no fim.

Como a câmera não se move e o contêiner sai do quadro no fim, o último quadro é
um "fundo limpo". A diferença de cada quadro para ele é o contêiner (+ spreader e cabos).
Cabos finos somem com uma abertura morfológica; o spreader é cortado porque as linhas
do corpo do contêiner são quase totalmente preenchidas e as do spreader não.
Saída: {"fps":24,"frames":N,"aspect":W/H,"box":[[x,y,w,h] normalizado 0-1 ou null, ...]}
"""
import sys, json, subprocess, pathlib
import numpy as np
import cv2

def frames(path, w=640):
    cap = cv2.VideoCapture(str(path))
    out = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        h = int(f.shape[0] * w / f.shape[1])
        out.append(cv2.resize(f, (w, h), interpolation=cv2.INTER_AREA))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    return out, fps

def box_for(f, plate, k):
    if plate is None:  # modo cor: contêiner vermelho saturado contra o porto azulado
        hsv = cv2.cvtColor(cv2.GaussianBlur(f, (5, 5), 0), cv2.COLOR_BGR2HSV)
        hue, sat, val = hsv[..., 0], hsv[..., 1], hsv[..., 2]
        m = (((hue <= 10) | (hue >= 165)) & (sat > 70) & (val > 35)).astype(np.uint8)
    else:
        d = cv2.absdiff(cv2.GaussianBlur(f, (5, 5), 0), cv2.GaussianBlur(plate, (5, 5), 0)).max(axis=2)
        m = (d > 28).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2:
        return None
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    if st[i, cv2.CC_STAT_AREA] < m.size * 0.01:
        return None
    blob = (lab == i)
    x0, y0, bw, bh = st[i, :4]
    sub = blob[y0:y0 + bh, x0:x0 + bw]
    cols = sub.mean(axis=0)
    xs = np.where(cols > 0.35)[0]
    if not len(xs):
        return None
    cx0, cx1 = xs[0], xs[-1] + 1
    rows = sub[:, cx0:cx1].mean(axis=1)
    ys = np.where(rows > 0.82)[0]          # linhas do corpo: quase cheias (spreader não)
    if not len(ys):
        return None
    # maior trecho contínuo de linhas cheias = corpo do contêiner
    runs = np.split(ys, np.where(np.diff(ys) > 2)[0] + 1)
    r = max(runs, key=len)
    H, W = m.shape
    return [(x0 + cx0) / W, (y0 + r[0]) / H, (cx1 - cx0) / W, (r[-1] + 1 - r[0]) / H]

def smooth(boxes, win=2):
    out = []
    for i, b in enumerate(boxes):
        if b is None:
            out.append(None); continue
        near = [boxes[j] for j in range(max(0, i - win), min(len(boxes), i + win + 1)) if boxes[j] is not None]
        out.append([round(float(np.median([n[c] for n in near])), 4) for c in range(4)])
    return out

def hold(boxes):
    """Quadro de "pausa": a maior lateral entre os quadros do meio do vídeo (usado no poster)."""
    n = len(boxes); best, bi = -1, n // 2
    for i in range(n // 4, 3 * n // 4):
        b = boxes[i]
        if b and b[2] * b[3] > best:
            best, bi = b[2] * b[3], i
    return bi

def main():
    src, dst = sys.argv[1], sys.argv[2]
    dbg = sys.argv[sys.argv.index("--debug") + 1] if "--debug" in sys.argv else None
    fs, fps = frames(src)
    plate = None if "--red" in sys.argv else fs[-1]
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    raw = [box_for(f, plate, k) for f in fs]
    # continuidade: caixa que encolhe ou salta demais de um quadro para o outro é erro -> mantém a anterior
    prev = None
    for i, b in enumerate(raw):
        if b and prev:
            area, parea = b[2] * b[3], prev[2] * prev[3]
            jump = abs((b[0] + b[2] / 2) - (prev[0] + prev[2] / 2)) + abs((b[1] + b[3] / 2) - (prev[1] + prev[3] / 2))
            if area < parea * 0.7 or area > parea * 1.4 or jump > 0.12:
                raw[i] = b = list(prev)
        if b:
            prev = b
    boxes = smooth(raw)
    # caixa ausente no meio (oclusão) -> repete a anterior; nas pontas fica null (fora do quadro)
    H, W = fs[0].shape[:2]
    pathlib.Path(dst).write_text(json.dumps({"fps": fps, "frames": len(fs), "aspect": round(W / H, 4), "hold": hold(boxes), "box": boxes}, separators=(",", ":")))
    seen = [i for i, b in enumerate(boxes) if b]
    print(f"{len(fs)} quadros, contêiner em {len(seen)} ({seen[0] if seen else '-'}..{seen[-1] if seen else '-'})")
    if dbg:
        p = pathlib.Path(dbg); p.mkdir(parents=True, exist_ok=True)
        for i in range(0, len(fs), max(1, len(fs) // 12)):
            f = fs[i].copy()
            if boxes[i]:
                x, y, w, h = boxes[i]
                cv2.rectangle(f, (int(x * W), int(y * H)), (int((x + w) * W), int((y + h) * H)), (0, 255, 0), 2)
            cv2.imwrite(str(p / f"{i:03d}.jpg"), f)

if __name__ == "__main__":
    main()
