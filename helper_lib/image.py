from __future__ import division

import numpy as np
from skimage import morphology as morph
from skimage.measure import label as lbl
from skimage.filters import threshold_otsu
from scipy import ndimage


def unify_shape(x, y):
    """
    Pads the two given arrays to bring them to the same shape.

    Parameters
    ----------
    x, y : ndarray
        Input arrays

    Returns
    -------
    x, y : ndarray
        Modified input arrays having the same shape.
    """
    if len(x.shape) != len(y.shape):
        raise ValueError("The number of dimensions in the two arrays must be equal!")
    nshape = np.array([x.shape, y.shape]).max(0) + 2
    n = (nshape - np.array(x.shape))
    pad_width = []
    for i in range(len(n)):
        pad_width.append((int(n[i] / 2), n[i] - int(n[i] / 2)))
    x = np.pad(x, pad_width=pad_width, mode='constant', constant_values=0)
    pad_width = []
    n = (nshape - np.array(y.shape))
    for i in range(len(n)):
        pad_width.append((int(n[i] / 2), n[i] - int(n[i] / 2)))
    y = np.pad(y, pad_width=pad_width, mode='constant', constant_values=0)

    return x, y


def segment(img, thr=None, relative_thr=False, median=None, gaussian=None,
            morphology=False, fill_holes=False, label=False):
    """
    Segments the input image with given settings for pre- and post-processing.

    Parameters
    ----------
    img : ndarray
        Input image.
    thr : scalar, optional
        Threshold value for image segmentation.
        If None, automatic Otsu threshold will be computed.
        Default is None.
    relative_thr : bool, optional
        If True, the value of `thr` is multiplied by the maximum intensity of the image.
        Default is False.
    median : int, optional
        Size of the median filter for preprocessing.
        If None, median filter will not be applied.
        Default is None.
    gaussian : int, optional
        Standard deviation of the Gaussian filter for preprocessing.
        If None, Gaussian filter will not be applied.
        Default is None.
    morphology : bool, optional
        If True, morphological opening and closing will be done after thresholding.
        Default is False.
    fill_holes : bool, optional
        If True, binary holes filling will be done after thresholding.
        Default is False.
    label : bool, optional
        If True, connected region will be labeled by unique labels.
        Default is True.

    Returns
    -------
    ndarray
        Segmented image of the same shape as 'img'
    """

    if np.max(img) > 0:
        if median is not None:
            img = ndimage.median_filter(img, median)
        if gaussian is not None:
            img = ndimage.gaussian_filter(img, gaussian)
        if thr is None:
            thr = threshold_otsu(img)
        else:
            if relative_thr:
                thr = thr*np.max(img)

        mask = (img > thr)*1.

        if morphology:
            mask = morph.opening(mask)
            mask = morph.closing(mask)

        if fill_holes:
            mask = ndimage.binary_fill_holes(mask)

        if label is True:
            mask = lbl(mask)
    else:
        mask = img

    return mask
