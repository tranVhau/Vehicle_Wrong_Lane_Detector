from ultralytics import YOLO
import numpy as np
import cv2
import os
from draw_lane import LineDrawerGUI
from lane_detector import LaneDetector


# Define colors and font for the label of bouding box
box_color = (0, 255, 255)
box_color_alert = (0, 80, 255)
text_color = (0, 0, 0)
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
thickness = 2


# Calculate the centroid of the bounding box
def caculate_centroid(xmin, ymin, xmax, ymax):
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    return [x_center, y_center]


def draw_detection_line(frame, line):
    color = (253, 55, 165)
    thickness = 2
    isClosed = False

    #  shape_1 = points[0]
    #  shape_2 = points[1]
    #  shape_1 = np.array(shape_1)
    #  shape_2 = np.array(shape_2)
    #  shape_1 = shape_1.reshape((-1,1,2))
    #  shape_2 = shape_2.reshape((-1,1,2))
    #  frame = cv2.polylines(frame, [shape_1], isClosed, color, thickness)
    #  frame = cv2.polylines(frame, [shape_2], isClosed, color, thickness)
    detection_line = line
    detection_line = np.array(detection_line)
    detection_line = detection_line.reshape((-1, 1, 2))
    frame = cv2.polylines(frame, [detection_line], isClosed, color, thickness)
    return frame

# lane_area represent for the lane [x1 ,x2, x3, x4]
# point represent for position of vehicle [x,y]
# Purpose: to detecting the specific vehicle in the specific lane area or not


def lane_detector(lane_area, point, option_val, class_ID):
    # check if point in the left lane or not
    left_lane = cv2.pointPolygonTest(np.array(lane_area[0]), point, False)
    right_lane = cv2.pointPolygonTest(np.array(lane_area[1]), point, False)

    if (left_lane == 1.0 or right_lane == 1.0 or left_lane == 0 or right_lane == 0):  # inside the lane area
        if (left_lane == 1.0 or left_lane == 0):  # if the point (vehicle) on the left lane
            # print('Car-Motorbike')
            # print(class_ID)
            if (option_val == 1):  # car-motorbike
                if (class_ID == 4):
                    return False
                else:
                    return True
            else:
                if (class_ID == 4):

                    return True
                else:
                    return False
        else:  # on the right lane
            if (option_val == 1):
                if (class_ID == 4):
                    return True
                else:
                    return False
            else:  # motorbike-car
                if (class_ID == 4):
                    return False
                else:
                    return True
    else:  # outside
        return True


# Draw the bounding box and label on the image
# *****option_val variable values*****
# Car-Motorbike:1 (car-left, motorbike-right)
# Motorbike-Car:2 ...


def draw_bouding_box(frame, label, xmin, ymin, xmax, ymax, isWrong):
    # Get the size of the label text
    (label_width, label_height), _ = cv2.getTextSize(
        label, font, font_scale, thickness)

    if (isWrong == False):
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax),
                      box_color_alert, thickness)
        cv2.rectangle(frame, (xmin, ymin - label_height - 10),
                      (xmin + label_width, ymin), box_color_alert, -1)
        cv2.putText(frame, label, (xmin, ymin - 5), font,
                    font_scale, text_color, thickness)
    else:
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), box_color, thickness)
        cv2.rectangle(frame, (xmin, ymin - label_height - 10),
                      (xmin + label_width, ymin), box_color, -1)
        cv2.putText(frame, label, (xmin, ymin - 5), font,
                    font_scale, text_color, thickness)
    return frame


def run(source_path, destination_path):

    # Load the YOLO model
    # model = YOLO('best.pt')

    model = YOLO("./yolov8n")

    # get infomation of detecting video
    cap = cv2.VideoCapture(source_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Create a video out path by combining the destination path and the video name
    video_name = os.path.splitext(os.path.basename(source_path))[0] + ".mp4"
    video_out_path = os.path.join(destination_path, video_name)

    # Create a video writer object for the output video
    video_out = cv2.VideoWriter(
        video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # draw the detection lane
    ld = LineDrawerGUI(source_path)
    # print("Line coordinates:", ld.line_coords)
    print("Options:", ld.option_val)

    ld2 = LaneDetector(source_path, ld.line_coords)
    ld2.caculate_all_points()
    # print(list(ld2.points[0]))

    # print(ld2.points)
    # Loop over each frame of the video and perform object detection and tracking
    # Filter the detection to only include classes (2(cars) 7(trucks) 5(bus))=>car   3(motorbike)
    for result in model.track(source=source_path, tracker='bytetrack.yaml', show=False, stream=True, agnostic_nms=True):

        # Get the original frame from the detection result
        frame = result.orig_img

        # Convert the YOLO detection results to a Detections object
        detections = result.boxes.data.tolist()

        # append id with associate object that detected
        if result.boxes.id is not None:
            for index, data in enumerate(detections):
                data.append(result.boxes.id.cpu().numpy().astype(int)[index])

        # Filter the detection to only include classes 2 (cars) and 7 (trucks)
        # detections = [lst for lst in detections if lst[6] in [2, 7]]
        frame = draw_detection_line(frame, ld2.detection_line_coords)
        for data in detections:
            # Define the coordinates of the bounding box
            if (len(data) == 8):
                xmin, ymin, xmax, ymax = int(data[0]), int(
                    data[1]), int(data[2]), int(data[3])

                # Define the label for the bounding box
                label = f"id:{data[7]:.0f} { model.model.names[data[6]]}"

                # Draw the bounding box and label on the image
                # Get the size of the label text

                vehicle_pos = caculate_centroid(xmin, ymin, xmax, ymax)
                wrong_flag = lane_detector(
                    ld2.points, vehicle_pos, ld.option_val, data[6])
                draw_bouding_box(frame, label, xmin, ymin,
                                 xmax, ymax, wrong_flag)

        video_out.write(frame)
    video_out.release()


run(source_path="./QT2.1.mp4", destination_path="./results/")
