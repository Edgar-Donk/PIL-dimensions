import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import angled_text, dims

Font = ImageFont.truetype('consola.ttf', 12)

w, h = 100, 100
image = Image.new('RGB', (w,h), '#FFFFDD')

a = (30, 10)
b = (30, 24)
c = (30, 40)
d = (30, 54)
e = (30, 70)
f = (30, 84)

draw = ImageDraw.Draw(image)

draw.line([a, b], fill='black')
draw.line([c, d], fill='black')
draw.line([e,f], fill='black')

width, height = Font.getsize(str(d))

angled_text(image, (a[0] + 10 + width//2, a[1]),text=str(a), angle=0, fill='black',
            font=Font)
angled_text(image, (b[0] + 10 + width//2, b[1]),text=str(b), angle=0, fill='black',
            font=Font)
angled_text(image, (c[0] + 10 + width//2, c[1]),text=str(c), angle=0, fill='black',
            font=Font)
angled_text(image, (d[0] + 10 + width//2, d[1]),text=str(d), angle=0, fill='black',
            font=Font)
angled_text(image, (e[0] + 10 + width//2, e[1]),text=str(e), angle=0, fill='black',
            font=Font)
angled_text(image, (f[0] + 10 + width//2, f[1]),text=str(f), angle=0, fill='black',
            font=Font)


dims(image, draw, a, b, (8, 2), extB=(8, 2), text='16', font=Font, fill='lightblue',
        textorient='horizontal')
dims(image, draw, b, c, (8, 2), extB=(8, 2), text='14', font=Font, fill='lightblue',
        textorient='horizontal')
dims(image, draw, c, d, (8, 2), extB=(8, 2), text='16', font=Font, fill='lightblue',
        textorient='horizontal')
dims(image, draw, d, e, (8, 2), extB=(8, 2), text='14', font=Font, fill='lightblue',
        textorient='horizontal')
dims(image, draw, e, f, (8, 2), extB=(8, 2), text='16', font=Font, fill='lightblue',
        textorient='horizontal')

image.show()

