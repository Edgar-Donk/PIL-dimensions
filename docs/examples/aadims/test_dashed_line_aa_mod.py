import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw
from DimLinesPIL import int_up, polar2cart
from DimLinesAA import DashedLineAA

if __name__ == "__main__":

    start_pos = (100, 100)

    w, h = 205, 205 # 200, 200
    image = Image.new('RGB', (w,h), '#FFFFDD')

    draw = ImageDraw.Draw(image)

    dash = (7,1,1,1)

    for i in range(0,360,5):
        end_pos = polar2cart(start_pos, i, 100)
        DashedLineAA(draw, start_pos, end_pos,
                fill=(255-int_up(i*0.7),0,int_up(i*0.7)))

    image.show()
    #image.save('../../figures/zigle_dash_line.png')