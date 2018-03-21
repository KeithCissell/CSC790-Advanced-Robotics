#!/usr/bin/env pythno

from __future__ import print_function
from __future__ import division

import argparse
import cv2
from matplotlib import pyplot as plt



def main(args):

  img1 = cv2.imread(args.image1)
  img2 = cv2.imread(args.image2)

  if img1 is None:
    print('Could not open', args.image1)
    return
  if img2 is None:
    print('Could not open', args.image1)
    return

  sift = cv2.xfeatures2d.SIFT_create()

  mask = None
  keypoints1, descriptors1 = sift.detectAndCompute(img1, mask)
  keypoints2, descriptors2 = sift.detectAndCompute(img2, mask)

  bf_matcher = cv2.BFMatcher()

  matches = bf_matcher.knnMatch(descriptors1, descriptors2, k=2)

  good_matches = [[m] for m, n in matches if m.distance < args.factor * n.distance]

  im_matches = cv2.drawMatchesKnn(img1, keypoints1,
                                  img2, keypoints2,
                                  good_matches, None, flags=2)


  # Display Stuff

  plt.figure(1)
  plt.imshow(im_matches)
  plt.show()

  print(matches)



if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Match features in two images.')

  parser.add_argument('image1', type=str, help='Path to first image')
  parser.add_argument('image2', type=str, help='Path to second image')
  parser.add_argument('--factor', type=float, help='Matching factor', default=0.75)

  args = parser.parse_args()

  main(args)