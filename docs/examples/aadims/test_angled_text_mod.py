import sys
sys.path.append('../dims')

from PIL import Image, ImageFont
from DimLinesPIL import polar2cart, angled_text

if __name__ == "__main__":
    Text = "Chihuly Exhibit"

    Angle = 0

    Font = ImageFont.truetype('consola.ttf', 25)
    # tsize = Font.getsize(Text + str(0000))
    tsize = Font.getbbox(Text + str(0000))

    w = 501
    h = 501
    image2 = Image.new('RGB', (w, h), (255,255,221))
    pt = (200,120) #(w//2, h//2)

    a = (0, 45, 90, 135, 180, 225, 270, 315)
    for j in range(len(a)):
        pt = polar2cart(pt, a[j], tsize[0]//2)
        #print(pt)
        angled_text(image2, pt, Text +' '+ str(a[j]), a[j], font=Font,
                    fill=(0,0,0), aall=1)

    #angled_text(image2, pt, Text +' '+ str(Angle), Angle, font=Font, fill=(0,0,0))
    image2.show()
    #image2.save('../../temp/angled_text.png')

