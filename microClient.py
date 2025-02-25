import zmq
import json


def micro_client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Send JSON of email request info
    email_data = {"name": "Mike Fisher",
                  "email": "fishemic@oregonstate.edu",
                  "type": "paystub"}
    json_data = json.dumps(email_data)
    print("Client is sending email request info")
    socket.send_json(json_data)

    # Receive confirmation of email data delivery
    message = socket.recv()
    print(f"Received reply: {message.decode()}")

    print("Client is sending a file...")
    with open("paystub.pdf", "rb") as f:
        data = f.read()
        socket.send(data)

    # Receive reply from server
    message = socket.recv()
    print(f"Received reply: {message.decode()}")

    # End server
    socket.send(b"Q")

    socket.close()
    context.term()

    return


if __name__ == '__main__':
    micro_client()
