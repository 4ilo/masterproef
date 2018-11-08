#!/usr/bin/python3

import xml.etree.ElementTree as ET
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

classes = ['door_handle', 'sign', 'fire_extinquisher']

if __name__ == '__main__':
    tree = ET.parse(args.file)
    root = tree.getroot()

    print(root.tag)

    if not os.path.isdir('Anotations_yolo'):
        os.mkdir('Anotations_yolo')

    for child in root:
        if child.tag == 'image':
            image = child.get('name')
            w = float(child.get('width'))
            h = float(child.get('height'))

            boxes = ''
            for box in child.findall('box'):
                xtl = float(box.get('xtl'))
                ytl = float(box.get('ytl'))
                xbr = float(box.get('xbr'))
                ybr = float(box.get('ybr'))

                width = xbr - xtl
                height = ybr - ytl
                x = xtl + (width/2)     #center
                y = ytl + (height/2)

                boxes += '{} {} {} {} {}\n'.format(classes.index(box.get('label')), x/w, y/h, width/w, height/h)

            with open('Anotations_yolo/{}.txt'.format(os.path.splitext(image)[0]), 'w') as file:
                file.write(boxes)
