import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from math import radians, degrees, sin, cos
from DimLinesPIL import polar2cart, int_up, angled_text
from DimLinesAA import WideLineAA, LineAA, dimension_aa

def slant_dim_aa(im, dr, ptA, ptB =None, extA=(8,2),  angle=None, length=None,
              fill=(0,0,0), back=(255,255,221), text=None, font=None, tail=True,
                arrowhead=(8,10,3), arrow='both'):
    # slanting dimension with 45° tails
    # extension tuple first number drawn, second space
    # ptA point on item surface

    if isinstance(extA, int) or len(extA) == 1:
        extO = extA if isinstance(extA, int) else extA[0]
    elif len(extA) == 2:
        extO = sum(extA)
    else:
        raise Exception('slant_dim_aa: The leader tuple extA {} should be one or ' \
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
        raise Exception('slant_dim_aa: Either supply ptB {}, or length {} and ' \
                'angle {}'.format(ptB, length, angle))

    dirn = radians(45 + angle)

    # dimension line
    if tail:
        LineAA(dr, ptC, ptD, fill=fill, back=back)
        # create 45° end stubs
        p3=int_up(ptC[0]+4*cos(dirn)),int_up(ptC[1]+4*sin(dirn))
        p4=int_up(ptC[0]-4*cos(dirn)),int_up(ptC[1]-4*sin(dirn))
        p5=int_up(ptD[0]+4*cos(dirn)),int_up(ptD[1]+4*sin(dirn))
        p6=int_up(ptD[0]-4*cos(dirn)),int_up(ptD[1]-4*sin(dirn))

        LineAA(dr, p3,p4, back=back, fill=fill)
        LineAA(dr, p5,p6, back=back, fill=fill)
    else:
        dimension_aa(im, dr, ptC, ptB=ptD, fill=fill,
                     arrowhead=arrowhead, arrow=arrow)
        
    # extensions, leave a gap if extA 2 entries
    extO = extO if isinstance(extA, int) or len(extA) == 1 else extA[0]
    ptC3 = polar2cart(ptC, angle-90, 3)
    ptCe = polar2cart(ptC, angle+90, extO-1)
    LineAA(dr, ptC3, ptCe, back=back, fill=fill)
    ptD3 = polar2cart(ptD, angle-90, 3)
    ptDe = polar2cart(ptD, angle+90, extO-1)
    LineAA(dr, ptD3, ptDe, back=back, fill=fill)

    font = ImageFont.load_default() if font is None else font
    ft = font.getsize(text)

    h = ft[1] // 2

    angle = 360 + angle if angle < 0 else angle
    angle = angle if angle <= 360 else angle - 360
    
    mid = (ptC[0] + ptD[0])/2, (ptC[1] + ptD[1])/2
    at =  mid[0] + (h + 7) * sin(phir), mid[1] - (h + 7) * cos(phir)
    at = int_up(at[0]), int_up(at[1])
    
    angled_text(im, at, text, angle, font, aall=0)

if __name__ == "__main__":
    Text = 'Test'
    Angle = 330
    ct = (52, 45)
    Length = 40
    exta = (10, 5) #15 #
    Font = ImageFont.truetype('consola.ttf', 15)
    Back = (255,255,221)
    image2 = Image.new('RGB', (80, 80), Back)

    sdraw = ImageDraw.Draw(image2)
    bt = polar2cart(ct, Angle, Length//2)
    At = polar2cart(ct, 180+Angle, Length//2)
    Fill = (0,0,255)
    WideLineAA(sdraw, At, bt, width=2, fill=Fill, back=Back)

    slant_dim_aa(image2,sdraw, At, extA=exta, fill=(0,0,0), length=Length,
                    angle=Angle, back=Back, text=Text, font=Font, tail=True)

    image2.show()
    #image2.save('../../temp/slant_aa_dim_'+str(angle) +'.png')