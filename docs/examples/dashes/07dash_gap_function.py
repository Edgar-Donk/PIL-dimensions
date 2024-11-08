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
    dash0, dash1 = dash
    dash2 = dash0 - 1
    theta = atan2(y1 - y0, x1 - x0)

    # sort out lengths
    dash_gap_length = sum(dash)
    line_length = dist(start_pos, end_pos)

    # adjust length to suit start and end positions if required
    if line_length % dash_gap_length != 0:
        factor = line_length//dash_gap_length # + 1
        line_length = factor * dash_gap_length
        x1 = int_up(x0 + line_length * cos(theta))
        y1 = int_up(y0 + line_length * sin(theta))

    # inclusive number of dashes and gaps
    dash_amount = int_up(line_length / dash_gap_length) + 1

    start_arr = linspace((x0, y0), (x1, y1), dash_amount)

    # make second part of the line array
    x2 = x0 + int_up(dash2 * cos(theta))
    y2 = y0 + int_up(dash2 * sin(theta))
    x3 = x1 + int_up(dash2 * cos(theta))
    y3 = y1 + int_up(dash2 * sin(theta))

    end_arr = linspace((x2, y2), (x3, y3), dash_amount)

    both_arr = concatenate([start_arr, end_arr], axis=0)

    # sort along the column, where the maximum change occurs
    if abs(x1 -x0) > abs(y1 -y0):
        fin_arr = int_(both_arr[both_arr[:, 0].argsort()])
    else:
        fin_arr = int_(both_arr[both_arr[:, 1].argsort()])

    nr_lines = len(fin_arr)

    [dr.line([tuple(fin_arr[n]), tuple(fin_arr[n+1])], width=width, fill=fill)
            for n in range(0, nr_lines, 2)]

if __name__ == "__main__":
    Font = ImageFont.truetype('consola.ttf', 12)

    arr = array([[30, 10],
    [30, 24],
    [30, 40],
    [30, 54],
    [30, 70],
    [30, 84]])

    arr[:, 0], arr[:, 1] = arr[:, 1], arr[:, 0].copy() # swapping columns

    Nr_lines = len(arr)

    Dash =(15, 15)

    Start_pos = (10,30) # (30, 10)
    End_pos = (90, 30) # (30, 90)

    w, h = 100, 100
    image = Image.new('RGB', (w,h), '#FFFFDD')
    draw = ImageDraw.Draw(image)

    # wide, height = Font.getsize('(30, 84)')
    ununused1, unused2, wide, height = Font.getbbox('(30, 84)')

    for i in range(Nr_lines):
        angled_text(image, (arr[i][0], arr[i][1] + 10 + wide//2),text=str(arr[i]),
                angle=90, fill='black', font=Font)

    for j in range(Nr_lines - 1):
        # TypeError: only length-1 arrays can be converted to Python scalars
        dims(image, draw, arr[j], arr[j+1], (8, 2), text='15', font=Font, fill='lightgreen',
                textorient='vertical')

    line_dashed(draw, Start_pos, End_pos, dash=Dash, width = 1, fill='black')

    image.show()
