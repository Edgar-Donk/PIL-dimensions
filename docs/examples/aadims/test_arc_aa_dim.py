import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict
from math import radians, sqrt, sin, cos, tan
from DimLinesPIL import polar2cart, angled_text, int_up
from DimLinesAA import WideLineAA, findSect, LineAA, dimension_aa

def plot_sector_points(dr, xm, ym, x, y, sects, fill, all8=1):
    # plots all 8 sectors or only 4 sectors in the while loop
    if sects[0] < 0:
        ltemp = list(sects)
        ltemp[0] = -ltemp[0]
        sects = tuple(ltemp)
    if all8 == 1:
        if sects[0] == 1 or sects[1] == 1:
            dr.point((xm-x, ym+y), fill)               # I Octant
        elif sects[0] == 3 or sects[1] == 3:
            dr.point((xm-y, ym-x), fill)               # III. Octant
        elif sects[0] == 5 or sects[1] == 5:
            dr.point((xm+x, ym-y), fill)               # V  Octant
        elif sects[0] == 7 or sects[1] == 7:
            dr.point((xm+y, ym+x), fill)                #   VII. Octant

    if sects[0] == 4 or sects[1] == 4:
        dr.point((xm+x, ym+y), fill)               #  IV . Octant  +x +y
    elif sects[0] == 2 or sects[1] == 2:
        dr.point((xm+y, ym-x), fill)               # II Octant
    elif sects[0] == 8 or sects[1] == 8:
        dr.point((xm-x, ym-y), fill)               #  VIII. Octant  -x +y
    elif sects[0] == 6 or sects[1] == 6:
        dr.point((xm-y, ym+x), fill)               # VI Octant

def PartCircleAA(dr, xm, ym, r, start, finish, width, sects, fill=(0,0,0),
                    back=(255,255,221)):
    # xm, ym = centre
    # draw an antialiased circle on light background
    x = -r
    y = 0                                   # IV. Octant from left to bottom left

    err = 2 - 2 * r                         # initial difference

    sslope = abs((ym-start[1])/(xm-start[0]))
    fslope = abs((ym-finish[1])/(xm-finish[0]))
    # check sects
    ssect = 0
    fsect = 0
    plot = 0
    ssect, fsect = sects
    if sects[0] == sects[1]:
        # start, finish in one sector
        plot = 0
    elif (sects[0] == 0 and sects[1] in (1,3,5,7)) or \
            (sects[0] in (2,4,6,8) and sects[1] == 0):
        plot = 1

    if sects[0] < 0:
        plot = 1

    maxdi = [0]
    for n in range(0, width+1):
        maxdi.append(maxdi[n] + 2 * (r-n) -1)
    maxdi.remove(0)
    maxd = maxdi[0]
    # ensure inner aa working with conditions for single aa
    # find maxd of smallest main circle
    maxdsm = 2 * (r-width+1) - 1
    # thick factor used outer main lines
    thfact = (width-1)/2

    def errs(comp, size,j):
        return 255 if comp == 255 else int((255-comp) * j / size) + comp

    diffs = defaultdict(list)
    diffs = defaultdict(lambda:back, diffs)
    for i in range(maxd):
        if fill == (0,0,0):
            diffs[i] = tuple(int(255*i/maxd) for k in range(3))
        else:
            diffs[i] = tuple(errs(fill[k],maxd,i) for k in range(3))

    diffsm = defaultdict(list)
    diffsm = defaultdict(lambda:back, diffsm)
    for i in range(maxdsm):
        if fill == (0,0,0):
            diffsm[i] = tuple(int(255*i/maxdsm) for k in range(3))
        else:
            diffsm[i] = tuple(errs(fill[k],maxdsm,i) for k in range(3))

    while -x > y - 1:
        # actual and inverse slope
        aslope = abs((-y)/(-x))
        cslope = abs(-x/(y+0.2))

        if ssect in (1,5) and plot == 0:
            if aslope >= sslope:
                plot = 1
        elif fsect in (1,5) and plot == 1:
            if aslope >= fslope:
                plot = 0
        elif fsect in (2,6) and plot == 0: # and ssect > 0:
            if cslope <= fslope:
                plot = 1
        elif ssect in (2,6) and plot == 1:
            if cslope <= sslope:
                plot = 0

        elif ssect in (3,7) and plot == 0:
            if cslope <= sslope:
                plot = 1
        elif fsect in (3,7) and plot == 1:
            if cslope <= fslope:
                plot = 0
        elif fsect in (4,8) and plot == 0:
            if aslope >= fslope:
                plot = 1
        elif ssect in (4,8) and plot == 1:
            if aslope >= sslope:
                plot = 0

        err0 = err
        e2 = err-(2*y+1)-(2*x+1) # abs(err+2*(x+y)-2)
        ea = abs(e2)
        out = max(0,int(ea-thfact))
        if plot == 1:
            plot_sector_points(dr, xm, ym, x, y, sects, (diffs[out] if out > 0 else fill),
                    all8 = (1 if (xm+x, ym+y) != (xm-y, ym-x) \
                    or (x==-r and y == 0) else 0))

        # fill out diagonals
        x0 = -x
        eout = abs(e2 + 2*x0 + 2*y + 2)
        if eout < maxd: # and (width-1)//2 == 0
            if plot == 1:
                plot_sector_points(dr, xm, ym, x-1, y+1, sects, (diffs[eout] if eout > 0 else fill),
                    all8 = (1 if (xm+x, ym+y) != (xm-y, ym-x) else 0))

        ein = e2
        x0 = -x
        for n in range(0, width):
            ein = ein-(2*(x0-n)-1)
            e0 = -ein

            if n < width-2:
                fact = fill
            elif n == width-1:
                fact = diffs[abs(int(e0-maxd*thfact/10))] if n==0 else \
                        diffsm[e0-maxdi[n-1]]
            else:
                fact = diffsm[max(0,int(abs(e0-maxdi[n])-maxdsm*thfact/10))] # e2-maxdsm
            if plot == 1:
                plot_sector_points(dr, xm, ym, x+n+1, y, sects, fact,
                    all8 = (1 if (xm+x, ym+y) != (xm-y, ym-x) else 0))

        if (err0 <= y):
            y += 1
            err += y * 2 + 1            # e_xy+e_y < 0

        if (err0 > x or err > y):          # e_xy+e_x > 0 or no 2nd y-step
            x += 1
            # aa missed by diagonals
            eout = abs(e2 + 2*y - 1)
            if eout < maxd:
                if plot == 1:
                    plot_sector_points(dr, xm, ym, x-1, y, sects, (diffs[eout] if eout > 0 else fill),
                        all8 = (1 if (xm+x, ym+y) != (xm-y, ym-x) else 0))
            err += x * 2 + 1            # -> x-step now

def make_arc_aa(dr, centre, radius, start, finish, width=1, fill=(0,0,0), back = (255,255,221)):
    xm,ym = centre
    sq = findSect((xm, ym), (start[0], start[1]))
    fq = findSect((xm, ym), (finish[0], finish[1]))
    sects = ()

    diff_sect = fq[0] - sq[0]

    if diff_sect == 0:
        sects = sq[0],fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

    elif (diff_sect == 1) or (sq[0] == 8 and fq[0] == 1):
        sects = sq[0],0
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)
        sects = 0,fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

    elif (diff_sect == 2) or (sq[0] == 8 and fq[0] == 2) or (sq[0] == 7 and fq[0] == 1):
        sects = sq[0],0
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)
        if sq[0] < 8:
            sects = -sq[0]-1,-sq[0]-1
        else:
            sects = -1,-1
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)
        sects = 0,fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

    elif (diff_sect == 3) or (sq[0] == 8 and fq[0] == 3) or (sq[0] == 7 and fq[0] == 2):
        sects = sq[0],0
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

        if sq[0] < 7:
            sects = -sq[0]-2,-sq[0]-2
        else:
            sects = -1,-1
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

        if sq[0] < 8:
            sects = -sq[0]-1,-sq[0]-1
        else:
            sects = -2,-2
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

        sects = 0,fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

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

    if bq[1] in (3,4) and eq[1] in (1,2):
        alpha = (360 - begin + end)/2
        diff = 360 - begin + end
    else:
        alpha = (begin + end)/2
        diff = end - begin

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
        order = 'last' if radians(diff) * radius > 4 * arrowhead[1] else 'first'

        # find begin and end arc
        start = int_up(x + radius * cos(beginr)), int_up(y + radius * sin(beginr))
        finish = int_up(x + radius * cos(endr)), int_up(y + radius * sin(endr))
        dimension_aa(im,dr, start, angle=(begin - 90), arrow=order,fill=fill,back=back)
        dimension_aa(im,dr, finish, angle=(end + 90), arrow=order,fill=fill,back=back)

        start_arc = polar2cart(start, (begin + 90), d1)
        finish_arc = polar2cart(finish, end - 90, d1)

        if order == 'first':
            make_arc_aa(dr, centre, radius, beginp, endp, fill=fill, back=back)
        else:
            make_arc_aa(dr, centre, radius, start_arc, finish_arc, fill=fill, back=back)

    # placement of text
    if text is None:
        text = str(diff) + '°'
    if font is None:
        font_size=15
        font = ImageFont.truetype('consola.ttf', font_size)
    # (wide, ht) = font.getsize(text)
    unused1, unused2, wide, ht = font.getbbox(text)

    # stop upside down text
    if bq[1] in (3,4) and eq[1] in (1,2):
        alpha = begin + alpha -360

    angle = alpha - 90
    da = 7

    if diff == 90:
        X, Y = polar2cart(centre, alpha, radius * sqrt(2) + da)
    else:
        t = tan(radians(diff/2))
        a = wide/ 2 / t
        size = max(radius, a)
        X, Y = polar2cart(centre, alpha, size + ht/2+da) # alpha

    angled_text(im, (X, Y), text, angle, font, aall=aall)


if __name__ == "__main__":

    Xm = 101 #w//2
    Ym = 101 # h//2
    Radius = 30

    w, h = 201, 201
    Back = (255,255,221)
    image = Image.new('RGB', (w,h), Back) #'#FFFFDD'
    drawl = ImageDraw.Draw(image)


    beg = 260
    Diff = 105
    e = beg + Diff if beg + Diff < 360 else beg + Diff - 360
    #e = 15

    left = polar2cart((Xm,Ym), beg, Radius*2)
    right = polar2cart((Xm,Ym), e, Radius*2)
    #print((beg+e)/2)
    #al = polar2cart((Xm,Ym), (beg+e)/2, Radius*2)
    #drawl.line([al,(Xm,Ym)], fill ='red')
    WideLineAA(drawl, left, [Xm,Ym], fill=(0,0,255), width=2, back=Back)
    WideLineAA(drawl, right, [Xm,Ym], fill=(0,0,255), width=2, back=Back)


    arc_dim_aa(image, drawl, (Xm, Ym), Radius, beg, e, fill=(0,0,0),
                back = Back)

    image.show()
    #image.save('../../temp/arc_dim_'+ str(beg)+'_'+str(diff)+'.png')
