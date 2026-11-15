from PIL import Image, ImageEnhance
from urllib.request import urlopen
from io import BytesIO
import math, os
url="https://raw.githubusercontent.com/samasante23-hash/nuvio-collections/main/assets/19C31F1E-0E60-4CD7-B2CB-13F6065E848B.png"
im=Image.open(BytesIO(urlopen(url).read())).convert("RGB")
im.thumbnail((800,450),Image.Resampling.LANCZOS)
frames=[]
for i in range(16):
    phase=math.sin(math.pi*i/8)
    z=1.0+0.012*(1-math.cos(2*math.pi*i/16))/2
    w,h=im.size
    sw,sh=round(w/z),round(h/z)
    frame=im.crop(((w-sw)//2,(h-sh)//2,(w+sw)//2,(h+sh)//2)).resize((w,h),Image.Resampling.LANCZOS)
    frame=ImageEnhance.Brightness(frame).enhance(0.975+0.045*(1+phase)/2)
    frames.append(frame.quantize(colors=128,method=Image.Quantize.MEDIANCUT))
os.makedirs("assets",exist_ok=True)
frames[0].save("assets/vespertv-latest-digital-approved-animated.gif",save_all=True,append_images=frames[1:],duration=120,loop=0,optimize=True)
