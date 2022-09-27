import cv2
import math
import numpy as np
import os

import argparse
import sys


def main():
    args = parse_args(sys.argv[1:])
    capture = cv2.VideoCapture(args.path)

    assert capture.isOpened() and "Error opening video. Could be a multitude of problems, but likely corruption."

    fps = capture.get(cv2.CAP_PROP_FPS)

    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        cv2.imshow('Frame', frame)
        cv2.waitKey(int(1000/fps))

def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--path', dest='path', type=str, default='sample_videos/1.avi',
                        help='Path to video to load.')

    args = parser.parse_args(args)

    assert os.path.exists(args.path)

    return args



if __name__ == "__main__":
    main()
