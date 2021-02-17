from utils import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import cv2

set_path()

HEIGHT = 180
WIDTH = 240
FILTER_DIST = 400

raw_data_dir = './data/raw'
data_files = os.listdir(raw_data_dir)

for run_folder in data_files:
    if run_folder != 'run_4':
        continue

    # depth file
    with open(os.path.join(raw_data_dir, run_folder, 'depth.txt'), 'r') as f:
        lines = f.readlines()

    depth_raw = []
    depth_timestamp = []

    for line in lines:
        # last character is a '\n', so don't include it in the data
        data_line = list(map(int, line.split(',')[:-1]))
        # first number is the timestamp
        depth_timestamp.append(data_line[0])
        depth_raw.append(data_line[1:])

    depth_timestamp = np.array(depth_timestamp)
    depth_timestamp = (depth_timestamp - depth_timestamp.min()) / 1000.0

    depth_raw = np.array(depth_raw)

    num_frames = depth_raw.shape[0]
    frames = []

    for i in range(int(num_frames)):
        depths = []
        confidences = []
        for j in range(WIDTH * HEIGHT):
            depth = depth_raw[i][j] & 0x1FFF    # 13 bits for depth
            confidence_raw = depth_raw[i][j] >> 13 & 0b111  # 3 bits for confidence
            confidence = 1 if confidence_raw == 0 else confidence_raw/7.0
            depths.append(depth)
            confidences.append(confidence)
        frames.append([depths, confidences])

    for i, frame in enumerate(frames):
        depths = np.array(frame[0])
        depths_filtered = depths.copy()
        depths_filtered[depths_filtered > FILTER_DIST] = 0
        depths = np.reshape(depths, (HEIGHT, -1))

        confidences = np.reshape(np.array(frame[1]), (HEIGHT, -1))
        depths_filtered = np.reshape(depths_filtered, (HEIGHT, -1))

        plt.suptitle(f'{depth_timestamp[i]}s')
        plt.subplot(131), plt.imshow(depths), plt.title(run_folder + ': depth')
        plt.subplot(132), plt.imshow(depths_filtered), plt.title(run_folder + ': depth filtered')
        plt.subplot(133), plt.imshow(confidences), plt.title(run_folder + ': confidence')

        if i != len(frames) - 1:
            delay = depth_timestamp[i + 1] - depth_timestamp[i]
            plt.pause(delay)
    plt.show()
