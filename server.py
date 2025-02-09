import socket
import hashlib
import os
import random

CHUNK_SIZE = 1024  # Fixed chunk size

def calculate_checksum(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

def split_file(file_path):
    chunks = []
    with open(file_path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            chunks.append(chunk)
    return chunks

def simulate_errors(chunks):
    # Simulate packet loss (drop 10% of chunks)
    if random.random() < 0.1:
        index = random.randint(0, len(chunks) - 1)
        print(f"Simulating packet loss: Dropping chunk {index}")
        del chunks[index]

    # Simulate packet corruption (modify 10% of chunks)
    if random.random() < 0.1:
        index = random.randint(0, len(chunks) - 1)
        print(f"Simulating packet corruption: Corrupting chunk {index}")
        chunks[index] = b"corrupted_data"

    # Simulate out-of-order delivery
    random.shuffle(chunks)
    print("Simulating out-of-order delivery.")

    return chunks

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(1)
    print("Server listening on port 12345...")

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    # Receive file name and size
    file_name = client_socket.recv(1024).decode()
    file_size = int(client_socket.recv(1024).decode())
    print(f"Receiving file: {file_name} ({file_size} bytes)")

    # Receive file data
    file_path = f"received_{file_name}"
    with open(file_path, "wb") as f:
        while file_size > 0:
            chunk = client_socket.recv(CHUNK_SIZE)
            f.write(chunk)
            file_size -= len(chunk)
    print("File received successfully.")

    # Calculate checksum
    checksum = calculate_checksum(file_path)
    print(f"Checksum: {checksum}")

    # Split file into chunks
    chunks = split_file(file_path)
    print(f"File split into {len(chunks)} chunks.")

    # Simulate errors
    chunks = simulate_errors(chunks)

    # Send checksum and chunks to client
    client_socket.send(checksum.encode())
    for i, chunk in enumerate(chunks):
        client_socket.send(f"{i}:".encode() + chunk)  # Tag chunk with sequence number
    print("Chunks sent to client.")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()