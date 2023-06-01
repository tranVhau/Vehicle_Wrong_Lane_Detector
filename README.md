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

#### Download sample video for detection (already in repository)

```
wget https://

```

#### Download YOLOv8 model 

You can use pre-trained model by:

```
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt
```

visit: https://github.com/ultralytics/ultralytics#models for more

Or you can also use my trained model (already in repository best.pt)

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
![image](https://github.com/tranVhau/Vehicle_Wrong_Lane_Detector/assets/75488759/3527c22b-887e-43be-b07e-114ac6f0c0fb)


### 4. Results

samples of results in ./results

### 5. References

- https://github.com/ifzhang/ByteTrack.git <br>
- https://github.com/ultralytics/ultralytics.git
