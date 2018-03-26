#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import argparse
import cv2
from matplotlib import pyplot as plt


def open_image(image_filename, display_seconds):

  # Load Image
  print('Opening:', image_filename)
  img = cv2.imread(image_filename)

  if img is None:
    print('Could not open', image_filename)
    return None

  print('Image shape:', img.shape)

  # Display Image
  if img is not None and display_seconds > 0:
    cv2.imshow('Image', img)
    cv2.waitKey(display_seconds * 1000)
    cv2.destroyAllWindows()

  return img


def display_histograms(img, display_seconds):

  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Display Image
  if display_seconds > 0:
    cv2.imshow('Image', img_gray)
    cv2.waitKey(display_seconds * 1000)
    cv2.destroyAllWindows()

  hist = cv2.calcHist([img_gray], [0], None, [256], [0, 255])
  plt.plot(hist, '--', color='gray', linewidth=5)

  colors = ('b','g','r')
  for channel, color in enumerate(colors):
    hist = cv2.calcHist([img], [channel], None, [256], [0, 255])
    plt.plot(hist, color=color, linewidth=2)

  plt.xlim([0,255])
  plt.show()


def main(args):
  
  img = open_image(args.image, args.display)

  if img is not None:
    display_histograms(img, args.display)


if __name__ == '__main__':

  image_filename_barrel = 'construction_barrel.png'

  parser = argparse.ArgumentParser(description='Displays image histograms.')

  parser.add_argument('--image', type=str,
                      help='Image to display and analyze',
                      default=image_filename_barrel)
  parser.add_argument('--display', type=int,
                      help='Number of seconds to display image',
                      default=2)

  args = parser.parse_args()

  main(args)