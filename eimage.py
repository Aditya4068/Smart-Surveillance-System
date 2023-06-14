import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def SendMail(ImgFileName, msgcontent):
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'Alert! Suspicious Activity has been Detected'
    msg['From'] = 'adityasfox@gmail.com'
    msg['To'] = 'adityasfox@gmail.com'

    text = MIMEText(msgcontent)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("adityasfox@gmail.com", "pzktvilvkkrmiboq")
    s.sendmail("adityasfox@gmail.com", "adityasfox@gmail.com", msg.as_string())
    print("Mail Sent!")
    s.quit()

