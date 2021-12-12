import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from math import atan2, sin, cos, degrees
from DimLinesAA import WideLineAA, LineAA, dimension_aa
from DimLinesPIL import polar2cart, int_up, angled_text

def dims_aa(im, dr, ptA, ptB, extA, extB=None, text=None, font=None, textorient=None,
        fill=(0,0,0), dimsorient=None, arrowhead=(8, 10, 3),
        tail=True, back=(225,225,221)):
    # dimension vertical and horizontal tailed lines with extension lines.
    # ptA, ptB line coords, extA, extB extension lines to measured item, positive
    # to left when vertical or above it when horizontal
    if isinstance(extA, int) or len(extA) == 1:
        extaO = extA if isinstance(extA, int) else extA[0]
    elif len(extA) == 2:
        extaO = sum(extA)
        if extA[0] * extA[1] < 0:
            raise Exception('dims: The extension tuple extA {} should have ' \
                'entries of the same sign'.format(extA))
    else:
        raise Exception('dims_aa: The extension tuple extA {} should be one or ' \
                'two entries'.format(extA))

    if extB is None:
        extB = extA
        extbO = extaO
    elif isinstance(extB, int) or len(extB) == 1:
        extbO = extB if isinstance(extB, int) else extB[0]
    elif len(extB) == 2:
        extbO = sum(extB)
        if extB[0] * extB[1] < 0:
            raise Exception('dims: The extension tuple extB {} should have ' \
                'entries of the same sign'.format(extB))
    else:
        raise Exception('dims: The extension tuple extB {} should be one or ' \
                'two entries, if None then it will equal extA {}'.format(extB, extA))

    if textorient is None or textorient in  ('vertical', 'horizontal', 'h', 'v'):
        pass
    else:
        raise Exception('dims: The textorient {} should be None or' \
                '"horizontal", "h", "vertical" or "v"'.format(textorient))

    if font is None:
        font = ImageFont.load_default()

    (wide, height) = font.getsize(text)

    h = height // 2
    w = wide // 2

    if extaO == extbO:
        phir = atan2(ptB[1]-ptA[1], ptB[0]-ptA[0]) if extaO > 0 else \
                    atan2(ptA[1]-ptB[1], ptA[0]-ptB[0])
        angle = int_up(degrees(phir))
        ptC = polar2cart(ptA, angle-90, abs(extaO))
        ptD = polar2cart(ptB, angle-90, abs(extbO))

    elif dimsorient in ("h", "horizontal"):
        ptC = ptA[0] + extaO, ptA[1]
        ptD = ptB[0] + extbO. ptB[1]
        phir = atan2(ptD[1]-ptC[1], ptD[0]-ptC[0])
        angle = int_up(degrees(phir))
    elif dimsorient in ("v", "vertical"):
        ptC = ptA[0], ptA[1] + extaO
        ptD = ptB[0]. ptB[1] + extbO
        phir = atan2(ptD[1]-ptC[1], ptD[0]-ptC[0])
        angle = int_up(degrees(phir))
    else:
        raise Exception('dims: If the extension lines extA {} extB {} are of ' \
            'unequal length and the same sign, dimsorient {} should be one of ' \
            '"h", "horizontal", "v" or "vertical"'.format(extA, extB, dimsorient))

    # dimension line or tails
    if tail:
        LineAA(dr,ptC, ptD, fill=fill, back=back)
        # create 45° end stubs
        p2 = ptC[0]+3, ptC[1]+3
        p3 = ptC[0]-3, ptC[1]-3
        p4 = ptD[0]+3, ptD[1]+3
        p5 = ptD[0]-3, ptD[1]-3
        LineAA(dr, p2,p3, fill=fill, back=back)
        LineAA(dr, p4,p5, fill=fill, back=back)
    else:
        dimension_aa(im, dr, ptC, ptB=ptD, fill=fill, arrowhead=arrowhead,
                arrow='both')

    # extensions, leave a gap if extA 2 entries
    extaO = extaO if isinstance(extA, int) or len(extA) == 1 else extA[0]
    extbO = extbO if isinstance(extB, int) or len(extB) == 1 else extB[0]

    ptC3 = polar2cart(ptC, angle-90, 3)
    ptCe = polar2cart(ptC, angle+90, abs(extaO)-1) # polar2cart(ptC, angle+90, extaO-1)
    LineAA(dr,ptC3, ptCe, fill=fill, back=back)
    ptD3 = polar2cart(ptD, angle-90, 3)
    ptDe = polar2cart(ptD, angle+90, abs(extbO)-1)
    LineAA(dr,ptD3, ptDe, fill=fill, back=back)

    angle = 360 + angle if angle < 0 else angle
    angle = angle - 360 if angle >= 360 else angle

    dx = 0
    dy = 0
    if ptA[0] == ptB[0]:
        # vertical dimension
        if textorient in ('h', 'horizontal'):
            dx = -w/2 - 5 if extaO > 0 else w/2 + 5
            angle = 0 # text angle
    elif ptA[1] == ptB[1]:
        # horizontal dimension
        if textorient in ('v', 'vertical'):
            dy = +w/2 + 5 if extaO > 0 else -w/2 -5
            angle = 90

    mid = (ptC[0] + ptD[0])/2, (ptC[1] + ptD[1])/2
    at =  mid[0] + (h + 7) * sin(phir) + dx, mid[1] - (h + 7) * cos(phir) + dy
    at = int_up(at[0]), int_up(at[1])
    angled_text(im, at, text=text, angle=angle, font=font, fill=fill, aall=0)

if __name__ == "__main__":


    c = (60,60)
    pta = (c[0]+20, c[1])
    ptb = (c[0]-20, c[1])
    Text = 'Test'

    exta = (-5, -3)
    Font = ImageFont.truetype('consola.ttf', 12)
    Back = (255,255,221)

    image2 = Image.new('RGB', (120, 120), Back)
    sdraw = ImageDraw.Draw(image2)

    WideLineAA(sdraw, pta, ptb, width=2, fill=(0,0,255), back=Back)

    #dims_aa(image2, sdraw, pta, ptb, exta, text=Text, font=Font, tail=False)
    dims_aa(image2, sdraw, pta, ptb, exta, text=Text, font=Font,
            textorient='vertical', tail=False)

    image2.show()
    #image2.save('../../temp/dims_aa'+str(ptA)+'-'+str(ptB)+'.png')