import cv2
from deepface import DeepFace
import os
import time

face_db_path = "faces"

cap = cv2.VideoCapture(0)

print("🔍 Starting recognition...")

marked = set()            # ✅ already marked students
last_mark_time = {}       # ⏱ cooldown tracking
COOLDOWN = 10             # seconds

status_text = ""          # for "Marked" display

while True:
    ret, frame = cap.read()

    name_to_show = "Unknown"

    try:
        for file in os.listdir(face_db_path):
            path = os.path.join(face_db_path, file)

            result = DeepFace.verify(path, frame, enforce_detection=True)

            if result["verified"]:
                name = file.split(".")[0]
                name_to_show = name

                current_time = time.time()

                # ✅ Cooldown check
                if name not in last_mark_time or (current_time - last_mark_time[name]) > COOLDOWN:

                    print("✅ Recognized:", name)

                    # ✅ Attendance mark (only once per session)
                    if name not in marked:
                        print("🎯 Attendance Marked:", name)
                        marked.add(name)
                        status_text = "Marked"

                    last_mark_time[name] = current_time

                break

    except Exception as e:
        print("Error:", e)

    # 🔥 Show name on screen
    cv2.putText(frame, f"Name: {name_to_show}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    # 🔥 Show "Marked" status
    cv2.putText(frame, status_text,
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    cv2.imshow("Face Attendance", frame)

    # ESC key to exit
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()