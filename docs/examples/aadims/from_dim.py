def arc_dim_aa(im,dr,centre,radius,begin,end,fill=(0,0,0),text=None,font=None,
                arrowhead=(8,10,3),back=(225,225,221),aall=0):
    # x,y,radius all relate to centre coords and radius, give 2 angles
    rtimes2 = max(60, radius*2)
    if isinstance(begin, int):
        beginp = polar2cart(centre, begin, rtimes2)
    if isinstance(end, int):
        endp = polar2cart(centre, end, rtimes2)
    if isinstance(begin, tuple):
        beginp = begin
        begin, rayb = cart2polar(centre, begin)
    if isinstance(end, tuple):
        endp = end
        end, raye = cart2polar(centre, end)

    beginr = radians(begin)
    endr = radians(end)

    bq = findSect(centre, beginp)
    eq = findSect(centre, endp)

    alpha = (360 - begin + end)/2 if bq[1] == 4 and eq[1] == 1 else (begin + end)/2
    diff = 360 - begin + end if bq[1] == 4 and eq[1] == 1 else end - begin

    if diff == 180:
        raise Exception('arc_dim_aa: angle is 180°, begin {} end {}' \
            ' difference {} cannot draw dimension'.format(begin, end, diff))

    if diff == 90:
        ax, ay = polar2cart(centre, begin, radius)
        bx, by = polar2cart(centre, end, radius)
        dx, dy = polar2cart(centre, alpha, radius*sqrt(2))

        LineAA(dr, (ax,ay), (dx,dy), fill=fill, back=back)
        LineAA(dr, (bx,by), (dx,dy), fill=fill, back=back)

    else:
        x, y = centre
        d1, d2, d3 = arrowhead

        # placement of arrows, 'first' point inwards
        order = 'last' if sin(radians(diff)) * radius > 4 * arrowhead[1] else 'first'

        # find begin and end arc
        start = int_up(x + radius * cos(beginr)), int_up(y + radius * sin(beginr))
        finish = int_up(x + radius * cos(endr)), int_up(y + radius * sin(endr))

        dimension_aa(im,dr, start, angle=(begin - 90), arrow=order,fill=fill,back=back)
        dimension_aa(im,dr, finish, angle=(end + 90), arrow=order,fill=fill,back=back)

        start_arc = polar2cart(start, (begin + 90), d1)
        finish_arc = polar2cart(finish, end - 90, d1)

        if order == 'first':
            make_arc_aa(dr, centre, radius, beginp, endp, fill=fill, back = back)
        else:
            make_arc_aa(dr, centre, radius, start_arc, finish_arc, fill=fill, back = back)

    # placement of text
    if text is None:
        text = str(diff) + '°'
    if font is None:
        font_size=15
        font = ImageFont.truetype('consola.ttf', font_size)
    (wide, ht) = font.getsize(text)

    # stop upside down text
    if begin + alpha > 360:
        alpha = begin + alpha -360

    if 0 <= alpha <= 180:
        angle = 270-alpha
        da = 7
    elif 180 < alpha < 360:
        angle = 90-alpha
        da = 7

    if diff == 90:
        X, Y = polar2cart(centre, alpha, radius * sqrt(2) + da)
    else:
        t = tan(radians(diff/2))
        a = wide/ 2 / t
        size = max(radius, a)
        X, Y = polar2cart(centre, alpha, size + ht/2+da)

    angled_text(im, (X, Y), text, angle, font, aall=aall)
