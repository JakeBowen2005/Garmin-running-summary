import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

my_email = "jakeeb05@gmail.com"
# password = "Baller05$"
password = "jsyvqmqwkfxilewg"

def send_email(user_email):
    #Creating the message
    msg = MIMEMultipart()
    msg["From"] = my_email
    msg["To"] = user_email
    msg["Subject"] = "Your Garmin running Summary Visuals"

    #Email body
    body = "Here are your running summary visuals from your Garmin data project."
    msg.attach(MIMEText(body, "plain"))

    #Folder where all the users visuals are saved
    visuals_folder = "output/visuals"

    #Looping through all the pictures
    
    for filename in os.listdir(visuals_folder):
        if filename.endswith(".png"):
            file_path = os.path.join(visuals_folder, filename)
            with open(file_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())

            encoders.encode_base64(part)

            part.add_header("Content-Disposition",
                f"attachment; filename= {filename}")
            
            msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(my_email, password)
        server.send_message(msg)

    print("Success")