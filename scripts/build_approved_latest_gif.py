from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
from urllib.request import urlopen
from io import BytesIO
import math, os
url="https://raw.githubusercontent.com/samasante23-hash/nuvio-collections/main/assets/19C31F1E-0E60-4CD7-B2CB-13F6065E848B.png"
im=Image.open(BytesIO(urlopen(url).read())).convert("RGB")
im.thumbnail((800,450),Image.Resampling.LANCZOS)
frames=[]
for i in range(24):
    t=i/24
    # Noticeable slow push in, returning seamlessly to original framing.
    z=1.0+0.035*(1-math.cos(2*math.pi*t))/2
    w,h=im.size
    sw,sh=round(w/z),round(h/z)
    frame=im.crop(((w-sw)//2,(h-sh)//2,(w+sw)//2,(h+sh)//2)).resize((w,h),Image.Resampling.LANCZOS).convert("RGBA")
    # Moving blue cinematic light on the right, leaving the approved logo and text intact.
    light=Image.new("RGBA",(w,h),(0,0,0,0))
    draw=ImageDraw.Draw(light,"RGBA")
    cx=int(w*(.52+.36*t))
    draw.ellipse((cx-100,int(h*.3),cx+100,int(h*1.25)),fill=(50,140,255,70))
    light=light.filter(ImageFilter.GaussianBlur(55))
    frame=Image.alpha_composite(frame,light).convert("RGB")
    frame=ImageEnhance.Brightness(frame).enhance(.98+.06*(1+math.sin(2*math.pi*t))/2)
    frames.append(frame.quantize(colors=128,method=Image.Quantize.MEDIANCUT))
os.makedirs("assets",exist_ok=True)
frames[0].save("assets/vespertv-latest-digital-approved-animated-v2.gif",save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True)
