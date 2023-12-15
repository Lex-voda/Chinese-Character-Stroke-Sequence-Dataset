from utils import  read_data_from_json
import os
import svgwrite
import cairosvg
import cv2
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

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
    img[alpha_channel != 0] = [1,1,1, 0]
    img = img[:,:,:]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, img_binary = cv2.threshold(img_gray, 0, value, cv2.THRESH_BINARY)

    cv2.imwrite(jpg_path, img_binary, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

def process_strokes(graphic, fort_category, i):
    folder_name = "chinese_kaiti_{:04d}".format(i + 1)
    os.makedirs('data/svg/' + folder_name)
    os.makedirs('data/png/' + folder_name)
    os.makedirs('data/jpg/' + folder_name)

    strokes = graphic["strokes"]
    category_id = fort_category[i]["category_id"]

    for j, stroke in enumerate(strokes):
        svg_file_name = 'data/svg/' + folder_name + '/' + str(j) + '.svg'
        png_file_name = 'data/png/' + folder_name + '/' + str(j) + '.png'
        jpg_file_name = 'data/jpg/' + folder_name + '/' + str(j) + '.jpg'

        generate_svg(svg_file_name, stroke)
        svg_to_png(svg_file_name, png_file_name)
        convert_png_to_binary_jpg(png_file_name, jpg_file_name, category_id[j])


def run():
    graphics = read_data_from_json("data_graphics.json")
    fort_category = read_data_from_json("fort_annotation.json")
    with ThreadPoolExecutor() as executor:
        tasks = []
        for i, graphic in enumerate(tqdm(graphics, desc='create characters svg')):
            tasks.append(executor.submit(process_strokes, graphic, fort_category, i))
        # Wait for all tasks to complete
        for future in tqdm(tasks, desc='Waiting for tasks to complete'):
            future.result()

if __name__ == "__main__":
    run()