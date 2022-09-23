import sys

import cv2
import math
import numpy as np
import os

import argparse


class Ball:
    # Initializes Ball with color as an RGB tuple, acceleration in px/s^2, starting height in px, duration in either 
    # number of frames or bounces, and a boolean determining whether to count by bounces or frames. Also initializes
    # velocity and ball size.
    #
    # acceleration should be limited to a positive value less than the starting height * ACCEL_TO_HEIGHT_LIMIT.
    # starting_height should be a positive value. Can be more than the resolution height.
    # duration should a positive integer regardless of frames or bounces.
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

        assert type(duration) is int

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
    print('Number of balls: ' + str(len(args)))

    balls = []
    for arg in args:
        balls.append(Ball)

    return


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--color', dest='color', nargs="+", type=int, default=[255, 255, 255],
                        help='Color of the ball in RGB. Separate values by spaces (--color 255 255 255)')
    parser.add_argument('--count_frames', dest='count_frames', action='store_true',
                        help='Whether to determine video length by number of frames. If not, determined by number of '
                             'bounces.')
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
    parser.add_argument('--additional_ball', dest='additional_ball', action='store_true',
                        help='Input values for another ball after this one.')

    args = parser.parse_args(args)

    assert len(args.color) == 3
    assert 0 <= args.color[0] <= 255 and 0 <= args.color[1] <= 255 and 0 <= args.color[2] <= 255

    assert args.duration > 0
    assert args.acceleration > 0

    assert len(args.resolution) == 2
    assert args.resolution[0] > 0 and args.resolution[1] > 0

    assert args.starting_height > 0
    assert args.fps > 0

    acceleration = args.acceleration
    resolution = args.resolution
    count_frames = args.count_frames
    duration = args.duration
    fps = args.fps

    assert args.ball_radius * 2 <= resolution[0] and \
           args.ball_radius * 2 <= resolution[1] and \
           "Ball is larger than the resolution of the image."

    if args.starting_height + args.ball_radius > resolution[1]:
        print("WARNING: Inputted starting_height plus ball radius is greater than the height of the window.")

    balls = []
    if args.additional_ball:
        new_args = get_input('Input new arguments as before (formatted \": --color ...\"): ').strip().split(' ')
        if new_args[0] == '':
            new_args = []

        balls = parse_ball_args(new_args, resolution)

    ball = {'color': args.color,
            'starting_height': args.starting_height,
            'ball_radius': args.ball_radius}

    output_args = {'balls': [ball] + balls,
                   'acceleration': acceleration,
                   'resolution': resolution,
                   'count_frames': count_frames,
                   'duration': duration,
                   'fps': fps}

    return output_args


def get_input(text):
    return input(text)


def parse_ball_args(args, resolution):
    parser = argparse.ArgumentParser()

    parser.add_argument('--color', dest='color', nargs="+", type=int, default=[255, 255, 255],
                        help='Color of the ball in RGB. Separate values by spaces (--color 255 255 255)')
    parser.add_argument('--starting_height', dest='starting_height', type=float, default=400.,
                        help='Starting height of the ball in pixels.')
    parser.add_argument('--ball_radius', dest='ball_radius', type=float, default=20.,
                        help='Radius of the ball in pixels. Ball must be able to fit within given window.')
    parser.add_argument('--additional_ball', dest='additional_ball', action='store_true',
                        help='Input values for another ball after this one.')

    args = parser.parse_args(args)

    assert len(args.color) == 3
    assert 0 <= args.color[0] <= 255 and 0 <= args.color[1] <= 255 and 0 <= args.color[2] <= 255

    assert args.starting_height > 0

    assert args.ball_radius * 2 <= resolution[0] and \
           args.ball_radius * 2 <= resolution[1] and \
           "Ball is larger than the resolution of the image."

    if args.starting_height + args.ball_radius > resolution[1]:
        print("WARNING: Inputted starting_height plus ball radius is greater than the height of the window.")

    balls = []
    if args.additional_ball:
        new_args = get_input('Input new arguments as before (formatted \": --color ...\"): ').strip().split(' ')
        if new_args[0] == '':
            new_args = []

        balls = parse_ball_args(new_args, resolution)

    ball = {'color': args.color,
            'starting_height': args.starting_height,
            'ball_radius': args.ball_radius}
    balls.insert(0, ball)

    return balls


if __name__ == "__main__":
    main()
