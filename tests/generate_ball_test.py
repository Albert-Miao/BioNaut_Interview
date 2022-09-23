from generate_ball import *

import unittest


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

        self.assertTrue(args.color[0] == 128 and args.color[1] == 0 and args.color[2] == 64)
        self.assertTrue(args.count_frames)
        self.assertTrue(args.duration == 600)
        self.assertTrue(args.resolution[0] == 1920 and args.resolution[1] == 1080)
        self.assertTrue(args.starting_height == 800)
        self.assertTrue(args.ball_radius == 200)
        self.assertTrue(args.fps == 60)

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
