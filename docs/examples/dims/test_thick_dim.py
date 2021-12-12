from PIL import Image, ImageDraw, ImageFont
from math import radians, sin, cos
from DimLinesPIL import polar2cart, dimension, angled_text

def thickness_dim(im, dr, ptA, thick, angle=0, text=None, font=None, width=1, fill=(0,0,0),
              arrowhead=(8, 10, 3), arrow='last'):
    phir = radians(angle)
    ptB = int(ptA[0] + thick * cos(phir) + 0.5), \
          int(ptA[1] + thick * sin(phir) + 0.5)

    # Get drawing context
    tdraw = ImageDraw.Draw(im)

    tdraw.line([ptA, ptB], width=width, fill=fill)

    dimension(dr, ptA, angle=angle, arrow='last')
    dimension(dr, ptB, angle=angle, arrow='first')

    # thickness of item
    phir = radians(angle)
    tsize = font.getsize(text)
    
    h = tsize[1] // 2
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
    #(width, height), (offset_x, offset_y) = Font.font.getsize(text)

    image2 = Image.new('RGB', (80, 80), '#FFFFDD')

    draw = ImageDraw.Draw(image2)
    a = polar2cart(At, Angle+90, 30)
    b = polar2cart(At, Angle-90, 30)
    c = polar2cart(polar2cart(At, Angle, Thick), Angle+90, 30)
    d = polar2cart(polar2cart(At, Angle, Thick), Angle-90, 30)
    draw.line([a,b], width=2, fill='blue')
    draw.line([c,d], width=2, fill='blue')

    thickness_dim(image2, draw, At, Thick, angle=Angle, text=Text, font=Font)

    image2.show()
    #image2.save('../figures/thickness_dim_'+str(Angle)+'.png') #show()


