# import cv2
# import face_recognition
# import os

# # Folder to store captured faces
# path = 'face_recognition_app/student_faces'
# if not os.path.exists(path):
#     os.makedirs(path)

# video = cv2.VideoCapture(0)
# student_name = input("Enter student name: ")

# while True:
#     ret, frame = video.read()
#     cv2.imshow("Capture Face", frame)

#     if cv2.waitKey(1) & 0xFF == ord('c'):
#         file_path = os.path.join(path, f"{student_name}.jpg")
#         cv2.imwrite(file_path, frame)
#         print(f"Face captured for {student_name}")
#         break

# video.release()
# cv2.destroyAllWindows()