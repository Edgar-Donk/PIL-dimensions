from PIL import Image, ImageDraw
from DimLinesAA import polyAA

'''
def int_up(x):
    return int(x + 0.5) if x >= 0 else int(x - 0.5)

def flood(im, dr, x, y, fill, back):
    #print(x,y)
    xy = x,y
    if im.getpixel(xy) == back:

    #(r,g,b) = im.getpixel([x,y])
    #if (r,g,b) == (255,255,221):

        dr.point((x,y), fill)

        flood(im, dr, x+1,y, fill, back)
        flood(im, dr, x,y+1, fill, back)
        #flood(im, dr, x+1,y+1, fill, back)
        #flood(im, dr, x-1,y-1, fill, back)
        flood(im, dr, x-1,y, fill, back)
        flood(im, dr, x,y-1, fill, back)
        #flood(im, dr, x-1,y+1, fill, back)
        #flood(im, dr, x+1,y-1, fill, back)

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
    print(pta,ptb,'sx',sx,'sy',sy,'slope',slope)
    ed = dx + dy

    ed = 1 if ed == 0 else sqrt(dx*dx+dy*dy) # max(dx, dy) #
    dr = dx + 1 if dx > dy else dy + 1 # better plotting when steep
    print(round(ed,3), 'ed')
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
        print([x0, y0],'main',abs(err-dx+dy))
        e2 = err
        x2 = x0
        if e2<<1 >= -dx:                # y-step
            if e2+dy < ed and x < dr - 1:
                if (cross > 0 and slope > 0) or (cross < 0 and slope < 0) or cross == 0:
                    draw.point([x0,y0+sy], fill=diffs[abs(e2+dy)])
                    print([x0,y0+sy],'y')
            err -= dy
            x0 += sx
        if e2<<1 <= dy and x < dr - 1:  # x-step
            if dx-e2 < ed:
                if (cross < 0 and slope > 0) or (cross > 0 and slope < 0) or cross == 0:
                    draw.point([x2+sx,y0], diffs[abs(dx-e2)])
                    print([x2+sx,y0],'x')
            err += dx
            y0 += sy

def to_matrix(l,n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def solve(polygon, pt):
    ans = False
    for i in range(len(polygon)):
         x0, y0 = polygon[i]
         x1, y1 = polygon[(i + 1) % len(polygon)]
         if not min(y0, y1) < pt[1] <= max(y0, y1):
            continue
         if pt[0] < min(x0, x1):
            continue
         cur_x = x0 if x0 == x1 else x0 + (pt[1] - y0) * (x1 - x0) / (y1 - y0)
         ans ^= pt[0] > cur_x # ^ xor operator, one and only one is True
    return ans

def above_below(pta,ptb,ptc):
    x1, y1 = pta
    x2, y2 = ptb
    xA, yA = ptc
    # line [(x1,y1),(x2,y2)],point (xA,xB) is point one side or other
    v1 = (x2-x1, y2-y1)   # Vector 1
    v2 = (x2-xA, y2-yA)   # Vector 1
    xp = v1[0]*v2[1] - v1[1]*v2[0]  # Cross product
    if xp > 0:
        print ('on one side', xp)
    elif xp < 0:
        print ('on the other', xp)
    else:
        print ('on the same line!', xp)
    return xp

def centroid(points):
    # assume that points is a 2D list of points polygon
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    centroid = int_up(sum(x) / len(points)), int_up(sum(y) / len(points))
    return centroid

def polyAA(im,dr,xy,back=(255,255,221),fill=(0,0,0)):
    # xy list of consecutive points

    try:
        lpts = len(xy[0])
    except:
        lpts = 0

    #pt = []
    if lpts ==0:
        xy = to_matrix(xy, 2)
    lxy = len(xy)
    cx, cy = centroid(xy)
    print(xy, 'centroid', cx,cy)
    #dr.point([cx,cy], fill='red')
    for ix in range(lxy):
        #xy0, *xy = xy
        #print(xy1)
        #pt.append(xy0)
        #print(pt[ix])
        if ix > 0:
            #print(pt[ix-1], pt[ix], round((pt[ix-1][1] - pt[ix][1])/(pt[ix-1][0] - pt[ix][0]),2))
            cross = above_below(xy[ix-1],xy[ix],(cx,cy))
            LineAA(dr, xy[ix-1], xy[ix], back=(255,255,221),fill=fill,cross=cross)
    #print(pt[0],pt[lxy-1], round((pt[0][1] - pt[lxy-1][1])/(pt[0][0] - pt[lxy-1][0]),2))
    #print(pt[lxy-1],pt[0], round((pt[lxy-1][1] - pt[0][1])/(pt[lxy-1][0] - pt[0][0]),2))
    cross = above_below(xy[0],xy[lxy-1],(cx,cy))
    LineAA(dr, xy[0], xy[lxy-1], back=(255,255,221),fill=fill,cross=cross)

    # perp slope between centroid and tip arrow
    grad = -(xy[0][0] -cx)/(xy[0][1] -cy)
    #if im.getpixel(cx, cy) == back:
    flood(im, dr, cx, cy, fill, back)
'''

if __name__ == "__main__":
    w, h = 21, 21
    start_pos = (w//2, h//2)
    end_pos = 19,18

    image = Image.new('RGB', (w,h), '#FFFFDD') #  #'lightblue'
    drawl = ImageDraw.Draw(image)
    pts = [10,5,13,15,10,13,7,15] # [10,15,13,5,10,7,7,5] #
    #[80,140,110,100,80,120,50,100]
    #[150,290,180,190,150,210,120,190] #[4,4,18,11, 11,20]
    polyAA(image,drawl, pts)
    #print(len(pts),len(pts[0]))
    #LineAA(drawl, start_pos, end_pos, back=(255,255,221),fill=(255,0,0))

    #image.show()