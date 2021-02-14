# Author: BeiYu
# Github: https://github.com/beiyuouo
# Date  : 2021/2/13 16:22
# Description:

from PIL import Image, ImageOps, ImageFilter
import argparse
import numpy as np
import os

# 命令行输入参数处理
parser = argparse.ArgumentParser()

parser.add_argument('file')  # 输入文件
parser.add_argument('-o', '--output', default=os.path.join('.', 'result'))  # 输出文件
parser.add_argument('-l', '--len', type=int, default=4, help='number of paper')
parser.add_argument('--width', type=int, default=2812)  # 输出字符画宽 148
parser.add_argument('--height', type=int, default=1995)  # 输出字符画高 105
parser.add_argument('--border', type=int, default=10)  # TODO
parser.add_argument('--line_width', type=int, default=3)
parser.add_argument('--mb', type=int, default=7, help='medianBlur')

# 获取参数
args = parser.parse_args()

IMG = args.file
LENGTH = args.len
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output
BORDER = args.border
LINE_WIDTH = args.line_width


def get_layer(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = LENGTH
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1) / length
    return int(gray / unit)


def generate_imgs(pix):
    print(len(pix))
    for i in range(LENGTH):
        img = [[] for x in range(HEIGHT)]
        color = int(256 / LENGTH * i)
        for x in range(HEIGHT):
            for y in range(WIDTH):
                if pix[x][y] >= i:
                    img[x].append(color)
                else:
                    img[x].append(255)
        # print(img)
        img = np.array(img)
        img_arr = img.copy()
        img = img.astype(np.uint8)
        print(img.shape)
        # img = img.transpose((2, 1, 0)).astype(np.uint8)
        # print(img.shape)
        # print(img)
        img = Image.fromarray(img, 'L')
        # img.show()
        img.save(os.path.join(OUTPUT, f'cov_{i}.jpg'))
        generate_print(img_arr, color, os.path.join(OUTPUT, f'print_{i}.jpg'))


def generate_print(img, color, path):
    new_img = img.copy()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if img[i][j] == color:
                new_img[i][j] = 230
            else:
                new_img[i][j] = 255  # 0 black
    new_img = new_img.astype(np.uint8)
    new_img = Image.fromarray(new_img, 'L')
    # img.show()
    new_img.save(path)


if __name__ == '__main__':

    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

    im = im.filter(ImageFilter.GaussianBlur(radius=5))
    # im = im.filter(ImageFilter.EMBOSS)

    txt = ""
    pix = []

    for i in range(HEIGHT):
        pix.append([])
        for j in range(WIDTH):
            layer = get_layer(*im.getpixel((j, i)))
            txt += str(layer)
            pix[i].append(layer)
        txt += '\n'

    generate_imgs(pix)

    # print(txt)

    with open(os.path.join(OUTPUT, 'result.txt'), 'w') as f:
        f.write(txt)
