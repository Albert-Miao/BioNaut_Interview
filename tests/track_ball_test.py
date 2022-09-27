from track_ball import *

import unittest


class TestHelperMethods(unittest.TestCase):
    def test_parse_args1(self):
        args = parse_args([
            '--path', '../sample_videos/1.avi'
        ])

        self.assertTrue(args['path'] == '../sample_videos/1.avi')
