import cv2
import math
import numpy as np
import os

import argparse
import sys

def main():
    args = parse_args(sys.argv[1:])
    capture = cv2.VideoCapture(args['path'])

    assert capture.isOpened() and "Error opening video. Could be a multitude of problems, but likely corruption."

    fps = capture.get(cv2.CAP_PROP_FPS)
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        masks = distinct_color_masks(frame)

        cv2.imshow('Frame', frame)
        cv2.waitKey(int(1000/fps))


def distinct_color_masks(img):

    # Identify background color
    unique_colors, unique_counts = np.unique(img.reshape((-1, 3)), return_counts=True, axis=0)
    sorted_indices = np.argsort(unique_counts)
    bg_ind = sorted_indices[-1]
    bg_color = unique_colors[bg_ind]

    # Filter out background
    mask = cv2.bitwise_not(cv2.inRange(img, bg_color, bg_color))
    img = cv2.bitwise_and(img, img, mask=mask)

    sorted_indices = sorted_indices[:-1]

    for i in range(len(sorted_indices) - 1, -1, -1):
        color = unique_colors[sorted_indices[i]]
        mask = cv2.inRange(img, color, color)
        filtered_img = cv2.bitwise_and(img, img, mask=mask)

        print(color)
        cv2.imshow('test', filtered_img)
        cv2.waitKey(0)


    return filtered_img


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--path', dest='path', type=str, default='sample_videos/test.avi',
                        help='Path to video to load.')
    parser.add_argument('--tolerance', dest='tolerance', type=int, default=10,
                        help='Tolerance for colors. When detecting balls, colors that fall within the range of another'
                             'will be considered part of the same ball.')
    parser.add_argument('--output_dir', dest='output_dir', type=str, default='sample_videos',
                        help='Output directory for tracking video')
    parser.add_argument('--save_name', dest='save_name', type=str, default='tracking.avi',
                        help='Name to save video under')

    args = parser.parse_args(args)
    assert os.path.exists(args.path)

    assert args.save_name[-4:] == '.avi' and "Ending is not '.avi'"

    args = {
        'path': args.path,
        'tolerance': args.tolerance,
        'output_dir': args.output_dir,
        'save_name': args.save_name
    }

    return args



if __name__ == "__main__":
    main()
