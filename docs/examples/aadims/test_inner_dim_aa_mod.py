from PIL import Image, ImageDraw, ImageFont
from DimLinesAA import inner_dim_aa

if __name__ == '__main__':
    Text = 'Test'
    Font = ImageFont.truetype('consola.ttf', 15)

    image2 = Image.new('RGB', (120, 120), '#FFFFDD')

    draw2 = ImageDraw.Draw(image2)

    draw2.line([(30,30), (90,30)], width=2, fill='black')
    draw2.line([(30,90), (90,90)], width=2, fill='black')

    pta = (60,30)
    ptb = (60,90)

    inner_dim_aa(image2, draw2, pta, ptb, text=Text, font=Font)

    image2.show()