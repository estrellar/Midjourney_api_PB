import cv2
import requests
import json
import time
import re
import argparse
import sys
from sender import Sender
from receiver import Receiver

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize the sender and receiver
sender = Sender('r_params.json')
receiver = Receiver('r_params.json', './images')

# Start the video feed
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('Video Feed', frame)

    # Check for user input
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # Capture the current frame
        cv2.imwrite('capture.jpg', frame)

        # Send the image to the Midjourney API
        with open('capture.jpg', 'rb') as f:
            img_data = f.read()
        
        #TODO invoke people detection
        #TODO get image url form listeningbot
        num_people = 1
        subject_url = 'https://cdn.discordapp.com/attachments/1132085427302567967/1132501217210273955/IMG_6335.jpeg'
        # Prepare the prompt for the API
        prompt = f'{subject_url} anime, hand-drawn and cel animation techniques, guests at party, {num_people} subject(s) in foreground, natural design, beautifully rendered and expressive rich colors, vibrant pastel colors,imaginative and fantastical landscapes, sharp attention to detail,realism and a strong sense of nostalgia and warmth, sharp attention to small details and textures,fantastical creatures, settings, depth and emotions emphasized and accentuated by lighting and shading,extremely high quality, incredibly high finite definition, high resolution, hand-drawn and cel animation techniques, anime'

        # Send the prompt to the API
        sender.send(prompt)

        # Wait for the image to be generated and downloaded
        while True:
            receiver.main()
            if prompt in receiver.df['prompt'].values:
                break
            time.sleep(5)

        print('Image generated and downloaded!')

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()