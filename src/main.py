import cv2 as cv
import mediapipe as mp
import math

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

from volume_control_module import HandVolumeController


def main():

    # Open webcam
    cap = cv.VideoCapture(0)

    # Create HandVolumeController object
    controller = HandVolumeController(
        "hand_landmarker.task"
    )

    while True:

        # Read frame from camera
        success, frame = cap.read()

        if not success:
            break

        # Mirror camera
        frame = cv.flip(frame, 1)

        # Detect hand
        result = controller.detect(frame)

        # Check if hand detected
        if len(result.hand_landmarks) > 0:

            # Get first hand landmarks
            landmarks = result.hand_landmarks[0]

            # Draw hand connections
            controller.draw_hand(
                frame,
                landmarks
            )

            # Calculate distance between thumb and index finger
            distance, p1, p2 = controller.get_distance(
                frame,
                landmarks
            )

            # Draw line between thumb and index finger
            cv.line(
                frame,
                p1,
                p2,
                (0, 255, 255),
                3
            )

            # Draw circle on thumb point
            cv.circle(
                frame,
                p1,
                10,
                (0, 0, 255),
                -1
            )

            # Draw circle on index finger point
            cv.circle(
                frame,
                p2,
                10,
                (0, 0, 255),
                -1
            )

            # Set system volume
            volume_percent = controller.set_volume(
                distance
            )

            # -----------------------------
            # Volume Bar
            # -----------------------------

            bar_x = 50
            bar_y = 100

            bar_width = 30
            bar_height = 300

            # Draw outer volume bar
            cv.rectangle(
                frame,
                (bar_x, bar_y),
                (
                    bar_x + bar_width,
                    bar_y + bar_height
                ),
                (255, 255, 255),
                2
            )

            # Calculate filled bar height
            filled_height = int(
                bar_height * volume_percent / 100
            )

            # Draw filled volume bar
            cv.rectangle(
                frame,
                (
                    bar_x,
                    bar_y + bar_height - filled_height
                ),
                (
                    bar_x + bar_width,
                    bar_y + bar_height
                ),
                (0, 255, 0),
                -1
            )

            # Display volume percentage
            cv.putText(
                frame,
                f"Volume: {volume_percent}%",
                (100, 150),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            # Display finger distance
            cv.putText(
                frame,
                f"Distance: {int(distance)}",
                (100, 190),
                cv.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

        else:

            # No hand detected
            cv.putText(
                frame,
                "Show your hand",
                (50, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        # Show frame
        cv.imshow(
            "Gesture Volume Control",
            frame
        )

        # Press q to quit
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    # Release camera
    cap.release()

    # Close OpenCV windows
    cv.destroyAllWindows()

    # Close MediaPipe / controller resources
    controller.close()


# Run program
if __name__ == "__main__":
    main()