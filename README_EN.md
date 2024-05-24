# Chinese-Character-Stroke-Sequence-Dataset
**Image dataset of Chinese character stroke sequences**

#### Dataset Source

This project integrates the [CCES dataset](https://github.com/lizhaoliu-Lec/CCSE.git) proposed by Liu et al., and the [Chinese character stroke dataset](https://github.com/chanind/makemeahanzi.git) proposed by Arphic Technology Co., Ltd. Thanks to the contributions of the above two projects.

#### Dataset Description

Datasets containing stroke sequence information for Chinese characters are very rare. Arphic Technology Co., Ltd. provided an excellent work (makemeahanzi), drawing Chinese characters according to accurate stroke information; Liu et al.'s CCES work further annotated the stroke information with 25 stroke categories.

This dataset integrates the work of both, compared to the CCES dataset, this dataset aligns the curve data of makemeahanzi with the annotation data (fort_annotation.json) of CCES, and generates the corresponding stroke sequence diagram directly on the local machine through the curve information and annotation information. Therefore, the online files of this dataset are smaller, and the offline files have higher resolution.

The integrated annotation information is stored in `fort_graphics.json`.

Like CCES, this dataset contains annotation information for 9523 Chinese characters, and all images are 1024*1024 binary images.

The data generation script finally generates 9523 npz files, each of which is a compressed three-dimensional matrix. Each slice on the 0th dimension is a stroke of the character, arranged in stroke order. If stacked on the 0th dimension, it forms a complete character. This dataset retains as much information as possible for researchers to use.

#### Usage Instructions

This project is based on python development. In addition to common libraries, please run the following command to install some necessary libraries:

```bash
pip install opencv-python svgwrite cairosvg 
```

To use cairosvg correctly, please go here to download GTK-3 and restart your computer (Windows system) (add environment variables by default). The direct download link is here.

Run the command to start generating data:

```
python run.py
```

