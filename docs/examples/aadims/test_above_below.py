from PIL import Image, ImageDraw, ImageFont
from math import sqrt
from collections import defaultdict

def findSect(centre, outer):
    xm, ym = centre
    x, y = outer
    dx = x - xm
    dy = y - ym
    gradient = abs(dy/dx) if dx != 0 else 1000
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

def above_below(pta,ptb,ptc):
    x1, y1 = pta
    x2, y2 = ptb
    xC, yC = ptc
    # line [(x1,y1),(x2,y2)],point (xA,xB) is point one side or other
    v1 = (x2-x1, y2-y1)   # Vector 1
    v2 = (x2-xC, y2-yC)   # Vector 1
    xp = v1[0]*v2[1] - v1[1]*v2[0]  # Cross product

    return xp



# originally only part range of sector, this part plot was accurate
# see bres_line_zigl
# when working with steep slopes it works if the plottin constraints are flipped

def PartLineAA(draw, pta, ptb, fill=(0,0,0), back=(255,255,221), cross=0):
    x0, y0 = pta
    x1, y1 = ptb
    sects = findSect(pta, ptb)
    #print(sects,'sects')

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
    for l in range(int(ed)+1):
        if fill == (0,0,0):
            diffs[l] = tuple(int(255*i/ed) for k in range(3))
        else:
            diffs[l] = tuple(errs(fill[k],ed,l) for k in range(3))

    for j in range (dr):
        ez = err-dx-dy
        out = abs(ez)
        draw.point([x0, y0], fill=diffs[out])
        if abs(ez+dx) < ed-1:
            out = abs(ez+dx)
            if dx0 > dy0:
                #print(sects[0],pta, ptb, cross,'first')
                if cross < 0 and sects[0] in (4,8) or \
                    cross > 0 and sects[0] in (5,1): #
                    draw.point([x0,y0+sy], fill=diffs[out]) #
            else:
                #print(sects[0],pta, ptb, cross,'second')
                if cross < 0 and sects[0] in (2,6) or \
                    cross > 0 and sects[0] in (3,7): #
                    draw.point([x0+sx,y0], fill=diffs[out])

        if abs(ez-dx) < ed-1:
            out = abs(ez-dx)
            if dx0 > dy0:
                #print(sects[0],pta, ptb,cross,'first')
                if cross < 0 and sects[0] in (1,5) or \
                    cross > 0 and sects[0] in (8,4):
                    draw.point([x0,y0-sy], fill=diffs[out])
                    #print('here')
            else:
                #print(sects[0],pta, ptb, cross, 'second')
                if cross < 0 and sects[0] in (3,7) or \
                    cross > 0 and sects[0] in (6,2):
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

if __name__ == "__main__":

    font = ImageFont.truetype('consola.ttf', 10)
    w,h = 51,51

    Back = (255,255,221)
    image = Image.new('RGB', (w,h), Back)
    drawl = ImageDraw.Draw(image)

    #a = (26,23),(23,26),(17,26),(14,23),(14,17),(17,14),(23,14),(26,17),(26,23)
    #b = (36,26),(26,36),(14,36),(4,26) ,(4,14), (14,4), (26,4) ,(36,14)

    a = (25,25),(35,20),(25,15),(20,5),(15,15),(5,20),(15,25),(20,35),(25,25)
    #a = [(32, 11), (24, 17), (28, 18), (30, 21), (32, 11)]
    #a = [(32, 11), (1, 36), (14, 38), (21, 50), (32, 11)]
    #a = [(11, 43), (22, 4), (29, 16), (42, 18), (11, 43)]
    #a = [(14, 15), (49, 32), (37, 37), (33, 50), (14, 15)]
    #a = [(39, 39), (20, 4), (16, 17), (4, 22), (39, 39)]
    #a = [(34, 6), (46, 44), (34, 38), (22, 44), (34, 6)]
    #a = [(34, 40), (46, 2), (34, 8), (22, 2), (34, 40)]
    #a = [(13, 23), (51, 11), (45, 23), (51, 35), (13, 23)]
    #a = [(51, 23), (13, 11), (19, 23), (13, 35), (51, 23)]
    c = (20,20)
    #print ('centre', c)
    for i in range(1,len(a)):
        prod = above_below((a[i][0], a[i][1]), (a[i-1][0], a[i-1][1]), c)
        PartLineAA(drawl, (a[i][0], a[i][1]), (a[i-1][0], a[i-1][1]),
                fill=(0,0,0), back=Back, cross=prod)

    #LineAA(drawl, (26,23), (36,26), fill=(0,0,0), back=back)
    # (26,23),(29,33)
    #print(prod)
    image.show()
