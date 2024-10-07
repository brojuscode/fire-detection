import streamlit as st

from email.message import EmailMessage
import os
import cv2         # Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib     # Library for email sending
import ssl
from email.message import EmailMessage

import numpy as np

a=0
b=0
def send_mail(temp,levels):
    a=temp
    b=levels
    email_sender = 'fireforest989@gmail.com'
    email_password = 'uifoemttwoftgyrb'
    email_receiver = 'shishirhebbar74799@gmail.com'
    subject = 'EMERGENCY'
    body = """"
    Co2 levels of %d ppm and temperature of %d degree celsius is found at coordinates ()
    Drones are to be deployed to the affected region for visual confirmation.
    """%(b,a)
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())



st.title("FOREST FIRE DETECTION AND ANIMAL RESCUE ")
st.subheader(
    "Automating fire detection at early stage and preventing wildlife casualities ")
st.subheader("CO2 level detector")

number = st.number_input('C02 Level')
st.write('The current number is ', number)

number1 = st.number_input('Temperature')
st.write('The current number is ', number1)


if(number>1000):
    a=1
    st.write('Co2 levels are high')
if(number1>100):
    b=1
    st.write('Temperature levels are high')
if(a==1 and b==1):
    st.write('Drones need to be deployed ,Danger levels are high')
    send_mail(number1,number)

if(a==1 and b==0 or b==1 and a==0):
    st.write('Danger levels are moderate')
if(a==1 and b==1):
	 # To access xml file which includes positive and negative images of fire. (Trained images)
	fire_cascade = cv2.CascadeClassifier('C:\\Users\\Hp\\Documents\\git\\Fire_detection_python_project-main\\Fire_detection_python_project_git\\fire_detection_cascade_model.xml')
	# File is also provided with the code.

# To start camera this command is used "0" for laptop inbuilt camera and "1" for USB attahed camera
	vid = cv2.VideoCapture(0)
	runOnce = False  # created boolean


	def play_alarm_sound_function():  # defined function to play alarm post fire detection using threading
    # to play alarm # mp3 audio file is also provided with the code.
    		playsound.playsound('fire_alarm.mp3', True)
    		print("Fire alarm end")  # to print in consol


	def send_mail_function():
   
    		email_sender = 'fireforest989@gmail.com'
    		email_password = 'uifoemttwoftgyrb'
    		email_receiver = 'shishirhebbar74799@gmail.com'
    		subject = 'EMERGENCY'
    		body = """"
    		TEST FIRE EMAIL
    		"""
    		em = EmailMessage()
    		em['From'] = email_sender
    		em['To'] = email_receiver
    		em['Subject'] = subject
    		em.set_content(body)
    		context=ssl.create_default_context()
    		with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        		smtp.login(email_sender, email_password)
        		smtp.sendmail(email_sender, email_receiver, em.as_string())

	while (True):
    		Alarm_Status = False
    		ret, frame = vid.read()  # Value in ret is True # To read video frame
    # To convert frame into gray color
    		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    		fire = fire_cascade.detectMultiScale(
        		frame, 1.2, 5)  # to provide frame resolution

    # to highlight fire with square
    		for (x, y, w, h) in fire:
        		cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
        		roi_gray = gray[y:y+h, x:x+w]
        		roi_color = frame[y:y+h, x:x+w]

        		print("Fire alarm initiated")
        # To call alarm thread
        		threading.Thread(target=play_alarm_sound_function).start()

        		if runOnce == False:
            			print("Mail send initiated")
            # To call alarm thread
            			threading.Thread(target=send_mail_function).start()
            			runOnce = True
        		if runOnce == True:
            			print("Mail is already sent once")
            			runOnce = True

    		cv2.imshow('frame', frame)
    		if cv2.waitKey(1) & 0xFF == ord('q'):
       			break
