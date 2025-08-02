# ✋ Rock Paper Scissors — Ultimate Version (with Webcam & AI)

A next-level Rock Paper Scissors game built with **Python**, using **OpenCV**, **MediaPipe**, and basic **AI/ML logic** for different difficulty modes. Play using hand gestures via your **webcam**, or traditional keyboard input.

---

## 🎮 Game Modes

| Mode           | Description |
|----------------|-------------|
| 🟢 Beginner     | Random machine choices (no AI) |
| 🟡 Intermediate | Computer adapts based on simple patterns |
| 🔵 Expert       | Uses a transition matrix (basic ML-style prediction) |
| 🔴 Super Hard   | Very difficult AI with improved logic |
| 🟣 Big Bang Mode (Hidden) | Inspired by *Sheldon Cooper’s* Rock-Paper-Scissors-Lizard-Spock |

To unlock Big Bang mode, enter **`73`** as the game mode — a nod to Sheldon's favorite number.

---

## ✋ Webcam Hand Gesture Detection

- ✊ **Rock**: Fist or few fingers extended  

- ✋ **Paper**: 4 or 5 fingers extended  

- ✌️ **Scissors**: Exactly 2 fingers extended  

Webcam-based play uses **MediaPipe** to detect hand gestures in real time.

---

## 🧠 Technologies Used

- [Python 3](https://www.python.org/)

- [OpenCV](https://opencv.org/) – for camera and visualization

- [MediaPipe](https://google.github.io/mediapipe/) – hand tracking

- [NumPy](https://numpy.org/) – array handling

- Basic AI / Transition Matrix for learning opponent moves

---

## 💻 How to Run

1. **Clone the repository**:
   ```
   git clone https://github.com/Sathvik-Tumati/Rock-Paper-Scissors-with-OpenCV.git
   cd Rock-Paper-Scissors-with-OpenCV

2. **Install dependencies**:
   ```
    pip install -r requirements.txt

3. **Run the game**:
   ```
   python fullRPS.py

📦 **Requirements**

All dependencies are listed in requirements.txt, including:

opencv-python

mediapipe

numpy
