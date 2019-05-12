# import argparse
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    speed_seg = [float(x) for x in open('out/fps_seg.txt').read().splitlines()][:125]
    speed_non_seg = [float(x) for x in open('out/fps.txt').read().splitlines()][:125]

    plt.plot(speed_seg)
    plt.plot(speed_non_seg)

    plt.xlabel("Input Frame")
    plt.ylabel("Calculation time")
    plt.legend([
        'With segmentation: {}'.format(round(np.mean(speed_seg), 3)),
        'Without segmentation: {}'.format(round(np.mean(speed_non_seg), 3))
    ])
    plt.title("Location calculation speed on GPU")

    plt.show()