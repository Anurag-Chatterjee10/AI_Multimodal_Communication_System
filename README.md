# AI Multimodal Communication System

> **A modular AI-powered desktop application that integrates Computer Vision, Speech Processing, Optical Character Recognition, Face Recognition, and Sign Language Intelligence into a unified real-time communication platform.**

![Python](https://img.shields.io/badge/Python-3.x-blue)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-orange)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-purple)
![Version](https://img.shields.io/badge/Version-v1.0.0-success)

---

# Overview

The **AI Multimodal Communication System** is a modular desktop application developed using **Python** and **PySide6** that combines multiple Artificial Intelligence technologies into a single unified platform.

The application is capable of processing multiple communication modalities including:

- Images
- Videos
- Live Camera Feed
- Speech
- Text
- Sign Language

through a scalable and extensible AI architecture.

Unlike standalone AI applications that focus on a single task, this system provides a common framework capable of dynamically integrating multiple AI models while maintaining a professional desktop user experience.

---

# Key Features

## Computer Vision

- Real-Time Camera Processing
- Image Processing
- Video Processing
- Snapshot Capture
- Video Recording

---

## Artificial Intelligence

### Object Detection

- YOLOv8 Real-Time Object Detection

### Optical Character Recognition

- EasyOCR Integration

### Face Recognition

- InsightFace Integration

### Speech Recognition

- Offline Speech-to-Text

### Text-to-Speech

- Offline Text-to-Speech

### Sign Language

- Real-Time Sign Language Recognition
- Text-to-Sign Language Animation

---

## User Interface

- Professional PySide6 Desktop GUI
- Dark Theme
- Dynamic AI Model Switching
- Live AI Visualization
- Status Monitoring
- Modular Workspace Layout

---

# System Architecture

The project follows a modular architecture where every major subsystem is isolated into independent components.

```
                    +----------------------+
                    |      Main Window     |
                    +----------+-----------+
                               |
                               |
                    +----------v-----------+
                    |   Application        |
                    |    Controller        |
                    +----------+-----------+
                               |
         ------------------------------------------------
         |              |               |               |
         |              |               |               |
+--------v------+ +------v------+ +------v------+ +------v------+
| Camera Service| |Video Service| |Audio Service| |Microphone    |
|               | |             | |             | |Service       |
+--------+------+ +------+------+ +------+------+ +------+-------+
         |               |                |               |
         ----------------+----------------+---------------
                          |
                          |
                  +-------v--------+
                  | Frame Pipeline |
                  +-------+--------+
                          |
                 +--------v--------+
                 |    AI Worker    |
                 +--------+--------+
                          |
                  +-------v--------+
                  | Model Manager  |
                  +-------+--------+
                          |
      -----------------------------------------------------
      |          |          |          |         |         |
      |          |          |          |         |         |
+-----v--+ +-----v--+ +-----v--+ +-----v--+ +----v----+ +--v------+
| YOLO   | | OCR    | | Face   | | Speech | | Sign    | |Animation|
+---------+ +--------+ +--------+ +--------+ +---------+ +---------+
```

---

# Project Structure

```
AI_Multimodal_Communication_System

├── src
│   ├── ai
│   ├── config
│   ├── controllers
│   ├── core
│   ├── processing
│   ├── services
│   ├── ui
│   └── utils
│
├── assets
├── models
├── requirements.txt
├── main.py
└── README.md
```

---

# Technology Stack

## Programming Language

- Python

## GUI Framework

- PySide6 (Qt)

## Computer Vision

- OpenCV

## Deep Learning

- PyTorch

## AI Models

- Ultralytics YOLOv8
- EasyOCR
- InsightFace
- MediaPipe

## Runtime

- ONNX Runtime

## Packaging

- PyInstaller

## Version Control

- Git
- GitHub

---

# AI Modules

| Module | Technology |
|---------|------------|
| Object Detection | YOLOv8 |
| OCR | EasyOCR |
| Face Recognition | InsightFace |
| Speech Recognition | SpeechRecognition |
| Text-to-Speech | Qt TextToSpeech |
| Sign Language Recognition | MediaPipe |
| Sign Animation | Custom Animation Engine |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Anurag-Chatterjee10/AI_Multimodal_Communication_System.git
```

Move inside the project.

```bash
cd AI_Multimodal_Communication_System
```

Create Virtual Environment.

```bash
python -m venv .venv
```

Activate Environment.

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

Install Dependencies.

```bash
pip install -r requirements.txt
```

Run the Application.

```bash
python main.py
```

---

# Download

The latest executable can be downloaded from GitHub Releases.

**Latest Release**

https://github.com/Anurag-Chatterjee10/AI_Multimodal_Communication_System/releases/latest

---

# Screenshots

## Main Dashboard

*(Add Screenshot Here)*

---

## Object Detection

*(Add Screenshot Here)*

---

## OCR

*(Add Screenshot Here)*

---

## Face Recognition

*(Add Screenshot Here)*

---

## Sign Language Recognition

*(Add Screenshot Here)*

---

## Text-to-Sign Animation

*(Add Screenshot Here)*

---

# Current Release

## Version 1.0.0

### Highlights

- Modular AI Architecture
- Professional Desktop GUI
- Real-Time AI Processing
- Multiple AI Models
- Windows Standalone Executable
- GitHub Release

---

# Future Improvements

- Voice Command Integration
- Cloud AI Services
- Cross Platform Deployment
- Additional AI Models
- Performance Optimization
- User Profiles
- Plugin Support

---

# Author

## Anurag Chatterjee

**B.Tech Computer Science & Engineering**

KIIT University

GitHub

https://github.com/Anurag-Chatterjee10

---

# License

This project is developed for educational, research, and learning purposes.

---

# Acknowledgements

This project utilizes several outstanding open-source libraries and frameworks, including:

- PySide6
- OpenCV
- PyTorch
- Ultralytics YOLO
- EasyOCR
- InsightFace
- MediaPipe
- ONNX Runtime

Special thanks to the open-source community for making these technologies accessible to developers worldwide.
