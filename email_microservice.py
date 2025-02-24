import smtplib
import zmq
import time
import json

from email.message import EmailMessage


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
    with open("received_paystub.pdf", "wb") as f:
        f.write(message)

    # Sleep
    time.sleep(3)

    # Compose and send email

    # Create SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # Start TLS for security
    s.starttls()

    # Authentication
    s.login("evoskate@gmail.com", "udli wwpe llqj mvdk")

    msg = EmailMessage()
    msg['Subject'] = f"{email_data["name"]} {email_data["type"]}"
    msg['From'] = 'evoskate@gmail.com'
    msg['To'] = f"{email_data["email"]}"

    with open("received_paystub.pdf", "rb") as f:
        file_data = f.read()

    msg.add_attachment(file_data, maintype='application',
                       subtype='pdf',
                       filename="received_paystub.pdf")
    s.send_message(msg)


if __name__ == '__main__':
    email_notification()
