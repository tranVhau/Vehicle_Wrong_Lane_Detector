# Vehicle_Wrong_Lane_Detector

### 1. Introduction

using Yolov8 to detect object, Bytetrack to tracking and open-cv to detect vehicle in the wrong lane (car and motorbike)

### 2. Installation

```
git clone https://github.com/tranVhau/Vehicle_Wrong_Lane_Detector.git
pip install ultralytics==8.0.111
pip install opencv-python
pip install numpy

```

#### Download sample video for detection

```
wget https://

```

#### Download YOLOv8 model

You can use pre-trained model by:

```
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt
```

visit: https://github.com/ultralytics/ultralytics#models for more

Or you can also use my trained model

```
wget https://

```

### 3. Usage

Open terminal

```
python run.py
```

In the **Draw Detection Line** window use mouse to draw detection line <br>
...<br>
And select **Specify the side of lane** <br>

### 4. Results

...

### 5. References

- https://github.com/ifzhang/ByteTrack.git <br>
- https://github.com/ultralytics/ultralytics.git
