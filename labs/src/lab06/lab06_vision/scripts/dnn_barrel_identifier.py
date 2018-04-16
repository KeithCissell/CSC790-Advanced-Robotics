#!/usr/bin/env python

from __future__ import print_function
from __future__ import division


def run(command, env):

    process = Popen(command, stdout=PIPE, shell=True, env=env, executable='/bin/bash')

    line = process.stdout.readline()
    while True:
        if not line:
            break
        else:
            yield line

if __name__ == '__main__':

    fastai_env = environment.copy()
    fastai_env['PATH'] = '/home/keith/anaconda3/bin:' + fastai_env['PATH']
    fastai_env['PYTHONPATH'] = ''

    run('source activate fastai-cpu && ./fastai_dnn_helper', fastai_env)
