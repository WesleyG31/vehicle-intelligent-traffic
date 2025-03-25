# 🚦 Intelligent Traffic Analysis System (YOLOv8 + OCR + Streamlit)

An end-to-end **vehicle detection and traffic monitoring system** powered by **Computer Vision** and **Deep Learning**. This project is designed for real-world applications like smart cities, traffic law enforcement, autonomous mobility, and urban analytics.

Deployed with **Streamlit** and hosted via **Hugging Face Spaces** using a custom **Docker** environment.

---

## 📸 What it Does

- 🚗 Detects cars, buses, motorbikes, pedestrians, and trams
- 🧠 Tracks individual vehicles over time with object IDs
- ⚡ Estimates real speed using perspective transformation
- 🚨 Detects speed violations
- 🔍 Reads license plates using OCR (EasyOCR)
- 📊 Generates real-time traffic statistics
- 📄 Outputs automatic PDF report with charts and violations
- 🌐 Allows users to upload their own videos via web app

---

## 🧠 Technologies Used

| Component       | Tech Stack                        |
|----------------|------------------------------------|
| Object Detection | YOLOv8 (Ultralytics)              |
| Tracking         | Built-in Tracker / DeepSORT       |
| Speed Estimation | OpenCV + Perspective Geometry     |
| OCR              | EasyOCR                           |
| Dashboard        | Streamlit                         |
| Deployment       | Hugging Face Spaces + Docker      |
| Visualization    | Matplotlib, Seaborn               |
| Report Generation| FPDF                              |

---

## 📂 Project Structure

```
├── streamlit_app.py          # Web interface
├── src/
│   ├── pipeline/             # Main pipeline (process_video)
│   ├── speed_analysis/       # Speed estimator
│   ├── analytics/            # Charts & statistics
│   ├── reports/              # PDF generator
│   └── utils/                # Video saving, perspective points
├── data/
│   ├── output_data/          # Output: video, csv, report
│   └── videos/               # Input test videos
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🚀 How to Run It Locally

1. Clone the repo
```bash
git clone https://github.com/your-username/vehicle-intelligent-traffic.git
cd vehicle-intelligent-traffic
```

2. (Optional) Create a virtual environment
```bash
conda create -n traffic python=3.10
conda activate traffic
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the app locally
```bash
streamlit run streamlit_app.py
```

5. Upload a video (`.mp4`) and get real-time results, charts, and PDF report

---

## 🌐 Try the Live Demo

> [![Hugging Face Space](https://img.shields.io/badge/🚀%20Try%20on-Hugging%20Face-blue?logo=huggingface)](https://huggingface.co/spaces/your-username/vehicle-intelligent-traffic)

No installation required. Just open the link and upload a traffic video!

---

## 🧪 Example Use Cases

- 🚓 Speed enforcement with license plate capture
- 🧠 Urban analytics and vehicle density mapping
- 🚦 Smart city infrastructure and automation
- 🤖 Robotics & autonomous navigation input

---

## 📄 Sample Outputs

- ✅ Annotated video with speed overlays
- ✅ CSV with tracking and violations
- ✅ Charts: vehicle count, average speed
- ✅ Auto-generated PDF report

---

## 💼 Why This Project Matters

This project demonstrates:
- End-to-end pipeline (from detection to deployment)
- Real-time processing with computer vision
- Integration of multiple advanced AI components
- Hands-on understanding of AI for mobility and cities

> ✅ Perfect for companies in robotics, smart mobility, autonomous vehicles, and AI-driven urban systems.

---

## 👨‍💻 Author

**[Your Full Name]**  
Computer Vision & AI Engineer  
📫 [your.email@example.com]  
🔗 [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)  
🌐 [yourportfolio.com](https://yourportfolio.com)

---

## 🪪 License

This project is licensed under the MIT License.