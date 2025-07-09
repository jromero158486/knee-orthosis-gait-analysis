import cv2
import mediapipe as mp
import numpy as np
import math

class PoseDetector:
    def __init__(self, static_image_mode=False, model_complexity=1, enable_segmentation=False,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=static_image_mode,
                                      model_complexity=model_complexity,
                                      enable_segmentation=enable_segmentation,
                                      min_detection_confidence=min_detection_confidence,
                                      min_tracking_confidence=min_tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def get_landmarks(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            h, w, _ = img.shape
            lm_list = [(int(lm.x * w), int(lm.y * h), int(lm.z * w)) for lm in landmarks]
            return lm_list
        return None

    def draw_landmarks(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)
        if results.pose_landmarks:
            self.mp_draw.draw_landmarks(img, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return img

    def angle(self, lm, p1, p2, p3):
        x1, y1, _ = lm[p1]
        x2, y2, _ = lm[p2]
        x3, y3, _ = lm[p3]

        a = np.array([x1 - x2, y1 - y2])
        b = np.array([x3 - x2, y3 - y2])

        cosine_angle = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)

    def midline_deviation(self, lm):
        left_hip = lm[23]  # left hip
        right_hip = lm[24]  # right hip
        left_ankle = lm[27]  # left ankle
        right_ankle = lm[28]  # right ankle

        mid_hip = np.array([(left_hip[0] + right_hip[0]) / 2, (left_hip[1] + right_hip[1]) / 2])
        mid_ankle = np.array([(left_ankle[0] + right_ankle[0]) / 2, (left_ankle[1] + right_ankle[1]) / 2])

        deviation = abs(mid_hip[0] - mid_ankle[0])
        return deviation