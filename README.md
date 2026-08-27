# ✋ Hand Gesture Volume Control

> Control your Windows system volume in real-time using hand gestures captured via webcam.

---

## 📋 Overview

This project uses **computer vision** and **hand tracking** to let you control your system volume naturally — just by pinching your thumb and index finger together or spreading them apart. The distance between your thumb tip and index finger tip is mapped directly to your Windows master volume level.

---

## 🎯 Features

- 🖐️ **Real-time hand detection** using MediaPipe Hand Landmarker
- 🔊 **System volume control** via Windows Core Audio API (pycaw)
- 📊 **Live volume bar** overlay on the video feed
- 🎨 **Visual hand skeleton** rendering with landmarks
- 🪞 **Mirrored webcam feed** for intuitive interaction
- ⚡ **Lightweight & fast** — runs smoothly on standard webcams

---

## 🔄 System Flow

```
Webcam
   ↓
OpenCV Captures Frame
   ↓
Convert BGR → RGB
   ↓
Create MediaPipe Image
   ↓
MediaPipe Hand Landmarker
   ↓
Detect Hand Landmarks
   ↓
Extract Thumb Tip (4)
and Index Finger Tip (8)
   ↓
Calculate Euclidean Distance
   ↓
Clamp Distance
   ↓
Normalize Distance (0 → 1)
   ↓
Map to Windows Volume Range
   ↓
Set Windows Master Volume
   ↓
Display Hand Landmarks and Volume
```

---

## 🛠️ Prerequisites

- **Python 3.8+**
- **Windows OS** (required for `pycaw` volume control)
- A working **webcam**
- MediaPipe **Hand Landmarker model file** (`hand_landmarker.task`)

---

## 📦 Installation

### 1. Clone or download the repository

```bash
git clone <your-repo-url>
cd hand-gesture-volume-control
```

### 2. Install dependencies

```bash
pip install opencv-python mediapipe pycaw comtypes
```

### 3. Download the MediaPipe Hand Landmarker model

Download `hand_landmarker.task` from the [MediaPipe Models](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker#models) page and place it in the project root directory.

---

## 📁 Project Structure

```
hand-gesture-volume-control/
│
├── volume_control_module.py      # HandVolumeController class (detection + volume logic)
├── main.py                        # Main application script (webcam loop + UI)
├── hand_landmarker.task           # MediaPipe Hand Landmarker model (download separately)
└── README.md                      # This file
```

### `volume_control_module.py`
Contains the `HandVolumeController` class which handles:
- MediaPipe hand landmark detection
- Euclidean distance calculation between thumb (4) and index finger (8)
- Distance-to-volume mapping and Windows volume setting
- Hand skeleton drawing on frames

### `main.py`
The entry point that:
- Opens the webcam via OpenCV
- Runs the detection loop
- Renders the volume bar and on-screen info
- Handles the "Press Q to quit" logic

---

## 🚀 Usage

### Run the application

```bash
python main.py
```

### How to use

1. **Launch** the script — a window titled *"Gesture Volume Control"* will open.
2. **Show your hand** to the webcam.
3. **Pinch** your thumb and index finger together to **lower** the volume.
4. **Spread** them apart to **raise** the volume.
5. **Press `Q`** to exit.

---

## ⚙️ Configuration

You can tweak the following values in `volume_control_module.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_distance` | `30` | Minimum pixel distance (maps to 0% volume) |
| `max_distance` | `200` | Maximum pixel distance (maps to 100% volume) |
| `num_hands` | `1` | Number of hands to track |
| `model_path` | `"hand_landmarker.task"` | Path to the MediaPipe model |

> **Tip:** Adjust `min_distance` and `max_distance` based on your camera resolution and how far you sit from the webcam.

---

## 🧠 How It Works

### 1. Hand Detection
MediaPipe's Hand Landmarker processes each video frame and returns 21 hand landmarks with normalized `(x, y, z)` coordinates.

### 2. Landmark Extraction
The system specifically tracks:
- **Landmark 4** — Thumb Tip
- **Landmark 8** — Index Finger Tip

### 3. Distance Calculation
The Euclidean distance between these two points is computed in pixel space:

```
distance = √((x₂ - x₁)² + (y₂ - y₁)²)
```

### 4. Volume Mapping
The raw distance is:
1. **Clamped** to the `[min_distance, max_distance]` range
2. **Normalized** to a `[0, 1]` value
3. **Scaled** to your system's actual volume range (typically `-65.25 dB` to `0 dB` on Windows)
4. **Applied** via the Windows Core Audio API

### 5. Visualization
The app overlays:
- A **green hand skeleton** with connection lines
- A **cyan line** between thumb and index finger
- A **vertical volume bar** on the left side
- **Volume percentage** and **distance** text

---

## 🖼️ On-Screen Display

| Element | Description |
|---------|-------------|
| Green dots & blue lines | Hand skeleton |
| Cyan line + red circles | Thumb-index distance indicator |
| White-bordered green bar | Volume level (0–100%) |
| "Volume: X%" | Current system volume |
| "Distance: X" | Raw pixel distance |
| "Show your hand" | Appears when no hand is detected |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `hand_landmarker.task not found` | Download the model from MediaPipe and place it in the project folder |
| Webcam not opening | Check if another app is using the camera; try changing `cv.VideoCapture(0)` to `cv.VideoCapture(1)` |
| Volume not changing | Ensure you're on **Windows** — `pycaw` only works on Windows |
| Low FPS | Close other heavy applications; lower webcam resolution if needed |
| Hand not detected | Ensure good lighting and keep your hand within the camera frame |

---

## 📚 Dependencies

| Package | Purpose |
|---------|---------|
| `opencv-python` | Webcam capture and image rendering |
| `mediapipe` | Hand landmark detection |
| `pycaw` | Windows volume control |
| `comtypes` | COM interface for Windows audio |

---

## 🔮 Future Improvements

- [ ] Add support for **both hands** (e.g., one for volume, one for mute)
- [ ] Implement a **mute gesture** (e.g., fist or specific pose)
- [ ] Add **smooth volume transitions** with exponential moving average
- [ ] Configurable **sensitivity settings** via a settings file
- [ ] Cross-platform support (macOS/Linux with alternative volume libraries)

---

## 👤 Author

**Ali Sher** — Developer

- 💼 [LinkedIn](https://www.linkedin.com/in/alisherml/)
- 🐙 [GitHub](https://github.com/alisherml)

---

## 📄 License

This project is open-source. Feel free to use, modify, and distribute.

---

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) by Google for the hand tracking model
- [pycaw](https://github.com/AndreMiras/pycaw) for Windows audio control
- [OpenCV](https://opencv.org/) for computer vision utilities

---

> 💡 **Pro Tip:** Sit about 1–2 feet from your webcam in a well-lit room for the best hand detection accuracy.
