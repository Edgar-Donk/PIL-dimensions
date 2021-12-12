import sys
sys.path.append('../dims')

#from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import polar2cart
from DimLinesattr import aq, dimension_attr

text = 'Test'
angle = 30

at = (60, 60)
ptB = (100, 60)
length = 40
extA = (10, 5) #15 #
#font = ImageFont.truetype('consola.ttf', 15)
#back = dc.back
#dc.image = Image.new('RGB', (120, 120), dc.back)

#dc.draw = ImageDraw.Draw(dc.image)
ct = polar2cart(at, angle, length)
#fill = dc.fill
#WideLineATTR(sdraw, at, ct, width=2, fill=fill, back=back)

ptA=(10,110)
ptB=(10,10)
ptC=(20,10)
ptD=(110,110)
dimension_attr(ptA, ptB) # ptB=ptB,  at, ct
dimension_attr(ptC, ptD)

# slant_dim(im, ptA, ptB =None, extA=None,  angle=None, length=None,
            #fill='black', width=1, text=None, Font=None)

aq.image.show()
#image2.save('../figures/slant_dim_'+str(angle) +'.png') # .show()
#dc.image.save('../../temp/dimension_2_attr_arrows.png')

'''
image2 = Image.new('RGB', (120, 120), '#FFFFDD')
sdraw = ImageDraw.Draw(image2)

arrowhead=(8, 10, 3)
fill='black'
width=1
ptA=(10,110)
ptB=(10,10)
dimension(image2, ptA, ptB, width=width, fill=fill, arrowhead=arrowhead,
                arrow='both')
ptC=(20,10)
ptD=(110,110)
dimension(image2, ptC, ptD, width=width, fill=fill, arrowhead=arrowhead,
                arrow='both')
'''