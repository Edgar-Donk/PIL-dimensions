from PIL import Image, ImageDraw, ImageFont
from DimLinesAA import dims_aa

if __name__ == "__main__":


    c = (60,60)
    pta = (c[0], c[1]-20) # (40, 60)
    ptb = (c[0], c[1]+20) # (80, 60)
    Text = str(pta)+','+ str(ptb)

    exta = (-5, -3)
    Font = ImageFont.truetype('consola.ttf', 12)

    image2 = Image.new('RGB', (120, 120), '#FFFFDD')
    sdraw = ImageDraw.Draw(image2)

    sdraw.line([pta, ptb], width=1, fill='black')

    dims_aa(image2, sdraw, pta, ptb, exta, text=Text, font=Font, textorient='v',
        tail=True)

    image2.show()
    #image2.save('../figures/horiz_above_dim.png')