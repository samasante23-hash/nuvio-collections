from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os
W,H=720,405
os.makedirs("assets",exist_ok=True)
def font(size,bold=True):
 paths=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
 return ImageFont.truetype(paths[0 if bold else 1],size)
def make(which):
 digital=which=="latest"
 frames=[]
 for i in range(8):
  im=Image.new("RGB",(W,H));px=im.load()
  for y in range(H):
   for x in range(W):
    nx=x/W;ny=y/H
    wave=max(0,1-abs(nx-(i/7*.7+.1))/.24)
    light=wave*.21+max(0,1-abs(ny-.62)*2)*.12
    if digital: px[x,y]=(int(5+20*light+10*ny),int(14+88*light+23*ny),int(31+125*light+35*ny))
    else:px[x,y]=(int(19+90*light+28*ny),int(8+45*light+12*ny),int(33+80*light+23*ny))
  d=ImageDraw.Draw(im,"RGBA")
  # Cinematic concentric stage lines, off-axis
  for k in range(7):
   offset=k*18
   d.arc((-180-offset,-140-offset,900+offset,600+offset),192,345,fill=((50,205,255,22) if digital else (244,125,255,22)),width=2)
  # soft filmstrip ribbons
  for j in range(6):
   yy=298+j*10
   d.line([(0,yy+45),(W,yy-25)],fill=((51,175,220,26) if digital else (236,123,176,30)),width=4)
  # left metallic film reel icon
  cx,cy=100,190
  d.ellipse((cx-55,cy-55,cx+55,cy+55),outline=(180,204,222,145),width=5)
  for a in range(5):
   ang=a*math.pi*2/5
   xx=cx+31*math.cos(ang); yy=cy+31*math.sin(ang)
   d.ellipse((xx-11,yy-11,xx+11,yy+11),fill=(4,14,30,220),outline=(155,190,215,120),width=2)
  d.ellipse((cx-8,cy-8,cx+8,cy+8),fill=(215,230,240,160))
  # text clear professional typography
  title="LATEST DIGITAL" if digital else "UPCOMING"
  subtitle="RELEASES"
  tx=200
  f1=font(55 if digital else 65);f2=font(55)
  d.text((tx,121),title,font=f1,fill=(239,246,251,255),stroke_width=1,stroke_fill=(5,18,38,180))
  d.text((tx,194),subtitle,font=f2,fill=((61,225,246,255) if digital else (250,182,96,255)))
  d.rounded_rectangle((tx,276,640,279),radius=2,fill=((58,195,238,150) if digital else (245,166,98,150)))
  d.text((tx,302),"VESPERTV",font=font(22),fill=(196,214,225,190))
  frames.append(im)
 frames[0].save("assets/vespertv-"+("latest-digital" if digital else "upcoming")+"-cinematic.gif",save_all=True,append_images=frames[1:],duration=150,loop=0,optimize=True)
make("latest");make("upcoming")
