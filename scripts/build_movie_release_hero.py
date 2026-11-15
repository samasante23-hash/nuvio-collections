from PIL import Image,ImageDraw,ImageFont,ImageFilter
import math,os,random
W,H=1600,900
os.makedirs("assets",exist_ok=True)
def font(n):
 return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",n)
def create(digital):
 random.seed(24 if digital else 48)
 im=Image.new("RGB",(W,H)); p=im.load()
 for y in range(H):
  for x in range(W):
   r=math.sqrt(((x-W*.56)/W)**2+((y-H*.48)/H)**2)
   glow=max(0,1-r*1.8)
   if digital:p[x,y]=(int(3+12*glow),int(12+37*glow),int(30+69*glow))
   else:p[x,y]=(int(21+49*glow),int(7+15*glow),int(32+58*glow))
 d=ImageDraw.Draw(im,"RGBA")
 accent=(45,196,250,255) if digital else (255,169,69,255)
 # Film reel left side
 cx,cy=240,445
 for rr in (270,251,237):
  d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline=(180,203,218,150) if digital else (225,168,128,155),width=12)
 for k in range(5):
  a=k*math.pi*2/5
  hx=cx+153*math.cos(a);hy=cy+153*math.sin(a)
  d.ellipse((hx-66,hy-66,hx+66,hy+66),fill=(1,8,23,240),outline=(154,183,207,130),width=6)
 d.ellipse((cx-35,cy-35,cx+35,cy+35),fill=(130,156,174,255))
 # filmstrip sweeping bottom
 for k in range(3):
  points=[(x,740+int(48*math.sin(x/200+k*.25))+k*39) for x in range(0,W+1,8)]
  d.line(points,fill=(95,153,198,170) if digital else (202,124,174,170),width=8)
 for x in range(10,W,65):
  y=735+int(48*math.sin(x/200))
  d.rectangle((x,y+15,x+28,y+36),fill=(3,10,26,230))
 # rays
 for i in range(14):
  x=950+i*70
  d.line((x,20,x+120,380),fill=(accent[0],accent[1],accent[2],15),width=2)
 # Atmospheric cinematic background only. The app provides collection titles.
 # Film projector beam on the right, no embedded typography.
 light=(45,171,255,30) if digital else (245,126,96,30)
 for k in range(12):
  y0=80+k*24
  d.polygon([(W,200),(560,y0),(560,y0+13)],fill=(light[0],light[1],light[2],max(3,24-k)))
 for k in range(10):
  rr=55+k*26
  d.arc((980-rr,400-rr,980+rr,400+rr),20,160,fill=(accent[0],accent[1],accent[2],max(5,55-k*5)),width=3)
 # Cinematic horizontal letterbox edge, dark for readability.
 d.rectangle((0,0,W,120),fill=(0,0,0,65))
 d.rectangle((0,H-80,W,H),fill=(0,0,0,55))
 im.save("assets/vespertv-"+("latest-digital" if digital else "upcoming")+"-hero-cinematic.png",optimize=True)
create(True);create(False)

# Trigger publishing workflow.
