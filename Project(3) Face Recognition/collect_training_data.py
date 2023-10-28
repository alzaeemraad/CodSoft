import cv2
import matplotlib.pyplot as plt
def generating_dataset(img, id, img_id):
    cv2.imwrite(f"data/user.{id}.{img_id}.jpg", img)

def detect_the_boundaries(img, classifier, scaleFactor, minNeighbors, color, text):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
    return coords

def detect(img, face_cascade, img_id):
    color = (255, 0, 0)  # Blue color
    coords = detect_the_boundaries(img, face_cascade, 1.1, 10, color, "Face")
    if len(coords) == 4:
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        user_id = 1
        generating_dataset(roi_img, user_id, img_id)

    return img

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

if face_cascade.empty():
    raise IOError('Unable to load the face cascade classifier XML file')

video_capture = cv2.VideoCapture(0)

img_id = 0

while True:
    if img_id % 50 == 0:
        print(f"Collected {img_id} images")
    _, img = video_capture.read()
    img = detect(img, face_cascade, img_id)
    cv2.imshow("Face Detection", img)
    img_id += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
while True:
    if img_id % 50 == 0:
        print(f"Collected {img_id} images")
    _, img = video_capture.read()
    img = detect(img, face_cascade, img_id)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    img_id += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
