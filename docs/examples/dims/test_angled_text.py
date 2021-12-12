from PIL import Image, ImageFont, ImageDraw
from DimLinesPIL import polar2cart
# https://stackoverflow.com/questions/245447/how-do-i-draw-text-at-an-angle-using-pythons-pil
# stenci
# text aligned middle of text

def angled_text(im, at, text, angle, font=None, fill=(0,0,0), aall=1):

    if font is None:
        font = ImageFont.load_default()

    (wide, height) = font.getsize(text)
    wide = wide + 10

    image1 = Image.new('RGBA', (wide, height), (255,255,255,0))
    draw1 = ImageDraw.Draw(image1)

    draw1.text((0, 0), text=text, font=font, fill=fill)

    # ensure angles within 0 to 360
    angle = 360 + angle if angle < 0 else angle
    angle = angle if angle < 360 else angle - 360

    if aall == 0:
        if 90 <= angle < 180:
            angle = angle + 180
        if 180 <= angle < 270:
            angle = angle - 180

    px, py = at
    # rotate angle in degrees anticlockwise
    image1 = image1.rotate(-angle, expand=1, resample=Image.BICUBIC)

    sx, sy = image1.size

    if 0 <= angle < 90:
        im.paste(image1, (px-sx//2, py-sy//2, px + sx-sx//2, py + sy-sy//2), image1)
    elif 90 <= angle <= 180:
        im.paste(image1, (px-sx//2, py - sy+sy//2, px + sx-sx//2, py+sy//2 ), image1)
    elif 180 < angle < 270:
        im.paste(image1, (px-sx+sx//2, py-sy+sy//2, px+sx//2, py+sy//2 ), image1)
    elif 270 <= angle < 360:
        im.paste(image1, (px-sx//2, py-sy//2, px + sx-sx//2, py + sy-sy//2), image1)
    #print('angle',angle,'wide,height' ,wide,height,'px,py',px,py,'sx,sy',sx,sy)

if __name__ == "__main__":
    Text = "Chihuly Exhibit" 

    Angle = 0

    Font = ImageFont.truetype('consola.ttf', 25)
    tsize = Font.getsize(Text + str(0000))

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

