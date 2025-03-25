import numpy as np
import cv2
from collections import defaultdict # it's like a dictionary but if there's no key this will create the key automatically

class SpeedEstimator:
    def __init__(self, fps, perspective_matrix, pixel_to_meter_ratio=1.0):
        self.fps = fps # How many frames has the video
        self.M = perspective_matrix # to transform coordinates into pixels
        self.tracks = defaultdict(list)  # id: [(frame_num, x, y)] # x,y = num. pixels #save all the positions with the ID - ej: track[12]=[(3,120,450),(4,125,455)]
        self.pixel_to_meter = pixel_to_meter_ratio # if use perspective_matrix ignore it

    def update(self, frame_num, object_id, bbox_center): #everytime this see a object need to save the position - bbox_Center = (x,y) of the center of the object
        self.tracks[object_id].append((frame_num, *bbox_center)) #ej: track[12]=[(3,120,450),(4,125,455)]

    def compute_speed(self, object_id): #Calculate the speed
        points = self.tracks[object_id] # get all the ID save 
        if len(points) < 2: # if there just 1 we can not calculat the velocity we need 2 posicion V = d/t
            return 0.0

        (f1, x1, y1), (f2, x2, y2) = points[-2], points[-1] # we need to get the last 2 points 

        p1 = cv2.perspectiveTransform(np.array([[[x1, y1]]], dtype=np.float32), self.M)[0][0]
        p2 = cv2.perspectiveTransform(np.array([[[x2, y2]]], dtype=np.float32), self.M)[0][0]
        # Convert the points into real point in the real world in meters
        # p2 = last point , p1= 1 before last, return [x2,y2] or [x1,y1]

        dist = np.linalg.norm(p2 - p1) # Calculate the velocity based on euclidian formula D=sqr((x2-x)^2+(y2-y1)^2)

        dt = (f2 - f1) / self.fps # if we are in frame 10 and the video is 30 fps -> dt =(10-9)/30 = 0.033 seconds

        speed_mps = dist / dt # v= d/t -> remember dist (p1,p2) in meters dt in seconds so Velocity = m/s
        speed_kph = speed_mps * 3.6 # m/s to km/h
        return speed_kph # get the results
