# Buddy 🖲️

An intelligent camera system that automatically detects and centers the user's face using computer vision and PID control. Developed as a project for the Process Control course at UTFPR (Federal University of Technology - Paraná).

## 📋 Overview

Buddy is a face-tracking camera system that combines computer vision with hardware control to keep a detected face centered in the camera frame. The system uses:

- **Computer Vision**: OpenCV Haar Cascade classifier for real-time face detection
- **Control System**: PID controllers for precise pan and tilt servo positioning
- **Hardware Interface**: Arduino microcontroller with servo motors
- **Python Architecture**: Modular, threaded design for optimal performance

## ✨ Features

- **Real-time Face Detection**: Uses Haar Cascade classifier for efficient face detection
- **Automatic Tracking**: Continuously adjusts camera position to keep face centered
- **PID Control**: Dual PID controllers for smooth and accurate pan/tilt movements
- **Threaded Processing**: Separate threads for frame capture and processing
- **Serial Communication**: Automatic Arduino port detection and communication
- **Visual Feedback**: Real-time display with face detection overlay

## 🏗️ Architecture

```
buddy/
├── firmware/           # Arduino firmware for servo control
│   └── firmware.ino   # Servo control logic
├── src/
│   └── buddy/
│       ├── __init__.py      # Main Buddy class
│       ├── __main__.py      # Entry point
│       ├── utils.py         # Utility functions
│       ├── core/
│       │   ├── communication.py  # Serial communication with Arduino
│       │   ├── controllers.py    # PID controller implementation
│       │   ├── detectors.py      # Face detection algorithms
│       │   └── track.py          # Camera and tracking logic
│       └── models/
│           ├── configs.py   # Configuration models
│           ├── dto.py       # Data transfer objects
│           ├── objects.py   # Core data structures
│           └── states.py    # State classifications
```

## 🔧 Hardware Requirements

- **Microcontroller**: Arduino (Uno, Nano, or compatible)
- **Servos**: 2x servo motors (pan and tilt)
  - Pan servo: Connected to pin 6
  - Tilt servo: Connected to pin 3
- **Camera**: USB webcam or laptop camera
- **Mounting**: Pan-tilt mechanism for camera mounting

### Wiring Diagram

```
Arduino Pin 6  → Pan Servo (Signal)
Arduino Pin 3  → Tilt Servo (Signal)
Arduino 5V     → Servos (VCC)
Arduino GND    → Servos (GND)
```

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/benhuuur/buddy.git
cd buddy
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Requirements:**
- `numpy==2.2.6`
- `opencv-python==4.12.0.88`
- `pyserial` (for Arduino communication)

### 3. Upload Firmware to Arduino

1. Open `firmware/firmware.ino` in Arduino IDE
2. Select your Arduino board and port
3. Upload the sketch to your Arduino

## 💻 Usage

### Basic Usage

```bash
python -m src.buddy
```

### Configuration

Edit `src/buddy/__main__.py` to adjust parameters:

```python
camera = Camera(1)              # Camera index (0 for default, 1 for external)
detector = Cascade(0.5)         # Detection ratio (lower = faster, less accurate)
tracker = Tracker(camera, detector)

# PID parameters: (setpoint, kp, ki, kd, inverted)
pan_pid = PID(3.0, 3.8167, 0.5895, 0.5, False)
tilt_pid = PID(3.0, 5.5577, 0., 0.5, False)

buddy = Buddy(tracker, Arduino(), pan_pid, tilt_pid)
buddy.run()
```

### Controls

- **Q** or **ESC**: Quit the application

## 🎛️ PID Tuning

The system uses two PID controllers:

### Pan Controller (Horizontal)
- **Kp**: TODO (Proportional gain)
- **Ki**: TODO (Integral gain)
- **Kd**: TODO (Derivative gain)

### Tilt Controller (Vertical)
- **Kp**: TODO (Proportional gain)
- **Ki**: TODO (Integral gain)
- **Kd**: TODO (Derivative gain)

To tune PID values for your setup:
1. Start with P-only control (set Ki and Kd to 0)
2. Increase Kp until system oscillates
3. Add Kd to reduce oscillations
4. Add Ki to eliminate steady-state error

## 🔬 How It Works

1. **Frame Capture**: Camera continuously captures video frames in a separate thread
2. **Face Detection**: Haar Cascade classifier detects faces in frames
3. **Position Calculation**: Face center position is normalized to frame dimensions
4. **Error Calculation**: PID controllers compute error from center (setpoint = 0.5)
5. **Control Signal**: Error is converted to servo movement commands
6. **Serial Communication**: Commands sent to Arduino via serial port
7. **Servo Movement**: Arduino adjusts pan/tilt servos to center the face

## 📊 System Components

### Detector
- Uses OpenCV's Haar Cascade classifier
- Configurable detection ratio for performance tuning
- Returns face positions and dimensions

### Tracker
- Manages camera capture in dedicated thread
- Processes frames for face detection
- Maintains queue-based frame buffering

### Controller (PID)
- Implements standard PID algorithm
- Separate controllers for pan and tilt axes
- Tunable gains for system optimization

### Communication (Arduino)
- Auto-detects Arduino port
- Serial communication at 9600 baud
- Command format: `"pan;tilt\n"`

## 🐛 Troubleshooting

### Camera Not Found
```python
camera = Camera(0)  # Try different indices: 0, 1, 2...
```

### Arduino Not Detected
- Check USB connection
- Verify correct drivers are installed
- Manually specify port: `Arduino(port='COM3')`

### Poor Detection Performance
```python
detector = Cascade(0.5)  # Adjust ratio: higher = better quality, slower
```

### Servo Limits
Servos are constrained to:
- Pan: 0° to 180°
- Tilt: 20° to 175°

## 📝 License

This project is licensed under the terms specified in the LICENSE file.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 👨‍💻 Author

**benhuuur**
- GitHub: [@benhuuur](https://github.com/benhuuur)

## 🎓 Academic Context

This project was developed as part of the Process Control course at UTFPR (Federal University of Technology - Paraná), demonstrating practical applications of:
- PID control theory
- Real-time computer vision
- Hardware-software integration
- Embedded systems programming

---

**Note**: Ensure proper servo power supply to avoid brownouts. For multiple servos or high-torque servos, use an external power source.
