from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import dims

if __name__ == "__main__":


    c = (60,60)
    ptA = (c[0], c[1]-20) # (40, 60)
    ptB = (c[0], c[1]+20) # (80, 60)
    Text = str(ptA)+','+ str(ptB)

    Exta = (8,3)
    Extb = (28, 3)
    Text = str(Exta)
    atot = sum(Exta)
    btot = sum(Extb)
    back = (255,255,221)

    Font = ImageFont.truetype('consola.ttf', 12)

    image2 = Image.new('RGB', (120, 120), back)
    sdraw = ImageDraw.Draw(image2)

    if ptA[0] == ptB[0]:
        sdraw.line([(ptA[0]+atot, ptA[1]), (ptB[0]+btot, ptB[1])],
                fill=(0,0,255), width=2)
    else:
        sdraw.line([(ptA[0], ptA[1]+atot), (ptB[0], ptB[1]+btot)],
                fill=(0,0,255), width=2)

    dims(image2, sdraw, ptB, ptA, Exta, extB=Extb, text=Text, font=Font,
        tail=True)

    image2.show()
    #image2.save('../figures/horiz_above_dim.png')