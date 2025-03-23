import socket

HOST = "0.0.0.0"  # will be replaced with raspberry pi server 
PORT = 6000
portS = 6001

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("".encode(), (HOST, PORT))# this is for server to know client ip address 

print(f"Listening for data from {HOST}:{PORT}...")

try:

    while True:
        data, addr = client.recvfrom(1024)  
        print(f"Received from {addr}: {data.decode()}")
        
        ack_message = "Roger that :)" #Acknowledge message
        client.sendto(ack_message.encode(), (HOST, PORT))


except KeyboardInterrupt:
    print("Client Server is shutting down... Sending signal to server to also shutdown")
    clientS.sendto("STOP".encode(), (HOST, portS))
    clientS.close()
    client.close()
    print("\n Client closed... server alerted to Stop. Bye :)")