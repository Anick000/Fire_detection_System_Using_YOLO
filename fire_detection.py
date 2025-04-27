import tkinter as tk
from tkinter import filedialog
import threading
import pygame
import time
import cv2
from twilio.rest import Client
from ultralytics import YOLO

# Load YOLO model
model = YOLO(r'best 2.pt')#model file path

# Alarm setup
pygame.mixer.init()
alarm_playing = False
alarm_reset_time = 0
alarm_duration = 5  # Alarm plays at least this many seconds
fire_stop_delay = 2  # seconds

def play_alarm():
    global alarm_playing, alarm_reset_time
    current_time = time.time()
    if not alarm_playing:
        alarm_playing = True
        alarm_reset_time = current_time + alarm_duration
        pygame.mixer.music.load(r'alarm-327234.mp3')#alarm file path
        pygame.mixer.music.play(-1)
        print("🔊 Alarm started!")
        toggle_alarm_button.config(text="Stop Alarm")
    else:
        alarm_reset_time = current_time + alarm_duration  # Extend alarm duration

def stop_alarm():
    global alarm_playing
    pygame.mixer.music.stop()
    alarm_playing = False
    print("🔇 Alarm stopped!")
    toggle_alarm_button.config(text="Start Alarm")

def toggle_alarm():
    global alarm_playing
    if alarm_playing:
        stop_alarm()
    else:
        play_alarm()

def check_alarm_timeout():
    global alarm_playing, alarm_reset_time
    if alarm_playing and time.time() > alarm_reset_time:
        pygame.mixer.music.stop()
        alarm_playing = False
        print("🔇 Alarm stopped automatically.")
        toggle_alarm_button.config(text="Start Alarm")

# Twilio credentials
account_sid = 'YOUR_TWILIO_ACCOUNT_ID'
auth_token = 'YOUR_TWILIO_AUTHORISATION_TOKEN'
twilio_number = '+16502156279'#YOUR TWILIO NUMBER
target_number = '+919346591842'#YOUR TARGER NUMBER
client = Client(account_sid, auth_token)

# SMS cooldown setup
last_sent_time = 0
cooldown_seconds = 30
sms_lock = threading.Lock()

def send_fire_alert():
    global last_sent_time
    current_time = time.time()
    with sms_lock:
        if current_time - last_sent_time >= cooldown_seconds:
            try:
                message = client.messages.create(
                    body="🚨 FIRE DETECTED! Please check the area immediately!",
                    from_=twilio_number,
                    to=target_number
                )
                print("📩 SMS sent:", message.sid)
                last_sent_time = current_time
            except Exception as e:
                print("❌ Error sending SMS:", e)
        else:
            remaining = int(cooldown_seconds - (current_time - last_sent_time))
            print(f"⏳ SMS already sent. Try again in {remaining} seconds.")

# Handle image detection
def detect_on_image(path):
    image = cv2.imread(path)
    if image is None:
        print("❌ Could not load image.")
        return
    results = model.predict(source=image, imgsz=640, conf=0.65, verbose=False)
    annotated = results[0].plot()

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if 'fire' in model.names[cls].lower():
                threading.Thread(target=play_alarm).start()
                threading.Thread(target=send_fire_alert).start()

    cv2.imshow("🖼 Fire Detection (Image)", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Handle video detection
def detect_on_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("❌ Could not open video.")
        return

    fire_detected_frames = 0
    fire_threshold = 3
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 3 != 0:
            continue

        results = model.predict(source=frame, imgsz=640, conf=0.7, verbose=False)
        annotated_frame = results[0].plot()

        fire_in_frame = False
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if 'fire' in model.names[cls].lower():
                    fire_in_frame = True
                    break

        if fire_in_frame:
            fire_detected_frames += 1
        else:
            fire_detected_frames = 0

        if fire_detected_frames >= fire_threshold:
            threading.Thread(target=play_alarm).start()
            threading.Thread(target=send_fire_alert).start()

        check_alarm_timeout()
        cv2.imshow("🔥 Fire Detection (Video)", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Handle webcam detection
def detect_on_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not access webcam.")
        return

    fire_detected_frames = 0
    fire_threshold = 5
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 5 != 0:
            continue

        results = model.predict(source=frame, imgsz=640, conf=0.7, verbose=False)
        annotated = results[0].plot()

        fire_in_frame = False
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if 'fire' in model.names[cls].lower():
                    fire_in_frame = True
                    break

        if fire_in_frame:
            fire_detected_frames += 1
        else:
            fire_detected_frames = 0

        if fire_detected_frames >= fire_threshold:
            threading.Thread(target=play_alarm).start()
            threading.Thread(target=send_fire_alert).start()

        check_alarm_timeout()
        cv2.imshow("📷 Fire Detection (Webcam)", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start detection based on source
def start_detection():
    choice = source_var.get()
    if choice == "Image":
        path = filedialog.askopenfilename(title="Select an image", filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if path:
            detect_on_image(path)
    elif choice == "Video":
        path = filedialog.askopenfilename(title="Select a video", filetypes=[("Videos", "*.mp4 *.avi *.mov")])
        if path:
            detect_on_video(path)
    elif choice == "Webcam":
        detect_on_webcam()

# GUI
def create_gui():
    global toggle_alarm_button
    root = tk.Tk()
    root.title("🔥 Fire Detection System")
    root.geometry("350x250")

    tk.Label(root, text="Choose input source:", font=("Arial", 12)).pack(pady=10)

    options = ["Image", "Video", "Webcam"]
    global source_var
    source_var = tk.StringVar(value="Webcam")

    tk.OptionMenu(root, source_var, *options).pack(pady=10)

    tk.Button(root, text="Start Detection", width=20, height=2,
              command=lambda: threading.Thread(target=start_detection).start()).pack(pady=10)

    toggle_alarm_button = tk.Button(root, text="Start Alarm", width=20, height=2, command=toggle_alarm)
    toggle_alarm_button.pack(pady=10)

    root.mainloop()

def monitor_fire_timeout():
    while True:
        time.sleep(1)
        check_alarm_timeout()

threading.Thread(target=monitor_fire_timeout, daemon=True).start()

# Launch GUI
create_gui()
