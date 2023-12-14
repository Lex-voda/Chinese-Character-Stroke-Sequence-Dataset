from utils import  read_data_from_json
import os
import svgwrite
import cairosvg
import cv2
from tqdm import tqdm

def generate_svg(svg_save_path, path_data):
    dwg = svgwrite.Drawing(svg_save_path, profile='tiny', size=(1024, 1024))
    group = dwg.g(transform="scale(1, -1) translate(0, -900)")
    path = dwg.path(d=path_data, class_="stroke1")
    group.add(path)
    dwg.add(group)
    dwg.save()

def svg_to_png(svg_file_path, jpg_file_path):
    with open(svg_file_path, 'r') as svg_file:
        svg_content = svg_file.read()
    cairosvg.svg2png(bytestring=svg_content, write_to=jpg_file_path)

def convert_png_to_binary_jpg(png_path, jpg_path, value):
    img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    alpha_channel = img[:, :, 3]
    #_, mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)
    #img[mask == 0] = [0, 0, 0, 0]
    img[alpha_channel != 0] = [1,1,1, 0]
    img = img[:,:,:]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, img_binary = cv2.threshold(img_gray, 0, value, cv2.THRESH_BINARY)

    cv2.imwrite(jpg_path, img_binary, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


if __name__ == "__main__":
    graphics = read_data_from_json("data_graphics.json")
    fort_category = read_data_from_json("fort_annotation.json")
    for i, graphic in enumerate(tqdm(graphics, desc = 'create characters svg')):
        folder_name = "chinese_kaiti_{:04d}".format(i)
        os.makedirs('data/svg/' + folder_name)
        strokes = graphic["strokes"]
        for i, stroke in enumerate(strokes):
            svg_file_name = 'data/svg/' + folder_name + '/' + str(i) + '.svg'
            svg_creator = generate_svg(svg_file_name, stroke)

    for i, graphic in enumerate(tqdm(graphics, desc='create characters png')):
        folder_name = "chinese_kaiti_{:04d}".format(i)
        os.makedirs('data/png/' + folder_name)
        strokes = graphic["strokes"]
        for i, stroke in enumerate(strokes):
            svg_file_name = 'data/svg/' + folder_name + '/' + str(i) + '.svg'
            png_file_name = 'data/png/' + folder_name + '/' + str(i) + '.png'
            svg_to_png(svg_file_name, png_file_name)

    for i, graphic in enumerate(tqdm(graphics, desc='create characters binary_jpg')):
        folder_name = "chinese_kaiti_{:04d}".format(i)
        os.makedirs('data/jpg/' + folder_name)
        strokes = graphic["strokes"]
        category_id = fort_category[i]["category_id"]
        for j, stroke in enumerate(strokes):
            png_file_name = 'data/png/' + folder_name + '/' + str(i) + '.png'
            jpg_file_name = 'data/jpg/' + folder_name + '/' + str(i) + '.jpg'
            value = category_id[j]
            convert_png_to_binary_jpg(png_file_name,jpg_file_name,value)
