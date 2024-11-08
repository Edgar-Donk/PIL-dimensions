import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw
from DimLinesDC import dc, leader_dc


if __name__ == "__main__":
    text = 'y+ε+m'

    #font = ImageFont.truetype('consola.ttf', 12)
    #(wi, ht) = dc.font.getsize(text)
    unused1, unused2, wi, ht = dc.font.getbbox(text)

    eb = wi + 10
    #back = (225,225,221)
    dc.image = Image.new('RGB', (120, 120), dc.back)
    # Get drawing context
    dc.draw = ImageDraw.Draw(dc.image)

    lat = (60, 60)
    a = 45
    #fill = (0,0,0)
    leader_dc(lat, angle=a, extB=20, text=text)

    dc.image.show()
    #image2.save('../figures/leader'+str(a)+'.png')



