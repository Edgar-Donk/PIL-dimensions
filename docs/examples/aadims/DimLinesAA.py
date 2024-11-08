import sys
sys.path.append('../dims')

from PIL import ImageDraw, ImageFont
from math import sin, cos, radians, sqrt, atan2, pi, degrees, tan

from collections import defaultdict
from DimLinesPIL import angled_text, int_up, polar2cart, cart2polar, DashedLine

# Use this to make arrowhead on the end of lines
# tuple (d1, d2, d3) specifies shape, default (8, 10, 3)
# d1 specifies length along the line
# d2 is the long side
# d3 is the vertical height

# make linear dimension with option for arrows both ends or one end only
# arrow='first', arrow='last', arrow='both'

# dimension_aa normal dimensioning, used as base for other dimensions
# dim_arc dimension over an angle

# to_matrix, changes list to 2D list
# above_below, cross product to determine on which side a point liesrelative to line
# centroid, finds centroid from list 2D points
# flood, fills a space with a colour
# findSect, finds sector (Octant) and quadrant
# plot_sector_points, 8-way plot with sector switch
# DashedLineAA, 1 pixel wide dashed line
# WideLineAA, normal thick aa line
# LineAA, 1 pixel wide normal aa line
# PartLineAA, 1 pixel wide aa line which can switch off aa on one or other side
# polyAA, draws aa polygon
# PartCircleAA, aa circle with start and finish

# dimension_aa, basic aa line with arrows either end
# dims_aa, dimension vertical and horizontal tailed lines with extension lines
# inner_dim_aa, inner vertical and horizontal dimensions
# thickness_dim_aa, thickness dimension
# make_arc_aa, driving routine for arcs
# arc_dim_aa, angle dimension
# leader_aa, leader to object
# slant_dim_aa, slanting dimension with 45° tails
# level_dim_aa, leader to triangle on tank level




def to_matrix(l,n):
    # convert list to multidimensional list
    return [l[i:i+n] for i in range(0, len(l), n)]

def above_below(ptA,ptB,ptC):
    x1, y1 = ptA
    x2, y2 = ptB
    xA, yA = ptC
    # line [(x1,y1),(x2,y2)],point (xA,xB) is point one side or other
    v1 = (x2-x1, y2-y1)   # Vector 1
    v2 = (x2-xA, y2-yA)   # Vector 1
    xp = v1[0]*v2[1] - v1[1]*v2[0]  # Cross product

    return xp

def centroid(points):
    # assume that points is a 2D list of points polygon, point counted twice
    points = points + [points[0],]
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    centre = int_up(sum(x) / len(points)), int_up(sum(y) / len(points))
    return centre

def flood(im, dr, at, fill, back):
    x, y = at
    if im.getpixel(at) == back:
        dr.point((x,y), fill)

        flood(im, dr, (x+1,y), fill, back)
        flood(im, dr, (x,y+1), fill, back)
        flood(im, dr, (x-1,y), fill, back)
        flood(im, dr, (x,y-1), fill, back)

def findSect(centre, outer):
    xm, ym = centre
    x, y = outer
    dx = x - xm
    dy = y - ym
    gradient = abs(dy/dx) if dx != 0 else 5000
    # check which quadrant(s) left and right lines are in
    # 1st quadrant
    if (x > xm and y >= ym):
        quad = 1
        sect = 2 if gradient > 1 else 1
    # 2nd quadrant
    if (x <= xm and y > ym):
        quad = 2
        sect = 3 if gradient > 1 else 4
    # 3rd quadrant
    if (x < xm and y <= ym):
        quad = 3
        sect = 6 if gradient > 1 else 5
    # 4th quadrant
    if (x >= xm and y < ym):
        quad = 4
        sect = 7 if gradient > 1 else 8

    return sect, quad

def plot_sector_points(dr, xm, ym, x, y, sects, fill, all8=1):
    # plots all 8 sectors or only 4 sectors in the while loop
    if sects[0] < 0:
        ltemp = list(sects)
        ltemp[0] = -ltemp[0]
        sects = tuple(ltemp)
    if all8 == 1:
        if sects[0] == 1 or sects[1] == 1:
            dr.point((xm-x, ym+y), fill)               # I Octant
        elif sects[0] == 3 or sects[1] == 3:
            dr.point((xm-y, ym-x), fill)               # III. Octant
        elif sects[0] == 5 or sects[1] == 5:
            dr.point((xm+x, ym-y), fill)               # V  Octant
        elif sects[0] == 7 or sects[1] == 7:
            dr.point((xm+y, ym+x), fill)                #   VII. Octant

    if sects[0] == 4 or sects[1] == 4:
        dr.point((xm+x, ym+y), fill)               #  IV . Octant  +x +y
    elif sects[0] == 2 or sects[1] == 2:
        dr.point((xm+y, ym-x), fill)               # II Octant
    elif sects[0] == 8 or sects[1] == 8:
        dr.point((xm-x, ym-y), fill)               #  VIII. Octant  -x +y
    elif sects[0] == 6 or sects[1] == 6:
        dr.point((xm-y, ym+x), fill)               # VI Octant

def DashedLineAA(drawl, ptA, ptB, dash=(5,5), fill=(0,0,0), back=(255,255,221),
                    adjust=False):
    # check dash input
    if len(dash)%2 != 0 and len(dash) !=1:
        raise Exception('The dash tuple: {} should be one or an equal number '\
                    'of entries'.format(dash))
    dash = dash + dash if len(dash) == 1 else dash

    x0, y0 = ptA
    x1, y1 = ptB
    dx = (x1 - x0)
    dy = (y1 - y0)

    if adjust is True:
        slope = atan2(dy, dx)
        slope = slope if slope >= 0 else (2*pi + slope)

    dx = abs(dx)
    dy = abs(dy)

    pattern = []
    # use extend rather than append
    while len(dash) > 0:
        dash0, *dash = dash
        if adjust is True:
            dash0 = abs(int_up(dash0*cos(slope) if dx >= dy else dash0*sin(slope)))
        pattern.extend([1] * dash0) # dashes
        dash0, *dash = dash
        if adjust is True:
            dash0 = abs(int_up(dash0*cos(slope) if dx >= dy else dash0*sin(slope)))
        pattern.extend([0] * dash0) # spaces

    if not pattern:
        pattern.append(1)
    len_pattern = len(pattern)
    count = 0

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy
    ed = dx + dy
    ed = 1 if ed == 0 else sqrt(dx*dx+dy*dy) # max(dx, dy)

    dr = dx + 1 if dx > dy else dy + 1

    def contrast(comp, size,j):
        return 255 if comp == 255 else int((255-comp) * j / size) + comp

    diffs = defaultdict(list)
    diffs = defaultdict(lambda:back, diffs)
    for i in range(int(ed)+1):
        if fill == (0,0,0):
            diffs[i] = tuple(int(255*i/ed) for j in range(3))
        else:
            diffs[i] = tuple(contrast(fill[j],ed,i) for j in range(3))

    for _ in range (dr):
        if pattern[count] == 1:
            drawl.point([x0, y0], fill=diffs[abs(err-dx+dy)])
        e2 = err<<1
        x2 = x0

        if e2 >= -dx:           # y-step
            if e2+dy < ed and pattern[count] == 1:
                drawl.point([x0,y0+sy], fill=diffs[abs(e2+dy)])
            err -= dy
            x0 += sx

        if e2 <= dy:      # x-step
            if dx-e2 < ed and pattern[count] == 1:
                drawl.point([x2+sx,y0], fill=diffs[abs(dx-e2)])
            err += dx
            y0 += sy
        count = count + 1 if count < len_pattern -1 else 0

def WideLineAA(draw, ptA, ptB, fill=(0,0,0), width=1, back=(255,255,221)):

    x0, y0 = ptA
    x1, y1 = ptB
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    ed = dx + dy
    ed = 1 if ed == 0 else sqrt(dx*dx+dy*dy)
    dr = dx + 1 if dx > dy else dy + 1          # better plotting when steep

    def contrast(comp, size,j):
        return 255 if comp == 255 else int((255-comp) * j / size) + comp

    diffs = defaultdict(list)
    diffs = defaultdict(lambda:back, diffs)
    for i in range(int(ed)+1):
        if fill == (0,0,0):
            diffs[i] = tuple(int(255*i/ed) for j in range(3))
        else:
            diffs[i] = tuple(contrast(fill[j],ed,i) for j in range(3))

    for _ in range (dr):
        out = 0 if dy==0 else max(0,int(abs(err-dx+dy)-(width-1)/2))
        draw.point([x0, y0], fill=diffs[out])
        e2 = err
        x2 = x0
        if e2 << 1 >= -dx:
            e2 += dy
            y2 = y0
            while e2 < ed*width and (y1 != y2 or dx > dy):# and x < dr-1:
                #hue = 0 if dx==0 else max(0, int(255*(abs(e2)/ed-(width-1)/2)))
                out = 0 if dy==0 else max(0, int((abs(e2)-dy*(width-1)/2)))
                y2 += sy
                draw.point([x0, y2], fill=diffs[out])
                e2 += dx
            e2 = err
            err -= dy
            x0 += sx
        if e2 << 1 <= dy:
            e2 = dx - e2 # e2 -= dx #
            while e2 < ed*width and (x1 != x2 or dx < dy):# and x < dr-1:
                #hue = 0 if dx == 0 else max(0, int(255*(abs(e2)/ed-(width-1)/2)))
                out = 0 if dx == 0 else max(0, int(abs(e2)-dx*(width-1)/2))
                x2 += sx
                draw.point([x2 , y0], fill=diffs[out])
                e2 += dy
            err += dx
            y0 += sy

def LineAA(draw, ptA, ptB, fill=(0,0,0), back=(255,255,255)):
    # draw a dark anti-aliased line on light background
    x0, y0 = ptA
    x1, y1 = ptB
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy   # error value e_xy

    ed = dx + dy
    ed = 1 if ed == 0 else sqrt(dx*dx+dy*dy)
    dr = dx + 1 if dx > dy else dy + 1 # better plotting when steep

    def contrast(comp, size,j):
        return 255 if comp == 255 else int((255-comp) * j / size) + comp

    diffs = defaultdict(list)
    diffs = defaultdict(lambda:back, diffs)
    for i in range(int(ed)+1):
        if fill == (0,0,0):
            diffs[i] = tuple(int(255*i/ed) for j in range(3))
        else:
            diffs[i] = tuple(contrast(fill[j],ed,i) for j in range(3))

    for x in range (dr):                 # pixel loop
        draw.point([x0, y0], fill=diffs[abs(err-dx+dy)])
        e2 = err
        x2 = x0
        if e2<<1 >= -dx:                # y-step
            if e2+dy < ed and x < dr - 1:
                draw.point([x0,y0+sy], fill=diffs[abs(e2+dy)])
            err -= dy
            x0 += sx
        if e2<<1 <= dy and x < dr - 1:   # x-step
            if dx-e2 < ed:
                draw.point([x2+sx,y0], diffs[abs(dx-e2)])
            err += dx
            y0 += sy

def PartLineAA(draw, ptA, ptB, fill=(0,0,0), back=(255,255,221), cross=0):
    # draw a dark anti-aliased line on light background, cross disables
    # antialiasing on one side
    x0, y0 = ptA
    x1, y1 = ptB

    sects = findSect(ptA,ptB)

    dx = dx0 = abs(x1 - x0)
    dy = dy0 = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    if dx0 > dy0:       # gentle incline
        dy = -dy
        dr = dx0 + 1
    else:               # steep slope
        dx = -dx
        dr = dy0 + 1
        dx, dy = dy, dx
    err = dx + dy
    ed = 1 if err == 0 else sqrt(dx*dx+dy*dy)

    def contrast(comp, size,j):
        return 255 if comp == 255 else int((255-comp) * j / size) + comp

    diffs = defaultdict(list)
    diffs = defaultdict(lambda:back, diffs)
    for i in range(int(ed)+1):
        if fill == (0,0,0):
            diffs[i] = tuple(int(255*i/ed) for k in range(3))
        else:
            diffs[i] = tuple(contrast(fill[k],ed,i) for k in range(3))

    for _ in range (dr):

        ez = err-dx-dy
        out = abs(ez)
        draw.point([x0, y0], fill=diffs[out])
        if abs(ez+dx) < ed-1:
            #if (cross > 0 and slope > 0) or (cross < 0 and slope < 0) or cross == 0:
            out = abs(ez+dx)
            if dx0 > dy0:
                if cross < 0 and sects[0] in (4,8):
                    draw.point([x0,y0+sy], fill=diffs[out]) # fill=diffs[out]
            else:
                if cross < 0 and sects[0] in (2,6):
                    draw.point([x0+sx,y0], fill=diffs[out])

        if abs(ez-dx) < ed-1:
            #if (cross < 0 and slope > 0) or (cross > 0 and slope < 0) or cross == 0:
            out = abs(ez-dx)
            if dx0 > dy0:
                if cross < 0 and sects[0] in (1,5):
                    draw.point([x0,y0-sy], fill=diffs[out])
            else:
                if cross < 0 and  sects[0] in (3,7):
                    draw.point([x0-sx,y0], fill=diffs[out])

        e2 = err<<1
        if e2 >= dy:
            err += dy
            if dx0 > dy0:
                x0 += sx
            else:
                y0 += sy
        if e2 <= dx:
            err += dx
            if dx0 > dy0:
                y0 += sy
            else:
                x0 += sx

def polyAA(im, dr, xy, back=(255,255,221), fill=(0,0,0), outline=None):
    # xy list of consecutive points
    try:
        lpts = len(xy[0])
    except:
        lpts = 0

    if lpts ==0:
        xy = to_matrix(xy, 2)
    lxy = len(xy)
    cx, cy = centroid(xy)

    for ix in range(lxy):
        if ix > 0:
            cross = above_below(xy[ix-1],xy[ix],(cx,cy))
            PartLineAA(dr, xy[ix-1], xy[ix], back=back,fill=fill,cross=cross)
    cross = above_below(xy[0],xy[lxy-1],(cx,cy))

    PartLineAA(dr, xy[0], xy[lxy-1], back=back,fill=fill,cross=cross)
    if isinstance(outline,tuple) is False:
        flood(im, dr, (cx, cy), fill, back)


def PartCircleAA(dr, xm, ym, r, start, finish, width, sects, fill=(0,0,0),
                    back=(255,255,221)):
    # xm, ym = centre
    # draw an antialiased circle on light background
    x = -r
    y = 0                                   # IV. Octant from left to bottom left

    err = 2 - 2 * r                         # initial difference

    sslope = abs((ym-start[1])/(xm-start[0]))
    fslope = abs((ym-finish[1])/(xm-finish[0]))
    # check sects
    ssect = 0
    fsect = 0
    plot = 0
    ssect, fsect = sects
    if sects[0] == sects[1]:
        # start, finish in one sector
        plot = 0
    elif (sects[0] == 0 and sects[1] in (1,3,5,7)) or \
            (sects[0] in (2,4,6,8) and sects[1] == 0):
        plot = 1

    if sects[0] < 0:
        plot = 1

    maxdi = [0]
    for n in range(0, width+1):
        maxdi.append(maxdi[n] + 2 * (r-n) -1)
    maxdi.remove(0)
    maxd = maxdi[0]
    # ensure inner aa working with conditions for single aa
    # find maxd of smallest main circle
    maxdsm = 2 * (r-width+1) - 1
    # thick factor used outer main lines
    thfact = (width-1)/2

    def contrast(comp, size,j):
        return 255 if comp == 255 else int((255-comp) * j / size) + comp

    diffs = defaultdict(list)
    diffs = defaultdict(lambda:back, diffs)
    for i in range(maxd):
        if fill == (0,0,0):
            diffs[i] = tuple(int(255*i/maxd) for k in range(3))
        else:
            diffs[i] = tuple(contrast(fill[k],maxd,i) for k in range(3))

    diffsm = defaultdict(list)
    diffsm = defaultdict(lambda:back, diffsm)
    for i in range(maxdsm):
        if fill == (0,0,0):
            diffsm[i] = tuple(int(255*i/maxdsm) for k in range(3))
        else:
            diffsm[i] = tuple(contrast(fill[k],maxdsm,i) for k in range(3))

    while -x > y - 1:
        # actual and inverse slope
        aslope = abs((-y)/(-x))
        cslope = abs(-x/(y+0.2))

        if ssect in (1,5) and plot == 0:
            if aslope >= sslope:
                plot = 1
        elif fsect in (1,5) and plot == 1:
            if aslope >= fslope:
                plot = 0
        elif fsect in (2,6) and plot == 0: # and ssect > 0:
            if cslope <= fslope:
                plot = 1
        elif ssect in (2,6) and plot == 1:
            if cslope <= sslope:
                plot = 0

        elif ssect in (3,7) and plot == 0:
            if cslope <= sslope:
                plot = 1
        elif fsect in (3,7) and plot == 1:
            if cslope <= fslope:
                plot = 0
        elif fsect in (4,8) and plot == 0:
            if aslope >= fslope:
                plot = 1
        elif ssect in (4,8) and plot == 1:
            if aslope >= sslope:
                plot = 0

        err0 = err
        e2 = err-(2*y+1)-(2*x+1) # abs(err+2*(x+y)-2)
        ea = abs(e2)
        out = max(0,int(ea-thfact))
        if plot == 1:
            plot_sector_points(dr, xm, ym, x, y, sects, (diffs[out] if out > 0 else fill),
                    all8 = (1 if (xm+x, ym+y) != (xm-y, ym-x) \
                    or (x==-r and y == 0) else 0))

        # fill out diagonals
        x0 = -x
        eout = abs(e2 + 2*x0 + 2*y + 2)
        if eout < maxd: # and (width-1)//2 == 0
            if plot == 1:
                plot_sector_points(dr, xm, ym, x-1, y+1, sects, (diffs[eout] if eout > 0 else fill),
                    all8 = (1 if (xm+x, ym+y) != (xm-y, ym-x) else 0))

        ein = e2
        x0 = -x
        for n in range(0, width):
            ein = ein-(2*(x0-n)-1)
            e0 = -ein

            if n < width-2:
                fact = fill
            elif n == width-1:
                fact = diffs[abs(int(e0-maxd*thfact/10))] if n==0 else \
                        diffsm[e0-maxdi[n-1]]
            else:
                fact = diffsm[max(0,int(abs(e0-maxdi[n])-maxdsm*thfact/10))] # e2-maxdsm
            if plot == 1:
                plot_sector_points(dr, xm, ym, x+n+1, y, sects, fact,
                    all8 = (1 if (xm+x, ym+y) != (xm-y, ym-x) else 0))

        if (err0 <= y):
            y += 1
            err += y * 2 + 1            # e_xy+e_y < 0

        if (err0 > x or err > y):          # e_xy+e_x > 0 or no 2nd y-step
            x += 1
            # aa missed by diagonals
            eout = abs(e2 + 2*y - 1)
            if eout < maxd:
                if plot == 1:
                    plot_sector_points(dr, xm, ym, x-1, y, sects, (diffs[eout] if eout > 0 else fill),
                        all8 = (1 if (xm+x, ym+y) != (xm-y, ym-x) else 0))
            err += x * 2 + 1            # -> x-step now


def dimension_aa(im, dr, ptA, ptB=None, angle=None, back=(255,255,255), fill=(0,0,0),
                arrowhead=(8, 10, 3), arrow='last'):
    if isinstance(arrowhead, tuple) and len(arrowhead) == 3:
        d1, d2, d3 = arrowhead
    else:
        raise Exception('dimension_aa: arrowhead {} needs a 3 entry'  \
                'tuple'.format(arrowhead))

    if arrow not in ('first', 'last', 'both'):
        raise Exception('dimension_aa: arrow {} can only be the strings "first",' \
            '"last", "both"'.format(arrow))

    # extract dims from tuples
    x0, y0 = ptA
    if angle is None and ptB:
        x1, y1 = ptB
        phi = atan2(y1-y0, x1-x0)

    elif ptB is None and isinstance(angle, int):
        x1,y1 = ptA
        phi = radians(angle)
    else:
        raise Exception('dimension_aa: Either supply ptB {} or angle {} not both' \
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
        polyAA(im,dr,[(x0, y0), (fx0, fy0), (cx0, cy0),
                    (gx0, gy0)], fill=fill)
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
        polyAA(im,dr,[(x1, y1), (fx0, fy0), (cx1, cy1),
                    (gx0, gy0)], fill=fill)
        cx3 = cx1
        cy3 = cy1

        if ptB:
            LineAA(dr, (cx2, cy2), (cx3, cy3), back=back, fill=fill)

def dims_aa(im, dr, ptA, ptB, extA, extB=None, text=None, font=None,
        textorient=None, fill=(0,0,0), back=(255,255,221),tail=True,
        arrowhead=(8, 10, 3), arrow='both'):
    # dimension vertical and horizontal tailed lines with extension lines.
    # ptA, ptB line coords, extA, extB extension lines to measured item, positive
    # to right when vertical or above it when horizontal

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

def inner_dim_aa(im, ldraw, ptA, ptB, text=None, font=None, fill=(0,0,0),
              arrowhead=(8, 10, 3), arrow='both', back=(225,225,221)):
    # used on horizontal or vertical inner dimensions

    dimension_aa(im, ldraw, ptA, ptB, fill=fill, arrowhead=arrowhead,
              arrow=arrow, back=back)
    # vertical
    if ptA[0] == ptB[0]:
        at = ptA[0] - 10, (ptA[1] + ptB[1]) //2
        angle = 90

    # horizontal
    elif ptA[1] == ptB[1]:
        at = (ptA[0] + ptB[0]) // 2, ptA[1] - 10
        angle = 0
    else:
        raise Exception('The inner dimension: should be vertical or horizontal '\
                        '{} {} coordinates'.format(ptA, ptB))

    angled_text(im, at, text, angle, font=font, fill=fill)

def thickness_dim_aa(im, dr, ptA, thick, angle=0, text=None, font=None, fill=(0,0,0),
              arrowhead=(8, 10, 3), back=(255,255,221)):
    phir = radians(angle)
    ptB = int(ptA[0] + thick * cos(phir) + 0.5), \
          int(ptA[1] + thick * sin(phir) + 0.5)

    # Get drawing context
    tdraw = ImageDraw.Draw(im)

    tdraw.line([ptA, ptB], width=1, fill=fill)

    dimension_aa(im,dr, ptA, angle=angle, arrow='last',fill=fill,back=back)
    dimension_aa(im,dr, ptB, angle=angle, arrow='first',fill=fill,back=back)

    # thickness of item
    phir = radians(angle)
    # ft = font.getsize(text)
    # unused1, unused2, wide, height
    ft = font.getbbox(text)
    h = ft[3] // 2
    dx = - (h + arrowhead[1] + 5) * cos(phir)
    dy = - (h + arrowhead[1] + 5) * sin(phir)

    # stop upside down text
    if 0 <= angle <= 180:
        angle = 90-angle
    elif 180 < angle < 360:
        angle = 270-angle

    at = (ptA[0] + int(dx), ptA[1] + int(dy))
    angled_text(im, at, text=text, angle=angle, font=font)

def make_arc_aa(dr, centre, radius, start, finish, width=1, fill=(0,0,0), back = (255,255,221)):
    xm,ym = centre
    sq = findSect((xm, ym), (start[0], start[1]))
    fq = findSect((xm, ym), (finish[0], finish[1]))
    sects = ()

    diff_sect = fq[0] - sq[0]

    if diff_sect == 0:
        sects = sq[0],fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

    elif (diff_sect == 1) or (sq[0] == 8 and fq[0] == 1):
        sects = sq[0],0
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)
        sects = 0,fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

    elif (diff_sect == 2) or (sq[0] == 8 and fq[0] == 2) or (sq[0] == 7 and fq[0] == 1):
        sects = sq[0],0
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)
        if sq[0] < 8:
            sects = -sq[0]-1,-sq[0]-1
        else:
            sects = -1,-1
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)
        sects = 0,fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

    elif (diff_sect == 3) or (sq[0] == 8 and fq[0] == 3) or (sq[0] == 7 and fq[0] == 2):
        sects = sq[0],0
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

        if sq[0] < 7:
            sects = -sq[0]-2,-sq[0]-2
        else:
            sects = -1,-1
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

        if sq[0] < 8:
            sects = -sq[0]-1,-sq[0]-1
        else:
            sects = -2,-2
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

        sects = 0,fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

def arc_dim_aa(im,dr,centre,radius,begin,end,fill=(0,0,0),text=None,font=None,
                arrowhead=(8,10,3),back=(225,225,221),aall=0):
    # x,y,radius all relate to centre coords and radius, give 2 angles
    rtimes2 = max(60, radius*2)
    if isinstance(begin, int):
        beginp = polar2cart(centre, begin, rtimes2)
    if isinstance(end, int):
        endp = polar2cart(centre, end, rtimes2)
    if isinstance(begin, tuple):
        beginp = begin
        begin, rayb = cart2polar(centre, begin)
    if isinstance(end, tuple):
        endp = end
        end, raye = cart2polar(centre, end)

    beginr = radians(begin)
    endr = radians(end)

    bq = findSect(centre, beginp)
    eq = findSect(centre, endp)

    if bq[1] in (3,4) and eq[1] in (1,2):
        alpha = (360 - begin + end)/2
        diff = 360 - begin + end
    else:
        alpha = (begin + end)/2
        diff = end - begin

    if diff == 180:
        raise Exception('arc_dim_aa: angle is 180°, begin {} end {}' \
            ' difference {} cannot draw dimension'.format(begin, end, diff))

    if diff == 90:
        ax, ay = polar2cart(centre, begin, radius)
        bx, by = polar2cart(centre, end, radius)
        dx, dy = polar2cart(centre, alpha, radius*sqrt(2))

        LineAA(dr, (ax,ay), (dx,dy), fill=fill, back=back)
        LineAA(dr, (bx,by), (dx,dy), fill=fill, back=back)

    else:
        x, y = centre
        d1, d2, d3 = arrowhead

        # placement of arrows, 'first' point outwards
        order = 'last' if radians(diff) * radius > 4 * arrowhead[1] else 'first'

        # find begin and end arc
        start = int_up(x + radius * cos(beginr)), int_up(y + radius * sin(beginr))
        finish = int_up(x + radius * cos(endr)), int_up(y + radius * sin(endr))

        dimension_aa(im,dr, start, angle=(begin - 90), arrow=order,fill=fill,back=back)
        dimension_aa(im,dr, finish, angle=(end + 90), arrow=order,fill=fill,back=back)

        start_arc = polar2cart(start, (begin + 90), d1)
        finish_arc = polar2cart(finish, end - 90, d1)

        if order == 'first':
            make_arc_aa(dr, centre, radius, beginp, endp, fill=fill, back = back)
        else:
            make_arc_aa(dr, centre, radius, start_arc, finish_arc, fill=fill, back = back)

    # placement of text
    if text is None:
        text = str(diff) + '°'
    if font is None:
        font_size=15
        font = ImageFont.truetype('consola.ttf', font_size)
    # (wide, ht) = font.getsize(text)
    unused1, unused2, wide, ht = font.getbbox(text)

    # stop upside down text
    if bq[1] in (3,4) and eq[1] in (1,2):
        alpha = begin + alpha -360

    angle = alpha - 90
    da = 7

    if diff == 90:
        X, Y = polar2cart(centre, alpha, radius * sqrt(2) + da)
    else:
        t = tan(radians(diff/2))
        a = wide/ 2 / t
        size = max(radius, a)
        X, Y = polar2cart(centre, alpha, size + ht/2+da)

    angled_text(im, (X, Y), text, angle, font, aall=aall)

def leader_aa(im, dr, at, angle=315, extA=20, extB=20, arrowhead=(3,5,1),
            arrow='first', fill=(0,0,0), text=None, font=None, back=(255,255,221)):
    # leader to object, angle and length (extA) first part, then goes horizontal
    # for second part (extB). Only one arrow where leader points.
    # start at,

    font = font if font else ImageFont.load_default()
    # (wide, height) = font.getsize(text)
    unused1, unused2, wide, height = font.getbbox(text)

    h = height // 2

    if wide > extB:
        print('extB was increased from:',extB,'to accommodate the text',wide+10)
        extB = wide+10

    # dimension line
    phi = 180 if 90 < angle < 270 else 0
    ptB = polar2cart(at, angle, extA)
    ptC = polar2cart(ptB, phi, extB)
    ptD = polar2cart(at, angle, arrowhead[0])
    dimension_aa(im, dr, at, ptB, arrowhead=arrowhead,
              arrow=arrow, fill=fill, back=back)
    LineAA(dr, ptB, ptC, fill=fill, back=back)
    LineAA(dr, ptB, ptD, fill=fill, back=back)

    # text position
    tp = ((ptB[0] + ptC[0])//2, ptB[1] - h - 5)

    angled_text(im, tp, text, 0, font)

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
        raise Exception('slant_dim: The leader tuple extA {} should be one or ' \
                'two entries'.format(extA))

    if ptB is None and length and 0 <= angle <360:
        phir = radians(angle)
        ptC = polar2cart(ptA, angle-90, extO)
        ptD = polar2cart(ptC, angle, length)
    elif length is None and ptB:
        phir = atan2(ptB[1]-ptA[1], ptB[0]-ptA[0])
        angle = int(degrees(phir) + 0.5)
        ptC = polar2cart(ptA, angle-90, extO)
        ptD = ptC[0] + (ptB[0] - ptA[0]), ptC[1] + (ptB[1] - ptA[1])
    else:
        raise Exception('slant_dim: Either supply ptB {}, or length {} and ' \
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

    print(font , 'font')
    font = ImageFont.load_default() if font is None else font
    #ft = font.getsize(text)
    #unused1, unused2, wide, height
    ft = font.getbbox(text)

    h = ft[3] // 2

    angle = 360 + angle if angle < 0 else angle
    angle = angle - 360 if angle >= 360 else angle

    mid = (ptC[0] + ptD[0])/2, (ptC[1] + ptD[1])/2
    at =  mid[0] + (h + 7) * sin(phir), mid[1] - (h + 7) * cos(phir)
    at = int_up(at[0]), int_up(at[1])

    angled_text(im, at, text, angle, font, aall=0)

def level_dim_aa(im, dr, at, diam, ext=0, ldrA=20, ldrB=20, dash=(10,4), text=None,
                fill=(0,0,0), back=(255,255,221), tri=8, font=None):
    # at on left tank wall, diam internal tank diameter,
    # triangle at level (8,8,8) p0 tip triangle, p1, p2 angles, p2 continues to p4
    # p3 opposite side to at, both drawn to inside tank wall
    # leader (ldr) at 60° up to p4 then horizontal to p5
    # if ext != 0, p7 position of end of extender before touching tank wall

    # check dash input
    if len(dash)%2 != 0 and len(dash) !=1:
        raise Exception('level_dim_aa: the dash tuple {} should be one or an' \
                        ' equal number of entries'.format(dash))

    if isinstance(ext, int) or len(ext) == 1:
        exto = ext if isinstance(ext, int) else ext[0]
    elif len(ext) == 2:
        exto = sum(ext)
    else:
        raise Exception('level_dim_aa: The extension tuple ext {} should be one' \
                        ' or two entries'.format(ext))

    font = ImageFont.load_default() if font is None else font

    # wide, ht = font.getsize(text) if text is not None else (0,0)
    unused1, unused2, wide, ht = font.getbbox(text) if text is not None else (0,0)

    angle = 0

    p3 = (at[0] + diam, at[1]) # outer wall
    # check whether left or right position
    if ldrA > 0:
        if ext == 0:
            p0 = (at[0] + int_up(diam * 0.4), at[1])
            p4 = (p0[0] + int_up(ldrA * 0.5), p0[1] - int_up(ldrA * sin(pi/3)))
            p5 = (at[0] + diam, p4[1]) if ldrB < diam else (at[0] + diam + ldrB, p4[1])
        else:
            p0 = (at[0] + int_up(diam + 0.6 * exto), at[1]) # tip triangle
            p4 = (p0[0] + int_up(ldrA * 0.5), p0[1] - int_up(ldrA * sin(pi/3))) # top ldr
            p5 = (p4[0] + ldrB, p4[1]) # end ldr
            p7 = (p3[0] + est, at[1])
    else:
        if ext == 0:
            p0 = (at[0] + int_up(diam * 0.6), at[1])
            p4 = (p0[0] + int_up(ldrA * 0.5), p0[1] + int_up(ldrA * sin(pi/3)))
            p5 = (at[0], p4[1])
        else:
            p0 = (at[0] - int_up(0.6 * exto), at[1])
            p4 = (p0[0] + int_up(ldrA * 0.5), p0[1] + int_up(ldrA * sin(pi/3)))
            p5 = (p4[0] - ldrB, p4[1])
            p7 = (at[0] - est, at[1])

    ldr_s = abs(p5[0] - p4[0])

    if ldr_s < wide:
        raise Exception('The leader size is too small: {} should be larger '\
                        'than the text width {}'.format(ldr_s, wide))

    p2 = (p0[0] + int_up(tri * 0.5), p0[1] - int_up(tri * sin(pi/3)))
    p1 = (p2[0] - tri, p2[1])


    DashedLine(dr, at, end_pos=p3, dash=dash, width = 1, fill=fill)
    polyAA(im, dr, [p0, p1, p2], outline=fill)

    if ldrA > 0:
        if ext == 0:
            DashedLineAA(dr, p2, p4, dash=dash, fill=fill, back=back)
        else:
            LineAA(dr, p2, p4, fill=fill, back=back)
            dr.line([p7, (p7[0] + exto, p7[1])], width = 1, fill=fill)
    else:
        if ext ==0:
            DashedLineAA(dr, p1, p4, dash=dash, fill=fill)
        else:
            LineAA(dr, p1, p4, fill=fill, back=back)
            dr.line([p7, (p7[0] - exto, p7[1])], width = 1, fill=fill)

    if ext == 0:
        DashedLineAA(dr, p4, p5, dash=dash, fill=fill)
    else:
        dr.line([p4, p5], width = 1, fill=fill)

    p6 = (int((p4[0] + p5[0])//2), p4[1] - ht - 5)

    angled_text(im, p6, text, angle, font, fill=fill)
