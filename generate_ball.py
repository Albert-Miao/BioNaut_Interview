import sys

import cv2
import math
import numpy as np
import os

import argparse

PRE_SCALED_HOR_VEL = 1


class Ball:
    # Initializes Ball with color as an RGB tuple, ball radius, & starting height in px, all in a dictionary.
    #
    # ball_attr is a dictionary with keys ['color', 'radius', 'starting_height']
    #   'color': A 3-dim tuple of integers between 0 and 255
    #   'radius': A positive float larger than 0.5
    #   'starting_height': A positive float greater than radius.
    #   'deformation': A positive float from 0 to 1.
    def __init__(self, ball_attr):
        assert type(ball_attr['color']) is list and len(ball_attr['color']) == 3
        assert type(ball_attr['color'][0]) is int and \
               type(ball_attr['color'][1]) is int and \
               type(ball_attr['color'][2]) is int
        assert 0 <= ball_attr['color'][0] <= 255 and \
               0 <= ball_attr['color'][1] <= 255 and \
               0 <= ball_attr['color'][2] <= 255

        assert type(ball_attr['radius'] is float or type(ball_attr['radius'] is int))
        assert ball_attr['radius'] > 0.5

        assert type(ball_attr['starting_height']) is float or type(ball_attr['starting_height']) is int
        assert ball_attr['starting_height'] > 0

        assert type(ball_attr['deformation'] is float or type(ball_attr['deformation'] is int))
        assert 0 <= ball_attr['deformation'] <= 1

        self.color = ball_attr['color']
        self.radius = ball_attr['radius']
        self.height = ball_attr['starting_height']
        self.deformation = ball_attr['deformation']

        self.hor_vel = PRE_SCALED_HOR_VEL
        self.ver_vel = 0

    def nextFrame(self):
        return tuple()


# Create a separate BallManager class because there are many attributes that are shared between balls, thus making it
# redundant in the Ball class, that are also relevant to trajectory calculation, making it different from the
# ScreenWriter class.
class BallManager:
    # Initializes BallManager with duration in either number of frames or bounces, a boolean determining whether to
    # count by bounces or frames, and acceleration.
    #
    # acceleration should be a positive value.
    # duration should a positive integer regardless of frames or bounces.
    # bounces_or_frames = True when counting bounces, False when counting frames.
    def __init__(self, acceleration, duration, count_frames, fps, balls=None):
        if balls is None:
            balls = []

        assert type(acceleration) is float or type(acceleration) is int
        assert acceleration > 0

        assert type(count_frames) is bool
        assert type(duration) is int

        self.acceleration = acceleration
        self.count_bounces = count_frames
        if self.count_bounces:
            self.max_frames = duration
            self.curr_frames = 0
        else:
            self.max_bounces = duration
            self.curr_bounces = 0

        self.fps = fps
        self.balls = balls

    def nextFrame(self):
        return [], 0


class ScreenWriter:
    # Initializes ScreenWriter. Only takes in resolution, a 2-dim tuple of positive integers, and fps, a positive
    # integer.
    def __init__(self, resolution, fps):
        assert (type(resolution) is list or type(resolution) is tuple) and len(resolution) == 2
        assert type(resolution[0]) is int and type(resolution[1]) is int
        assert resolution[0] > 0 and resolution[1] > 0

        assert type(fps) is int and fps > 0

        self.resolution = resolution
        self.curr_display = np.zeros((resolution[0], resolution[1], 3))
        self.fps = fps
        return

    def generate_image(self):
        return 0


# DONE: creates argparse object and passes to parse_args function
# DONE: creates Ball object to be run, initialized with core args
# DONE: creates BallManager object with all relevant balls.
# DONE: creates ScreenWriter object, initialized with core args
# NEED: For however long the video lasts, grab the next frame from Ball with something like nextFrame().
#       Probably returns info of position, color, major and minor axis.
# NEED: Store the relevant info of Ball at each frame until end.
# NEED: Scale the horizontal distance traveled by Ball to better fit the resolution.
# NEED: Pass relevant info to ScreenWriter and append result to images list
# NEED: Save images.


def main():
    args = parse_args(sys.argv[1:])
    ball_args = args['balls']
    print('Number of balls: ' + str(len(ball_args)))

    balls = []
    for ball_arg in ball_args:
        balls.append(Ball(ball_arg))

    manager = BallManager(args['acceleration'], args['duration'], args['count_frames'], args['fps'], balls)
    screenwriter = ScreenWriter(args['resolution'], args['fps'])



    return


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--color', dest='color', nargs="+", type=int, default=[255, 255, 255],
                        help='Color of the ball in RGB. Separate values by spaces (--color 255 255 255)')
    parser.add_argument('--starting_height', dest='starting_height', type=float, default=400.,
                        help='Starting height of the ball in pixels.')
    parser.add_argument('--radius', dest='radius', type=float, default=20.,
                        help='Radius of the ball in pixels. Ball must be able to fit within given window.')
    parser.add_argument('--deformation', dest='deformation', type=float, default=0.0,
                        help='Deformation of the ball, between 0 and 1. 0 is no deformation, 1 is the most.')

    parser.add_argument('--count_frames', dest='count_frames', action='store_true',
                        help='Whether to determine video length by number of frames. If not, determined by number of '
                             'bounces.')
    parser.add_argument('--duration', dest='duration', type=int, default=3,
                        help='If --count_frames, number of frames, else number of bounces.')
    parser.add_argument('--acceleration', dest='acceleration', type=float, default=9.81,
                        help='Acceleration due to gravity in pixels/seconds^2. Must be positive (above 0).')
    parser.add_argument('--resolution', dest='resolution', nargs="+", type=int, default=[640, 480],
                        help='Resolution of video. Must be 2-dim tuple of positive integers.')
    parser.add_argument('--fps', dest='fps', type=float, default=30.,
                        help='Frames per second.')
    parser.add_argument('--additional_ball', dest='additional_ball', action='store_true',
                        help='Input values for another ball after this one.')

    args = parser.parse_args(args)

    assert len(args.color) == 3
    assert 0 <= args.color[0] <= 255 and 0 <= args.color[1] <= 255 and 0 <= args.color[2] <= 255
    assert args.radius > 0.5
    assert args.starting_height > 0
    assert 0 <= args.deformation <= 1

    assert args.duration > 0
    assert args.acceleration > 0
    assert len(args.resolution) == 2
    assert args.resolution[0] > 0 and args.resolution[1] > 0
    assert args.fps > 0

    acceleration = args.acceleration
    resolution = args.resolution
    count_frames = args.count_frames
    duration = args.duration
    fps = args.fps

    assert args.radius * 2 <= resolution[0] and \
           args.radius * 2 <= resolution[1] and \
           "Ball is larger than the resolution of the image."

    assert args.starting_height - args.radius > 0 and 'Ball cannot start below or on the ground.'

    if args.starting_height + args.radius > resolution[1]:
        print("WARNING: Inputted starting_height plus ball radius is greater than the height of the window.")

    balls = []
    if args.additional_ball:
        new_args = get_input('Input new arguments as before (formatted \": --color ...\"): ').strip().split(' ')
        if new_args[0] == '':
            new_args = []

        balls = parse_ball_args(new_args, resolution)

    ball = {
        'color': args.color,
        'starting_height': args.starting_height,
        'radius': args.radius,
        'deformation': args.deformation
    }

    output_args = {
        'balls': [ball] + balls,
        'acceleration': acceleration,
        'resolution': resolution,
        'count_frames': count_frames,
        'duration': duration,
        'fps': fps
    }

    return output_args


def get_input(text):
    return input(text)


def parse_ball_args(args, resolution):
    parser = argparse.ArgumentParser()

    parser.add_argument('--color', dest='color', nargs="+", type=int, default=[255, 255, 255],
                        help='Color of the ball in RGB. Separate values by spaces (--color 255 255 255)')
    parser.add_argument('--starting_height', dest='starting_height', type=float, default=400.,
                        help='Starting height of the ball in pixels.')
    parser.add_argument('--radius', dest='radius', type=float, default=20.,
                        help='Radius of the ball in pixels. Ball must be able to fit within given window.')
    parser.add_argument('--deformation', dest='deformation', type=float, default=0.0,
                        help='Deformation of the ball, between 0 and 1. 0 is no deformation, 1 is the most.')
    parser.add_argument('--additional_ball', dest='additional_ball', action='store_true',
                        help='Input values for another ball after this one.')

    args = parser.parse_args(args)

    assert len(args.color) == 3
    assert 0 <= args.color[0] <= 255 and 0 <= args.color[1] <= 255 and 0 <= args.color[2] <= 255
    assert args.radius > 0.5
    assert args.starting_height > 0
    assert 0 <= args.deformation <= 1

    assert args.radius * 2 <= resolution[0] and \
           args.radius * 2 <= resolution[1] and \
           "Ball is larger than the resolution of the image."

    if args.starting_height + args.radius > resolution[1]:
        print("WARNING: Inputted starting_height plus ball radius is greater than the height of the window.")

    balls = []
    if args.additional_ball:
        new_args = get_input('Input new arguments as before (formatted \": --color ...\"): ').strip().split(' ')
        if new_args[0] == '':
            new_args = []

        balls = parse_ball_args(new_args, resolution)

    ball = {
        'color': args.color,
        'starting_height': args.starting_height,
        'radius': args.radius,
        'deformation': args.deformation
    }
    balls.insert(0, ball)

    return balls


if __name__ == "__main__":
    main()
