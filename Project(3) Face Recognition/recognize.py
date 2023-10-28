import cv2

def detect_the_boundaries(img, classifier, scaleFactor, minNeighbors, color, text, clf):
    try:
        # Converting image to gray-scale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # detecting features in gray-scale image, returns coordinates, width and height of features
        features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
        coords = []
        # drawing rectangle around the feature and labeling it
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            # Predicting the id of the user
            id, _ = clf.predict(gray_img[y:y+h, x:x+w])
            # Check for id of user and label the rectangle accordingly
            if id==1:
                cv2.putText(img, "Raad", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            coords = [x, y, w, h]
    except Exception as e:
        print(f"Error in detect_the_boundaries: {e}")

    return coords

# Method to recognize the person
def recognizing(img, clf, faceCascade):
    coords = []  # Initialize coords with an empty list
    try:
        color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0), "black": (0, 0, 0)}
        coords = detect_the_boundaries(img, faceCascade, 1.1, 10, color["black"], "Face", clf)
    except Exception as e:
        print(f"Error in recognizing: {e}")
    return img


# Loading classifier
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Loading custom classifier to recognize
clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("classifier.xml")

# Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
video_capture = cv2.VideoCapture(0)

while True:
    try:
        # Reading image from video stream
        ret, img = video_capture.read()
        if not ret:
            continue  # Skip if frame is not valid
        # Call method we defined above
        img = recognizing(img, clf, faceCascade)
        # Writing processed image in a new window
        cv2.imshow("face detection", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(f"Error in main loop: {e}")


# releasing web-cam
video_capture.release()
# Destroying output window
cv2.destroyAllWindows()
