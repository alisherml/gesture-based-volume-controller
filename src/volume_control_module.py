import cv2 as cv
import mediapipe as mp
import math

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


class HandVolumeController:

    def __init__(self, model_path="hand_landmarker.task"):

        # -----------------------------
        # MediaPipe Hand Landmarker
        # -----------------------------

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1
        )

        self.detector = vision.HandLandmarker.create_from_options(
            options
        )

        self.timestamp = 0

        # -----------------------------
        # Windows Volume
        # -----------------------------

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        self.volume = interface.QueryInterface(
            IAudioEndpointVolume
        )

        self.volume_range = self.volume.GetVolumeRange()

        self.min_volume = self.volume_range[0]
        self.max_volume = self.volume_range[1]

    # =================================
    # Detect hand
    # =================================

    def detect(self, frame):

        rgb = cv.cvtColor(
            frame,
            cv.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        self.timestamp += 1

        result = self.detector.detect_for_video(
            mp_image,
            self.timestamp
        )

        return result

    # =================================
    # Calculate thumb-index distance
    # =================================

    def get_distance(self, frame, landmarks):

        h, w, _ = frame.shape

        # Thumb tip = 4
        # Index tip = 8

        x1 = int(landmarks[4].x * w)
        y1 = int(landmarks[4].y * h)

        x2 = int(landmarks[8].x * w)
        y2 = int(landmarks[8].y * h)

        # Euclidean distance

        distance = math.hypot(
            x2 - x1,
            y2 - y1
        )

        return distance, (x1, y1), (x2, y2)

    # =================================
    # Convert distance to volume
    # =================================

    def set_volume(self, distance):

        # Camera distance range
        min_distance = 30
        max_distance = 200

        # Clamp distance

        distance = max(
            min_distance,
            min(max_distance, distance)
        )

        # Convert distance -> volume

        volume = (
            (distance - min_distance)
            /
            (max_distance - min_distance)
        )

        # Convert 0-1 -> system volume range

        system_volume = (
            self.min_volume
            +
            volume *
            (self.max_volume - self.min_volume)
        )

        self.volume.SetMasterVolumeLevel(
            system_volume,
            None
        )

        # Return percentage

        percentage = int(volume * 100)

        return percentage

    # =================================
    # Draw hand
    # =================================

    def draw_hand(self, frame, landmarks):

        h, w, _ = frame.shape

        connections = [

            # Thumb
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),

            # Index
            (0, 5),
            (5, 6),
            (6, 7),
            (7, 8),

            # Middle
            (0, 9),
            (9, 10),
            (10, 11),
            (11, 12),

            # Ring
            (0, 13),
            (13, 14),
            (14, 15),
            (15, 16),

            # Pinky
            (0, 17),
            (17, 18),
            (18, 19),
            (19, 20),

            # Palm
            (5, 9),
            (9, 13),
            (13, 17)
        ]

        # Draw points

        for landmark in landmarks:

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )

        # Draw connections

        for start, end in connections:

            x1 = int(landmarks[start].x * w)
            y1 = int(landmarks[start].y * h)

            x2 = int(landmarks[end].x * w)
            y2 = int(landmarks[end].y * h)

            cv.line(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

    # =================================
    # Close
    # =================================

    def close(self):

        self.detector.close()
