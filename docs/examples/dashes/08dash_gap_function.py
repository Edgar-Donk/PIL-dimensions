import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from math import dist, atan2, sin, cos
from numpy import array, linspace, concatenate, argsort, int_
from DimLinesPIL import angled_text, dims, int_up

def line_dashed(dr, start_pos, end_pos, dash=(5,5), width = 1, fill='black'):
    # create dashed lines in PIL

    # unpack tuples
    x0, y0 = start_pos
    x1, y1 = end_pos

    if len(dash) == 1 :
        dash = dash + dash

    theta = atan2(y1 - y0, x1 - x0)

    # sort out lengths
    dash_gap_length = sum(dash)
    line_length = dist(start_pos, end_pos)

    all_arr = None

    # adjust length to suit start and end positions if required
    if line_length % dash_gap_length != 0:
        factor = line_length//dash_gap_length
        line_length = factor * dash_gap_length
        x1 = int_up(x0 + line_length * cos(theta))
        y1 = int_up(y0 + line_length * sin(theta))

    # inclusive number of dashes and gaps
    dash_amount = int_up(line_length / dash_gap_length) + 1

    while len(dash) > 0:
        start_arr = linspace((x0, y0), (x1, y1), dash_amount)

        dash0, *dash = dash
        dash_minus = dash0 - 1

        # make second part of the line array
        x0 = x0 + int_up(dash_minus * cos(theta))
        y0 = y0 + int_up(dash_minus * sin(theta))
        x1 = x1 + int_up(dash_minus * cos(theta))
        y1 = y1 + int_up(dash_minus * sin(theta))

        end_arr = linspace((x0, y0), (x1, y1), dash_amount)

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

    nr_lines = len(fin_arr)

    [dr.line([tuple(fin_arr[n]), tuple(fin_arr[n+1])], width=width, fill=fill)
            for n in range(0, nr_lines, 2)]

if __name__ == "__main__":
    Font = ImageFont.truetype('consola.ttf', 12)

    arr=array([[10, 30],
 [16, 30],
 [18, 30],
 [18, 30],
 [20, 30],
 [26, 30],
 [28, 30],
 [28, 30],
 [30, 30],
 [36, 30],
 [38, 30],
 [38, 30],
 [40, 30],
 [46, 30],
 [48, 30],
 [48, 30],
 [50, 30],
 [56, 30],
 [58, 30],
 [58, 30],
 [60, 30],
 [66, 30],
 [68, 30],
 [68, 30],
 [70, 30],
 [76, 30],
 [78, 30],
 [78, 30],
 [80, 30],
 [86, 30],
 [88, 30],
 [88, 30],
 [90, 30],
 [96, 30],
 [98, 30],
 [98, 30]])

    Dash = (7,1,1,1)

    Start_pos = (10,30) # (30, 10)
    End_pos = (90, 30) # (30, 90)
    #x0, y0 = (30, 10)
    #x1, y1 = (30, 90)

    w, h = 100, 100
    image = Image.new('RGB', (w,h), '#FFFFDD')
    draw = ImageDraw.Draw(image)

    #wide, height = Font.getsize('(30, 84)')
    unused1, unused2, wide, height = Font.getbbox('(30, 84)')

    line_dashed(draw, Start_pos, End_pos, dash=Dash, width = 1, fill='black')
    #line_dashed(image, (x0, y0), (x1, y1), dash=dash, width = 1, fill='black')

    image.show()
