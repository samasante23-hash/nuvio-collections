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
 # title with shadow
 lines=["LATEST DIGITAL","RELEASES"] if digital else ["UPCOMING","RELEASES"]
 sizes=[117,136] if digital else [143,136]
 for line,y,sz in zip(lines,[350,490],sizes):
  f=font(sz);box=d.textbbox((0,0),line,font=f);tw=box[2]-box[0]
  x=max(440,(W+380-tw)//2)
  d.text((x+5,y+7),line,font=f,fill=(0,0,0,190))
  d.text((x,y),line,font=f,fill=(244,248,252,255) if y==350 else accent,stroke_width=2,stroke_fill=(12,25,42,255))
 d.text((680,230),"VESPERTV",font=font(56),fill=(227,236,245,235))
 d.rounded_rectangle((680,667,1430,672),radius=3,fill=accent)
 im.save("assets/vespertv-"+("latest-digital" if digital else "upcoming")+"-hero-cinematic.png",optimize=True)
create(True);create(False)
