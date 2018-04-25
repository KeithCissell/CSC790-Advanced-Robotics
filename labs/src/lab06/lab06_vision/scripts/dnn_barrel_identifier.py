#!/usr/bin/env python2.7

from __future__ import print_function, division
from subprocess import Popen, PIPE
from os import environ
import time
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

image_converter = CvBridge()

image_dir = "barrel/working/"


def camera_callback(gz_image):
    # Split image into left and right and look for barrel and each
    cv_image = image_converter.imgmsg_to_cv2(gz_image, "bgr8")

    left_image = cv_image[:, :int(cv_image.shape[1]//2)]
    right_image = cv_image[:, int(cv_image.shape[1]//2):]

    # write images
    cv2.imwrite(image_dir + "left.png", left_image)
    cv2.imwrite(image_dir + "right.png", right_image)

    # Search for barrel with helper

    # LEFT
    # Wait for prompt from py3_fastai
    prompt = process.stdout.readline().rstrip('\n')

    # Send filename to py3_fastai
    image_fullfile = image_dir + "left.png"
    print(image_fullfile, file=process.stdin)
    process.stdin.flush()

    # Read response from py3_fastai
    left_response = process.stdout.readline().rstrip('\n')
    print('LEFT:  ', left_response)

    # RIGHT
    # Wait for prompt from py3_fastai
    prompt = process.stdout.readline().rstrip('\n')

    # Send filename to py3_fastai
    image_fullfile = image_dir + "right.png"
    print(image_fullfile, file=process.stdin)
    process.stdin.flush()

    # Read response from py3_fastai
    left_response = process.stdout.readline().rstrip('\n')
    print('RIGHT: ', left_response)


# def run(command, env):
    # for fname in image_fnames:
    #     start_time = time.time()
    #
    #     # Read prompt from py3_fastai
    #     print('>>', process.stdout.readline().rstrip('\n'))
    #
    #     # Send filename to py3_fastai
    #     image_fullfile = image_dir + fname
    #     print('Sending:', image_fullfile)
    #     print(image_dir + fname, file=process.stdin)
    #     process.stdin.flush()
    #
    #     # Read response from py3_fastai
    #     print('>>', process.stdout.readline().rstrip('\n'))
    #     print('Elapsed time:', time.time() - start_time, '\n')

    # Read final prompt and send quit
    # process.stdout.readline().rstrip('\n')
    # print('quit', file=process.stdin)
    # process.stdin.flush()

if __name__ == '__main__':
    # Setup environment for fastai
    fastai_env = environ.copy()
    fastai_env['PATH'] = '/home/keith/anaconda3/bin:' + fastai_env['PATH']
    fastai_env['PYTHONPATH'] = ''

    # create a process
    command = 'source activate fastai-cpu && ./fastai_dnn_helper.py'
    process = Popen(command, stdin=PIPE, stdout=PIPE,
                    shell=True, bufsize=1, universal_newlines=True,
                    env=fastai_env, executable='/bin/bash')

    # time.sleep(30)

    # Initialize Node and Subscriber
    rospy.init_node('dnn_barrel_identifier', anonymous=True)
    rospy.Subscriber('/ddr/rgba_camera/image_raw', Image, camera_callback, queue_size=1)

    rospy.spin()
