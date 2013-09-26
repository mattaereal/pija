#!/bin/python2

from __future__ import division
import cv2
import numpy as np
import math

MAX_DISTANCE_PIXEL = math.sqrt(3*math.pow(255,2))
MIN_SCENE_LENGTH = 10
THRESHOLD = 0.1

def get_key_frames(video_capture):
    """Yields the key frames of the video."""
    sucess, previous_frame = video_capture.read()
    frame_size = previous_frame.shape[0] * previous_frame.shape[1]
    max_distance_frame = frame_size * MAX_DISTANCE_PIXEL
    frame_index = 0
    scene_start_index = 0

    while sucess:
        success, actual_frame = video_capture.read()

        if not success:
            return

        subs = np.abs(previous_frame.astype(np.float) - actual_frame.astype(np.float))
        power = np.power(subs, 2)
        add = np.sum(power, axis=-1, keepdims=True)
        sqrt = np.sqrt(add)
        dist = np.sum(sqrt)
        norm_dist = (dist / max_distance_frame)

        if norm_dist > THRESHOLD:
            scene_length = frame_index - scene_start_index
            if scene_length >= MIN_SCENE_LENGTH:
                key_frame_index = math.ceil(scene_length / 2) + \
                    scene_start_index
                scene_start_index = frame_index

                yield get_frame_by_index(video_capture, key_frame_index)


        frame_index += 1
        previous_frame = actual_frame
        sucess, actual_frame = video_capture.read()

def get_frame_by_index(video_capture, frame_index):
    """Returns an frame from a cv2 video capture or None on failure."""
    current_index = video_capture.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    video_capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_index)

    success, frame = video_capture.read()

    video_capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, current_index)

    if success:
        return frame

    return None
