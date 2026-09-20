



# Real-Time Edge Traffic Analytics & Vehicle Telemetry Pipeline

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![YOLO11](https://img.shields.io/badge/Model-YOLO11%20Nano-00FFFF?style=for-the-badge&logo=ultralytics&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![ONNX Runtime](https://img.shields.io/badge/Inference-ONNX%20Runtime%20GPU-005CED?style=for-the-badge&logo=onnx&logoColor=white)](https://onnxruntime.ai/)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV%204.8-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![Roboflow](https://img.shields.io/badge/Dataset-Roboflow%20Universe-6706CE?style=for-the-badge&logo=roboflow&logoColor=white)](https://roboflow.com/)

An end-to-end edge computer vision pipeline engineered for multi-vehicle detection, persistent tracking, real-time velocity estimation, and structured telemetry logging from 1080p highway surveillance feeds.

---

## 🚀 Key Highlights & Engineering Features

* **SOTA Vision Backbone:** Powered by **YOLO11 nano**, optimized for low parameter footprint, high mAP, and robust detection across 4 primary vehicle classes (Cars, Motorcycles, Buses, Trucks).
* **Multi-Object Tracking (MOT):** Integrates **ByteTrack** association algorithms to maintain track persistence through temporary occlusions, lane switches, and dense traffic conditions.
* **Calibrated Velocity Estimation:** Uses dual virtual tripwires and Euclidean displacement algorithms to calculate vehicle speeds in real-time ($km/h$) with $<4\%$ duplicate count error.
* **High-Throughput Edge Pipeline:** Features an asynchronous, multi-threaded video stream ingest worker (`ThreadedVideoStream`) coupled with an **ONNX graph runtime**, achieving **45+ FPS** on consumer-grade NVIDIA RTX hardware.
* **Automated Telemetry Sink:** Continuously logs vehicle IDs, timestamps, classes, speed measurements, and overspeed infraction flags into a structured CSV data sink.
* **Custom Dataset Pipeline:** Fully integrated with **Roboflow** for dataset ingestion, domain-specific augmentation (low light, glare, occlusion), and transfer learning.

---

## 🏗️ System Architecture

```text
               +----------------------------------+
               |   1080p Highway Video Stream     |
               +-----------------+----------------+
                                 |
                                 v
               +----------------------------------+
               |  Threaded Ingestion Worker (I/O) |
               +-----------------+----------------+
                                 | (Asynchronous Frame Queue)
                                 v
               +----------------------------------+
               |  YOLO11 Nano ONNX Runtime Engine |
               +-----------------+----------------+
                                 | (Detections + Confidence Scores)
                                 v
               +----------------------------------+
               |   ByteTrack State Association    |
               +-----------------+----------------+
                                 | (Persistent Object IDs)
                                 v
               +----------------------------------+
               |    Dual Virtual Tripwire Math    |
               |  v = (Distance / Δt) * 3.6 km/h  |
               +-----------------+----------------+
                                 |
        +------------------------+------------------------+
        |                                                 |
        v                                                 v
+-------------------------------+         +-------------------------------+
|    Live HUD Overlay Display   |         | Structured CSV Telemetry Sink |
|  - Real-time FPS (45+)        |         |  - Timestamps & Track IDs     |
|  - Vehicle Class Counts       |         |  - Instantaneous Velocity     |
|  - Speed Infraction Warnings  |         |  - Compliance Status Flags    |
+-------------------------------+         +-------------------------------+


https://github.com/user-attachments/assets/cde158bb-3e94-4d29-8f74-5c716dcb8dae

