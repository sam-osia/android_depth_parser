import os
import sys
import numpy as np


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
    max = frame.max()
    min = frame.min()
    return np.interp(frame, [min, max], [0, 255]).astype(np.uint8)
