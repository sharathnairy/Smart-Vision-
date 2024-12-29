import cv2
import numpy as np
import mediapipe as mp

def inFrame(lst):
    # Ensure that key landmarks are visible to confirm the person is within the frame
    if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility > 0.6 and lst[16].visibility > 0.6:
        return True 
    return False

cap = cv2.VideoCapture(0)
holistic = mp.solutions.pose
holis = holistic.Pose()
drawing = mp.solutions.drawing_utils

X = []  # List to store pose data
y = []  # List to store labels
data_size = 0
label = "fighting"  # Set label to 'fighting' for all data points

print("Label is automatically set to 'fighting' for all data points.")

while True:
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
    lst = []

    if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
        # Capture pose landmarks
        for i in res.pose_landmarks.landmark:
            lst.append(i.x - res.pose_landmarks.landmark[0].x)
            lst.append(i.y - res.pose_landmarks.landmark[0].y)

        X.append(lst)

        # Automatically append the 'fighting' label for each data point
        y.append(label)

        data_size += 1
        cv2.putText(frm, str(data_size), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frm, "Make Sure Full body visible", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    drawing.draw_landmarks(frm, res.pose_landmarks, holistic.POSE_CONNECTIONS)
    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27 or data_size > 100:  # Stop after 100 frames or if Esc is pressed
        # Save data with the 'fighting' label
        np.save("pose_data.npy", np.array(X))
        np.save("pose_labels.npy", np.array(y))
        print("Data and labels saved.")
        break

cap.release()
cv2.destroyAllWindows()
