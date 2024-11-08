from PIL import Image, ImageFont, ImageDraw
from DimLinesPIL import polar2cart, angled_text

Text = 'Test' #"Chihuly Exhibit"


Font = ImageFont.truetype('consola.ttf', 25)
#tsize = Font.getsize(Text) #  + str(0000)
#unused1,unused2,wide,ht
tsize = Font.getbbox(Text)  # text width, height

w = 501
h = 501
image2 = Image.new('RGB', (w, h), (255,255,221))
dr = ImageDraw.Draw(image2)
pt = (200,120) #(w//2, h//2)

a = (330,) #(0, 45, 90, 135, 180, 225, 270, 315)
for j in range(len(a)):
    pt = polar2cart(pt, a[j], tsize[2]//2)
    print(pt)
    dr.point(pt, fill='red')
    angled_text(image2, pt, Text, a[j], font=Font, #  +' '+ str(a[j])
                    fill=(0,0,0), aall=0)

image2.show()