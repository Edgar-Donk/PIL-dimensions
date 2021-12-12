import sys
sys.path.append('C:\\Users\\mike\\sphinx\\dims_rev\\docs\\examples\\dims')

from PIL import Image, ImageDraw
from DimLinesPIL import int_up, polar2cart
from DimLinesAA import DashedLineAA

'''
def DashedLineAA(drawl, pta, ptb, dash=(5,5), fill=(0,0,0), back=(255,255,221),
                    adjust=False):
    # check dash input
    if len(dash)%2 == 0 or len(dash) ==1:
        pass
    else:
        raise Exception('The dash tuple: {} should be one or an equal number '\
                    'of entries'.format(dash))
    dash = dash + dash if len(dash) == 1 else dash

    x0, y0 = pta
    x1, y1 = ptb
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

    for x in range (dr):
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
'''
if __name__ == "__main__":

    start_pos = (100, 100)
    a = (30,29)
    b=(187,150)

    w, h = 205, 205 # 200, 200
    back = (255,255,221)
    image = Image.new('RGB', (w,h), back)

    draw = ImageDraw.Draw(image)

    dash = (7,1,1,1)

    for i in range(0,360,5):
        end_pos = polar2cart(start_pos, i, 100)
        DashedLineAA(draw, start_pos, end_pos, dash=dash,
                fill=(255-int_up(i*0.7),0,int_up(i*0.7)), adjust=True)

    #DashedLineAA(draw, a, b, dash=dash)
    #bres(draw, a, b, fill='red')

    image.show()
    #image.save('../../temp/DashedLineAA_adj.png')