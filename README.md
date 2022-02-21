# Hands-Free-Inputs

This is a collection of hands-free input demonstrations that demonstrate how we can use computer vision to change the way that we interact with a computer. Modern computers have 2 predominant input methods:

1) Keyboard and Mouse
2) Touch Input

Both of these are tactile (touch-based) inputs. Our goal is to show that we can eliminate the need for tactile inputs through computer vision. Although eliminating the tactile input may seem undesirable, it may be a solution to ergonomics issues, and a further polished hands-free input system may eliminate the necessity of additional equipment when using technology.

# User Interface

## Volume Controls

![Volume Control Demo](Animation_volume_test2.gif)

## Brightness Controls
<img src="https://user-images.githubusercontent.com/85316690/154621660-5d5d4d53-a4e4-4dc4-a600-c47f22c6d70d.png" width=50% height=50%>

# Dependencies/How to Install

The following portions of this project have different dependencies:

## Base Dependencies

- Mediapipe ("pip install mediapipe")
- OpenCV ("pip install opencv-python")
- NumPy ("pip install numpy")

## Volume-Control

- pycaw ("pip install pycaw", Link to the creator's github here: https://github.com/AndreMiras/pycaw)

## Brightness-Control

- screen_brightness_control ("pip install screen_brightness_control", Link to the creator's github here: https://github.com/Crozzers/screen_brightness_control)

# Some Limitations

The limitations of this are the usual ones that plague computer vision tasks.

- Dependence on lighting conditions (good lighting is imperative to a clean input)
- Framerate dependent on computer specifications. If the user's computer specifications are not optimal, the FPS will be less than optimal (I get about 15-25 FPS on a relatively weak computer)
- GPUs will not offer any performance benefit (we are not training any machine learning model)

# Contact

Please contact me at andrewjych@gmail.com, if you want to collaborate or suggest improvements to this project. 
