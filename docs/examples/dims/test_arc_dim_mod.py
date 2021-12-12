from PIL import Image, ImageFont, ImageDraw
from DimLinesPIL import polar2cart, arc_dim

if __name__ == "__main__":
    # Create an empty image
    w, h = 250, 250
    image1 = Image.new('RGBA', (w,h), '#FFFFDD')
    sdraw = ImageDraw.Draw(image1)

    c=(100,100)
    r=30
    Start=350
    End=95
    #Text = str(End-Start) + '°' #if Start < End else str(End + 360 -Start) + '°'

    font_size=15
    Font = ImageFont.truetype('consola.ttf', font_size)

    Ax, Ay = polar2cart(c, Start, 80)
    sdraw.line([c, (Ax, Ay)], width=3, fill='blue')

    Bx, By = polar2cart(c, End, 80)
    sdraw.line([c, (Bx, By)], width=3, fill='blue')

    arc_dim(image1, sdraw, c, r, Start, End, font=Font)
    image1.show()
    #image1.save('../figures/angle_dim_'+ str(start)+'_'+str(end-start)+'.png')