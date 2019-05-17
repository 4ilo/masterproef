import numpy as np
import matplotlib.pyplot as plt

# Data to plot
n_groups = 2
# GPU Data
# means_hp = [0.1650, 0.4230]
# means_seg = [0.1708, 0.4878]
# means_hough = [0.0145, 0.0201]

# CPU Data
means_hp = [0.9393, 2.6309]
means_seg = [0.9422, 2.6463]
means_hough = [0.0150, 0.0189]

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.3
opacity = 0.8

rects1 = plt.bar(index - bar_width, means_hp, bar_width,
alpha=opacity,
label='Highest Pixel')

rects2 = plt.bar(index, means_seg, bar_width,
alpha=opacity,
label='Hough segmentation')

rects2 = plt.bar(index + bar_width, means_hough, bar_width,
alpha=opacity,
label='Hough transform')

plt.ylabel('Detection time [s]')
plt.title('VP detection time on CPU')
plt.xticks(index, ('747x420p', '1280x720p'))
plt.legend()

for i in range(len(index)):
    plt.text(x=i-bar_width*1.4, y=means_hp[i]+0.009, s=str(means_hp[i])+' s')
    plt.text(x=i-0.12, y=means_seg[i]+0.009, s=str(means_seg[i])+' s')
    plt.text(x=i+bar_width*0.6, y=means_hough[i]+0.009, s=str(means_hough[i])+' s')

plt.show()