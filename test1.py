from ultralytics import YOLO

model = YOLO('./yolov8s.pt')

if 11 in [1,2,3,4,5]:
    print('right')
else:
    print('wrong')
    
    
print(model.model.names)