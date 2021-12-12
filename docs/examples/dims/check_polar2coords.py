from PIL import Image, ImageDraw, ImageFont
from math import pi, atan2, degrees, radians, dist
from DimLinesPIL import angled_text, polar2cart, int_up

Font = ImageFont.truetype('consola.ttf', 12)

w, h = 200, 200 # 30, 30 #
image = Image.new('RGB', (w,h), '#FFFFDD')

draw = ImageDraw.Draw(image)

o = (30, 30) # (100, 100)

y = [100, 150, 150,150, 100, 50, 50, 50]
x = [150, 150, 100, 50, 50, 50, 100, 150]

#angle = [0, 90, 180, 270]
angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
x2 = (120,126) #(10, 10)
size = 60
'''
print(size)
for i in range(len(angle)):
    x3 = polar2cart(x2, angle[i], size)
    print(x3, round(dist(x2,x3),3), angle[i])

for i in range(len(angle)):
    x1, y1 = polar2cart(o, angle[i],100)
    draw.line([o,(x1, y1)], fill='black')
    fact = -1 if abs(atan2(y1-o[1], x1-o[0])) > pi/2 else 1
    text = str(int_up(degrees(abs(atan2(y1-o[1], x1-o[0])))))
    angled_text(image, (x1+fact*20,y1), text,
                fact*angle[i], font=Font)
    #print(i, angle[i], x1, y1, text ,'i, angle, x1, y1, text')
'''
ang = 350
end = 25

x3 = polar2cart(x2, ang, size)
draw.line([x2, x3], fill = 'blue')
x4 = polar2cart(x2, end, size)
draw.line([x2, x4], fill = 'blue')
print(x2, 'x2', x3, 'x3', dist(x2,x3), 'angle', ang, 'size', size)
draw.text((4,19), str(ang), fill='blue')
image.show()
'''
angle = 185
theta = radians(angle)
x0, y0 = polar2cart(o, theta, 63)
x1, y1 = polar2cart(o, theta, 63*9)

print(x0, y0, 'x0, y0')
print(x1, y1, 'x1, y1')
print(int_up(degrees(atan2(y1-o[1], x1-o[0]))), 'x1, y1')
print(int_up(degrees(atan2(y0-o[1], x0-o[0]))), 'x0, y0')


#draw.line([(o), (x1,y1)], fill='black')
#draw.line([(o), (x0,y0)], fill='red')

x = [26, 26]
y = [74, 26]

theta = atan2(y[1] - y[0], x[1] - x[0])
print(theta)
theta = theta if theta >= 0 else theta + 2 * pi
if theta == 3*pi/2: #4.7123 < theta < 4.7124:
    print('yup')
else:
    print('nope')
'''
#image.show()