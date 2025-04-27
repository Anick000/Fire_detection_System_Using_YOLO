🔥 Fire Detection System using YOLO


A real-time fire detection system using the YOLO object detection algorithm, featuring image, video, and webcam support with an integrated GUI and alarm functionality.

🚀 Features
🔥 Real-time fire detection

🎥 Detect fires in images, videos, and live webcam feed

🔔 Alarm sound when fire is detected

✅ False positive filtering

📦 Build standalone EXE with PyInstaller

🛠️ Built With
Python

YOLOv5 (PyTorch)

OpenCV

Tkinter (for GUI)

PyInstaller (for app packaging)

📁 Dataset
The system uses the DFire Dataset organized as:

bash
Copy
Edit
dataset_dfire/
    ├── train/
    │    ├── images/
    │    └── labels/
    └── test/
         ├── images/
         └── labels/
Each image has a corresponding .txt file in YOLO format containing the bounding box annotations.

🖥️ Getting Started
Prerequisites
Python 3.8+

pip package manager

Installation
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/fire-detection-yolo.git
cd fire-detection-yolo
Install the required dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the application

bash
Copy
Edit
python app.py
(Optional) Build the executable

bash
Copy
Edit
pyinstaller --onefile --noconsole app.py
⚙️ How It Works
The trained YOLO model identifies fire in frames.

When fire is detected:

Bounding boxes are drawn.

Alarm sound is triggered (can be toggled).

Theme (Dark/Light) can be switched via the GUI.

Supports:

Static images

Pre-recorded videos

Real-time webcam streams


Image Detection	Video Detection	Webcam Detection
📈 Future Work
Advanced false positive filtering

SMS/Email alert system

Cloud integration for real-time monitoring

Mobile App version

📚 Acknowledgments
YOLOv5 by Ultralytics

OpenCV

[DFire Dataset Authors]

🚀 Thank you for checking out the project!

