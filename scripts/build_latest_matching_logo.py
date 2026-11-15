from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from urllib.request import urlopen
from io import BytesIO
import math,os
base=Image.open(BytesIO(urlopen("https://raw.githubusercontent.com/samasante23-hash/nuvio-collections/main/assets/19C31F1E-0E60-4CD7-B2CB-13F6065E848B.png").read())).convert("RGB")
up=Image.open(BytesIO(urlopen("https://raw.githubusercontent.com/samasante23-hash/nuvio-collections/main/assets/VesperTV_Upcoming_Releases_Option2.gif").read()))
up.seek(0)
source=up.convert("RGB")
# Extract exactly the same VesperTV wordmark used on Upcoming Releases.
crop=source.crop((36,31,198,75)).convert("RGBA")
mask=Image.new("L",crop.size)
cp=crop.load();mp=mask.load()
for y in range(crop.height):
 for x in range(crop.width):
  r,g,b,_=cp[x,y]
  # white or violet lettering, exclude dark sky behind it
  white=(r>128 and g>126 and b>126 and abs(r-g)<48)
  purple=(b>r*1.10 and r>54 and b>80)
  mp[x,y]=255 if (white or purple) else 0
mask=mask.filter(ImageFilter.GaussianBlur(.45))
crop.putalpha(mask)
# Preserve the original art and replace only its existing different logo.
w,h=base.size
scale=w/960
cover=Image.new("RGBA",base.size,(0,0,0,0))
draw=ImageDraw.Draw(cover)
box=(int(30*scale),int(17*scale),int(238*scale),int(113*scale))
draw.rounded_rectangle(box,radius=int(13*scale),fill=(7,17,30,255))
blur=cover.getchannel("A").filter(ImageFilter.GaussianBlur(int(14*scale)))
cover.putalpha(blur)
base=Image.alpha_composite(base.convert("RGBA"),cover)
logo_w=int(173*scale);logo_h=int(crop.height*logo_w/crop.width)
logo=crop.resize((logo_w,logo_h),Image.Resampling.LANCZOS)
base.alpha_composite(logo,(int(55*scale),int(43*scale)))
base=base.convert("RGB")
base.thumbnail((800,450),Image.Resampling.LANCZOS)
frames=[]
for i in range(20):
 t=i/20
 z=1+.032*(1-math.cos(2*math.pi*t))/2
 w,h=base.size
 sw,sh=round(w/z),round(h/z)
 f=base.crop(((w-sw)//2,(h-sh)//2,(w+sw)//2,(h+sh)//2)).resize((w,h),Image.Resampling.LANCZOS)
 f=ImageEnhance.Brightness(f).enhance(.98+.045*(1+math.sin(2*math.pi*t))/2)
 frames.append(f.quantize(colors=128))
os.makedirs("assets",exist_ok=True)
frames[0].save("assets/vespertv-latest-matching-upcoming-logo-v3.gif",save_all=True,append_images=frames[1:],duration=110,loop=0,optimize=True)
