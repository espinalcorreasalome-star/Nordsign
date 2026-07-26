# LASIC
<p aling ="center">
    <img src="demo/recursos/logo_lasic_circular.png" width=220>
</p>

<h3 align="center">
Colombian Sign Language Visual Translator using Artificial Intelligence
</h3> 

<p align="center">

Project developed to strengthen the inclusion of the Colombian deaf community.

</p>

______________________________________________________________________________________________

# Description

LASIC is a system developed in Python that recognizes different signs of Colombian Sign Language (LSC) using Computer Vision and Artificial Intelligence. The system captures real-time video through a webcam, detects the hand using MediaPipe Hands, and classifies the sign performed using a Machine Learning model based on Random Forest trained with custom data.

______________________________________________________________________________________________

# Features 

- Real-time recognition of specific signs.
- Automatic hand detection using MediaPipe.
- Classification using Random Forest.
- Graphical User Interface (GUI) developed with CustomTkinter.
- Real-time processing.
- Modular architecture.

______________________________________________________________________________________________

# Technologies Used

| Technology | Function / Role |
|------------|----------|
| Python | Main language |
| OpenCV | Video capture and processing |
| MediaPipe Hands | Hand detection |
| Scikit-Learn | Machine Learning model |
| NumPy | Numerical processing |
| Pillow | Image conversion |
| CustomTkinter | Graphical User Interface (GUI) |

______________________________________________________________________________________________

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/shalomfrog/NORDSIGN.git
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Run the application

```bash
python demo/app.py
```

______________________________________________________________________________________________

# Current Status

The system currently recognizes various basic signs of Colombian Sign Language.

The project is still under development, and future versions will include:

- A larger number of signs.
- Model optimization.
- Higher accuracy.
- Full-word recognition.
- Feedback for learning.

______________________________________________________________________________________________

# License

This project is intended for academic and educational purposes.
