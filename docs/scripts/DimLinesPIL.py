"""Dimension Toolbox for PIL

Dimensions with associated extenders and leaders
dimension.py line with arrows used as base for other dimensions

"""

from PIL import Image, ImageDraw, ImageFont
from math import sin, cos, radians, sqrt, atan2, pi, dist, degrees
from numpy import linspace, concatenate, argsort, array, delete, int_

# Use this to make arrowhead on the end of lines
# tuple (d1, d2, d3) specifies shape, default (8, 10, 3)
# d1 specifies length along the line
# d2 is the äong side
# d3 is the vertical height

# make linear dimension with option for arrows both ends or one end only
# arrow='first', arrow='last', arrow='both'

# dimension normal dimensioning, used as base for other dimensions
# dim_arc dimension over an angle

# slanted text centred to middle of text

def int_up(x):
    """Decimal part of number rounded up if greater than .5 if positive otherwise
    rounded down.

    Parameters
    ----------
    x : float

    Returns
    -------
    int
    """

    return int(x + 0.5) if x >= 0 else int(x - 0.5)

def bres(dr, ptA, ptB, fill='black'):
    """Use integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.
    The result contains both the start and the end point.

    Parameters
    ----------
    dr : str
        PIL drawing handle
    ptA : int
        coordinate tuple at line start
    ptB : int
        coordinate tuple at line finish
    fill : str or int
        line colour name, hash or tuple
    """
    x0,y0 = ptA
    x1,y1 = ptB
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1 # negate step direction for -ve gradients
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy: # gentle slope
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:       # steep slope
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = (dy<<1) - dx # D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        #yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        dr.point([x0 + x*xx + y*yx, y0 + x*xy + y*yy], fill=fill)
        if D >= 0:
            y += 1
            D -= dx<<1 # 2*dx
        D += dy<<1 # 2*dy

def dimension(dr, ptA, ptB=None, angle=None, width=1, fill=(0,0,0),
                arrowhead=(8, 10, 3), arrow='last'):
    """Creates a line with an arrow at one or both ends, basis for other scripts.

    Enter two coordinates for line, or one coordinate and angle for just an
    arrow.

    Arrowhead tuple gives size and shape of arrow.

    Arrow gives relative position arrow on line.

    Parameters
    ----------
    dr : str
        PIL drawing handle
    ptA : int
        coordinate tuple at line start
    ptB : int, optional
        coordinate tuple at line end
    angle : float, optional
        line angle  (degrees)
    width : int
        line width
    fill : int
        line colour tuple
    arrowhead : int
        tuple arrow size and shape
    arrow : str
        arrow position 'first', 'last' or 'both'

    Returns
    -------
    draws line with one or two arrows either end or just an arrow
    """

    if len(arrowhead) == 3:
        d1, d2, d3 = arrowhead
    else:
        raise Exception('dimension: arrowhead {} needs a 3 entry tuple' \
                .format(arrowhead))

    if arrow not in ('first', 'last', 'both'):
        raise Exception('dimension: arrow {} can only be the strings "first", \
            "last", "both"'.format(arrow))

    # extract dims from tuples
    x0, y0 = ptA
    if angle is None and ptB:
        x1, y1 = ptB
        phi = atan2(y1-y0, x1-x0)
        dr.line((ptA,ptB), width=width, fill=fill)
    elif ptB is None and isinstance(angle, int):
        x1,y1 = ptA
        phi = radians(angle)
    else:
        raise Exception('dimension: Either supply ptB {} or angle {} not both' \
                .format(ptB, angle))

    # perpendicular distance shaft to arrow tip
    el = int(sqrt(d2 * d2 - d3 * d3) + 0.5)

    if arrow in ('first', 'both'):
        cx0 = x0 + d1 * cos(phi)
        cy0 = y0 + d1 * sin(phi)
        ex0 = x0 + el * cos(phi)
        ey0 = y0 + el * sin(phi)
        fx0 = ex0 + d3 * sin(phi)
        fy0 = ey0 - d3 * cos(phi)
        gx0 = ex0 - d3 * sin(phi)
        gy0 = ey0 + d3 * cos(phi)
        dr.polygon([(x0, y0), (fx0, fy0), (cx0, cy0),
                    (gx0, gy0)], fill=fill)

    if arrow in ('last', 'both'):
        cx0 = x1 - d1 * cos(phi)
        cy0 = y1 - d1 * sin(phi)
        ex0 = x1 - el * cos(phi)
        ey0 = y1 - el * sin(phi)
        fx0 = ex0 + d3 * sin(phi)
        fy0 = ey0 - d3 * cos(phi)
        gx0 = ex0 - d3 * sin(phi)
        gy0 = ey0 + d3 * cos(phi)
        dr.polygon([(x1, y1), (fx0, fy0), (cx0, cy0),
                    (gx0, gy0)], fill=fill)

def angled_text(im, at, text, angle, font, fill='black', aall=1):
    """Text drawn at an angle, text position in centre of text.

    Parameters
    ----------
    im : str
        PIL image handle
    at : int
        coordinate tuple, text position
    text : str
        text input
    angle : float
        text angle (degrees)
    font : str
        font to be used
    fill : int
        text colour tuple
    aall : int
        unconstrained or angle constrained, default 1 unconstrained

    Returns
    -------
    im : str
        PIL image handle
    """
    print('font', font)
    #width, height = font.getsize(text)
    unused1, unused2, width, height = font.getbbox(text)

    image1 = Image.new('RGBA', (width, height), (255,255,255, 0))
    draw1 = ImageDraw.Draw(image1)
    draw1.text((0, 0), text=text, font=font, fill=fill)

    # ensure angles within 0 to 360
    angle = 360 + angle if angle < 0 else angle
    angle = angle if angle < 360 else angle - 360

    if aall == 0:
        if 90 <= angle < 180:
            angle = angle + 180
        if 180 <= angle < 270:
            angle = angle - 180

    px, py = at

    image1 = image1.rotate(angle, expand=1, resample=Image.BICUBIC)

    sx, sy = image1.size

    if 0 <= angle <= 90:
        im.paste(image1, (px-sx//2, py-sy//2, px + sx-sx//2, py + sy-sy//2), image1)
    elif 90 < angle <= 180:
        im.paste(image1, (px-sx//2, py - sy+sy//2, px + sx-sx//2, py+sy//2 ), image1)
    elif 180 < angle <= 270:
        im.paste(image1, (px-sx+sx//2, py-sy+sy//2, px+sx//2, py+sy//2 ), image1)
    elif 270 < angle < 360:
        im.paste(image1, (px-sx//2, py-sy//2, px + sx-sx//2, py + sy-sy//2), image1)

def create_arc(dr, c, r, start, end, fill='black'):
    """Returns arc using centre and radius

    Parameters
    ----------
    dr : str
        PIL draw handle
    c : int
        centre coordinate tuple
    r : int
        radius of enclosing circle
    start : int
        starting angle degrees
    end : int
        finishing angle degrees
    fill : int
        colour tuple of filled arc
    outline = int
        colour tuple of arc outline

    Returns
    -------
    arc drawing
    """

    return dr.arc([c[0]-r,c[1]-r,c[0]+r,c[1]+r], start, end, fill=fill)

def polar2cart(centre, phi, ray, units='degrees'):
    """Convert polar to cartesian coordinates

    Parameters
    ----------
    centre : int
        coordinate tuple
    phi : float
        angle of ray (degrees or radians)
    ray : int
        distance from centre
    units : str
        angle units in 'degrees' or 'radians'

    Returns
    -------
    x, y : int
        coordinate tuple
    """
    if units == 'degrees':
        phi = phi if phi >= 0 else phi + 360
        phi = phi if phi < 360 else phi - 360
        phi = radians(phi)
    elif units == 'radians':
        phi = phi if phi >= 0 else phi + 2 * pi
        phi = phi if phi < 2 * pi else phi - 2 * pi
    else:
        raise Exception('polar2cart: units {} can only be "degrees" or "radians"'\
            .format(units))

    dx = abs(ray) * cos(phi)
    dy = abs(ray) * sin(phi)
    x = centre[0] + dx
    y = centre[1] + dy

    return int_up(x), int_up(y)

def cart2polar(centre, outer):
    """Convert cartesian coordinates to polar

    Parameters
    ----------
    centre : int
        coordinates for central point
    outer : int
        coordinates for outer point

    Returns
    -------
    polar tuple degrees and ray (length)

    """
    dx = outer[0] - centre[0]
    dy = outer[1] - centre[1]

    deg = int_up(degrees(atan2(dy, dx)))
    if deg < 0: deg = 360 + deg
    ray = int_up(sqrt(dx*dx + dy*dy))
    deg = min(max(deg, 0), 360)

    return deg, ray

def arc_dim(im, dr, centre, radius, begin, end, fill=(0,0,0),
            text=None, font=None, arrowhead=(8,10,3)):
    """Draw arc dimension based on centre and radius

    Parameters
    ----------
    dr : str
        PIL image handle
    dr : str
        PIL drawing handle
    centre : int
        coordinate tuple
    radius : int
        radius of arc
    begin : int
        starting angle degrees
    end : int
        finishing angle degrees
    fill : int
        colour tuple
    text : str
        arc text
    font : str
        text font
    arrowhead : int
        tuple arrow size and shape

    Returns
    -------
    arc dimension
    """

    create_arc(dr, centre, radius, begin, end, fill=fill)

    beginr = radians(begin)
    endr = radians(end)
    if 180 <= begin <= 360 and 0 <= end <= 180:
        alpha = (360 - begin + end)/2
        diff = 360 + end -begin
    else:
        alpha = (begin + end) / 2
        diff = end - begin

    if diff == 180:
        raise Exception('angle dimension: angle is 180°, begin {} end {}' \
            ' difference {} cannot draw dimension'.format(begin, end, diff))

    if diff != 90:
        x, y = centre
        create_arc(dr,centre,radius, begin, end, fill=fill)

        # find begin and end arc
        start = x + radius * cos(beginr), y + radius * sin(beginr)
        finish = x + radius * cos(endr), y + radius * sin(endr)

        # placement of arrows, 'first' point inwards
        order = 'last' if radians(diff) * radius > 4 * arrowhead[1] else 'first'

        dimension(dr, start, angle=(begin - 90), arrow=order)
        dimension(dr, finish, angle=(end + 90), arrow=order)

    else:
        ax, ay = polar2cart(centre, begin, radius)
        bx, by = polar2cart(centre, end, radius)
        dx, dy = polar2cart(centre, alpha, radius*sqrt(2))

        dr.line([(ax,ay), (dx,dy)], fill=fill)
        dr.line([(bx,by), (dx,dy)], fill=fill)

    # placement of text
    if text is None:
        text = str(diff) + '°'
    if font is None:
        font_size=15
        font = ImageFont.truetype('consola.ttf', font_size)
    (wide, ht) = font.getsize(text)

    if 180 <= begin <= 360 and 0 <= end <= 180:
        alpha = begin + alpha -360

    angle = alpha - 90
    da = 7

    if diff == 90:
        X, Y = polar2cart(centre, alpha, radius * sqrt(2) + da)
    else:
        t = tan(radians(diff/2))
        a = wide/ 2 / t
        size = max(radius, a)
        X, Y = polar2cart(centre, alpha, size + ht/2+da)

    angled_text(im, (X, Y), text, angle, font=font, fill=fill, aall=0)

def DashedLine(dr, start_pos, end_pos=None, dash=(5,5), angle=None,
                size=None, width = 1, fill=(0,0,0)):
    """Create dashed lines in PIL.

    Parameters
    ----------
    dr : str
        PIL drawing handle
    start_pos : int
        starting coordinate tuple
    end_pos : int
        finishing coordinate tuple, optional
    dash : int
        tuple of line pattern
    angle : int
        slope of line degrees, optional
    size : int
        line size
    width : int
        line width
    fill : int
        colour tuple

    Returns
    -------
    dashed line
    """

    x0, y0 = start_pos
    if end_pos is None:
        theta = radians(angle)
        end_pos = x1, y1 = polar2cart(start_pos, theta, size)
    elif angle is None:
        x1, y1 = end_pos
        theta = atan2(y1 - y0, x1 - x0) # line slope
        size = dist(start_pos, end_pos)
    else:
        raise Exception('DashedLine: Either supply end_pos {}, or ' \
            'size {} and angle {}'.format(end_pos, size, angle))

    # check dash input
    if len(dash)%2 != 0 and len(dash) !=1:
        raise Exception('The dash tuple: {} should be one or an equal number '\
                        'of entries'.format(dash))

    if len(dash) == 1 :
        dash = dash + dash

    dash_gap_length = sum(dash)

    # is the line increasing or decreasing
    fact = -1 if sum(start_pos) > sum(end_pos) else 1

    # length of longest ordinate
    if abs(x1 - x0) >= abs(y1 - y0):
        length = abs(x1 - x0)
    else:
        length = abs(y1 - y0)
    if length % dash_gap_length != 0:
        factor = length//dash_gap_length
        length = factor * dash_gap_length
        x1 = int_up(x0 + length * cos(theta))
        y1 = int_up(y0 + length * sin(theta))

    # sort out lengths
    dash_amount = int(length / dash_gap_length + 0.5) + 1

    all_arr = None

    while len(dash) > 0:
        start_arr = linspace((x0, y0), (x1, y1), dash_amount)
        while(dist(start_pos,start_arr[-1,:]) > size):
            start_arr = delete (start_arr, (-1), axis=0)

        dash0, *dash = dash
        dash_minus = dash0 - 1

        # make second part of the line array
        x0 = x0 + int_up(dash_minus * cos(theta))
        y0 = y0 + int_up(dash_minus * sin(theta))
        x1 = x1 + int_up(dash_minus * cos(theta))
        y1 = y1 + int_up(dash_minus * sin(theta))

        end_arr = linspace((x0, y0), (x1, y1), dash_amount)
        while(dist(start_pos,end_arr[-1,:]) > size):
            end_arr = delete (end_arr, (-1), axis=0)

        if all_arr is None:
            all_arr = concatenate([start_arr, end_arr], axis=0)
        else:
            all_arr = concatenate([start_arr, end_arr, all_arr], axis=0)

        dash0, *dash = dash
        dash_plus = dash0 + 1

        x0 = x0 + int_up(dash_plus * cos(theta))
        y0 = y0 + int_up(dash_plus * sin(theta))
        x1 = x1 + int_up(dash_plus * cos(theta))
        y1 = y1 + int_up(dash_plus * sin(theta))

    # sort along the column, where the maximum change occurs
    if abs(x1 -x0) > abs(y1 -y0):
        fin_arr = int_(all_arr[all_arr[:, 0].argsort()])
    else:
        fin_arr = int_(all_arr[all_arr[:, 1].argsort()])
    fin_arr = fin_arr[::-1] if fact == -1 else fin_arr

    nr_lines = len(fin_arr) //2 * 2


    [dr.line([tuple(fin_arr[n]), tuple(fin_arr[n+1])], width=1, fill=fill)
            for n in range(0, nr_lines, 2)]

def thickness_dim(im, dr, ptA, thick, angle=0, text=None, font=None, width=1, fill='black',
              arrowhead=(8, 10, 3), arrow='last'):
    """Horizontal or vertical dimension to show thickness of object.

    It will be drawn with two inwardly pointing arrows, and text placed outside
    of the object.

    Parameters
    ----------
    im : str
        PIL image handle
    dr : str
        PIL drawing handle
    ptA : int
        starting coordinate tuple
    thick : int
        thickness of object in pixels
    angle : int
        angle of dimension, in degrees
    text : str
        dimension text
    font : str
        text font
    width : int
        line width
    fill : int
        colour tuple
    arrowhead : int
        tuple arrow size and shape
    arrow : str
        arrow position 'first' or 'last' the default

    Returns
    -------
    thickness dimension
    """

    phir = radians(angle)
    ptB = int(ptA[0] + thick * cos(phir) + 0.5), \
          int(ptA[1] + thick * sin(phir) + 0.5)
    d1,d2,d3 = arrowhead

    dr.line([ptA, ptB], width=width, fill=fill)

    dimension(dr, ptA, angle=angle, arrow='last')
    dimension(dr, ptB, angle=angle, arrow='first')

    # thickness of item
    phir = radians(angle)
    (wide, height) = font.getsize(text)
    w = wide // 2
    h = height // 2
    dx = - (h + d2 + 5) * cos(phir)
    dy = - (h + d2 + 5) * sin(phir)

    # stop upside down text
    if 0 <= angle <= 180:
        angle = 90-angle
    elif 180 < angle < 360:
        angle = 270-angle

    at = (ptA[0] + int(dx), ptA[1] + int(dy))
    angled_text(im, at, text=text, angle=angle, font=font)

def dims(im, dr, ptA, ptB, extA, extB=None, text=None, font=None, textorient=None,
        fill=(0,0,0), tail=True, arrowhead=(8, 10, 3), arrow='both'):
    """Dimension vertical and horizontal tailed lines with extender lines,
    option to use arrows.

    Extenders can be integer or tuple of line and gap size

    Extenders can be unequal length, if extB excluded same size.

    Extenders positive right when vertical, above when horizontal

    Parameters
    ----------
    im : str
        PIL image handle
    dr : str
        PIL drawing handle
    ptA : int
        starting coordinate tuple
    ptB : int
        ending coordinate tuple
    extA : int
        integer size of extender at starting point or tuple of line and gap
    extB : int
        size of extender at finishing point, optional
    text : str
        dimension text
    font : str
        text font
    textorient : str
        'vertical' or 'horizontal', optional
    fill : int
        colour tuple
    tail : bool
        'True' default show tails on dimension line, 'False' use arrows
    arrowhead : int
        tuple arrow size and shape
    arrow : str
        arrow position 'first', 'last' or 'both' default

    Returns
    -------
    outside dimension
    """

    if isinstance(extA, int) or len(extA) == 1:
        exta = extA if isinstance(extA, int) else extA[0]
    elif len(extA) == 2:
        exta = extA[0]
        if extA[0] * extA[1] < 0:
            raise Exception('extA: both entries of extension tuple extA {} ' \
                'should either be positive or negative'.format(extA))
    else:
        raise Exception('extA: The extension tuple extA {} should be one or ' \
                'two entries'.format(extA))
    if extB is None:
        extB = extA
        extb = exta
    elif isinstance(extB, int) or len(extB) == 1:
        extb = extB if isinstance(extB, int) else extB[0]
    elif len(extB) == 2:
        extb = extB[0]
        if extB[0] * extB[1] < 0:
            raise Exception('extB: The extension tuple extB {} should be one or ' \
                'two entries, if None then it will equal extA {}'.format(extB, extA))
    if textorient is not None and textorient not in  ('vertical', 'horizontal', 'h', 'v'):
        raise Exception('dims: textorient {} should be None or' \
                '"horizontal", "h", "vertical" or "v"'.format(textorient))

    font = ImageFont.load_default() if font is None else font
    (wide, height)= font.getsize(text)

    h = height // 2
    w = wide // 2

    dx = dy = 0
    if ptA[0] == ptB[0]:
        # vertical dimension
        ang = 270 if exta > 0 else 90
        if textorient is None or textorient in ('vertical', 'v'):
            dx = -h -5 if exta > 0 else h+5 # text positioning
            phi = 90                        # text angle
        elif textorient in ('horizontal', 'h'):
            dx = -w - 5 if exta > 0 else w + 5
            phi = 0                         # text angle

    elif ptA[1] == ptB[1]:
        # horizontal dimension
        ang = 0 if exta > 0 else 180
        if textorient is None or textorient in ('horizontal', 'h'):
            dy = -h -5 if exta > 0 else +h +5
            phi = 0                        # text angle
        elif textorient in ('vertical', 'v'):
            dy = -w -5 if exta > 0 else +w +5 # text positioning
            phi = 90

    else:
        raise Exception('dims: should be vertical or horizontal '\
                        '{} {} coordinates'.format(ptA, ptB))

    # extensions
    ptA3 = polar2cart(ptA, ang-90, 3)
    ptAe = polar2cart(ptA, ang+90, abs(exta))
    dr.line([ptA3, ptAe], width=1, fill=fill)
    ptB3 = polar2cart(ptB, ang-90, 3)
    ptBe = polar2cart(ptB, ang+90, abs(extb))
    dr.line([ptB3, ptBe], width=1, fill=fill)

    # dimension line and tails or arrows
    if tail:
        dr.line([ptA, ptB], width=1, fill=fill)
        # create 45° end stubs
        p2 = ptA[0]+3, ptA[1]+3
        p3 = ptA[0]-3, ptA[1]-3
        p4 = ptB[0]+3, ptB[1]+3
        p5 = ptB[0]-3, ptB[1]-3
        dr.line([p2,p3], width=1, fill=fill)
        dr.line([p4,p5], width=1, fill=fill)
    else:
        dimension(dr, ptA, ptB=ptB, width=1, fill=fill, arrowhead=arrowhead,
                arrow=arrow)

    at = (ptA[0]+ptB[0])//2+dx,(ptA[1]+ptB[1])//2+dy

    angled_text(im, at, text=text, angle=phi, font=font, fill=fill, aall=0)

def inner_dim(im, dr, ptA, ptB, text=None, font=None, width=1, fill='black',
              arrowhead=(8, 10, 3), arrow='both'):
    """Used on horizontal or vertical inner dimensions.

    Parameters
    ----------
    im : str
        PIL image handle
    dr : str
        PIL drawing handle
    ptA : int
        tuple starting coordinates
    ptB : int
        tuple finishing coordinates, optional
    text : str
        text
    font : str
        text font
    width : int
        line width
    fill : int
        colour tuple
    arrowhead : int
        tuple size and shape arrow
    arrow : str
        position arrow, 'first', 'last' or 'both'

    Returns
    -------
    inner dimension
    """

    dimension(dr, ptA, ptB, width=width, fill=fill, arrowhead=arrowhead,
              arrow='both')
    # vertical
    if ptA[0] == ptB[0]:
        at = ptA[0] - 10, (ptA[1] + ptB[1]) //2
        angle = 90

    # horizontal
    elif ptA[1] == ptB[1]:
        at = (ptA[0] + ptB[0]) // 2, ptA[1] - 10
        angle = 0
    else:
        raise Exception('The inner dimension: should be vertical or horizontal '\
                        '{} {} coordinates'.format(ptA, ptB))

    angled_text(im, at, text, angle, font=font, fill='black')

def slant_dim(im, dr, ptA, ptB =None, extA=None,  angle=None, size=None,
              fill='black', text=None, font=None):
    """Used on slanting dimensions, with 45" tails.

    Extenders can be integer or tuple of line and gap size

    Extenders positive left when vertical, above when horizontal

    Parameters
    ----------
    im : str
        PIL image handle
    dr : str
        PIL drawing handle
    ptA : int
        tuple starting coordinates
    ptB : int
        tuple finishing coordinates, optional
    extA : int
        integer or tuple of extender length, second entry space
    extB : int
        integer or tuple of extender length, second entry space, optional
    angle : int
        slope line, optional
    size : int
        length dimension, optional
    text : str
        text
    font : str
        text font
    width : int
        line width
    fill : int
        colour tuple

    Returns
    -------
    slanting dimension
    """

    if isinstance(extA, int) or len(extA) == 1:
        extO = extA if isinstance(extA, int) else extA[0]
    elif len(extA) == 2:
            extO = sum(extA)
    else:
        raise Exception('slant_dim: The extender tuple extA {} should be one or ' \
                'two entries'.format(extA))

    if ptB is None and size and 0 <= angle <360:
        phir = radians(angle)
        ptC = polar2cart(ptA, angle-90, extO)
        ptD = polar2cart(ptC, angle, size)
    elif size is None and ptB:
        phir = atan2(ptB[1]-ptA[1], ptB[0]-ptA[0])
        angle = int_up(degrees(phir))
        ptC = polar2cart(ptA, angle-90, extO)
        ptD = ptC[0] + (ptB[0] - ptA[0]), ptC[1] + (ptB[1] - ptA[1])
    else:
        raise Exception('slant_dim: Either supply ptB {}, or size {} and ' \
                'angle {}'.format(ptB, size, angle))

    dirn = radians(45 + angle)

    # dimension line
    dr.line([ptC, ptD], width=1, fill=fill)

    # extenders
    extO = extO if isinstance(extA, int) or len(extA) == 1 else extA[0]
    ptC3 = polar2cart(ptC, angle-90, 3)
    ptCe = polar2cart(ptC, angle+90, extO-1)
    dr.line([ptC3, ptCe], width=1, fill='black')
    ptD3 = polar2cart(ptD, angle-90, 3)
    ptDe = polar2cart(ptD, angle+90, extO-1)
    dr.line([ptD3, ptDe], width=1, fill='black')

    # create 45° end stubs
    p3=ptC[0]+4*cos(dirn),ptC[1]+4*sin(dirn)
    p4=ptC[0]-4*cos(dirn),ptC[1]-4*sin(dirn)
    p5=ptD[0]+4*cos(dirn),ptD[1]+4*sin(dirn)
    p6=ptD[0]-4*cos(dirn),ptD[1]-4*sin(dirn)

    dr.line([p3,p4], width=1, fill=fill)
    dr.line([p5,p6], width=1, fill=fill)

    font = ImageFont.load_default() if font is None else font
    (wide, height) = font.getsize(text)
    h = height // 2

    angle = 360 + angle if angle < 0 else angle
    angle = angle - 360 if angle >= 360 else angle
    # stop upside down text
    if 0 <= angle <= 90:
        angle = 360-angle
    elif 90 < angle <= 180:
        angle = 180-angle
    elif 180 < angle <= 270:
        angle = 180-angle
    elif 270 < angle < 360:
        angle = -angle

    mid = (ptC[0] + ptD[0])/2, (ptC[1] + ptD[1])/2
    at =  mid[0] + (h + 7) * sin(phir), mid[1] - (h + 7) * cos(phir)
    at = int_up(at[0]), int_up(at[1])

    angled_text(im, at, text, angle, font)

def dim_level(im, dr, at, diam, ldr=20, dash=(10,4), text=None, fill='black', tri=8):
    """Level dimension, dashed diameter, leader from surface to wall

    at on left tank wall, diam internal tank diameter,

    triangle on top of level (8,8,8) p0 tip triangle, p1, p2 angles, p2 on at-p4
    p3 opposite side to at, both drawn to inside tank wall

    leader (ldr) at 60° up to p4 then horizontal to p5

    Parameters
    ----------
    im : str
        PIL image handle
    dr : str
        PIL drawing handle
    at : int
        coordinate tuple left hand tank wall
    diam : int
        internal tank diameter
    ldr : int
        leader length from surface
    dash : int
        dash pattern
    text : str
        level text
    fill : int
        colour tuple
    tri : int
        size equilateral triangle at surface

    Returns
    -------
    im : str
        PIL image handle
    """

    # check dash input
    if len(dash)%2 !=0 and len(dash) !=1:
        raise Exception('The dash tuple: {} should be one or an equal number '\
                        'of entries'.format(dash))

    font = ImageFont.truetype('consola.ttf', 12)
    wide, height = font.getsize(text)

    angle = 0

    p3 = (at[0] + diam, at[1])
    p0 = (at[0] + diam * 0.4, at[1])
    p4 = (p0[0] + ldr * 0.5, p0[1] - int_up(ldr * sin(pi/3)))
    p5 = (at[0] + diam, p4[1])
    p2 = (p0[0] + tri * 0.5, p0[1] - int_up(tri * sin(pi/3)))
    p1 = (p2[0] - tri, p2[1])

    ldr_w = p5[0] - p4[0]
    if ldr_w < wide:
        raise Exception('The leader width is too small: {} should be larger '\
                        'than the text width {}'.format(ldr_w, wide))

    DashedLine(dr, at, end_pos=p3, dash=dash, width = 1, fill='black')
    dr.polygon([p0, p1, p2], outline='black')
    DashedLine(dr, p2, end_pos=p4, dash=dash, width = 1, fill='black')
    DashedLine(dr, p4, end_pos=p5, dash=dash, width = 1, fill='black')

    p6 = (int((p4[0] + p5[0])//2), p4[1] - height - 5)

    angled_text(im, p6, text, angle, font, fill='black')

def leader(im, dr, at, angle=315, extA=20, extB=20, width=1, arrowhead=(3,5,1),
            arrow='first', fill='black', text=None, font=None):
    """Leader to object

    angle and length (extA) first part

    horizontal length for second part (extB)

    Parameters
    ----------
    im : str
        PIL image handle
    dr : str
        PIL drawing handle
    at : int
        coordinate tuple start of leader
    angle : int
        slope of first part, angle changes the leader
    extA : int
        length line in first part
    extB : int
        length line in second part
    width : int
        line width
    arrowhead : int
        tuple size and shape arrow
    arrow : str
        position arrow, normally 'first'
    fill : int
        tuple to show colour
    text : str
        descriptive text
    font : str
        text font

    Returns
    -------
    leader
    """

    font = font if font else ImageFont.load_default()
    (wide, height) = font.getsize(text)

    h = height // 2

    if wide > extB:
        print('extB was increased from:',extB,'to accommodate the text',wide+10)
        extB = wide + 10

    # dimension line
    phi = 180 if 90 < angle < 270 else 0
    ptB = polar2cart(at, angle, extA)
    ptC = polar2cart(ptB, phi, extB)
    dimension(dr, at, ptB, width=width, fill=fill, arrowhead=arrowhead,
              arrow=arrow)
    dr.line([ptB, ptC], width=width, fill=fill)

    # text position
    tp = ((ptB[0] + ptC[0])//2, ptB[1] - h - 5)

    angled_text(im, tp, text, 0, font=font)

if __name__ == "__main__":
    # Create an empty white image
    w, h = 640, 480 # 250, 250
    im = Image.new('RGBA', (w,h), (255,255,255))
    drawl = ImageDraw.Draw(im)

    c=(100,100)
    r=25
    start=30
    end=70
    text = '30°'
    font_size=15
    font = ImageFont.truetype('consola.ttf', font_size)

    arc_dim(drawl, c, r, start, end, text=text, font=font)

    '''
    ptA = (110,110)
    ptB = (430,430)
    im = dimension(im, ptA, ptB, arrow='both', arrowhead=(80, 100, 30))
    ptA = (50,400)
    ptB = (400,50)
    im = dimension(im, ptA, ptB, arrow='both', arrowhead=(80, 100, 30))
    '''
    im.show()  #('result6.png')

