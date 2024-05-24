import os
import svgwrite
import cairosvg
import cv2
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from utils import read_data_from_json

class CharacterGenerator:
    def __init__(self, overwrite=False, remove_intermediate_files=False):
        self.overwrite = overwrite
        self.remove_intermediate_files = remove_intermediate_files

    def generate_svg(self, svg_save_path, path_data):
        dwg = svgwrite.Drawing(svg_save_path, profile='tiny', size=(1024, 1024))
        group = dwg.g(transform="scale(1, -1) translate(0, -900)")
        path = dwg.path(d=path_data, class_="stroke1")
        group.add(path)
        dwg.add(group)
        dwg.save()

    def svg_to_png(self, svg_file_path, jpg_file_path):
        with open(svg_file_path, 'r') as svg_file:
            svg_content = svg_file.read()
        cairosvg.svg2png(bytestring=svg_content, write_to=jpg_file_path)

    def convert_png_to_binary(self, png_path, value):
        img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
        alpha_channel = img[:, :, 3]
        img[alpha_channel != 0] = [1,1,1, 0]
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, img_binary = cv2.threshold(img_gray, 0, value, cv2.THRESH_BINARY)
        return img_binary

    def process_strokes(self, graphic, i):
        folder_name = "chinese_kaiti_{:04d}".format(i + 1)
        os.makedirs('data/svg/' + folder_name)
        os.makedirs('data/png/' + folder_name)

        strokes = graphic["strokes"]
        category_id = graphic["category_id"]

        binary = []
        for j, stroke in enumerate(strokes):
            svg_file_name = 'data/svg/' + folder_name + '/' + str(j) + '.svg'
            png_file_name = 'data/png/' + folder_name + '/' + str(j) + '.png'

            self.generate_svg(svg_file_name, stroke)
            self.svg_to_png(svg_file_name, png_file_name)
            binary.append(self.convert_png_to_binary(png_file_name, category_id[j]))
            if self.remove_intermediate_files:
                os.remove(svg_file_name)
                os.remove(png_file_name)
        if self.remove_intermediate_files:
            os.rmdir('data/svg/' + folder_name)
            os.rmdir('data/png/' + folder_name)
        # convert binary to npz
        binary = np.array(binary)
        np.savez_compressed('data/npz/' + folder_name + '.npz', binary=binary)

    def run(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        os.makedirs('data/npz/')
        self.graphics = read_data_from_json("fort_graphics.json")
        with ThreadPoolExecutor() as executor:
            tasks = []
            for i, graphic in enumerate(tqdm(self.graphics, desc='create characters')):
                tasks.append(executor.submit(self.process_strokes, graphic, i))
                if i == 10:
                    break
            # Wait for all tasks to complete
            for future in tqdm(tasks, desc='Waiting for tasks to complete'):
                future.result()
        if self.remove_intermediate_files:
            os.rmdir('data/svg/')
            os.rmdir('data/png/')
        print('Done')

if __name__ == "__main__":
    generator = CharacterGenerator(overwrite=True, remove_intermediate_files=True)
    generator.run()