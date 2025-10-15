import cv2
import time
import numpy as np
from ultralytics import YOLO
from llm_for_tts import print_message
import threading
import torch
# Global dictionaries for tracking object positions and speeds
last_message_time = 0
prev_positions = {}   # track_id -> (cx, cy)
frame_time = {}       # track_id -> last update time
last_speeds = {}      # track_id -> last speed

def calculate_distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    distance = np.sqrt(dx**2 + dy**2)
    direction_sign = -np.sign(dy) if dy != 0 else 1
    return distance, direction_sign

def calculate_speed(distance, fps, direction_sign):
    scaling_factor = 30  # pixels ≈ 1 meter
    speed = (distance / scaling_factor) * fps * 3.6  # km/h
    return speed * direction_sign

def result_boxes_pred(frame, results, model, conf_threshold=0.6, fps=30):
    global prev_positions, frame_time, last_speeds

    detected_info = []
    current_ids = set()

    for r in results:
        boxes = r.boxes
        if len(boxes) == 0:
            continue

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            if conf < conf_threshold:
                continue

            cls = int(box.cls[0])
            label = model.names[cls]

            # Create a pseudo track_id using label + grid cell
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            track_id = f"{label}_{cx//50}_{cy//50}"
            current_ids.add(track_id)

            # Speed calculation
            speed = 0.0
            current_time = time.time()
            if track_id in prev_positions:
                prev_pt = prev_positions[track_id]
                dt = current_time - frame_time.get(track_id, current_time)
                if dt > 0:
                    distance_val, direction_sign = calculate_distance(prev_pt, (cx, cy))
                    speed = calculate_speed(distance_val, 1 / dt, direction_sign)
                    last_speeds[track_id] = speed
            else:
                last_speeds[track_id] = 0.0

            prev_positions[track_id] = (cx, cy)
            frame_time[track_id] = current_time

            # Draw box & label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f} {speed:.1f} km/h",
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

            detected_info.append((label, track_id, speed))

    # Handle no detections case
    if not detected_info:
        cv2.putText(frame, "No objects detected", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return frame, detected_info

def run_realtime_detection(model, camera_index=0):
    global last_message_time
    cap = cv2.VideoCapture(camera_index)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, stream=True,device=device)
        frame, detected_info = result_boxes_pred(frame, results, model, fps=fps)

        cv2.imshow("YOLOv8 Real-Time Detection with Speed", frame)

        # Prepare message list
        message_list = []
        if detected_info:
            for obj in detected_info:
                label, track_id, speed = obj
                speed=float(speed)
                message_list.append([label, speed])

            # Throttle output to 1 second
            current_time = time.time()
            if current_time - last_message_time >= 10:
                if(len(message_list)>0):
                    threading.Thread(target=print_message, args=(message_list,)).start()
                    last_message_time = current_time
        else:
            print("No objects detected.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    model = YOLO("./runs/detect/train2/weights/best.pt")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    run_realtime_detection(model)