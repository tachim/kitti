import argparse as ap
#import IPython
from collections import defaultdict as dd
import os
import numpy as np
import random

from PIL import Image

import cv2
import skvideo.io
import itertools as it
import sys

def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    parser = ap.ArgumentParser()
    parser.add_argument('--n_frames', type=int, default=0)
    parser.add_argument('--seek', type=str)
    parser.add_argument('--n_every', type=int, default=1)
    parser.add_argument('--skip_n', type=int, default=0)
    parser.add_argument('--subsample_rate', type=float, default=1)
    parser.add_argument('--output_dir', type=str, default='.')
    parser.add_argument('filename')
    args = parser.parse_args()

    basename = os.path.basename(args.filename)[:-4]

    output_dir = args.output_dir
    if output_dir is None:
        output_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'imgs/%s' % basename[:-4]
                )
        mkdir_p(output_dir)

    skip_n = args.skip_n

    print 'FILENAME:', args.filename
    inputdict = {}

    seek = args.seek
    if seek is not None:
        print 'Seeking to', seek
        inputdict['-ss'] = seek
    vc = skvideo.io.vreader(args.filename, inputdict=inputdict)
    n_frames = int(skvideo.io.ffprobe(args.filename)['video']['@nb_frames'])
    print n_frames, 'FRAMES TOTAL IN FILE'

    subsample_rate = args.subsample_rate
    print 'SUBSAMPLE RATE:', subsample_rate

    image_size = None
    for (i, (orig_ind, img)) in it.takewhile(
                lambda (i, (orig_ind, img)): not args.n_frames or i < args.n_frames,
                enumerate(
                    it.ifilter(
                        lambda (i, img): i >= skip_n and i % args.n_every == 0 and random.random() < args.subsample_rate,
                        enumerate(vc)
                        ))):
        fname = os.path.join(args.output_dir, 'frame_%0.5d.png' % orig_ind)
        Image.fromarray(img).save(fname)
        print 'Saved', fname

if __name__ == '__main__':
    main()
