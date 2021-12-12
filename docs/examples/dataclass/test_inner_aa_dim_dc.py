import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw
from DimLinesDC import dc, inner_dim_dc, WideLineDC

if __name__ == '__main__':
    text = 'Test'
    #font = ImageFont.truetype('consola.ttf', 15)

    #Back = (225,225,221)

    dc.image = Image.new('RGB', (120, 120), dc.back)

    dc.draw = ImageDraw.Draw(dc.image)

    Fill = (0,0,0)
    dc.fill = (0,0,255)
    WideLineDC((30,30), (30,90), width=2)
    WideLineDC((90,30), (90,90), width=2)
    dc.fill = (0,0,0)
    #dc.draw.line([(30,30), (30,90)], width=2, fill=Fill)
    #dc.draw.line([(90,30), (90,90)], width=2, fill=Fill)

    ptA = (30,60)
    ptB = (90,60)

    inner_dim_dc(ptA, ptB, text=text)

    #dc.image.save('../../temp/horiz_inner_dc.png') #
    dc.image.show()

