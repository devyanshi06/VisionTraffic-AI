import cv2
import numpy as np
from ultralytics import YOLO
import torch

class TrafficAnalyticsEngine:
    def __init__(self, video_source="traffic.mp4"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = YOLO("yolov8n.pt") 
        if self.device == "cuda":
            self.model.to(self.device)
        
        self.cap = cv2.VideoCapture(video_source)
        self.counted_footprints = []
        self.total_passed_count = 0
        self.frame_counter = 0

    def process_next_frame(self, conf_threshold=0.20):
        if not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            return None

        self.frame_counter += 1
        height, width, _ = frame.shape
        
        # 🚀 MOVING GATES NORTH & SPACING THEM FOR TWO LANES
        line_north_y = int(height * 0.40) # Line 1 (Further up the screen)
        line_south_y = int(height * 0.55) # Line 2 (Second Lane)

        results = self.model.predict(
            frame, 
            classes=[2, 3, 5, 7], 
            conf=conf_threshold, 
            imgsz=640,
            device=self.device,
            verbose=False
        )

        self.counted_footprints = [f for f in self.counted_footprints if self.frame_counter - f[2] < 30]

        if results[0].boxes is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()

            for box in boxes:
                x1, y1, x2, y2 = box
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)

                # ⚡ CHECK BOTH GATES IN A SINGLE PASS
                is_near_gate_1 = abs(cy - line_north_y) < 35
                is_near_gate_2 = abs(cy - line_south_y) < 35

                if is_near_gate_1 or is_near_gate_2:
                    already_logged = False
                    for past_cx, past_cy, _ in self.counted_footprints:
                        distance = np.hypot(cx - past_cx, cy - past_cy)
                        if distance < 50:
                            already_logged = True
                            break
                    
                    if not already_logged:
                        self.total_passed_count += 1
                        self.counted_footprints.append((cx, cy, self.frame_counter))

        # 🎨 RENDER BOTH BOUNDARY TELEMETRY LINES
        cv2.line(frame, (0, line_north_y), (width, line_north_y), (255, 0, 0), 3) # Lane 1
        cv2.line(frame, (0, line_south_y), (width, line_south_y), (255, 0, 0), 3) # Lane 2
        
        cv2.putText(frame, "LANE 1 - NORTH GATE", (20, line_north_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, "LANE 2 - SOUTH GATE", (20, line_south_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        display_frame = cv2.resize(frame, (720, 405))
        rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)

        return {
            "frame": rgb_frame,
            "count": self.total_passed_count,
            "frame_idx": self.frame_counter
        }

    def close(self):
        if self.cap.isOpened():
            self.cap.release()