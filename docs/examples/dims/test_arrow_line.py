from PIL import Image, ImageDraw
from math import atan2, sin, cos, radians, sqrt

def dimension(dr, ptA, ptB=None, angle=None, width=1, fill=(0,0,0),
                arrowhead=(8, 10, 3), arrow='last'):

    if isinstance(arrowhead, tuple) and len(arrowhead) == 3:
        d1, d2, d3 = arrowhead
    else:
        raise Exception('dimension: arrowhead {} needs a 3 entry'  \
                'tuple'.format(arrowhead))

    if arrow not in ('first', 'last', 'both'):
        raise Exception('dimension: arrow {} can only be the strings "first",' \
            '"last", "both"'.format(arrow))

    # Get drawing context
    ldraw = ImageDraw.Draw(im)

    # extract dims from tuples
    x0, y0 = ptA
    if angle is None and ptB:
        x1, y1 = ptB
        phi = atan2(y1-y0, x1-x0)
        dr.line((ptA,ptB), width=width, fill=fill)
    elif ptB is None and angle:
        x1,y1 = ptA
        phi = radians(angle)
    else:
        raise Exception('dimension: Either supply ptB {} or angle {} not both' \
                .format(ptB, angle))

    # perpendicular distance shaft to arrow tip
    el = int(sqrt(d2 * d2 - d3 * d3) + 0.5)

    if arrow in ('first', 'both'):
        cx0 = x0 + d1 * cos(phi)
        cy0 = y0 + d1 * sin(phi)
        ex0 = x0 + el * cos(phi)
        ey0 = y0 + el * sin(phi)
        fx0 = ex0 + d3 * sin(phi)
        fy0 = ey0 - d3 * cos(phi)
        gx0 = ex0 - d3 * sin(phi)
        gy0 = ey0 + d3 * cos(phi)
        dr.polygon([(x0, y0), (fx0, fy0), (cx0, cy0),
                    (gx0, gy0)], fill=fill)

    if arrow in ('last', 'both'):
        cx0 = x1 - d1 * cos(phi)
        cy0 = y1 - d1 * sin(phi)
        ex0 = x1 - el * cos(phi)
        ey0 = y1 - el * sin(phi)
        fx0 = ex0 + d3 * sin(phi)
        fy0 = ey0 - d3 * cos(phi)
        gx0 = ex0 - d3 * sin(phi)
        gy0 = ey0 + d3 * cos(phi)
        dr.polygon([(x1, y1), (fx0, fy0), (cx0, cy0),
                    (gx0, gy0)], fill=fill)

if __name__ == '__main__':
    w, h = 640, 480
    im = Image.new('RGB', (w,h), '#FFFFDD')
    dr = ImageDraw.Draw(im)

    ptA = (110,110)
    ptB = (430,430)
    dimension(dr, ptA, ptB, arrow='both', arrowhead=(8, 10, 3))
    ptA = (400,50)
    ptB = (50,400)
    dimension(dr, ptA, ptB, arrow='both', arrowhead=(8, 10, 3))

    im.show()
    #im.save('../figures/test_dimension.png')
