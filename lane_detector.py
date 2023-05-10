import cv2
import numpy as np

class LaneDetector:
     def __init__(self,video_source,line_coords):
         self.first_coords = list(np.array(line_coords[0])*2)
         self.second_coords = list(np.array(line_coords[1])*2)
         self.video_source = video_source
         self.video = cv2.VideoCapture(video_source)
         self.points = None
         self.detection_line_coords = None
    
     def caculate_all_points(self):  #caculate all point from given 2 coordinates (2 tuples, 8 points)
        #  Open the video file
         cap = cv2.VideoCapture(self.video_source)
        #  Get the frame dimensions of the video
         width_vid = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        
         self.points = [[[0,self.first_coords[1]],self.first_coords, self.second_coords,[0,self.second_coords[1]]],[[width_vid, self.first_coords[1]],self.first_coords, self.second_coords,[width_vid,self.second_coords[1]]]]
         self.detection_line_coords = [self.first_coords, self.second_coords]
         print(self.points)
         print(self.detection_line_coords)
     
     def draw_shape(self, frame):
        #  image = cv2.imread("./img2.png")
         # color, thickness and isClosed
         color = (255, 0, 0)
         thickness = 2
         isClosed = False
         
         currPoint = self.points[0]
         currPoint = np.array(currPoint)
         currPoint = currPoint.reshape((-1,1,2))
         
         return cv2.polylines(frame, [currPoint], isClosed, color, thickness)
         


     
# ld = LaneDetector(video_source='./bridge.mp4', line_coords=((1,1),(129,1029)))

# ld.caculate_all_points()
# ld.draw_shape()
    