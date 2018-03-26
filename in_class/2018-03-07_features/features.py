#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import argparse

import cv2
import numpy as np

def open_image(image_filename):

    print('Opening:', image_filename)
    im = cv2.imread(image_filename)

    if im is None:
        print('Could not open', image_filename)
        return None, None

    print('Image shape:', im.shape)

    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    return im, im_gray

def main():
    image_filename = '../construction_barrel.png'

    im_bgr, im_gray = open_image(image_filename)

    sift = cv2.xfeatures2d.SIFT_create()
    keypoints = sift.detect(im_gray, None)

    im_keypoints = cv2.drawKeypoints(im_bgr, keypoints,
            None,
            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow('Image', im_keypoints)
    cv2.waitKey(0000)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()
