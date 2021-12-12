import sys
sys.path.append('../dims')

#from PIL import Image, ImageDraw
from DimLinesPIL import polar2cart
from DimLinesattr import aq, arc_dim_attr, WideLineATTR


if __name__ == "__main__":
    #w, h = 201, 201
    #dc.image = Image.new('RGB', (w,h), dc.back)
    #dc.draw = ImageDraw.Draw(dc.image)

    c=(100,108)
    r=30
    start=55
    end=125

    ax, ay = polar2cart(c, start, 80)
    bx, by = polar2cart(c, end, 80)
    #sdraw.line([c, (ax, ay)], width=3, fill='black')
    #dc.fill = (0,0,255)
    WideLineATTR(c, (ax, ay), width=2)
    WideLineATTR(c,(bx, by), width=2)
    #dc.fill = (0,0,0)
    #LineATTR(c, (ax, ay))


    #sdraw.line([c, (bx, by)], width=3, fill='black')
    #LineATTR(c, (bx, by))

    arc_dim_attr(c, r, start, end)

    aq.image.show()
    #diff = end-start if start<=270 else 360-start+end
    #print('angle_dim_'+ str(start)+'_'+str(diff)+'.png')
    #dc.image.save('../../temp/angle_dim_'+ str(start)+'_'+str(end)+'.png')