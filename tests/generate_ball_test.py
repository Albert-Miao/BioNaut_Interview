from generate_ball import *

import unittest

class TestBallMethods(unittest.TestCase):
    def test_init(self):
        ball = Ball((127, 100, 156), 9.81, 300, 5, True)
        
        self.assertTrue(ball.color[0] == 127 and ball.color[1] == 100 and ball.color[2] == 156)
        self.assertTrue(ball.acceleration == 9.81)
        self.assertTrue(ball.height == 300)
        self.assertTrue(ball.count_bounces == True)
        
        self.assertTrue(hasattr(ball, 'max_bounces'))
        self.assertTrue(hasattr(ball, 'curr_bounces'))
        self.assertTrue(not hasattr(ball, 'max_frames') and not hasattr(ball, 'curr_frames'))
        self.assertTrue(ball.max_bounces == 5)
        