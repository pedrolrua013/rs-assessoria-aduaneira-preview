import sys, cv2, numpy as np
from PIL import Image
src=sys.argv[1]
im=Image.open(src).convert('RGBA')
a=np.array(im)
S=8
def trace(mask, eps=1.1):
    m=Image.fromarray(mask).resize((mask.shape[1]*S,mask.shape[0]*S),Image.LANCZOS)
    m=np.array(m); m=cv2.GaussianBlur(m,(0,0),3); _,b=cv2.threshold(m,127,255,cv2.THRESH_BINARY)
    cs,_=cv2.findContours(b,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    d=[]
    for c in cs:
        if cv2.contourArea(c)<40: continue
        c=cv2.approxPolyDP(c,eps,True)
        pts=c.reshape(-1,2)/S
        d.append('M'+' '.join(f'{x:.1f} {y:.1f}' for x,y in pts)+'Z')
    return ''.join(d)
r,g,bb,al=[a[...,i].astype(int) for i in range(4)]
red=((r>120)&(g<90)&(al>20)); gray=((r<120)&(al>20))
def m(sel): return (np.where(sel,al,0)).astype(np.uint8)
ys,xs=np.where(al>20); print('bbox',xs.min(),ys.min(),xs.max(),ys.max())
rd=trace(m(red)); gd=trace(m(gray))
x0,y0,x1,y1=xs.min()-1,ys.min()-1,xs.max()+2,ys.max()+2
open('assets/logo.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1-x0} {y1-y0}"><path fill="#B11116" fill-rule="evenodd" d="{rd}"/><path fill="#3A3A3C" fill-rule="evenodd" d="{gd}"/></svg>')
# mark only
ys2,xs2=np.where(red); mx0,my0,mx1,my1=xs2.min()-1,ys2.min()-1,xs2.max()+2,ys2.max()+2
print('mark',mx0,my0,mx1,my1)
open('assets/mark.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{mx0} {my0} {mx1-mx0} {my1-my0}"><path fill="#B11116" fill-rule="evenodd" d="{rd}"/></svg>')
open('assets/logo-light.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1-x0} {y1-y0}"><path fill="#E0262C" fill-rule="evenodd" d="{rd}"/><path fill="#ffffff" fill-rule="evenodd" d="{gd}"/></svg>')
