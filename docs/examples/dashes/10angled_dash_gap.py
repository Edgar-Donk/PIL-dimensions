import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import angled_text, dims, polar2cart, int_up
from numpy import array, linspace, concatenate, argsort, int_, delete
from math import dist, atan2, tan, pi, radians

def line_dashed(dr, start_pos, end_pos=None, dash=(5,5), angle=None,
                size=None, width = 1, fill='black'):
    # create dashed lines in PIL
    x0, y0 = start_pos
    if end_pos is None:
        theta = radians(angle)
        end_pos = x1, y1 = polar2cart(start_pos, theta, size)
    elif angle is None:
        x1, y1 = end_pos
        theta = atan2(y1 - y0, x1 - x0) # line slope
        size = dist(start_pos, end_pos)
    else:
        raise Exception('line_dashed: Either supply end_pos {}, or ' \
            'size {} and angle {}'.format(end_pos, size, angle))

    # check dash input
    if len(dash)%2 == 0 or len(dash) ==1:
        pass
    else:
        raise Exception('The dash tuple: {} should be one or an equal number '\
                        'of entries'.format(dash))

    if len(dash) == 1 :
        dash = dash + dash

    dash_gap_length = sum(dash)

    # is the line increasing or decreasing
    fact = -1 if abs(theta) >= pi else 1
    theta = theta if theta > 0 else 2*pi + theta # change minus values
    phi = pi/2 - theta
    fx = -1 if pi/2 < theta < 3*pi/2 else 1
    fy = 1 if 0 < theta < pi else -1

    # lengthof longest ordinate
    length = abs(x1 - x0) if abs(x1 - x0) >= abs(y1 - y0) else abs(y1 - y0)

    if length % dash_gap_length != 0:
        factor = length//dash_gap_length # + 1
        length = factor * dash_gap_length
        if abs(x1 - x0) >= abs(y1 - y0):
            x1 = x0 + fx * length
            y1 = int_up(y0 + fy * length * abs(tan(theta)))
        else:
            y1 = y0 + fy * length
            x1 = int_up(x0 + fx * length * abs(tan(phi)))

    # sort out lengths
    dash_amount = int_up(length / dash_gap_length) + 1

    all_arr = None

    while len(dash) > 0:
        start_arr = linspace((x0, y0), (x1, y1), dash_amount)
        while(dist(start_pos,start_arr[-1,:]) > size):
            start_arr = delete (start_arr, (-1), axis=0)

        dash0, *dash = dash
        dash_minus = dash0 - 1

        # make second part of the line array
        if abs(x1 - x0) >= abs(y1 - y0):
            x0 = x0 + fx * dash_minus
            y0 = y0 + fy * int_up(dash_minus * abs(tan(theta)))
            x1 = x1 + fx * dash_minus
            y1 = y1 + fy * int_up(dash_minus * abs(tan(theta)))
        else:
            x0 = x0 + fx * int_up(dash_minus * abs(tan(phi)))
            y0 = y0 + fy * dash_minus
            x1 = x1 + fx * int_up(dash_minus * abs(tan(phi)))
            y1 = y1 + fy * dash_minus

        end_arr = linspace((x0, y0), (x1, y1), dash_amount)
        while(dist(start_pos,end_arr[-1,:]) > size):
            end_arr = delete (end_arr, (-1), axis=0)

        if all_arr is None:
            all_arr = concatenate([start_arr, end_arr], axis=0)
        else:
            all_arr = concatenate([start_arr, end_arr, all_arr], axis=0)

        dash0, *dash = dash
        dash_plus = dash0 + 1

        if abs(x1 - x0) >= abs(y1 - y0):
            x0 = x0 + fx * dash_plus
            y0 = y0 + fy * int_up(dash_plus * abs(tan(theta)))
            x1 = x1 + fx * dash_plus
            y1 = y1 + fy * int_up(dash_plus * abs(tan(theta)))
        else:
            x0 = x0 + fx * int_up(dash_plus * abs(tan(phi)))
            y0 = y0 + fy * dash_plus
            x1 = x1 + fx * int_up(dash_plus * abs(tan(phi)))
            y1 = y1 + fy * dash_plus

    # sort along the column, where the maximum change occurs
    if abs(x1 -x0) > abs(y1 -y0):
        fin_arr = int_(all_arr[all_arr[:, 0].argsort()])
    else:
        fin_arr = int_(all_arr[all_arr[:, 1].argsort()])
    fin_arr = fin_arr[::-1] if (fin_arr[-1,:] == start_pos).all() else fin_arr

    nr_lines = len(fin_arr) //2 * 2

    [dr.line([tuple(fin_arr[n]), tuple(fin_arr[n+1])], width=width, fill=fill)
            for n in range(0, nr_lines, 2)]

if __name__ == "__main__":
    Font = ImageFont.truetype('consola.ttf', 12)
    # wide, height = Font.getsize('(30, 84)')
    unused1, unused2, wide, height = Font.getbbox('(30, 84)')

    Dash = (21,3,3,3)
    Dash1 = (7,1,1,1)
    Dash2 = (5, 5)

    Start_pos = (50, 50) # (30, 10) (10, 10)
    End_pos = (26, 26) # (75, 75)  (30, 90)
    x0, y0 = (80, 90)
    x1, y1 = (15, 25)

    w, h = 200, 200
    image = Image.new('RGB', (w,h), '#FFFFDD')
    draw = ImageDraw.Draw(image)

    for i in range(0, 360, 5):
        line_dashed(draw, (100, 100), size=65, angle=i, dash=Dash1,
                width = 1, fill=(255-int_up(i*0.7),int_up(i*0.7),0)) #

    '''
    a = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
    #a = [0, 45, 90, 135, 180, 225, 270, 315]
    #a = [30, 45]

    for i in range(len(a)):
        line_dashed(image, (100, 100), angle=a[i], size = 65, dash=Dash1,
                width = 1, fill=(255-15*i,15*i,0))

    x = [74, 74, 50, 26, 26, 26, 50, 74]
    y = [50, 74, 74, 74, 50, 26, 26, 26]
    for i in range(len(x)):
        line_dashed(image, Start_pos, (x[i], y[i]), dash=Dash2, width = 1, fill='black')
    '''

    #drawa = ImageDraw.Draw(image)
    '''
    draw.line([(80, 80), (74, 74)], fill='red')
    draw.line([(72, 72), (72, 72)], fill='red')
    draw.line([(70, 70), (64, 64)], fill='red')
    '''
    image.show()
    #image.save('../figures/10angled_dashes.png')  #



