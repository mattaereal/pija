#!/bin/env python2

"""Analizer module."""

from __future__ import division
import cv2
import magic
import random
import numpy as np
from scipy import ndimage

from key_frame_extractor import get_key_frames


PERCENTAGE_OF_FRAMES_TO_ANALIZE = 0.1
BYTES_PER_PIXEL = 3

class SkinRegion(object):

    def __init__(self, image, skin_mask, labeled_image, label_number,
                 rectangle_slices):
        """Creates a new skin region.

            image: The entire image in YCrCb mode.
            skin_mask: The entire image skin mask.
            labeled_image: A matrix of the size of the image with the region
                label in each position. See scipy.ndimage.measurements.label.
            label_number: The label number of this skin region.
            rectangle_slices: The slices to get the rectangle of the image in
                which the region fits as returned by
                scipy.ndimage.measurements.find_objects.
        """
        self.region_skin_pixels = np.count_nonzero(
            labeled_image[rectangle_slices] == label_number
        )

        self.bounding_rectangle_size = \
            (
                rectangle_slices[1].start - rectangle_slices[0].start
            ) * (
                rectangle_slices[1].stop - rectangle_slices[0].stop
            )

        self.bounding_rectangle_skin_pixels = np.count_nonzero(
            skin_mask[rectangle_slices]
        )

        self.bounding_rectangle_avarage_pixel_intensity = np.average(
            image[rectangle_slices].take([0], axis=2)
        )


def analize(path):
    """Analizes a file, returning True if it contains pornography."""

    try:
        type_ = magic.from_file(path)
    except IOError:
        return False

    if type_ is None:
        return False

    type_ = type_.lower()

    if "video" in type_:
        return analize_video(path)

    if "image" in type_:
        return analize_image(path)

    return False

def analize_image(path):
    """Analizes a file, returning True if it contains nudity."""
    image = cv2.imread(path)

    if image is None:
        return False

    return analize_numpy_array(image)

def analize_video(path):
    """Analizes a video, returning True if it contains nudity."""

    vidcap = cv2.VideoCapture(path)

    if vidcap is None:
        return False

    for frame in get_key_frames(vidcap):
        has_porn = analize_numpy_array(frame)

        #If we find one porn frame we tag the video as porn, this can be
        #really improved.
        if has_porn:
            return True

    return False

def analize_numpy_array(image):
    """Analize an image as a numpy array, returning True if it contains
    nudity."""

    MIN_SKIN_PERCENTAGE = 0.15

    image_in_ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    skin_mask = get_skin_mask(image, image_in_ycbcr)

    image_pixels_count = image.size / BYTES_PER_PIXEL
    skin_pixels_count = np.count_nonzero(skin_mask)
    percentage_of_skin = skin_pixels_count / image_pixels_count

    if percentage_of_skin < MIN_SKIN_PERCENTAGE:
        return False

    regions = get_skin_regions(image_in_ycbcr, skin_mask)

    if (regions[0].region_skin_pixels / skin_pixels_count < 0.35) \
        and (regions[1].region_skin_pixels / skin_pixels_count < 0.30) \
        and (regions[2].region_skin_pixels / skin_pixels_count < 0.30):
        return False

    if (regions[0].region_skin_pixels / skin_pixels_count < 0.45):
        return False

    if percentage_of_skin < 0.3 and \
        (regions[0].bounding_rectangle_size / image_pixels_count) < 0.55:
        return False

    if len(regions) > 60 and \
        (regions[0].bounding_rectangle_avarage_pixel_intensity / 255) < 0.25:

        return False

    return True


def get_skin_mask(image, image_in_ycbcr):
    """Returns a mask of the same size of the image with True on the skin-color
    pixel. NOTE: This function expects the image color representation to be
    YCrCb."""

    return np.logical_and(

        np.logical_and(
            np.logical_and(
                (np.abs(image.take([2], axis=2) - image.take([1], axis=2)) > 15).\
                    squeeze(),
                (image.take([2], axis=2) > image.take([1], axis=2)).squeeze()
            ),
            np.logical_and(
                np.logical_and(
                    np.all(
                        image > [20, 40, 95],
                        axis=2
                    ),
                    (np.amax(image, axis=2) - np.min(image, axis=2)) > 15
                ),
                (image.take([2], axis=2) > image.take([0], axis=2)).squeeze()
            )
        ),

        np.all(
            np.logical_and(
                [0, 133, 80] <= image_in_ycbcr,
                image_in_ycbcr <= [255, 173, 120]
            ),
            axis=2
        )
    )

def paint_non_skin_pixels(image, color_r=0, color_g=0, color_b=0,
                          skin_mask=None):
    """Paints non-skin colored pixels in-place."""
    if skin_mask is None:
        skin_mask = get_skin_mask(image)

    image[~skin_mask] = [color_b, color_g, color_r]

def paint_skin_pixels(image, color_r=0, color_g=0, color_b=0, skin_mask=None):
    """Paints the skin colored pixels in-place."""
    if skin_mask is None:
        skin_mask = get_skin_mask(image)

    image[skin_mask] = [color_b, color_g, color_r]

def skin_binarize_image(image):
    """Paints all skin colored pixels of white and non-skin pixels of black
    in-place."""
    skin_mask = get_skin_mask(image)
    paint_skin_pixels(image, 255, 255, 255, skin_mask)
    paint_non_skin_pixels(image, 0, 0, 0, skin_mask)

def get_skin_regions(image, skin_mask):
    """Returns an array of SkinRegion for the image with the data for the
    analizer computed. NOTE: The image must be in YCrCb mode."""
    regions = []

    labeled_image, regions_count = ndimage.label(skin_mask)
    region_rectangles_slices = ndimage.find_objects(labeled_image)

    for i in xrange(regions_count):
        label = i + 1
        region = SkinRegion(image, skin_mask, labeled_image, label,
                            region_rectangles_slices[i])
        regions.append(region)

    return sorted(regions, key=lambda r: r.region_skin_pixels, reverse=True)
