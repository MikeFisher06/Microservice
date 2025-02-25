import smtplib
import zmq
import json
import os

from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()


def email_notification():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Server is running...")

    # Receive JSON email request
    email_request = socket.recv_json()
    email_data = json.loads(email_request)
    # Acknowledge receipt
    socket.send(b"Received email data")

    # Wait for file from client
    message = socket.recv()
    print("Receiving file...")
    # Send reply back to client
    socket.send(b"File received successfully")
    print("File received successfully")

    # Close socket when done
    if message == b'Q':
        print("Closing socket connectione")
        context.destroy()
        return

    # Create file to attach to email
    file_name = f"{email_data['name']}_{email_data['type']}.pdf"
    with open(file_name, "wb") as f:
        f.write(message)

    # Compose and send email

    # Create SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # Start TLS for security
    s.starttls()

    # Authentication
    my_email = os.getenv("EMAIL_ADDRESS")
    app_password = os.getenv("APP_PASSWORD")
    s.login(my_email, app_password)

    msg = EmailMessage()
    msg['Subject'] = f"{email_data["name"]} {email_data["type"]}"
    msg['From'] = my_email
    msg['To'] = f"{email_data["email"]}"

    with open(file_name, "rb") as f:
        file_data = f.read()

    msg.add_attachment(file_data, maintype='application',
                       subtype='pdf',
                       filename=file_name)
    s.send_message(msg)
    s.quit()


if __name__ == '__main__':
    email_notification()
