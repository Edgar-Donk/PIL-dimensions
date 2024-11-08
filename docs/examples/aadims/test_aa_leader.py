from PIL import Image, ImageDraw, ImageFont
from DimLinesAA import leader_aa

'''
def leader_aa(im, dr, at, angle=315, extA=20, extB=20, width=1, arrowhead=(3,5,1),
            arrow='first', fill=(0,0,0), text=None, font=None, back=(255,255,221)):
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
    dimension_aa(im, dr, at, ptB, fill=fill, arrowhead=arrowhead,
              arrow=arrow, back=back)
    LineAA(dr, ptB, ptC, fill=fill, back=back)

    # text position
    tp = ((ptB[0] + ptC[0])//2, ptB[1] - h - 5)

    angled_text(im, tp, text, 0, font)

    #ldraw.text([at[0], at[1] +15], text=text, fill='black')

'''


if __name__ == "__main__":
    text = 'y+ε+m'

    font = ImageFont.truetype('consola.ttf', 12)
    # (wi, ht) = font.getsize(text)
    unused1, unused2, wi, ht = font.getbbox(text)

    eb = wi + 10
    back = (255,255,221)
    fill = (0,0,0)

    image2 = Image.new('RGB', (120, 120), back)
    drawl = ImageDraw.Draw(image2)

    lat = (60, 60)
    a = 45

    leader_aa(image2, drawl, lat, angle=a, extB=20, text=text, font=font, fill=fill,
            back=back)

    image2.show()
    #image2.save('../figures/leader'+str(a)+'.png')



