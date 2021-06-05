# SleepyWheels
### An ensemble drowsiness detection system

This project is an effort towards higher accuracy and more robustness to varying real-life situations, in which drowsinss of a driver must be detected before it is too late. It consists of:
* an EfficientNetB0 that outputs the probability that the driver is sleepy or alert
* a HOG-SVM Landmark detector from DLib that helps calculate aspect ratios of eyes and mouth
* an alarm that gets triggered if driver is sleepy
* a web dashboard that keeps track of alarm and yawn triggers

[Dataset](https://drive.google.com/drive/folders/16NQg2ijQfumMlEqn1sYoo5Tg3IkLbfFO) - custom 2500-image-dataset scrapped from Google Images
