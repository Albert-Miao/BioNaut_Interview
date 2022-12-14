from generate_ball import *

import unittest
from unittest.mock import patch

import numpy as np


class TestBallMethods(unittest.TestCase):
    def test_init(self):
        ball_attr = {
            'color': [127, 100, 156],
            'radius': 10,
            'starting_height': 300,
            'deformation': 0,
            'hor_vel': 20
        }

        ball = Ball(ball_attr)

        self.assertTrue(ball.color[0] == 127 and ball.color[1] == 100 and ball.color[2] == 156)
        self.assertTrue(ball.radius == 10)
        self.assertTrue(ball.x == 10)
        self.assertTrue(ball.y == 300)
        self.assertTrue(ball.deformation == 0)
        self.assertTrue(ball.deformation_acceleration == -1)

        self.assertTrue(hasattr(ball, 'hor_vel'))
        self.assertTrue(hasattr(ball, 'ver_vel'))
        self.assertTrue(ball.hor_vel == 20)
        self.assertTrue(ball.ver_vel == 0)

    def test_get_info(self):
        ball_attr = {
            'color': [127, 100, 156],
            'radius': 10,
            'starting_height': 300,
            'deformation': 0,
            'hor_vel': 20
        }

        info = Ball(ball_attr).get_info()
        self.assertTrue(info['x'] == 10)
        self.assertTrue(info['y'] == 300)
        self.assertTrue(info['major'] == 10 and info['minor'] == 10)
        self.assertTrue(info['color'][0] == 127 and info['color'][1] == 100 and info['color'][2] == 156)


class TestBallManagerMethods(unittest.TestCase):
    def test_init1(self):
        manager = BallManager(9.81, 5, False, fps=60)

        self.assertTrue(manager.acceleration == 9.81)
        self.assertFalse(manager.count_frames)

        self.assertTrue(hasattr(manager, 'max_bounces'))
        self.assertTrue(hasattr(manager, 'curr_bounces'))
        self.assertFalse(hasattr(manager, 'max_frames') or hasattr(manager, 'curr_frames'))
        self.assertTrue(manager.max_bounces == 5)
        self.assertTrue(len(manager.balls) == 0)

    def test_init2(self):
        ball_attr1 = {
            'color': [127, 100, 156],
            'radius': 10,
            'starting_height': 300,
            'deformation': 0,
            'hor_vel': 20
        }

        ball_attr2 = {
            'color': [1, 2, 3],
            'radius': 5,
            'starting_height': 100,
            'deformation': 0.4,
            'hor_vel': 10
        }

        balls = [Ball(ball_attr1), Ball(ball_attr2)]

        manager = BallManager(9.81, 5, False, 60, balls)

        self.assertTrue(manager.balls[0].color[0] == 127 and
                        manager.balls[0].color[1] == 100 and
                        manager.balls[0].color[2] == 156)
        self.assertTrue(manager.balls[0].radius == 10)
        self.assertTrue(manager.balls[0].x == 10)
        self.assertTrue(manager.balls[0].y == 300)
        self.assertTrue(manager.balls[0].deformation == 0)
        self.assertTrue(manager.balls[0].deformation_acceleration == -1)

        self.assertTrue(manager.balls[1].color[0] == 1 and
                        manager.balls[1].color[1] == 2 and
                        manager.balls[1].color[2] == 3)
        self.assertTrue(manager.balls[1].radius == 5)
        self.assertTrue(manager.balls[1].x == 5)
        self.assertTrue(manager.balls[1].y == 100)
        self.assertTrue(manager.balls[1].deformation == 0.4)
        self.assertTrue(manager.balls[1].deformation_acceleration == -1)

    def test_get_info(self):
        ball_attr1 = {
            'color': [127, 100, 156],
            'radius': 10,
            'starting_height': 300,
            'deformation': 0,
            'hor_vel': 20
        }

        ball_attr2 = {
            'color': [1, 2, 3],
            'radius': 5,
            'starting_height': 100,
            'deformation': 0.4,
            'hor_vel': 10
        }

        balls = [Ball(ball_attr1), Ball(ball_attr2)]

        manager = BallManager(9.81, 5, False, 60, balls)
        info = manager.get_info()

        self.assertTrue(info[0]['x'] == 10)
        self.assertTrue(info[0]['y'] == 300)
        self.assertTrue(info[0]['major'] == 10 and info[0]['minor'] == 10)
        self.assertTrue(info[0]['color'][0] == 127 and info[0]['color'][1] == 100 and info[0]['color'][2] == 156)

        self.assertTrue(info[1]['x'] == 5)
        self.assertTrue(info[1]['y'] == 100)
        self.assertTrue(info[1]['major'] == 5 and info[1]['minor'] == 5)
        self.assertTrue(info[1]['color'][0] == 1 and info[1]['color'][1] == 2 and info[1]['color'][2] == 3)


class TestScreenWriterMethods(unittest.TestCase):
    def test_init(self):
        screenwriter = ScreenWriter((100, 100, 100), (1280, 720), 60.)

        self.assertTrue(screenwriter.bg_color[0] == 100 and
                        screenwriter.bg_color[1] == 100 and
                        screenwriter.bg_color[2] == 100)
        self.assertTrue(screenwriter.resolution[0] == 1280 and screenwriter.resolution[1] == 720)
        self.assertTrue(screenwriter.fps == 60)

        test_display = np.zeros((720, 1280, 3))
        test_display[:] = (100, 100, 100)
        self.assertTrue(np.all(screenwriter.curr_display == test_display))

        self.assertTrue(len(screenwriter.imgs) == 0)
        self.assertTrue(type(screenwriter.writer) == cv2.VideoWriter)


class TestHelperMethods(unittest.TestCase):
    def test_parse_args1(self):
        args = parse_args(['--color', '128', '0', '64',
                           '--count_frames',
                           '--duration', '600',
                           '--acceleration', '12',
                           '--deformation', '0.45',
                           '--resolution', '1920', '1080',
                           '--background_color', '15', '20', '25',
                           '--starting_height', '800',
                           '--radius', '200',
                           '--fps', '60',
                           '--title', 'bounce.avi'])
        balls = args['balls']
        self.assertTrue(balls[0]['color'][0] == 128 and balls[0]['color'][1] == 0 and balls[0]['color'][2] == 64)
        self.assertTrue(balls[0]['starting_height'] == 800)
        self.assertTrue(balls[0]['radius'] == 200)
        self.assertTrue(balls[0]['deformation'] == 0.45)

        self.assertTrue(args['count_frames'])
        self.assertTrue(args['duration'] == 600)
        self.assertTrue(args['acceleration'] == 12)
        self.assertTrue(args['resolution'][0] == 1920 and args['resolution'][1] == 1080)
        self.assertTrue(args['fps'] == 60)
        self.assertTrue(args['title'] == 'bounce.avi')
        self.assertTrue(args['background_color'][0] == 15 and
                        args['background_color'][1] == 20 and
                        args['background_color'][2] == 25)

    def test_parse_args2(self):
        self.assertRaises(AssertionError,
                          parse_args, ['--color', '128', '0', '64',
                                       '--count_frames',
                                       '--duration', '600',
                                       '--acceleration', '12',
                                       '--deformation', '0.45',
                                       '--resolution', '1920', '1080',
                                       '--starting_height', '800',
                                       '--radius', '600',
                                       '--fps', '60'])

    def test_parse_args3(self):
        self.assertRaises(AssertionError,
                          parse_args, ['--color', '128', '0', '64',
                                       '--count_frames',
                                       '--duration', '600',
                                       '--acceleration', '50',
                                       '--deformation', '0.45',
                                       '--resolution', '1920', '1080',
                                       '--starting_height', '10',
                                       '--radius', '200',
                                       '--fps', '1'])

    @patch('generate_ball.get_input', return_value='--color 1 2 3 --starting_height 400 --radius 40 --deformation 0.2')
    def test_parse_args4(self, input):
        args = parse_args(['--color', '128', '0', '64',
                           '--count_frames',
                           '--duration', '600',
                           '--acceleration', '12',
                           '--deformation', '0.45',
                           '--resolution', '1920', '1080',
                           '--starting_height', '800',
                           '--radius', '200',
                           '--fps', '60',
                           '--additional_ball'])

        balls = args['balls']

        self.assertTrue(balls[0]['color'][0] == 128 and balls[0]['color'][1] == 0 and balls[0]['color'][2] == 64)
        self.assertTrue(balls[0]['starting_height'] == 800)
        self.assertTrue(balls[0]['radius'] == 200)
        self.assertTrue(balls[0]['deformation'] == 0.45)

        self.assertTrue(balls[1]['color'][0] == 1 and balls[1]['color'][1] == 2 and balls[1]['color'][2] == 3)
        self.assertTrue(balls[1]['starting_height'] == 400)
        self.assertTrue(balls[1]['radius'] == 40)
        self.assertTrue(balls[1]['deformation'] == 0.2)

        self.assertTrue(args['count_frames'])
        self.assertTrue(args['duration'] == 600)
        self.assertTrue(args['acceleration'] == 12)
        self.assertTrue(args['resolution'][0] == 1920 and args['resolution'][1] == 1080)
        self.assertTrue(args['fps'] == 60)

    @patch('generate_ball.get_input', return_value='')
    def test_parse_args5(self, input):
        args = parse_args(['--color', '128', '0', '64',
                           '--count_frames',
                           '--duration', '600',
                           '--acceleration', '12',
                           '--deformation', '0.45',
                           '--resolution', '1920', '1080',
                           '--starting_height', '800',
                           '--radius', '200',
                           '--fps', '60',
                           '--additional_ball'])

        balls = args['balls']

        self.assertTrue(balls[0]['color'][0] == 128 and balls[0]['color'][1] == 0 and balls[0]['color'][2] == 64)
        self.assertTrue(balls[0]['starting_height'] == 800)
        self.assertTrue(balls[0]['radius'] == 200)
        self.assertTrue(balls[0]['deformation'] == 0.45)

        self.assertTrue(balls[1]['color'][0] == 255 and balls[1]['color'][1] == 255 and balls[1]['color'][2] == 255)
        self.assertTrue(balls[1]['starting_height'] == 600)
        self.assertTrue(balls[1]['radius'] == 20)
        self.assertTrue(balls[1]['deformation'] == 0.5)

        self.assertTrue(args['count_frames'])
        self.assertTrue(args['duration'] == 600)
        self.assertTrue(args['acceleration'] == 12)
        self.assertTrue(args['resolution'][0] == 1920 and args['resolution'][1] == 1080)
        self.assertTrue(args['fps'] == 60)

    def test_get_horizontal_scale1(self):
        ball_args = [
            {
                'color': [127, 100, 156],
                'radius': 10,
                'starting_height': 300,
                'deformation': 0,
            }, {
                'color': [1, 2, 3],
                'radius': 5,
                'starting_height': 100,
                'deformation': 0.4,
            }
        ]

        args = {
            'count_frames': False,
            'duration': 5,
            'acceleration': 9.81,
            'resolution': [1920, 1080],
            'fps': 60
        }

        ball_args = get_horizontal_scale(ball_args, args)
        self.assertTrue(42 < ball_args[0]['hor_vel'] < 43)

    def test_get_horizontal_scale2(self):
        ball_args = [
            {
                'color': [127, 100, 156],
                'radius': 10,
                'starting_height': 300,
                'deformation': 0,
            }, {
                'color': [1, 2, 3],
                'radius': 5,
                'starting_height': 100,
                'deformation': 0.4,
            }
        ]

        args = {
            'count_frames': True,
            'duration': 600,
            'acceleration': 9.81,
            'resolution': [1920, 1080],
            'fps': 60
        }

        ball_args = get_horizontal_scale(ball_args, args)
        self.assertTrue(189 < ball_args[0]['hor_vel'] < 191)


if __name__ == '__main__':
    unittest.main()
