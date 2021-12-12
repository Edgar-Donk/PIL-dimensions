from PIL import Image, ImageDraw
from DimLinesAA import PartLineAA
# corrected
'''
def LineAA(draw, pta, ptb, fill=(0,0,0), back=(255,255,255), cross=0):
    # draw a dark anti-aliased line on light background
    x0, y0 = pta
    x1, y1 = ptb
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy   # error value e_xy
    slope = (y1-y0)/(x1-x0) if x1!=x0 else 0
    ed = dx + dy
    print(pta,ptb,'sx',sx,'sy',sy,'slope',slope) # pink x-step below main all time sy -ive

    ed = 1 if ed == 0 else sqrt(dx*dx+dy*dy) # max(dx, dy) #
    dr = dx + 1 if dx > dy else dy + 1 # better plotting when steep

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
        #hue = int(255*abs(err-dx+dy)/ed)
        #hue = diffs[abs(err-dx+dy)]
        #print(int(255*abs(err-dx+dy)/ed))
        draw.point([x0, y0], fill=diffs[abs(err-dx+dy)])
        #print(err,[x0, y0], err-dx+dy)
        e2 = err
        x2 = x0
        if e2<<1 >= -dx:                # y-step
            if e2+dy < ed and x < dr - 1:
                #hue = int(255*(e2+dy)/ed)
                if (cross < 0 and slope < 0) or (cross > 0 and slope > 0) or cross==0:
                    #pass
                    #print([x0,y0+sy],round(slope,3),'-ve')
                #else:
                    draw.point([x0,y0+sy], fill=diffs[abs(e2+dy)])
                #print(e2+dy)
            err -= dy
            x0 += sx
        if e2<<1 <= dy and x < dr - 1:  # x-step
            #print(x2, dr)
            if dx-e2 < ed:
                #hue = int(255*(dx-e2)/ed)
                if (cross < 0 and slope > 0) or (cross > 0 and slope < 0) or cross==0:
                    #pass
                    #print([x2+sx,y0],round(slope,3),'+ve')
                #else:
                    draw.point([x2+sx,y0], diffs[abs(dx-e2)])
                #draw.point([x2+sx,y0], 'pink')
                #print(dx-e2)
            err += dx
            y0 += sy

'''

if __name__ == "__main__":

    '''
    w, h = 210, 210
    start_pos = (w//2, h//2)
    #start_pos = (0,0)
    #end_pos = 5,14
    # 15,6

    '''
    w,h = 21,21
    image = Image.new('RGB', (w,h), '#FFFFDD') #  #'lightblue'
    drawl = ImageDraw.Draw(image)
    start_pos = (10, 15)
    end_pos = (7, 5)
    PartLineAA(drawl, start_pos, end_pos, back=(255,255,221),fill=(0,0,0),cross=-21) #,cross=21

    pta = (12,15)
    ptb = (15,5)
    PartLineAA(drawl, pta, ptb, back=(255,255,221),fill=(0,0,0),cross=-21) #,cross=-21
    '''
    w, h = 29, 29
    start_pos = (w//2, h//2)
    end_pos = 19,18

    image = Image.new('RGB', (w,h), '#FFFFDD') #  #'lightblue'
    drawl = ImageDraw.Draw(image)

    #LineAA(drawl, start_pos, end_pos, back=(255,255,221),fill=(255,0,0))

    #image.show()


    a = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
    w, h = 210, 210 # 140, 140
    start_pos = (w//2, h//2)

    image = Image.new('RGB', (w,h), '#FFFFDD')
    drawl = ImageDraw.Draw(image)

    for i in range(len(a)): # len(a)
        end_pos = polar2cart(start_pos, a[i], 65)
        LineAA(drawl, start_pos, end_pos,
                fill=(0,0,0))

    for i in range(0, 360,5): # len(a)
        end_pos = polar2cart(start_pos, i, 100)
        LineAA(drawl, start_pos, end_pos,
                width=1, fill='black')
    '''
    image.show()

    #image.save('../figures/zigl_aa.png')
