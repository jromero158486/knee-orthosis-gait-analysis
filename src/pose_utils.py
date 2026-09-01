import cv2
import mediapipe as mp
import numpy as np


class PoseDetector:
    """Small wrapper around MediaPipe Pose."""

    def __init__(
        self,
        static_image_mode: bool = False,
        model_complexity: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def get_landmarks(self, image: np.ndarray):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if not results.pose_landmarks:
            return None

        height, width, _ = image.shape

        return [
            (
                int(landmark.x * width),
                int(landmark.y * height),
                int(landmark.z * width),
            )
            for landmark in results.pose_landmarks.landmark
        ]

    def draw_landmarks(self, image: np.ndarray) -> np.ndarray:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if results.pose_landmarks:
            self.mp_draw.draw_landmarks(
                image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
            )

        return image

    @staticmethod
    def angle(landmarks, p1: int, p2: int, p3: int) -> float:
        point1 = np.array(landmarks[p1][:2], dtype=float)
        point2 = np.array(landmarks[p2][:2], dtype=float)
        point3 = np.array(landmarks[p3][:2], dtype=float)

        vector1 = point1 - point2
        vector2 = point3 - point2

        denominator = np.linalg.norm(vector1) * np.linalg.norm(vector2)

        if denominator == 0:
            return float("nan")

        cosine = np.dot(vector1, vector2) / denominator
        cosine = np.clip(cosine, -1.0, 1.0)

        return float(np.degrees(np.arccos(cosine)))

    @staticmethod
    def midline_deviation(landmarks) -> float:
        left_hip = np.array(landmarks[23][:2], dtype=float)
        right_hip = np.array(landmarks[24][:2], dtype=float)

        left_ankle = np.array(landmarks[27][:2], dtype=float)
        right_ankle = np.array(landmarks[28][:2], dtype=float)

        hip_midpoint = (left_hip + right_hip) / 2
        ankle_midpoint = (left_ankle + right_ankle) / 2

        return float(abs(hip_midpoint[0] - ankle_midpoint[0]))