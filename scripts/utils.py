import os
import sys
from pathlib import Path
import numpy as np
import cv2


def set_path(user='auto'):
    if user == 'auto':
        user = detect_user()

    print(f'Setting path for {user}...')

    if user == 'saman':  # saman's personal computer
        recursive_unix_dir_backtrack('android_depth_parser')
    elif user == 'samosia':  # vector cluster
        recursive_unix_dir_backtrack('android_depth_parser')
    else:
        raise Exception('unable to recognize user')


def mkdir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def recursive_unix_dir_backtrack(desired_dir):
    dir_name = os.getcwd().split('/')[-1]
    if dir_name != desired_dir:
        os.chdir('..')
        recursive_unix_dir_backtrack(desired_dir)


def detect_user():
    users = ['saman', 'samosia']
    exec_path = sys.executable.lower()
    user = None
    for u in users:
        if u in exec_path:
            user = u

    if user is None:
        raise Exception('unable to detect user')
    return user


def convert_to_rgb(frame: np.ndarray):
    max = frame.max(initial=0)
    min = frame.min(initial=255)
    return np.interp(frame, [min, max], [0, 255]).astype(np.uint8)


def get_frame_count(cap):
    return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


def get_video_frame(cap, frame_ind):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_ind)
    ret, frame = cap.read()
    return frame
