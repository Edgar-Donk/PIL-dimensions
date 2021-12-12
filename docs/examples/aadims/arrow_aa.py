from PIL import Image, ImageDraw
from DimLinesAA import dimension_aa

'''
def to_matrix(l,n):
    # convert list to multidimensional list
    return [l[i:i+n] for i in range(0, len(l), n)]

def int_up(x):
    return int(x + 0.5) if x >= 0 else int(x - 0.5)

def above_below(pta,ptb,ptc):
    x1, y1 = pta
    x2, y2 = ptb
    xA, yA = ptc
    # line [(x1,y1),(x2,y2)],point (xA,xB) is point one side or other
    v1 = (x2-x1, y2-y1)   # Vector 1
    v2 = (x2-xA, y2-yA)   # Vector 1
    xp = v1[0]*v2[1] - v1[1]*v2[0]  # Cross product

    return xp

def centroid(points):
    # assume that points is a 2D list of points polygon
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    centroid = int_up(sum(x) / len(points)), int_up(sum(y) / len(points))
    return centroid

def flood(im, dr, x, y, fill, back):
    #print(x,y)
    xy = x,y
    if im.getpixel(xy) == back:

    #(r,g,b) = im.getpixel([x,y])
    #if (r,g,b) == (255,255,221):

        dr.point((x,y), fill)

        flood(im, dr, x+1,y, fill, back)
        flood(im, dr, x,y+1, fill, back)
        #flod(im, dr, x+1,y+1, fill, back)
        #flod(im, dr, x-1,y-1, fill, back)
        flood(im, dr, x-1,y, fill, back)
        flood(im, dr, x,y-1, fill, back)
        #flod(im, dr, x-1,y+1, fill, back)
        #flod(im, dr, x+1,y-1, fill, back)

def LineAA(draw, pta, ptb, fill=(0,0,0), back=(255,255,255),cross=0):
    # draw a dark anti-aliased line on light background
    x0, y0 = pta
    x1, y1 = ptb
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy   # error value e_xy
    slope = (y1-y0)/(x1-x0) if x1!=x0 else 0
    #print(pta,ptb,'sx',sx,'sy',sy,'slope',(y1-y0)/(x1-x0) if x1!=x0 else 'inf')

    ed = dx + dy

    ed = 1 if ed == 0 else sqrt(dx*dx+dy*dy) # max(dx, dy) #
    dr = dx + 1 if dx > dy else dy + 1 # better plotting when steep
    #print(dx,dy,dr,'dr')

    def errs(comp, size,j):
        return 255 if comp == 255 else int((255-comp) * j / size) + comp

    diffs = defaultdict(list)
    diffs = defaultdict(lambda:back, diffs)
    for i in range(int(ed)+1):
        if fill == (0,0,0):
            diffs[i] = tuple(int(255*i/ed) for j in range(3))
        else:
            diffs[i] = tuple(errs(fill[j],ed,i) for j in range(3))

    for x in range (dr): # x0, x1+1     # pixel loop
        draw.point([x0, y0], fill=diffs[abs(err-dx+dy)])
        e2 = err
        x2 = x0
        if e2<<1 >= -dx:                # y-step
            if e2+dy < ed and x < dr - 1:
                if (cross > 0 and slope > 0) or (cross < 0 and slope < 0) or cross == 0:
                      draw.point([x0,y0+sy], fill=diffs[abs(e2+dy)])
            err -= dy
            x0 += sx
        if e2<<1 <= dy and x < dr - 1:  # x-step
            if dx-e2 < ed:
                if (cross < 0 and slope > 0) or (cross > 0 and slope < 0) or cross == 0:
                    draw.point([x2+sx,y0], diffs[abs(dx-e2)])
            err += dx
            y0 += sy

def PartLineAA(draw, pta, ptb, fill=(0,0,0), back=(255,255,221), cross=0):
    # draw a dark anti-aliased line on light background, cross disables
    # antialiasing on one side
    x0, y0 = pta
    x1, y1 = ptb

    sects = findSect(pta,ptb)

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

    def errs(comp, size,j):
        return 255 if comp == 255 else int((255-comp) * j / size) + comp

    diffs = defaultdict(list)
    diffs = defaultdict(lambda:back, diffs)
    for i in range(int(ed)+1):
        if fill == (0,0,0):
            diffs[i] = tuple(int(255*i/ed) for k in range(3))
        else:
            diffs[i] = tuple(errs(fill[k],ed,i) for k in range(3))

    for j in range (dr):

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

def polyAA(im, dr,xy,back=(255,255,221),fill=(0,0,0), outline=None):
    # xy list of consecutive points

    try:
        lpts = len(xy[0])
    except:
        lpts = 0

    if lpts ==0:
        xy = to_matrix(xy, 2)
    print(xy)
    lxy = len(xy)
    cx, cy = centroid(xy)

    for ix in range(lxy):
        if ix > 0:
            cross = above_below(xy[ix-1],xy[ix],(cx,cy))
            PartLineAA(dr, xy[ix-1], xy[ix], back=(255,255,221),fill=fill,cross=cross)
    cross = above_below(xy[0],xy[lxy-1],(cx,cy))
    PartLineAA(dr, xy[lxy-1], xy[0], back=(255,255,221),fill=fill,cross=cross)
    if isinstance(outline,tuple) is False:
        flood(im, dr, cx, cy, fill, back)

def dimension(im, dr, ptA, ptB=None, angle=None, back=(255,255,255), fill=(0,0,0),
                arrowhead=(8, 10, 3), arrow='last'):

    if isinstance(arrowhead, tuple) and len(arrowhead) == 3:
        d1, d2, d3 = arrowhead
    else:
        raise Exception('dimension: arrowhead {} needs a 3 entry'  \
                'tuple'.format(arrowhead))

    if arrow not in ('first', 'last', 'both'):
        raise Exception('dimension: arrow {} can only be the strings "first",' \
            '"last", "both"'.format(arrow))

    # extract dims from tuples
    x0, y0 = ptA
    if angle is None and ptB:
        x1, y1 = ptB
        phi = atan2(y1-y0, x1-x0)

        if arrow in ('first', 'both'):
            cx0 = int_up(x0 + d1 * cos(phi))
            cy0 = int_up(y0 + d1 * sin(phi))
        else:
            cx0, cy0 = ptA
        if arrow in ('last', 'both'):
            cx1 = int_up(x1 - d1 * cos(phi))
            cy1 = int_up(y1 - d1 * sin(phi))
        else:
            cx1, cy1 = ptB

        LineAA(dr, (cx0, cy0), (cx1, cy1), back=(255,255,221),fill=fill)

    elif ptB is None and angle:
        x1,y1 = ptA
        phi = radians(angle)
    else:
        raise Exception('dimension: Either supply ptB {} or angle {} not both' \
                .format(ptB, angle))

    # perpendicular distance shaft to arrow tip
    el = int(sqrt(d2 * d2 - d3 * d3) + 0.5)

    if arrow in ('first', 'both'):
        ex0 = int_up(x0 + el * cos(phi))
        ey0 = int_up(y0 + el * sin(phi))
        fx0 = int_up(ex0 + d3 * sin(phi))
        fy0 = int_up(ey0 - d3 * cos(phi))
        gx0 = int_up(ex0 - d3 * sin(phi))
        gy0 = int_up(ey0 + d3 * cos(phi))
        polyAA(im,ldraw,[(x0, y0), (fx0, fy0), (cx0, cy0),
                    (gx0, gy0)], fill=fill)

    if arrow in ('last', 'both'):
        ex0 = int_up(x1 - el * cos(phi))
        ey0 = int_up(y1 - el * sin(phi))
        fx0 = int_up(ex0 + d3 * sin(phi))
        fy0 = int_up(ey0 - d3 * cos(phi))
        gx0 = int_up(ex0 - d3 * sin(phi))
        gy0 = int_up(ey0 + d3 * cos(phi))
        polyAA(im,ldraw,[(x1, y1), (fx0, fy0), (cx1, cy1),
                    (gx0, gy0)], fill=fill)

'''
if __name__ == '__main__':
    w, h = 64, 48
    im = Image.new('RGB', (w,h), '#FFFFDD')
    # Get drawing context
    ldraw = ImageDraw.Draw(im)

    ptA = (13,23)#(34,6) #(14,15) #(11,43)
    ptB = (51,23)#(34,40) #(39,39) #(32,11)
    dimension_aa(im, ldraw, ptA, ptB, arrow='both', arrowhead=(32, 40, 12), # (8, 10, 3)
                fill=(0,0,0), back = (255,255,221))
    #ptA = (400,50)
    #ptB = (50,400)
    #dimension(ldraw, ptA, ptB, arrow='both', arrowhead=(8, 10, 3))

    #im.save('../figures/test_dimension.png')
    im.show()