from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import angled_text, dims, polar2cart, leader


wi = 240
ht = 240

thick = 20

font = ImageFont.truetype('consola.ttf', 12)
#(width, height), (offset_x, offset_y) = Font.font.getsize(text)

image2 = Image.new('RGB', (wi, ht), '#FFFFDD')

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

draw.line([a,b], width=2, fill='blue')
draw.line([c,d], width=2, fill='blue')
draw.line([a,c], width=2, fill='blue')
draw.line([b,d], width=2, fill='blue')



# dims(im, ptA, ptB, extA, extB=None, text=None, font=None, textorient=None,
        #width=1, fill='black', tail=True, arrowhead=(8, 10, 3), arrow='both')
# dims(image2, sdraw, ptA, ptB, Exta, extB=Extb, text=Text, font=Font, tail=True)
image2 = dims(image2, ptA, ptB, extA, extB=extA, text=text, font=font, tail=True)

leader(image2, (120,90), angle=135, extA=20, extB=80, text='stub extender')
leader(image2, (130,90), angle=315, extA=20, extB=90, text='extension line')
leader(image2, (122,135), angle=135, extA=20, extB=90, text='dimension line')


image2.show()
#image2.save('../figures/extender.png')