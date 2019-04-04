#!/usr/bin/python3

import argparse
import shutil
from random import sample
from os import listdir
from os.path import isfile, join


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Select x random images from dir')
    parser.add_argument('--amount', type=int, default=50, help="Amount of images to take")
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')

    args = parser.parse_args()

    files = [f for f in listdir(args.input_dir) if isfile(join(args.input_dir, f))]

    selected = sample(files, args.amount)

    # Copy files to output dir
    for file in selected:
        shutil.copy2("{}/{}".format(args.input_dir, file), "{}/{}".format(args.output_dir, file))

    print("Created sample of {} files.".format(len(selected)))
