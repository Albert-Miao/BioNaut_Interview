from track_ball import *

import unittest


class TestHelperMethods(unittest.TestCase):
    def test_parse_args1(self):
        args = parse_args([
            '--path', '../sample_videos/1.avi',
            '--tolerance', '15',
            '--background_color', '15', '20', '25',
            '--output_dir', 'random_folder',
            '--save_name', 'random.avi'
        ])

        self.assertTrue(args['path'] == '../sample_videos/1.avi')
        self.assertTrue(args['tolerance'] == 15)
        self.assertTrue(args['background_color'][0] == 15 and
                        args['background_color'][1] == 20 and
                        args['background_color'][2] == 25)
        self.assertTrue(args['output_dir'] == 'random_folder')
        self.assertTrue(args['save_name'] == 'random.avi')

    def test_distinct_contours(self):
        img = cv2.imread('contour_test.png')
        contours = distinct_contours(img, 0, [50, 50, 50])

        possible_centers = [(20, 600), (20, 400), (20, 200)]

        self.assertTrue(len(possible_centers) == len(contours))
        for c in contours:
            m = cv2.moments(c)
            cX = int(m["m10"] / m["m00"])
            cY = int(m["m01"] / m["m00"])

            # We have to subtract cY from height because of opencv bottom up image write.
            for center in possible_centers:
                if center[0] - 10 <= cX <= center[0] + 10 and center[1] - 10 <= img.shape[0] - cY <= center[1] + 10:
                    possible_centers.remove(center)

        self.assertFalse(possible_centers)


if __name__ == "__main__":
    unittest.main()
