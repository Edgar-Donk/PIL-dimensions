import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw
from DimLinesPIL import polar2cart
from DimLinesDC import dc, thickness_dim_dc, WideLineDC

if __name__ == "__main__":
    text = 'Test'
    angle = 270
    at = (40, 45)
    thick = 20
    #font = ImageFont.truetype('consola.ttf', 15)

    dc.image = Image.new('RGB', (80, 80), dc.back)

    dc.draw = ImageDraw.Draw(dc.image)

    a = polar2cart(at, angle+90, 30)
    b = polar2cart(at, angle-90, 30)
    c = polar2cart(polar2cart(at, angle, thick), angle+90, 30)
    d = polar2cart(polar2cart(at, angle, thick), angle-90, 30)

    dc.fill = (0,0,255)
    WideLineDC((a), (b), width=2)
    WideLineDC((c), (d), width=2)
    dc.fill = (0,0,0)
    #dc.draw.line([a,b], width=2, fill='blue')
    #dc.draw.line([c,d], width=2, fill='blue')

    thickness_dim_dc(at, thick, angle=angle, text=text)

    dc.image.show()
    #dc.image.save('../../temp/thick_dim_'+str(angle)+'.png') #show()


