from PIL import Image, ImageDraw, ImageFont
from DimLinesAA import leader_aa

if __name__ == "__main__":
    Text = 'y+ε+m'

    Font = ImageFont.truetype('consola.ttf', 12)
    (wi, ht) = Font.getsize(Text)

    eb = wi + 10

    image2 = Image.new('RGB', (120, 120), '#FFFFDD')
    sdraw = ImageDraw.Draw(image2)

    lat = (60, 60)
    a = 315

    leader_aa(image2, sdraw, lat, angle=a, extB=50, text=Text, font=Font)

    image2.show()
    #image2.save('../figures/leader'+str(a)+'.png')