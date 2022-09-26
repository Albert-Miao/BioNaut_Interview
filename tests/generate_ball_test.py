from generate_ball import *

import unittest
from unittest.mock import patch

import numpy as np


class TestBallMethods(unittest.TestCase):
    def test_init(self):
        ball_attr = {
            'color': [127, 100, 156],
            'radius': 10,
            'starting_height': 300
        }

        ball = Ball(ball_attr)

        self.assertTrue(ball.color[0] == 127 and ball.color[1] == 100 and ball.color[2] == 156)
        self.assertTrue(ball.radius == 10)
        self.assertTrue(ball.height == 300)

        self.assertTrue(hasattr(ball, 'hor_vel'))
        self.assertTrue(hasattr(ball, 'ver_vel'))
        self.assertTrue(ball.hor_vel == PRE_SCALED_HOR_VEL)
        self.assertTrue(ball.ver_vel == 0)


class TestBallManagerMethods(unittest.TestCase):
    def test_init1(self):
        manager = BallManager(9.81, 5, False, fps=60)

        self.assertTrue(manager.acceleration == 9.81)
        self.assertFalse(manager.count_bounces)

        self.assertTrue(hasattr(manager, 'max_bounces'))
        self.assertTrue(hasattr(manager, 'curr_bounces'))
        self.assertFalse(hasattr(manager, 'max_frames') or hasattr(manager, 'curr_frames'))
        self.assertTrue(manager.max_bounces == 5)
        self.assertTrue(len(manager.balls) == 0)

    def test_init2(self):
        ball_attr1 = {
            'color': [127, 100, 156],
            'radius': 10,
            'starting_height': 300
        }

        ball_attr2 = {
            'color': [1, 2, 3],
            'radius': 5,
            'starting_height': 100
        }

        balls = [Ball(ball_attr1), Ball(ball_attr2)]

        manager = BallManager(9.81, 5, False, 60, balls)

        self.assertTrue(manager.balls[0].color[0] == 127 and
                        manager.balls[0].color[1] == 100 and
                        manager.balls[0].color[2] == 156)
        self.assertTrue(manager.balls[0].radius == 10)
        self.assertTrue(manager.balls[0].height == 300)

        self.assertTrue(manager.balls[1].color[0] == 1 and
                        manager.balls[1].color[1] == 2 and
                        manager.balls[1].color[2] == 3)
        self.assertTrue(manager.balls[1].radius == 5)
        self.assertTrue(manager.balls[1].height == 100)



class TestScreenWriterMethods(unittest.TestCase):
    def test_init(self):
        screenwriter = ScreenWriter((1280, 720))

        self.assertTrue(screenwriter.resolution[0] == 1280 and screenwriter.resolution[1] == 720)
        test_display = np.zeros((1280, 720, 3))
        self.assertTrue(np.all(screenwriter.curr_display == test_display))


class TestHelperMethods(unittest.TestCase):
    def test_parse_args1(self):
        args = parse_args(['--color', '128', '0', '64',
                           '--count_frames',
                           '--duration', '600',
                           '--acceleration', '12',
                           '--resolution', '1920', '1080',
                           '--starting_height', '800',
                           '--radius', '200',
                           '--fps', '60'])
        balls = args['balls']
        self.assertTrue(balls[0]['color'][0] == 128 and balls[0]['color'][1] == 0 and balls[0]['color'][2] == 64)
        self.assertTrue(balls[0]['starting_height'] == 800)
        self.assertTrue(balls[0]['radius'] == 200)

        self.assertTrue(args['count_frames'])
        self.assertTrue(args['duration'] == 600)
        self.assertTrue(args['resolution'][0] == 1920 and args['resolution'][1] == 1080)
        self.assertTrue(args['fps'] == 60)

    def test_parse_args2(self):
        self.assertRaises(AssertionError,
                          parse_args, ['--color', '128', '0', '64',
                                       '--count_frames',
                                       '--duration', '600',
                                       '--acceleration', '12',
                                       '--resolution', '1920', '1080',
                                       '--starting_height', '800',
                                       '--radius', '600',
                                       '--fps', '60'])

    @patch('generate_ball.get_input', return_value='--color 1 2 3 --starting_height 400 --radius 40')
    def test_parse_args3(self, input):
        args = parse_args(['--color', '128', '0', '64',
                           '--count_frames',
                           '--duration', '600',
                           '--acceleration', '12',
                           '--resolution', '1920', '1080',
                           '--starting_height', '800',
                           '--radius', '200',
                           '--fps', '60',
                           '--additional_ball'])

        balls = args['balls']

        self.assertTrue(balls[0]['color'][0] == 128 and balls[0]['color'][1] == 0 and balls[0]['color'][2] == 64)
        self.assertTrue(balls[0]['starting_height'] == 800)
        self.assertTrue(balls[0]['radius'] == 200)

        self.assertTrue(balls[1]['color'][0] == 1 and balls[1]['color'][1] == 2 and balls[1]['color'][2] == 3)
        self.assertTrue(balls[1]['starting_height'] == 400)
        self.assertTrue(balls[1]['radius'] == 40)

        self.assertTrue(args['count_frames'])
        self.assertTrue(args['duration'] == 600)
        self.assertTrue(args['resolution'][0] == 1920 and args['resolution'][1] == 1080)
        self.assertTrue(args['fps'] == 60)

    @patch('generate_ball.get_input', return_value='')
    def test_parse_args4(self, input):
        args = parse_args(['--color', '128', '0', '64',
                           '--count_frames',
                           '--duration', '600',
                           '--acceleration', '12',
                           '--resolution', '1920', '1080',
                           '--starting_height', '800',
                           '--radius', '200',
                           '--fps', '60',
                           '--additional_ball'])

        balls = args['balls']

        self.assertTrue(balls[0]['color'][0] == 128 and balls[0]['color'][1] == 0 and balls[0]['color'][2] == 64)
        self.assertTrue(balls[0]['starting_height'] == 800)
        self.assertTrue(balls[0]['radius'] == 200)

        self.assertTrue(balls[1]['color'][0] == 255 and balls[1]['color'][1] == 255 and balls[1]['color'][2] == 255)
        self.assertTrue(balls[1]['starting_height'] == 400)
        self.assertTrue(balls[1]['radius'] == 20)

        self.assertTrue(args['count_frames'])
        self.assertTrue(args['duration'] == 600)
        self.assertTrue(args['resolution'][0] == 1920 and args['resolution'][1] == 1080)
        self.assertTrue(args['fps'] == 60)


if __name__ == '__main__':
    unittest.main()
