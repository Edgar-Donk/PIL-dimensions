import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw
from DimLinesPIL import polar2cart
from DimLinesDC import dc, WideLineDC, slant_dim_dc


if __name__ == "__main__":
    text = 'Test'
    angle = 0
    at = (60, 60)
    ptB = (100, 60)
    a = (30, 100)
    f = (236, 50)
    length = 40
    extA = (10, 5) #15 #
    dc.image = Image.new('RGB', (300, 160), dc.back) # 120, 120

    dc.draw = ImageDraw.Draw(dc.image)
    ct = polar2cart(at, angle, length)
    slant_dim_dc(a, ptB=f, extA=(8,2), text=text)

    WideLineDC(a,f, width=2)

    dc.image.show()
    #image2.save('../figures/slant_dim_'+str(angle) +'.png') # .show()