import argparse
import numpy as np
import matplotlib.pyplot as plt


def calc_error(ground_truth, data):
    error = []
    for point in data[:125]:
        if point[0] in ground_truth:
            real_location = ground_truth[point[0]]
            detected_location = int(point[1])
            error.append(detected_location - real_location)

    mean_error = np.mean(error)
    return error, mean_error


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate localisation accuracy")
    parser.add_argument('ground_truth', type=str, help="Csv file with image names and actual location on map")
    # parser.add_argument('location_data', type=str, help="Csv file with image names and detected location")
    args = parser.parse_args()

    ground_truth = {x.split(',')[0]: int(x.split(',')[1]) for x in open(args.ground_truth, 'r').read().splitlines()}

    data_hough = [x.split(',') for x in open("out/output_lights_hough.csv", 'r').read().splitlines()]
    data_hp = [x.split(',') for x in open("out/output_lights_hp.csv", 'r').read().splitlines()]
    data_houghfloor = [x.split(',') for x in open("out/output_lights_houghfloor.csv", 'r').read().splitlines()]

    e1 = calc_error(ground_truth, data_hough)
    e2 = calc_error(ground_truth, data_hp)
    e3 = calc_error(ground_truth, data_houghfloor)

    plt.plot(e1[0])
    plt.plot(e2[0])
    plt.plot(e3[0])

    plt.xlabel("Input frame")
    plt.ylabel("Location error")
    plt.legend([
            'Hough transform: {}'.format(round(e1[1], 3)),
            'Seg Highest pixel: {}'.format(round(e2[1], 3)),
            'Seg Hough: {}'.format(round(e3[1], 3))
        ])
    plt.title("Location error with 1 class detector")
    plt.show()