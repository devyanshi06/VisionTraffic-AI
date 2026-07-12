import cv2
import numpy as np
from ultralytics import YOLO
import torch

class TrafficAnalyticsEngine:
    def __init__(self, video_source="traffic.mp4"):
        # Initialize YOLOv8 Nano
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = YOLO("yolov8n.pt") 
        if self.device == "cuda":
            self.model.to(self.device)
        
        # Establish video reader hook
        self.cap = cv2.VideoCapture(video_source)
        
        # Tracking logic persistent attributes
        self.tracked_vehicle_ids = set()
        self.total_passed_count = 0
        self.frame_counter = 0

    def process_next_frame(self, conf_threshold=0.20):
        if not self.cap.isOpened():
            return None

        # ⚡ FIXED TYPO: Replaced cv2.read(cap) with standard cap.read()
        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            return None

        self.frame_counter += 1
        height, width, _ = frame.shape
        # Establish the blue gate line right across the horizontal center matrix
        counting_line_y = int(height * 0.5)

        # Leverage ByteTrack algorithm to map top-down roofs securely
        results = self.model.track(
            frame, 
            classes=[2, 3, 5, 7], 
            conf=conf_threshold, 
            persist=True, 
            tracker="bytetrack.yaml", 
            device=self.device,
            verbose=False
        )

        # Check if active trackers exist in current frame processing arrays
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)

            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = box
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                # Overlay target track marker dot
                cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)

                # Threshold window check area (15 pixels buffer) to avoid skipping fast vehicle updates
                if abs(cy - counting_line_y) < 15:
                    if track_id not in self.tracked_vehicle_ids:
                        self.tracked_vehicle_ids.add(track_id)
                        self.total_passed_count += 1

        # Generate the standard background box visualization elements
        annotated_frame = results[0].plot() if results[0].boxes.id is not None else frame
        
        # Superimpose the physical Gate Line marker
        cv2.line(annotated_frame, (0, counting_line_y), (width, counting_line_y), (255, 0, 0), 3)

        # Scale down image dimensions slightly for hyper-smooth web rendering transfer
        display_frame = cv2.resize(annotated_frame, (720, 405))
        rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)

        # 🚀 Return the analytical package data back to your friend's app.py frontend
        return {
            "frame": rgb_frame,
            "count": self.total_passed_count,
            "frame_idx": self.frame_counter
        }

    def close(self):
        if self.cap.isOpened():
            self.cap.release()