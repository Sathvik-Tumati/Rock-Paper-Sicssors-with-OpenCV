#!/usr/bin/env python3
import random
import cv2
import mediapipe as mp
import numpy as np

# ANSI escape codes for color formatting
X = '\033[0m'
Bold = '\033[1;36m'
HighB = '\033[1;44m'

# Game stats tracking
winEas = loseEas = tieEas = winInt = loseInt = tieInt = winHard = loseHard = tieHard = winExp = loseExp = tieExp = winspec = losespec = tiespec = 0.0
hiddenfound = False

# Transition matrices for expert mode
buildTMatrix = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
buildTMatrixL = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
buildTMatrixT = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
n = 3
m = 3
tMatrix = [[0] * m for i in range(n)]
tMatrixL = [[0] * m for i in range(n)]
tMatrixT = [[0] * m for i in range(n)]
probabilitiesRPS = [1/3, 1/3, 1/3]

# For Big Bang Mode
buildTMatrixrpsclsp = {'rr': 1, 'rp': 1, 'rsc': 1, 'rl': 1, 'rsp': 1, 'pr': 1, 'pp': 1, 'psc': 1, 'pl': 1, 'psp': 1,
                       'scr': 1, 'scp': 1, 'scsc': 1, 'scl': 1, 'scsp': 1, 'lr': 1, 'lp': 1, 'lsc': 1, 'll': 1, 'lsp': 1,
                       'spr': 1, 'spp': 1, 'spsc': 1, 'spl': 1, 'spsp': 1}
buildTMatrixLrpsclsp = buildTMatrixTrpsclsp = buildTMatrixrpsclsp.copy()
sheldon = 5
cooper = 5
tMatrixrpsclsp = [[0] * sheldon for _ in range(cooper)]
tMatrixLrpsclsp = [[0] * sheldon for _ in range(cooper)]
tMatrixTrpsclsp = [[0] * sheldon for _ in range(cooper)]
probabilitiesrpsclsp = [1/5, 1/5, 1/5, 1/5, 1/5]

# Gesture detection setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

intro = """
Welcome to Rock Paper Scissors the Ultimate Version! There are four modes: Beginner, Intermediate, Expert, and Super Hard. 
Beginner is random, Intermediate uses AI, Expert uses Machine Learning, and Super Hard is... well... super hard.
There's also a hidden Sheldon Cooper-level mode unlocked by entering 73!

Now, you can play using hand gestures via webcam!
"""

print(Bold)
print(intro)
print(X)

# === HAND GESTURE DETECTION FUNCTIONS ===
def get_hand_gesture(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    result = hands.process(frame_rgb)
    gesture = None

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            landmarks = [(lm.x, lm.y) for lm in handLms.landmark]
            extended_fingers = 0

            # Thumb
            if landmarks[4][0] < landmarks[3][0]: extended_fingers += 1
            # Index
            if landmarks[8][1] < landmarks[7][1]: extended_fingers += 1
            # Middle
            if landmarks[12][1] < landmarks[11][1]: extended_fingers += 1
            # Ring
            if landmarks[16][1] < landmarks[15][1]: extended_fingers += 1
            # Pinky
            if landmarks[20][1] < landmarks[19][1]: extended_fingers += 1

            # Classify gesture
            if extended_fingers == 2: gesture = "Scissors"
            elif extended_fingers >= 4: gesture = "Paper"
            else: gesture = "Rock"

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    return gesture, frame

def capture_gesture():
    cap = cv2.VideoCapture(0)
    print("Show your hand gesture (press 'q' when ready):")

    while True:
        ret, frame = cap.read()
        if not ret: break

        gesture, annotated_frame = get_hand_gesture(frame)

        if gesture:
            cv2.putText(annotated_frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Webcam - Press 'q' to confirm", annotated_frame)
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return map_gesture_to_choice(gesture)

    cap.release()
    cv2.destroyAllWindows()
    return None

def map_gesture_to_choice(gesture):
    return {"Rock": 0, "Paper": 1, "Scissors": 2}.get(gesture, None)

# === GAME LOGIC FUNCTIONS ===
def chooseMode():
    mode = 6
    try:
        mode = int(input("What Mode do you want to play in? 1: beginner, 2: intermediate, 3: expert, or 4: super hard? Enter a number\n"))
    except ValueError:
        print("you must enter an integer\n")
    if mode > 4 and mode != 73:
        print("You must enter an integer less than five\n")
        while mode > 4 and mode != 73:
            try:
                mode = int(input("What Mode do you want to play in? 1: beginner, 2: intermediate, 3: expert, or 4: super hard? Enter a number\n"))
            except ValueError:
                print("you must enter an integer\n")
    return mode

def checkWin(user, machine, mode):
    global winEas, loseEas, tieEas, winInt, loseInt, tieInt, winHard, loseHard, tieHard, winExp, loseExp, tieExp, winspec, losespec, tiespec
    win = tie = False

    if mode == 73:  # Big Bang Mode
        win_conditions = {
            0: [2, 3], 1: [0, 4], 2: [1, 3], 3: [4, 1], 4: [2, 0]
        }
        win = machine in win_conditions[user]
        tie = user == machine
    else:
        win_conditions = {0: 2, 1: 0, 2: 1}
        win = win_conditions.get(user) == machine
        tie = user == machine

    checkStats(0 if win else 1 if not tie else 2, mode)
    return "Win!" if win else "Tied!" if tie else "Lose!"

def checkStats(wlt, modeChosen):
    global winEas, loseEas, tieEas, winInt, loseInt, tieInt, winHard, loseHard, tieHard, winExp, loseExp, tieExp, winspec, losespec, tiespec
    mapping = {
        1: (winEas, loseEas, tieEas),
        2: (winInt, loseInt, tieInt),
        3: (winExp, loseExp, tieExp),
        4: (winHard, loseHard, tieHard),
        73: (winspec, losespec, tiespec)
    }
    if wlt == 0:
        mapping[modeChosen] = (mapping[modeChosen][0] + 1, mapping[modeChosen][1], mapping[modeChosen][2])
    elif wlt == 1:
        mapping[modeChosen] = (mapping[modeChosen][0], mapping[modeChosen][1] + 1, mapping[modeChosen][2])
    else:
        mapping[modeChosen] = (mapping[modeChosen][0], mapping[modeChosen][1], mapping[modeChosen][2] + 1)

# --- MODE IMPLEMENTATIONS ---
def easyMode():
    choices = ["Rock", "Paper", "Scissors"]
    continuePlaying = True

    use_camera = input("Use webcam for input? (yes/no): ").lower() == 'yes'

    while continuePlaying:
        if use_camera:
            choice = capture_gesture()
            if choice is None:
                print("Invalid gesture. Try again.")
                continue
        else:
            try:
                choice = int(input("0: Rock, 1: Paper, 2: Scissors, 5: exit\n"))
            except ValueError:
                print("you must enter an integer\n")
                continue

        if choice == 5:
            print("Thanks for Playing!")
            continuePlaying = False
        else:
            machineChoice = random.randint(0, 2)
            result = checkWin(choice, machineChoice, 1)
            print(f"You chose {choices[choice]}")
            print(f"The machine chose {choices[machineChoice]}")
            print(f"You {result}")

# --- OTHER MODES REMAIN THE SAME (INTERMEDIATE, EXPERT, SUPER HARD, BIG BANG) ---

# You can copy over other mode functions from your original code here unchanged.

# === FINAL STATS DISPLAY ===
def finalstats():
    print(HighB + "Final Stats:" + X)
    # Add all stat printing logic similar to original here...

# === START GAME ===
def main():
    playAgain = True
    while playAgain:
        chosenMode = chooseMode()
        if chosenMode == 1:
            easyMode()
        # Add other modes here
        playAgain = input("Do you wanna play again? Type Yes or No\n").lower() == 'yes'

main()