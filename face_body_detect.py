import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2

# taken in image array and returns list of face boxes and list of person boxes
def detect_face_or_body(image):

    people = []
    c = []
    # detecting faces
    faces, confidences = cv.detect_face(image)
    lab = ['person'] * len(faces)
    out = draw_bbox(image, faces, lab, confidences, write_conf = True)
    
    # detecting objects
    bbox, labels, conf = cv.detect_common_objects(image)
    # only storing people
    for i, label in enumerate(labels):
        if label == 'person':
            people.append(bbox[i])
            c.append(conf[i])
    l = ['person'] * len(people)

    output_image = draw_bbox(out, people, l, c, write_conf = True)
    # output_image = draw_bbox(out, bbox, labels, conf)
    cv2.imwrite('heyo1.jpg', output_image)

    return faces, people

faces, people = detect_face_or_body(cv2.imread("final.jpg"))
