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
    def __init__(self, color, acceleration, starting_height, duration, bounces_or_frames):
        assert type(color) is tuple and len(color) == 3
        assert type(color[0]) is int and type(color[1]) is int and type(color[2]) is int
        assert 0 <= color[0] <= 255 and 0 <= color[1] <= 255 and 0 <= color[2] <= 255

        assert type(acceleration) is float or type(acceleration) is int
        assert acceleration > 0

        assert type(starting_height) is float or type(starting_height) is int
        assert starting_height > 0

        assert type(bounces_or_frames) is bool

        if bounces_or_frames:
            assert type(duration) is int
        else:
            assert type(duration) is int or type(duration) is float

        # Initialize Ball values
        self.color = color
        self.acceleration = acceleration
        self.height = starting_height
        self.count_bounces = bounces_or_frames

        if self.count_bounces:
            self.max_bounces = duration
            self.curr_bounces = 0
        else:
            self.max_frames = duration
            self.curr_frames = 0

        self.hor_vel = PRE_SCALED_HOR_VEL
        self.ver_vel = 0

    def nextFrame(self):
        return tuple()


class ScreenWriter:
    def __init__(self, resolution):
        return

    def generate_image(self):
        return 0


# NEED: creates argparse object and passes to parse_args function
# NEED: creates Ball object to be run, initialized with core args
# NEED: creates ScreenWriter object, initialized with core args
# NEED: For however long the video lasts, grab the next frame from Ball with something like nextFrame().
#       Probably returns info of position, color, major and minor axis.
# NEED: Store the relevant info of Ball at each frame until end.
# NEED: Scale the horizontal distance traveled by Ball to better fit the resolution.
# NEED: Pass relevant info to ScreenWriter and append result to images list
# NEED: Save images.


def main():

    return


if __name__ == "__main__":
    main()
