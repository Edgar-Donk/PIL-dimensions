import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from math import atan2, degrees, sin, cos
from DimLinesAA import dims_aa, WideLineAA, LineAA
from DimLinesPIL import int_up, polar2cart, angled_text


def dims_aa(im, dr, ptA, ptB, extA, extB=None, text=None, font=None, textorient=None,
        fill=(0,0,0), tail=True, arrowhead=(8, 10, 3), arrow='both'):
    # vertical and horizontal dimension with extension lines tailed lines ,
    # option to use arrows.
    # ptA, ptB dim coords, extA, extB extension lines to measured item,
    # positive to right when vertical or above it when horizontal
    # read from bottom - unidirectional, read from bottom and right - aligned

    if isinstance(extA, int) or len(extA) == 1:
        exta = extA if isinstance(extA, int) else extA[0]
    elif len(extA) == 2:
        exta = extA[0]
        if extA[0] * extA[1] < 0:
            raise Exception('extA: both entries of extension tuple extA {} ' \
                'should either be positive or negative'.format(extA))
    else:
        raise Exception('extA: The extension tuple extA {} should be one or ' \
                'two entries'.format(extA))
    if extB is None:
        extB = extA
        extb = exta
    elif isinstance(extB, int) or len(extB) == 1:
        extb = extB if isinstance(extB, int) else extB[0]
    elif len(extB) == 2:
        extb = extB[0]
        if extB[0] * extB[1] < 0:
            raise Exception('extB: The extension tuple extB {} should be one or ' \
                'two entries, if None then it will equal extA {}'.format(extB, extA))
    if textorient is not None and textorient not in  ('vertical', 'horizontal', 'h', 'v'):
        raise Exception('dims: textorient {} should be None or' \
                '"horizontal", "h", "vertical" or "v"'.format(textorient))

    font = ImageFont.load_default() if font is None else font
    # (wide, height)= font.getsize(text)
    unused1, unused2, wide, height = font.getbbox(text)

    h = height // 2
    w = wide // 2

    dx = dy = 0
    if ptA[0] == ptB[0]:
        # vertical dimension
        ang = 270 if exta > 0 else 90
        if textorient is None or textorient in ('vertical', 'v'):
            dx = -h -5 if exta > 0 else h+5 # text positioning
            phi = 90                        # text angle
        elif textorient in ('horizontal', 'h'):
            dx = -w - 5 if exta > 0 else w + 5
            phi = 0                         # text angle

    elif ptA[1] == ptB[1]:
        # horizontal dimension
        ang = 0 if exta > 0 else 180
        if textorient is None or textorient in ('horizontal', 'h'):
            dy = -h -5 if exta > 0 else +h +5
            phi = 0                        # text angle
        elif textorient in ('vertical', 'v'):
            dy = -w -5 if exta > 0 else +w +5 # text positioning
            phi = 90

    else:
        raise Exception('dims: should be vertical or horizontal '\
                        '{} {} coordinates'.format(ptA, ptB))


    # dimension line or tails
    if tail:
        LineAA(dr,ptA, ptB, fill=fill, back=back)
        # create 45° end stubs
        p2 = ptA[0]+3, ptA[1]+3
        p3 = ptA[0]-3, ptA[1]-3
        p4 = ptB[0]+3, ptB[1]+3
        p5 = ptB[0]-3, ptB[1]-3
        LineAA(dr, p2,p3, fill=fill, back=back)
        LineAA(dr, p4,p5, fill=fill, back=back)
    else:
        dimension_aa(im, dr, ptC, ptB=ptD, fill=fill, arrowhead=arrowhead,
                arrow='both')

    # extensions, leave a gap if extA 2 entries
    ptA3 = polar2cart(ptA, ang-90, 3)
    ptAe = polar2cart(ptA, ang+90, abs(exta))
    LineAA(dr,ptA3, ptAe, fill=fill, back=back)
    ptB3 = polar2cart(ptB, ang-90, 3)
    ptBe = polar2cart(ptB, ang+90, abs(extb))
    LineAA(dr,ptB3, ptBe, fill=fill, back=back)

    at = (ptA[0]+ptB[0])//2+dx,(ptA[1]+ptB[1])//2+dy

    angled_text(im, at, text=text, angle=phi, font=font, fill=fill, aall=0)

if __name__ == "__main__":

    c = (60,60)
    ptA = (c[0],c[1]-20) # (40, 60)
    ptB = (c[0],c[1]+20) # (80, 60)
    text = 'Text' #str(ptA)+','+ str(ptB)

    extA = (5, 3)
    extB = (10,3)
    atot = sum(extA)
    btot = sum(extB)
    font = ImageFont.truetype('consola.ttf', 12)
    back = (255,255,221)
    image2 = Image.new('RGB', (120, 120), back)
    sdraw = ImageDraw.Draw(image2)
    if ptA[0] == ptB[0]:
        WideLineAA(sdraw, (ptA[0]+atot, ptA[1]), (ptB[0]+btot, ptB[1]),
                fill=(0,0,255), back=back, width=2)
    else:
        WideLineAA(sdraw, (ptA[0], ptA[1]+atot), (ptB[0], ptB[1]+btot),
                fill=(0,0,255), back=back, width=2)

    dims_aa(image2,sdraw, ptA, ptB, extA, extB=extB, text=text, font=font)

    image2.show()
    #image2.save('../../temp/dims_aa'+str(ptA)+'-'+str(ptB)+'.png')