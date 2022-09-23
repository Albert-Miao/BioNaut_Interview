import sys

import cv2
import math
import numpy as np
import os

import argparse

BALL_SIZE = 20
FPS = 30
ACCEL_TO_HEIGHT_LIMIT = 2
PRE_SCALED_HOR_VEL = 1


class Ball:
    # Initializes Ball with color as an RGB tuple, acceleration in px/s^2, starting height in px, duration in either 
    # number of frames or bounces, and a boolean determining whether to count by bounces or frames. Also initializes
    # velocity and ball size.
    #
    # acceleration should be limited to a positive value less than the starting height * ACCEL_TO_HEIGHT_LIMIT.
    # starting_height should be a positive value. Can be more than the resolution height.
    # duration should a positive value, and an integer if counting bounces
    # bounces_or_frames = True when counting bounces, False when counting frames.
    def __init__(self, color, acceleration, starting_height, duration, count_frames):
        assert type(color) is list and len(color) == 3
        assert type(color[0]) is int and type(color[1]) is int and type(color[2]) is int
        assert 0 <= color[0] <= 255 and 0 <= color[1] <= 255 and 0 <= color[2] <= 255

        assert type(acceleration) is float or type(acceleration) is int
        assert acceleration > 0

        assert type(starting_height) is float or type(starting_height) is int
        assert starting_height > 0

        assert type(count_frames) is bool

        if count_frames:
            assert type(duration) is int
        else:
            assert type(duration) is int or type(duration) is float

        # Initialize Ball values
        self.color = color
        self.acceleration = acceleration
        self.height = starting_height
        self.count_bounces = count_frames

        if self.count_bounces:
            self.max_frames = duration
            self.curr_frames = 0
        else:
            self.max_bounces = duration
            self.curr_bounces = 0

        self.hor_vel = PRE_SCALED_HOR_VEL
        self.ver_vel = 0

    def nextFrame(self):
        return tuple()


class ScreenWriter:
    def __init__(self, resolution):
        return

    def generate_image(self):
        return 0


# DONE: creates argparse object and passes to parse_args function
# NEED: creates Ball object to be run, initialized with core args
# NEED: creates ScreenWriter object, initialized with core args
# NEED: For however long the video lasts, grab the next frame from Ball with something like nextFrame().
#       Probably returns info of position, color, major and minor axis.
# NEED: Store the relevant info of Ball at each frame until end.
# NEED: Scale the horizontal distance traveled by Ball to better fit the resolution.
# NEED: Pass relevant info to ScreenWriter and append result to images list
# NEED: Save images.


def main():
    args = parse_args(sys.argv[1:])

    return


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--color', dest='color', nargs="+", type=int, default=[255, 255, 255],
                        help='Color of the ball in RGB. Separate values by spaces (--color 255 255 255)')
    parser.add_argument('--count_frames', dest='count_frames', action='store_true')
    parser.add_argument('--duration', dest='duration', type=int, default=3,
                        help='If --count_frames, number of frames, else number of bounces.')
    parser.add_argument('--acceleration', dest='acceleration', type=float, default=9.81,
                        help='Acceleration due to gravity in pixels/seconds^2. Must be positive (above 0).')
    parser.add_argument('--resolution', dest='resolution', nargs="+", type=int, default=[640, 480],
                        help='Resolution of video. Must be 2-dim tuple of positive integers.')
    parser.add_argument('--starting_height', dest='starting_height', type=float, default=400.,
                        help='Starting height of the ball in pixels.')
    parser.add_argument('--ball_radius', dest='ball_radius', type=float, default=20.,
                        help='Radius of the ball in pixels. Ball must be able to fit within given window.')
    parser.add_argument('--fps', dest='fps', type=float, default=30.,
                        help='Frames per second.')

    args = parser.parse_args(args)

    assert len(args.color) == 3
    assert 0 <= args.color[0] <= 255 and 0 <= args.color[1] <= 255 and 0 <= args.color[2] <= 255

    assert args.duration > 0

    assert args.acceleration > 0

    assert len(args.resolution) == 2
    assert args.resolution[0] > 0 and args.resolution[1] > 0

    assert args.starting_height > 0
    
    assert args.ball_radius * 2 <= args.resolution[0] and \
           args.ball_radius * 2 <= args.resolution[1] and \
           "Ball is larger than the resolution of the image."
    
    assert args.fps > 0

    if args.starting_height + args.ball_radius > args.resolution[1]:
        print("WARNING: Inputted starting_height plus ball radius is greater than the height of the window.")

    return args


if __name__ == "__main__":
    main()
