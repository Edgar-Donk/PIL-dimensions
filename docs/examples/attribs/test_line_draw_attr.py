import sys
sys.path.append('../dims')

#from PIL import Image, ImageDraw
from DimLinesattr import aq, LineATTR

#dc.arrowhead = (2,3,4,5)
#print(dc.arrowhead)
'''
def LineATTR(pta, ptb, cross=0):
    # draw a dark anti-aliased line on light background, cross disables
    # antialiasing on one side
    x0, y0 = pta
    x1, y1 = ptb
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy   # error value e_xy
    slope = (y1-y0)/(x1-x0) if x1!=x0 else 0

    ed = dx + dy
    ed = 1 if ed == 0 else sqrt(dx*dx+dy*dy)
    dr = dx + 1 if dx > dy else dy + 1 # better plotting when steep

    def errs(comp, size,j):
        return 255 if comp == 255 else int((255-comp) * j / size) + comp

    diffs = defaultdict(list)
    diffs = defaultdict(lambda: dc.back, diffs)
    for i in range(int(ed)+1):
        if dc.fill == (0,0,0):
            diffs[i] = tuple(int(255*i/ed) for j in range(3))
        else:
            diffs[i] = tuple(errs(fill[j],ed,i) for j in range(3))
    #print(diffs)

    for x in range (dr):                 # pixel loop
        dc.draw.point([x0, y0], fill=diffs[abs(err-dx+dy)]
                    if abs(err-dx+dy) < ed//2 else diffs[int_up(ed)])
        #print([x0, y0],diffs[abs(err-dx+dy)] \
                    #if abs(err-dx+dy) < ed//2 else diffs[int_up(ed)])
        e2 = err
        x2 = x0
        if e2<<1 >= -dx:                # y-step
            if e2+dy < ed and x < dr - 1:
                if (cross > 0 and slope > 0) or (cross < 0 and slope < 0) or cross == 0:
                    dc.draw.point([x0,y0+sy], fill=diffs[abs(e2+dy)])
                    #print([x0,y0+sy],diffs[abs(e2+dy)])
            err -= dy
            x0 += sx
        if e2<<1 <= dy and x < dr - 1:  # x-step
            if dx-e2 < ed:
                if (cross < 0 and slope > 0) or (cross > 0 and slope < 0) or cross == 0:
                    dc.draw.point([x2+sx,y0], fill=diffs[abs(dx-e2)])
                    #print([x2+sx,y0],diffs[abs(dx-e2)])
            err += dx
            y0 += sy
'''
#dc.image = Image.new('RGB', (300, 160), '#FFFFDD')
#dc.draw = ImageDraw.Draw(dc.image)

a = (30, 100)
c = (186, 100)
f = (236, 50)

LineATTR(a,f)

aq.image.show()