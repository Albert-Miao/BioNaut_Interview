from generate_ball import *

import unittest
from unittest.mock import patch


class TestBallMethods(unittest.TestCase):
    def test_init(self):
        ball = Ball([127, 100, 156], 9.81, 300, 5, False)

        self.assertTrue(ball.color[0] == 127 and ball.color[1] == 100 and ball.color[2] == 156)
        self.assertTrue(ball.acceleration == 9.81)
        self.assertTrue(ball.height == 300)
        self.assertTrue(not ball.count_bounces)

        self.assertTrue(hasattr(ball, 'max_bounces'))
        self.assertTrue(hasattr(ball, 'curr_bounces'))
        self.assertTrue(not hasattr(ball, 'max_frames') and not hasattr(ball, 'curr_frames'))
        self.assertTrue(ball.max_bounces == 5)

        self.assertTrue(hasattr(ball, 'hor_vel'))
        self.assertTrue(hasattr(ball, 'ver_vel'))
        self.assertTrue(ball.hor_vel == PRE_SCALED_HOR_VEL)
        self.assertTrue(ball.ver_vel == 0)


class TestHelperMethods(unittest.TestCase):
    def test_parse_args1(self):
        args = parse_args(['--color', '128', '0', '64',
                           '--count_frames',
                           '--duration', '600',
                           '--acceleration', '12',
                           '--resolution', '1920', '1080',
                           '--starting_height', '800',
                           '--ball_radius', '200',
                           '--fps', '60'])

        self.assertTrue(args[0].color[0] == 128 and args[0].color[1] == 0 and args[0].color[2] == 64)
        self.assertTrue(args[0].count_frames)
        self.assertTrue(args[0].duration == 600)
        self.assertTrue(args[0].resolution[0] == 1920 and args[0].resolution[1] == 1080)
        self.assertTrue(args[0].starting_height == 800)
        self.assertTrue(args[0].ball_radius == 200)
        self.assertTrue(args[0].fps == 60)
        self.assertFalse(args[0].additional_ball)

    def test_parse_args2(self):
        self.assertRaises(AssertionError,
                          parse_args, ['--color', '128', '0', '64',
                                       '--count_frames',
                                       '--duration', '600',
                                       '--acceleration', '12',
                                       '--resolution', '1920', '1080',
                                       '--starting_height', '800',
                                       '--ball_radius', '600',
                                       '--fps', '60'])

    @patch('generate_ball.get_input', return_value='--color 1 2 3 --duration 8 --acceleration 10 --resolution 1280 720 '
                                     '--starting_height 400 --ball_radius 40 --fps 10')
    def test_parse_args3(self, input):
        args = parse_args(['--color', '128', '0', '64',
                           '--count_frames',
                           '--duration', '600',
                           '--acceleration', '12',
                           '--resolution', '1920', '1080',
                           '--starting_height', '800',
                           '--ball_radius', '200',
                           '--fps', '60',
                           '--additional_ball'])

        self.assertTrue(args[0].color[0] == 128 and args[0].color[1] == 0 and args[0].color[2] == 64)
        self.assertTrue(args[0].count_frames)
        self.assertTrue(args[0].duration == 600)
        self.assertTrue(args[0].resolution[0] == 1920 and args[0].resolution[1] == 1080)
        self.assertTrue(args[0].starting_height == 800)
        self.assertTrue(args[0].ball_radius == 200)
        self.assertTrue(args[0].fps == 60)
        self.assertTrue(args[0].additional_ball)

        self.assertTrue(args[1].color[0] == 1 and args[1].color[1] == 2 and args[1].color[2] == 3)
        self.assertFalse(args[1].count_frames)
        self.assertTrue(args[1].duration == 8)
        self.assertTrue(args[1].resolution[0] == 1280 and args[1].resolution[1] == 720)
        self.assertTrue(args[1].starting_height == 400)
        self.assertTrue(args[1].ball_radius == 40)
        self.assertTrue(args[1].fps == 10)
        self.assertFalse(args[1].additional_ball)

    @patch('generate_ball.get_input', return_value='')
    def test_parse_args4(self, input):
        args = parse_args(['--color', '128', '0', '64',
                           '--count_frames',
                           '--duration', '600',
                           '--acceleration', '12',
                           '--resolution', '1920', '1080',
                           '--starting_height', '800',
                           '--ball_radius', '200',
                           '--fps', '60',
                           '--additional_ball'])

        self.assertTrue(args[0].color[0] == 128 and args[0].color[1] == 0 and args[0].color[2] == 64)
        self.assertTrue(args[0].count_frames)
        self.assertTrue(args[0].duration == 600)
        self.assertTrue(args[0].resolution[0] == 1920 and args[0].resolution[1] == 1080)
        self.assertTrue(args[0].starting_height == 800)
        self.assertTrue(args[0].ball_radius == 200)
        self.assertTrue(args[0].fps == 60)
        self.assertTrue(args[0].additional_ball)

        self.assertTrue(args[1].color[0] == 255 and args[1].color[1] == 255 and args[1].color[2] == 255)
        self.assertFalse(args[1].count_frames)
        self.assertTrue(args[1].duration == 3)
        self.assertTrue(args[1].resolution[0] == 640 and args[1].resolution[1] == 480)
        self.assertTrue(args[1].starting_height == 400)
        self.assertTrue(args[1].ball_radius == 20)
        self.assertTrue(args[1].fps == 30)
        self.assertFalse(args[1].additional_ball)
