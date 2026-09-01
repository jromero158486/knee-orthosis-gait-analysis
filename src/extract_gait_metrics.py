from argparse import ArgumentParser
from pathlib import Path

import cv2
import pandas as pd

from src.pose_utils import PoseDetector


DEFAULT_VIDEO_DIR = Path("data/videos")
DEFAULT_OUTPUT = Path("results/metrics/gait_metrics.csv")

VIDEOS = {
    "with_orthosis.mp4": "with_orthosis",
    "without_orthosis.mp4": "without_orthosis",
}


def process_video(
    video_path: Path,
    condition: str,
    detector: PoseDetector,
) -> list[dict]:
    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        raise RuntimeError(f"Could not open {video_path}")

    rows = []
    frame_id = 0

    while True:
        success, frame = capture.read()

        if not success:
            break

        landmarks = detector.get_landmarks(frame)

        if landmarks is not None:
            rows.append(
                {
                    "condition": condition,
                    "frame": frame_id,
                    "knee_angle_right": detector.angle(
                        landmarks, 24, 26, 28
                    ),
                    "knee_angle_left": detector.angle(
                        landmarks, 23, 25, 27
                    ),
                    "midline_deviation": detector.midline_deviation(
                        landmarks
                    ),
                }
            )

        frame_id += 1

    capture.release()

    return rows


def main() -> None:
    parser = ArgumentParser(
        description="Extract gait metrics from videos using MediaPipe Pose."
    )
    parser.add_argument(
        "--video-dir",
        type=Path,
        default=DEFAULT_VIDEO_DIR,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
    )

    args = parser.parse_args()

    detector = PoseDetector()
    rows = []

    for filename, condition in VIDEOS.items():
        video_path = args.video_dir / filename

        if not video_path.exists():
            print(f"Skipping missing video: {video_path}")
            continue

        rows.extend(
            process_video(
                video_path=video_path,
                condition=condition,
                detector=detector,
            )
        )

    if not rows:
        raise RuntimeError("No gait data was extracted.")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(args.output, index=False)

    print(f"Saved {len(dataframe)} frames to {args.output}")


if __name__ == "__main__":
    main()