# PiMachineLearning

This repo consists of multiple ARM Machine Learning projects. Raspbeery Pi is used for the entire projects.

## Introduction

The potential of AI and machine learning easily makes them be the fastest growing category in the computing industry. However, not everyone can afford an expensive, power consuming and bulky machine to implement and train their AI model for their practical applications. In addtion, an increase in demand for IoT and mobile platform encourages us to port out deep learning models to these compact computing units and run the models at close to real-time.

## Hardware

  - Raspberry Pi 4
      - ARM architecture
      - Raspbian OS
  - Intel NCSM2450.DK1 Movidius Neural Compute Stick
      - AI Accelerator USB Stick

## Project 1: Deep Learning Object Detection

This project is a Real-Time Object Detection program written that runs on ARM machine using YOLO model from Darknet. Considering the computing power on ARM architecture, I decided to use Tiny-Yolo instead of the full version.

### Environment Setup

  - Install Movidius on Raspberry Pi 4
    - ncappzoo
  - Requried Python3 Library:
    - cython3
    - numpy
    - pillow
    - tensorflow for ARM
    - opencv
    - mvnc
    - darkflow
  - Install VNC on Raspberry Pi 4 for GUI
  
### TODO:

Since I don't have a camera module for Raspberry Pi 4, I use recorded video for testing. Real-time object detection feature using camera will be added once I get the camera module.
