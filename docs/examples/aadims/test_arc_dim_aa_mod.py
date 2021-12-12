import sys
sys.path.append('../dims')

from PIL import Image, ImageFont, ImageDraw
from DimLinesPIL import polar2cart
from DimLinesAA import arc_dim_aa, WideLineAA

if __name__ == "__main__":
    # Create an empty image
    w, h = 201, 201 #250, 250
    image1 = Image.new('RGBA', (w,h), '#FFFFDD')
    sdraw = ImageDraw.Draw(image1)

    c=(101,101) # 100,100
    r=30
    Start=350
    End=25
    #Text = str(End-Start) + '°' #if Start < End else str(End + 360 -Start) + '°'

    font_size=15
    Font = ImageFont.truetype('consola.ttf', font_size)

    Ax, Ay = polar2cart(c, Start, 80)
    WideLineAA(sdraw, c, (Ax, Ay), width=3, fill=(0,0,255))

    Bx, By = polar2cart(c, End, 80)
    WideLineAA(sdraw, c, (Bx, By), width=3, fill=(0,0,255))

    arc_dim_aa(image1, sdraw, c, r, Start, End, font=Font)
    image1.show()
    #image1.save('../figures/angle_dim_'+ str(start)+'_'+str(end-start)+'.png')