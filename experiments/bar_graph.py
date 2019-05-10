import numpy as np
import matplotlib.pyplot as plt

# Data to plot
n_groups = 2
means_cpu = [7.6924, 7.8738]
means_gpu = [0.0271, 0.0335]
r = means_cpu + means_gpu

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, means_cpu, bar_width,
alpha=opacity,
label='CPU')

rects2 = plt.bar(index + bar_width, means_gpu, bar_width,
alpha=opacity,
label='GPU')

plt.ylabel('Inference time')
plt.title('YOLOv2 inference time')
plt.xticks(index + bar_width/2, ('747x420p', '1280x720p'))
plt.legend()

for i in range(len(index)):
    plt.text(x=i-bar_width/4, y=means_cpu[i]+0.1, s=str(means_cpu[i])+' s')
    plt.text(x=i+bar_width/1.4, y=means_gpu[i]+0.1, s=str(means_gpu[i])+' s')

plt.show()