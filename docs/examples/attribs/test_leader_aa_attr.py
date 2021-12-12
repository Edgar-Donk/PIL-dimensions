import sys
sys.path.append('../dims')

#from PIL import Image, ImageDraw
from math import atan2, radians, sin, cos, sqrt
from DimLinesPIL import polar2cart, int_up, angled_text
from DimLinesattr import aq, LineATTR, polyATTR

def dimension_attr(ptA, ptB=None, angle=None, arrow='both'):
    #print(ar.arrow, 'dims1')
    d1, d2, d3 = aq.arrowhead
    # extract dims from tuples
    x0, y0 = ptA
    if angle is None and ptB:
        x1, y1 = ptB
        phi = atan2(y1-y0, x1-x0)

    elif ptB is None and isinstance(angle, int):
        x1,y1 = ptA
        phi = radians(angle)
    else:
        raise Exception('dimension_attr: Either supply ptB {} or angle {} not both' \
                .format(ptB, angle))

    # perpendicular distance shaft to arrow tip
    el = int(sqrt(d2 * d2 - d3 * d3) + 0.5)
    cx2, cy2 = ptA
    if ptB:
        cx3, cy3 = ptB

    if arrow in ('first', 'both'):
        cx0 = int_up(x0 + d1 * cos(phi))
        cy0 = int_up(y0 + d1 * sin(phi))
        ex0 = int_up(x0 + el * cos(phi))
        ey0 = int_up(y0 + el * sin(phi))
        fx0 = int_up(ex0 + d3 * sin(phi))
        fy0 = int_up(ey0 - d3 * cos(phi))
        gx0 = int_up(ex0 - d3 * sin(phi))
        gy0 = int_up(ey0 + d3 * cos(phi))
        polyATTR([(x0, y0), (fx0, fy0), (cx0, cy0),(gx0, gy0)])
        cx2 = cx0
        cy2 = cy0

    if arrow in ('last', 'both'):
        cx1 = int_up(x1 - d1 * cos(phi))
        cy1 = int_up(y1 - d1 * sin(phi))
        ex0 = int_up(x1 - el * cos(phi))
        ey0 = int_up(y1 - el * sin(phi))
        fx0 = int_up(ex0 + d3 * sin(phi))
        fy0 = int_up(ey0 - d3 * cos(phi))
        gx0 = int_up(ex0 - d3 * sin(phi))
        gy0 = int_up(ey0 + d3 * cos(phi))
        polyATTR([(x1, y1), (fx0, fy0), (cx1, cy1), (gx0, gy0)])
        cx3 = cx1
        cy3 = cy1

        if ptB:
            LineATTR((cx2, cy2), (cx3, cy3))
    #print(ar.arrow, 'dims2')

def leader_attr(at, angle=315, extA=20, extB=20, text=None):
    # leader to object, angle and length (extA) first part, then goes horizontal
    # for second part (extB). Only one arrow where leader points.
    # start at,

    (wide, height) = aq.font.getsize(text)

    h = height // 2

    if wide > extB:
        print('extB was increased from:',extB,'to accommodate the text',wide+10)
        extB = wide+10

    # dimension line
    phi = 180 if 90 < angle < 270 else 0
    ptB = polar2cart(at, angle, extA)
    ptC = polar2cart(ptB, phi, extB)
    ptD = polar2cart(at, angle, aq.arrowhead[0])
    #ar = arr(arrow='first')
    dimension_attr(at, ptB, arrow='first')
    #ar = arr(arrow='both')
    LineATTR(ptB, ptC)
    LineATTR(ptB, ptD)

    # text position
    tp = ((ptB[0] + ptC[0])//2, ptB[1] - h - 5)

    angled_text(aq.image, tp, text, 0, aq.font)

if __name__ == "__main__":
    Text = 'y+ε+m'

    #font = ImageFont.truetype('consola.ttf', 12)
    (wi, ht) = aq.font.getsize(Text)

    eb = wi + 10
    #back = (225,225,221)
    #dc.image = Image.new('RGB', (120, 120), dc.back)
    # Get drawing context
    #dc.draw = ImageDraw.Draw(dc.image)

    lat = (60, 60)
    a = 45
    #fill = (0,0,0)
    leader_attr(lat, angle=a, extB=45, text=Text)

    aq.image.show()
    #image2.save('../figures/leader'+str(a)+'.png')



