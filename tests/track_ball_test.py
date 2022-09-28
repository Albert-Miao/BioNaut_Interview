from track_ball import *

import unittest


class TestHelperMethods(unittest.TestCase):
    def test_parse_args1(self):
        args = parse_args([
            '--path', '../sample_videos/test.avi',
            '--tolerance', '15',
            '--output_dir', 'random_folder',
            '--save_name', 'random.avi'
        ])

        self.assertTrue(args['path'] == '../sample_videos/test.avi')
        self.assertTrue(args['tolerance'] == 15)
        self.assertTrue(args['output_dir'] == 'random_folder')
        self.assertTrue(args['save_name'] == 'random.avi')
