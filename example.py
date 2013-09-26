#!/bin/env python2
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt
import sys
import analizer


def doit(path):
    im = cv2.imread(path)
    image_in_ycbcr = cv2.cvtColor(im, cv2.COLOR_BGR2YCR_CB)
    mask = analizer.get_skin_mask(im, image_in_ycbcr)

    label_im, nb_labels = ndimage.label(mask)

    plt.figure(figsize=(9,3))

    plt.subplot(131)
    plt.imshow(im)
    plt.axis('off')
    plt.subplot(132)
    plt.imshow(mask)
    plt.axis('off')
    plt.subplot(133)
    plt.imshow(label_im)
    plt.axis('off')

    plt.subplots_adjust(wspace=0.02, hspace=0.02, top=1, bottom=0, left=0, right=1)
    plt.show()


if __name__ == "__main__":
    doit(sys.argv[1])
