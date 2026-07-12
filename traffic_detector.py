import cv2
from ultralytics import YOLO

def run_traffic_engine():
    # Initialize YOLOv8 Nano
    model = YOLO("yolov8n.pt") 
    
    # Establish video reader hook
    video_source = "traffic.mp4"
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("❌ Error: Could not open video file.")
        return

    # Track tracking logic persistent attributes
    tracked_vehicle_ids = set()
    total_passed_count = 0

    print("🚀 VisionTraffic Drone Counting Engine Online...")

    while cap.isOpened():
        ret, frame = cv2.read(cap) if hasattr(cap, 'read') else cap.read()
        if not ret:
            break

        height, width, _ = frame.shape
        # Establish the blue gate line right across the horizontal center matrix
        counting_line_y = int(height * 0.5)

        # Leverage ByteTrack algorithm to map top-down roofs securely
        results = model.track(frame, classes=[2, 3, 5, 7], conf=0.20, persist=True, tracker="bytetrack.yaml", verbose=False)

        # Check if active trackers exist in current frame processing arrays
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)

            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = box
                # Pinpoint exact center pixel point coordinates
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                # Overlay target track tracker marker dot
                cv2.circle(frame, (cx, cy), 4, (0, 255, 255), -1)

                # Threshold window check area (15 pixels buffer) to avoid skipping fast vehicle updates
                if abs(cy - counting_line_y) < 15:
                    if track_id not in tracked_vehicle_ids:
                        tracked_vehicle_ids.add(track_id)
                        total_passed_count += 1

        # Generate the standard background box visualization elements
        annotated_frame = results[0].plot() if results[0].boxes.id is not None else frame
        
        # Superimpose the physical Gate Line marker
        cv2.line(annotated_frame, (0, counting_line_y), (width, counting_line_y), (255, 0, 0), 3)

        # Render Information Overlays
        cv2.putText(annotated_frame, f"Vehicles Passed: {total_passed_count}", (30, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)

        cv2.imshow("VisionTraffic Engine - Terminal Test", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_traffic_engine()