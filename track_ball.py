import cv2
import math
import numpy as np
import os

import argparse
import sys
import time

CONTOUR_THRESHOLD = 2
THUMBNAIL_FACTOR = 5

BORDER_COLOR = (0, 255, 0)
THUMBNAIL_COLOR = (0, 255, 0)


def main():
    args = parse_args(sys.argv[1:])
    capture = cv2.VideoCapture(args['path'])

    assert capture.isOpened() and "Error opening video. Could be a multitude of problems, but likely corruption."

    fps = capture.get(cv2.CAP_PROP_FPS)
    error_shown = False
    count = 0

    # Iterate through frames of video
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        start = time.time()
        count += 1

        # Copy the original image, resized.
        thumbnail = frame[::THUMBNAIL_FACTOR, ::THUMBNAIL_FACTOR].copy()
        thumbnail[:, -2:] = THUMBNAIL_COLOR
        thumbnail[-2:] = THUMBNAIL_COLOR

        # Find contours and draw them.
        contours = distinct_contours(frame, args['tolerance'], args['background_color'])
        frame = cv2.drawContours(frame, contours, -1, BORDER_COLOR, 2)

        # Added thumbnail and frame number to video.
        frame[:thumbnail.shape[0], :thumbnail.shape[1]] = thumbnail
        frame = cv2.putText(frame, str(count).zfill(5), (0, frame.shape[0] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color=THUMBNAIL_COLOR)

        end = time.time()
        time_to_run = end - start

        cv2.imshow('Frame', frame)

        # Try to show the image in time with the fps. If not able to, show an error.
        if int(1000) / fps - time_to_run > 0:
            cv2.waitKey(int(1000 / fps))
        elif not error_shown:
            print("WARNING: Scene too difficult to draw with given fps. Saved video will be in correct speed. Consider "
                  "increasing tolerance.")
            cv2.waitKey(1)
            error_shown = True


def distinct_contours(img, tolerance, bg_color):
    assert type(img) is np.ndarray and len(img.shape) == 3 and img.shape[-1] == 3
    assert tolerance >= 0
    assert (type(bg_color) is list or type(bg_color) is np.ndarray) and len(bg_color) == 3

    bg_color = np.array(bg_color)

    # Filter out background with tolerance. Since the video is saved in a compressed format, there are going to be some
    # artifacts in the image. We could do a harder gaussian blur to get rid of some of the most extreme cases, but I
    # believe that might inhibit tracking of the smallest balls.
    bg_high = np.clip(bg_color.astype('int') + tolerance, 0, 255).astype('uint8')
    bg_low = np.clip(bg_color.astype('int') - tolerance, 0, 255).astype('uint8')
    mask = cv2.bitwise_not(cv2.inRange(img, bg_low, bg_high))
    img = cv2.bitwise_and(img, img, mask=mask)

    # Find unique colors from all remaining pixels. These are our potential balls colors.
    unique_colors, unique_counts = np.unique(img[mask.astype('bool')], return_counts=True, axis=0)

    all_contours = []
    while len(unique_colors):
        # While there are still possible colors, we take the color with the most pixels and mask it.
        color_ind = np.argmax(unique_counts)
        color = unique_colors[color_ind].astype('int')
        color_high = np.clip(color + tolerance, 0, 255).astype('uint8')
        color_low = np.clip(color - tolerance, 0, 255).astype('uint8')
        mask = cv2.inRange(img, color_low, color_high)

        # We then find contours with a minimum area and record them.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [contour for contour in contours if cv2.contourArea(contour) > CONTOUR_THRESHOLD]

        # Finally, we remove colors that fall within the tolerance of the currently iterated color.
        valid_inds = cv2.inRange(unique_colors.reshape(-1, 1, 3), color_low, color_high)
        valid_inds = cv2.bitwise_not(valid_inds).astype('bool').reshape(-1)
        unique_colors = unique_colors[valid_inds]
        unique_counts = unique_counts[valid_inds]
        all_contours += contours

    return all_contours


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--path', dest='path', type=str, default='sample_videos/test.avi',
                        help='Path to video to load.')
    parser.add_argument('--tolerance', dest='tolerance', type=int, default=30,
                        help='Tolerance for colors. When detecting balls, colors that fall within the range of another'
                             'will be considered part of the same ball.')
    parser.add_argument('--background_color', dest='background_color', nargs="+", type=int, default=[50, 50, 50],
                        help='Color of the background. For optimal detection, avoid choosing too similar ball and '
                             'background colors.')
    parser.add_argument('--output_dir', dest='output_dir', type=str, default='sample_videos',
                        help='Output directory for tracking video')
    parser.add_argument('--save_name', dest='save_name', type=str, default='tracking.avi',
                        help='Name to save video under')

    args = parser.parse_args(args)
    assert os.path.exists(args.path)
    assert args.tolerance >= 0
    assert 0 <= args.background_color[0] <= 255 and \
           0 <= args.background_color[1] <= 255 and \
           0 <= args.background_color[2] <= 255

    assert args.save_name[-4:] == '.avi' and "Ending is not '.avi'"

    args = {
        'path': args.path,
        'tolerance': args.tolerance,
        'output_dir': args.output_dir,
        'save_name': args.save_name,
        'background_color': args.background_color
    }

    return args


if __name__ == "__main__":
    main()
