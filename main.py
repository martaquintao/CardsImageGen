from PIL import Image, ImageDraw
import math
import colorsys
import random
import os
import datetime

outputs_folder = 'outputs'

## define color ranges
hue_options = {
    'red1' : (0.9861, 1.0),
    'red2' : (0.0, 0.0278),
    'red_orange' : (0.0278, 0.0556),
    'orange_brown': (0.0556, 0.1111),
    'orange_yellow' : (0.1111, 0.1389),
    'yellow' : (0.1389, 0.1667),
    'yellow_green' : (0.1667, 0.2222),
    'green' : (0.2222, 0.3889),
    'green_cyan' : (0.3889, 0.4694),
    'cyan' : (0.4694, 0.5556),
    'cyan_blue' : (0.5556, 0.6111),
    'blue' : (0.6111, 0.6667),
    'blue_magenta' : (0.6667, 0.7778),
    'magenta' : (0.7778, 0.8889),
    'magenta_pink' : (0.8889, 0.9167),
    'pink' : (0.9167, 0.9583),
    'pink_red' : (0.9583, 0.9861),
    'random' : (0.0, 1.0)
}

## define saturation and values ranges
sv_options = {
    'upper' : (0.5, 1.0),
    'lower' : (0.0, 0.5),
    'medium' : (0.25, 0.75),
    'narrow_upper' : (0.7, 1.0),
    'medium_upper' : (0.8, 0.9),
    'narrow_lower' : (0.0, 0.25),
    'narrow_medium' : (0.375, 0.625),
    '0.7' : (0.7,0.7),
    '0.8' : (0.8,0.8),
    '0.9' : (0.9,0.9),
    'full' : (0.0, 1.0),
    'top' : (1.0, 1.0),
    'bottom' : (0.0, 0.0)
}


def ImageGen(num_squares=27, x_size=697, y_size=1039, background="white", hues='cycle', saturations='narrow_upper', values='narrow_upper', iterations=20, save=True, show=False):


    square_size = float(x_size)/num_squares
    square_ynum = int(math.floor(y_size/square_size))
    square_xnum = num_squares

    if save:
        folder = CreateNewFolder(num_squares, background, hues, saturations, values, iterations)

    for iter in xrange(iterations):

        img = Image.new('RGB',(x_size,y_size),background)
        draw = ImageDraw.Draw(img)

        hues_iter = GetIterHues(hues)

        for i in xrange(square_ynum):
            for j in range(square_xnum):

                coord = (j*square_size, i*square_size, (j+1)*square_size, (i+1)*square_size)
                probability = 1-float(i)/square_ynum
                chance = random.random()

                if chance < probability:
                    color = GetRandomSquareColor(hues_iter,saturations,values)
                    draw.rectangle(coord, outline=background,fill=color)
                    #draw.chord(coord,0,360,outline="black",fill=color)
                    #draw.line(coord,width=1,fill="blue")
        if show:
            img.show()
        if save:
            img.save(outputs_folder +'/' + folder
                     +'/img_' + str(iter) + '_' + hues_iter
                     +'.png','PNG')


def GetIterHues(hues):
    return random.choice(hue_options.keys()) if hues == 'cycle' else hues


def GetRandomSquareColor(hues_iter,saturations,values):

    if hues_iter == 'random_options' or hues_iter == 'cycle':
        hues_temp = random.choice(hue_options.keys())
        print hues_temp
    elif hues_iter == 'red':
        hues_temp = random.choice('red1','red2')
    else:
        hues_temp = hues_iter

    hsv_tuple = (random.uniform(hue_options.get(hues_temp)[0],hue_options.get(hues_temp)[1]),
                 random.uniform(sv_options.get(saturations)[0],sv_options.get(saturations)[1]),
                 random.uniform(sv_options.get(values)[0],sv_options.get(values)[1]))
    #rgb_tuples = map(lambda x: hsv2rgb(*x), hsv_tuples)
    #hsv_tuples = [(random.random(), 0.7, 0.9) for x in range(n)]

    rgb_tuple = hsv2rgb(*hsv_tuple)

    color= rgb_tuple

    return color

def hsv2rgb(h,s,v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


def CreateNewFolder(num_squares, background, hues, saturations, values, iterations):

    now = datetime.datetime.now()
    now = now.replace(microsecond=0)
    folder = 'Images_' + str(now) \
             + '_squares_' + str(num_squares) \
             + '_b_' + str(background) \
             + '_iter_' + str(iterations) \
             + '_h_' + str(hues) \
             + '_s_' + str(saturations) \
             + '_v_' + str(values)

    cwd = os.getcwd()
    dest_outputs = os.path.join(cwd, outputs_folder)
    if not os.path.exists(dest_outputs):
        os.makedirs(dest_outputs)

    dest_folder = os.path.join(cwd, outputs_folder, folder)

    # create results folder
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    return folder

ImageGen()


























def tests():

    imgcolors = Image.new('RGB', (255, 255), "black")  # create a new black image
    pixels = imgcolors.load()  # create the pixel map

    for i in range(imgcolors.size[0]):  # for every pixel:
        for j in range(imgcolors.size[1]):
            pixels[i, j] = (i, j, 1)  # set the colour accordingly

    imgcolors.show()