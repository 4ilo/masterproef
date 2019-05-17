# import argparse
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    speed_seg = [x.split(',') for x in open('out/fps_seg.txt').read().splitlines()][:125]
    speed_non_seg = [x.split(',') for x in open('out/fps.txt').read().splitlines()][:125]

    speed_seg = np.array(speed_seg, dtype=float)
    speed_non_seg = np.array(speed_non_seg, dtype=float)

    # Speed plot
    fig, ax = plt.subplots()
    ax.boxplot([speed_seg[:, 5], speed_non_seg[:, 5]], 0, '')
    # plt.plot(speed_seg[:, 5])
    # plt.plot(speed_non_seg[:, 5])
    ax.set_xticklabels(["With segmentation", "Without segmentation"])

    # plt.xlabel("Input Frame")
    plt.ylabel("Calculation time [s]")
    plt.legend([
        'With segmentation: mean = {} s'.format(round(np.mean(speed_seg[:, 5]), 3)),
        'Without segmentation: mean = {} s'.format(round(np.mean(speed_non_seg[:, 5]), 3))
    ])
    plt.title("Location calculation speed on GPU")
    plt.show()

    # Remove last col
    speed_seg = speed_seg[:, :5]
    speed_non_seg = speed_non_seg[:, :5]

    # Calculate normalized means to get a circle
    speed_seg = speed_seg.mean(axis=0)
    row_sum = speed_seg.sum()
    speed_seg = speed_seg/row_sum

    speed_non_seg = speed_non_seg.mean(axis=0)
    row_sum = speed_non_seg.sum()
    speed_non_seg = speed_non_seg/row_sum

    labels = [
        'YOLOv2 object detector',
        'Vanishing point detection',
        'Calculate angles',
        'Calculate costs + location',
        'Plot route'
    ]

    fig1, ax1 = plt.subplots()
    p, t = ax1.pie(speed_seg)
    ax1.legend(p, labels, loc="best")
    ax1.axis('equal')
    plt.title("Calculation time with segmentation")
    plt.show()

    fig2, ax2 = plt.subplots()
    p, t = ax2.pie(speed_non_seg)
    ax2.legend(p, labels, loc="best")
    ax2.axis('equal')
    plt.title("Calculation time without segmentation")
    plt.show()
