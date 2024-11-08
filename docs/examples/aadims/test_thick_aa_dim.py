import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from math import cos, sin, radians
from DimLinesPIL import polar2cart, angled_text
from DimLinesAA import dimension_aa


def thickness_dim_aa(im, dr, ptA, thick, angle=0, text=None, font=None, fill=(0,0,0),
              arrowhead=(8, 10, 3), back=(255,255,221)):
    phir = radians(angle)
    ptB = int(ptA[0] + thick * cos(phir) + 0.5), \
          int(ptA[1] + thick * sin(phir) + 0.5)

    dr.line([ptA, ptB], width=1, fill=fill)

    dimension_aa(im, dr, ptA, angle=angle, arrow='last',fill=fill,back=back)
    dimension_aa(im, dr, ptB, angle=angle, arrow='first',fill=fill,back=back)

    # thickness of item
    # (wide, height) = font.getsize(text)
    unused1, unused2, wide, height = font.getbbox(text)
    h = height // 2
    dx = - (h + arrowhead[1] + 5) * cos(phir)
    dy = - (h + arrowhead[1] + 5) * sin(phir)

    # stop upside down text
    if 0 <= angle <= 180:
        angle = 90-angle
    elif 180 < angle < 360:
        angle = 270-angle

    at = (ptA[0] + int(dx), ptA[1] + int(dy))
    angled_text(im, at, text=text, angle=angle, font=font)


if __name__ == "__main__":
    Text = 'Test'
    Angle = 0
    At = (40, 40)
    Thick = 20
    Font = ImageFont.truetype('consola.ttf', 15)

    image2 = Image.new('RGB', (80, 80), '#FFFFDD')

    draw = ImageDraw.Draw(image2)

    a = polar2cart(At, Angle+90, 30)
    b = polar2cart(At, Angle-90, 30)
    c = polar2cart(polar2cart(At, Angle, Thick), Angle+90, 30)
    d = polar2cart(polar2cart(At, Angle, Thick), Angle-90, 30)
    draw.line([a,b], width=2, fill='blue')
    draw.line([c,d], width=2, fill='blue')

    thickness_dim_aa(image2, draw, At, Thick, angle=Angle, text=Text, font=Font)

    image2.show()
    #image2.save('../figures/thick_dim_'+str(angle)+'.png') #show()


