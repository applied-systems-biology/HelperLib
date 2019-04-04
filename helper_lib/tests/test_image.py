import unittest

from ddt import ddt, data
import numpy as np
from scipy import ndimage

from helper_lib.image import unify_shape, segment


@ddt
class TestUnifyshape(unittest.TestCase):

    @data(
        (np.ones([10, 40]), np.zeros([30, 30]))
    )
    def test_extensions(self, case):
        image1, image2 = case
        image1, image2 = unify_shape(image1, image2)
        self.assertEqual(image1.shape, image2.shape)
        self.assertEqual(tuple(np.unique(image1)), (0, 1))
        self.assertEqual(tuple(np.unique(image2)), tuple([0]))

    @data(
        (np.array([[[0, 0, 2, 5],
                    [0, 0, 0, 0],
                    [10, 0, 0, 0]],
                  [[0, 0, 1, 1],
                   [0, 0, 0, 0],
                   [2, 0, 0, 5]],
                  [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [15, 2, 0, 0]]]
                  ), 2)
    )
    def test_segmentation_preprocess(self, case):
        img, num = case
        img = segment(img, thr=0, median=3, label=True)
        self.assertEqual(len(np.unique(img)) - 1, num)

    @data(
        (np.array([[[0, 0, 2, 5],
                    [0, 0, 1, 0],
                    [10, 0, 0, 0]],
                  [[0, 0, 1, 1],
                   [0, 0, 0, 0],
                   [2, 0, 0, 0]],
                  [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [15, 2, 0, 0]]]
                  ), 2, [4, 5]),
        (np.array([[[0, 0, 2, 5],
                    [0, 0, 0, 0],
                    [10, 0, 0, 0]],
                  [[0, 0, 1, 1],
                   [0, 0, 0, 0],
                   [2, 0, 0, 5]],
                  [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [15, 2, 0, 0]]]
                  ), 3, [4, 4, 1])
    )
    def test_segmentation(self, case):
        img, num, sizes = case
        img = segment(img, thr=0, label=True)
        self.assertEqual(len(np.unique(img)) - 1, num)
        sizes.sort()
        cellsizes = list(ndimage.sum(img > 0, img, np.unique(img)[1:]))
        cellsizes.sort()
        self.assertEqual(tuple(cellsizes), tuple(sizes))

    @data(
        (np.array([[[0, 0, 2, 5],
                    [0, 0, 1, 0],
                    [10, 0, 0, 0]],
                  [[0, 0, 1, 1],
                   [0, 0, 0, 0],
                   [2, 0, 0, 0]],
                  [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [15, 2, 0, 0]]]
                  ), 2, [4, 2]),
        (np.array([[[0, 0, 2, 5],
                    [0, 0, 0, 0],
                    [10, 0, 0, 0]],
                  [[0, 0, 1, 1],
                   [0, 0, 0, 0],
                   [2, 0, 0, 5]],
                  [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [15, 2, 0, 0]]]
                  ), 3, [4, 2, 1])
    )
    def test_segmentation_thr1(self, case):
        img, num, sizes = case
        img = segment(img, thr=1, label=True)
        self.assertEqual(len(np.unique(img)) - 1, num)
        sizes.sort()
        cellsizes = list(ndimage.sum(img > 0, img, np.unique(img)[1:]))
        cellsizes.sort()
        self.assertEqual(tuple(cellsizes), tuple(sizes))

if __name__ == '__main__':
    unittest.main()
