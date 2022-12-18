import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
import os

# bounding boxes go left, top, right, bottom
# taken in image array and returns list of face boxes and list of person boxes
def detect_face_or_body(video_name):
    locs = []
    for i, frame in enumerate(os.listdir(video_name + "/frames")):
        boxes = []
        frame_path = os.path.join(video_name, ("frames/keyframe_scene_" + str(i+1) + ".jpg"))
        image = cv2.imread(frame_path)

        people = []
        c = []
        # detecting faces
        faces, confidences = cv.detect_face(image)
        boxes.append(faces)
        label = ['person'] * len(faces)
        out = draw_bbox(image, faces, label, confidences, write_conf = True)
        
        # detecting objects
        bbox, labels, conf = cv.detect_common_objects(image)
        # only storing people
        for i, label in enumerate(labels):
            if label == 'person':
                people.append(bbox[i])
                c.append(conf[i])
        l = ['person'] * len(people)
        boxes.append(people)
        locs.append(boxes)
        output_image = draw_bbox(out, people, l, c, write_conf = True)
        cv2.imwrite("bbox" + str(i+1) + ".jpg", output_image)


    return locs