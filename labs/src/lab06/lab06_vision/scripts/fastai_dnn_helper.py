#!/usr/bin/env python3.6

import sys
sys.path.append('/home/keith/Documents/fastai')

# Import fastai and dependencies
from fastai.imports import *
from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *
from fastai.sgdr import *
from fastai.plots import *

PATH = './barrel/'
arch = resnet34
size = 200

data = ImageClassifierData.from_paths(PATH, tfms=tfms_from_model(arch, size))
learn = ConvLearner.pretrained(arch, data)
learn.precompute = False
learn.load('barrel_model')

trn_tfms, val_tfms = tfms_from_model(arch, size) # get transformations

image_fullfile = input('Full filename: ')
im = val_tfms(open_image(image_fullfile))
preds = learn.predict_array(im[None])
probs = np.exp(preds)
