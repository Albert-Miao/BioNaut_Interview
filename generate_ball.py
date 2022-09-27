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
        assert ball_attr['radius'] >= 1

        assert type(ball_attr['starting_height']) is float or type(ball_attr['starting_height']) is int
        assert ball_attr['starting_height'] > 0

        assert type(ball_attr['deformation'] is float or type(ball_attr['deformation'] is int))
        assert 0 <= ball_attr['deformation'] <= 1

        self.color = ball_attr['color']
        self.radius = ball_attr['radius']
        self.deformation = ball_attr['deformation']

        self.hor_vel = ball_attr['hor_vel']
        self.ver_vel = 0
        self.deformation_acceleration = -1

        self.x = self.radius
        self.y = ball_attr['starting_height']

    def nextFrame(self, acceleration, step):

        # Check to see if ball is not in impact
        if self.y > self.radius or (self.y == self.radius and self.ver_vel > 0):
            # Predict change in y
            y_delta = self.ver_vel * step + (1 / 2) * acceleration * (step ** 2)
            # Impact occurs when the expected y is below the ground:
            if self.y + y_delta <= self.radius:

                # Determine impact speed
                vel_dir = np.sign(self.ver_vel)
                impact_vel = vel_dir * (((self.ver_vel ** 2) +
                                         vel_dir * 2 * acceleration * (self.y - self.radius)) ** (1 / 2))

                # Determine length of time til impact and set x and y accordingly.
                curr_step = (impact_vel - self.ver_vel) / acceleration
                self.x += curr_step * self.hor_vel
                self.y = self.radius

                # If there is deformation to the ball, determine the resulting acceleration of the center position from
                # impact speed and the given deformation constant.
                if self.deformation != 0:
                    self.deformation_acceleration = (impact_vel ** 2) / (2 * (self.radius - 1))
                    self.deformation_acceleration = self.deformation_acceleration / self.deformation

                    self.ver_vel = impact_vel

                    # Calculate the remainder of the timestep.
                    return self.nextFrame(acceleration, step - curr_step)

                # If there is no deformation, calculate the remainder of the timestep after the vertical velocity is
                # completely reversed.
                self.ver_vel = -impact_vel
                return self.nextFrame(acceleration, step - curr_step)[0], True

            # If no expected impact, predict values as normal.
            self.x += step * self.hor_vel
            self.y += y_delta
            self.ver_vel += acceleration * step

        # If in the middle of impact, make calculations as per deformation_acceleration.
        else:
            y_delta = self.ver_vel * step + (1 / 2) * self.deformation_acceleration * (step ** 2)

            # If leaving impact, calculate rest with gravity acceleration.
            if self.y + y_delta >= self.radius:
                escape_vel = (self.ver_vel ** 2 + 2 * self.deformation_acceleration * (self.radius - self.y)) ** (1 / 2)
                curr_step = (escape_vel - self.ver_vel) / self.deformation_acceleration

                self.x += curr_step * self.hor_vel
                self.y = self.radius
                self.ver_vel = escape_vel
                return self.nextFrame(acceleration, step - curr_step)[0], True

            # If not leaving impact, predict values with deformation_acceleration.
            self.x += step * self.hor_vel
            self.y += y_delta
            self.ver_vel += self.deformation_acceleration * step

        minor = min(self.y, self.radius)
        major = (self.radius ** 2) / minor

        ball_info = {
            'x': self.x,
            'y': self.y,
            'major': major,
            'minor': minor,
            'color': self.color
        }

        return ball_info, False


# Create a separate BallManager class because there are many attributes that are shared between balls, thus making it
# redundant in the Ball class, that are also relevant to trajectory calculation, making it different from the
# ScreenWriter class.
class BallManager:
    # Initializes BallManager with duration in either number of frames or bounces, a boolean determining whether to
    # count by bounces or frames, and acceleration.
    #
    # acceleration should be a positive value.
    # duration should a positive integer regardless of frames or bounces.
    # count_frames = True when counting bounces, False when counting frames.
    # fps is a positive integer
    def __init__(self, acceleration, duration, count_frames, fps, balls=None):
        if balls is None:
            balls = []

        assert type(acceleration) is float or type(acceleration) is int
        assert acceleration > 0

        assert type(count_frames) is bool
        assert type(duration) is int

        self.acceleration = acceleration
        self.count_frames = count_frames
        if self.count_frames:
            self.max_frames = duration
            self.curr_frames = 0
        else:
            self.max_bounces = duration
            self.curr_bounces = [0] * len(balls)

        self.fps = fps
        self.balls = balls

    def nextFrame(self):
        balls_info = []
        finished = False

        # If counting frames, return finished if max_frames is surpassed.
        if self.count_frames:
            self.curr_frames += 1
            if self.curr_frames >= self.max_frames:
                finished = True

        # Iterate though each ball and store info.
        for i, ball in enumerate(self.balls):
            ball_info, bounced = ball.nextFrame(-self.acceleration, 1 / self.fps)
            balls_info.append(ball_info)

            # If the ball bounced in the last frame, record it, and then return finished when a ball that has reached
            # max bounces reaches its peak.
            if not self.count_frames and bounced:
                self.curr_bounces[i] += 1
            if not self.count_frames and self.curr_bounces[i] >= self.max_bounces and self.balls[i].ver_vel < 0:
                finished = True

        return balls_info, finished


class ScreenWriter:
    # Initializes ScreenWriter. Only takes in resolution, a 2-dim tuple of positive integers, and fps, a positive
    # integer.
    def __init__(self, resolution, fps, title='test.avi'):
        assert (type(resolution) is list or type(resolution) is tuple) and len(resolution) == 2
        assert type(resolution[0]) is int and type(resolution[1]) is int
        assert resolution[0] > 0 and resolution[1] > 0

        assert type(fps) is int and fps > 0

        self.resolution = resolution
        self.curr_display = np.zeros((resolution[0], resolution[1], 3))
        self.fps = fps
        self.imgs = []

        self.writer = cv2.VideoWriter(title, cv2.VideoWriter_fourcc(*'DIVX'), fps, resolution)
        return

    def generate_image(self, balls_info):
        self.curr_display = np.zeros((self.resolution[1], self.resolution[0], 3))
        for ball in balls_info:
            self.curr_display = cv2.ellipse(self.curr_display,
                                            np.round((ball['x'], self.resolution[1] - ball['y'])).astype('uint32'),
                                            np.round((ball['major'], ball['minor'])).astype('uint32'),
                                            0, 0, 360, ball['color'], thickness=-1)

        # Memory error, going to need to presave imgs.
        # self.imgs.append(self.curr_display)
        return self.curr_display


# DONE: creates argparse object and passes to parse_args function
# DONE: creates Ball object to be run, initialized with core args
# DONE: creates BallManager object with all relevant balls.
# DONE: creates ScreenWriter object, initialized with core args
# DONE: Predict horizontal scale
# DONE: For however long the video lasts, grab the next frame from Ball with something like nextFrame().
#       Probably returns info of position, color, major and minor axis.
# NEED: Store the relevant info of Ball at each frame until end.
# NEED: Pass relevant info to ScreenWriter and append result to images list
# NEED: Save images.


def main():
    args = parse_args(sys.argv[1:])
    ball_args = args['balls']
    print('Number of balls: ' + str(len(ball_args)))

    ball_args = get_horizontal_scale(ball_args, args)
    print(ball_args)

    # Initialize balls, manager, and screenwriter
    balls = []
    for ball_arg in ball_args:
        balls.append(Ball(ball_arg))

    manager = BallManager(args['acceleration'], args['duration'], args['count_frames'], args['fps'], balls)
    screenwriter = ScreenWriter(args['resolution'], args['fps'], args['title'])

    finished = False
    count = 0
    while not finished:
        count += 1
        print(count)
        test, finished = manager.nextFrame()
        img = screenwriter.generate_image(test)


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--color', dest='color', nargs="+", type=int, default=[255, 255, 255],
                        help='Color of the ball in RGB. Separate values by spaces (--color 255 255 255)')
    parser.add_argument('--starting_height', dest='starting_height', type=float, default=400.,
                        help='Starting height of the ball in pixels.')
    parser.add_argument('--radius', dest='radius', type=float, default=20.,
                        help='Radius of the ball in pixels. Ball must be able to fit within given window.')
    parser.add_argument('--deformation', dest='deformation', type=float, default=0.3,
                        help='Deformation of the ball, between 0 and 1. 0 is no deformation, 1 is the most.')

    parser.add_argument('--count_frames', dest='count_frames', action='store_true',
                        help='Whether to determine video length by number of frames. If not, determined by number of '
                             'bounces.')
    parser.add_argument('--duration', dest='duration', type=int, default=5,
                        help='If --count_frames, number of frames, else number of bounces.')
    parser.add_argument('--acceleration', dest='acceleration', type=float, default=9.81,
                        help='Acceleration due to gravity in pixels/seconds^2. Must be positive (above 0).')
    parser.add_argument('--resolution', dest='resolution', nargs="+", type=int, default=[640, 480],
                        help='Resolution of video. Must be 2-dim tuple of positive integers.')
    parser.add_argument('--fps', dest='fps', type=int, default=30,
                        help='Frames per second.')
    parser.add_argument('--title', dest='title', type=str, default='test.avi',
                        help='Title of the video. Make ending ".avi".')
    parser.add_argument('--additional_ball', dest='additional_ball', action='store_true',
                        help='Input values for another ball after this one.')

    args = parser.parse_args(args)

    assert len(args.color) == 3
    assert 0 <= args.color[0] <= 255 and 0 <= args.color[1] <= 255 and 0 <= args.color[2] <= 255
    assert args.radius >= 1
    assert args.starting_height > 0
    assert 0 <= args.deformation <= 1

    assert args.duration > 0
    assert args.acceleration > 0
    assert len(args.resolution) == 2
    assert args.resolution[0] > 0 and args.resolution[1] > 0
    assert args.title[-4:] == '.avi' and "Ending is not '.avi'"
    assert args.fps > 0

    acceleration = args.acceleration
    resolution = args.resolution
    count_frames = args.count_frames
    duration = args.duration
    fps = args.fps
    title = args.title

    assert args.radius * 2 <= resolution[0] and \
           args.radius * 2 <= resolution[1] and \
           "Ball is larger than the resolution of the image."

    assert args.starting_height - args.radius > 0 and 'Ball cannot start below or on the ground.'
    assert fps > (args.starting_height * 2 / acceleration) * (-1 / 2) and \
           "Ball falls too quickly to the ground for the given fps."

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
        'fps': fps,
        'title': title,
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


# Function to determine the best horizontal velocity of balls. Aims to make sure the ball travels the entirety of the
# screen. Does so by predicting the amount of time for the video to complete. Easy when counting frames, hard when
# counting bounces due to the impact acceleration detection.
#
# ball_args: list of arguments dictionaries for each ball, as formatted in parse_args.
# args: argument dictionaries for totality of video, as formatted in parse_args.
def get_horizontal_scale(ball_args, args):

    # Since every ball has the same horizontal velocity, the ball with the largest radius will travel the least
    # since we're trying to make the ball go from edge to edge of the screen.
    ball_rads = [ball['radius'] for ball in ball_args]
    largest_rad = max(ball_rads)

    # Predict horizontal scale of frames by determining distance traveled per second (fps / duration)
    if args['count_frames']:
        horizontal_vel = (args['resolution'][0] - 2 * largest_rad) * args['fps'] / args['duration']
        for ball in ball_args:
            ball['hor_vel'] = horizontal_vel
    # Predicting horizontal scale in bounces is much harder. Find the time from starting height to the flattest possible
    # ball. The quickest time will bounce the most, so calculate time assuming that ball.
    else:
        min_time = np.Inf
        for ball in ball_args:
            fall_time = ((ball['starting_height'] - ball['radius']) * 2 / args['acceleration']) ** (1/2)

            if ball['deformation'] == 0:
                if min_time > fall_time * args['duration'] * 2:
                    min_time = fall_time * args['duration'] * 2
                continue

            impact_vel = fall_time * args['acceleration']
            deformation_acceleration = (impact_vel ** 2) / (2 * (ball['radius'] - 1))
            deformation_acceleration = deformation_acceleration / ball['deformation']
            deform_time = impact_vel / deformation_acceleration

            if min_time > (fall_time + deform_time) * args['duration'] * 2:
                min_time = (fall_time + deform_time) * args['duration'] * 2

        horizontal_vel = (args['resolution'][0] - 2 * largest_rad) / min_time
        for ball in ball_args:
            ball['hor_vel'] = horizontal_vel

    return ball_args


if __name__ == "__main__":
    main()
