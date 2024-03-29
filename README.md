# SleepyWheels
### An ensemble drowsiness detection system

This project is an effort towards higher accuracy and more robustness to varying real-life situations, in which drowsiness of a driver must be detected before it is too late. It consists of:
* an EfficientNetV2B0 that outputs the probability of the driver being sleepy
* the FaceMesh landmark detector from Google's Mediapipe that helps calculate aspect ratios of eyes and mouth
* an alarm that gets triggered if driver is sleepy
* a web dashboard that keeps track of alarm and yawn triggers

| Item | Link |
| :------- | :-------: |
| 10,000-image-dataset scrapped from Google | [Dataset](https://drive.google.com/drive/folders/1bhrgY8RcUFuD675oxcSLJkmtxY3Wxfg9?usp=sharing) |
| Web dashboard for drivers | [Dashboard](http://jominjose.42web.io/dashboard.php) |
| Live demo of the system | [Demo](https://www.youtube.com/watch?v=KaCROQi2XRs) |
| Download the trained model | [Model](https://drive.google.com/file/d/1IEohZ-2uFnPpOMblCZ516eTCe8wnnpwQ/view?usp=share_link) |

