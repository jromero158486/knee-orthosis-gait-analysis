from argparse import ArgumentParser
from pathlib import Path

import cv2

from src.pose_utils import PoseDetector


LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28


def draw_leg(
    frame,
    landmarks,
    hip: int,
    knee: int,
    ankle: int,
    detector: PoseDetector,
) -> None:
    hip_point = landmarks[hip][:2]
    knee_point = landmarks[knee][:2]
    ankle_point = landmarks[ankle][:2]

    cv2.line(frame, hip_point, knee_point, (0, 255, 0), 2)
    cv2.line(frame, knee_point, ankle_point, (0, 255, 0), 2)

    angle = detector.angle(landmarks, hip, knee, ankle)

    cv2.putText(
        frame,
        f"{angle:.0f} deg",
        (knee_point[0] - 25, knee_point[1] - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 200, 255),
        2,
    )


def annotate_video(
    input_path: Path,
    output_path: Path,
) -> None:
    capture = cv2.VideoCapture(str(input_path))

    if not capture.isOpened():
        raise RuntimeError(f"Could not open {input_path}")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS) or 30

    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    detector = PoseDetector()

    while True:
        success, frame = capture.read()

        if not success:
            break

        landmarks = detector.get_landmarks(frame)

        if landmarks is not None:
            draw_leg(
                frame,
                landmarks,
                LEFT_HIP,
                LEFT_KNEE,
                LEFT_ANKLE,
                detector,
            )

            draw_leg(
                frame,
                landmarks,
                RIGHT_HIP,
                RIGHT_KNEE,
                RIGHT_ANKLE,
                detector,
            )

        writer.write(frame)

    capture.release()
    writer.release()

    print(f"Saved annotated video to {output_path}")


def main() -> None:
    parser = ArgumentParser(
        description="Overlay knee landmarks and angles on a gait video."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)

    args = parser.parse_args()

    annotate_video(args.input, args.output)


if __name__ == "__main__":
    main()