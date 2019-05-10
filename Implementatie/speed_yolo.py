import argparse
import time
from tqdm import tqdm
from os import listdir
import os
import matplotlib.pyplot as plt
from os.path import isfile, join
from Detector.darknet.Darknet import performDetect
import numpy as np

if __name__ == "__main__":
    print("##### FORCE CPU WITH \"FORCE_CPU=1\" ENV VARIABLE ######")
    parser = argparse.ArgumentParser(description='Get average yolo frame rate/inference time')
    parser.add_argument('img_path', help="Path to image files")
    parser.add_argument('yolo_config_dir', help="Path to yolo config dir")
    args = parser.parse_args()

    run_cpu = 'FORCE_CPU' in os.environ

    # Get all images
    images = sorted([args.img_path + "/" + f for f in listdir(args.img_path) if isfile(join(args.img_path, f))])
    images = images[:50]

    time_data = []

    # Init network
    performDetect(imagePath=images[0],
                            thresh=0.25,
                            configPath=args.yolo_config_dir + "/cust.cfg",
                            weightPath=args.yolo_config_dir + "/cust.weights",
                            metaPath=args.yolo_config_dir + "/cust.data",
                            showImage=False)

    # Run on gpu
    for img in tqdm(images):
        start = time.time()

        performDetect(imagePath=img,
                            thresh=0.25,
                            configPath=args.yolo_config_dir + "/cust.cfg",
                            weightPath=args.yolo_config_dir + "/cust.weights",
                            metaPath=args.yolo_config_dir + "/cust.data",
                            showImage=False)

        end = time.time()
        time_data.append(end-start)


    mean_gpu = np.mean(time_data)
    print("Mean GPU: {}".format(mean_gpu))
    mean_data = [mean_gpu for x in range(len(time_data))]

    plt.plot(time_data, label="Time")
    plt.plot(mean_data, label="Average time: {}s".format(round(mean_gpu,4)))
    plt.suptitle('Inference time YOLOv2 on {}'.format("CPU" if run_cpu else "GPU"))
    plt.ylabel("Inference time")
    plt.xlabel("Input frame")
    plt.legend()
    plt.show()