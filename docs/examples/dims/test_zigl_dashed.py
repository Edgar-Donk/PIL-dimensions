from PIL import Image, ImageDraw
from math import atan2, sin, cos, pi
from DimLinesPIL import int_up, polar2cart


def DashedLine(dr, pta, ptb, dash=(5,5), fill='red', adjust=False):
    # check dash input
    if len(dash)%2 != 0 and len(dash) !=1:
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
    #print(pattern)
    count = 0

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    dr = dx + 1 if dx > dy else dy + 1

    for x in range (dr):
        #print(pattern[count],count)
        if pattern[count] == 1:
            draw.point([x0, y0], fill= fill)
            
        e2 = err<<1

        if e2 >= -dx:
            err -= dy
            x0 += sx

        if e2 <= dy:
            err += dx
            y0 += sy
        count = count + 1 if count < len_pattern -1 else 0

if __name__ == "__main__":

    start_pos = (100, 100)

    w, h = 205, 205 # 200, 200
    image = Image.new('RGB', (w,h), '#FFFFDD')

    draw = ImageDraw.Draw(image)

    dash = (5,5)
    
    for i in range(0,360,5):
        end_pos = polar2cart(start_pos, i, 100)
        DashedLine(draw, start_pos, end_pos,
                fill=(255-int_up(i*0.7),0,int_up(i*0.7)),adjust=True)
    
    #end_pos = (190, 190)
    #DashedLine(draw, start_pos, end_pos,fill='black')

    image.show()
    #image.save('../../figures/zigle_dash_line.png')