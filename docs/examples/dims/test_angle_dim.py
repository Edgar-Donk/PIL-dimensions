from PIL import Image, ImageFont, ImageDraw
from math import sqrt, radians, sin, cos
from DimLinesPIL import polar2cart, create_arc, angled_text, dimension


def arc_dim(im, dr, centre, radius, begin, end, fill=(0,0,0),
            text=None, font=None, arrowhead=(8,10,3)):
    # x,y,radius all relate to centre coords and radius, give 2 angles
    # arcs all less than 180

    beginr = radians(begin)
    endr = radians(end)
    alpha = (begin + end) / 2 #if begin < end else (begin + 360 + end) / 2 
    diff = end - begin # if begin < end else end + 360 - end
    if diff == 180:
        raise Exception('angle dimension: angle is 180°, begin {} end {}' \
            ' difference {} cannot draw dimension'.format(begin, end, diff))

    if diff == 90:
        ax, ay = polar2cart(centre, begin, radius)
        bx, by = polar2cart(centre, end, radius)
        dx, dy = polar2cart(centre, alpha, radius*sqrt(2))

        dr.line([(ax,ay), (dx,dy)], fill=fill)
        dr.line([(bx,by), (dx,dy)], fill=fill)

    else:
        x, y = centre

        create_arc(dr,centre,radius, begin, end, fill=fill)
        # find begin and end arc
        start = x + radius * cos(beginr), y + radius * sin(beginr)
        finish = x + radius * cos(endr), y + radius * sin(endr)

        # placement of arrows, 'first' point outwards
        order = 'last' if abs(endr - beginr) * radius > 4 * arrowhead[1] else 'first'

        dimension(dr, start, angle=(begin - 90), arrow=order)
        dimension(dr, finish, angle=(end + 90), arrow=order)

    # placement of text
    wide, ht = font.getsize(text)
    
    angle = 90 - (begin + end) / 2 
    angle = 360 + angle if angle < 0 else angle
    angle = angle - 360 if angle >= 360 else angle
    '''
    # stop upside down text
    if 0 <= angle <= 180:
        angle = 90-angle
        da = 0
    elif 180 < angle < 360:
        angle = 270-angle
        da = 7
    '''
    
    el = wide/2/sin(radians(diff/2))
    ray = max(radius*0.8,el)
    
    if diff == 90:
        X, Y = polar2cart(centre, alpha, ray*1.7) # radius * sqrt(2) + da
    else:
        X, Y = polar2cart(centre, alpha, (ray+ht)*1.1) # radius + height/2 + da #*1.3

    angled_text(im, (X, Y), text, angle, font=Font, fill=fill, aall=0)


if __name__ == "__main__":
    # Create an empty image
    w, h = 250, 250
    image1 = Image.new('RGBA', (w,h), '#FFFFDD')
    sdraw = ImageDraw.Draw(image1)

    c=(100,100)
    r=30
    Start=350
    End=375
    Text = str(End-Start) + '°' #if Start < End else str(End + 360 -Start) + '°'

    font_size=15
    Font = ImageFont.truetype('consola.ttf', font_size)

    Ax, Ay = polar2cart(c, Start, 80)
    sdraw.line([c, (Ax, Ay)], width=3, fill='blue')

    Bx, By = polar2cart(c, End, 80)
    sdraw.line([c, (Bx, By)], width=3, fill='blue')

    arc_dim(image1, sdraw, c, r, Start, End, text=Text, font=Font)
    image1.show()
    #image1.save('../figures/angle_dim_'+ str(start)+'_'+str(end-start)+'.png') # show()