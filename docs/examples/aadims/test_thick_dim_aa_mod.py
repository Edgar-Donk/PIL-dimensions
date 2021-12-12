import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import polar2cart
from DimLinesAA import thickness_dim_aa

if __name__ == "__main__":
    Text = 'Test'
    Angle = 0
    At = (40, 40)
    Thick = 20
    Font = ImageFont.truetype('consola.ttf', 15)
    #(width, height), (offset_x, offset_y) = Font.font.getsize(text)

    image2 = Image.new('RGB', (80, 80), '#FFFFDD')

    draw = ImageDraw.Draw(image2)
    a = polar2cart(At, Angle+90, 30)
    b = polar2cart(At, Angle-90, 30)
    c = polar2cart(polar2cart(At, Angle, Thick), Angle+90, 30)
    d = polar2cart(polar2cart(At, Angle, Thick), Angle-90, 30)
    draw.line([a,b], width=2, fill='blue')
    draw.line([c,d], width=2, fill='blue')

    thickness_dim_aa(image2, draw, At, Thick, angle=Angle, text=Text, font=Font)

    image2.show()
    #image2.save('../figures/thick_dim_'+str(Angle)+'.png')