# Number plate detection and OCR

import cv2
import pytesseract
from datetime import datetime
from eimage import SendMail
import threading


def numplate():
    frameWidth = 640
    frameHeight = 480
    count=0

    # pre-trained number plate detection Cascade classifier
    numberPlateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

    # OCR of the vehicle number plate
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    # Turning on the camera
    cap = cv2.VideoCapture(0)

    # adjusting the output video features
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, 150)

    while True:
        success, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # finding the number plates in each frame
        numberPlates = numberPlateCascade.detectMultiScale(imgGray, 1.1, 4)
        
        for i, (x,y,w,h) in enumerate(numberPlates, 1):
            imgRoi = img[y:y+h, x:x+w] # region of interest
            imgRoi = cv2.resize(imgRoi, (150,50))
            time = datetime.now().strftime("%H-%M-%S")
            
            # saving the number plate photos
            cv2.imwrite("Scanned/NumPlate_"+str(time)+"_"+str(i)+".jpg", imgRoi)
            cv2.imshow("Plate", imgRoi)

            if count==0:
                count=1
                msgcontent = datetime.now().strftime('Date: %#d-%#m-%#y\nTime: %H-%M-%S')
                #SendMail(f"Scanned/NumPlate_"+str(time)+"_"+str(i)+".jpg", msgcontent)
                threading.Thread(target=SendMail, args=(f"Scanned/NumPlate_"+str(time)+"_"+str(i)+".jpg", msgcontent, )).start()
            
            #imgRoi = cv2.cvtColor(imgRoi, cv2.COLOR_BGR2GRAY)
            #imgRoi = cv2.threshold(imgRoi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # OCR of the number plate
            number = pytesseract.image_to_string(imgRoi)
            string = ""
            for ch in number:
                if (ch>='A' and ch<='Z') or (ch>='0' and ch<='9'):
                    string = string+ch
                    
            if len(string)!=0:
                # saving the number in the csv file
                with open("NumberPlate.csv", "a+") as f:
                    time = datetime.now().strftime("%#d-%#m-%#y, %H:%M:%S")
                    f.write(f"\n{string},{time}")
        
        # drawing the boxes around the number plate on the output screen
        for (x,y,w,h) in numberPlates:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 2)
        
        cv2.imshow("Output", img)

        #Send notification mail
        #count=1
        #msgcontent = datetime.now().strftime('Date: %#d-%#m-%#y\nTime: %H-%M-%S')
        #SendMail(f"Scanned/NumPlate_"+str(time)+"_"+str(i)+".jpg", msgcontent)
        
        # press 'esc' to exit
        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            break
