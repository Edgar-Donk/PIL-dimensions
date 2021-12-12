import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import angled_text, dims

Font = ImageFont.truetype('consola.ttf', 12)

w, h = 100, 100
image = Image.new('RGB', (w,h), '#FFFFDD')

a = (30, 10)
b =  (30, 25)
c = (30, 40)
d = (30, 55)

draw = ImageDraw.Draw(image)

draw.line([a, b], fill='black')
draw.line([c, d], fill='black')

width, height = Font.getsize(str(d))

angled_text(image, (a[0] + 10 + width//2, a[1]),text=str(a), angle=0, fill='black',
            font=Font)
angled_text(image, (b[0] + 10 + width//2, b[1]),text=str(b), angle=0, fill='black',
            font=Font)
angled_text(image, (c[0] + 10 + width//2, c[1]),text=str(c), angle=0, fill='black',
            font=Font)
angled_text(image, (d[0] + 10 + width//2, d[1]),text=str(d), angle=0, fill='black',
            font=Font)

dims(image, draw, a, b, (8, 2), extB=(8, 2), text='16', font=Font, fill='red',
        textorient='horizontal')
dims(image, draw, b, c, (8, 2), extB=(8, 2), text='14', font=Font, fill='red',
        textorient='horizontal')
dims(image, draw, c, d, (8, 2), extB=(8, 2), text='16', font=Font, fill='red',
        textorient='horizontal')

image.show()

