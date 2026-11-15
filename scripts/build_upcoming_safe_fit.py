from PIL import Image, ImageFilter, ImageEnhance
from urllib.request import urlopen
from io import BytesIO
import os
source="https://raw.githubusercontent.com/samasante23-hash/nuvio-collections/main/assets/VesperTV_Upcoming_Releases_Option2.gif"
raw=urlopen(source).read()
gif=Image.open(BytesIO(raw))
frames=[]
for i in range(getattr(gif,"n_frames",1)):
 gif.seek(i)
 original=gif.convert("RGB")
 w,h=original.size
 # Preserve the exact approved frame, but inset it within a safe zone so TV overscan cannot clip branding.
 backdrop=original.resize((w,h),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(max(16,w//20)))
 backdrop=ImageEnhance.Brightness(backdrop).enhance(.28)
 inset_w=int(w*.76)
 inset_h=int(h*.76)
 inset=original.resize((inset_w,inset_h),Image.Resampling.LANCZOS)
 backdrop.paste(inset,((w-inset_w)//2,(h-inset_h)//2))
 frames.append(backdrop.quantize(colors=128,method=Image.Quantize.FASTOCTREE))
os.makedirs("assets",exist_ok=True)
frames[0].save("assets/vespertv-upcoming-option2-safe-fit.gif",save_all=True,append_images=frames[1:],duration=110,loop=0,optimize=True,disposal=2)
