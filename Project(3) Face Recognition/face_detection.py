import cv2
import sys

# Load the cascade classifiers
frontalFaceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
profileFaceCascade = cv2.CascadeClassifier("haarcascade_profileface.xml")
eyeCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
mouthCascade = cv2.CascadeClassifier("Mouth.xml")

# Constants
BLUE = (240, 180, 70)
GREEN = (125, 210, 40)
THICKNESS = 3


def determine_the_rectangle(image, color, faces):
    for (x, y, w, h) in faces:
        bar_length = int(h / 8)
        bar_width = w
        cv2.rectangle(image, (x, y - bar_length), (x + bar_width, y), color, -1)
        cv2.rectangle(image, (x, y - bar_length), (x + bar_width, y), color, THICKNESS)
        cv2.rectangle(image, (x, y), (x + w, y + h), color, THICKNESS)
    return image


def detect_face(grayscale, image, is_webcam):
    # Detects frontal faces in the image using the face cascade
    faces = frontalFaceCascade.detectMultiScale(
        grayscale,
        scaleFactor=1.04,
        minNeighbors=3,
        minSize=(25, 25),
    )

    if not is_webcam:
        # Detects profile faces in the image using the face cascade
        profile_faces = profileFaceCascade.detectMultiScale(
            grayscale,
            scaleFactor=1.04,
            minNeighbors=3,
            minSize=(25, 25),
        )
        # Detect profile faces in the flipped image to detect profile faces facing right
        flipped = cv2.flip(grayscale, 1)
        profile_faces_flipped = profileFaceCascade.detectMultiScale(
            flipped,
            scaleFactor=1.04,
            minNeighbors=3,
            minSize=(25, 25)
        )

        # Draw a rectangle around each detected profile face
        image = determine_the_rectangle(image, GREEN, profile_faces)
        image = cv2.flip(image, 1)
        image = determine_the_rectangle(image, GREEN, profile_faces_flipped)
        image = cv2.flip(image, 1)

    # Draw a rectangle around each detected frontal face
    image = determine_the_rectangle(image, BLUE, faces)

    # Detect eyes in each face
    for (x, y, w, h) in faces:
        roi_gray = grayscale[y:y + h, x:x + w]
        eyes = eyeCascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(image, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)

        # Detect mouth in each face
        mouths = mouthCascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)
        for (mx, my, mw, mh) in mouths:
            cv2.rectangle(image, (x + mx, y + my), (x + mx + mw, y + my + mh), (0, 0, 255), 2)

    return image


def Using_Webcam():
    video = cv2.VideoCapture(0)
    while True:
        _, frame = video.read()

        # Convert frame to grayscale
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = detect_face(grayscale, frame, True)

        # Flip the frame
        frame = cv2.flip(frame, 1)

        cv2.imshow("Face Detection", frame)
        if cv2.waitKey(1) > 0:
            break

    video.release()
    cv2.destroyAllWindows()


def Using_Image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert image to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = detect_face(grayscale, image, False)

    cv2.imshow("Face Detection", image)
    cv2.waitKey(0)


def main():
    if len(sys.argv) == 1:
        Using_Webcam()
    elif len(sys.argv) == 2:
        Using_Image(sys.argv[1])
    else:
        print("Usage: python face-detect-haar.py [optional.jpg]")
        exit()


if __name__ == "__main__":
    main()
