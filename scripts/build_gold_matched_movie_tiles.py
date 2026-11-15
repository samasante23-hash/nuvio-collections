from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from urllib.request import urlopen
from io import BytesIO
import math, os
ROOT="https://raw.githubusercontent.com/samasante23-hash/nuvio-collections/main/assets/"
latest=Image.open(BytesIO(urlopen(ROOT+"19C31F1E-0E60-4CD7-B2CB-13F6065E848B.png").read())).convert("RGB")
upgif=Image.open(BytesIO(urlopen(ROOT+"VesperTV_Upcoming_Releases_Option2.gif").read()))
upgif.seek(0)
upcoming=upgif.convert("RGB")
# Use the same exact Upcoming Releases logo for both cards.
# This source region is the small VesperTV wordmark in the upper left.
sw,sh=upcoming.size
logo=upcoming.crop((round(sw*.035),round(sh*.055),round(sw*.207),round(sh*.145))).convert("RGBA")
alpha=Image.new("L",logo.size)
lp=logo.load();ap=alpha.load()
for y in range(logo.height):
 for x in range(logo.width):
  r,g,b,_=lp[x,y]
  white=(r>135 and g>130 and b>130 and max(r,g,b)-min(r,g,b)<65)
  violet=(b>r*1.08 and r>65 and b>110)
  ap[x,y]=255 if white or violet else 0
logo.putalpha(alpha.filter(ImageFilter.GaussianBlur(.45)))
W,H=960,540
os.makedirs("assets",exist_ok=True)
for key,art in [("latest",latest),("upcoming",upcoming)]:
 art=art.resize((W,H),Image.Resampling.LANCZOS).convert("RGBA")
 # Remove old branding from the source by covering only the upper left logo area.
 # Both cards use the same dark inset with the identical logo and same position.
 back=art.convert("RGB").filter(ImageFilter.GaussianBlur(36))
 back=ImageEnhance.Brightness(back).enhance(.18).convert("RGBA")
 card=Image.new("RGBA",(W,H),(0,0,0,0))
 inset=(42,33,918,507)
 content=art.crop((0,0,W,H)).resize((inset[2]-inset[0],inset[3]-inset[1]),Image.Resampling.LANCZOS)
 card.alpha_composite(content,(inset[0],inset[1]))
 # Patch old logo region with dark navy tint, then apply identical source wordmark.
 draw=ImageDraw.Draw(card,"RGBA")
 draw.rounded_rectangle((inset[0]+16,inset[1]+14,inset[0]+220,inset[1]+83),radius=9,fill=(7,18,31,245))
 logo_resized=logo.resize((155,round(155*logo.height/logo.width)),Image.Resampling.LANCZOS)
 card.alpha_composite(logo_resized,(inset[0]+35,inset[1]+27))
 mask=Image.new("L",(W,H),0)
 md=ImageDraw.Draw(mask)
 md.rounded_rectangle(inset,radius=17,fill=255)
 # Composite with a consistent gold border and safe padding.
 frames=[]
 for i in range(20):
  t=i/20
  f=Image.alpha_composite(back,card)
  border=ImageDraw.Draw(f,"RGBA")
  border.rounded_rectangle((40,31,920,509),radius=19,outline=(245,185,68,255),width=5)
  glow=Image.new("RGBA",(W,H),(0,0,0,0))
  gd=ImageDraw.Draw(glow,"RGBA")
  cx=round(400+280*t)
  gd.ellipse((cx-80,120,cx+80,460),fill=(40,135,240,40))
  glow=glow.filter(ImageFilter.GaussianBlur(65))
  f=Image.alpha_composite(f,glow)
  f=ImageEnhance.Brightness(f.convert("RGB")).enhance(.99+.035*(1+math.sin(2*math.pi*t))/2)
  frames.append(f.quantize(colors=128))
 frames[0].save("assets/vespertv-"+key+"-gold-matched-v5.gif",save_all=True,append_images=frames[1:],duration=120,loop=0,optimize=True)
 # Background with no giant visible lettering, only dark blurred atmosphere.
 hero=ImageEnhance.Brightness(art.convert("RGB").filter(ImageFilter.GaussianBlur(85))).enhance(.16)
 hero.save("assets/vespertv-"+key+"-dark-hero-v5.png",optimize=True)
