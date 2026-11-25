#!/usr/bin/env python3
"""Cria uma variante de cor do vídeo do contêiner (vermelho -> azul-aço), só dentro da área rastreada, e espelha.
Uso: python3 _tools/recolor.py ORIGEM.mp4 SAIDA.mp4 assets/video/crate.json
Depois: encodar como em _tools/video.py e espelhar o JSON (x -> 1 - x - w)."""
import cv2, numpy as np, sys, subprocess
import json
src, out = sys.argv[1], sys.argv[2]
B = json.load(open(sys.argv[3]))['box']; fi = 0
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
W = int(cap.get(3)); H = int(cap.get(4))
p = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(fps),"-i","-","-c:v","libx264","-crf","14","-preset","veryfast","-pix_fmt","yuv420p",out], stdin=subprocess.PIPE)
while True:
    ok, f = cap.read()
    if not ok: break
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[...,0], hsv[...,1], hsv[...,2]
    d = np.minimum(np.abs(h - 0), np.abs(h - 180))            # distância ao vermelho
    wh = np.clip((11 - d) / 5, 0, 1) * np.clip((215 - v) / 30, 0, 1)   # só o vermelho do aço; poupa luzes
    ws = np.clip((s - 45) / 40, 0, 1)
    reg = np.zeros_like(h); b = B[min(fi, len(B)-1)]; fi += 1
    if b:
        x0, y0 = int((b[0]-.01)*W), int((b[1]-.01)*H); x1, y1 = int((b[0]+b[2]+.01)*W), int((b[1]+b[3]+.015)*H)
        reg[max(0,y0):y1, max(0,x0):x1] = 1
    w = cv2.GaussianBlur((wh * ws * reg).astype(np.float32), (5, 5), 0)
    nh = np.full_like(h, 106.0)                                 # azul-aço
    ns = s * 0.62
    nv = np.clip(v * 0.92, 0, 255)
    hsv2 = np.stack([h*(1-w)+nh*w, s*(1-w)+ns*w, v*(1-w)+nv*w], -1)
    g = cv2.cvtColor(hsv2.astype(np.uint8), cv2.COLOR_HSV2BGR)
    p.stdin.write(cv2.flip(g, 1).tobytes())
p.stdin.close(); p.wait()
