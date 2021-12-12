from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import angled_text, dimension, polar2cart


def leader(im, dr, at, angle=315, extA=20, extB=20, width=1, arrowhead=(3,5,10),
            arrow='first', fill=(0,0,0), text=None, font=None):
    # leader to object, angle and length (extA) first part, then goes horizontal
    # for second part (extB). Only one arrow where leader points.
    # start at,

    #font = ImageFont.load_default() if font is None else font
    font = font if font else ImageFont.load_default()
    (wide, height) = font.getsize(text)

    h = height // 2

    if wide > extB:
        print('extB was increased from:',extB,'to accommodate the text',wide+10)
        extB = wide+10


    # dimension line
    phi = 180 if 90 < angle < 270 else 0
    ptB = polar2cart(at, angle, extA)
    ptC = polar2cart(ptB, phi, extB)
    dimension(dr, at, ptB, width=width, fill=fill, arrowhead=arrowhead,
              arrow=arrow)
    dr.line([ptB, ptC], width=width, fill=fill)

    # text position
    tp = ((ptB[0] + ptC[0])//2, ptB[1] - h - 5)

    angled_text(im, tp, text, 0, font, aall=0)

    #ldraw.text([at[0], at[1] +15], text=text, fill='black')

if __name__ == "__main__":
    Text = 'y+ε+m'

    Font = ImageFont.truetype('consola.ttf', 12)
    (wi, ht) = Font.getsize(Text)

    eb = wi + 10

    image2 = Image.new('RGB', (120, 120), '#FFFFDD')
    sdraw = ImageDraw.Draw(image2)

    lat = (60, 60)
    a = 315

    leader(image2, sdraw, lat, angle=a, extB=50, text=Text, font=Font)

    image2.show()
    #image2.save('../figures/leader'+str(a)+'.png')



