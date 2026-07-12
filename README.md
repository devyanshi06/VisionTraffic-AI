# VisionTraffic AI 🚦

An intelligent, real-time traffic monitoring and transport operations platform built in 8 hours for the hackathon. `VisionTraffic AI` leverages computer vision to transform standard traffic camera feeds into actionable, live analytics for smart city management.

## 🚀 Features
* **Real-Time Vehicle Detection:** Utilizes a pre-trained YOLOv8 model to instantly identify and classify cars, trucks, buses, and motorbikes.
* **Density & Congestion Analytics:** Dynamically calculates traffic density per frame to flag high-congestion zones (Red/Yellow/Green statuses).
* **Live Operations Dashboard:** A responsive Streamlit-based interface displaying live metrics, traffic flow graphs, and automated routing alerts.
* **Hardware-Ready Logic:** Simulated API payload triggers designed to interface with smart city infrastructure (like adaptive traffic signals).

## 🛠️ Tech Stack
* **Machine Learning & CV:** Python, OpenCV, Ultralytics YOLOv8
* **Dashboard / Frontend:** Streamlit
* **Data Processing:** Pandas, NumPy

## 📦 Quick Start

### 1. Clone the repository
```bash
git clone [https://github.com/devyanshi06/VisionTraffic-AI.git](https://github.com/devyanshi06/VisionTraffic-AI.git)
cd VisionTraffic-AI
