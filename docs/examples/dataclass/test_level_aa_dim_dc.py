import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw
from DimLinesDC import dc, level_dim_dc

if __name__ == "__main__":
    #font = ImageFont.truetype('consola.ttf', 12)
    text='2500 hl'
    #wide, height = dc.font.getsize(text)
    unused1, unused2, wide, height = dc.font.getbbox(text)  # text width, height


    #back = (255,255,221)

    w, h = 200, 200
    dc.image = Image.new('RGB', (w,h), dc.back)

    dc.draw = ImageDraw.Draw(dc.image)

    a=(10,10)
    b=(10,190)
    c=(190,10)
    d=(190,190)
    fill = (0,0,0)

    dc.draw.line([a,b], width=2, fill=dc.fill)
    dc.draw.line([c,d], width=2, fill=dc.fill)

    at=(10,100)
    diam = c[0] - a[0]

    # DimLinesDC.py", line 1070
    # DashedLine() got an unexpected keyword argument 'back'
    level_dim_dc(at, diam, ldrA=20, ldrB=20, dash=(10,4), text=text, tri=8)

    dc.image.show()
    #image.save('../figures/level_dim_neg.png') # show()