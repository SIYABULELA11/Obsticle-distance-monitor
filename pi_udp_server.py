import socket
import time
import pi  # Importing the sensor module which we was modified after originally got from below url
#https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi?srsltid=AfmBOooBbwPBw2HpgeUywNQIZwbgYTYj3TNNs5LYm3SivR8NJW2NVrKP


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # server config
stop_com = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket for receiving stop command

ip = "0.0.0.0"  # will be replaced with raspberry pi ip address
portS = 6001
port = 6000
server.bind((ip,port))
stop_com.bind((ip,portS))  

print(f"UDP server running using  ")

blank_message, address = server.recvfrom(1024) # this is to get the address of client


print("Sending sensor data to computer...")

stop_com.settimeout(1)  # will prevent recvfrom from blocking other operations

try:
  while True:
      distance = pi.get_distance()  # Calling the function that calculates distance from pi.py

      if distance == -1:
          data = "Error: Sensor timeout"
      else:
          data = f"Distance detected: {distance} cm"
      
      server.sendto(data.encode(), address)  # sending distance detected
      print(f"Sent to client: {data}")

      # To Send warning or approval message based on the distance detected 
      if distance < 50:
          wmsg = "Too close to obstacle! Avoid collision!!!"
          server.sendto(wmsg.encode(), address)
          print(f"Sent warning: {wmsg}")

      else:
          amsg = "Good safe distance from obstacle :)"
          server.sendto(amsg.encode(), address)
          print(f"Sent approval: {amsg}")

      
    
      try:
          msg, addr = stop_com.recvfrom(1024)
          if msg.decode().strip() == "STOP":
              print("STOP command received. Shutting down :( ")
              break
      except socket.timeout:
          pass # continues loop

      time.sleep(2)  # Send an update every 2 seconds 
except KeyboardInterrupt:
    server.sendto("Server Shutting Down. Bye:)".encode(), address)
    print("Server interrupted. Shutting down...")
    print("Server sockets closed")
    server.close()
    stop_com.close()

server.close()
stop_com.close()