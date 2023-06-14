import cv2
import os
import numpy as np
import tkinter as tk
import tkinter.font as font
import face_recognition
from datetime import datetime
from eimage import SendMail

import winsound
import threading

alarm_mode = True

def alarm():
    for _ in range(10):
        if not alarm_mode:
            break
        winsound.Beep(2500,1000)

def collect_data(device_num=0, dir_path='data/temp', ext='jpg', delay=1, window_name='frame'):
    name = input("Enter name of person : ")
    cap = cv2.VideoCapture(device_num)
    
    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, name)

    n = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('c'):
            cv2.imwrite('{}.{}'.format(base_path, ext), frame)
            n += 1
        elif key == ord('q'):
            break

    cv2.destroyWindow(window_name)





def identify():
    global alarm_mode
    alarm_mode = True
    count=0
    fname=""
    video_capture = cv2.VideoCapture(0)
    my_dir = 'data/temp/' # Folder where all your image files reside. Ensure it ends with '/
    encoding_for_file = [] # Create an empty list for saving encoded files
    known_face_encodings=[]
    known_face_names =[]
    for i in os.listdir(my_dir): # Loop over the folder to list individual files
        image = my_dir + i
        image = face_recognition.load_image_file(image) # Run your load command
        image_encoding = face_recognition.face_encodings(image) # Run your encoding command
        known_face_encodings.append(image_encoding[0]) # Append the results to encoding_for_file list
        known_face_names.append(i.rsplit('.', maxsplit=1)[0])
# Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    right, left = "", ""

    while True:
    # Grab a single frame of video
        ret, frame = video_capture.read()

        
        _, frame2 = video_capture.read()
        #visitor detection start
        diff = cv2.absdiff(frame2, frame)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        diff = cv2.blur(diff, (5,5))
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        contr, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        x = 300
        if len(contr) > 0:
            max_cnt = max(contr, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(max_cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, "MOTION", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)
            
        
        if right == "" and left == "":
            if x > 500:
                right = True
            
            elif x < 200:
                left = True
                
        elif right:
                if x < 200:
                    print("to left")
                    x = 300
                    right, left = "", ""
                    cv2.imwrite(f"visitors/in/{datetime.now().strftime('%#y-%#m-%#d-%H-%M-%S')}.jpg", frame)
            
        elif left:
                if x > 500:
                    print("to right")
                    x = 300
                    right, left = "", ""
                    cv2.imwrite(f"visitors/out/{datetime.now().strftime('%#y-%#m-%#d-%H-%M-%S')}.jpg", frame)
        #visitor detection end
    # Only process every other frame of video to save time
        if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


    # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
           top *= 4
           right *= 4
           bottom *= 4
           left *= 4

        # Draw a box around the face
           cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
           cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
           font = cv2.FONT_HERSHEY_DUPLEX
           cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
           fname=name
    # Display the resulting image
        cv2.imshow('Video', frame)

    # Save frames with unknown visitors and send mail notification
        
        msgcontent = datetime.now().strftime('Date: %#d-%#m-%#y\nTime: %H-%M-%S')
        if count==0 and fname=="Unknown":
            count=1
            cv2.imwrite(f"data/stored/{datetime.now().strftime('%#y-%#m-%#d-%H-%M-%S')}.jpg", frame)
            #SendMail(f"data/stored/{datetime.now().strftime('%#y-%#m-%#d-%H-%M-%S')}.jpg", msgcontent)
            threading.Thread(target=SendMail, args=(f"data/stored/{datetime.now().strftime('%#y-%#m-%#d-%H-%M-%S')}.jpg", msgcontent, )).start()
            #alarm function called
            threading.Thread(target=alarm).start()
        elif fname!="Unknown":
            count=0
    # Hit 't' on the keyboard to toggle alarm mode!
        if cv2.waitKey(30) == ord('t'):
            alarm_mode = not alarm_mode
    # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

# Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

def maincall():


	root = tk.Tk()

	root.geometry("480x100")
	root.title("identify")

	label = tk.Label(root, text="Select below buttons ")
	label.grid(row=0, columnspan=2)
	label_font = font.Font(size=35, weight='bold',family='Helvetica')
	label['font'] = label_font

	btn_font = font.Font(size=25)

	button1 = tk.Button(root, text="Add Member ", command=collect_data, height=2, width=20)
	button1.grid(row=1, column=0, pady=(10,10), padx=(5,5))
	button1['font'] = btn_font

	button2 = tk.Button(root, text="Start with known ", command=identify, height=2, width=20)
	button2.grid(row=1, column=1,pady=(10,10), padx=(5,5))
	button2['font'] = btn_font
	root.mainloop()

	return


