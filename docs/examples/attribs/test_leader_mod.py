from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import leader

if __name__ == "__main__":
    Text = 'y+ε+m'

    Font = ImageFont.truetype('consola.ttf', 12)
    #(wi, ht) = Font.getsize(Text)
    unused1,unused2,wi,ht = Font.getbbox(Text)  # text width, height

    eb = wi + 10

    image2 = Image.new('RGB', (120, 120), '#FFFFDD')
    sdraw = ImageDraw.Draw(image2)

    lat = (60, 60)
    a = 315

    leader(image2, sdraw, lat, angle=a, extB=50, text=Text, font=Font)

    image2.show()
    #image2.save('../figures/leader'+str(a)+'.png')