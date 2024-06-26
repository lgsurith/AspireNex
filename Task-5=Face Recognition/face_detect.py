import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#functinality to handle faces by frame rate.
def detect_faces(frame, haar_cascade):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces_rect = haar_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
    
    for (x,y,w,h) in faces_rect:
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), thickness=2)
    
    return frame

#functionality to process image1

def process_image(image_path, haar_cascade):
    img = cv.imread(image_path)
    down_width, down_height = 1400 , 900
    resized_down = cv.resize(img, (down_width, down_height), interpolation=cv.INTER_LINEAR)
    
    result = detect_faces(resized_down, haar_cascade)
    cv.imshow('Detected Face/Faces', result)
    cv.waitKey(0)
    cv.destroyAllWindows()

#functionality to process video
def process_video(video_path, haar_cascade):
    vid_cap = cv.VideoCapture(video_path)
    
    while True:
        success, frame = vid_cap.read()
        if not success:
            break
        
        result = detect_faces(frame, haar_cascade)
        cv.imshow('Detected Face/Faces', result)
        
        if cv.waitKey(1) & 0xFF == ord('k'):
            break
    
    vid_cap.release()
    cv.destroyAllWindows()

#functionality to process webcam - make sure to add your video port properly to access webcam.3

def process_webcam(haar_cascade):
    vid_cap = cv.VideoCapture(0)
    
    while True:
        success, frame = vid_cap.read()
        if not success:
            break
        
        result = detect_faces(frame, haar_cascade)
        cv.imshow('Detected Face/Faces', result)
        
        if cv.waitKey(1) & 0xFF == ord('k'):
            break
    
    vid_cap.release()
    cv.destroyAllWindows()

def main():
    haar_cascade = cv.CascadeClassifier('Task-5=Face Recognition/haar_face.xml')

    while True:
        print("\nChoose an option:")
        print("1. Process an image")
        print("2. Process a video")
        print("3. Use webcam")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            image_path = "Task-5=Face Recognition/face.jpg"
            process_image(image_path, haar_cascade)
        elif choice == '2':
            video_path = "Task-5=Face Recognition/face.mp4"
            process_video(video_path, haar_cascade)
        elif choice == '3':
            process_webcam(haar_cascade)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice :( ,  Please try again.")

if __name__ == "__main__":
    main()