import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import angled_text, dims, polar2cart, int_up
from numpy import array, linspace, concatenate, argsort, int_, delete, all
from math import dist, atan2, sin, cos, radians

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

    size = dist(start_pos, end_pos)
    dash_gap_length = sum(dash)

    # length of longest ordinate
    length = abs(x1 - x0) if abs(x1 - x0) >= abs(y1 - y0) else abs(y1 - y0)

    if length % dash_gap_length != 0:
        factor = length//dash_gap_length
        length = factor * dash_gap_length
        if angle not in (45, 135, 225, 315):
            x1 = int_up(x0 + length * cos(theta))
            y1 = int_up(y0 + length * sin(theta))
        else:
            x1 = x0 + length * int_up(cos(theta))
            y1 = y0 + length * int_up(sin(theta))

    # sort out number of generated samples
    dash_amount = int_up(length / dash_gap_length) + 1
    all_arr = None

    while len(dash) > 0:
        start_arr = linspace((x0, y0), (x1, y1), dash_amount)
        while(dist(start_pos,start_arr[-1,:]) > size):
            start_arr = delete (start_arr, (-1), axis=0)

        dash0, *dash = dash
        dash_minus = dash0 - 1

        # make second part of the line array
        if angle not in (45, 135, 225, 315):
            x0 = x0 + int_up(dash_minus * cos(theta))
            y0 = y0 + int_up(dash_minus * sin(theta))
            x1 = x1 + int_up(dash_minus * cos(theta))
            y1 = y1 + int_up(dash_minus * sin(theta))
        else:
            x0 = x0 + dash_minus * int_up(cos(theta))
            y0 = y0 + dash_minus * int_up(sin(theta))
            x1 = x1 + dash_minus * int_up(cos(theta))
            y1 = y1 + dash_minus * int_up(sin(theta))

        end_arr = linspace((x0, y0), (x1, y1), dash_amount)
        while(dist(start_pos,end_arr[-1,:]) > size):
            end_arr = delete (end_arr, (-1), axis=0)

        if all_arr is None:
            all_arr = concatenate([start_arr, end_arr], axis=0)
        else:
            all_arr = concatenate([start_arr, end_arr, all_arr], axis=0)

        dash0, *dash = dash
        dash_plus = dash0 + 1

        if angle not in (45, 135, 225, 315):
            x0 = x0 + int_up(dash_plus * cos(theta))
            y0 = y0 + int_up(dash_plus * sin(theta))
            x1 = x1 + int_up(dash_plus * cos(theta))
            y1 = y1 + int_up(dash_plus * sin(theta))
        else:
            x0 = x0 + dash_plus * int_up(cos(theta))
            y0 = y0 + dash_plus * int_up(sin(theta))
            x1 = x1 + dash_plus * int_up(cos(theta))
            y1 = y1 + dash_plus * int_up(sin(theta))

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
    wide, height = Font.getsize('(30, 84)')

    Dash = (21,3,3,3)
    
    Dash1 = (7,1,1,1)

    w, h = 200, 200
    image = Image.new('RGB', (w,h), '#FFFFDD')
    draw = ImageDraw.Draw(image)

    for i in range(0, 360, 5):
        line_dashed(draw, (100, 100), size=65, angle=i, dash=Dash1,
                width = 1, fill=(0,int_up(i*0.7),255-int_up(i*0.7)))

    '''
    x = [50, 150, 150, 50, 50]
    y = [50, 50, 150, 150, 50]

    #x = [50, 50]
    #y = [150, 50]

    for i in range(len(x)-1):
        #print(i, 'i')
        line_dashed(image, (x[i],y[i]), end_pos= (x[i+1],y[i+1]),   dash=dash1,
                width = 1, fill=(0,i*63,255-(i*63)))


    a = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
    #a = [0,30,45,60]

    for i in range(len(a)):
        line_dashed(image, (100, 100), size=65, angle=a[i], dash=dash1,
                width = 1, fill=(0,i*15,255-(i*15)))
    '''
    image.show()
    #image.save('../figures/11angled_dashes.png')  #



