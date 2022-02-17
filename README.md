# Hands-Free-Inputs

![image](https://user-images.githubusercontent.com/85316690/154574889-f26766e1-a5ae-4b15-9fc7-3493f8fe134a.png)

This is a collection of hands-free input demonstrations that demonstrate how we can use computer vision to change the way that we interact with a computer. Modern computers have 2 predominant input methods:

1) Keyboard and Mouse
2) Touch Input

Both of these are tactile (touch-based) inputs. Our goal is to show that we can eliminate the need for tactile inputs through computer vision. Although eliminating the tactile input may seem undesirable, it may be a solution to ergonomics issues, and a further polished hands-free input system may eliminate the necessity of additional equipment when using technology.

# Dependencies/How to Install

The following portions of this project have different dependencies:

## Base Dependencies

- Mediapipe
- OpenCV
- NumPy

## Volume-Control

- pycaw (Link to the creator's github here: https://github.com/AndreMiras/pycaw)

## Brightness-Control

(TBA)

# Some Limitations

The limitations of this are the usual ones that plague computer vision tasks.

- Dependence on lighting conditions (good lighting is imperative to a clean input)
- Framerate dependent on computer specifications. If the user's computer specifications are not optimal, the FPS will be less than optimal (I get about 15-25 FPS on a relatively weak computer)
- GPUs will not offer any performance benefit (we are not training any machine learning model)

# Contact

Please contact me at andrewjych@gmail.com, if you want to collaborate or suggest improvements to this project. 
