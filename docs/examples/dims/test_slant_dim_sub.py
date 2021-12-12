from PIL import Image, ImageDraw, ImageFont
from math import radians, atan2, sin, cos, degrees
from DimLinesPIL import polar2cart, int_up, angled_text


def slant_dim(im, dr, ptA, ptB=None, extA=None,  angle=None, length=None,
              fill=(0,0,0), text=None, font=None):
    # slanting dimension with 45° tails
    # extension tuple first number drawn, second space
    # ptA point on item surface

    if isinstance(extA, int) or len(extA) == 1:
        extO = extA if isinstance(extA, int) else extA[0]
    elif len(extA) == 2:
        extO = sum(extA)
    else:
        raise Exception('slant_dim: The leader tuple extA {} should be one or ' \
                'two entries'.format(extA))

    if ptB is None and length and 0 <= angle <360:
        phir = radians(angle)
        ptC = polar2cart(ptA, angle-90, extO)
        ptD = polar2cart(ptC, angle, length)
    elif length is None and ptB:
        phir = atan2(ptB[1]-ptA[1], ptB[0]-ptA[0])
        angle = int_up(degrees(phir))
        ptC = polar2cart(ptA, angle-90, extO)
        ptD = ptC[0] + (ptB[0] - ptA[0]), ptC[1] + (ptB[1] - ptA[1])
    else:
        raise Exception('slant_dim: Either supply ptB {}, or length {} and ' \
                'angle {}'.format(ptB, length, angle))

    dirn = radians(45 + angle)

    # dimension line
    dr.line([ptC, ptD], width=1, fill=fill)

    # extensions, leave a gap if extA 2 entries
    extO = extO if isinstance(extA, int) or len(extA) == 1 else extA[0]
    ptC3 = polar2cart(ptC, angle-90, 3)
    ptCe = polar2cart(ptC, angle+90, extO-1)
    dr.line([ptC3, ptCe], width=1, fill=fill)
    ptD3 = polar2cart(ptD, angle-90, 3)
    ptDe = polar2cart(ptD, angle+90, extO-1)
    dr.line([ptD3, ptDe], width=1, fill=fill)

    # create 45° end stubs
    p3=ptC[0]+7*cos(dirn),ptC[1]+7*sin(dirn)
    p4=ptC[0]-7*cos(dirn),ptC[1]-7*sin(dirn)
    p5=ptD[0]+7*cos(dirn),ptD[1]+7*sin(dirn)
    p6=ptD[0]-7*cos(dirn),ptD[1]-7*sin(dirn)

    dr.line([p3,p4], width=1, fill=fill)
    dr.line([p5,p6], width=1, fill=fill)

    font = ImageFont.load_default() if font is None else font
    tsize = font.getsize(text)

    h = tsize[1] // 2

    angle = 90 + angle
    angle = 360 + angle if angle < 0 else angle
    angle = angle - 360 if angle >= 360 else angle

    mid = (ptC[0] + ptD[0])/2, (ptC[1] + ptD[1])/2
    at =  mid[0] + (h + 7) * sin(phir), mid[1] - (h + 7) * cos(phir)
    at = int(at[0] + 0.5), int(at[1] + 0.5)

    angled_text(im, at, text, angle, font, aall=0)

if __name__ == "__main__":
    Text = 'Test'
    Angle = 45
    At = (60, 60)
    ptb = (30, 30)
    Length = 50
    exta = (10,) #15 #
    Font = ImageFont.truetype('consola.ttf', 15)

    image2 = Image.new('RGB', (120, 120), '#FFFFDD')

    sdraw = ImageDraw.Draw(image2)
    ct = polar2cart(At, Angle, Length)
    #print(ct,'ct')

    sdraw.line([At, ct], width=2, fill='blue')

    slant_dim(image2, sdraw, At, extA=exta, fill=(0,0,0), length=Length,
                    angle=Angle, text=Text, font=Font) #

    image2.show()
    #image2.save('../figures/slant_dim_'+str(angle) +'.png')