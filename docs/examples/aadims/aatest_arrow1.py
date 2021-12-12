import sys
sys.path.append('C:\\Users\\mike\\sphinx\\dims_rev\\docs\\examples\\dims')

from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import polar2cart
from DimLinesAA import slant_dim_aa, WideLineAA

text = 'Test'
angle = 0

at = (60, 60)
ptB = (100, 60)
length = 40
extA = (10, 5) #15 #
font = ImageFont.truetype('consola.ttf', 15)
back = (255,255,221)
image2 = Image.new('RGB', (120, 120), back)

sdraw = ImageDraw.Draw(image2)
ct = polar2cart(at, angle, length)
fill = (0,0,0)
WideLineAA(sdraw, at, ct, width=2, fill=fill, back=back)

slant_dim_aa(image2,sdraw, at, extA=extA, fill=fill, length=length,
                angle=angle, back=back, text=text, font=font) 

image2.show()
#image2.save('../figures/slant_dim_'+str(angle) +'.png') # .show()