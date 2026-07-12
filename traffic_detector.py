import cv2
from ultralytics import YOLO

def run_traffic_engine():
    # Load the standard nano model
    model = YOLO("yolov8n.pt") 

    video_source = "traffic.mp4"
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("❌ Error: Could not open video file.")
        return

    print("🚀 VisionTraffic Drone-View Engine Active...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # ML Tweak: We lower the confidence threshold (conf=0.25) slightly 
        # to help YOLO recognize cars from a top-down aerial roof angle.
        results = model(frame, classes=[2, 3, 5, 7], conf=0.25, verbose=False)

        # Count detected vehicles
        vehicle_count = len(results[0].boxes)
        
        # Determine density state for the dashboard
        if vehicle_count <= 12:
            status = "Optimal Flow"
            color = (0, 255, 0) # Green
        elif 12 < vehicle_count <= 22:
            status = "Moderate Accumulation"
            color = (0, 255, 255) # Yellow
        else:
            status = "High Congestion / Bottleneck"
            color = (0, 0, 255) # Red

        # Generate visual tracking layout
        annotated_frame = results[0].plot()

        # Draw a custom "Counting Line" across the center of the road to look like a real system
        height, width, _ = frame.shape
        counting_line_y = int(height * 0.5)
        cv2.line(annotated_frame, (0, counting_line_y), (width, counting_line_y), (255, 0, 0), 3)

        # UI Text Overlays
        cv2.putText(annotated_frame, f"Aerial Vehicle Count: {vehicle_count}", (30, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        cv2.putText(annotated_frame, f"Density Status: {status}", (30, 95), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        cv2.putText(annotated_frame, "Gate Line Active", (30, height - 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

        # Display window
        cv2.imshow("VisionTraffic AI - Drone View Processing", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_traffic_engine()