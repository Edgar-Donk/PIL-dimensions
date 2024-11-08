import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import polar2cart
from DimLinesAA import WideLineAA, leader_aa, dims_aa


wi = 260
ht = 240

thick = 20
back = (255,255,221)

font = ImageFont.truetype('consola.ttf', 12)
#(width, height), (offset_x, offset_y) = Font.font.getsize(text)

image2 = Image.new('RGB', (wi, ht), back)

draw = ImageDraw.Draw(image2)

at = (wi//2 + 20, ht//2)
angle = 0

a = polar2cart(at, angle+90, 30)
b = polar2cart(at, angle-90, 30)
#print(a,b)
c = polar2cart(polar2cart(at, angle, thick), angle+90, 30)
d = polar2cart(polar2cart(at, angle, thick), angle-90, 30)

text = str(a[1] - b[1])

extA = (15, 3)
ptA = a
ptB = b

WideLineAA(draw, a,b, width=2, fill=(0,0,255), back=back)
WideLineAA(draw, c,d, width=2, fill=(0,0,255), back=back)
WideLineAA(draw, a,c, width=2, fill=(0,0,255), back=back)
WideLineAA(draw, b,d, width=2, fill=(0,0,255), back=back)



# dims(im, ptA, ptB, extA, extB=None, text=None, font=None, textorient=None,
        #width=1, fill='black', tail=True, arrowhead=(8, 10, 3), arrow='both')
dims_aa(image2, draw, ptA, ptB, extA, text=text, font=font)

leader_aa(image2, draw, (129,87), angle=135, extA=20, extB=105,
            text='stub extender', font=font)
leader_aa(image2, draw, (136,90), angle=315, extA=20, extB=110,
            text='extension line', font=font)
leader_aa(image2, draw, (132,133), angle=135, extA=20, extB=110,
            text='dimension line', font=font)


image2.show()
#image2.save('../../temp/extender_aa.png')