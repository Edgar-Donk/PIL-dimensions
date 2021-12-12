from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import slant_dim, polar2cart

if __name__ == "__main__":
    Text = 'Test'
    Angle = 225
    At = (60, 60)
    ptb = (30, 30)
    Length = 50
    exta = (10,) #15 #
    Font = ImageFont.truetype('consola.ttf', 15)

    image2 = Image.new('RGB', (120, 120), '#FFFFDD')

    sdraw = ImageDraw.Draw(image2)
    ct = polar2cart(At, Angle, Length)

    sdraw.line([At, ct], width=2, fill='blue')

    slant_dim(image2, sdraw, At, extA=exta, fill=(0,0,0), length=Length,
                    angle=Angle, text=Text, font=Font)

    image2.show()