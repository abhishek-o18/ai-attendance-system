import cv2
import os

# folder create if not exists
if not os.path.exists("faces"):
    os.makedirs("faces")

cap = cv2.VideoCapture(0)

# student roll number input
roll_number = input("Enter Roll Number: ")

print("Press 's' to save image, 'q' to quit")

while True:
    ret, frame = cap.read()

    cv2.imshow("Capture Face", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):  # press s to save
        file_path = f"faces/{roll_number}.jpg"
        cv2.imwrite(file_path, frame)
        print(f"Image saved as {file_path} ✅")

    elif key == ord('q'):  # press q to quit
        break

cap.release()
cv2.destroyAllWindows()