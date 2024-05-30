# SleepyWheels

### An ensemble drowsiness detection system

This project is an effort towards higher accuracy and more robustness to various real-life situations (different camera angles, skin complexion, presence of face wear like eyeglasses/masks, etc.) in which a driver's drowsy behaviour must be detected and they must be alerted before a road accident can occur. It consists of:

- an EfficientNetV2B0 CNN model that outputs the probability of the driver being sleepy
- a FaceMesh landmark detector (from Google's Mediapipe library) that enables calculation of aspect ratios of eyes and mouth
- an alarm that gets triggered if the driver is sleepy
- a web dashboard that can be visited later to check alarm and yawn timestamps from previous journeys

| Item                                      |                                              Link                                               |
| :---------------------------------------- | :---------------------------------------------------------------------------------------------: |
| 10,000-image-dataset scrapped from Google | [Dataset](https://drive.google.com/drive/folders/1bhrgY8RcUFuD675oxcSLJkmtxY3Wxfg9?usp=sharing) |
| Web dashboard for drivers                 |                          [Dashboard](https://sleepywheels.vercel.app/)                          |
| Live demo of the system                   |                       [Demo](https://www.youtube.com/watch?v=KaCROQi2XRs)                       |
| Download the trained model                | [Model](https://drive.google.com/file/d/1IEohZ-2uFnPpOMblCZ516eTCe8wnnpwQ/view?usp=share_link)  |
| Research Paper link                       |               [Paper](https://jai.front-sci.com/index.php/jai/article/view/1117)                |

#### Versions used

| Item       | Version |
| :--------- | :-----: |
| python     |   3.9   |
| tensorflow | 2.12.0  |
