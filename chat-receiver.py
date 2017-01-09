import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 54321

sock.connect((host, port))



while True:
  # If message is over 1024 bytes long, it will be broken into parts.
  message = sock.recv(1024)
  print(message)
