import argparse
from os import listdir
import os
from os.path import isfile, join, splitext

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Do something")
    parser.add_argument('image_folder', type=str, help="Path to folder with input images")
    parser.add_argument('output_folder', type=str, default=False, help="Path to output folder")

    args = parser.parse_args()

    files = [f for f in listdir(args.image_folder) if isfile(join(args.image_folder, f))]

    for file in files:
        if splitext(file)[1] == '.png':
            print("Processing {}".format(args.image_folder + "/" + file))
            os.system("python test_seg.py {} {} {} > /dev/null 2>&1".format(args.image_folder + "/" + file, "--output_path", args.output_folder + "/" + file))
