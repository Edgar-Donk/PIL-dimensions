import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw
from DimLinesDC import dc, dims_dc, WideLineDC

w, h = 61, 61
c = (w//2, h//2)
ptA = (c[0]-20, c[1]+10) # (40, 60)
ptB = (c[0]+20, c[1]+10) # (80, 60)
text = 'Test'

extA = (5, 3)
ext = sum(extA)
#font = ImageFont.truetype('consola.ttf', 12)
#back = (255,255,221)
dc.image = Image.new('RGB', (w, h), dc.back)
dc.draw = ImageDraw.Draw(dc.image)

dc.fill = (0,0,255)
WideLineDC((ptA[0],ptA[1]+ext), (ptB[0],ptB[1]+ext), width=2)
dc.fill = (0,0,0)

dims_dc(ptA, ptB, extA, text=text)

dc.image.show()
#dc.image.save('../../temp/horiz_above_dim.png')